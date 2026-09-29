---
name: add-article
description: Add a new article to Lynn's website from a Word document, a scanned or digital PDF, pasted text or a web link, optionally with extra pictures. Use when Lynn says "add this article", shares a PDF/Word file, or wants something new on the site.
---

Read `CLAUDE.md` and `style-guide.md` first. Talk to Lynn in plain, non-technical language throughout
(never mention the steps, tools or file names below). The **strict proofreading rule** applies: the
wording is final – transcribe faithfully, fix only genuine typos/scanning errors, never improve prose.

## 1. Gather what she gave you
The main source (Word file, PDF, pasted text, link) plus any extra pictures. Don't interrogate her yet.

## 2. Unpack the source
```bash
uv run python scripts/extract_source.py "<path to her file>"
```
It writes to a work folder outside the site (path is printed) and reports what it found:

| Report says | Meaning | What you do |
|---|---|---|
| `word` | `source.md` has the text with headings, bold, italics, quotes; `media/` has pictures | Use `source.md` as the base text (still check it against the document for lost formatting) |
| `pdf-text` | PDF has a text layer | The text layer is **not trustworthy** – magazine scans usually carry rough OCR ("dift'erently", "Wlnery"). Transcribe from the page pictures; use `page-N.txt` only to double-check spellings of names |
| `pdf-scanned` | PDF is only pictures | Transcribe entirely from the page pictures |
| pasted text / link | – | Use as given (fetch the link and take just the article text) |

For PDFs, **look at every `page-N.jpg`** with the Read tool. In each page picture, work out the reading order
(magazines use columns: down the first column, then the next). Where the picture and the text layer disagree,
the picture wins. If something is genuinely illegible or ambiguous (a name, number, address), don't guess:
note it and ask Lynn in plain words ("The date in the second paragraph is blurry – is it 1999 or 1989?").

## 3. Write the text
**From a PDF (or scan):** first produce a plain transcript, then let Lynn proofread it (step 3a) *before* laying out the
page. **From a Word document or pasted text:** skip 3a – she already has the text – and go to 3b.

Transcript/page-text rules (both cases):
- **Include:** headline material as printed, the article body, sub-headings, boxed sidebars, captions and photo credits.
- **Leave out:** page numbers, running headers/footers, adverts, "continued on page X", and the printed byline
  (the site adds "By Lynn Elsey"). Display pull-quotes that merely repeat a line from the body can be left out –
  tell Lynn you did.
- Keep the author's spelling, punctuation and wording exactly, including Australian/British spelling. Remove only
  scanning artefacts: hyphenation left at line ends, stray soft hyphens, words split across columns.
- Where you can't tell what a word/number is, write it as `[[CHECK: best guess?]]` so it stands out.

### 3a. PDF only – offer Lynn a Word document to proofread first
1. Write the transcript to the work folder as `transcript.md`, in plain markdown with **no** site shortcodes:
   title as `# Title`, the printed standfirst as the first paragraph in italics, sub-headings as `##`, quotes as `>`,
   sidebars under a bold "Box:" line, and captions as italic lines marked "Picture caption:".
2. Make a Word file and put it where she can find it, then open it for her:
   ```bash
   mkdir -p ~/Documents/Elseyworks
   pandoc transcript.md -o ~/Documents/Elseyworks/"<Article title> - text to check.docx"
   open ~/Documents/Elseyworks/"<Article title> - text to check.docx"
   ```
3. Tell her, plainly: "I've typed out the article from your PDF and opened it in Word. Could you read it through against
   the original and fix anything that's wrong, just by typing over it? Save it when you're done and tell me. Anything
   marked CHECK is a spot I couldn't read properly." Don't ask her for comments or track changes – typing over is enough.
   Then **stop and wait** for her. (If she'd rather skip this and just see the page, that's fine – carry on to 3b
   and mention the text can still be corrected in the preview.)
