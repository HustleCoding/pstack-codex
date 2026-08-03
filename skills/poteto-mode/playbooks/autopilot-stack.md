### Autopilot-stack

**Build and verify one linear stack. Never land it.** Use when the user wants a reviewable PR chain and withholds merge authority.

1. Spawn one Codex collaboration agent per bounded change. Give each writer an isolated worktree, exact scope, acceptance checks, and the current pstack standing orders.
2. Owners build, self-verify, apply **unslop** and **no-comments**, address review findings, and report the exact head SHA. Keep disjoint work parallel.
3. Hold one topology writer. Use the repository's existing stacking tool when available. Otherwise create ordinary GitHub PRs whose base branches form one explicit chain. Never force-push a shared branch without user approval.
4. Swarm-verify every proposed stack head. Re-run gates, exercise the real behavior, and audit the diff and receipts. Findings return to the owner. A changed patch requires a fresh verdict.
5. Append only clean, verified PRs. No owner merges, arms auto-merge, or closes a PR.
6. When trunk or a parent changes, restack through the single topology writer. Compare `git patch-id` and re-verify every changed patch.
7. Deliver the chain bottom-up with one verdict per PR. The user reviews and lands it.

**Reply:** the root and tip links, parent relationship, head SHA, verdict for each PR, and parked work.
