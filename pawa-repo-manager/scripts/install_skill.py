#!/usr/bin/env python3
"""Install one canonical package into Claude and/or Codex skill roots."""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def default_codex() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills"


def default_claude() -> Path:
    return Path.home() / ".claude" / "skills"


def copy_package(source: Path, root: Path, approve: bool) -> Path:
    destination = root / source.name
    root.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        same = filecmp.dircmp(source, destination).left_only == [] and filecmp.dircmp(source, destination).right_only == []
        if not same and not approve:
            raise RuntimeError(f"destination is modified; rerun with --approve: {destination}")
        if not same:
            backup = destination.with_name(destination.name + ".backup-" + datetime.now().strftime("%Y%m%d%H%M%S"))
            shutil.move(str(destination), str(backup))
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--claude-root", type=Path)
    parser.add_argument("--codex-root", type=Path)
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args()
    source = Path(args.source).resolve()
    targets = []
    if args.target in {"claude", "both"}:
        targets.append(("Claude", args.claude_root or default_claude()))
    if args.target in {"codex", "both"}:
        targets.append(("Codex", args.codex_root or default_codex()))
    print("Resolved installation destinations:")
    for name, root in targets:
        print(f"- {name}: {root / source.name}")
    if not args.approve:
        print("Dry run only. Re-run with --approve to install.")
        return 2
    installed = [copy_package(source, root, True) for _, root in targets]
    for path in installed:
        print(f"Installed {source.name} at {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
