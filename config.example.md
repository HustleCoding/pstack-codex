# pstack configuration for Codex

## Parent task

- runtime: Codex
- recommendation: gpt-6.1-sol@high for daily coding and final synthesis
- boundary: pstack cannot change the active task model or reasoning effort; select them when starting the task

## Budget

- profile: balanced
- policy: balanced preserves the per-role efforts below; unlimited, large, medium, and small target max, xhigh, high, and medium respectively, using a supported effort at or below the target
- verified: 2026-10-09 from the active Codex collaboration schema

## Model routes

- default child: gpt-6-luna@medium
- routine work: gpt-6.1-sol@medium
- complex work: gpt-6.1-sol@high
- bug-fix: gpt-6.1-sol@high
- perf-issue: gpt-6.1-sol@high
- hillclimb: gpt-6.1-sol@high
- hardest tasks: gpt-6-astra@high
- how explorers: gpt-6-luna@high
- how explainer: gpt-6.1-sol@high
- why investigators: gpt-6-luna@high
- why synthesizer: gpt-6.1-sol@high
- arena runners: gpt-6-luna@high, gpt-6.1-sol@high, gpt-6-astra@high
- architect runners: gpt-6-luna@high, gpt-6.1-sol@high, gpt-6-astra@high
- interrogate reviewers: gpt-6-luna@high, gpt-6.1-sol@high, gpt-6-astra@high
- arena cross-judge pool: gpt-6-astra@high, gpt-6.1-sol@high, gpt-6-luna@high
- reflect tooling: gpt-6-luna@medium
- reflect judgment: gpt-6.1-sol@high
- reflect divergent: gpt-6-astra@high
- reflect synthesizer: gpt-6.1-sol@high
- swarm workers: gpt-6-luna@high

## Runtime policy

- model routing: pass a route's model and reasoning effort when the collaboration tool supports both; otherwise inherit the session runtime; use minimal task-local context for a model override
- maximum parallel children: 3
- default arena candidates: 3
- default review panel: 3
- simple investigations: main agent
- complex investigations: up to 3 parallel explorers, then parent synthesis
- swarm: use bounded parallel workers for coverage, races, and exploration; use arena for design bakeoffs
- subagent isolation: separate output paths or worktrees for writers
- memory source: Codex memory index first, scoped task history second
- verification: real artifact plus focused automated checks
- browser verification: installed browser, computer-use, or project verification skill
- pull request creation: only when the user or active workflow authorizes publication
- pull request follow-through: inspect checks and review feedback until the requested terminal state
- PR monitoring: bundled watch-pr with Bun and authenticated gh
- merge authority: require an explicit request to merge, land, ship, or enable merge when ready
- external writes: stay inside the user's request and existing authority
- prose: unslop
