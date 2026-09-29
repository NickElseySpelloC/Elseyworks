"""Tests for unpacking Word and PDF source files."""

from __future__ import annotations

import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
from pathlib import Path

import pytest

from scripts import extract_source as ex

ROOT = Path(__file__).resolve().parent.parent
SAMPLE_PDF = ROOT / "content/careers/let-the-net-work-for-you/let-the-net.pdf"
needs_poppler = pytest.mark.skipif(shutil.which("pdftoppm") is None, reason="poppler not installed")
needs_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")


def test_classify_no_text_is_scanned() -> None:
    assert ex.classify_text_layer("", 3) == "pdf-scanned"


def test_classify_real_text() -> None:
    assert ex.classify_text_layer("word " * 400, 1) == "pdf-text"


def test_suspect_count_flags_ocr_noise() -> None:
    assert ex.suspect_count("Oppo�ite and dift'erently and ever­green") >= 3
    assert ex.suspect_count("A perfectly clean sentence about wine.") == 0


def test_unsupported_type(tmp_path: Path) -> None:
    bad = tmp_path / "x.xyz"
    bad.write_text("hi")
    with pytest.raises(ValueError, match="Unsupported"):
        ex.extract(bad, tmp_path / "out")


@needs_poppler
def test_pdf_pages_rendered(tmp_path: Path) -> None:
    result = ex.extract(SAMPLE_PDF, tmp_path / "out")
    assert result.pages == 2
    assert (result.out_dir / "page-1.jpg").is_file()
    assert (result.out_dir / "page-2.txt").is_file()
    assert "page-1.jpg" in ex.report(result)


@needs_poppler
def test_image_only_pdf_is_scanned(tmp_path: Path) -> None:
    subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        ["pdftoppm", "-jpeg", "-f", "1", "-l", "1", "-singlefile", str(SAMPLE_PDF), str(tmp_path / "p")],  # ruff: ignore[start-process-with-partial-path]
        check=True,
    )
    pdf = tmp_path / "scan.pdf"
    if shutil.which("sips") is None:
        pytest.skip("sips not available to build an image-only PDF")
    subprocess.run(["sips", "-s", "format", "pdf", str(tmp_path / "p.jpg"), "--out", str(pdf)],  # ruff: ignore[subprocess-without-shell-equals-true, start-process-with-partial-path]
                   check=True, capture_output=True)
    result = ex.extract(pdf, tmp_path / "out")
    assert result.kind == "pdf-scanned"
    assert any("no readable text" in w for w in result.warnings)


@needs_pandoc
def test_word_document_becomes_markdown(tmp_path: Path) -> None:
    md = tmp_path / "in.md"
    md.write_text("# Title\n\nSome *italic* and **bold** text.\n\n> A quote\n", encoding="utf-8")
    docx = tmp_path / "article.docx"
    subprocess.run(["pandoc", str(md), "-o", str(docx)], check=True)  # ruff: ignore[subprocess-without-shell-equals-true, start-process-with-partial-path]
    result = ex.extract(docx, tmp_path / "out")
    text = (result.out_dir / "source.md").read_text(encoding="utf-8")
    assert result.kind == "word"
    assert "*italic*" in text
    assert "**bold**" in text
    assert "> A quote" in text
