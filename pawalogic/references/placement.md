# Placement in the current system

Reviewed 2026-11-08. These are evidence-based starting points, not blanket ownership rules. Current source and the target repository's instructions take precedence.

| Responsibility | Start here | Verify before recommending |
|---|---|---|
| BO form behavior and orchestration | `pawapos-bo` feature folders | Existing form, permissions, UI standards; use pawadesigner when modifying forms |
| BO-local pure calculation | `pawapos-bo/classes/ProductTransactions/ProductUnitCalculator.cs` as an example | Actual consumers; keep input/output calculation independent of form and DB state |
| Existing shared business objects | `pawapos-shared/PawaShared.csproj`; example `CustomerDeposit.cs` | Business owner and consumers; sharing is justified by real reuse, not a generic name |
| PostgreSQL mechanics | `pawapos-db/PawaDb.csproj`; `Db.cs`, `Db.TransactionScope.cs` | Existing CRUD/transaction interfaces; business decisions stay with their owner |
| Local queue tasks (LiteDB `queue_process`) | `pawapos-fo/LiteEngine/commons/QueueDb.cs` for persistence; `pawapos-queue/PawaQueue/QueueProcessor.cs` for polling/dispatch; handlers in `TaskTypes/` | Task state changes (status, `StartTime`, retry) belong in `QueueDb`; processing policy (network, retry, logging) in `QueueProcessor`. See [queue-flow](queue-flow.md) |
| SQLite queues/cache/events | `pawa-lite/PawaLiteEngine`, its README | README leaves PostgreSQL and freshness decisions with application data services; distinguish legacy FO LiteEngine |
| Password authentication | `pawapos-auth/Authenticator.cs` | Existing authentication entry points, security/permission invariants; user administration also spans `pawapos-user` |
| Shared updater behavior | `pawa-updates` README and Core/Support/Windows/Updater projects | App-specific adapters versus shared behavior; README identifies excluded historical FO copies |
| Startup/company/connection health | `PawaStart` | Existing entry point and consumers; inspect app-specific integration |
| WPF PawaLoop upload/download behavior | `D:/cp/wpf/PawaLoop/PawaData`, `docs/upload.md`, `docs/download.md` | Existing service and callers; UI orchestration remains in PawaLoop app project |
| WPF PawaPos models/interfaces | `D:/cp/wpf/PawaPos/PawaCore` | This is a separate tree from PawaLoop; project references alone do not establish current product authority |
| Schema, functions, permissions and configuration seeds | `pawapos-dblog` versioned queue | Read current task/release instructions and updater splitter; queued does not mean applied. Do not hardcode the receipt-specific release from BO instructions as a global version |

## Recommendation procedure

Locate an existing operation with the same responsibility. Identify its inputs, side effects and consumers. Inspect the project's existing dependencies before proposing new ones. Recommend the smallest change in the existing owner that supports the request; a second owner or generic helper is justified by concrete shared behavior.

Give a specific project/folder and namespace confirmed from nearby source, not a guessed namespace from the repo name. Call out ambiguity when the source contains overlapping implementations. Keep any proposed extraction, dependency inversion or larger redesign explicitly separate and optional unless the task requires it.

Examples are navigation anchors, not endorsements of all their transaction, concurrency or error-handling choices. For financial changes, separately verify rounding, transaction/rollback behavior, authorization and affected consumers using the target repo's checks.
