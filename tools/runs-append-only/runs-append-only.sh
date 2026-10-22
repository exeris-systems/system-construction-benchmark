#!/usr/bin/env bash
# Run records are append-only (docs/repo-review-rules.md B2): a pull request may add files under
# runs/, never modify, rename or delete one.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. tools/base-ref.sh
changed=$(git diff --name-status --diff-filter=MDRTC "$merge_base" HEAD -- runs/)
if [ -n "$changed" ]; then
  echo "FAIL: existing run records changed (only additions are allowed under runs/):"
  echo "$changed"
  exit 1
fi
echo "OK: runs/ changes are additions only ($(git diff --name-only --diff-filter=A "$merge_base" HEAD -- runs/ | wc -l) file(s) added)"
