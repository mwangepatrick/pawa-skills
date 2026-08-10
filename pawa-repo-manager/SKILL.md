---
name: pawa-repo-manager
description: Safely inventory, audit, plan, and synchronize configured Git repositories with workspace policy, remote validation, dry-run planning, lock protection, and per-repository action summaries. Use when managing multiple repositories, checking repository health, syncing repositories, repairing approved remotes, or installing the manager in Claude or Codex.
---

# Pawa Repo Manager

Use the bundled `scripts/repo_manager.py` against the workspace `repo.json`.
Resolve the manifest location before doing anything else; do not assume a fixed
drive or operating system path.

## Required workflow

1. Run `audit` for read-only inventory.
2. Run `plan-sync` before any batch synchronization.
3. Show the exact repository, branch, remote, commit range, and proposed action
   before requesting approval for push, merge, rebase, remote repair, or move.
4. Run only approved operations. Safe synchronization is fast-forward-only.
5. Verify the final Git state after every mutation.
6. End every action with the Markdown table emitted by the CLI:

   `Repository | Action | Before | Result | After | Notes`

Never use reset, clean, force-push, deletion, automatic conflict resolution, or
pull/merge/rebase into a dirty worktree. Archives, `release`, and manifest
ignored paths are out of scope unless the user explicitly includes them.

## Commands

```text
python scripts/repo_manager.py audit --manifest <workspace>/repo.json
python scripts/repo_manager.py plan-sync --manifest <workspace>/repo.json
python scripts/repo_manager.py sync --manifest <workspace>/repo.json
python scripts/repo_manager.py push --manifest <workspace>/repo.json --repo <name> --approve
python scripts/repo_manager.py repair-remote --manifest <workspace>/repo.json --repo <name> --remote <url> --approve
python scripts/repo_manager.py move --manifest <workspace>/repo.json --repo <name> --destination <relative-path> --approve
python scripts/repo_manager.py verify --manifest <workspace>/repo.json
python scripts/repo_manager.py unlock --manifest <workspace>/repo.json
```

`sync` fetches first and only fast-forwards clean, behind-only repositories.
Dirty, divergent, detached, invalid, missing-remote, suspicious, and
permission-blocked repositories are reported and left untouched. Push requires
an exact-target approval; the CLI refuses force-push.

Read [workspace-policy.md](references/workspace-policy.md) for registry fields,
status meanings, locks, exit codes, and report requirements. Read the Claude or
Codex installation reference only when installing or updating the skill.
