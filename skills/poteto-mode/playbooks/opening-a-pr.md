### Opening a PR

Check this gate at the end of every change playbook. Open or update a PR only when the user requested publication, the active task explicitly includes it, or an established repository workflow already placed the work on a PR branch. Otherwise stop after local verification and report that the changes are ready. A request to build or fix does not by itself authorize a PR, push, or external review action.

**Worktree.** Preserve the user's current work. Use a fresh branch or worktree when parallel writers or unrelated dirty changes make isolation necessary. Give every writing agent a separate worktree. Never use a destructive reset to clean up user work.

**Commits.** Commit liberally; rebase into small, ordered commits before opening PRs. Each commit is a future PR: landable, ordered to tell the story. Amend when the fix belongs in a just-made commit; new commit when separable.

**PRs.** Inspect the diff for generated clutter, dead code, and unrelated edits before committing. Apply the **unslop** skill to the PR description and commit bodies. Prefer small ordered PRs. Use the team's stacking tool when present and keep dependencies visible. Run `gh pr view <number>` before referencing PR status. Rebase only when it is safe for the current branch. After opening, monitor checks and review feedback with the GitHub skills or `gh`; push back when feedback drifts from intent.

A child agent that opens a PR runs `interrogate`, inspects the diff for clutter, and returns the URL. The parent owns check and review follow-through.
