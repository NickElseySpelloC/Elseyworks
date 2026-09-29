#!/usr/bin/env bash
# Start (or reuse) the local preview of the site and print its address.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT=1313
if curl -fs "http://localhost:${PORT}/" >/dev/null 2>&1; then
  echo "Preview already running: http://localhost:${PORT}/"
  exit 0
fi

nohup hugo server --port "${PORT}" --disableFastRender >/tmp/elseyworks-preview.log 2>&1 &
for _ in $(seq 1 30); do
  if curl -fs "http://localhost:${PORT}/" >/dev/null 2>&1; then
    echo "Preview running: http://localhost:${PORT}/"
    exit 0
  fi
  sleep 1
done
echo "The preview did not start. Log:" >&2
tail -20 /tmp/elseyworks-preview.log >&2
exit 1
