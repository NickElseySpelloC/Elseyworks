---
name: add-article
description: Add a new article to Lynn's website from a PDF, Word document, pasted text or web link. Use when Lynn says "add this article", shares a PDF/document, or wants something new on the site.
---

Follow `CLAUDE.md`: talk to Lynn in plain, non-technical language throughout.

1. **Get the material.** Read the PDF/document/text she gave you (`Read` for PDFs; `pdftotext -layout` if
   helpful; for a web link, fetch it). If she attached page scans or photos, keep them.
2. **Work out the details yourself; only ask about what's missing.** You need:
   - subject: `food-travel`, `careers`, `magazines`, `business` or `health` (suggest one),
   - title, and the date first published (month and year is fine – use the 1st of the month),
   - where it was published, if anywhere (e.g. "NSW Law Society Journal, July 2018").
   Write a one-sentence `description` yourself.
3. **Create the article folder** `content/<subject>/<slug>/` (lowercase, hyphens, no punctuation) with
   `index.md`. Use the article layout in `archetypes/default.md` and the shortcodes listed in `CLAUDE.md`:
   - open with `{{< lead >}}` (her standfirst/intro sentence),
   - turn section titles into `##` headings, pull-quotes into `>` quotes, sidebars into `{{< callout >}}`,
   - remove page numbers, running headers/footers and hyphenation left over from scanning,
   - end with an italic/bold line saying where it was originally published, e.g.
     `**Originally published in the July 2018 edition of the NSW Law Society Journal.**` and set `publication:`.
4. **Pictures.**
   - Copy the original PDF into the folder as `<slug>.pdf` if it is a published copy, and link it with
     `{{< img-caption src="<slug>-page.jpg" href="<slug>.pdf" caption="Published in …" >}}`.
   - Render the first page (or a good page) as `<slug>-landscape.jpg`
     (`pdftoppm -jpeg -r 110 -f 1 -l 1 -singlefile in.pdf <slug>-page`, then crop/scale if you can – cards show a 3:2
     crop, so favour a picture that looks fine cropped). Use photos she supplied if they look better.
   - Set `thumbnail:` to that file. Give inline pictures captions.
   - Keep each picture under ~1.5 MB (`sips -Z 1800 file.jpg` shrinks it).
5. **Check** with `uv run python scripts/check_content.py` and fix anything it reports.
6. **Preview:** run `scripts/preview.sh`, then send Lynn the link to the new article, e.g.
   `http://localhost:1313/<subject>/<slug>/`, and tell her in one or two sentences what you did
   (mention any typos you fixed). Ask if she'd like any changes or is happy to publish.
7. Do **not** publish until she agrees – then use the `publish` skill.
