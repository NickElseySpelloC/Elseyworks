# Elseyworks – design notes

**Decisions (agreed with Nick):** work directly on `main`; drop Decap CMS; warm editorial look; Lynn is the only
author but keeps a bio page; no legacy URL aliases (redirects from elseyworld.com to be added by Nick later).

- **Custom Hugo layouts, no Congo** – removes the submodule, keeps the site to a few small templates.
- **Flat structure:** subjects are top-level sections (`/food-travel/…`), replacing categories + the "Lynn" tag.
- **Design:** cream/ink/terracotta palette (auto dark mode), Fraunces headings, Newsreader body, Inter labels.
  Home: hero, featured articles, subject tiles, recent writing. Card images come from each article's `thumbnail`.
- **Managing content:** Lynn uses Claude Code with the project `CLAUDE.md` + skills (`add-article`, `edit-article`,
  `preview`, `publish`). `scripts/check_content.py` guards every publish.

**Open items for Nick:** favicon/apple-touch icon still the old "EW" navy tile; article thumbnails are mixed
covers/landscapes (cards crop to 3:2); Wild West article has OCR typos worth proofreading; GitHub Pages custom
domain + Cloudflare settings; Lynn's Claude Code install.
