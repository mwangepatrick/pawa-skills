# Search and ReSearch

### Golden Rule: Reuse Search/ReSearch

When adding or modifying listing search, inspect an existing form using the same grid and reuse its shared search implementation. **Search** is the first free-text term; **ReSearch** refines those results with a second term. Each term may match a different searchable column: `(column A OR column B ...) AND (column A OR column B ...)`. ReSearch is not refresh, reload, or clear.

Select the helper by the actual control and binding contract; verify the referenced assembly supports it:

| Grid | Existing implementation | Binding requirement |
|---|---|---|
| Legacy `DataGridViewX` | `Shared.search_grid(search, grid)` and `Shared.re_search_grid(search, research, grid)` | `BindingSource` backed by `DataTable`; searches string columns |
| Syncfusion `SfDataGrid` | `PawaUtils.SfGridCtrls.ApplyMultipleFilters(grid, Dictionary<string,string>)` with Search and ReSearch entries | Assign a `DataTable` before calling; returns a `DataView` to bind afterward. Does not accept a `DataView` or `BindingSource` directly |
| Existing `PawaControls.PawaGrid` | Built-in two search inputs and filtering; inspect `SearchColumns` when needed | Preserve the control's existing binding contract |

Verified source references in the usual workspace: `D:\cp\pp\pawapos-shared\Shared.cs`, `D:\cp\pp\PawaUtils\SfGridCtrls.cs`, and `D:\cp\pp\pawa-controls\PawaControls\PawaGrid.cs`. A legacy example is `purchase_ledger/master/FrmSupplier.cs`. Recheck these APIs in the target checkout rather than assuming every version is identical.

- For forms with separate search fields, declare `txt_search` and `txt_research`, labels **Search** and **ReSearch**, aligned heights, and event wiring in Designer. Recompute both terms together on either field changing. Clearing one removes only that term; clearing both restores the base filtered results. Preserve both terms on ordinary refresh.
- Preserve date, branch, location, status, payment-mode, cashier, and permission filters. Shared helpers can replace `RowFilter`; apply base filters first to an appropriate separate table or use a compatible shared composition path. Search must never restore rows excluded by those filters. Preserve exact stored-code comparisons and value casing independently of case-insensitive text search.
- Counts, totals, selection/actions, and export must use the resulting filtered rows. Follow existing uppercase input and keyboard conventions without modifying stored values.
- Do not introduce a form-specific matching engine, hidden normalized search column, or substitute Clear for ReSearch when a compatible shared implementation exists. Do not migrate the grid solely to obtain search. Investigate binding/API mismatches first; extend the shared helper only when necessary and within the authorized scope.
- Verify each term alone and both together across different columns, clearing independently and together, empty/null values, apostrophes and existing wildcard behavior, base-filter and code-casing preservation, refresh persistence, totals/export, keyboard navigation, and Designer/runtime layout. Do not claim literal wildcard matching unless the helper implements it.
