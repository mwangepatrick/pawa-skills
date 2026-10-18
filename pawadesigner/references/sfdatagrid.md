---
name: pawadesigner-sfdatagrid
description: SfDataGrid usage patterns for the Syncfusion-pilot form pattern in PawaPos
metadata:
  type: reference
---

# SfDataGrid

**Status: pilot only.** The default PawaPos grid control is still `DataGridView` (see main SKILL.md Grid Column Configuration section). `SfDataGrid` was adopted for one form — `DepartmentalStockSales.cs` — as a scoped experiment. `SfDataGrid` does **not** inherit `DataGridView` (base is `Syncfusion.Windows.Forms.Core.BaseControl`), so `ThemeManager.StyleDataGrid(DataGridView)` will not accept it — style it manually (see below) or add a new `ThemeManager.StyleSfDataGrid()` overload if this becomes the project default (would require adding a `Syncfusion.SfDataGrid.WinForms` reference to `PawaShared.csproj`, which it doesn't have today).

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
- Fill column: set `AutoSizeColumnsMode = AutoSizeColumnsMode.Fill` on exactly one column (same free-text-column rule as `DataGridView.AutoSizeMode = Fill`) — every other column keeps an explicit `Width`.
- Row headers: `ShowRowHeader = false` is the `RowHeadersVisible = false` equivalent.
- Row/header height: `dgvStockSales.RowHeight` / `dgvStockSales.HeaderRowHeight` (both `int`).
- Selected row data: `dgvStockSales.SelectedItem` — for a `DataTable`-bound grid this is a `System.Data.DataRowView`, cast it the same way you would `DataGridView.SelectedRows[0].DataBoundItem`.
- Double-click: subscribe to `CellDoubleClick` (`Syncfusion.WinForms.DataGrid.Events.CellClickEventHandler`, args type `CellClickEventArgs` — has `.DataRow`/`.DataColumn`, but it's simpler to just read `grid.SelectedItem` in the handler like the pilot form does), not a plain `DoubleClick`.

## Manual styling (ThemeManager has no SfDataGrid support yet)

Reuse `ThemeManager`'s existing color tokens rather than inventing new literals:

```csharp
dgvStockSales.Style.HeaderStyle.BackColor = ThemeManager.BrandColors.GridHeaderBackground;
dgvStockSales.Style.HeaderStyle.TextColor = System.Drawing.Color.White;
dgvStockSales.Style.HeaderStyle.Font.Bold = true;
dgvStockSales.Style.HeaderStyle.HorizontalAlignment = System.Windows.Forms.HorizontalAlignment.Center;
dgvStockSales.Style.SelectionStyle.BackColor = ThemeManager.UIColors.SelectionBackground;
dgvStockSales.Style.SelectionStyle.TextColor = ThemeManager.UIColors.SelectionForeground;
dgvStockSales.Style.BorderColor = ThemeManager.UIColors.BorderLight;
```

`dgvStockSales.Style` is a `DataGridStyle` sub-object (mutate its properties directly, same pattern as `GridColumn.CellStyle`/`HeaderStyle`) — don't try to assign a new `Style` object.

## Common Mistakes

**❌ Calling `ThemeManager.StyleDataGrid(dgvStockSales)`**
→ Compile error: `SfDataGrid` doesn't inherit `DataGridView`, the method's parameter type.

**✅ Style manually via `dgvStockSales.Style.*`, reusing `ThemeManager.BrandColors`/`UIColors` tokens (see above).**

---

**❌ Relying on `AutoGenerateColumns = true` and looking up columns by name after binding (the `DataGridView` pattern)**
→ Works, but you can't be certain what column type (`GridTextColumn` vs `GridNumericColumn`) gets inferred for a given .NET type, and it's not Designer-first.

**✅ Declare `GridColumn`s explicitly with `AutoGenerateColumns = false`** (see pattern above) — this also lets you delete any runtime `ConfigureColumns()`-style method entirely.
