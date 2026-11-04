---
name: pawadesigner
description: Use when designing, auditing or modifying PawaPos forms, listings, reports, dialogs, controls, layouts or validation patterns.
---

# PawaDesigner

Apply PawaPos UI standards through the project's actual shared controls and APIs. User instructions and approved scope take precedence.

## Scope first

- **Preserve the existing layout unless the user requests a layout change.** Keep field order, grouping, relative positions, size and workflow. Replacing controls or fixing styling does not authorize redesign. Identify unavoidable clipping/fit conflicts before moving fields and propose the smallest adjustment.
- Carry existing authorization forward. Work within scope without repeated approval gates or unrelated refactors. For reported failures, establish the cause before changing behavior.
- Preserve business calculations, transactions, permissions, sorting, filters, selection, validation, stored-value casing and keyboard behavior.
- Read this entrypoint once, then only references relevant to the task. Use bounded source searches and concise build/test output; avoid loading every reference or restating generic tutorials.

## Working checklist

1. **Inspect the touched form completely.** Confirm solution/project/source/Designer paths, controls, events, bindings, shared libraries and comparable working forms. Search PawaDb, PawaUtils, PawaControls, PawaShared and existing services before adding infrastructure. Keep business rules in services and presentation in forms.
2. **Prove the control path before migration.** Use `SfForm` and compatible installed Syncfusion controls. Audit direct/transitive assembly versions, HintPaths, Copy Local and designer-host architecture. Document a fallback only where the equivalent is missing or loses behavior. Follow the migration gate in [Designer workflow](references/designer-workflow.md).
3. **Keep Designer ownership.** Use conventional Designer-generated declarations/properties/events. Start with `InitializeComponent()` and a design-time guard before database, singleton, device or file access. Set the executable icon at runtime and fixed form sizing. Runtime-only control factories do not establish Designer support.
4. **Apply shared presentation.** Use the referenced `PawaControls.ThemeManager` and shared controls. Verify source and deployed DLL APIs; centralize fonts, palettes, spacing and interaction states. Check Designer/runtime agreement and that the tested application actually loads the new binaries.
5. **Preserve values and feedback contracts.** Bind uppercase human-readable dropdown labels separately from original codes; use selected values in logic. Set editable text CharacterCasing to Upper in Designer, or use the audited control equivalent, without silently rewriting historical records. Use verified PawaUtils.Dialogs APIs on the owning UI thread plus ErrorProvider. Suppress user validation during programmatic loading/reset. See [shared services and feedback](references/shared-services-feedback.md).
6. **Verify proportionally, then stop.** Finish source changes before compiling the test binary. Run existing checks and meaningful regressions for changed behavior; inspect the rendered form. A build is not a visual or actual Designer-load check. Report implementation, checks and unverified behavior separately using [Designer workflow](references/designer-workflow.md).

## Presentation requirements

- **Commands:** Save/Submit/main Apply orange; supporting utilities grey; Close/Cancel black; service/tools blue; final destructive commands red. New/Edit/Delete selectors use white outlined shared `PawaStateButton` controls and mutually exclusive group coordination. Selecting a mode does not execute deletion. Read [button/dropdown standards](references/buttons-dropdowns.md) for exact normal/hover/pressed/disabled/focus palettes, sizing and labels, and [action states](references/action-states.md) when changing form modes.
- **Layout:** For new or approved layout work, use ThemeManager's 28px inputs, 36px row pitch, 16px margins and 36px commands. Compute same-row heights/label centers. Use a bottom-docked command footer, fill-docked scrolling body and screen-height cap. Fit 1366x768 at 100%; verify 125%/150% on 1920x1080. Preserve the user's arrangement during maintenance; flag constraints instead of silently reflowing it. Read [layout fit](references/layout-fit.md) when sizing/layout is in scope.
- **Fields:** Right-align numbers and compact operational identifiers; left-align names/descriptions. Choose read-only versus disabled deliberately. Disabled displays skip Tab and stay readable; display text centers vertically through load/font/size/handle changes. Date inputs use `dd/MM/yyyy`.
- **Grids:** Hide row headers and keep a visible border. Description is the sole detail-grid fill column; keep codes, numbers, dates and checkboxes compact/fixed-width. SfDataGrid uses `LastColumnFill` for a final free-text column or column `Fill` elsewhere; use `MinimumWidth`, not explicit fill-column `Width`. Preserve full-row navigation/selection, branded states, alternating rows and conditional highlights. Humanize headers; timestamps show `dd/MM/yyyy HH:mm`. Read [grid/display rules](references/grid-display-consistency.md).
- **Receipt payments:** Display/export omit exactly zero payment amounts and retain negative refunds. Scope this to receipt payments, preserve meaningful zeros elsewhere, and do not alter stored records.

## Read only when relevant

| Task | Reference |
| --- | --- |
| Search / ReSearch | [Shared search contracts](references/search-research.md) |
| Form base / dependencies | [SfForm](references/sfform.md) |
| Dropdown migration | [SfComboBox](references/sfcombobox.md) |
| Commands | [SfButton](references/sfbutton.md) |
| Grid migration | [SfDataGrid](references/sfdatagrid.md) |
| Date controls | [SfDateTimeEdit](references/sfdatetimeedit.md), [legacy fallback](references/sfdatetimepicker.md) |
| Numeric controls | [SfNumericTextBox](references/sfnumerictextbox.md) |

Use a compact ASCII sketch when a requested layout change benefits from comparison. [Pilot history](references/syncfusion-pilot-history.md) is historical evidence, not current policy. Verify API claims against the target checkout rather than guessing helpers or dependencies.

## Maintain and install

The tracked source is `D:\cp\pp\pawapos-shared\.codex\skills\pawadesigner`. Update requested durable rules there, keeping detailed requirements in one authoritative reference. A one-off form choice does not authorize a universal redesign requirement.

Run `scripts/Sync-Installations.ps1` to update and hash-verify the complete Codex and Claude copies. Commit/push only intended skill files and preserve unrelated work. Installed copies are snapshots; resync after changes and report the source commit and verified installation paths.
