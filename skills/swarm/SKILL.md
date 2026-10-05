---
name: swarm
description: "Fan out bounded Codex workers, collect their results, and return one evidence-backed report. Use for 'swarm this', parallel coverage, races, gauntlets, or exploration partitions."
---

# Swarm

Fan out independent Codex workers, drain them, and return one report. Workers may cover separate slices, race the same brief, or mix both. This is for coverage and exploration; use **arena** when the output needs a chosen base and manual grafting.

For a model override, spawn a fresh child with minimal task-local context (`fork_turns: "none"` where supported). Full-history forks inherit model and effort.

## Start

Create a task plan with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape: partition into slices, race workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set the worker count from the user's request or derive it from the shape. The configured `maximum parallel children` in `~/.codex/pstack/config.md` and the live collaboration-slot limit cap simultaneous workers. Keep the fan-out no larger than the work warrants.
4. When the collaboration tool exposes model and reasoning-effort selection, use model route `swarm workers`. For a difficult code slice, use model route `complex work`. Otherwise inherit the session runtime. Never invent a model slug or reasoning value.
5. Give each writer its own worktree or output path. Verification briefs name exact commit SHAs. Measurement briefs also name the method, sample count, what one sample is, and order. Workers record those in their results.

## Phase B: Fan out

Spawn all independent workers before waiting. Each brief must stand alone and include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that proves defects reports `ISSUES` with every proven issue.

If a worker drops out, proceed with the completed set and name the gap. Do not quietly substitute a different scope.

## Phase C: Aggregate

Read every result. Reject receipts that omit the SHAs or measurement method the brief named. Respawn that worker once; a second miss becomes an explicit gap, never a pass. For coverage, every required slice needs a result. For a race, apply the declared selection rule. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts. The parent owns the judgment; worker consensus is signal, not a verdict.

## Phase D: Report

Return one consolidated report with the result table, evidenced issues, gaps or dropouts, and the race rule when used.
