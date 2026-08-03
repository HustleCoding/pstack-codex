### Autopilot-full

**Own the verdicts, not each PR.** Use for a queue of independent PRs that the user explicitly authorized Codex to drive through merge.

1. Mark items the user reserved. State the protocol and wait only when the user asked for a plan rather than execution.
2. Spawn one Codex collaboration agent per independent PR. Give every writer an isolated worktree, exact scope, acceptance checks, and the current pstack standing orders. Each owner builds, verifies, applies **unslop** and **no-comments**, addresses review findings, and drives its PR to merge-ready.
3. Keep owners parallel only across disjoint branches. Serialize overlapping work. Use the repository's existing stacking workflow only when the project already has one.
4. At each merge-ready head SHA, run the **swarm** skill. Re-run gates at that SHA, exercise the load-bearing behavior through the installed verification surface, and audit the diff and receipts. A new SHA voids the verdict unless `git patch-id` proves the patch is unchanged.
5. Merge only when the user granted merge authority and the clean verdict still names the current head. Otherwise stop at merge-ready. Never infer merge permission from a request to build, review, or babysit.
6. Monitor owners with collaboration status and bounded waits. Audit progress and protocol adherence at each wake. Collect each owner's decision trail.
7. Send a zero-write hold to every owner when the user says stop.

**Reply:** the PR owners, states, head SHAs, verifier verdicts, merges, user-held items, and decision-trail paths.
