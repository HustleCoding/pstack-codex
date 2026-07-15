#!/usr/bin/env bash

set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
codex_home=${CODEX_HOME:-"$HOME/.codex"}
skills_dir="$codex_home/skills"
backup_dir="$codex_home/backups/pstack-codex-$(date -u +%Y%m%dT%H%M%SZ)"
dry_run=false

if [[ ${1:-} == "--dry-run" ]]; then
  dry_run=true
fi

mkdir -p "$skills_dir"

while IFS= read -r name; do
  [[ -n "$name" ]] || continue
  source_dir="$repo_root/skills/$name"
  target_dir="$skills_dir/$name"

  if [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "missing source skill: $source_dir" >&2
    exit 1
  fi

  if $dry_run; then
    if [[ -e "$target_dir" ]]; then
      echo "would back up and replace: $name"
    else
      echo "would install: $name"
    fi
    continue
  fi

  if [[ -e "$target_dir" ]]; then
    mkdir -p "$backup_dir"
    mv "$target_dir" "$backup_dir/$name"
  fi

  mkdir -p "$target_dir"
  cp -R "$source_dir/." "$target_dir/"
done < "$repo_root/manifest.txt"

if $dry_run; then
  exit 0
fi

mkdir -p "$codex_home/pstack"
cp "$repo_root/manifest.txt" "$codex_home/pstack/manifest.txt"
if [[ ! -f "$codex_home/pstack/config.md" ]]; then
  cp "$repo_root/config.example.md" "$codex_home/pstack/config.md"
fi

python3 "$repo_root/scripts/audit.py" --skills-root "$skills_dir"

echo "installed pstack skills into $skills_dir"
if [[ -d "$backup_dir" ]]; then
  echo "backup: $backup_dir"
fi
echo "start a new Codex task to load the refreshed skill catalog"

