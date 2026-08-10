# Pawa Repo Manager Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable `pawa-repo-manager` skill that inventories, audits, plans, and safely synchronizes configured repositories from both Claude and Codex.

**Architecture:** Keep one canonical skill package under `pawa-skills/pawa-repo-manager`. Implement deterministic repository operations in a dependency-free Python CLI, use `repo.json` for workspace policy, and keep generated status/action data under `.pawa-repo-manager`. The skill instructions provide the safety contract and route user requests to the CLI; installers copy the same package into Claude and Codex skill directories.

**Tech Stack:** Python 3 standard library, Git CLI, JSON, Markdown, YAML frontmatter, unittest fixtures, Claude/Codex skill folders.

---

## File map

- Create `pawa-repo-manager/SKILL.md`: trigger metadata and agent workflow.
- Create `pawa-repo-manager/agents/openai.yaml`: Codex display metadata.
- Create `pawa-repo-manager/references/workspace-policy.md`: policy semantics and report contract.
- Create `pawa-repo-manager/references/claude-install.md`: Claude installation and update behavior.
- Create `pawa-repo-manager/references/codex-install.md`: Codex installation and update behavior.
- Create `pawa-repo-manager/scripts/repo_manager.py`: CLI, discovery, status, planning, and safe Git operations.
- Create `pawa-repo-manager/scripts/install_skill.py`: validated dual-platform installation.
- Create `pawa-repo-manager/scripts/validate_skill.py`: package and registry validation.
- Create `pawa-repo-manager/tests/test_repo_manager.py`: fixture-based safety and status tests.
- Create `repo.json`: current workspace registry with active, nested, shared, and ignored entries.
- Create `D:\cp\pp\.gitignore` additions only if the root repository has an applicable ignore file; otherwise keep generated runtime data outside tracked repositories.
- Modify `pawa-skills/docs/superpowers/specs/2026-08-10-pawa-repo-manager-design.md` only if implementation discovers a genuine contract correction.

### Task 1: Scaffold the canonical skill package

**Files:**
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\` using the skill creator initializer.
- Create: generated `SKILL.md`, `agents/openai.yaml`, `references/`, and `scripts/` paths.

- [ ] **Step 1: Run the skill initializer**

Run:

```powershell
python C:\Users\ADMIN\.codex\skills\.system\skill-creator\scripts\init_skill.py pawa-repo-manager --path D:\cp\pp\pawa-skills --resources scripts,references
```

Expected: `D:\cp\pp\pawa-skills\pawa-repo-manager` exists with required skill metadata and resource folders.

- [ ] **Step 2: Replace generated metadata with the canonical trigger**

Use this frontmatter in `SKILL.md`:

```yaml
---
name: pawa-repo-manager
description: Safely inventory, audit, plan, and synchronize configured Git repositories with workspace policy, remote validation, dry-run planning, lock protection, and per-repository action summaries. Use when managing multiple repositories, checking repository health, syncing repositories, repairing approved remotes, or installing the manager in Claude or Codex.
---
```

- [ ] **Step 3: Add the skill workflow**

Document that the agent must locate `repo.json`, run audit before mutation, use `plan-sync` for batches, require exact approval for pushes/merges/rebases/remote edits/moves, never use destructive Git commands, and always end with the required repository table.

- [ ] **Step 4: Commit the scaffold**

```powershell
git -C D:\cp\pp\pawa-skills add pawa-repo-manager
git -C D:\cp\pp\pawa-skills commit -m "Scaffold Pawa Repo Manager skill"
```

### Task 2: Implement registry loading and repository discovery

**Files:**
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py`
- Create: `D:\cp\pp\repo.json`
- Test: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`

- [ ] **Step 1: Write tests for registry and classification**

Use temporary fixture directories containing a valid repository, a dirty repository, a `.git` shell, a nested repository, and an ignored archive. Assert that discovery returns the configured repository kinds and never returns ignored paths as active repositories.

- [ ] **Step 2: Define the registry schema**

Implement `schemaVersion`, `workspace`, `ignorePaths`, and `repositories`. Each repository entry must include `name`, relative `path`, `kind`, `scope`, `remote`, `defaultBranch`, and `syncPolicy`. Validate that paths remain inside the workspace and that duplicate names/paths are rejected.

- [ ] **Step 3: Implement safe Git subprocess helpers**

Use `subprocess.run([...], cwd=repo_path, text=True, capture_output=True, check=False)` with argument arrays. Redact credential-bearing URLs before storing or displaying output. Never invoke a shell string.

- [ ] **Step 4: Implement discovery**

Resolve the workspace from the manifest location, normalize relative paths, skip configured exclusions, validate repositories with `git rev-parse --show-toplevel`, and classify invalid `.git` shells, nested repositories, worktrees, submodules, shared project folders, and missing paths.

- [ ] **Step 5: Run focused tests**

```powershell
python -m unittest D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py -v
```

Expected: registry and classification tests pass.

- [ ] **Step 6: Commit the registry layer**

```powershell
git -C D:\cp\pp\pawa-skills add pawa-repo-manager/scripts/repo_manager.py pawa-repo-manager/tests/test_repo_manager.py
git -C D:\cp\pp\pawa-skills commit -m "Add repo registry and discovery"
```

### Task 3: Add audit, status, and mandatory tabular reporting

**Files:**
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\references\workspace-policy.md`

