# Example: BO customer-deposit migration

Source inspected 2026-11-08. This is an observed existing call chain, not a transaction/concurrency template. Line numbers are lookup hints; verify current method declarations after edits.

1. `D:/cp/pp/pawapos-bo/admin/FrmCustomerDepositMigration.cs`, around lines 63 and 89, constructs `CustomerDeposit` and calls `deposit.RegisterMigration(Pos.CurrentUser["id"].ToString())`.
2. `D:/cp/pp/pawapos-shared/CustomerDeposit.cs`, `RegisterMigration`, around lines 17–32, obtains `Main.db`, reads a number through `SelectValueByKeyValue`, then calls `db.Insert("deposits", Dictionary<string, object>)`.
3. `D:/cp/pp/pawapos-shared/Main.cs`, around lines 13 and 33, declares the shared `db` field as `PawaDb.Db` and initializes it. Shared state and PostgreSQL implementation are distinct owners.
4. `D:/cp/pp/pawapos-db/Db.cs`, Dictionary-based `Insert` overload around lines 229–242, creates and executes the Npgsql command.

The project-reference route agrees with the observed call chain: BO `pos.csproj` references `PawaShared.csproj`; `PawaShared.csproj` references `PawaDb.csproj`. Those references alone would not prove that this particular operation uses the DB wrapper.

When asked to change this behavior, inspect the relevant form and shared method, then find other callers before deciding whether the rule is form-specific or shared. Changes to the insert mechanism belong in the DB wrapper only when they concern PostgreSQL mechanics rather than deposit policy.
