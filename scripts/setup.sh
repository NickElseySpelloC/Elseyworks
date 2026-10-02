#!/usr/bin/env bash
# One-time setup for a new computer (macOS). Safe to run again.
# Uses Homebrew (Apple Silicon Macs) or MacPorts (Intel Macs, where Homebrew is no longer supported).
set -euo pipefail
cd "$(dirname "$0")/.."

# MacPorts installs to /opt/local; make sure it is on the PATH for this run.
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"

if command -v brew >/dev/null; then
    brew install hugo poppler pandoc uv git
elif command -v port >/dev/null; then
    sudo port install hugo poppler pandoc uv git
else
    echo "No package manager found. Install Homebrew (Apple Silicon Mac) or MacPorts (Intel Mac) first - see README.md, Part 2, Step 2."
    exit 1
fi

uv sync
echo "Setup complete."
