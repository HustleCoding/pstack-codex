### Orchestrate

**Own the program, not the code.** Use for a multi-day project with many independently verifiable units. Use Autonomous run when one agent can finish within the current task budget.

## Durable state

Create one task store outside writer scopes:

- `preferences.md` holds standing orders.
- `units.tsv` holds one row per unit and its state.
- `ledger.tsv` holds verdicts keyed by PR and head SHA.
- `frontier.json` holds the ordered PR list, branches, head SHAs, generation, and lowest unmerged PR.
- `gates.md` holds genuine user decisions with options and a safe default.
- `decisions.tsv` follows the **show-me-your-work** skill.
- `status.md` is regenerated from the tables at every checkpoint.

## Roles

- The coordinator frames work, writes briefs, drains completions, owns user reports, and makes judgment calls. It does not write application code.
- A sub-coordinator owns one track only when the parent can no longer drain that track efficiently.
- Workers and verifiers are bounded Codex collaboration agents. Give each writer an isolated worktree or branch. Keep the durable store outside writer scope.
- Use configured model routes only when the active collaboration schema exposes model and reasoning controls. Otherwise inherit the session runtime.

## Brief contract

Every worker receives the goal, writable and forbidden scope, source pointers, checkable acceptance criteria, exact verification commands, a timebox, forbidden operations, report shape, and current standing orders. Missing fields are a refuse-to-spawn condition.

## Run

1. State a countable done predicate, unit count, rough effort, track boundaries, and wall-clock budget. Route smaller work to Autonomous run.
2. Create the durable state. Discover existing PRs with `gh`, freeze their order in `frontier.json`, and record head SHAs. Use a repository stacking tool only when it is already installed and configured.
3. Push one representative unit through brief, implementation, verification, PR placement, ledger entry, and merge-ready state. Fix the contract from pilot evidence.
4. Spawn a rolling window of workers up to the configured collaboration limit. Refill after completions. Relay upstream reports into dependent briefs.
5. Drain completions at bounded checkpoints. Classify each result, update `units.tsv` and `ledger.tsv`, regenerate `status.md`, then start the next ready work.
6. Integrate continuously through one topology writer. Recompute `frontier.json` after every merge, base change, or new head SHA. A new SHA voids its old verdict.
7. Close only when every unit is terminal, the done predicate passes on the real artifact, and every current PR head has a ledger verdict.

## Liveness and safety

- Check liveness with collaboration or task-coordination status. Never restart an idle agent merely to ask for status.
- Retry network failures as-is. Retry a tool failure through another configured route when available. Split work after a context or memory cap. Stop after two failed retries and replan.
- After a Codex restart, reconcile from durable state, PRs, branches, and head SHAs. Do not trust stale agent identifiers.
- Escalate irreversible writes, product decisions, and program-level dead ends. Route around ordinary retries, CI triage, and format fixes.

**Reply:** the predicate count, tracks, frontier with SHAs, verdict summary, abandoned units, user gates, store path, and decision-trail path.
