#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = {
    ".cursor/": "Cursor filesystem path",
    "Task tool": "Cursor Task tool",
    "`Task`": "Cursor Task call",
    "pstack-models.mdc": "Cursor model rule",
    "`/loop": "Cursor loop command",
    "/deslop": "Cursor-only cleanup skill",
    "cursor.com/docs": "Cursor runtime documentation",
    "subagent_type": "Cursor subagent type",
    "run_in_background": "Cursor Task option",
    "agent-transcripts": "Cursor transcript layout",
    "Cursor's `/loop`": "Cursor loop command",
    '@cursor-skill/': "Cursor package namespace",
    'environment: "cloud"': "Cursor cloud environment",
    "cursor-team-kit": "Cursor-only plugin dependency",
    "Task schema": "Cursor Task schema",
    "Cursor dashboard": "Cursor dashboard runtime",
}
AUDITED_SUFFIXES = {".md", ".ts", ".js", ".mjs", ".json", ".sh"}
MODEL_EFFORTS = {
    "gpt-6.1-sol": {"low", "medium", "high", "xhigh", "max", "ultra"},
    "gpt-6-astra": {"low", "medium", "high", "xhigh", "max", "ultra"},
    "gpt-6-sol": {"low", "medium", "high", "xhigh", "max", "ultra"},
    "gpt-6-luna": {"low", "medium", "high", "xhigh", "max"},
    "gpt-5.6-sol": {"low", "medium", "high", "xhigh", "max", "ultra"},
    "gpt-5.6-luna": {"low", "medium", "high", "xhigh", "max"},
    "gpt-5.5": {"low", "medium", "high", "xhigh"},
}
DEFAULT_MODEL_SLUGS = {"gpt-6.1-sol", "gpt-6-astra", "gpt-6-luna"}
INHERITED_ROUTES = {"inherit-parent", "auto"}
FOREIGN_MODELS = re.compile(r"\b(?:claude-[a-z0-9.-]+|grok-[a-z0-9.-]+|fable-[a-z0-9.-]+)\b", re.I)
MODEL_ROUTE_REFERENCE = re.compile(r"model route `([^`]+)`")
MODEL_ROUTE_VALUE = re.compile(r"([a-z0-9][a-z0-9.-]*)@(low|medium|high|xhigh|max|ultra)")
PANEL_ROUTE_COUNT_SETTINGS = {
    "arena runners": "default arena candidates",
    "architect runners": "default arena candidates",
    "interrogate reviewers": "default review panel",
}


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--skills-root", type=Path, default=REPO_ROOT / "skills")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config.example.md")
    parser.add_argument("--allowed-model", action="append", default=[])
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
        if key.strip() in fields:
            raise ValueError(f"duplicate frontmatter field: {key.strip()}")
        fields[key.strip()] = value.strip()
    return fields, text[end + 5 :]


