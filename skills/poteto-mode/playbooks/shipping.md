### Shipping

**Verify what lands and stop at the first gap.** Use only when the user explicitly asks to merge, land, ship, or enable merge when ready.

1. Spawn one independent Codex collaboration verifier per PR. Each verifier checks parent versus head on the real behavior and returns `PASS`, `PASS+NOTES`, or `FAIL` for the exact head SHA.
2. Walk from the lowest unmerged PR and stop at the first missing or failing verdict. Only the contiguous passing run can land.
3. Compare `git patch-id` when a restack changed SHAs. Re-verify every patch that changed.
4. Use the repository's established merge queue or stacking tool. If none exists, merge bottom-up with `gh pr merge` and re-check the next PR after every merge. Do not arm GitHub auto-merge on child PRs whose base is another feature branch.
5. Confirm merge or queue state from the authoritative service after every write. A successful command response is not proof that the PR merged or queued.
6. Once a queue drains, stop changing branches. Monitor it with `scripts/watch-pr/watch-pr` and bounded waits until the verified ceiling lands or a blocker appears.
7. Stop at the ceiling. Extending the verified run requires a new verification pass.

**Reply:** the verified run, ceiling, verdict and head SHA per PR, merge mechanism, confirmed landed PRs, and next gap.
