# Using pstack in Codex

Start a new Codex chat in the repository you want to work on. For substantial work, say `Use poteto-mode` followed by the goal and a check that can pass or fail. For an obvious small edit, ask directly. Installation makes skills available; it does not start workflows or schedule background work.

## Give the agent a checkable task

A useful prompt gives the goal, done check, proof to return, known symptoms, and real constraints. For example:

```text
Use poteto-mode. The CSV export drops its last row since yesterday's deploy.
The failing job is 4812. Reproduce first, then fix it. Done means the
60,000-row fixture exports every row. Show row counts before and after.
```

For a noisy report, first ask the agent to restate the problem in plain words. Share observations and logs, and identify theories as hypotheses. Once the chat has enough context, "continue" is enough. Say "new task" when changing subjects.

The [prompting reference](../skills/poteto-help/references/prompting.md) explains how to steer a run. The [recipes](../skills/poteto-help/references/recipes.md) cover investigation, design, implementation, review, and handoff. `Use poteto-help` returns guidance and a prompt you can send; it does not start the example task.

## Understand and design before changing code

When the cause is unclear, ask for a read-only investigation with findings, evidence, and hypotheses. `how` traces current behavior; `why` investigates the reasons behind it. `recall` can recover scoped prior context from available history. `teach` explains the mechanism and tradeoffs in plain language.

For consequential design choices, ask for a few runnable prototypes. Use screenshots for UI, or real outputs and measurements for behavior. For a shared package or API, write the caller's tutorial first and work back to the implementation. `architect` handles boundaries and types; `arena` compares alternatives. `swarm` covers independent slices with bounded workers. `interrogate` challenges a diff without applying its findings automatically.

Once the design is settled, ask poteto-mode to turn it into small verifiable PRs through the Multi-phase plan playbook. Planning returns a plan; execution needs a request to proceed. For a compatibility migration, state whether output must match exactly, including existing bugs.

## Make verification repeatable

Match proof to the changed behavior: run the real CLI, drive the UI flow, replay an input, compare profiles, or read back persisted state. Ask for an artifact you can inspect. A green build alone does not prove the user-visible result. If a fix is already merged, repeat the relevant check on main.

Use an existing project verification harness when available. If none exists, `create-verification-skill` can create a project-local harness when installed and requested. Verify it end to end before relying on it. Keep its feature map current with `maintain-verification-skill` when available; request a scheduled review if that cadence helps your project.

Repeated manual app-driving scripts can become a small control CLI with useful help, machine-readable output, actionable errors, and dry runs for destructive operations. Seeded data and one repeatable development command make verification easier for every agent.

For performance claims, run `benchmark-checklist`. It checks the limiting resource, production tuning, physical limits, correctness, alternating measurements, end-to-end impact, and whether the timed work actually ran. An unexplained or untuned comparison is inconclusive. Runtime forensics diagnoses a live process; Trace forensics maps an existing profile to source. Ask for diagnosis only when a fix is not yet wanted.

## Give longer runs clear scope

Before leaving a task unattended, observe a successful run, give the agent the verification tools it needs, and make each stage produce evidence. State a checkable done condition, allowed actions, review gates, and what to do if blocked. Request a decision log for later review.

Give concurrent writers separate worktrees or output paths. Codex collaboration workers share a machine, so worktrees alone do not isolate ports or build caches. Respect the configured concurrency cap and give conflicting processes separate resources.

For later or recurring work, explicitly request a Codex heartbeat automation when available. It should stay quiet while nothing meaningful changes and report completion, failure, or required input. Confirm that it was actually saved. A local run does not imply that work continues while the machine is unavailable.

Say "pause safely" to request a checkpoint and resume note. On return, ask poteto-mode to take over the branch and read that note. "Keep going" continues the current authorized work. A plan, an overnight prompt, or installing pstack does not itself authorize external messages or deployment.

PR status, merge-ready, and merged are different outcomes. "Check on PR 123" makes one status pass. "Babysit PR 123 until merge-ready" follows checks and review feedback. "Merge PR 123" grants that merge scope.

## Fix repeated mistakes in the repository

`correct` finds repeated mistake classes in commits and review history. It prefers architecture and data structures that prevent the mistake, then types or checks, then tests, and finally written rules. Each new check should reject a real past mistake. `reflect` instead proposes skill improvements from a session; proposals need authorization before application.

Add skills or checks in response to demonstrated failures. For a substantial skill change, ask for an evaluation against realistic tasks and inspect the outputs yourself. A structural skill validator checks packaging, not future agent judgment.

## Control the models and cost

The parent model is selected in Codex. The [configuration](../config.example.md) supplies compatible child routes and concurrency limits. Existing global choices survive installation. Smaller reasoning budgets and shorter panels can reduce work; inheritance uses the parent's model and is not inherently cheaper.

`setup-pstack` can change models and reasoning budgets when requested. Balanced preserves per-role efforts; unlimited, large, medium, and small target max, xhigh, high, and medium. Unsupported efforts fall back within the same verified model at or below the target. A missing configuration is an opportunity to offer setup, not a reason to block the original question.
