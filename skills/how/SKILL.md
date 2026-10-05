---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Read `~/.codex/pstack/config.md` when it exists. Pass a route's verified model and reasoning effort only when the active collaboration schema supports them. Otherwise inherit the session runtime. Missing routes also inherit. Tell every child the task is read-only; do not invent a read-only spawn option.

For a model override, spawn a fresh child with minimal task-local context (`fork_turns: "none"` where supported). Full-history forks inherit model and effort.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Decompose the question into 2 to 4 exploration angles, each a distinct slice of the subsystem. Spawn the explorers before waiting, bounded by the available slots.

Use Codex collaboration agents with model route `how explorers`, bounded by available slots.

Each explorer gets the prompt in `references/explorer-prompt.md` with its angle filled in. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

Spawn one Codex collaboration agent that explores and explains in one pass:

Use a Codex collaboration agent with model route `how explainer`.

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers have returned, spawn one Codex collaboration agent to synthesize their findings into one explanation:

Use a Codex collaboration agent with model route `how explainer`.

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Review the explanation against the source and own the final synthesis. Preserve the explainer's evidence and uncertainty. For critique requests, route the completed explanation to `interrogate` instead of reviving the retired How critic panel.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