- [ ] **Step 1: Write status tests**

Cover clean/synced, dirty, ahead, behind, diverged, no-upstream, missing remote, detached HEAD, and unborn repository states. Assert that the status classification includes both the raw counts and a human-readable state.

- [ ] **Step 2: Implement status collection**

Collect branch, upstream, remote, HEAD, latest commit, worktree status, ahead/behind counts, remote identity, and special Git state. Treat fetched state as separate from synchronized state.

- [ ] **Step 3: Implement report rendering**

Render columns exactly as `Repository | Action | Before | Result | After | Notes`, followed by totals for touched, changed, skipped, blocked, and failed. Redact secrets and include commit IDs for changes.

- [ ] **Step 4: Implement `audit`**

`audit` must be read-only, evaluate every configured entry, write a non-authoritative status snapshot under `.pawa-repo-manager`, and print the complete table.

- [ ] **Step 5: Validate report behavior**

```powershell
python D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py audit --manifest D:\cp\pp\repo.json
```

Expected: active repositories, nested repositories, shared folders, invalid shells, and ignored paths are clearly distinguished.

- [ ] **Step 6: Commit audit/reporting**

```powershell
git -C D:\cp\pp\pawa-skills add pawa-repo-manager
git -C D:\cp\pp\pawa-skills commit -m "Add repository audit and status reports"
```

### Task 4: Implement fetch, planning, locks, and safe synchronization

**Files:**
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\references\workspace-policy.md`

- [ ] **Step 1: Test dry-run planning and safety refusal**

Assert that dirty repositories never receive pull commands, divergent repositories produce blocked plans, pushes require an approval token supplied to the operation, and destructive command strings are rejected before execution.

- [ ] **Step 2: Implement atomic workspace locking**

Create `.pawa-repo-manager/lock.json` with exclusive creation. Store process ID, host, start time, operation, and manager version. Refuse active locks; stale locks require `--override-stale-lock` and remain in the action log.

- [ ] **Step 3: Implement fetch and `plan-sync`**

Fetch only configured remotes, refresh status, and generate JSON plus Markdown plans. Do not modify worktrees, branches, remotes, or files in plan mode.

- [ ] **Step 4: Implement safe synchronization**

Allow only clean, behind-only, fast-forward updates through `git pull --ff-only`. Leave dirty, divergent, suspicious, missing-remote, detached, and invalid repositories untouched. Stop on conflicts, permission errors, identity mismatches, or lock violations.

- [ ] **Step 5: Implement explicit push preview**

Before push, show repository, branch, redacted remote, local/remote commit IDs, commit subjects, and exact commit range. Require explicit approval of that preview; reject force-push.

- [ ] **Step 6: Implement action logs and exit statuses**

Log before state, approval, command class, result, after state, and manager version with secret redaction. Return success only when all requested operations complete, a distinct partial/blocked status when operations are skipped or blocked, and failure for unexpected errors.

- [ ] **Step 7: Run safety tests and a dry-run**

```powershell
python -m unittest D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py -v
python D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py plan-sync --manifest D:\cp\pp\repo.json
```

- [ ] **Step 8: Commit synchronization**

```powershell
git -C D:\cp\pp\pawa-skills add pawa-repo-manager
git -C D:\cp\pp\pawa-skills commit -m "Add safe repository synchronization"
```

### Task 5: Add remote repair, move policy, and special Git handling

**Files:**
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`

- [ ] **Step 1: Test remote identity refusal**

Assert that a changed or unverified remote blocks push and that a remote repair cannot proceed without an explicit complete replacement URL.

- [ ] **Step 2: Implement approved remote repair**

Require the repository path, current remote, replacement remote, and explicit approval. Fetch the replacement remote before changing configuration, write the old remote to the action log, and verify the new remote after mutation.

- [ ] **Step 3: Implement archive/move protection**

Require explicit inclusion of excluded paths, validate source and destination containment, refuse moves with dirty worktrees unless separately approved, and verify the destination repository after moving.

- [ ] **Step 4: Implement special-state refusal**

