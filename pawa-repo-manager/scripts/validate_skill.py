#!/usr/bin/env python3
"""Validate the Pawa Repo Manager package and an optional workspace manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["SKILL.md", "agents/openai.yaml", "scripts/repo_manager.py",
            "scripts/install_skill.py", "references/workspace-policy.md"]


def validate(package: Path, manifest: Path | None) -> list[str]:
    errors = []
    skill = package / "SKILL.md"
    if not skill.exists():
        errors.append("missing SKILL.md")
    else:
        text = skill.read_text(encoding="utf-8")
        if not re.search(r"^---\s*\nname:\s*pawa-repo-manager\s*$", text, re.M):
            errors.append("SKILL.md has invalid name frontmatter")
        if "TODO" in text:
            errors.append("SKILL.md contains TODO placeholders")
    for relative in REQUIRED:
        if not (package / relative).exists():
            errors.append(f"missing required file: {relative}")
    yaml = package / "agents" / "openai.yaml"
    if yaml.exists() and "display_name:" not in yaml.read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml has no display_name")
    if manifest:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("schemaVersion") != 1:
            errors.append("manifest schemaVersion must be 1")
        root = manifest.parent.resolve()
        seen_names, seen_paths = set(), set()
        for entry in data.get("repositories", []):
            name, rel = entry.get("name"), entry.get("path")
            if not name or not rel:
                errors.append("manifest entry requires name and path")
                continue
            if name in seen_names or rel in seen_paths:
                errors.append(f"duplicate manifest identity: {name}/{rel}")
            seen_names.add(name); seen_paths.add(rel)
            path = (root / rel).resolve()
            if __import__("os").path.commonpath([str(root), str(path)]) != str(root):
                errors.append(f"manifest path escapes workspace: {rel}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    errors = validate(Path(args.package).resolve(), args.manifest.resolve() if args.manifest else None)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
