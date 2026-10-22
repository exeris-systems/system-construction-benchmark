#!/usr/bin/env bash
# No credential and no session link (docs/repo-review-rules.md B3): scans the lines a pull request
# adds and the messages of its commits.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. tools/base-ref.sh
keys='AIza[0-9A-Za-z_-]{30,}|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[abpr]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
session='claude\.ai/code/session_|Claude-Session:'
found=0
# The scanner and the rule that names the patterns contain them by definition; commit messages are
# still scanned without exception.
added=$(git diff --unified=0 "$merge_base" HEAD -- . ':(exclude).agents/vendor' \
  ':(exclude)tools/credential-scan/credential-scan.sh' ':(exclude)docs/repo-review-rules.md' \
  | grep -E '^\+[^+]' || true)
if hits=$(printf '%s\n' "$added" | grep -nE "$keys|$session"); then
  echo "FAIL: added lines carry a credential or a session link:"
  printf '%s\n' "$hits" | cut -c1-120
  found=1
fi
if hits=$(git log --format='%h %B' "$merge_base"..HEAD | grep -nE "$session|$keys"); then
  echo "FAIL: commit messages carry a credential or a session link:"
  printf '%s\n' "$hits" | cut -c1-120
  found=1
fi
[ "$found" -eq 0 ] && echo "OK: no credential or session link in added lines or commit messages"
exit "$found"