def model_routes(config_path: Path, allowed_models: set[str]) -> tuple[dict[str, list[tuple[str, str]]], list[str]]:
    errors: list[str] = []
    routes: dict[str, list[tuple[str, str]]] = {}
    if not config_path.is_file():
        return routes, [f"{config_path}: missing config"]

    text = config_path.read_text()
    recommendation_match = re.search(r"(?m)^- recommendation: ([^ ]+) for ", text)
    if not recommendation_match:
        errors.append(f"{config_path}: missing parent-task recommendation")
    else:
        recommendation = recommendation_match.group(1)
        value_match = MODEL_ROUTE_VALUE.fullmatch(recommendation)
        if recommendation in INHERITED_ROUTES:
            pass
        elif not value_match:
            errors.append(f"{config_path}: invalid parent-task recommendation: {recommendation}")
        elif value_match.group(1) not in allowed_models:
            errors.append(f"{config_path}: unavailable parent-task model: {value_match.group(1)}")
        elif value_match.group(2) not in MODEL_EFFORTS.get(value_match.group(1), set()):
            errors.append(f"{config_path}: unsupported parent-task effort: {recommendation}")

    marker = "## Model routes\n"
    start = text.find(marker)
    if start < 0:
        return routes, [f"{config_path}: missing '## Model routes' section"]
    section_start = start + len(marker)
    section_end = text.find("\n## ", section_start)
    section = text[section_start : section_end if section_end >= 0 else len(text)]

    for line in section.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"- ([a-z][a-z0-9 -]*): (.+)", line)
        if not match:
            errors.append(f"{config_path}: invalid model-route line: {line}")
            continue
        role, raw_values = match.groups()
        if role in routes:
            errors.append(f"{config_path}: duplicate model route: {role}")
            continue

        parsed_values: list[tuple[str, str]] = []
        for raw_value in raw_values.split(", "):
            if raw_value in INHERITED_ROUTES:
                parsed_values.append((raw_value, ""))
                continue
            value_match = MODEL_ROUTE_VALUE.fullmatch(raw_value)
            if not value_match:
                errors.append(f"{config_path}: invalid route value for {role}: {raw_value}")
                continue
            model, effort = value_match.groups()
            if model not in allowed_models:
                errors.append(f"{config_path}: unavailable model for {role}: {model}")
            if effort not in MODEL_EFFORTS.get(model, set()):
                errors.append(f"{config_path}: unsupported reasoning effort for {role}: {effort}")
            parsed_values.append((model, effort))
        routes[role] = parsed_values

    for role, count_setting in PANEL_ROUTE_COUNT_SETTINGS.items():
        count_match = re.search(rf"(?m)^- {re.escape(count_setting)}: ([0-9]+)$", text)
        if not count_match:
            errors.append(f"{config_path}: missing panel count setting: {count_setting}")
            continue
        expected_count = int(count_match.group(1))
        actual_count = len(routes.get(role, []))
        if actual_count != expected_count:
            errors.append(f"{config_path}: {role} needs {expected_count} entries, found {actual_count}")

    for role, values in routes.items():
        if role not in PANEL_ROUTE_COUNT_SETTINGS and role != "arena cross-judge pool" and len(values) != 1:
            errors.append(f"{config_path}: {role} needs exactly one route entry")
    if not routes.get("arena cross-judge pool"):
        errors.append(f"{config_path}: empty arena cross-judge pool")
    limit_match = re.search(r"(?m)^- maximum parallel children: ([0-9]+)$", text)
    if not limit_match or int(limit_match.group(1)) < 1:
        errors.append(f"{config_path}: maximum parallel children must be positive")
    return routes, errors


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    route_references: set[str] = set()
    names = [line.strip() for line in (REPO_ROOT / "manifest.txt").read_text().splitlines() if line.strip()]

    if len(names) != len(set(names)):
        errors.append("manifest.txt: duplicate skill names")
    actual_names = {p.name for p in args.skills_root.iterdir() if (p / "SKILL.md").is_file()}
    if args.skills_root.resolve() == (REPO_ROOT / "skills").resolve():
        for name in sorted(actual_names - set(names)):
            errors.append(f"manifest.txt: unlisted skill: {name}")

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

        for path in folder.rglob("*"):
            if {"node_modules", "__pycache__"} & set(path.relative_to(folder).parts):
                continue
            if not path.is_file() or path.suffix not in AUDITED_SUFFIXES:
                continue
            contents = path.read_text()
            route_references.update(MODEL_ROUTE_REFERENCE.findall(contents))
            for token, reason in FORBIDDEN.items():
                if token in contents:
                    errors.append(f"{path}: {reason}: {token}")

            if re.search(r"(?m)^(<<<<<<<|=======|>>>>>>>)", contents):
                errors.append(f"{path}: unresolved merge conflict")
            for model in FOREIGN_MODELS.findall(contents):
                errors.append(f"{path}: non-Codex model: {model}")
            for target in re.findall(r"\]\(([^)]+)\)", contents) if path.suffix == ".md" else []:
                if "://" in target or target.startswith("#"):
                    continue
                relative_target = target.split("#", 1)[0]
                if (relative_target.startswith(("./", "../")) or relative_target.endswith((".md", ".sh", ".mjs", ".ts"))) and not (path.parent / relative_target).exists():
                    errors.append(f"{path}: missing Markdown target {target}")

            for match in re.finditer(r"(?:references|playbooks)/[A-Za-z0-9_.\-/]+", contents):
                relative = match.group(0).rstrip(".,:;)")
                if not (folder / relative).exists():
                    errors.append(f"{path}: missing referenced path {relative}")

    setup_text = (args.skills_root / "setup-pstack" / "SKILL.md").read_text() if (args.skills_root / "setup-pstack" / "SKILL.md").is_file() else ""
    example = re.search(r"```md\n(.*?)\n```", setup_text, re.S)
    if example and example.group(1).strip() != (REPO_ROOT / "config.example.md").read_text().strip():
        errors.append("setup-pstack: configuration example differs from config.example.md")

    allowed_models = set(args.allowed_model) or DEFAULT_MODEL_SLUGS
    for model in sorted(allowed_models - MODEL_EFFORTS.keys()):
        errors.append(f"unverified Codex model allowlist entry: {model}")
    routes, route_errors = model_routes(args.config, allowed_models)
    errors.extend(route_errors)
    route_names = set(routes)
    for role in sorted(route_references - route_names):
        errors.append(f"{args.config}: missing model route referenced by a skill: {role}")
    for role in sorted(route_names - route_references):
        errors.append(f"{args.config}: unused model route: {role}")

    if errors:
        print("pstack audit failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"pstack audit passed: {len(names)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
