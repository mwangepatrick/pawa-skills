# Workspace Policy

`repo.json` is the authoritative policy file. Paths are relative to the
directory containing the manifest. Current status is always collected from Git
and is never trusted from the manifest.

## Safety

- `audit` is read-only.
- `plan-sync` fetches and plans but does not mutate a worktree.
- `sync` may use `git pull --ff-only` only for a clean, behind-only repository.
- `push`, remote repair, branch/upstream changes, merge, rebase, and moves need
  exact explicit approval.
- Never reset, clean, force-push, delete, or resolve conflicts automatically.
- Never touch `scope: ignored` entries without explicit inclusion.

## Entry fields

```json
{
  "name": "example",
  "path": "example",
  "kind": "repository",
  "scope": "active",
  "remote": "https://github.com/owner/example.git",
  "defaultBranch": "main",
  "syncPolicy": "fast-forward-only",
  "notes": ""
}
```

Kinds include `repository`, `nested-repository`, `worktree`, `submodule`,
`shared-project`, `invalid-git-shell`, and `missing`. Scopes include `active`,
`ignored`, and `archive`.

## Statuses and exit codes

The manager reports `clean/synced`, `dirty`, `ahead`, `behind`, `diverged`,
`no-upstream`, `missing-remote`, `inaccessible`, `detached`, `unborn`, and
`invalid`. Exit codes are 0 for complete success, 2 for blocked/partial work,
and 1 for unexpected failure.

## Lock and logs

Mutating operations create `.pawa-repo-manager/lock.json` atomically. A stale
lock requires `--override-stale-lock`. Action logs are written under
`.pawa-repo-manager/actions.jsonl` with credentials redacted.

Every command ends with a per-repository table containing action, before state,
result, after state, and notes, followed by totals.
