---
date: '2026-05-03T13:34:04+10:00'
title: 'Folder Structure'
description: "A reference to the key folders and files in this repo"
showTableOfContents: true
showBreadcrumbs: true
---

This page documents the key folders and files in the ElseyWorld repository.

## Top-level overview

```
Elseyworks/
├── archetypes/       # Default front matter templates for new pages
├── assets/           # Source files processed by Hugo (CSS, images)
├── config/           # Hugo site configuration files
├── content/          # All site content (markdown pages)
├── data/             # (currently unused) Hugo data files
├── docs/             # Internal project documentation and briefs
├── i18n/             # Internationalisation string overrides
├── layouts/          # Custom Hugo templates overriding the theme
├── migration/        # Python tooling for legacy CMS content migration
├── public/           # Hugo build output — never edit directly
├── resources/        # Hugo internal cache — never edit directly
├── static/           # Static files copied verbatim to the build output
└── themes/congo/     # The Congo theme — do not edit directly
```

---

## archetypes/

Contains `default.md` — the front matter template Hugo uses when creating a new content page with `hugo new`. Edit this to change the default fields that appear in new pages.

---

## assets/

Source assets that Hugo processes through its asset pipeline before publishing.

```
assets/
├── css/
│   └── custom.css    # All custom CSS overrides for the site
└── img/
    ├── logo/         # Site logo images (light/dark variants)
    └── people/       # Author headshots used in bio components
```

**Key rule:** `custom.css` is automatically bundled by Congo — no configuration needed. All custom styles go here, never inline or in theme files.

---

## config/_default/

All Hugo configuration is split across these files:

| File | Purpose |
|:--|:--|
| `hugo.toml` | Core settings: base URL, title, language, timezone, pagination |
| `params.toml` | Congo theme parameters: colour scheme, navigation, social links, features |
| `languages.en.toml` | Language-specific settings (site title, description) |
| `menus.en.toml` | Navigation menu items |
| `markup.toml` | Goldmark markdown renderer settings, syntax highlighting, table of contents |
| `module.toml` | Hugo module configuration (theme import) |

---

## content/

All site content as markdown files. Hugo builds a page for every file here.

```
content/
├── _index.html       # Home page
├── articles/         # Lynn's magazine-style articles
│   ├── business/
│   ├── careers/
│   ├── food-travel/
│   ├── health/
│   └── magazines/
├── blog/             # Nick's travel blog posts
│   ├── asia-2009/
│   ├── australia-2002-trip-1/
│   ├── australia-2002-trip-2/
│   ├── australia-2009/
│   ├── moving-to-dc/
│   └── south-pacific-1997/
├── categories/       # Taxonomy term pages (one per category)
├── contact/          # Contact pages for Nick and Lynn
└── resources/        # Site guides and technical reference (this section)
```

Most section landing pages use `_index.md` (branch bundles). Individual posts use `index.md` (leaf bundles) with co-located images in the same folder. See the [index vs _index](../index#understanding-index-vs-_index-pages) page for the distinction.

---

## docs/

Internal project documentation — not part of the published site. Contains planning briefs and notes used during development and content migration.

---

## i18n/

Internationalisation override files. Currently unused but available to override any UI strings that the Congo theme defines (e.g. "Read more", "Table of Contents").

---

## layouts/

Custom Hugo templates that override the Congo theme. Hugo's lookup order means any file here takes precedence over its equivalent in `themes/congo/layouts/`.

```
layouts/
├── simple.html               # Custom simple layout template
├── term.html                 # Custom taxonomy term layout
├── partials/
│   ├── article-link.html     # Custom article link component
│   ├── author.html           # Author bio component
│   ├── footer.html           # Site footer override
│   ├── logo.html             # Site logo override
│   ├── term-article-list.html # Article listing for taxonomy pages
│   ├── functions/            # Hugo template helper functions
│   └── header/               # Header partial overrides
├── resources/
│   └── list.html             # Custom list template for the resources section
└── shortcodes/               # Custom shortcodes (see Short Code Reference)
```

**Key rule:** Never edit files inside `themes/congo/`. Always create an override in the matching path under `layouts/`.

---

## migration/

Python tooling used to fetch and migrate content from the legacy CMS. Not used in the day-to-day running of the site.

| File | Purpose |
|:--|:--|
| `main.py` | Entry point |
| `config.py` | Migration configuration (source URLs, paths) |
| `fetch.py` | Fetches pages from the legacy CMS |
| `migrate.py` | Converts fetched content to Hugo markdown |
| `parser.py` | Parses and cleans legacy HTML content |
| `images.py` | Downloads and processes images |
| `fingerprint.py` | Content fingerprinting to detect changes |
| `debug_fetch.py` | Debug helper for fetch operations |
| `image-migration-log.csv` | Log of migrated images |
| `internal-links-log.csv` | Log of internal link rewrites |

Run scripts as modules from the repo root with the virtual environment active:

```bash
source .venv/bin/activate
python -m migration.fetch
```

Package management uses `uv` (not `pip`). The virtual environment is at `.venv/`.

---

## public/

Hugo's build output. Generated by running `hugo` or `hugo server`. **Never edit files here directly** — they are overwritten on every build. Deploy this folder to the hosting provider.

---

## resources/

Hugo's internal asset cache (generated files, processed images). Managed automatically by Hugo. Do not edit.

---

## static/

Files copied verbatim into the root of the build output without any processing.

```
static/
├── CNAME                 # Custom domain for GitHub Pages hosting
├── site.webmanifest      # PWA manifest for the site
├── apple-touch-icon.png  # iOS home screen icon
├── favicon-*.png         # Browser tab favicons
├── img/                  # Static images referenced site-wide
└── admin/
    ├── index.html        # Decap CMS admin interface
    └── config.yml        # Decap CMS configuration
```

Use `static/` for files that need a fixed, known URL (e.g. `favicon.ico`, `robots.txt`). Use `assets/` for files that need Hugo processing (e.g. CSS bundling).

---

## themes/congo/

The Congo Hugo theme, included as a Git submodule. **Do not edit any files here.** All customisations are made by placing override files in the corresponding `layouts/`, `assets/`, or `static/` paths at the repo root — Hugo's lookup order will prefer them automatically.

To update the theme: `git submodule update --remote themes/congo`

