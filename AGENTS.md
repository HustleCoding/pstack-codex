# pstack Codex port rules

- Preserve the original MIT license and attribution.
- Treat `https://github.com/cursor/plugins/tree/main/pstack` as upstream.
- Keep frontmatter to `name` and `description`.
- Do not introduce Cursor-only paths, tools, model slugs, or agent types.
- Codex collaboration agents inherit the session runtime unless the active tool schema says otherwise.
- Keep external writes inside the user's explicit scope.
- Run `./scripts/audit.py` before publishing changes. For audit, installer, or plan-checker changes, also run `python3 -m unittest discover -s tests -v`.
- Keep model and reasoning pairs verified in the current Codex schema. Luna has no Ultra effort. Full-history child forks inherit the parent; overrides need a fresh task-local child.
- Update `UPSTREAM_COMMIT` only after the corresponding upstream changes have been reviewed and ported.