Return blocked status for detached HEAD, unborn repositories, worktrees, submodules, and invalid Git shells unless a dedicated approved operation exists.

- [ ] **Step 5: Commit special handling**

```powershell
git -C D:\cp\pp\pawa-skills add pawa-repo-manager
git -C D:\cp\pp\pawa-skills commit -m "Harden remote and repository state handling"
```

### Task 6: Add Claude/Codex installation and validation

**Files:**
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\install_skill.py`
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\validate_skill.py`
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\references\claude-install.md`
- Create: `D:\cp\pp\pawa-skills\pawa-repo-manager\references\codex-install.md`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\agents\openai.yaml`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\SKILL.md`
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`

- [ ] **Step 1: Write installer tests**

Use temporary home directories and assert that installation resolves `CODEX_HOME` when present, otherwise `.codex/skills`; resolves the Claude override/default; backs up modified destinations; and verifies identical package versions.

- [ ] **Step 2: Implement package validation**

Validate frontmatter, skill name, required files, `agents/openai.yaml`, script syntax, references, and version metadata. Run the existing `quick_validate.py` as an additional check.

- [ ] **Step 3: Implement dual installation**

Display resolved destinations before writing, refuse silent overwrite of modified installations, create backups with timestamps when approved, copy the canonical package, and verify installed hashes/version.

- [ ] **Step 4: Document commands and install paths**

Document `audit`, `plan-sync`, `sync`, `push`, `install`, `verify`, and `unlock`, including expected report output and failure statuses.

- [ ] **Step 5: Commit installation support**

```powershell
git -C D:\cp\pp\pawa-skills add pawa-repo-manager
git -C D:\cp\pp\pawa-skills commit -m "Add Claude and Codex installation support"
```

### Task 7: Populate and verify the workspace registry

**Files:**
- Create: `D:\cp\pp\repo.json`
- Create or update: `D:\cp\pp\.gitignore` only if a root Git repository exists and tracks workspace metadata.
- Modify: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`

- [ ] **Step 1: Build the registry from current workspace evidence**

Include active repositories and nested repositories discovered under `D:\cp\pp`. Mark `_repo-archives` and `release` as ignored, mark shared project folders as `shared-project`, and record suspicious remotes such as the current `pawapos-etims-bridge` remote in notes without changing them.

- [ ] **Step 2: Validate the registry**

```powershell
python D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\validate_skill.py --manifest D:\cp\pp\repo.json
python D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py audit --manifest D:\cp\pp\repo.json
```

Expected: manifest paths resolve inside the workspace, ignored paths are excluded, duplicate identities are reported, and every action produces the required table.

- [ ] **Step 3: Commit the workspace registry only if its owning repository is defined**

Do not commit `D:\cp\pp\repo.json` to an unrelated repository. If the workspace root is not itself a Git repository, leave the registry as a local workspace artifact and record that decision in the final report.

### Task 8: Final validation and handoff

**Files:**
- Test: `D:\cp\pp\pawa-skills\pawa-repo-manager\tests\test_repo_manager.py`
- Inspect: all files under `D:\cp\pp\pawa-skills\pawa-repo-manager`

- [ ] **Step 1: Run syntax and unit validation**

```powershell
python -m compileall D:\cp\pp\pawa-skills\pawa-repo-manager
python -m unittest discover -s D:\cp\pp\pawa-skills\pawa-repo-manager\tests -v
python C:\Users\ADMIN\.codex\skills\.system\skill-creator\scripts\quick_validate.py D:\cp\pp\pawa-skills\pawa-repo-manager
```

- [ ] **Step 2: Run read-only real-workspace audit**

```powershell
python D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py audit --manifest D:\cp\pp\repo.json
```

Expected: no archive or `release` operations, no secret leakage, clear nested/shared/invalid classification, and a complete table.

- [ ] **Step 3: Run plan-only synchronization**

```powershell
python D:\cp\pp\pawa-skills\pawa-repo-manager\scripts\repo_manager.py plan-sync --manifest D:\cp\pp\repo.json
```

Expected: no worktree or remote mutations; dirty and divergent repositories are blocked with safe next actions.

- [ ] **Step 4: Verify both installations**

Install to temporary Claude and Codex roots, compare package versions and hashes, and run `verify` against both destinations.

- [ ] **Step 5: Review final diff and commit**

```powershell
git -C D:\cp\pp\pawa-skills diff --check
git -C D:\cp\pp\pawa-skills status --short
git -C D:\cp\pp\pawa-skills add pawa-repo-manager
git -C D:\cp\pp\pawa-skills commit -m "Complete Pawa Repo Manager skill"
```

Expected: only the skill package, its tests, and approved documentation are changed.
