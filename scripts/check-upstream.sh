#!/usr/bin/env bash

set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
upstream_repo=https://github.com/cursor/plugins.git
base=$(tr -d '[:space:]' < "$repo_root/UPSTREAM_COMMIT")
head=$(git ls-remote "$upstream_repo" refs/heads/main | awk '{print $1}')

if [[ -z "$base" || -z "$head" ]]; then
  echo "could not resolve upstream commits" >&2
  exit 1
fi

echo "base=$base"
echo "head=$head"

if [[ "$base" == "$head" ]]; then
  echo "status=up-to-date"
  exit 0
fi

tmp=$(mktemp -d "${TMPDIR:-/tmp}/pstack-upstream.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

git -C "$tmp" init -q
git -C "$tmp" remote add origin "$upstream_repo"
git -C "$tmp" fetch -q --filter=blob:none origin "$base" "$head"

echo "status=upstream-changed"
echo
echo "pstack commits:"
git -C "$tmp" log --oneline "$base..$head" -- pstack || true
echo
echo "pstack files:"
git -C "$tmp" diff --name-status "$base..$head" -- pstack || true

if git -C "$tmp" diff --quiet "$base..$head" -- pstack; then
  echo
  echo "relevance=no-pstack-changes"
else
  echo
  echo "relevance=review-required"
fi

