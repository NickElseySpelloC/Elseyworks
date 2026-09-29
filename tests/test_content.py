"""Tests for the content checker, and a guard that the real site content is valid."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scripts import check_content as cc

if TYPE_CHECKING:
    from pathlib import Path

GOOD = """---
title: Test
description: A test article.
date: 2024-01-01T00:00:00+10:00
thumbnail: pic.jpg
---

Hello.

{{< img-caption src="pic.jpg" caption="x" >}}
"""


def _make(tmp_path: Path, text: str, *, with_pic: bool = True) -> Path:
    folder = tmp_path / "health" / "test"
    folder.mkdir(parents=True)
    (tmp_path / "health" / "_index.md").write_text("---\ntitle: Health\n---\n")
    if with_pic:
        (folder / "pic.jpg").write_bytes(b"x")
    index = folder / "index.md"
    index.write_text(text, encoding="utf-8")
    return index


def test_good_article_has_no_problems(tmp_path: Path) -> None:
    index = _make(tmp_path, GOOD)
    assert cc.check_article(index, tmp_path) == []


def test_missing_thumbnail_file(tmp_path: Path) -> None:
    index = _make(tmp_path, GOOD, with_pic=False)
    messages = [p.message for p in cc.check_article(index, tmp_path)]
    assert any("thumbnail" in m for m in messages)


def test_missing_required_field(tmp_path: Path) -> None:
    index = _make(tmp_path, GOOD.replace("description: A test article.\n", ""))
    messages = [p.message for p in cc.check_article(index, tmp_path)]
    assert "'description' is missing" in messages


def test_missing_referenced_image(tmp_path: Path) -> None:
    index = _make(tmp_path, GOOD + '\n<img src="other.jpg">\n')
    messages = [p.message for p in cc.check_article(index, tmp_path)]
    assert any("other.jpg" in m for m in messages)


def test_h1_in_body_flagged(tmp_path: Path) -> None:
    index = _make(tmp_path, GOOD + "\n# Big heading\n")
    messages = [p.message for p in cc.check_article(index, tmp_path)]
    assert any("top-level heading" in m for m in messages)


def test_bad_front_matter(tmp_path: Path) -> None:
    index = _make(tmp_path, "no front matter here")
    assert cc.check_article(index, tmp_path)


def test_real_site_content_is_valid() -> None:
    assert cc.check_site() == []
