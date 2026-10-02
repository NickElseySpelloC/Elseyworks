# Elseyworks

The website for Lynn Elsey's writing – <https://elseyworks.com>.

Built with [Hugo](https://gohugo.io) using a custom "warm editorial" design (no external theme),
hosted on GitHub Pages (`.github/workflows/deploy.yml`, deploys on every push to `main`).

This README has three parts:

1. [About the site](#part-1--about-the-site) – what's in the project (for Nick)
2. [How to install](#part-2--how-to-install) – setting up a Mac so Lynn can work on the site (for Nick)
3. [How to use your website assistant](#part-3--how-to-use-your-website-assistant) – a guide written for Lynn

---

# Part 1 – About the site

## Layout

| Path | What |
|---|---|
| `content/<subject>/<slug>/index.md` | One folder per article (text, pictures, PDF together). Subjects: `food-travel`, `careers`, `magazines`, `business`, `health` |
| `content/about.md`, `content/writing/` | Bio + contact form, and the full archive |
| `layouts/` | Page templates, partials and shortcodes |
| `assets/css/main.css`, `assets/img/` | Styles and Lynn's portrait |
| `scripts/` | `setup.sh`, `preview.sh`, `stop-preview.sh`, `publish.sh`, `extract_source.py` (unpacks Word/PDF sources), `proof_docx.py` (tracked-changes proofreading), `check_content.py` |
| `CLAUDE.md`, `style-guide.md`, `.claude/skills/` | Instructions for the Claude assistant Lynn uses, and Lynn's style rules. Skills: `add-article`, `edit-article`, `proofread-article`, `preview`, `publish`, `help` |
| `design/` | Brief, design notes and the outstanding-tasks list (`TODO.md`) |

## Working on the site (Nick)

```bash
scripts/setup.sh     # once per computer: installs hugo, poppler, pandoc, uv, git and the Python tools
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

---

# Part 2 – How to install

A step-by-step for **Nick** to turn an out-of-the-box Mac into a working Elseyworks machine for Lynn.
Run these in **Terminal** (Applications → Utilities → Terminal) unless noted.

**Machines:**
- Desktop: 2019 iMac Retina 5K, **Intel**, macOS 15.8.1 (Sequoia) → use **Step 2B (MacPorts)** and **Step 3B**.
- Laptop: MacBook Air M1, **Apple Silicon** → use **Step 2A (Homebrew)** and **Step 3A**.

> ⚠️ **Which package manager?** Homebrew has dropped support for Intel Macs and recommends MacPorts instead. So:
> **Apple Silicon → Homebrew (2A/3A). Intel → MacPorts (2B/3B).** Check which you have with `uname -m`
> (`arm64` = Apple Silicon, `x86_64` = Intel). Every other step is the same on both.

### Step 0: Before you start
- [ ] macOS fully updated (Apple menu → System Settings → General → Software Update).
- [ ] Signed in to the **App Store** with an Apple ID (needed if you install Pages/Word from there).
- [ ] Know which GitHub account gets push access, and Lynn's name + email for commit attribution.
- [ ] A stable internet connection (first Homebrew/MacPorts + `uv sync` pull a fair bit down).

### Step 1: Xcode Command Line Tools (git, compilers)
The Homebrew installer in Step 2A installs these automatically; MacPorts (Step 2B) needs them first. To do it explicitly:
```bash
xcode-select --install
```
Click through the dialog and wait for it to finish.

### Step 2A: Apple Silicon Mac – Homebrew (the package manager)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then add it to the PATH (on Apple Silicon Homebrew lives in `/opt/homebrew`; the installer also prints these two
lines — use its version if different):
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```
Check it works:
```bash
brew --version
```

### Step 2B: Intel Mac – MacPorts (the package manager)
Homebrew no longer supports Intel Macs, so use [MacPorts](https://www.macports.org) instead. It needs the Xcode
Command Line Tools from Step 1 (do that step first, and accept the Xcode licence: `sudo xcodebuild -license accept`).
- [ ] Download the MacPorts **`.pkg` installer for the Mac's macOS version** (e.g. "macOS 15 Sequoia") from
      <https://www.macports.org/install.php> and double-click it to install.
- [ ] Open a **new** Terminal window (the installer adds `/opt/local/bin` to the PATH in `~/.zprofile`) and check:
```bash
port version
```
If `port` is not found, add it by hand and try again:
```bash
echo 'export PATH="/opt/local/bin:/opt/local/sbin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```
Bring MacPorts up to date:
```bash
sudo port selfupdate
```

### Step 3A: Apple Silicon Mac – command-line tools (Homebrew)
```bash
brew install git gh uv hugo pandoc poppler
```
- **git** – version control (also came with the Command Line Tools; the package manager keeps it current).
- **gh** – GitHub CLI, used in Step 5 to give the machine push access the easy way.
- **uv** – Python tool/venv manager; pulls Python 3.13, ruff, mypy and pytest itself in Step 7.
- **hugo** – builds the website (Homebrew's hugo is the *extended* build; the site's styles are plain CSS so the
  standard build is also fine).
- **pandoc** – converts between Word and the site's text (proofreading + new-article workflows).
- **poppler** – reads and renders PDFs (`pdftotext`, `pdftoppm`, `pdfimages`).

Confirm they're all on the PATH:
```bash
for t in git gh uv hugo pandoc pdftoppm; do printf '%-8s ' "$t"; command -v "$t" || echo MISSING; done
hugo version   # Homebrew's build says "+extended"; MacPorts' may not, which is fine for this site
```

### Step 3B: Intel Mac – command-line tools (MacPorts)
```bash
sudo port -N install git gh uv hugo pandoc poppler
```
Same tools as Step 3A (see the list above). **This can take a long time** (up to an hour or more) because MacPorts
may compile some of them (pandoc and poppler especially) from source on an Intel Mac. Start it before Lynn needs the
machine and leave it running. Then run the same check as Step 3A:
```bash
for t in git gh uv hugo pandoc pdftoppm; do printf '%-8s ' "$t"; command -v "$t" || echo MISSING; done
hugo version
```

### Step 4: Claude Code (the desktop app Lynn will use)
- [ ] Download the **Claude desktop app** for macOS from <https://claude.ai/download> and drag it to Applications.
- [ ] Open it and **sign in** with Lynn's Claude account (the one on the plan that includes Claude Code).
- [ ] Confirm the app has a **Code** tab (this is what she'll work in). No VS Code needed.

### Step 5: GitHub access (so changes can be published)
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

### Step 6: Get the website
Clone the repo into a sensible spot (e.g. a `dev` folder in her home directory):
```bash
mkdir -p ~/dev && cd ~/dev
gh repo clone NickElseySpelloC/Elseyworks
cd Elseyworks
```

### Step 7: Install the site's Python tools
```bash
cd ~/dev/Elseyworks
./scripts/setup.sh
```
This runs `uv sync`, which fetches Python 3.13 and the dev tools (ruff, mypy, pytest).
> **Note:** `scripts/setup.sh` detects Homebrew or MacPorts and installs hugo/poppler/pandoc/uv/git with
> whichever it finds (already-installed tools are skipped). It does not install `gh` — that's why `gh` is in the
> manual install at Step 3A/3B.

### Step 8: Microsoft Word (for the proofreading workflow)
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

### Step 9: Prove the whole toolchain works
From `~/dev/Elseyworks`:
```bash
uv run pytest -q                        # expect: all pass (a few may skip if a tool is missing)
uv run ruff check .                     # expect: All checks passed!
uv run python scripts/check_content.py  # expect: All NN articles look good.
./scripts/preview.sh                     # prints http://localhost:1313/
```
- [ ] Open **http://localhost:1313/** in a web browser (Safari is fine) and confirm the site loads and looks right.
- [ ] Stop the preview when done: `./scripts/stop-preview.sh`

### Step 10: Open the project in Claude Code
- [ ] In the Claude desktop app → **Code** tab, open the folder `~/dev/Elseyworks`.
- [ ] Confirm the assistant picks up the project instructions and skills: ask it **"what can you do?"** — it should
      run the **help** skill and list add / change / proofread / add-article / look-and-feel / publish.
- [ ] Do a quick **dry run** with Lynn watching: ask it to show a preview, make a tiny reversible change, preview
      again, then discard it (don't publish the throwaway).

### Step 11: Hand-over to Lynn
- [ ] Show her how to open the Claude desktop app and the Code tab, and that she just types in plain English.
- [ ] Point her at **"what can you do?"** / **"I need help"** as her starting point.
- [ ] Agree what she does if something looks wrong: **call Nick** (the assistant is told to say this too).
- [ ] Optional: print a one-page "how to talk to your assistant" sheet (can be generated from the `help` skill).

### Everything installed – quick reference
| Tool | Why | Installed in |
|------|-----|--------------|
| Homebrew (Apple Silicon) or MacPorts (Intel) | package manager | Step 2A / 2B |
| git, gh | version control + GitHub access/publishing | Step 3A/3B, 5 |
| uv | Python + ruff/mypy/pytest + Python 3.13 | Step 3A/3B, 7 |
| hugo | builds the website | Step 3A/3B |
| pandoc | Word ↔ site text | Step 3A/3B |
| poppler | reads/renders PDFs | Step 3A/3B |
| Claude desktop app | what Lynn uses | Step 4 |
| Microsoft Word | proofreading `.docx` with tracked changes | Step 8 |

_Not installing:_ VS Code, Node (the desktop app doesn't need it), Xcode (full IDE — Command Line Tools are enough).

---

# Part 3 – How to use your website assistant

Hello Lynn! This part is just for you. Your website is looked after by an assistant you chat with
in plain English – like emailing a helpful editor's assistant. There are no commands to learn and nothing
technical to do. If you can type a message, you can run your website.

## Starting up

1. Open the **Claude** app (it's in your Applications folder, and in the Dock).
2. Click the **Code** tab at the top.
3. Choose the **Elseyworks** project if it isn't already showing.
4. Type what you'd like, in your own words, and press Enter.

Not sure where to start? Type **"What can you do?"** and the assistant will give you a friendly list.

## What you can ask for

| You could say… | What happens |
|---|---|
| "Show me the site." | A private preview of your website opens, so you can see it exactly as visitors will. Only you can see it. |
| "Add this article." (and share the file) | Give the assistant a Word document or a PDF (a scan is fine) and any photos. It builds a new page and shows you a preview. |
| "Can you change the date on the Rome article?" | Fixes a detail, swaps a picture, changes a title, or takes an article down. |
| "Please check the Verona article for typos." | The assistant looks for spelling and scanning mistakes only – it never touches your wording. |
| "I'd like the headings a bit bigger." | Small changes to colours, fonts, spacing and the wording of menus. |
| "Looks good, publish it." | Puts your approved changes live on elseyworks.com. |

You don't need special phrases – just say what you want, the way you'd tell a person.

## Adding a new article

1. Tell the assistant: **"Add this article,"** and share the Word document or PDF. Share any photos too.
2. If it's a scan of a printed page, the assistant types it up first and opens a **Word document** for you to read
   through. Fix anything you like in Word and save it. Whatever you change is used exactly as you wrote it.
3. The assistant builds the page and shows you a preview. It may ask a quick question, such as which
   subject it belongs under, and will suggest an answer.
4. Look it over. Ask for any changes you'd like.
5. When you're happy, say **"Publish it."**

## Checking an article for typos

Many of your articles were scanned in, so the odd letter may have gone astray. Ask the assistant to check one.
For a few mistakes it simply tells you what it fixed. For a longer list it opens a **Word document** with its
suggestions marked as tracked changes:

- **Accept** the ones you agree with, and **reject** any you don't.
- Save the document, then tell the assistant you're done.

It only ever fixes genuine mistakes, never your writing style, and it will ask you if it's unsure
(for example a name or a number).

## Looking at the preview

Say **"Show me the site"** at any time. The preview opens in your web browser. Click around as a visitor would.
Nothing you see in the preview is public until you say so. When you've finished, the assistant
closes the preview for you.

## Publishing

When you've seen the preview and you're happy, say **"Looks good, publish it."** The assistant puts the changes on
your website, and they usually appear within a minute or two. It will **never** publish until you've looked and
said yes.

## Telling the assistant your preferences

If there's something you always (or never) want – "I don't like full stops at the end of headings" – just say so.
The assistant will apply it from then on and keep a note of it in your style guide.

## If something looks wrong

Don't worry – nothing goes live without your approval, and changes can be undone. If the assistant says it
can't fix something, or the website looks odd, **call Nick** and tell him what you asked for and what you saw.
