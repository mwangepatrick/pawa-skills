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

The workspace registry is `repo.json` at the workspace root. For this workspace
that is `D:\cp\pp\repo.json`; the manager must resolve the root from the
manifest location so the same skill works from another machine or operating
system. It is separate from the reusable skill and contains repository policy,
not cached status.

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
the fetched remote identity and the user-approved target. Remote repair must
never infer a replacement URL: the user must provide or explicitly approve the
complete new URL.

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

Audit and plan actions report every evaluated repository. Mutating actions report
every touched repository and any dependency that blocked it. Every action ends
with a table:

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
  commit range. The approval preview must include commit subjects and the
  destination remote URL.
- Never modify excluded paths unless the user explicitly includes them.
- Never trust a changed or unverified remote URL.
- Stop a batch when an unexpected conflict, permission failure, or identity
  mismatch occurs.
- Use a workspace lock to prevent concurrent manager actions.
- Preserve an action log and a resumable failure report.

The lock must be created atomically and contain the process, host, start time,
operation, and manager version. A stale lock requires an explicit override and
must be preserved in the action log.

## Synchronization policy

The manager classifies repositories as clean/synced, dirty, ahead, behind,
diverged, no-upstream, missing-remote, inaccessible, or invalid. It may
fast-forward a clean, behind-only repository when policy allows. Dirty,
diverged, missing-remote, or suspicious repositories are reported with a safe
next action and left untouched.

It must also classify detached HEADs, unborn repositories, tags checked out as
worktrees, submodules, and linked worktrees. These states are never silently
converted to ordinary branches.

The manager must never interpret “fetch succeeded” as “repository synced.” It
must verify the final branch and worktree state after every mutation.

## Installation and updates

The canonical package provides installers for both Claude and Codex. By default,
the Codex installer targets `$CODEX_HOME/skills/pawa-repo-manager`, falling back
to the user's `.codex/skills/pawa-repo-manager` directory. The Claude installer
targets the user's global `.claude/skills/pawa-repo-manager` directory, with an
explicit configuration override. Installers must display the resolved paths
before writing and verify the installed version afterward.

Installation must:

- validate the package before installation;
- install the same skill version into both target locations;
- report exact destination paths and versions;
- support update, verification, and uninstall;
- avoid overwriting a locally modified installation without backup or approval.

The skill package version and registry schema version are independent.

## Commands

The skill must document and implement these commands:

- `audit` — read-only inventory and current status.
- `plan-sync` — fetch and show safe and risky proposed actions.
- `sync` — execute approved safe actions and produce the final table.
- `push` — preview exact commit ranges and require explicit approval.
- `install` — install or update the skill in Claude and Codex.
- `verify` — validate the skill, registry, installation, and remotes.
- `unlock` — inspect and explicitly clear a stale workspace lock.

Commands must return a useful exit status: success only when all requested
actions completed; a distinct blocked/partial status when work was skipped or
blocked; and failure when an unexpected operation error occurs.

## Failure, logging, and recovery

Independent safe operations may continue after a repository is blocked, but the
batch must stop on an unexpected conflict, permission error, identity mismatch,
or lock violation. The final report must identify all completed, skipped,
blocked, and failed operations and provide a resumable next action.

Action logs must redact access tokens, passwords, credential-bearing URLs,
authorization headers, and sensitive command output. Each log entry records the
repository, operation, before state, approval, command class, result, after
state, and manager version without exposing secrets.

## Testing

Automated tests must cover clean/synced, dirty, ahead, behind, divergent,
no-upstream, missing-remote, inaccessible, invalid Git shell, nested repository,
worktree, excluded path, credential-redaction, lock contention, permission
failure, and interrupted-action recovery scenarios.

Tests must verify that dangerous operations are refused and that every action
produces the required per-repository summary. They must also cover detached
HEAD, unborn repositories, worktrees, submodules, stale locks, partial batches,
exit statuses, installation overrides, and secret redaction.

## Success criteria

- One canonical skill installs and validates in both Claude and Codex.
- `repo.json` accurately records tracked workspace repositories and policy.
- Audit output reliably distinguishes active repositories, shared folders,
  nested repositories, incomplete shells, and excluded paths.
- Safe synchronization can run in batches without overwriting local work.
- Risky actions require exact approval and are fully logged.
- Every action reports understandable before/result/after state per repository.
