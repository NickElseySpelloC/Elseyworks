#!/usr/bin/env bash
# One-time setup for a new computer (macOS). Safe to run again.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v brew >/dev/null || { echo "Homebrew is required: https://brew.sh"; exit 1; }
brew install hugo poppler pandoc uv git
uv sync
echo "Setup complete."
