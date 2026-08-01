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
- the `skill-creator` and verification skills

Do not invent capabilities. In particular, Codex collaboration agents inherit the session runtime unless the active tool schema exposes model selection. When it does expose model and reasoning-effort selection, write only verified model slugs and supported effort values. Never invent either.

## 2. Load current configuration

Read `~/.codex/pstack/config.md` when it exists. Treat its values as the current choices and preserve intentional overrides unless the user asks for a reset.

## 3. Recommend settings

Show the proposed values and the reason for any meaningful change. Prefer the smallest useful fan-out. Three independent candidates or reviewers is the default when parallel judgment matters, bounded by the session's concurrency limit. Use one agent for narrow work and no subagent when delegation would add no independent value.

If the user already asked to apply your recommendations, write them without another confirmation. Ask only when a preference would materially change behavior and cannot be inferred.

## 4. Write the configuration

Use this shape, adjusted to the capabilities you verified:

```md
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
- complex investigations: parallel explorers, then parent synthesis
- swarm: use bounded parallel workers for coverage, races, and exploration; use arena for design bakeoffs
- subagent isolation: separate output paths or worktrees for writers
- memory source: Codex memory first, scoped task history second
- verification: real artifact plus focused automated checks
- browser verification: use an installed browser or computer-use skill
- pull request follow-through: inspect checks and review feedback until terminal state
- prose: unslop
```

Keep the file factual. Omit unavailable integrations instead of leaving aspirational settings.

The model-route labels are stable identifiers used by pstack workflow skills. Every route entry uses `model@reasoning_effort`; panel entries are comma-separated and launch one child per entry in order. The `Parent task` recommendation is advisory because a child-spawn setting cannot change the active task. When the active collaboration tool cannot select a model or effort, omit both fields and inherit the session runtime.

## 5. Confirm and offer verification

Report the path written and the effective settings. Check whether the active project already has `.codex/skills/verify-*` or another real-user verification harness. If none exists, mention `create-verification-skill` once. Do not create it unless the user asks.
