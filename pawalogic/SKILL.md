---
name: pawalogic
description: Use when locating PawaPos classes or business logic across repositories, understanding project relationships, finding an authoritative implementation, or deciding which existing project and namespace should own new code under D:\cp\pp or D:\cp\wpf.
---

# Pawalogic

Navigate the existing Pawa system and recommend placement from current source evidence. Present architectural improvements separately from the immediate recommendation.

## Find the owner

1. Read the affected repository's `AGENTS.md` and applicable domain/architecture docs. Use [the system map](references/system-map.md) to select the relevant group; load only that group's source docs.
2. Use `scripts/lookup.py` for bounded project/type/dependency queries; see [lookup commands](references/lookup.md). The default roots are `D:\cp\pp` and `D:\cp\wpf`; override them if the checkout moved. Query an existing snapshot first. Refresh explicitly if absent, incomplete, stale for this task, or after branch changes/additions.
3. Narrow by full project path. A folder, Git repository, project, assembly and namespace are different identities. Duplicate project/type names require disambiguation; nearest-directory project ownership in the index is only a candidate. Confirm the repository boundary with `git -C <dir> rev-parse --show-toplevel` and `repo.json`: a sibling folder is not necessarily inside the nearby repo (e.g. `pawapos-fo/LiteEngine` is a separate repo, not part of `pawapos-fo/PawaPosFo`).
4. Verify the declaration, namespace, project compile inclusion, relevant callers and owning repo's instructions in current source. Trace business behavior through actual calls; manifest dependencies alone establish possible references. Read short excerpts or use scoped `rg -n -F` with explicit files/globs. Expand the scope only when a targeted query has no useful result.
5. For new code, apply [placement guidance](references/placement.md): reuse existing behavior first; keep the rule with its business owner and inspect actual consumers before sharing it. Explain the recommended repo, project, folder/namespace, closest existing example, caller impact and evidence.

## Answer compactly

Return exact paths/type names, their role and the source that supports the answer. Distinguish verified facts, placement recommendations and unresolved ownership. For a dependency answer, state whether evidence is a project reference, DLL hint, package, database/API/queue interaction, or an observed call. A DLL/package path does not establish business ownership.

If a match changed or disappeared, verify source or refresh before relying on it. A snapshot with scan errors or no matches does not prove absence. The index covers lexical C# type declarations and .NET/Node manifests, not method bodies, complete language semantics, reflection or runtime wiring; use source search for these.

## Maintain the map

Keep generated facts in the local cache, out of committed references. Update curated ownership notes when source proves a durable change, with evidence and review date; preserve uncertainties until resolved. Use existing repo glossaries for business definitions and ADRs for agreed trade-offs. Traced flows: [deposit](references/deposit-flow.md) and [local queue](references/queue-flow.md).

When evaluating or extending this skill, consult [validation evidence and gaps](references/validation.md).

This skill advises and navigates. Repository synchronization, schema changes, UI standards and production diagnosis remain with their existing repo instructions and relevant Pawa skills. Lookup does not run builds, load assemblies, contact services or change application data.
