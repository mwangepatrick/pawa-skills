# Example: pawapos-queue network-dependent task

Source inspected 2026-11-11 (fix for `mwangepatrick/pawapos-bo#10`). Observed call chain, not a design template. Verify current declarations after edits.

1. `D:/cp/pp/pawapos-queue/PawaQueue/QueueProcessor.cs`, `PollLoopAsync`, reads `status == "new" && StartTime <= now` (batch `QueueConfig.GetBatchSize()`, default 50) through `QueueDb.GetQueueProcesses`, marks each `processing` and enqueues it. While offline it queries without network types (`email`, `watcher_log`, `data_sync`, `*newrelic*`; `RequiresNetwork`).
2. `ProcessItemAsync` runs the handler by `Type` (`TaskTypes/EmailTask.cs`, `watcher_log` via `BetterStack.cs`, `newrelic:log` via `NewRelicLogger`). On success `MarkQueueProcessAsDone`; on failure `UpdateQueueProcessRetryStatus` (increments `RetryCount`, status `error` at max).
3. No-network path: `QueueDb.RescheduleQueueProcess(id, startTime, reason)` sets status `new` and a future `StartTime` and leaves `RetryCount`. Delay is `GetNetworkFailureRescheduleDelaySeconds` (default 300).
4. `NetworkOutageTracker.cs` turns connectivity observations into one down / hourly-reminder / restored log line per outage. Connectivity is cached for `GetNetworkCheckIntervalMinutes` (default 1) in `ShouldAttemptNetworkOperation`.
5. Persistence is `LiteEngine.commons.QueueDb` (LiteDB collection `queue_process`, `QueueProcess` in `LiteEngine/data/DefaultDefinitions.cs`), in the separate `cosmopawa/pawapos-liteengine` repo at `D:/cp/pp/pawapos-fo/LiteEngine`.

Checks: `pawapos-queue/manual-tests/network-outage/Run-Checks.ps1` (console harness; no test framework exists). Pitfall: `Db.DefineConstants(name)` creates `<drive>:\local\<name>.db`; use a throwaway name in checks so the real queue DB is not touched. Retry-failure scheduling (`IncrementQueueProcessRetry`) does not set `StartTime`, so failed tasks retry on the next poll; this was not changed.
