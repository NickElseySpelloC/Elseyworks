"""Check every article for the problems that would break or spoil the site.

Run with ``uv run python scripts/check_content.py``. Exits non-zero and prints
plain-English problems if anything needs fixing.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SECTIONS = ("food-travel", "careers", "magazines", "business", "health")
REQUIRED = ("title", "description", "date", "thumbnail")
_FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_SRC = re.compile(r'(?:src|href)="([^"/][^":]*?\.(?:jpe?g|png|gif|webp|pdf))"', re.IGNORECASE)
_MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)\s:]+)\)")


@dataclass(frozen=True)
class Problem:
    """A single thing wrong with an article.

    Attributes:
        article: Path of the article folder, relative to ``content``.
        message: Plain-English description of the problem.
    """

    article: str
    message: str

    def __str__(self) -> str:
        return f"{self.article}: {self.message}"


def parse_front_matter(text: str) -> tuple[dict[str, object], str]:
    """Split an article into its front matter and body.

    Args:
        text: Full text of an ``index.md`` file.

    Returns:
        The parsed front matter (empty if missing or invalid) and the body text.
    """
    match = _FRONT_MATTER.match(text)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}, text[match.end():]
    return (data if isinstance(data, dict) else {}), text[match.end():]


def check_article(index: Path, content: Path = CONTENT) -> list[Problem]:
    """Check one article.

    Args:
        index: Path to the article's ``index.md``.
        content: The content root, used to build readable names.

    Returns:
        Problems found (empty when the article is fine).
    """
    folder = index.parent
    name = str(folder.relative_to(content))
    problems: list[Problem] = []
    meta, body = parse_front_matter(index.read_text(encoding="utf-8"))
    if not meta:
        return [Problem(name, "the top section (title, date, etc.) is missing or unreadable")]

    problems.extend(
        Problem(name, f"'{key}' is missing") for key in REQUIRED if not str(meta.get(key) or "").strip()
    )
    thumb = str(meta.get("thumbnail") or "").strip()
    if thumb and not (folder / thumb).is_file():
        problems.append(Problem(name, f"the thumbnail picture '{thumb}' is not in the article folder"))

    referenced = set(_SRC.findall(body)) | set(_MD_IMG.findall(body))
    problems.extend(
        Problem(name, f"the file '{ref}' is used in the article but is not in its folder")
        for ref in sorted(referenced)
        if not (folder / ref).is_file()
    )
    if re.search(r"^# ", body, re.MULTILINE):
        problems.append(Problem(name, "the body has a top-level heading; use '##' (the title is added automatically)"))
    return problems


def check_site(content: Path = CONTENT) -> list[Problem]:
    """Check every article and section on the site.

    Args:
        content: The content root folder.

    Returns:
        All problems found.
    """
    problems: list[Problem] = []
    for section in sorted(p for p in content.iterdir() if p.is_dir() and p.name != "writing"):
        if not (section / "_index.md").is_file():
            problems.append(Problem(section.name, "this subject folder has no _index.md"))
        for index in sorted(section.glob("*/index.md")):
            problems.extend(check_article(index, content))
    return problems


def main() -> int:
    """Run the checks and report.

    Returns:
        Process exit code: 0 if everything is fine, 1 otherwise.
    """
    problems = check_site()
    if problems:
        print("Please fix the following before publishing:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    count = len(list(CONTENT.glob("*/*/index.md")))
    print(f"All {count} articles look good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
