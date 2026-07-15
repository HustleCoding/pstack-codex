#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = {
    ".cursor/": "Cursor filesystem path",
    "Task tool": "Cursor Task tool",
    "subagent_type": "Cursor subagent type",
    "run_in_background": "Cursor Task option",
    "agent-transcripts": "Cursor transcript layout",
    "Cursor's `/loop`": "Cursor loop command",
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--skills-root", type=Path, default=REPO_ROOT / "skills")
    return parser.parse_args()


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing frontmatter delimiter")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, text[end + 5 :]


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    names = [line.strip() for line in (REPO_ROOT / "manifest.txt").read_text().splitlines() if line.strip()]

    for name in names:
        folder = args.skills_root / name
        skill_file = folder / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue

        text = skill_file.read_text()
        try:
            fields, _ = frontmatter(text)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue

        if set(fields) != {"name", "description"}:
            errors.append(f"{name}: frontmatter fields are {sorted(fields)}")
        if fields.get("name") != name:
            errors.append(f"{name}: frontmatter name is {fields.get('name')!r}")
        if not fields.get("description"):
            errors.append(f"{name}: empty description")

        for path in folder.rglob("*.md"):
            contents = path.read_text()
            for token, reason in FORBIDDEN.items():
                if token in contents:
                    errors.append(f"{path}: {reason}: {token}")

            for match in re.finditer(r"(?:references|playbooks)/[A-Za-z0-9_.\-/]+", contents):
                relative = match.group(0).rstrip(".,:;)")
                if not (folder / relative).exists():
                    errors.append(f"{path}: missing referenced path {relative}")

    if errors:
        print("pstack audit failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"pstack audit passed: {len(names)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())

