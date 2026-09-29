---
name: publish
description: Put Lynn's approved changes live on elseyworks.com. Only use after Lynn has seen the preview and clearly said yes.
---

Follow `CLAUDE.md`. Only continue if Lynn has looked at the preview **and** said to publish (e.g. "looks good",
"publish it"). If unsure, ask: "Shall I put this live now?"

1. Run `scripts/publish.sh "<short description, e.g. Add article: The Wild West>"`. It checks the site,
   saves the changes and sends them live.
2. If the check reports problems, fix them (or, if it's about content she must decide, ask her in plain words),
   then run it again. If saving/sending fails for any other reason, don't show her the error: tell her the
   publish didn't go through and that Nick will need to help.
3. Tell her: it's published, and it should show at https://elseyworks.com within a couple of minutes
   (a refresh may be needed). Offer to stop the preview with `scripts/stop-preview.sh` only if asked.
