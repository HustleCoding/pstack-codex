#!/usr/bin/env bash

# Usage: worktree-audit.sh [-b|--base <ref>] [repo-path]
# Without -b, use origin/HEAD, then origin/main, then origin/master.
set -u

base=""
while [ $# -gt 0 ]; do
	case "$1" in
		-b|--base) [ $# -ge 2 ] || { echo "error: $1 needs a ref" >&2; exit 2; }; base="$2"; shift 2 ;;
		-h|--help) sed -n '2,/^set -u/p' "$0" | sed '$d; s/^# \{0,1\}//'; exit 0 ;;
		-*) echo "error: unknown option: $1" >&2; exit 2 ;;
		*) break ;;
	esac
done
[ $# -le 1 ] || { echo "error: expected at most one repo path" >&2; exit 2; }

repo="${1:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$repo" ] || { echo "not in a git repo; pass a repo path" >&2; exit 1; }
cd "$repo" || exit 1
git rev-parse --git-dir >/dev/null 2>&1 || { echo "error: not a git repo: $repo" >&2; exit 1; }

main_wt=$(git worktree list --porcelain | awk '/^worktree /{print $2; exit}')
if [ -z "$base" ]; then
	for candidate in "$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null)" origin/main origin/master; do
		if [ -n "$candidate" ] && git rev-parse --verify --quiet "$candidate^{commit}" >/dev/null; then
			base="$candidate"
			break
		fi
	done
	[ -n "$base" ] || { echo "error: no base ref (origin/HEAD, origin/main, origin/master all missing); pass -b <ref>" >&2; exit 1; }
	echo "warn: no -b given; MERGED checks against $base" >&2
fi

# The explicit refspec refreshes the merge target in single-branch clones too.
case "$base" in
	origin/*) git fetch origin "+refs/heads/${base#origin/}:refs/remotes/$base" --quiet 2>/dev/null \
		|| echo "warn: could not fetch $base; merged state may be stale" >&2 ;;
esac
git rev-parse --verify --quiet "$base^{commit}" >/dev/null 2>&1 || { echo "error: base ref not found: $base" >&2; exit 1; }

prs=$(mktemp)
trap 'rm -f "$prs"' EXIT
prs_known=yes
if ! gh pr list --state all --limit 1000 --json number,state,headRefName > "$prs" 2>/dev/null; then
	prs_known=no
	echo "warn: could not read GitHub PR state; every candidate requires review" >&2
	echo "[]" > "$prs"
fi
now=$(date +%s)

echo "# base: $base"
printf "SIZE\tAGE\tMERGED\tDIRTY\tREMOTE\tPR\tBUCKET\tWORKTREE\n"

git worktree list --porcelain | awk '/^worktree /{print $2}' | while read -r wt; do
	[ "$wt" = "$main_wt" ] && continue

	size=$(du -sh "$wt" 2>/dev/null | awk '{print $1}')
	head=$(git -C "$wt" rev-parse HEAD 2>/dev/null)
	head_ts=$(git -C "$wt" log -1 --format='%ct' HEAD 2>/dev/null || echo 0)
	age=$([ "$head_ts" -gt 0 ] 2>/dev/null && echo "$(( (now - head_ts) / 86400 ))d" || echo "?")
	git merge-base --is-ancestor "$head" "$base" 2>/dev/null && merged=YES || merged=no

	porcelain=$(git -C "$wt" status --porcelain 2>/dev/null)
	if [ -z "$porcelain" ]; then dirty=clean
	elif printf '%s\n' "$porcelain" | grep -qv '^??'; then
		dirty="wip:$(printf '%s\n' "$porcelain" | grep -cv '^??')"
	else
		dirty="scratch:$(printf '%s\n' "$porcelain" | grep -c '^??')"
	fi

	branch=$(git -C "$wt" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "")
	if [ -z "$branch" ]; then remote=detached
	elif git -C "$wt" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
		if [ "$(git -C "$wt" rev-parse "origin/$branch" 2>/dev/null)" = "$head" ]; then
			remote=pushed
		else
			remote="ahead$(git -C "$wt" rev-list --count "origin/$branch..HEAD" 2>/dev/null)"
		fi
	else
		remote=no-remote
	fi

	if [ "$prs_known" = no ]; then
		pr="?"
	else
		pr=$([ -n "$branch" ] && jq -r --arg b "$branch" '.[] | select(.headRefName==$b) | "#\(.number)/\(.state)"' "$prs" 2>/dev/null | head -1)
		[ -n "$pr" ] || pr="-"
	fi

	case "$dirty" in
		wip:*) bucket=hold-wip ;;
		*) case "$pr" in
			*OPEN*) bucket=hold-open-pr ;;
			\?) bucket=review ;;
			*) if [ "$merged" = YES ] || [ "$pr" != "-" ]; then bucket=verify-task-usage; else bucket=review; fi ;;
		esac ;;
	esac

	printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$size" "$age" "$merged" "$dirty" "$remote" "$pr" "$bucket" "$wt"
done | sort -t$'\t' -k1,1 -rh
