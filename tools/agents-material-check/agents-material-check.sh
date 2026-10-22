#!/usr/bin/env bash
# The agent material agrees with its pinned bundle (agents-md-schema.md rules 2, 5 and 8): runs the
# bundle's own file check, render check and digest verification at the ref .agents/manifest.yaml pins.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
ref=$(sed -n 's/^ *ref: *\([0-9a-f]\{40\}\).*/\1/p' .agents/manifest.yaml | head -1)
[ -n "$ref" ] || { echo "FAIL: no pinned ref in .agents/manifest.yaml"; exit 1; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git -C "$tmp" init --quiet
git -C "$tmp" fetch --quiet --depth 1 https://github.com/exeris-systems/exeris-agents "$ref"
git -C "$tmp" checkout --quiet FETCH_HEAD
status=0
python3 -I "$tmp/tools/agents_file_check.py" --root . || status=1
python3 -I "$tmp/tools/agents_render.py" --root . --check || status=1
python3 -I "$tmp/tools/agents_bundle.py" verify --root . || status=1
exit "$status"
