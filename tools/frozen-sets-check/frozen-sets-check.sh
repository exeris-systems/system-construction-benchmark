#!/usr/bin/env bash
# A frozen set is not edited in place (docs/repo-review-rules.md B1). Everything under
# contract/user-stories/ belongs to the user-story procedure; a change to an existing file there is
# allowed only together with a new version line in its procedure.md.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
. tools/base-ref.sh
frozen="contract/user-stories/"
edited=$(git diff --name-only --diff-filter=MDRT "$merge_base" HEAD -- "$frozen")
if [ -z "$edited" ]; then
  echo "OK: no existing file of a frozen set changed"
  exit 0
fi
version() { git show "$1:${frozen}procedure.md" 2>/dev/null | grep -m1 '^Version:' || true; }
before=$(version "$merge_base")
after=$(version HEAD)
if [ -n "$after" ] && [ "$before" != "$after" ]; then
  echo "OK: frozen files changed with a new procedure version ('$before' -> '$after'):"
  echo "$edited"
  exit 0
fi
echo "FAIL: files of a frozen set changed without a new procedure version ('$before'):"
echo "$edited"
exit 1
