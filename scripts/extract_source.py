"""Unpack a source file (Word document or PDF) so an article can be prepared from it.

Usage::

    uv run python scripts/extract_source.py path/to/source.pdf [--out DIR]

Everything is written to a work folder outside the site (default
``/tmp/elseyworks-extract/<name>``) and a plain report is printed describing what was found:

* Word / OpenDocument / RTF: ``source.md`` (text with headings, bold, italics, lists, quotes)
  plus any embedded pictures in ``media/``.
* PDF: one ``page-N.jpg`` picture per page (read these to transcribe), ``page-N.txt`` with the
  PDF's own text layer (a cross-check only - in scanned magazines it is often poor OCR), and any
  photographs embedded in the PDF in ``images/``.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

WORD_TYPES = {".docx", ".odt", ".rtf", ".doc"}
TEXT_TYPES = {".txt", ".md"}
DEFAULT_OUT = Path(tempfile.gettempdir()) / "elseyworks-extract"
PAGE_LONG_SIDE = 1800
MIN_EMBEDDED_BYTES = 15_000
_SUSPECT = re.compile(r"[�­]|(?<=[a-z])[A-Z](?=[a-z]*\b)|\b[a-z]+[.,;:'][a-z]+\b")


@dataclass
class Extraction:
    """Result of unpacking a source file.

    Attributes:
        source: The original file.
        out_dir: Work folder holding the unpacked material.
        kind: One of ``word``, ``text``, ``pdf-text``, ``pdf-scanned``.
        pages: Number of pages (PDFs only).
        pictures: Picture files worth considering for the article.
        warnings: Plain-English notes for whoever prepares the article.
    """

    source: Path
    out_dir: Path
    kind: str
    pages: int = 0
    pictures: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def classify_text_layer(text: str, pages: int) -> str:
    """Decide whether a PDF has a usable text layer.

    Args:
        text: All text extracted from the PDF.
        pages: Number of pages in the PDF.

    Returns:
        ``"pdf-scanned"`` when there is effectively no text (pictures only),
        otherwise ``"pdf-text"``.
    """
    letters = sum(ch.isalpha() for ch in text)
    return "pdf-scanned" if letters < 200 * max(pages, 1) * 0.25 else "pdf-text"


def suspect_count(text: str) -> int:
    """Count tell-tale signs of poor OCR in a text layer.

    Args:
        text: Extracted text.

    Returns:
        Number of suspicious fragments (replacement characters, soft hyphens, odd mid-word capitals).
    """
    return len(_SUSPECT.findall(text))


def _run(cmd: list[str]) -> str:
    """Run a command and return its output.

    Args:
        cmd: The command and arguments.

    Returns:
        Standard output as text.

    Raises:
        RuntimeError: If the tool is missing or fails.
    """
    if shutil.which(cmd[0]) is None:
        msg = f"'{cmd[0]}' is not installed (run scripts/setup.sh)"
        raise RuntimeError(msg)
    done = subprocess.run(cmd, capture_output=True, text=True, check=False)  # ruff: ignore[subprocess-without-shell-equals-true]
    if done.returncode != 0:
        msg = f"{cmd[0]} failed: {done.stderr.strip()[:300]}"
        raise RuntimeError(msg)
    return done.stdout


def extract_word(source: Path, out_dir: Path) -> Extraction:
    """Convert a Word/OpenDocument/RTF file to markdown with pandoc.

    Args:
        source: The document.
        out_dir: Work folder.

    Returns:
        The extraction result.
    """
    result = Extraction(source, out_dir, "word")
    src = source
    if source.suffix.lower() == ".doc":
        _run(["textutil", "-convert", "docx", "-output", str(out_dir / "converted.docx"), str(source)])
        src = out_dir / "converted.docx"
    _run(["pandoc", str(src), "-t", "gfm", "--wrap=none", f"--extract-media={out_dir / 'media'}",
          "-o", str(out_dir / "source.md")])
    result.pictures = sorted(p for p in (out_dir / "media").rglob("*") if p.is_file())
    text = (out_dir / "source.md").read_text(encoding="utf-8")
    if not text.strip():
        result.warnings.append("No text was found in the document.")
    if "<table" in text or "|---" in text:
        result.warnings.append("The document contains a table - check it laid out properly.")
    return result


def extract_pdf(source: Path, out_dir: Path) -> Extraction:
    """Render a PDF's pages, pull out its text layer and embedded photographs.

    Args:
        source: The PDF.
        out_dir: Work folder.

    Returns:
        The extraction result.
    """
    info = _run(["pdfinfo", str(source)])
    match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
    pages = int(match.group(1)) if match else 0
    _run(["pdftoppm", "-jpeg", "-r", "110", "-scale-to", str(PAGE_LONG_SIDE), str(source), str(out_dir / "page")])
    # pdftoppm zero-pads numbers depending on page count; normalise to page-N.jpg
    for jpg in sorted(out_dir.glob("page-*.jpg")):
        number = int(jpg.stem.split("-")[1])
        jpg.rename(out_dir / f"page-{number}.jpg")
    all_text = []
    for number in range(1, pages + 1):
        text = _run(["pdftotext", "-f", str(number), "-l", str(number), str(source), "-"])
        (out_dir / f"page-{number}.txt").write_text(text, encoding="utf-8")
        all_text.append(text)
    joined = "\n".join(all_text)
    kind = classify_text_layer(joined, pages)
    result = Extraction(source, out_dir, kind, pages)

    images = out_dir / "images"
    images.mkdir(exist_ok=True)
    _run(["pdfimages", "-j", str(source), str(images / "img")])
    for image in sorted(images.iterdir()):
        if image.stat().st_size < MIN_EMBEDDED_BYTES:
            image.unlink()
    result.pictures = sorted(images.iterdir())

    if kind == "pdf-scanned":
        result.warnings.append("This PDF has no readable text (it is a picture of the pages). "
                               "Transcribe the text by reading the page pictures.")
    else:
        bad = suspect_count(joined)
        if bad > pages * 3:
            result.warnings.append(f"The PDF's built-in text looks like rough scanning ({bad} suspicious spots). "
                                   "Transcribe from the page pictures; use the text only as a cross-check.")
        else:
            result.warnings.append("The PDF's built-in text looks clean, but still check it against the page pictures.")
    return result


def extract(source: Path, out_dir: Path | None = None) -> Extraction:
    """Unpack any supported source file.

    Args:
        source: A Word, OpenDocument, RTF, text or PDF file.
        out_dir: Where to unpack; defaults to a folder under ``/tmp/elseyworks-extract``.

    Returns:
        The extraction result.

    Raises:
        ValueError: If the file type is not supported.
    """
    source = source.resolve()
    suffix = source.suffix.lower()
    out = out_dir or DEFAULT_OUT / re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    if suffix == ".pdf":
        return extract_pdf(source, out)
    if suffix in WORD_TYPES:
        return extract_word(source, out)
    if suffix in TEXT_TYPES:
        shutil.copy(source, out / "source.md")
        return Extraction(source, out, "text")
    msg = f"Unsupported file type '{suffix}'. Use a PDF, Word document (.docx) or text file."
    raise ValueError(msg)


def report(result: Extraction) -> str:
    """Describe an extraction in plain text.

    Args:
        result: The extraction to describe.

    Returns:
        A short multi-line report.
    """
    lines = [f"Source: {result.source.name}", f"Type:   {result.kind}", f"Folder: {result.out_dir}"]
    if result.pages:
        lines.append(f"Pages:  {result.pages} (page-1.jpg ... page-{result.pages}.jpg, with page-N.txt text layers)")
    if result.kind in {"word", "text"}:
        lines.append("Text:   source.md")
    if result.pictures:
        lines.append(f"Pictures found ({len(result.pictures)}):")
        lines.extend(f"  {p.relative_to(result.out_dir)}" for p in result.pictures)
    lines.extend(f"Note:   {w}" for w in result.warnings)
    return "\n".join(lines)


def main() -> int:
    """Command-line entry point.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    try:
        print(report(extract(args.source, args.out)))
    except (RuntimeError, ValueError, OSError) as err:
        print(f"Problem: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
