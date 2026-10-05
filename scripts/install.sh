#!/usr/bin/env bash

set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
codex_home=${CODEX_HOME:-"$HOME/.codex"}
skills_dir="$codex_home/skills"
dry_run=false

if [[ $# -gt 1 || ( $# -eq 1 && $1 != "--dry-run" ) ]]; then
  echo "usage: install.sh [--dry-run]" >&2
  exit 2
fi
if [[ ${1:-} == "--dry-run" ]]; then
  dry_run=true
fi

python3 "$repo_root/scripts/audit.py"
if $dry_run; then
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    if [[ -e "$skills_dir/$name" ]]; then
      echo "would back up and replace: $name"
    else
      echo "would install: $name"
    fi
  done < "$repo_root/manifest.txt"
  exit 0
fi

mkdir -p "$codex_home"
stage_dir=$(mktemp -d "$codex_home/.pstack-stage.XXXXXX")
backup_dir=""
installed=()
replaced=()
state_saved=false
finished=false

cleanup() {
  result=$?
  trap - EXIT
  set +e
  if ! $finished; then
    restore_failed=false
    for name in "${installed[@]-}"; do
      [[ -n "$name" ]] || continue
      rm -rf "$skills_dir/$name" || restore_failed=true
    done
    for name in "${replaced[@]-}"; do
      [[ -n "$name" ]] || continue
      mv "$backup_dir/$name" "$skills_dir/$name" || restore_failed=true
    done
    if $state_saved; then
      for name in manifest.txt config.md; do
        if [[ -f "$backup_dir/.pstack-state/$name" ]]; then
          cp -p "$backup_dir/.pstack-state/$name" "$codex_home/pstack/$name" || restore_failed=true
        else
          rm -f "$codex_home/pstack/$name" || restore_failed=true
        fi
      done
    fi
    if $restore_failed; then
      echo "installation failed; rollback incomplete; recover from $backup_dir" >&2
    else
      echo "installation failed; previous catalog restored" >&2
    fi
  fi
  rm -rf "$stage_dir"
  exit "$result"
}
trap cleanup EXIT

mkdir -p "$stage_dir/skills"
while IFS= read -r name; do
  [[ -n "$name" ]] || continue
  mkdir -p "$stage_dir/skills/$name"
  tar -C "$repo_root/skills/$name" --exclude=node_modules --exclude=__pycache__ -cf - . | tar -C "$stage_dir/skills/$name" -xf -
done < "$repo_root/manifest.txt"
python3 "$repo_root/scripts/audit.py" --skills-root "$stage_dir/skills"

mkdir -p "$skills_dir" "$codex_home/backups" "$codex_home/pstack"
backup_dir=$(mktemp -d "$codex_home/backups/pstack-codex-$(date -u +%Y%m%dT%H%M%SZ).XXXXXX")
mkdir -p "$backup_dir/.pstack-state"
for name in manifest.txt config.md; do
  if [[ -f "$codex_home/pstack/$name" ]]; then
    cp -p "$codex_home/pstack/$name" "$backup_dir/.pstack-state/$name"
  fi
done
state_saved=true

while IFS= read -r name; do
  [[ -n "$name" ]] || continue
  if [[ -e "$skills_dir/$name" ]]; then
    mv "$skills_dir/$name" "$backup_dir/$name"
    replaced+=("$name")
  fi
  mv "$stage_dir/skills/$name" "$skills_dir/$name"
  installed+=("$name")
done < "$repo_root/manifest.txt"

cp "$repo_root/manifest.txt" "$codex_home/pstack/manifest.txt"
if [[ ! -f "$codex_home/pstack/config.md" ]]; then
  cp "$repo_root/config.example.md" "$codex_home/pstack/config.md"
fi
python3 "$repo_root/scripts/audit.py" --skills-root "$skills_dir"
finished=true

echo "installed pstack skills into $skills_dir"
echo "backup: $backup_dir"
echo "start a new Codex task to load the refreshed skill catalog"
