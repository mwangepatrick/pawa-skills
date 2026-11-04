---
name: pawadesigner-sfdatagrid
description: SfDataGrid usage patterns for the Syncfusion-pilot form pattern in PawaPos
metadata:
  type: reference
---

# SfDataGrid

`Syncfusion.WinForms.DataGrid.SfDataGrid` is supported when its dependencies are present. It does not inherit DataGridView: use verified `PawaControls.ThemeManager.StyleSfDataGrid`. Audit the target source and DLL before migration.

## Official Docs
https://help.syncfusion.com/windowsforms/datagrid/gettingstarted

## Namespace / Assembly
- Namespace: `Syncfusion.WinForms.DataGrid` (columns), `Syncfusion.WinForms.DataGrid.Enums` (enums), `Syncfusion.WinForms.DataGrid.Events` (event args)
- Assembly: `Syncfusion.SfDataGrid.WinForms` (already referenced in `pos.csproj`)

## PawaPos Pattern — explicit columns, not AutoGenerateColumns

Prefer declaring columns explicitly in the Designer (`AutoGenerateColumns = false`) over relying on autogeneration + runtime header/format lookup — it's more Designer-first and avoids guessing what column type autogeneration will infer for a given DataTable column.

```csharp
// grid-level (Designer)
dgvStockSales.AllowSorting = false;
dgvStockSales.AllowEditing = false;
dgvStockSales.AllowDeleting = false;
dgvStockSales.AllowFiltering = false;
dgvStockSales.AllowGrouping = false;
dgvStockSales.AllowDraggingColumns = false;
dgvStockSales.AutoGenerateColumns = false;
dgvStockSales.ShowRowHeader = false;               // equivalent of RowHeadersVisible = false
dgvStockSales.SelectionMode = Syncfusion.WinForms.DataGrid.Enums.GridSelectionMode.Single;
dgvStockSales.SelectionUnit = Syncfusion.WinForms.DataGrid.Enums.SelectionUnit.Row;

// columns
var colName = new Syncfusion.WinForms.DataGrid.GridTextColumn
{
    HeaderText = "Department Name",
    MappingName = "name",
    AutoSizeColumnsMode = Syncfusion.WinForms.DataGrid.Enums.AutoSizeColumnsMode.Fill, // the ONE fill column
};
var colSales = new Syncfusion.WinForms.DataGrid.GridNumericColumn
{
    HeaderText = "Total Sales",
    MappingName = "sales_value",
    Format = "N2",
    Width = 110,
};
colSales.CellStyle.HorizontalAlignment = System.Windows.Forms.HorizontalAlignment.Right; // numeric right-align hard rule
dgvStockSales.Columns.Add(colName);
dgvStockSales.Columns.Add(colSales);

dgvStockSales.DataSource = someDataTable; // binds directly, same as DataGridView
```

- Column types: `GridTextColumn` (strings/codes, left-aligned by default), `GridNumericColumn` (numbers — set `Format` + `CellStyle.HorizontalAlignment = Right`), also available: `GridDateTimeColumn`, `GridCheckBoxColumn`, `GridComboBoxColumn`, `GridButtonColumn`, `GridHyperlinkColumn`.
- Fill column: use grid LastColumnFill for a final free-text column, or column Fill elsewhere. Set MinimumWidth, not Width, on the fill column; other columns retain compact explicit widths.
- Row headers: `ShowRowHeader = false` is the `RowHeadersVisible = false` equivalent.
- Row/header height: `dgvStockSales.RowHeight` / `dgvStockSales.HeaderRowHeight` (both `int`).
- Selected row data: `dgvStockSales.SelectedItem` — for a `DataTable`-bound grid this is a `System.Data.DataRowView`, cast it the same way you would `DataGridView.SelectedRows[0].DataBoundItem`.
- Double-click: subscribe to `CellDoubleClick` (`Syncfusion.WinForms.DataGrid.Events.CellClickEventHandler`, args type `CellClickEventArgs` — has `.DataRow`/`.DataColumn`, but it's simpler to just read `grid.SelectedItem` in the handler like the pilot form does), not a plain `DoubleClick`.

## Shared styling

Use the verified PawaControls.ThemeManager.StyleSfDataGrid helper. [Grid/display consistency](grid-display-consistency.md) owns current selection, striping, conditional highlights, row headers and fill-column rules. Do not copy historical local palette code.

## Common Mistakes

**❌ Calling `ThemeManager.StyleDataGrid(dgvStockSales)`**
→ Compile error: `SfDataGrid` doesn't inherit `DataGridView`, the method's parameter type.

**✅ Style manually via `dgvStockSales.Style.*`, reusing `ThemeManager.BrandColors`/`UIColors` tokens (see above).**

---

**❌ Relying on `AutoGenerateColumns = true` and looking up columns by name after binding (the `DataGridView` pattern)**
→ Works, but you can't be certain what column type (`GridTextColumn` vs `GridNumericColumn`) gets inferred for a given .NET type, and it's not Designer-first.

**✅ Declare `GridColumn`s explicitly with `AutoGenerateColumns = false`** (see pattern above) — this also lets you delete any runtime `ConfigureColumns()`-style method entirely.
