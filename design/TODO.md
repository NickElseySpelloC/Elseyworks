# Elseyworks – outstanding tasks

_Last updated 2026-09-30. Local `main` is ahead of GitHub (not pushed). Section 1 is done._

## 1. Finish the tracked-changes proofreading tool ✅ DONE (committed, not pushed)
- [x] Re-run `uv run pytest`, `uv run ruff check .` and `uv run mypy --strict scripts tests` — 20 passed, ruff clean, mypy clean.
- [x] Fix the remaining `ruff` findings in `scripts/proof_docx.py` (refactored `parse_article` into `_ArticleBuilder`, `itertools.pairwise`, docstrings, `_execute` helper for `main`).
- [x] Write `.claude/skills/proofread-article/SKILL.md`.
- [x] Add `proof_docx.py` and the new skill to `CLAUDE.md` (skills table + technical reference) and `README.md`.
- [x] Check the generated `.docx` opens correctly — validated with `python-docx` (styles map correctly; `w:ins`/`w:del`/comments present) and pandoc round-trip (reject→original, accept→correction). Could not screenshot the Word window (no screen-recording permission), but Word opened it without error.
- [x] Commit (don't push).

## 2. Proofreading the existing articles
- [x] The Wild West is done. Nick confirmed the three guesses ("eastwards", "Yakima Valley Red", "Thu-Sun"). Still open: whether "brick-buildinged" is original wording, and the `+ 1 589 522 1234` phone number (other Walla Walla numbers use 509).

## 3. Help skill ✅ DONE (committed, not pushed)
- [x] Create a "Help skill" for Lynn — `.claude/skills/help/SKILL.md`: friendly plain-English menu of what she can ask for (preview, change an article, proofread, add an article, look-and-feel, publish), expands on any one on request. Added to the `CLAUDE.md` skills table.

## 4. Design and site follow-ups to be done by Nick

- [ ] Nick's style-guide document from Lynn: fold into `style-guide.md` (currently: headlines one font/colour with no trailing full stop; always light).
- [ ] Mobile layout check of all page types (only checked on a desktop viewport so far); check dark-mode removal looks right on phones.
- [x] Google Analytics ID (`G-G6X0C9Z7F4`) – confirm it is the right property for this site.
- [x] Redirects from elseyworld.com to elseyworks.com (Nick, Cloudflare) once ready.
- [ ] Optional: 
  - [ ] site search
  - [ ] sitemap/SEO check
  - [x] RSS - not wanted

## 5. Set up Lynn's desktop (needs Nick at her machine)
- [ ] Install Claude Code (desktop app) and sign her in.
- [ ] Install Homebrew, then run `scripts/setup.sh` (installs hugo, poppler, pandoc, uv, git and the Python tools).
- [ ] Clone `NickElseySpelloC/Elseyworks` and give her machine git push access (GitHub login / token or SSH key). Check `git push` works.
- [ ] Open the project in Claude Code and confirm `CLAUDE.md` and the skills load (`add-article`, `edit-article`, `preview`, `publish`).
- [ ] Confirm Word (or Pages) is installed and that `open` starts it for `.docx` files.
- [ ] Check her machine handles the preview at `http://localhost:1313/` and the `~/Documents/Elseyworks/` folder for Word files.
- [ ] Dry-run the full workflow with her: add a real (or throwaway) article from a scanned PDF → Word proofread → preview → publish. Delete any throwaway afterwards.
- [ ] Walk her through the preview / approve / publish flow and how to ask for changes.
- [ ] Decide what she does if something goes wrong (call Nick). Consider a short one-page "how to talk to your assistant" sheet.

## 6. Design and site follow-ups to be done with Lynn
- [ ] Run the `proofread-article` workflow on the other 24 articles, one at a time, typos and OCR errors only.
- [ ] "Elsey*works*" logo is two-tone – ask Lynn whether she wants it one style (the headline rule may not apply to a logo).
- [ ] Contact form: send a real test message through Web3Forms and confirm it reaches Lynn.
- [ ] Article thumbnails are a mix of covers and landscapes; review cards on each subject page and re-crop any that look poor.
- [ ] The featured articles on the home page (Verona, Age Discrimination, Rome, Terri Janke) were my picks – get Lynn's choices.

## 6. Housekeeping
- [x] Push the 3 local commits (and later ones) when the connection is good.
- [x] Verify the GitHub Pages deploy after each push.
- [x] `git status` clean-up: `.claude/settings.local.json` is per-machine; consider adding it to `.gitignore`.
