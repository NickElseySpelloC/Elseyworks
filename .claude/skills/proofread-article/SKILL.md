---
name: proofread-article
description: Proofread an article already on the site for genuine typos and scanning (OCR) errors, and give Lynn a Word document with the proposed corrections as tracked changes when there are more than a handful. Use when Lynn or Nick asks to proofread, check or clean up an article (or all articles).
---

Read `CLAUDE.md` (**strict proofreading rule**) and `style-guide.md` first.

**Scope – typos only.** These articles were published elsewhere, so the wording is final. You may propose fixes for
misspelt or garbled words, scanning/OCR damage (`volcmoes`, `Yallay Marlots`, letter O for zero), stray soft
hyphens, sentences broken by a paragraph split, and broken links. **Never** propose changes to grammar, syntax, style,
tone, punctuation choices or word choice – not even as optional suggestions. Anything unusual that might just be the
author's wording (e.g. `brick-buildinged`) or a name/number/address you can't verify is a *query*, not a fix.

## 1. Read the article carefully
Read the whole of `content/<subject>/<slug>/index.md`. For scanned magazine pieces, also compare against the
original PDF in the same folder if there is one (`uv run python scripts/extract_source.py <pdf>`, then look at the
page pictures) – it settles most guesses. Keep a list of proposed fixes, each with the exact text and a short reason.

## 2. Few changes (up to about five) – just tell the person
List them plainly in the chat (old → new, one line each, with the reason), then make them in `index.md` once they agree.

## 3. Many changes – use a Word document with tracked changes
1. Write the fixes to a scratch file (e.g. in the scratchpad) as JSON:
   ```json
   [
     {"find": "volcmoes", "replace": "volcanoes", "note": "Spelling."},
     {"find": "eastwanfs green", "replace": "eastwards green", "note": "Scanning error; 'eastwards' is my best reading - please check."},
     {"find": "Tel: + 1 589 522 1234", "replace": null, "note": "Query: area code is 589 but the other Walla Walla numbers are 509."}
   ]
   ```
   - `find` is matched against the article's **plain text** (no `**`, `_`, `[]()` marks; line breaks from `<br>` count as newlines).
     Use enough surrounding words that it appears exactly once, or add `"all": true` for a repeated error.
   - `"replace": null` adds a comment with no change (a query).
   - Every entry needs a `note`. Say when a fix is a guess.
   - Fixes that join a split paragraph or change layout aren't supported – list those in chat instead.
2. Build the document and open it for the reader:
   ```bash
   mkdir -p ~/Documents/Elseyworks
   uv run python scripts/proof_docx.py make content/<subject>/<slug> fixes.json \
       --out ~/Documents/Elseyworks/"<Article title> - proposed corrections.docx"
   open ~/Documents/Elseyworks/"<Article title> - proposed corrections.docx"
   ```
   Fix any "Could not find / appears N times / overlap" message by adjusting `find`, then rerun.
3. Tell the reader, in plain words (to Lynn: no technical terms): "I've opened the article in Word with my suggested
   corrections shown as tracked changes, with a short note beside each one. Please accept the ones that are right,
   reject or fix the others, then save the document and tell me." Then **stop and wait**.
4. When they say they've finished:
   ```bash
   uv run python scripts/proof_docx.py diff content/<subject>/<slug> "<their saved .docx>"
   ```
   It lists every wording difference between the article and the accepted document (`CHANGE: "old" -> "new"` with context).
   Apply each of them to `index.md` with careful edits (keep the markdown marks and shortcodes around the text intact).
   **Their document is the final wording** – apply what they accepted *and anything they typed themselves*,
   even if you'd have worded it differently. Changes they rejected simply don't appear in the list.
   If the list shows a paragraph added, removed or merged, look at the document to see what they did and mirror it.
5. Run `uv run python scripts/check_content.py`, run `scripts/preview.sh`, and give the link to the page. Do not publish
   until they've looked at it and said yes (then use the `publish` skill).

## Tips
- Comments left in the document by the reader are not picked up by `diff`; if they say they left comments, ask
  them to tell you what they said, or to type the change into the text.
- Whole-site pass: do one article at a time, in the order Nick or Lynn asks; make a Word file only for articles with
  more than a handful of fixes.
