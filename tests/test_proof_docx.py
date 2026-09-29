"""Tests for the tracked-changes proofreading tool."""

from __future__ import annotations

import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
from typing import TYPE_CHECKING

import pytest

from scripts import proof_docx as pd

if TYPE_CHECKING:
    from pathlib import Path

needs_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")

ARTICLE = """---
title: "A Test"
---

{{< lead >}}
An *italic* standfirst.
{{< /lead >}}

## A heading

First paragraph with a **bold** typo: volcmoes and more.

> A quoted line with volcmoes.

ADDRESS ONE<br>
**Tasting**: Daily<br>
Tel: +1 503 000

{{< img-caption src="a.jpg" caption="A caption" >}}
"""


def test_inline_formatting_and_breaks() -> None:
    runs = pd.parse_inline("plain **bold** and _it_<br>next [link](http://x.y)")
    assert "".join(r.text for r in runs) == "plain bold and it\nnext link"
    assert [r.text for r in runs if r.bold] == ["bold"]
    assert [r.text for r in runs if r.italic] == ["it"]


def test_parse_article_structure() -> None:
    title, paras = pd.parse_article(ARTICLE)
    assert title == "A Test"
    assert [p.style for p in paras] == ["BodyText", "Heading2", "BodyText", "BlockText", "BodyText", "BodyText"]
    assert paras[0].runs[0].italic
    assert paras[4].text == "ADDRESS ONE\nTasting: Daily\nTel: +1 503 000"
    assert paras[5].text == "[Picture caption: A caption]"


def test_missing_ambiguous_and_overlapping_fixes() -> None:
    _, paras = pd.parse_article(ARTICLE)
    with pytest.raises(ValueError, match="Could not find"):
        pd.locate_edits(paras, [pd.Fix("nothing here", "x")])
    with pytest.raises(ValueError, match="appears 2 times"):
        pd.locate_edits(paras, [pd.Fix("volcmoes", "volcanoes")])
    assert sum(len(v) for v in pd.locate_edits(paras, [pd.Fix("volcmoes", "volcanoes", all=True)]).values()) == 2
    with pytest.raises(ValueError, match="overlap"):
        pd.locate_edits(paras, [pd.Fix("bold typo", "x"), pd.Fix("typo: volc", "y")])


def test_diff_paragraphs_reports_word_changes() -> None:
    lines = pd.diff_paragraphs(["one two three four"], ["one 2 three four"])
    assert len(lines) == 1
    assert '"two" -> "2"' in lines[0]


def test_diff_paragraphs_identical() -> None:
    assert pd.diff_paragraphs(["a b"], ["a b"]) == []


@needs_pandoc
def test_docx_round_trip(tmp_path: Path) -> None:
    title, paras = pd.parse_article(ARTICLE)
    fixes = [pd.Fix("volcmoes and", "volcanoes and", "Spelling."), pd.Fix("Tel: +1 503 000", None, "Please check.")]
    out = tmp_path / "proof.docx"
    assert pd.build_docx(title, paras, fixes, out) == 2

    def read(mode: str) -> str:
        done = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
            ["pandoc", f"--track-changes={mode}", "-t", "plain", "--wrap=none", str(out)],  # ruff: ignore[start-process-with-partial-path]
            capture_output=True, text=True, check=True)
        return done.stdout

    assert "volcanoes and" in read("accept")
    assert "volcmoes and" in read("reject")
    assert "volcmoes and" not in read("accept")
    original = [pd._normalise(p.text) for p in paras]  # ruff: ignore[private-member-access]
    edited = pd.docx_paragraphs(out)
    changes = pd.diff_paragraphs(original, edited)
    assert len(changes) == 1
    assert '"volcmoes" -> "volcanoes"' in changes[0]
