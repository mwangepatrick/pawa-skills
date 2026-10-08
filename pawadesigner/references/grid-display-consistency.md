# Grid and display-field consistency

Read this reference when styling SfDataGrid listings, historical detail fields,
or receipt payment details. Keep controls, properties and event wiring editable
in the Visual Studio Designer; runtime handlers may apply shared styling and
control-specific text positioning.

## SfDataGrid listing behavior and branding

For receipt/detail listings, explicitly configure:

```csharp
grid.SelectionUnit = Syncfusion.WinForms.DataGrid.Enums.SelectionUnit.Row;
grid.NavigationMode = Syncfusion.WinForms.DataGrid.Enums.NavigationMode.Row;
grid.ShowRowHeader = false;
```

Set `SelectionMode = GridSelectionMode.Single` for a single-record workflow.
Retain existing multiple selection when actions/export depend on it. For standard
DataGridView listings, use the equivalent `FullRowSelect` and hide row headers.
Do not change an intentional cell-editing workflow into a row-only workflow.

Use the actual referenced `PawaControls.ThemeManager` and its color tokens:

| Grid element | Shared token / treatment |
|---|---|
| Header background | `BrandColors.GridHeaderBackground` |
| Header text | White, Verdana 8 bold |
| Ordinary row | `UIColors.CardBackground` / `UIColors.GridText` |
| Alternate row | `UIColors.GridAlternate` / `UIColors.GridText` |
| Selected row | `UIColors.SelectionBackground` / `UIColors.SelectionForeground` |
| Current cell | Same background/text as the selected row; `UIColors.SelectionBackground` border |
| Border | `UIColors.BorderLight` |

SfDataGrid uses `Style.HeaderStyle`, `Style.CellStyle`, `Style.SelectionStyle`
and `Style.CurrentCellStyle`; styling only the header leaves default cell
selection colors behind. Apply Verdana 8 cell fonts, 35-pixel headers and
28-pixel rows as the existing theme baseline, respecting deliberate project/DPI
adjustments. Preserve one free-text fill column and existing numeric formats.

For the referenced Syncfusion 31.2.10 grid, alternate data rows through
`QueryRowStyle` using the visible row index and shared tokens. Apply striping to
data rows only, excluding headers, summaries and other special rows. Compose
with existing conditional row styling rather than overwriting business signals.
Selection styling must remain readable across the whole selected row. Check
mouse selection, keyboard navigation, sorting/filtering and focus changes.

## Display-only text fields

Choose state according to the requested interaction:

| Intended use | Properties |
|---|---|
| Values remain focusable/copyable | `ReadOnly = true`, `Enabled = true`; preserve useful Tab navigation |
| Explicitly disabled display values | `ReadOnly = true`, `Enabled = false`, `TabStop = false` |
| Editable input | Keep its existing editable behavior and validation |

Use ThemeManager tokens for disabled background, foreground and borders. For
TextBoxExt, audit `ThemeStyle.DisabledBackColor`, `DisabledForeColor` and
`DisabledBorderColor`; verify their actual rendering in the active theme.
Do not rewrite historical values or their casing while applying presentation
styles. Preserve user-requested horizontal `TextAlign` independently of vertical
centering.

Aligning labels/controls within a row does not center the text inside a tall
textbox. Use a supported vertical-alignment property when one is available.
The audited TextBoxExt fallback uses `Multiline = true`, `WordWrap = false` and
the native `EM_SETRECT` formatting rectangle: set its top inset from
`(ClientSize.Height - Font.Height) / 2`, with small horizontal margins. Native
single-line edit controls ignore this rectangle. Audit clipping, overflow and
line-break behavior before reusing this fallback outside disabled single-value
fields; it is not a general editable-input solution.

Apply centering after handles exist and again after `Shown`, `TextChanged`,
`FontChanged`, `SizeChanged` and handle recreation. Syncfusion initialization or
value loading can reset an earlier rectangle. Avoid forcing handle creation in
Designer or adding database access to styling. Verify populated fields visually
at the runtime font/DPI as well as checking properties.

## Shared helper recommendations and API status

The inspected `PawaControls.ThemeManager` currently provides `StyleDataGrid`
for standard DataGridView; `ApplyModernTheme` alone does not fully style
SfDataGrid. At this update, these helper names are recommendations, not available
methods:

- `StyleSfDataGrid(...)`: centralize header/cell/selection/current-cell colors,
  fonts, row sizes and compatible data-row striping. Respect caller selection
  mode, editing behavior, conditional styling and existing event handlers.
- `StyleDisplayTextBox(...)`: centralize explicitly chosen read-only/disabled
  state, disabled colors and vertical text positioning while preserving
  horizontal alignment. Register lifecycle handlers once and remain design-safe.

Before calling either helper, verify it exists in the referenced source and
compiled assembly. If it is absent, document the local audited fallback; only
implement shared library changes when the task authorizes that scope. When
introduced, update this API-status section and audit design-time loading.

## Receipt payment placeholders

For receipt payment detail listings, exclude exactly zero payment amounts from
the shared display/export dataset, preferably with `p.amount <> 0` in the
receipt-scoped query. Preserve receipt/date/till/operator/branch identity filters,
payment descriptions and nonzero split-payment rows. Negative amounts are
refunds and remain visible; do not replace the condition with `amount > 0`.
Handle missing/null amounts under the existing data contract rather than
silently converting them to zero.

If all rows are placeholders, show the existing empty-state message and prevent
an empty export using the established workflow. Do not delete or update stored
payments, recalculate receipt totals, or impose this rule on stock, balance,
quantity or other grids where zero may be meaningful.

## Verification

Verify populated previews and runtime behavior, including full-row selection,
alternation after sorting, conditional styling, disabled/read-only interaction,
Tab navigation and text centering after lifecycle changes. Check positive, zero
and negative payment amounts and agreement between displayed/exported rows.
Confirm the form remains loadable in its correct designer host. A build or a
.NET DesignSurface check does not establish interactive Visual Studio Designer
success; report which host was actually exercised.
