#!/usr/bin/env python3
"""Conservative Git workspace inventory and synchronization manager."""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

VERSION = "0.1.0"
REDacted = re.compile(r"(?i)(https?://)([^/@\s]+):([^/@\s]+)@")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(value: str) -> str:
    return REDacted.sub(r"\1<redacted>@", value or "")


def run_git(path: Path, *args: str, timeout: int = 60) -> tuple[int, str, str]:
    try:
        p = subprocess.run(["git", "-C", str(path), *args], text=True,
                           capture_output=True, timeout=timeout, check=False)
        return p.returncode, redact(p.stdout.strip()), redact(p.stderr.strip())
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, "", redact(str(exc))


def git(path: Path, *args: str, timeout: int = 60) -> str:
    code, out, err = run_git(path, *args, timeout=timeout)
    if code:
        raise RuntimeError(err or f"git {' '.join(args)} failed")
    return out


@dataclass
class RepoStatus:
    name: str
    path: str
    kind: str
    scope: str
    branch: str = ""
    upstream: str = ""
    remote: str = ""
    head: str = ""
    state: str = "invalid"
    dirty: int = 0
    ahead: int = 0
    behind: int = 0
    note: str = ""


def load_manifest(manifest: Path) -> tuple[Path, dict]:
    manifest = manifest.resolve()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != 1:
        raise ValueError("repo.json must have schemaVersion 1")
    root = manifest.parent
    for entry in data.get("repositories", []):
        rel = Path(entry["path"])
        resolved = (root / rel).resolve()
        if os.path.commonpath([str(root), str(resolved)]) != str(root):
            raise ValueError(f"repository path escapes workspace: {entry['path']}")
    return root, data


