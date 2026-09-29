# Elseyworks

The website for Lynn Elsey's writing – <https://elseyworks.com>.

Built with [Hugo](https://gohugo.io) using a custom "warm editorial" design (no external theme),
hosted on GitHub Pages (`.github/workflows/deploy.yml`, deploys on every push to `main`).

## Layout

| Path | What |
|---|---|
| `content/<subject>/<slug>/index.md` | One folder per article (text, pictures, PDF together). Subjects: `food-travel`, `careers`, `magazines`, `business`, `health` |
| `content/about.md`, `content/writing/` | Bio + contact form, and the full archive |
| `layouts/` | Page templates, partials and shortcodes |
| `assets/css/main.css`, `assets/img/` | Styles and Lynn's portrait |
| `scripts/` | `preview.sh`, `publish.sh`, `extract_source.py` (unpacks Word/PDF sources), `check_content.py`, `setup.sh` |
| `CLAUDE.md`, `.claude/skills/` | Instructions for the Claude assistant Lynn uses to manage the site |
| `design/` | Brief and design notes |

## Working on the site

```bash
scripts/setup.sh     # once per computer: installs hugo, poppler, pandoc, uv
scripts/preview.sh   # local preview at http://localhost:1313/
uv run pytest        # content checks + tests
uv run ruff check . && uv run mypy --strict scripts tests
```

Lynn does not use these directly; she asks the Claude assistant (see `CLAUDE.md`) to add articles
from PDFs, preview them and publish.

## Article front matter

```yaml
title: "Title"
description: "One-sentence summary used on cards"
date: 2018-07-01
draft: false
thumbnail: picture-in-same-folder.jpg
featured: true          # optional: shows on the home page (max 4 shown)
publication: "Magazine" # optional
```

Shortcodes: `lead`, `callout`, `img-caption`, `img-caption-float`, `img-float`, `clear-float`, `contact-form`.

## Contact form

Uses [Web3Forms](https://web3forms.com); the access key is in `config/_default/hugo.toml`.
