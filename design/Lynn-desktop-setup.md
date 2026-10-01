# Lynn's desktop – setup checklist

A step-by-step for **Nick** to turn an out-of-the-box Mac into a working Elseyworks machine for Lynn.
Run these in **Terminal** (Applications → Utilities → Terminal) unless noted.

**Machine:** 2019 iMac Retina 5K, **Intel**, macOS 15.8.1 (Sequoia).

> ⚠️ **Intel note:** on this Intel Mac, Homebrew installs to **`/usr/local`** (not `/opt/homebrew` as on Apple
> Silicon). The PATH line in step 2 reflects that. Everything else is arch-independent — Homebrew fetches the
> right build automatically.

---

## 0. Before you start
- [ ] macOS fully updated (Apple menu → System Settings → General → Software Update).
- [ ] Signed in to the **App Store** with an Apple ID (needed if you install Pages/Word from there).
- [ ] Know which GitHub account gets push access, and Lynn's name + email for commit attribution.
- [ ] A stable internet connection (first Homebrew + `uv sync` pull a fair bit down).

## 1. Xcode Command Line Tools (git, compilers)
The Homebrew installer in step 2 installs these automatically. To do it explicitly first:
```bash
xcode-select --install
```
Click through the dialog and wait for it to finish.

## 2. Homebrew (the package manager)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then add it to the PATH for this Intel Mac (the installer also prints these two lines — use its version if different):
```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/usr/local/bin/brew shellenv)"
```
Check it works:
```bash
brew --version
```

## 3. Command-line tools Elseyworks needs
```bash
brew install git gh uv hugo pandoc poppler
```
- **git** – version control (also came with the Command Line Tools; brew keeps it current).
- **gh** – GitHub CLI, used in step 5 to give the machine push access the easy way.
- **uv** – Python tool/venv manager; pulls Python 3.13, ruff, mypy and pytest itself in step 7.
- **hugo** – builds the website (Homebrew's hugo is the *extended* build the site requires).
- **pandoc** – converts between Word and the site's text (proofreading + new-article workflows).
- **poppler** – reads and renders PDFs (`pdftotext`, `pdftoppm`, `pdfimages`).

Confirm they're all on the PATH:
```bash
for t in git gh uv hugo pandoc pdftoppm; do printf '%-8s ' "$t"; command -v "$t" || echo MISSING; done
hugo version   # should say "+extended"
```

## 4. Claude Code (the desktop app Lynn will use)
- [ ] Download the **Claude desktop app** for macOS from <https://claude.ai/download> and drag it to Applications.
- [ ] Open it and **sign in** with Lynn's Claude account (the one on the plan that includes Claude Code).
- [ ] Confirm the app has a **Code** tab (this is what she'll work in). No VS Code needed.

## 5. GitHub access (so changes can be published)
Authenticate the machine with GitHub. `gh` will also offer to set up git so pushing "just works" — say **yes**.
```bash
gh auth login
```
Choose: **GitHub.com** → **HTTPS** → **Yes** (authenticate Git with your GitHub credentials) → **Login with a
web browser**, then paste the code. When done:
```bash
gh auth status              # should show logged in
```
Set who commits are attributed to (use Lynn's details):
```bash
git config --global user.name  "Lynn Elsey"
git config --global user.email "lynn@example.com"    # <-- Lynn's email
```

## 6. Get the website
Clone the repo into a sensible spot (e.g. a `dev` folder in her home directory):
```bash
mkdir -p ~/dev && cd ~/dev
gh repo clone NickElseySpelloC/Elseyworks
cd Elseyworks
```

## 7. Install the site's Python tools
```bash
cd ~/dev/Elseyworks
./scripts/setup.sh
```
This runs `uv sync`, which fetches Python 3.13 and the dev tools (ruff, mypy, pytest).
> **Note:** `scripts/setup.sh` installs hugo/poppler/pandoc/uv/git but not `gh` — that's why `gh` is in the manual
> `brew install` at step 3.

## 8. Microsoft Word (for the proofreading workflow)
The proofreading and new-article skills open a `.docx` for Lynn to edit, and read it back with tracked changes.
Lynn uses **Word** (her preference).
- [ ] Install **Microsoft Word** and sign in to her Microsoft 365 account.
- [ ] Make sure double-clicking a `.docx` opens **Word** (not TextEdit or Pages, which handle tracked changes
      poorly). If needed: right-click a `.docx` → Get Info → Open with: Microsoft Word → **Change All…**
- [ ] Test that the workflow's path and Word launch both work:
```bash
mkdir -p ~/Documents/Elseyworks
printf '%s' 'hello' | pandoc -o ~/Documents/Elseyworks/test.docx && open ~/Documents/Elseyworks/test.docx
```
      It should open in Word showing "hello". Then delete `~/Documents/Elseyworks/test.docx`.

## 9. Prove the whole toolchain works
From `~/dev/Elseyworks`:
```bash
uv run pytest -q                        # expect: all pass (a few may skip if a tool is missing)
uv run ruff check .                     # expect: All checks passed!
uv run python scripts/check_content.py  # expect: All NN articles look good.
./scripts/preview.sh                     # prints http://localhost:1313/
```
- [ ] Open **http://localhost:1313/** in a web browser (Safari is fine) and confirm the site loads and looks right.
- [ ] Stop the preview when done: `./scripts/stop-preview.sh`

## 10. Open the project in Claude Code
- [ ] In the Claude desktop app → **Code** tab, open the folder `~/dev/Elseyworks`.
- [ ] Confirm the assistant picks up the project instructions and skills: ask it **"what can you do?"** — it should
      run the **help** skill and list add / change / proofread / add-article / look-and-feel / publish.
- [ ] Do a quick **dry run** with Lynn watching: ask it to show a preview, make a tiny reversible change, preview
      again, then discard it (don't publish the throwaway).

## 11. Hand-over to Lynn
- [ ] Show her how to open the Claude desktop app and the Code tab, and that she just types in plain English.
- [ ] Point her at **"what can you do?"** / **"I need help"** as her starting point.
- [ ] Agree what she does if something looks wrong: **call Nick** (the assistant is told to say this too).
- [ ] Optional: print a one-page "how to talk to your assistant" sheet (can be generated from the `help` skill).

---

## Quick reference – everything installed
| Tool | Why | Installed in |
|------|-----|--------------|
| Homebrew | package manager | step 2 |
| git, gh | version control + GitHub access/publishing | step 3, 5 |
| uv | Python + ruff/mypy/pytest + Python 3.13 | step 3, 7 |
| hugo (extended) | builds the website | step 3 |
| pandoc | Word ↔ site text | step 3 |
| poppler | reads/renders PDFs | step 3 |
| Claude desktop app | what Lynn uses | step 4 |
| Microsoft Word | proofreading `.docx` with tracked changes | step 8 |

_Not installing:_ VS Code, Node (the desktop app doesn't need it), Xcode (full IDE — Command Line Tools are enough).
