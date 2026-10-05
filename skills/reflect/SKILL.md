---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

For a model override, spawn a fresh child with minimal task-local context (`fork_turns: "none"` where supported). Full-history forks inherit model and effort.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

Use the active conversation and its scoped Codex task history or a supplied transcript. Read Codex memory first when relevant. Never scan unrelated projects or chats. If the actual transcript is unavailable, write a digest and label that evidence limit.

### 2. Spawn three reviewers in parallel

Launch up to three independent Codex collaboration reviewers, bounded by available slots. Keep them read-only and pass the appropriate prompt.

| Lens | Model route | Prompt |
|---|---|---|
| Judgment | model route `reflect judgment` | `references/judgment-reviewer.md` |
| Tooling | model route `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | model route `reflect divergent` | `references/divergent-reviewer.md` |

Read `~/.codex/pstack/config.md`. Pass a verified model and reasoning effort only when the collaboration schema supports both. Otherwise inherit. Give each reviewer the transcript or labeled digest and source pointers.

### 3. Synthesize

After the reviewers finish, use one fresh Codex collaboration agent with model route `reflect synthesizer`. Keep the task read-only. Use `references/synthesizer.md`, passing every reviewer's findings and the source pointers. The parent spot-checks citations and owns the final Accepted / Rejected / Backlog judgment.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Keep backlog items local unless the user explicitly authorized writing to the tracker. Apply only the skill edits the user selected or previously authorized. A reflection request alone does not authorize global skill or memory changes.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the installed `skill-creator` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
