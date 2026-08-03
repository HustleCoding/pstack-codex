---
name: no-comments
description: Spawn an independent comment reviewer, fix accepted findings, and offer enforceable replacements for comments that claim constraints. Use for /no-comments or before code review.
---

# No comments

Read `references/comment-reviewer.md` in full. Spawn one read-only Codex collaboration agent with those instructions and the caller's files or diff. If no scope exists, use the working tree and current diff against the base branch, default `main`.

## Review the report

Inspect the report and the actual diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat intentional kept code as guilty. Restore a deletion only when the scoped evidence proves an exception. Audit missed lint and TypeScript suppressions.

Before accepting an ambiguous deletion or keep, use the **how** or **why** skill on the named symbol. Rerun one rejected review with the failure named. If the second report still violates the contract, report the review as failed.

## Act on accepted findings

If the caller asked only for review, diagnosis, or a report, stop after reporting accepted findings. Apply changes only when the caller authorized edits or when this skill runs inside an already authorized change workflow.

Delete dead comments and trivial workarounds directly. If a fix changes a code boundary, run the **architect** skill once and implement the smallest root-cause fix in scope. Leave out-of-scope causes open.

For comments that claim `do not remove`, `do not change wording`, or an approval requirement, offer the cheapest type, runtime check, test, or CI rule that can enforce the constraint. Wait for approval only when encoding the constraint expands scope or changes external state. Otherwise encode it and remove the comment.

Report the deletion count, restored comments, reruns, fixes, enforcement offers, enforced constraints, and open work.
