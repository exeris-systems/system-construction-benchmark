# Sourced by the checks: the commit a pull request is compared against. CI checks the pull request
# out with full history; GITHUB_BASE_REF names its base branch. Run locally, the base is origin/main.
base_ref="origin/${GITHUB_BASE_REF:-main}"
if ! git rev-parse --verify --quiet "$base_ref" >/dev/null; then
  git fetch --quiet origin "${GITHUB_BASE_REF:-main}" || true
fi
merge_base=$(git merge-base "$base_ref" HEAD)
