#!/usr/bin/env bash
# Stop the local preview server, if running.
pkill -f "hugo server --port 1313" && echo "Preview stopped." || echo "No preview was running."
