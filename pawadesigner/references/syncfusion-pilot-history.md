# Syncfusion Full-Stack Pilot (history)

Preserved verbatim from the Claude-side copy of this skill (2026-08-11). It describes the original
scoped pilot that first used Syncfusion controls for data entry. It is kept for reference only; the
Hard Rules and Golden Rules in SKILL.md take precedence where they differ.

## Syncfusion Full-Stack Pilot (scoped exception, 2026-08-11)

`DepartmentalStockSales.cs` (D:\cp\pp\pawapos-bo\pos_ledger\) is a deliberate, explicitly-scoped pilot of using **Syncfusion controls for data entry too**, not just the `SfForm` base class — i.e. an intentional exception to the "Data entry controls are standard .NET" hard rule above, requested and scoped by the user to that one form only. It is not yet the project default — don't copy this pattern into other forms without the same explicit "this form only" confirmation from the user.

What changed on that form: `SfForm` (base), `SfComboBox` (category/department filters), `SfDateTimeEdit` (date filters), `SfButton` (action buttons), `SfDataGrid` (results grid), `SfNumericTextBox` (disabled numeric summary fields). Component-specific gotchas, verified property/event names, and copy-pasteable PawaPos patterns for each are documented in:
- [[pawadesigner-sfform]] (references/sfform.md)
- [[pawadesigner-sfdatagrid]] (references/sfdatagrid.md)
- [[pawadesigner-sfcombobox]] (references/sfcombobox.md) — note `SfComboBox` and `SfButton` were already in real use elsewhere (`DiaPackingMaster.cs`) before this pilot
- [[pawadesigner-sfdatetimeedit]] (references/sfdatetimeedit.md) — the real Syncfusion WinForms class is `SfDateTimeEdit`, not "SfDateTimePicker"
- [[pawadesigner-sfnumerictextbox]] (references/sfnumerictextbox.md)
- [[pawadesigner-sfbutton]] (references/sfbutton.md)

Key risk carried by this pilot: `ThemeManager.cs` has no styling support for `SfDataGrid`/`SfComboBox`/`SfDateTimeEdit`/`SfButton` (only `SfNumericTextBox` gets it for free, since it inherits `TextBox`) — each reference doc above explains what manual styling was needed to compensate, reusing `ThemeManager`'s existing color tokens rather than hand-coded literals.
