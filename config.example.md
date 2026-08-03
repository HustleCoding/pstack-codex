# pstack configuration for Codex

## Parent task

- runtime: Codex
- recommendation: gpt-5.6-sol@xhigh for architecture and final synthesis
- boundary: pstack cannot change the active task model or reasoning effort; select them when starting the task

## Model routes

- default child: gpt-5.6-terra@medium
- routine work: gpt-5.6-terra@high
- complex work: gpt-5.6-sol@high
- how explorers: gpt-5.6-terra@medium
- why investigators: gpt-5.6-terra@medium
- why synthesizer: gpt-5.6-sol@high
- how critics: gpt-5.6-terra@high, gpt-5.6-sol@high, gpt-5.6-sol@xhigh
- arena runners: gpt-5.6-terra@high, gpt-5.6-sol@high, gpt-5.6-sol@xhigh
- architect runners: gpt-5.6-terra@high, gpt-5.6-sol@high, gpt-5.6-sol@xhigh
- interrogate reviewers: gpt-5.6-terra@high, gpt-5.6-sol@high, gpt-5.6-sol@xhigh
- cross-judge: gpt-5.6-terra@xhigh
- reflect tooling: gpt-5.6-terra@medium
- reflect judgment: gpt-5.6-sol@high
- reflect divergent: gpt-5.6-terra@xhigh
- reflect synthesizer: gpt-5.6-sol@high
- swarm workers: gpt-5.6-terra@medium

## Runtime policy

- model routing: pass a route's model and reasoning effort when the collaboration tool supports both; otherwise inherit the session runtime
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
