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
DEFAULT_MODEL_SLUGS = {"gpt-5.6-sol", "gpt-5.6-terra"}
REASONING_EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
MODEL_ROUTE_REFERENCE = re.compile(r"model route `([^`]+)`")
MODEL_ROUTE_VALUE = re.compile(r"([a-z0-9][a-z0-9.-]*)@(low|medium|high|xhigh|max|ultra)")
PANEL_ROUTE_COUNT_SETTINGS = {
    "how critics": "default review panel",
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
        if not value_match:
            errors.append(f"{config_path}: invalid parent-task recommendation: {recommendation}")
        elif value_match.group(1) not in allowed_models:
            errors.append(f"{config_path}: unavailable parent-task model: {value_match.group(1)}")

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
            value_match = MODEL_ROUTE_VALUE.fullmatch(raw_value)
            if not value_match:
                errors.append(f"{config_path}: invalid route value for {role}: {raw_value}")
                continue
            model, effort = value_match.groups()
            if model not in allowed_models:
                errors.append(f"{config_path}: unavailable model for {role}: {model}")
            if effort not in REASONING_EFFORTS:
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

    return routes, errors


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    route_references: set[str] = set()
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
            route_references.update(MODEL_ROUTE_REFERENCE.findall(contents))
            for token, reason in FORBIDDEN.items():
                if token in contents:
                    errors.append(f"{path}: {reason}: {token}")

            for match in re.finditer(r"(?:references|playbooks)/[A-Za-z0-9_.\-/]+", contents):
                relative = match.group(0).rstrip(".,:;)")
                if not (folder / relative).exists():
                    errors.append(f"{path}: missing referenced path {relative}")

    allowed_models = set(args.allowed_model) or DEFAULT_MODEL_SLUGS
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
