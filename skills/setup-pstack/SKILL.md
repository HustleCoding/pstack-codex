---
name: setup-pstack
description: Configure pstack for Codex, including delegation limits, review fan-out, memory sources, verification tools, and GitHub follow-through. Use for setup-pstack, "configure pstack", or changing how pstack runs in Codex.
---

# Setup pstack for Codex

Write `~/.codex/pstack/config.md`. This is an override layer for the pstack skills, not a requirement. Re-running setup replaces the file so the result stays idempotent.

## 1. Inspect the runtime

Check the capabilities available in the current Codex session:

- collaboration tools and the maximum number of concurrent agents
- thread and memory lookup tools
- browser or computer-use tools
- GitHub or `gh` access
- Bun when the user wants bundled PR monitoring
- the `skill-creator` and verification skills

Do not invent capabilities. In particular, Codex collaboration agents inherit the session runtime unless the active tool schema exposes model selection. When it does expose model and reasoning-effort selection, write only verified model slugs and supported effort values. Never invent either.

## 2. Load current configuration

Read `~/.codex/pstack/config.md` when it exists. Treat its values as the current choices and preserve intentional overrides unless the user asks for a reset.

## 3. Choose budget and recommend settings

Use a stated budget or infer it from the request. If none is stated, recommend balanced, preserving the role-specific efforts. For a budget-focused setup, offer unlimited (keep role efforts), large (xhigh), medium (high), or small (medium). Apply the target only when the model supports it. Keep intentional model overrides and list retired routes such as `how critics` and `cross-judge` before dropping them.

Show the proposed values and the reason for any meaningful change. Prefer the smallest useful fan-out. Three independent candidates or reviewers is the default when parallel judgment matters, bounded by the session's concurrency limit. Use one agent for narrow work and no subagent when delegation would add no independent value.

If the user already asked to apply your recommendations, write them without another confirmation. Ask only when a preference would materially change behavior and cannot be inferred.

## 4. Write the configuration

Use this shape, adjusted to the capabilities you verified:

```md
# pstack configuration for Codex

## Parent task

- runtime: Codex
- recommendation: gpt-6.1-sol@high for daily coding and final synthesis
- boundary: pstack cannot change the active task model or reasoning effort; select them when starting the task

## Budget

- profile: balanced
- policy: preserve the per-role efforts below; a requested large, medium, or small budget maps routes to xhigh, high, or medium only when that model supports it
- verified: 2026-10-05 from the active Codex collaboration schema

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
```

Keep the file factual. Omit unavailable integrations instead of leaving aspirational settings.

The example models were verified on 2026-10-05. Re-check the actual session before writing them. If a model is unavailable, choose a verified Codex model for that role or inherit, and disclose the change. Never route to another provider. Luna supports up to max, not ultra.

The model-route labels are stable identifiers used by pstack workflow skills. Every route entry uses `model@reasoning_effort`, or `inherit-parent` to omit both fields. `auto` is an alias for inheritance, not permission to choose another provider; panel entries are comma-separated and launch one child per entry in order. The `Parent task` recommendation is advisory because a child-spawn setting cannot change the active task. For an override, use a fresh child with minimal task-local context. Full-history forks inherit model and effort. When the active collaboration tool cannot select a model or effort, omit both fields and inherit the session runtime.

## 5. Confirm and offer verification

Report the path written and the effective settings. Check whether the active project already has `.codex/skills/verify-*` or another real-user verification harness. If none exists, mention `create-verification-skill` once. Do not create it unless the user asks.
