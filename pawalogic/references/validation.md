# Validation and scope

Validated 2026-11-08 against the local main checkouts; no application code, databases or Git state were changed by the lookup utility.

## Automated checks

`python tests/test_lookup.py`: 12 passing fixture/CLI checks covering duplicate project identities, nested Git directories/files, typed dependency edges and direct reverse consumers, comment/string masking, scoped symbol lookup, build-output and agent-snapshot exclusions, changed/deleted source, missing-root snapshot preservation, invalid manifests, missing reference targets, bounded read-only queries, partial-scan exit status, and record loop-variable disambiguation.

The Codex skill-creator `quick_validate.py` accepts SKILL.md. This validates metadata, not architecture correctness. Fixture tests use temporary files and only the standard Python library; the separate skill validator requires its existing PyYAML environment.

## Actual workspace coverage

Snapshot: 34 discovered Git repositories, 95 .NET/Node manifests, 2,662 lexical C# declarations and 969 declared dependency edges under `D:/cp/pp` and `D:/cp/wpf`, excluding generated/dependency/archive/agent-snapshot directories. Counts describe the indexed scope, not every possible source language or runtime relationship.

One scan error remains: `D:/cp/pp/pawapos-fo/PawaPosFo/PawaStart.csproj` is empty. It remains visible as a discovered project but its dependencies cannot be parsed. The tool returns a partial-scan status and exposes this error rather than treating coverage as complete. It does not repair the application manifest.

Live queries verified the exact `PawaShared.CustomerDeposit` source, direct Shared consumers and both distinct WPF PawaData project paths. The documented deposit operation was checked through actual form/shared/DB source, not inferred from manifest edges.

## Behavioral evaluation

An independent read-only agent answered: “Where is PawaData, who consumes it, and where should a PawaLoop-specific upload retry rule go?” Baseline used three investigation tool calls but did not establish the exact retry owner. With the skill it used two skill/reference reads plus three investigation calls and located `PawaLoop/PawaData/Services/Updates/DataSyncService.cs`, `ProcessUploadWithRetryAsync`, actual scheduled/immediate callers and WPF app wiring; it distinguished the other PawaData project and retained uncertainty about exhaustive consumers. This is one navigation scenario, not a measured general token-saving claim.

That evaluation exposed false `record in` type matches and filename-driven symbol noise. A regression fixture now covers both; the final scanner and name/namespace query behavior pass it. An independent review found no blocking ownership errors and prompted the more precise `item_condition` dependency field.

## Remaining limits

The selective map leaves several cloud/legacy/tax ownership questions unresolved and labels them accordingly. The snapshot is not a compiler, call graph or runtime inventory. Refresh explicitly after relevant source/branch changes; verify current declarations, compile inclusion and callers before edits. Non-C# symbols, generated designer types, MSBuild condition evaluation, HTTP/database/queue relationships and reflection require targeted source inspection.

Skill installation copies are separate from canonical source. After editing `D:/cp/pp/pawa-skills/pawalogic`, update the intended agent installation as well. Do not run the collection's bulk installer solely to update this skill: existing install destinations differ among tools.

## 2026-11-11 refresh

After the `pawapos-queue` network-reschedule fix (`pawapos-bo#10`): added [queue-flow](queue-flow.md); corrected the legacy local-storage row (`pawapos-fo/LiteEngine` is LiteDB, now the standalone repo `cosmopawa/pawapos-liteengine`; consumers taken from `lookup.py deps --incoming`: BO, Shared, Queue, TestCenter). Gap found: a repo-boundary mistake (assuming `pawapos-fo/LiteEngine` lived in the nearby `pawapos-fo/PawaPosFo` repo) came from path proximity, so SKILL.md step 3 now requires a `git rev-parse` check. Still open: whether `Pos Cash.csproj` and `PawaCloud` reach LiteEngine by compile-include rather than ProjectReference (the index shows no ProjectReference edge).
