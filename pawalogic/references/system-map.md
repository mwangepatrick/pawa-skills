# Pawa system entry points

Reviewed 2026-11-08 against local checkouts. This is a selective ownership map, not an exhaustive verified architecture. Use `lookup.py` for current manifest/type inventory. Preserve full project paths: `workspace → Git repository (if any) → project → type`; assemblies/namespaces are independent identities.

`D:/cp/pp/repo.json` supplies an existing registry including nested repos and shared projects. It is incomplete for newer groups and `D:/cp/wpf`. Discover manifests in both roots and compare rather than treating either folder names or the registry as authoritative for behavior.

Paths in the table are relative to `D:/cp/pp` unless marked WPF. **Source** means inspected types/manifests or substantive docs; **partial** means the listed identity is established but ownership/current authority needs more investigation.

| Area | Repo/project entry points | Evidence and routing |
|---|---|---|
| Desktop apps | `pawapos-bo/pos.csproj`; `pawapos-fo/PawaPosFo/Pos Cash.csproj`; `pawapos-till/Pos Till/Pos Till.csproj` | Source/project identities. FO contains a nested repository; read app-local instructions |
| Shared business logic | `pawapos-shared/PawaShared.csproj` | Source folders/types cover sales, inventory, purchases, GL, cashbook and payments; overlapping ownership with specialized libs needs caller inspection |
| Finance/loyalty | `pawapos-fin/PawaPosFin.csproj`, `pawapos-loy/Loyalty.csproj` | Source: GL and loyalty types with separate DB initialization; complete boundaries partial |
| PostgreSQL and migration queue | `pawapos-db/PawaDb.csproj`, `pawapos-dblog` | Source: query/CRUD/transaction wrapper; versioned migration policy comes from affected repo/task instructions |
| Local SQLite | `pawa-lite/PawaLiteEngine`; legacy `pawapos-fo/LiteEngine` | Read `pawa-lite/README.md` for ownership. BO references both; names are not interchangeable |
| Identity/users | `pawapos-auth`, `pawapos-user/PawaUser.csproj`, `PawaSign` | Source: authentication/crypto, user/branch/biometric types; complete signing scope partial |
| UI/startup/helpers | `pawa-controls/PawaControls`, `PawaStart`, `PawaUtils` | Source and BO references: shared controls, startup/company/connection health, dialogs/crypto/data helpers |
| Logging/mail/print | `pawapos-logger`, `pawapos-mail/PawaMail`, `pawapos-pdf/pdf` | Source/README: logging sinks, Mailgun, ESC/POS-to-PDF |
| Messages/jobs/API | `pawapos-com/SmartComServer`, `pawapos-queue/PawaQueue`, `pawapos-api/PawaApi` | Com AGENTS/source: modem/SMS/mobile-message parsing; job/API boundaries partial |
| Sync | `pawacloud-sync`, `pawapos-sync/PawaSync/PSync.csproj` | Read their READMEs: PostgreSQL outbox to cloud REST; Windows sync/backup/update service respectively |
| Other cloud helpers | `PawaSupa`, `PawaCloud`, `PawaPosX` | Project/source identity only; product authority and complete responsibilities unresolved |
| Shared updater | `pawa-updates` | Read README first: Core/Support/Windows/Updater; app-specific BO/FO adapters; old excluded FO copies are historical |
| Other distribution/installers | `pawapos-upd`, `pawapos-updater`, `pawapull`, `pawapos-isc`, `PawaInstall` | `pawapull` README documents manifest downloader; installer templates/DB manager identities inspected. Legacy updater authority unresolved |
| Licensing/testing/tools | `pawapos-lic/PawaLicense`, `pawapos-test`, `dbmanager/DbManager`, `pawa-tool` | Type/file identities; behavior partial. Tools include PostgreSQL command binaries |
| Tax/payment/web | `ushuru-plus-2`, `node/pawapos-etims-bridge`, `ushuru-plus`, `pawa-pay`, BO `pawapos-ui` | Bridge README documents eTIMS middleware/dashboard. Authority between tax trees unresolved; payment tree has preview HTML/nginx; BO UI is React |
| WPF PawaLoop | `D:/cp/wpf/PawaLoop` | Read AGENTS and upload/download docs: `PawaLoop` app, `PawaData` data/sync, `PawaLog` logging. `PawaLoopRouter` references this PawaLog |
| WPF PawaPos | `D:/cp/wpf/PawaPos` | Source/manifests: `PawaCore` Common/Interfaces/Models/ViewModels; its `PawaData` references Core, `PawaCloud` references Core and Data. Current product role unresolved |

## Disambiguation and dependencies

- `D:/cp/wpf/PawaLoop/PawaData/PawaData.csproj` and `D:/cp/wpf/PawaPos/PawaData/PawaData.csproj` are different projects. Ask which product only when the task and caller evidence cannot disambiguate them.
- BO declares references to Shared, DB, Finance, Auth, User, Logger, Queue, API, local engines, startup, utilities, controls and updater projects. Query a specific project for its actual current list.
- Shared declares DB; DB declares Logger and PawaUtils. A declaration is not a demonstrated runtime business flow; see the deposit example for that stronger evidence.
- A third-party package HintPath under another app's `packages` folder is package storage, not proof that the other app owns the behavior.
- `dlls`, `release`, `staging`, `latest`, package caches, build outputs and archive folders are excluded from normal indexing. Inspect them only for a task that actually concerns deployment/build provenance.
