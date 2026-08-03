### Worktree and simulator cleanup

**Audit first. Delete only confirmed targets.** Use to reclaim disk from stale worktrees, simulators, and caches.

1. Record `df -h /`. Run `scripts/worktree-audit.sh`. It discovers paths from `git worktree list` and reports size, age, merge state, dirty state, remote state, and PR state. It never deletes.
2. Treat the suggested bucket as evidence, not permission. Check active Codex tasks or ask the user for the active set when task-history tools are unavailable.
3. Inspect every uncertain worktree. A collaboration agent may inspect one bounded task or worktree read-only. An active task can own sibling arena or repro worktrees that do not appear in its title.
4. Pause for tracked uncommitted work or an active task. Show the diff before any destructive decision. Name untracked files before treating them as disposable.
5. Remove only the confirmed set with explicit paths. Prefer `git worktree remove <path>`. Use `--force` only when the user approved deletion of the remaining state. Then run `git worktree prune` and re-list.
6. For simulators, inspect before deleting unavailable or testing clones. Treat Xcode data and package caches as separate confirmed targets. Never broaden a cleanup target through an unresolved variable, glob, home directory, or workspace root.
7. Record `df -h /` again and verify every removed path is absent.

**Reply:** disk before and after, space reclaimed, removed targets, recoverability, and held targets with reasons.
