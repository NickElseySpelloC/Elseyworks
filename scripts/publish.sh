#!/usr/bin/env bash
# Check the site, then commit everything and push it live.
# Usage: scripts/publish.sh "Add article: The Wild West"
set -euo pipefail
cd "$(dirname "$0")/.."

MESSAGE="${1:-Update site content}"

uv run python scripts/check_content.py
hugo --gc --minify --destination /tmp/elseyworks-build >/dev/null
rm -rf /tmp/elseyworks-build

if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing has changed - there is nothing to publish."
  exit 0
fi

git add -A
git commit -m "${MESSAGE}"
git pull --rebase --quiet
git push
echo "Published. The live site updates in about two minutes."
