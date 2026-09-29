---
name: preview
description: Show Lynn a private preview of her website with any changes that are not yet live.
---

Run `scripts/preview.sh`. Give Lynn the link in plain terms: "Here's a preview of your site, only you can see
this: http://localhost:1313/" (add the article path if there is a specific page). Explain nothing technical.
Mention that the preview only works on her computer. If the preview doesn't start, try
`scripts/stop-preview.sh` then `scripts/preview.sh` again before saying anything to her.