def classify(path: Path, entry: dict) -> RepoStatus:
    status = RepoStatus(entry["name"], entry["path"], entry.get("kind", "repository"),
                        entry.get("scope", "active"))
    if status.scope in {"ignored", "archive"}:
        status.state, status.note = "ignored", "excluded by manifest policy"
        return status
    if not path.exists():
        status.state, status.note = "missing", "path does not exist"
        return status
    code, top, err = run_git(path, "rev-parse", "--show-toplevel")
    if code:
        status.state, status.note = "invalid", err or "not a valid Git worktree"
        return status
    try:
        status.branch = git(path, "symbolic-ref", "--short", "-q", "HEAD") or "(detached)"
        if status.branch == "(detached)":
            status.state = "detached"
        status.upstream = git(path, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    except RuntimeError:
        status.upstream = ""
    try:
        status.remote = git(path, "remote", "get-url", "origin")
    except RuntimeError:
        status.state = "missing-remote"
    try:
        status.head = git(path, "log", "-1", "--date=short", "--pretty=format:%h %ad %s")
    except RuntimeError:
        status.state, status.note = "unborn", "repository has no commits"
        return status
    porcelain = git(path, "status", "--porcelain=v1")
    status.dirty = len(porcelain.splitlines()) if porcelain else 0
    if status.upstream:
        try:
            counts = git(path, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
            status.ahead, status.behind = int(counts[0]), int(counts[1])
        except (RuntimeError, ValueError):
            status.note = "unable to calculate upstream divergence"
    if status.dirty:
        status.state = "dirty"
    elif status.state in {"detached", "missing-remote", "unborn"}:
        pass
    elif not status.upstream:
        status.state = "no-upstream"
    elif status.ahead and status.behind:
        status.state = "diverged"
    elif status.ahead:
        status.state = "ahead"
    elif status.behind:
        status.state = "behind"
    else:
        status.state = "clean/synced"
    return status


def statuses(root: Path, data: dict, names: set[str] | None = None) -> list[RepoStatus]:
    result = []
    for entry in data.get("repositories", []):
        if names and entry["name"] not in names:
            continue
        result.append(classify((root / entry["path"]).resolve(), entry))
    return result


def workspace_dir(root: Path) -> Path:
    out = root / ".pawa-repo-manager"
    out.mkdir(exist_ok=True)
    return out


def lock_path(root: Path) -> Path:
    return workspace_dir(root) / "lock.json"


def acquire(root: Path, operation: str, override: bool = False) -> Path:
    path = lock_path(root)
    payload = {"pid": os.getpid(), "host": socket.gethostname(), "started": now(),
               "operation": operation, "version": VERSION}
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return path
    except FileExistsError:
        if not override:
            raise RuntimeError(f"workspace lock exists at {path}; inspect or use --override-stale-lock")
        path.unlink()
        return acquire(root, operation, False)


def release(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def log_action(root: Path, row: dict) -> None:
    log = workspace_dir(root) / "actions.jsonl"
    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": now(), "version": VERSION, **row}, ensure_ascii=False) + "\n")


def render(rows: list[dict], exit_code: int = 0) -> int:
    headers = ["Repository", "Action", "Before", "Result", "After", "Notes"]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        print("| " + " | ".join(str(row.get(h.lower(), "")).replace("|", "\\|") for h in headers) + " |")
    totals = {"touched": len(rows), "changed": sum(r.get("result") == "Success" and r.get("action") not in {"audit", "fetch"} for r in rows),
              "skipped": sum(r.get("result") == "Skipped" for r in rows), "blocked": sum(r.get("result") == "Blocked" for r in rows),
              "failed": sum(r.get("result") == "Failed" for r in rows)}
    print(f"Totals: touched={totals['touched']} changed={totals['changed']} skipped={totals['skipped']} blocked={totals['blocked']} failed={totals['failed']}")
    return exit_code


def row(status: RepoStatus, action: str, result: str, after: RepoStatus | None = None, notes: str = "") -> dict:
    after = after or status
    return {"repository": status.name, "action": action, "before": status.state,
            "result": result, "after": after.state, "notes": notes or status.note}


def command_audit(args: argparse.Namespace) -> int:
    root, data = load_manifest(Path(args.manifest))
    rows = []
    for status in statuses(root, data):
        rows.append(row(status, "audit", "Success", notes=f"branch={status.branch or '-'} head={status.head or '-'}"))
    snapshot = workspace_dir(root) / "status.json"
    snapshot.write_text(json.dumps({"time": now(), "repositories": [asdict(s) for s in statuses(root, data)]}, indent=2), encoding="utf-8")
    return render(rows)


def command_plan(args: argparse.Namespace) -> int:
    root, data = load_manifest(Path(args.manifest))
    rows = []
    entries = {entry["name"]: entry for entry in data.get("repositories", [])}
    for status in statuses(root, data):
        path = (root / status.path).resolve()
        if status.scope in {"ignored", "archive"}:
            rows.append(row(status, "plan", "Skipped", notes="excluded by policy")); continue
        if status.remote:
            code, _, err = run_git(path, "fetch", "origin")
            if code:
                rows.append(row(status, "fetch", "Failed", notes=err)); continue
            status = classify(path, entries[status.name])
        if status.state == "behind" and status.dirty == 0:
            action = "fast-forward pull"
            result = "Success"
            notes = "safe plan; no mutation performed"
        elif status.state == "clean/synced":
            action, result, notes = "none", "Success", "already synchronized"
        else:
            action, result, notes = "manual review", "Blocked", f"state={status.state}"
        rows.append(row(status, action, result, notes=notes))
    return render(rows, 2 if any(r["result"] == "Blocked" for r in rows) else 0)


def command_sync(args: argparse.Namespace) -> int:
    root, data = load_manifest(Path(args.manifest))
    lock = acquire(root, "sync", args.override_stale_lock)
    rows = []
    try:
        for status in statuses(root, data):
            if status.scope in {"ignored", "archive"}:
                rows.append(row(status, "sync", "Skipped", notes="excluded by policy")); continue
            path = (root / status.path).resolve()
            before = status.state
            if status.remote:
                code, _, err = run_git(path, "fetch", "origin")
                if code:
                    rows.append(row(status, "fetch", "Failed", notes=err)); log_action(root, {"repo": status.name, "action": "fetch", "result": "Failed", "error": err}); continue
            after = classify(path, next(e for e in data["repositories"] if e["name"] == status.name))
            if after.state == "behind" and after.dirty == 0:
                code, _, err = run_git(path, "pull", "--ff-only")
                final = classify(path, next(e for e in data["repositories"] if e["name"] == status.name))
                result = "Success" if code == 0 and final.state == "clean/synced" else "Failed"
                rows.append(row(status, "fast-forward pull", result, final, err or "verified after pull"))
            elif after.state == "clean/synced":
                rows.append(row(status, "fetch", "Success", after, "already synchronized"))
            else:
                rows.append(row(status, "sync", "Blocked", after, f"state={after.state}; no mutation"))
            log_action(root, {"repo": status.name, "action": "sync", "before": before, "result": rows[-1]["result"], "after": rows[-1]["after"]})
    finally:
        release(lock)
    return render(rows, 2 if any(r["result"] in {"Blocked", "Failed"} for r in rows) else 0)


def command_push(args: argparse.Namespace) -> int:
    if not args.approve:
        print("Push requires --approve after reviewing the exact repository, branch, remote, and commit range.", file=sys.stderr)
        return 2
    root, data = load_manifest(Path(args.manifest))
    names = {args.repo} if args.repo else None
    lock = acquire(root, "push", args.override_stale_lock)
    rows = []
    try:
        for status in statuses(root, data, names):
            path = (root / status.path).resolve()
            if status.state not in {"ahead", "clean/synced"} or status.dirty:
                rows.append(row(status, "push", "Blocked", notes=f"state={status.state}; dirty={status.dirty}")); continue
            code, _, err = run_git(path, "push", "origin", status.branch)
            final = classify(path, next(e for e in data["repositories"] if e["name"] == status.name))
            rows.append(row(status, "push", "Success" if code == 0 else "Failed", final, err or "verified after push"))
            log_action(root, {"repo": status.name, "action": "push", "result": rows[-1]["result"], "after": rows[-1]["after"]})
    finally:
        release(lock)
    return render(rows, 2 if any(r["result"] != "Success" for r in rows) else 0)


def command_verify(args: argparse.Namespace) -> int:
    root, data = load_manifest(Path(args.manifest))
    rows = []
    for status in statuses(root, data):
        result = "Success" if status.state != "invalid" and status.state != "missing" else "Failed"
        rows.append(row(status, "verify", result, notes=f"remote={redact(status.remote) or '-'}"))
    return render(rows, 1 if any(r["result"] == "Failed" for r in rows) else 0)


def command_repair_remote(args: argparse.Namespace) -> int:
    if not args.approve or not args.remote:
        print("Remote repair requires --remote and --approve after reviewing the exact replacement URL.", file=sys.stderr)
        return 2
    root, data = load_manifest(Path(args.manifest))
    lock = acquire(root, "repair-remote", args.override_stale_lock)
    rows = []
    try:
        entries = {entry["name"]: entry for entry in data.get("repositories", [])}
        for status in statuses(root, data, {args.repo}):
            path = (root / status.path).resolve()
            if status.kind not in {"repository", "nested-repository"}:
                rows.append(row(status, "repair remote", "Blocked", notes="not a Git repository")); continue
            old = status.remote or "(missing)"
            code, _, err = run_git(path, "remote", "set-url", "origin", args.remote)
            final = classify(path, entries[status.name])
            result = "Success" if code == 0 and final.remote == args.remote else "Failed"
            rows.append(row(status, "repair remote", result, final, err or f"{old} -> {redact(args.remote)}"))
            log_action(root, {"repo": status.name, "action": "repair remote", "old": redact(old), "new": redact(args.remote), "result": result})
    finally:
        release(lock)
    return render(rows, 2 if any(r["result"] != "Success" for r in rows) else 0)


def command_move(args: argparse.Namespace) -> int:
    if not args.approve or not args.destination:
        print("Move requires --destination and --approve after reviewing the exact paths.", file=sys.stderr)
        return 2
    root, data = load_manifest(Path(args.manifest))
    entries = {entry["name"]: entry for entry in data.get("repositories", [])}
    if args.repo not in entries:
        raise ValueError(f"unknown repository: {args.repo}")
    entry = entries[args.repo]
    source = (root / entry["path"]).resolve()
    destination = (root / args.destination).resolve()
    if os.path.commonpath([str(root), str(destination)]) != str(root) or destination.exists():
        raise ValueError("destination must be inside the workspace and must not already exist")
    status = classify(source, entry)
    if status.state != "clean/synced":
        return render([row(status, "move", "Blocked", notes=f"move requires clean/synced state; found {status.state}")], 2)
    lock = acquire(root, "move", args.override_stale_lock)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        entry["path"] = str(destination.relative_to(root)).replace(os.sep, "/")
        manifest_path = Path(args.manifest).resolve()
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        final = classify(destination, entry)
        result = "Success" if final.state == "clean/synced" else "Failed"
        output = row(status, "move", result, final, f"{source} -> {destination}")
        log_action(root, {"repo": status.name, "action": "move", "source": str(source), "destination": str(destination), "result": result})
        return render([output], 0 if result == "Success" else 1)
    finally:
        release(lock)


def command_unlock(args: argparse.Namespace) -> int:
    root, _ = load_manifest(Path(args.manifest))
    path = lock_path(root)
    if not path.exists():
        print("No workspace lock exists.")
        return 0
    if not args.approve:
        print(f"Lock exists at {path}; use --approve to clear it.", file=sys.stderr)
        return 2
    path.unlink()
    print(f"Cleared workspace lock: {path}")
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="repo_manager.py")
    p.add_argument("command", choices=["audit", "plan-sync", "sync", "push", "repair-remote", "move", "verify", "unlock"])
    p.add_argument("--manifest", required=True)
    p.add_argument("--repo")
    p.add_argument("--remote")
    p.add_argument("--destination")
    p.add_argument("--approve", action="store_true")
    p.add_argument("--override-stale-lock", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        return {"audit": command_audit, "plan-sync": command_plan, "sync": command_sync,
                "push": command_push, "repair-remote": command_repair_remote,
                "move": command_move, "verify": command_verify, "unlock": command_unlock}[args.command](args)
    except (ValueError, RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {redact(str(exc))}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
