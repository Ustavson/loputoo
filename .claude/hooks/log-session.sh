#!/bin/bash
# SessionEnd hook: append a mechanical entry to LOG.md listing commits and
# uncommitted changes since the last auto entry. Skips if nothing changed.
set -u

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

state=.claude/.last-logged-head
head=$(git rev-parse --verify -q HEAD || echo none)
last=$(cat "$state" 2>/dev/null || echo "")

# Uncommitted changes, ignoring LOG.md itself (this hook edits it every time).
changes=$(git status --porcelain -- . ':(exclude)LOG.md')

commits=""
if [ "$head" != none ] && [ "$head" != "$last" ]; then
  if [ -n "$last" ] && git cat-file -e "${last}^{commit}" 2>/dev/null; then
    commits=$(git log --reverse --format='- `%h` %s' "${last}..HEAD")
  else
    commits=$(git log --reverse --format='- `%h` %s' -n 10 HEAD)
  fi
fi

[ -z "$changes" ] && [ -z "$commits" ] && exit 0

{
  echo
  echo "### $(date '+%Y-%m-%d %H:%M') · session end (auto)"
  if [ -n "$commits" ]; then
    echo
    echo "Commits:"
    echo "$commits"
  fi
  if [ -n "$changes" ]; then
    n=$(printf '%s\n' "$changes" | wc -l | tr -d ' ')
    echo
    echo "Uncommitted ($n):"
    printf '%s\n' "$changes" | head -n 30 | sed -E 's/^(..) (.*)$/- `\1` \2/'
    [ "$n" -gt 30 ] && echo "- … and $((n - 30)) more"
  fi
} >> LOG.md

echo "$head" > "$state"
exit 0
