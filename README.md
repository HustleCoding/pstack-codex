# pstack for Codex

This repository ports [pstack](https://github.com/cursor/plugins/tree/main/pstack) from Cursor to Codex.

The engineering principles and playbooks remain pstack's. The runtime integration is native Codex:

- Codex collaboration agents instead of Cursor `Task` and `poteto-agent`
- verified Codex model and reasoning routes when the collaboration tool exposes them, with session-runtime inheritance as the fallback
- Codex memory and task history instead of Cursor transcript paths
- Codex browser, computer-use, GitHub, and automation tools
- `.codex/skills` for global and project-local skills

The port tracks upstream **0.15.10** at [`4e5b1cf`](https://github.com/cursor/plugins/commit/4e5b1cf2ccb0ea3716f08c8ee0a5856b5ab93536), reviewed on October 5, 2026. It contains **50 skills**, including 24 engineering principles. This update adds `poteto-help`, `correct`, `benchmark-checklist`, three principle skills, a checked multi-PR plan, stronger architecture screening, and evidence-backed benchmark and PR verification guidance. See [the port record](docs/upstream-port.md) for adaptations and exclusions.

## Install

```bash
git clone https://github.com/HustleCoding/pstack-codex.git
cd pstack-codex
./scripts/install.sh
```

The installer validates the source, then backs up any same-named global skills before writing to `~/.codex/skills`. It preserves unrelated skills and existing pstack configuration. `./scripts/install.sh --dry-run` shows the changes without writing files. Local dependency caches are excluded.

Restart Codex or start a new task after installation so the refreshed skill catalog loads.

## Configure

Ask Codex:

```text
Use setup-pstack and configure pstack with your recommended Codex settings.
```

The setup skill writes `~/.codex/pstack/config.md`. When the active collaboration tool exposes model and reasoning-effort selection, the configuration routes verified Codex models by role; otherwise agents inherit the session runtime. It also controls fan-out, isolation, memory, verification, and publication policy.

The recommended balanced setup uses only models available in Codex:

| Role | Model and reasoning |
|---|---|
| Parent, complex implementation, and synthesis | `gpt-6.1-sol@high` |
| Routine implementation | `gpt-6.1-sol@medium` |
| Focused exploration and swarm workers | `gpt-6-luna@high` |
| Hardest design work and demanding review | `gpt-6-astra@high` |
| Review panels | Luna High, Sol High, Astra High |

These choices balance the efficient Luna with Sol for sustained work and Astra for the hardest judgment. They follow [official Codex model guidance](https://learn.chatgpt.com/docs/models) and were verified against this session's model schema on October 5, 2026. Re-check availability when configuring another account or client. Luna supports up to Max, not Ultra. See [config.example.md](config.example.md) for all routes.

Choose the parent in Codex's model picker. Routes control compatible child spawns and cannot change the active parent. A model override uses a fresh child with task-local context; full-history forks inherit. With no compatible override, children inherit the session runtime. Fan-out is capped by the live slot limit and configured maximum, with three children as the example cap.

After upgrading an existing installation, rerun `setup-pstack` to review model changes and retire `how critics` and `cross-judge`. Installation preserves your existing configuration.

## Use

Start rigorous work with:

```text
Use poteto-mode. Diagnose this bug, prove the root cause, fix it, and verify on the real surface.
```

You can also invoke focused skills such as `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `blast-radius`, `tdd`, and `teach`.

PR monitoring uses the bundled `poteto-mode` watcher. It requires Bun and an authenticated GitHub CLI:

```bash
bun --version
gh auth status
```

The watcher installs its pinned dependencies on first use and reads GitHub state without granting merge authority. Babysit stops at merge-ready. Shipping requires an explicit request to merge, land, or enable merge when ready.

## Check upstream

```bash
./scripts/check-upstream.sh
```

The script compares this port's recorded upstream commit with the current `cursor/plugins` main branch. It reports pstack changes without modifying the port.

After porting an upstream update, replace `UPSTREAM_COMMIT` with the reviewed upstream commit and run:

```bash
./scripts/audit.py
```

## Validate

```bash
./scripts/audit.py
python3 -m unittest discover -s tests -v
```

The audit checks skill discovery, frontmatter, references, runtime dependencies, and model routes. Tests exercise unsupported models and efforts, inherited panel seats, incomplete plans, and installation with backup and config preservation. GitHub Actions also runs the bundled PR watcher tests and strict typecheck.

The Multi-phase plan playbook includes a complete checklist template. Check a filled plan with:

```bash
node skills/poteto-mode/scripts/check-plan.mjs /path/to/plan.md
```

The Codex checker accepts a stated positive lane count and screenshots or terminal receipts. Choose lanes by the behavior being proved and run them within the runtime's capacity.

## Attribution

pstack was created by [Lauren Tan](https://github.com/poteto) and is published in the [Cursor plugins repository](https://github.com/cursor/plugins/tree/main/pstack) under the MIT License. This repository is an independent Codex port and is not affiliated with Cursor or OpenAI.
