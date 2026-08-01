# pstack for Codex

This repository ports [pstack](https://github.com/cursor/plugins/tree/main/pstack) from Cursor to Codex.

The engineering principles and playbooks remain pstack's. The runtime integration is native Codex:

- Codex collaboration agents instead of Cursor `Task` and `poteto-agent`
- verified Codex model and reasoning routes when the collaboration tool exposes them, with session-runtime inheritance as the fallback
- Codex memory and task history instead of Cursor transcript paths
- Codex browser, computer-use, GitHub, and automation tools
- `.codex/skills` for global and project-local skills

The port currently contains 41 skills, including `poteto-mode`, its playbooks, `swarm`, the workflow skills, and 21 engineering principles.

## Install

```bash
git clone https://github.com/HustleCoding/pstack-codex.git
cd pstack-codex
./scripts/install.sh
```

The installer backs up any same-named global skills before writing to `~/.codex/skills`. It does not touch unrelated skills.

Restart Codex or start a new task after installation so the refreshed skill catalog loads.

## Configure

Ask Codex:

```text
Use setup-pstack and configure pstack with your recommended Codex settings.
```

The setup skill writes `~/.codex/pstack/config.md`. When the active collaboration tool exposes model and reasoning-effort selection, the configuration routes verified Codex models by role; otherwise agents inherit the session runtime. It also controls fan-out, isolation, memory, verification, and publication policy.

## Use

Start rigorous work with:

```text
Use poteto-mode. Diagnose this bug, prove the root cause, fix it, and verify on the real surface.
```

You can also invoke focused skills such as `how`, `why`, `architect`, `arena`, `swarm`, `interrogate`, `blast-radius`, `tdd`, and `teach`.

## Check upstream

```bash
./scripts/check-upstream.sh
```

The script compares this port's recorded upstream commit with the current `cursor/plugins` main branch. It reports pstack changes without modifying the port.

After porting an upstream update, replace `UPSTREAM_COMMIT` with the reviewed upstream commit and run:

```bash
./scripts/audit.py
```

## Attribution

pstack was created by [Lauren Tan](https://github.com/poteto) and is published in the [Cursor plugins repository](https://github.com/cursor/plugins/tree/main/pstack) under the MIT License. This repository is an independent Codex port and is not affiliated with Cursor or OpenAI.
