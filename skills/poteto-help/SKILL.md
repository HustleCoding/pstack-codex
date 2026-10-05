---
name: poteto-help
description: Help users install, configure, and use pstack for Codex or choose a skill, playbook, or principle. Use for poteto-help and questions about using pstack. Requests to perform work route to the requested workflow.
---

# Poteto help

Answer the question, give a ready-to-send prompt, and link the skill that supports it. Read that skill before recommending it. A help request does not authorize starting an expensive workflow. A request to do work does.

## Setup

Install from [pstack-codex](https://github.com/HustleCoding/pstack-codex) with `./scripts/install.sh`. The installer backs up same-named skills and preserves unrelated skills. Start a new Codex task to load the refreshed catalog.

Run **setup-pstack** to choose verified Codex models, reasoning efforts, and bounded fan-out. It writes `~/.codex/pstack/config.md`. Existing settings remain intentional until the user asks to change them. A missing file means children inherit the session unless a workflow supplies a verified route.

Suggested prompt. "Use setup-pstack. Configure balanced Codex-only routes and explain the model choices."

Use **poteto-mode** with a concrete goal and a check that can pass or fail. Invoke it at the start of each new task. For a persistent project preference, the user can ask to add a scoped instruction to AGENTS.md. Do not assume a Custom Mode is available.

Suggested prompt. "Use poteto-mode. Diagnose this bug, prove the cause, fix it, and verify the user-visible result."

The parent model is chosen in Codex's model picker. A route cannot change the active parent's model. Child overrides require a compatible collaboration schema and a fresh child with minimal task-local context; full-history forks inherit. When overrides are unavailable, report inheritance.

## Pick a skill

| Goal | Skill |
|---|---|
| Run rigorous work with a matching playbook | poteto-mode |
| Understand runtime flow or ownership | how |
| Investigate design rationale or a threshold | why |
| Explain a subsystem or change plainly | teach |
| Rebuild recent scoped working context | recall |
| Find what a diff could break elsewhere | blast-radius |
| Design types and module boundaries | architect |
| Compare complete candidates and graft the best parts | arena |
| Cover independent slices or race workers | swarm |
| Challenge a diff with independent reviewers | interrogate |
| Fix test-first when explicitly requested | tdd |
| Apply schema-first TypeScript rules | typescript-best-practices |
| Review comments and expose workaround code | no-comments |
| Clean prose or write technical documents | unslop, technical-writing |
| Restate the last message plainly | bro |
| Create or maintain real-user verification | create-verification-skill, maintain-verification-skill |
| Vet benchmark claims | benchmark-checklist |
| Design a playbook for a large migration | figure-it-out |
| Keep a reviewable decision trail | show-me-your-work |
| Choose Codex models and budget | setup-pstack |
| Capture personal working conventions | automate-me |
| Propose evidence-backed skill improvements | reflect |
| Prevent repeated agent mistakes structurally | correct |

Resolve these names through the installed skill catalog. Link a real local SKILL.md when available, or its public source under `https://github.com/HustleCoding/pstack-codex/blob/main/skills/`. Principles live in `principle-*` skills. Read the leaf before citing a principle.

## Playbooks

Playbooks live inside poteto-mode, not separate slash commands. Read its Playbooks section for the full list.

- "Check on this PR" makes one status pass. "Babysit this PR to merge-ready" follows Babysit and stops at merge-ready.
- "Land this stack" follows Shipping and grants the stated merge scope.
- "Take over this branch" follows Session pickup. "Pause safely" writes a durable checkpoint.
- "Build and stack these, let me review" follows Autopilot-stack. Independent PRs with explicit landing authority use Autopilot-full.
- "Plan this migration" follows Multi-phase plan and returns a checked plan. Execution starts on the user's go.

An overnight task needs a checkable done predicate. Use an available Codex heartbeat automation for requested later or recurring work. Save the actual cadence, stay quiet while state is unchanged, and report a missing scheduler. Keep active waits bounded.

## Troubleshooting

A wrong skill choice starts with poteto-mode and a concrete done predicate. Missing live evidence calls for a project verification harness. Parallel writers need separate worktrees or output paths. Weak benchmark evidence calls for benchmark-checklist. Repeated corrections call for correct. Skill improvements start with reflect and stay proposals until the user authorizes edits.

This port uses Codex collaboration, memory, history, and available verification tools. It excludes the upstream Grok Bot UI integration. It does not assume cloud VMs, a particular stacking CLI, or another provider's models.
