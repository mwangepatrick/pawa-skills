# Pawa Repo Manager Design

## Goal

Create a reusable `pawa-repo-manager` skill that safely inventories and manages
multiple Git repositories from a workspace such as `D:\cp\pp`. It must be
installable in both Claude and Codex while using one canonical skill source.

The manager is two-way: it can fetch, fast-forward, push, configure upstreams,
repair approved remotes, and move repositories. It must remain conservative,
plan changes before risky actions, preserve local work, and provide a clear
per-repository result table after every action.

## Package layout

The canonical source lives at:

`pawa-skills/pawa-repo-manager/`

It contains:

- `SKILL.md` with the operating rules and workflow.
- `agents/openai.yaml` with Codex-facing metadata.
- `references/workspace-policy.md` with repository policy and safety rules.
- `references/claude-install.md` and `references/codex-install.md`.
- `scripts/` for discovery, auditing, planning, synchronization, validation,
  installation, and version reporting.
- `tests/` with fixture repositories and edge-case checks.

The skill name is `pawa-repo-manager`; its display name is **Pawa Repo Manager**.

## Workspace registry

The workspace registry is `D:\cp\pp\repo.json`. It is separate from the
reusable skill and contains repository policy, not cached status.

Each entry records:

- stable name and relative path;
- repository, nested repository, worktree, shared-project, or ignored kind;
- active/archive/ignored scope;
- expected remote and owner;
- expected default branch and upstream;
- synchronization policy;
- whether pushes, pulls, remote edits, or moves require confirmation;
- notes and schema metadata.

The registry is authoritative for configured policy. Discovery may propose new
entries but must never silently delete or downgrade existing entries.

Generated runtime data belongs under `.pawa-repo-manager/` and includes status
snapshots, plans, action logs, lock metadata, and migration backups. Tokens and
credentials must never be stored there or in `repo.json`.

Both files use explicit schema versions so future changes can be migrated safely.

## Discovery and classification

Discovery scans configured roots while excluding `_repo-archives`, `release`,
build output, dependency caches, and policy-defined paths. It validates Git
repositories with Git commands rather than assuming that any `.git` directory
is valid.

It separately identifies:

- normal repositories;
- nested repositories;
- worktrees and submodules;
- incomplete Git shells;
- shared project folders without their own Git metadata;
- missing paths and duplicate repository identities.

Remote URLs are normalized for comparison and credentials are redacted in all
output. Before any push or remote mutation, the configured identity must match
the fetched remote identity and the user-approved target.

## Operating modes

### Audit

Read-only. Discover repositories, fetch no data unless requested, collect fresh
status, and produce a report.

### Plan

Fetch remotes, recalculate status, and produce proposed operations without
changing working trees, branches, remotes, or files.

### Sync

Execute only operations allowed by policy and explicitly approved by the user.
Fast-forward-only updates are the default safe mutation. Pushes, upstream setup,
remote repairs, merges, rebases, and moves require exact-target confirmation.

Every operation ends with a table containing one row for every touched or
evaluated repository:

| Repository | Action | Before | Result | After | Notes |
|---|---|---|---|---|---|

Results use `Success`, `Skipped`, `Blocked`, or `Failed`. The report includes
commit IDs for changes and totals for touched, changed, skipped, blocked, and
failed repositories. A final status check is mandatory before reporting success.

## Hard safety rules

- Never run `reset --hard`, `clean`, force-push, delete, or automatic conflict
  resolution.
- Never pull, merge, or rebase into a dirty worktree.
- Never overwrite local modifications or untracked files.
- Never merge or rebase divergent histories automatically.
- Never push without approval of the exact repository, branch, remote, and
  commit range.
- Never modify excluded paths unless the user explicitly includes them.
- Never trust a changed or unverified remote URL.
- Stop a batch when an unexpected conflict, permission failure, or identity
  mismatch occurs.
- Use a workspace lock to prevent concurrent manager actions.
- Preserve an action log and a resumable failure report.

## Synchronization policy

The manager classifies repositories as clean/synced, dirty, ahead, behind,
diverged, no-upstream, missing-remote, inaccessible, or invalid. It may
fast-forward a clean, behind-only repository when policy allows. Dirty,
diverged, missing-remote, or suspicious repositories are reported with a safe
next action and left untouched.

The manager must never interpret “fetch succeeded” as “repository synced.” It
must verify the final branch and worktree state after every mutation.

## Installation and updates

The canonical package provides installers for both Claude and Codex. Installation
must:

- validate the package before installation;
- install the same skill version into both target locations;
- report exact destination paths and versions;
- support update, verification, and uninstall;
- avoid overwriting a locally modified installation without backup or approval.

The skill package version and registry schema version are independent.

## Testing

Automated tests must cover clean/synced, dirty, ahead, behind, divergent,
no-upstream, missing-remote, inaccessible, invalid Git shell, nested repository,
worktree, excluded path, credential-redaction, lock contention, permission
failure, and interrupted-action recovery scenarios.

Tests must verify that dangerous operations are refused and that every action
produces the required per-repository summary.

## Success criteria

- One canonical skill installs and validates in both Claude and Codex.
- `repo.json` accurately records tracked workspace repositories and policy.
- Audit output reliably distinguishes active repositories, shared folders,
  nested repositories, incomplete shells, and excluded paths.
- Safe synchronization can run in batches without overwriting local work.
- Risky actions require exact approval and are fully logged.
- Every action reports understandable before/result/after state per repository.
