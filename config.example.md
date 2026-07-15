# pstack configuration for Codex

- runtime: Codex
- subagent model: inherit session runtime
- maximum parallel children: 3
- default arena candidates: 3
- default review panel: 3
- simple investigations: main agent
- complex investigations: up to 3 parallel explorers, then parent synthesis
- subagent isolation: separate output paths or worktrees for writers
- memory source: Codex memory index first, scoped task history second
- verification: real artifact plus focused automated checks
- browser verification: installed browser, computer-use, or project verification skill
- pull request creation: only when the user or active workflow authorizes publication
- pull request follow-through: inspect checks and review feedback until the requested terminal state
- external writes: stay inside the user's request and existing authority
- prose: unslop