4. When she says she's finished: unpack her edited file with
   `uv run python scripts/extract_source.py "<her saved .docx>"` and compare `source.md` with your `transcript.md`.
   **Her version is now the final wording** – use it exactly, even where it differs from the original PDF or looks
   unconventional (the "no improvements" rule is about *your* edits; her own changes are always right).
   Leave any `[[CHECK…]]` markers she hasn't resolved out of the page and ask her about them.
   If she saved a new Word file elsewhere or under another name, ask her where it is.

### 3b. Lay out the page
Turn the final text into the page, following the layout conventions in `CLAUDE.md`:
- Standfirst/intro as printed → `{{< lead >}}…{{< /lead >}}` at the top. If the magazine had none, don't invent one.
- Sub-headings → `##` (or `###` for a level below); quotes → `>`; boxed sidebars → `{{< callout >}}`;
  lists of addresses/phone numbers → one entry per paragraph with `<br>` line breaks (see `content/food-travel/portland`).
- **Last line:** where it was first published, e.g. `**Originally published in the July 2018 edition of the NSW Law Society Journal.**`

## 4. Ask only what's missing (one question at a time, with a suggestion)
You can ask these while she proofreads, or before you start. Work these out yourself first from the document; ask only about what you can't tell:
- **Subject:** `food-travel`, `careers`, `magazines`, `business` or `health` – suggest one ("I'd put this under Food & Travel – OK?").
- **Publication and date** (month and year is enough; use the 1st of the month), if not printed on the pages.
- **Title**, if the source doesn't make it obvious. Use it as printed (headlines have no full stop at the end – see the style guide).

## 5. Create the article folder
`content/<subject>/<slug>/` – slug is the title in lowercase with hyphens and no punctuation (`the-wild-west`).
Inside: `index.md` and the picture/PDF files. Front matter:

```yaml
---
title: The Wild West
description: One-sentence summary shown on cards (use the printed standfirst; if there is none, describe the article neutrally)
date: 2003-06-01
draft: false
thumbnail: the-wild-west-landscape.jpg
publication: Decanter Magazine
---
```
Add `featured: true` only if Lynn asks.

## 6. Pictures – three kinds
1. **The article as published.** Copy the original PDF into the folder as `<slug>.pdf` (warn Nick if over ~8 MB) and
   show a picture of its first page linked to it:
   `{{< img-caption src="<slug>-cover.jpg" href="<slug>.pdf" caption="Published in Decanter Magazine, June 2003" >}}`.
   Use `page-1.jpg` from the work folder, renamed. Include this on every article that came from a magazine/PDF.
2. **Photographs from the article.** Look through the work folder's `images/` (PDF) or `media/` (Word). Use the good,
   relevant ones with the caption/credit printed in the magazine. Place them with `{{< img-caption-float side="right|left" >}}`
   (alternate sides) or `{{< img-caption >}}` for wide ones. Skip logos, tiny decorations and repeats.
3. **Pictures Lynn supplied.** Use them where she says, or where they fit best; ask her for a caption if it's not obvious.

Name files clearly (`<slug>-1.jpg`, …). Keep each under ~1.5 MB and no wider than ~1800 px
(`sips -Z 1800 file.jpg`). Every inline picture gets a caption. **Thumbnail:** a strong, clear picture that still looks
good cropped to a wide 3:2 shape; save it as `<slug>-landscape.jpg` and point `thumbnail:` at it. A page-1 scan is
fine when the article has no photos. View it in the preview cards to check the crop.

## 7. Check, then show Lynn
1. `uv run python scripts/check_content.py` – fix anything it reports.
2. `scripts/preview.sh`, then open the new page and look at it yourself (headings, pictures beside the right text,
   nothing cut off, PDF link works, the card on the subject page looks right).
3. Tell Lynn, in a few plain sentences: the link (`http://localhost:1313/<subject>/<slug>/`), what's on the page,
   and anything you want her eyes on – typos you fixed ("I corrected 'volcmoes' to 'volcanoes'"), anything you
   couldn't read, which pictures you used and why. Ask if she wants changes or is happy to publish.
4. Make her changes and show her again. Do **not** publish until she says yes – then use the `publish` skill.
