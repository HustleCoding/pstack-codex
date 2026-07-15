# pstack Codex port rules

- Preserve the original MIT license and attribution.
- Treat `https://github.com/cursor/plugins/tree/main/pstack` as upstream.
- Keep frontmatter to `name` and `description`.
- Do not introduce Cursor-only paths, tools, model slugs, or agent types.
- Codex collaboration agents inherit the session runtime unless the active tool schema says otherwise.
- Keep external writes inside the user's explicit scope.
- Run `./scripts/audit.py` before publishing changes.
- Update `UPSTREAM_COMMIT` only after the corresponding upstream changes have been reviewed and ported.

