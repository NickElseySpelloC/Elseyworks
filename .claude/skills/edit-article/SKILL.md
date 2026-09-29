---
name: edit-article
description: Change, correct, re-order or remove an existing article on Lynn's website (fix a typo, swap a picture, change a title or date, feature on the home page, delete an article).
---

Follow `CLAUDE.md`: plain, non-technical language with Lynn.

1. Find the article: `content/<subject>/<slug>/index.md` (search by title). If unsure which one she means, ask
   with the titles you found.
2. Make exactly the change she asked for. Notes:
   - Title/summary/date live in the top section of `index.md`; text below it is the article.
   - Swapping a picture: put the new file in the article's folder and update `thumbnail:` or the shortcode.
   - Featuring on the home page: `featured: true` (the home page shows the four newest featured articles – if
     there would then be more than four, tell her which will drop off).
   - Moving to another subject: move the whole folder to the other subject's folder.
   - Removing: delete the article's folder (confirm the title with her first – it can be recovered, but ask).
3. Run `uv run python scripts/check_content.py`, start `scripts/preview.sh`, and give her the link to the
   changed page (or `http://localhost:1313/` for home page changes). Ask if she's happy to publish.
