r"""Proofreading with Word tracked changes.

Two commands:

``make``
    Turn an article into a Word document in which each proposed typo fix is a real tracked change
    (deleted text struck through, inserted text underlined) with an explanatory comment, so Lynn can
    accept, reject or edit each one in Word::

        uv run python scripts/proof_docx.py make content/food-travel/the-wild-west fixes.json \\
            --out "~/Documents/Elseyworks/The Wild West - proposed corrections.docx"

    ``fixes.json`` is a list of ``{"find": "...", "replace": "...", "note": "..."}``. ``find`` is matched
    against the article's *plain* text (no markdown marks). It must appear exactly once unless
    ``"all": true`` is given. ``replace`` may be omitted/``null`` to add a comment without a change
    (for a query such as an unverifiable phone number).

``diff``
    Compare the article with the Word document after Lynn has finished (tracked changes accepted) and
    list every wording difference, so the accepted edits can be applied to the article::

        uv run python scripts/proof_docx.py diff content/food-travel/the-wild-west edited.docx
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

AUTHOR = "Claude"
INITIALS = "C"
_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_CAPTION = re.compile(r'caption="([^"]*)"')
_SHORTCODE = re.compile(r"^\s*\{\{<\s*(/?)\s*([a-z-]+)(.*?)>\}\}\s*$")
_INLINE = [
    ("bold", re.compile(r"\*\*(.+?)\*\*", re.DOTALL)),
    ("bold", re.compile(r"(?<!\w)__(.+?)__(?!\w)", re.DOTALL)),
    ("italic", re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", re.DOTALL)),
    ("italic", re.compile(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", re.DOTALL)),
    ("link", re.compile(r"\[([^\]]+)\]\([^)]*\)")),
]
_BR = re.compile(r"\s*<br\s*/?>\s*", re.IGNORECASE)
_TAG = re.compile(r"</?[a-zA-Z][^>]*>")


@dataclass(frozen=True)
class Run:
    """A stretch of text with one formatting.

    Attributes:
        text: The text (may contain newlines for line breaks).
        bold: Bold formatting.
        italic: Italic formatting.
    """

    text: str
    bold: bool = False
    italic: bool = False


@dataclass
class Para:
    """One paragraph of the article.

    Attributes:
        style: Word paragraph style id (e.g. ``BodyText``, ``Heading2``, ``BlockText``).
        runs: The formatted text runs.
    """

    style: str
    runs: list[Run] = field(default_factory=list)

    @property
    def text(self) -> str:
        """The paragraph's plain text."""
        return "".join(r.text for r in self.runs)


@dataclass(frozen=True)
class Fix:
    """A proposed correction.

    Attributes:
        find: Plain text to find.
        replace: Replacement text, or ``None`` for a comment-only query.
        note: Explanation shown as a Word comment.
        all: Apply to every occurrence rather than requiring exactly one.
    """

    find: str
    replace: str | None
    note: str = ""
    all: bool = False


def parse_inline(text: str, *, bold: bool = False, italic: bool = False) -> list[Run]:
    """Parse the inline markdown of one paragraph into formatted runs.

    Args:
        text: Paragraph text with markdown marks, ``<br>`` and stray HTML.
        bold: Inherited bold state.
        italic: Inherited italic state.

    Returns:
        The runs, with marks removed and ``<br>`` turned into newlines.
    """
    best: tuple[int, str, re.Match[str]] | None = None
    for kind, pattern in _INLINE:
        match = pattern.search(text)
        if match and (best is None or match.start() < best[0]):
            best = (match.start(), kind, match)
    if best is None:
        plain = re.sub(r"\\([\\`*_{}\[\]()#+.!-])", r"\1", _TAG.sub("", _BR.sub("\n", text)))
        return [Run(plain, bold, italic)] if plain else []
    _, kind, match = best
    inner_bold = bold or kind == "bold"
    inner_italic = italic or kind == "italic"
    return (
        parse_inline(text[: match.start()], bold=bold, italic=italic)
        + parse_inline(match.group(1), bold=inner_bold, italic=inner_italic)
        + parse_inline(text[match.end():], bold=bold, italic=italic)
    )


