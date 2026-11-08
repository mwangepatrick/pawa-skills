# Local lookup

Python 3.10+; standard library only. Run the script by its absolute installed or source path from any directory. Examples use the canonical source checkout:

```powershell
$lookup = 'D:\cp\pp\pawa-skills\pawalogic\scripts\lookup.py'
python $lookup status
python $lookup index
python $lookup find CustomerDeposit
python $lookup find PawaData --kind project
python $lookup find SysUploadService --scope 'wpf/PawaLoop'
python $lookup deps 'pawapos-shared/PawaShared.csproj'
python $lookup deps 'pawapos-shared/PawaShared.csproj' --incoming
```

`index` explicitly scans both roots and atomically writes `%LOCALAPPDATA%/pawalogic/architecture.json` (fallback `~/.cache/pawalogic/architecture.json`). It performs no network or Git mutations. Other commands read the snapshot and matched source-file metadata only. If filesystem permissions require it, use a writable cache explicitly:

```powershell
python $lookup --cache 'D:\scratch\pawa-index.json' index --roots 'D:\cp\pp' 'D:\cp\wpf'
python $lookup --cache 'D:\scratch\pawa-index.json' find CustomerDeposit --limit 5
```

`--cache` precedes the command. `--roots` belongs to `index`. `--scope` is a case-insensitive path substring for `find`. `--kind` selects `symbol` (default), `project` or `repo`. Symbol queries match name/namespace hints; project/repo queries also match paths. Results default to 12, maximum 100; `total_matches` reveals truncation. Prefer another focused query to increasing the limit. No-match queries return an empty result; they are not exhaustive proof.

## Evidence and freshness

- `project` edges are literal .NET ProjectReference declarations; `dll`, `assembly` and `package` remain separate. `item_condition` captures the item's own Condition only; enclosing ItemGroup/When conditions and MSBuild imports are not captured/evaluated. A null item condition does not imply an active or unconditional reference. Missing targets and expressions are labelled; declarations may be inactive.
- `--incoming` finds direct declared consumers, not transitive callers. Use a distinctive full project-path suffix to avoid merging equally named projects. Inspect callers with live `rg` after identifying the relevant projects.
- Symbols include class/interface/struct/enum/record declarations from C# source. Comments and common string literals are masked; this is a lexical aid, not Roslyn. Nested/multiple namespaces produce a `namespace_hint`, not a guaranteed fully qualified identity. Methods, VB/F#/TypeScript declarations, generated designer types and runtime reflection need source-specific search.
- `projects` on a symbol lists nearest-directory candidates, not evaluated compilation membership. Shared/linked compile items, excluded files and several projects in one folder need manifest verification. A type can have multiple partial declarations.
- `source_state` compares indexed size/mtime with a matched file. It can reveal changes/deletions but cannot detect newly added files or an unchanged timestamp collision. Refresh after branch switches, additions/renames, dependency edits, suspicious results, or when up-to-date completeness matters. `status` reports metadata, not a live audit.
- Scans skip output/dependency/archive directories and directory symlinks; exclusions are recorded in the snapshot. Regular source tests may be indexed. Repositories are discovered by `.git` file/directory, projects by manifest even without Git. `repo.json` remains a useful registry to compare against discovery, rather than an exhaustive list.
- Exit 0: completed query/scan. Exit 1: invalid input/missing snapshot/root or I/O failure. Exit 2: snapshot produced with scan errors; metadata lists them. Missing requested roots preserve the previous snapshot.

## Follow a result cheaply

Read the identified source file and its project, then search only plausible consumers:

```powershell
rg -n -F 'CustomerDeposit' 'D:\cp\pp\pawapos-bo\admin' -g '*.cs'
rg -n -F 'RegisterMigration' 'D:\cp\pp\pawapos-shared\CustomerDeposit.cs'
```

For a method lookup, start with indexed types or the relevant domain map, then use scoped source search. Keep result excerpts small. Refreshing the snapshot is a local cache operation; changing application code, Git state or database data is outside the utility.
