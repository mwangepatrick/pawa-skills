# Shared Services and Pawa Feedback

### Golden Rule: Reuse Shared Functions and Classes First

Before adding a helper, service, database wrapper, control or utility,
search the project and its referenced shared libraries for an existing
implementation. Inspect its actual source, public API and existing callers.

- Reuse compatible functionality from PawaDb, PawaUtils, PawaControls,
  PawaShared and existing application services.
- Prefer a small, backward-compatible extension to the owning shared
  library when a reusable capability is missing.
- Keep business rules in the appropriate service and presentation logic
  in the form. Do not duplicate shared infrastructure inside a form.
- Create a new implementation only when existing code cannot meet the
  requirement. Explain the concrete gap and why extension is unsuitable.
- Verify the referenced DLL contains the API before using it. Do not
  invent helper names or assume source changes are already deployed.

For database operations, prefer PawaDb. Where reads, locks and writes
must be atomic, use its scoped transaction API, such as
`Db.BeginTransactionScope()`, after verifying availability. Keep all
operations on that scope; check affected-row counts where correctness
depends on them. Do not mix independent connections into the transaction.

Verify shared changes against existing callers and report which
applications or DLLs must be rebuilt and deployed.

### Golden Rule: Use PawaDialogs for All User Feedback

Every new or modified form must use the shared Pawa dialog and toast
implementation, currently `PawaUtils.Dialogs`.

Audit the entire touched form and its directly invoked feedback paths.
Replace legacy `MessageBox` calls, `Shared.toast`, `Shared.Smart*Message`,
legacy confirmation/input dialogs and form-specific toast implementations
with the appropriate supported Pawa equivalent. This audit covers all
handlers on the touched form, including handlers unchanged by the feature;
it does not authorize an unrelated application-wide rewrite.

- Use `PawaToast` for transient feedback and the appropriate Pawa dialog
  for confirmations, blocking errors and user input.
- Verify available methods and overloads in the referenced library.
  Never guess APIs or substitute an unrelated dialog.
- Supply the owning form/control where supported.
- Preserve confirmation results, default buttons, cancellation,
  validation, keyboard behavior, severity and message meaning.
- Show feedback on the UI thread. Services return results or throw
  actionable exceptions; the form presents them.
- Keep `ErrorProvider` for field-level validation alongside Pawa feedback.
- If a required capability is missing, extend the shared implementation
  within the authorized scope rather than building a form-local copy.

Verify success, validation, failure, cancellation and background-work
paths. Report any feedback path that could not be migrated or verified.