def parse_article(text: str) -> tuple[str, list[Para]]:
    """Read an article's ``index.md`` into a title and paragraphs.

    Site shortcodes are simplified: ``lead`` and ``callout`` content becomes ordinary paragraphs,
    picture captions become ``[Picture caption: ...]`` paragraphs, and layout-only shortcodes are dropped.

    Args:
        text: The full text of ``index.md``.

    Returns:
        The article title and its paragraphs in reading order.
    """
    title = ""
    match = _FRONT.match(text)
    if match:
        found = re.search(r"^title:\s*(.+)$", match.group(1), re.MULTILINE)
        if found:
            title = found.group(1).strip().strip("\"'")
        text = text[match.end():]

    paras: list[Para] = []
    buffer: list[str] = []
    base = "BodyText"   # style outside quotes: BlockText inside a callout
    style = base
    italic_block = False

    def flush() -> None:
        nonlocal buffer, style
        if buffer:
            runs = parse_inline(" ".join(part.strip() for part in buffer))
            if italic_block:
                runs = [Run(r.text, r.bold, True) for r in runs]
            if runs:
                paras.append(Para(style, runs))
        buffer = []
        style = base

    for raw in text.splitlines():
        line = raw.rstrip()
        code = _SHORTCODE.match(line)
        if code:
            flush()
            closing, name, args = code.groups()
            if name in {"lead", "callout"}:
                italic_block = name == "lead" and not closing
                base = "BodyText" if closing or name == "lead" else "BlockText"
                style = base
            elif name.startswith("img") and (cap := _CAPTION.search(args)) and cap.group(1).strip():
                paras.append(Para("BodyText", [Run(f"[Picture caption: {cap.group(1)}]", italic=True)]))
            continue
        if not line.strip():
            flush()
            continue
        if line.lstrip().startswith(("<img", "<figure", "</figure", "<!--")):
            flush()
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush()
            paras.append(Para(f"Heading{min(len(heading.group(1)), 3)}", parse_inline(heading.group(2))))
            continue
        if line.lstrip().startswith(">"):
            quoted = line.lstrip()[1:].strip()
            if style != "BlockText":
                flush()
                style = "BlockText"
            if quoted:
                buffer.append(quoted)
            else:
                flush()
            continue
        buffer.append(line)
    flush()
    return title, paras


def load_fixes(path: Path) -> list[Fix]:
    """Load proposed corrections from a JSON file.

    Args:
        path: The JSON file.

    Returns:
        The fixes.

    Raises:
        ValueError: If an entry is malformed.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    fixes = []
    for entry in data:
        if not isinstance(entry, dict) or not entry.get("find"):
            msg = f"Each fix needs a 'find' text: {entry!r}"
            raise ValueError(msg)
        fixes.append(Fix(entry["find"], entry.get("replace"), entry.get("note", ""), bool(entry.get("all"))))
    return fixes


@dataclass
class _Edit:
    start: int
    end: int
    new: str | None
    note: str


def locate_edits(paras: list[Para], fixes: list[Fix]) -> dict[int, list[_Edit]]:
    """Work out where each fix applies.

    Args:
        paras: The article paragraphs.
        fixes: The proposed corrections.

    Returns:
        Edits keyed by paragraph index, sorted by position.

    Raises:
        ValueError: If a fix's text is missing, ambiguous or overlaps another fix.
    """
    edits: dict[int, list[_Edit]] = {}
    for fix in fixes:
        hits = [(i, m.start()) for i, p in enumerate(paras) for m in re.finditer(re.escape(fix.find), p.text)]
        if not hits:
            msg = f"Could not find the text {fix.find!r} in the article."
            raise ValueError(msg)
        if len(hits) > 1 and not fix.all:
            msg = f"The text {fix.find!r} appears {len(hits)} times; use a longer 'find' or set \"all\": true."
            raise ValueError(msg)
        for index, start in hits:
            edits.setdefault(index, []).append(_Edit(start, start + len(fix.find), fix.replace, fix.note))
    for index, items in edits.items():
        items.sort(key=lambda e: e.start)
        for first, second in zip(items, items[1:], strict=False):
            if second.start < first.end:
                msg = f"Two fixes overlap in the paragraph beginning {paras[index].text[:40]!r}."
                raise ValueError(msg)
    return edits


def _rpr(run: Run) -> str:
    props = ("<w:b/>" if run.bold else "") + ("<w:i/>" if run.italic else "")
    return f"<w:rPr>{props}</w:rPr>" if props else ""


def _text_xml(text: str, tag: str) -> str:
    """Build the XML for text, turning newlines into Word line breaks."""
    parts = text.split("\n")
    out = []
    for i, part in enumerate(parts):
        if i:
            out.append("<w:br/>")
        if part:
            out.append(f'<{tag} xml:space="preserve">{escape(part)}</{tag}>')
    return "".join(out)


def _slice_runs(runs: list[Run], start: int, end: int) -> list[Run]:
    """Return the part of ``runs`` between two character offsets, keeping formatting."""
    out, pos = [], 0
    for run in runs:
        lo, hi = max(start, pos), min(end, pos + len(run.text))
        if lo < hi:
            out.append(Run(run.text[lo - pos: hi - pos], run.bold, run.italic))
        pos += len(run.text)
    return out


class _Ids:
    """Hands out unique ids for tracked changes and comments."""

    def __init__(self) -> None:
        self.change = 100
        self.comments: list[str] = []

    def next_change(self) -> int:
        self.change += 1
        return self.change


def render_paragraph(para: Para, edits: list[_Edit], ids: _Ids, stamp: str) -> str:
    """Render one paragraph as WordprocessingML, with tracked changes for its edits.

    Args:
        para: The paragraph.
        edits: Edits in this paragraph, sorted by position.
        ids: Id generator shared across the document.
        stamp: ISO timestamp for the changes.

    Returns:
        The ``<w:p>`` XML.
    """
    def plain_runs(runs: list[Run]) -> str:
        return "".join(f"<w:r>{_rpr(r)}{_text_xml(r.text, 'w:t')}</w:r>" for r in runs)

    body, pos = [], 0
    for edit in edits:
        body.append(plain_runs(_slice_runs(para.runs, pos, edit.start)))
        removed = _slice_runs(para.runs, edit.start, edit.end)
        comment_id = None
        if edit.note:
            comment_id = len(ids.comments)
            ids.comments.append(edit.note)
            body.append(f'<w:commentRangeStart w:id="{comment_id}"/>')
        if edit.new is None:
            body.append(plain_runs(removed))
        else:
            fmt = removed[0] if removed else Run("")
            attrs = f'w:author="{AUTHOR}" w:date="{stamp}"'
            deleted = "".join(f"<w:r>{_rpr(r)}{_text_xml(r.text, 'w:delText')}</w:r>" for r in removed)
            body.append(f'<w:del w:id="{ids.next_change()}" {attrs}>{deleted}</w:del>')
            if edit.new:
                inserted = f"<w:r>{_rpr(fmt)}{_text_xml(edit.new, 'w:t')}</w:r>"
                body.append(f'<w:ins w:id="{ids.next_change()}" {attrs}>{inserted}</w:ins>')
        if comment_id is not None:
            body.append(f'<w:commentRangeEnd w:id="{comment_id}"/>'
                        f'<w:r><w:commentReference w:id="{comment_id}"/></w:r>')
        pos = edit.end
    body.append(plain_runs(_slice_runs(para.runs, pos, len(para.text))))
    return f'<w:p><w:pPr><w:pStyle w:val="{para.style}"/></w:pPr>{"".join(body)}</w:p>'


def _comments_xml(ids: _Ids, stamp: str) -> str:
    items = "".join(
        f'<w:comment w:id="{i}" w:author="{AUTHOR}" w:date="{stamp}" w:initials="{INITIALS}">'
        f'<w:p><w:r><w:t xml:space="preserve">{escape(note)}</w:t></w:r></w:p></w:comment>'
        for i, note in enumerate(ids.comments)
    )
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f"{items}</w:comments>")


def _pandoc(args: list[str], *, stdin: str | None = None) -> str:
    """Run pandoc.

    Raises:
        RuntimeError: If pandoc is missing or fails.
    """
    if shutil.which("pandoc") is None:
        msg = "pandoc is not installed (run scripts/setup.sh)"
        raise RuntimeError(msg)
    done = subprocess.run(["pandoc", *args], input=stdin, capture_output=True, text=True, check=False)  # ruff: ignore[subprocess-without-shell-equals-true, start-process-with-partial-path]
    if done.returncode != 0:
        msg = f"pandoc failed: {done.stderr.strip()[:300]}"
        raise RuntimeError(msg)
    return done.stdout


def build_docx(title: str, paras: list[Para], fixes: list[Fix], out: Path) -> int:
    """Write the Word document with tracked changes.

    Args:
        title: Article title (shown as the document title).
        paras: Article paragraphs.
        fixes: Proposed corrections.
        out: Where to save the ``.docx``.

    Returns:
        The number of fixes applied (occurrences).
    """
    edits = locate_edits(paras, fixes)
    stamp = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    ids = _Ids()
    with tempfile.TemporaryDirectory() as tmp:
        scaffold = Path(tmp) / "scaffold.docx"
        _pandoc(["-f", "markdown", "-o", str(scaffold)],
                stdin="---\ntitle: T\n---\n\n# A\n\n## B\n\n### C\n\n> quote\n\nText\n\nMore text\n")
        with zipfile.ZipFile(scaffold) as zin:
            files = {name: zin.read(name) for name in zin.namelist()}
        document = files["word/document.xml"].decode("utf-8")
        sect = re.search(r"<w:sectPr.*?</w:sectPr>", document, re.DOTALL)
        head = document[: document.index("<w:body>") + len("<w:body>")]
        title_para = Para("Title", [Run(title)])
        xml = "".join(render_paragraph(p, edits.get(i, []), ids, stamp) for i, p in enumerate(paras))
        files["word/document.xml"] = (
            head + render_paragraph(title_para, [], ids, stamp) + xml + (sect.group(0) if sect else "") + "</w:body></w:document>"
        ).encode("utf-8")
        files["word/comments.xml"] = _comments_xml(ids, stamp).encode("utf-8")
        types = files["[Content_Types].xml"].decode("utf-8")
        files["[Content_Types].xml"] = types.replace(
            "</Types>",
            '<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/></Types>',
        ).encode("utf-8")
        rels = files["word/_rels/document.xml.rels"].decode("utf-8")
        files["word/_rels/document.xml.rels"] = rels.replace(
            "</Relationships>",
            '<Relationship Id="rIdProofComments" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/></Relationships>',
        ).encode("utf-8")
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
            for name, data in files.items():
                zout.writestr(name, data)
    return sum(len(v) for v in edits.values())


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def docx_paragraphs(docx: Path) -> list[str]:
    """Read a Word file with all tracked changes accepted, as normalised paragraphs.

    Args:
        docx: The Word file.

    Returns:
        Paragraph texts (whitespace collapsed), excluding the title paragraph.
    """
    plain = _pandoc(["--track-changes=accept", "-t", "plain", "--wrap=none", str(docx)])
    return [_normalise(block) for block in re.split(r"\n\s*\n", plain) if block.strip()]


def diff_paragraphs(original: list[str], edited: list[str]) -> list[str]:
    """Describe the wording differences between two lists of paragraphs.

    Args:
        original: The article's paragraphs.
        edited: The paragraphs from Lynn's edited document.

    Returns:
        Human-readable lines, one per change.
    """
    lines: list[str] = []
    matcher = difflib.SequenceMatcher(None, original, edited, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            for old, new in zip(original[i1:i2], edited[j1:j2], strict=True):
                words_old, words_new = old.split(), new.split()
                sm = difflib.SequenceMatcher(None, words_old, words_new, autojunk=False)
                for wtag, a1, a2, b1, b2 in sm.get_opcodes():
                    if wtag == "equal":
                        continue
                    before = " ".join(words_old[max(0, a1 - 4): a1])
                    after = " ".join(words_old[a2: a2 + 4])
                    lines.append(f'CHANGE: "{" ".join(words_old[a1:a2])}" -> "{" ".join(words_new[b1:b2])}"'
                                 f'   (context: ...{before} [HERE] {after}...)')
            continue
        for old in original[i1:i2]:
            lines.append(f'PARAGRAPH REMOVED/MERGED: "{old[:90]}"')
        for new in edited[j1:j2]:
            lines.append(f'PARAGRAPH ADDED/CHANGED: "{new[:90]}"')
    return lines


def _article_index(path: Path) -> Path:
    return path / "index.md" if path.is_dir() else path


def main() -> int:
    """Command-line entry point.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("make", help="build a Word file with tracked changes")
    make.add_argument("article", type=Path)
    make.add_argument("fixes", type=Path)
    make.add_argument("--out", type=Path, required=True)
    cmp_ = sub.add_parser("diff", help="list wording differences in an edited Word file")
    cmp_.add_argument("article", type=Path)
    cmp_.add_argument("docx", type=Path)
    args = parser.parse_args()
    try:
        title, paras = parse_article(_article_index(args.article).read_text(encoding="utf-8"))
        if args.command == "make":
            out = args.out.expanduser()
            count = build_docx(title, paras, load_fixes(args.fixes), out)
            print(f"Wrote {out} with {count} proposed change(s).")
        else:
            original = [_normalise(p.text) for p in paras]
            edited = docx_paragraphs(args.docx.expanduser())
            if edited and _normalise(title) == edited[0]:
                edited = edited[1:]
            changes = diff_paragraphs(original, edited)
            print("\n".join(changes) if changes else "No wording differences.")
    except (RuntimeError, ValueError, OSError, json.JSONDecodeError) as err:
        print(f"Problem: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
