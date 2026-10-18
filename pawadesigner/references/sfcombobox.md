---
name: pawadesigner-sfcombobox
description: SfComboBox usage patterns for the Syncfusion-pilot form pattern in PawaPos
metadata:
  type: reference
---

# SfComboBox

**Status: this one is not just a pilot** — `Syncfusion.WinForms.ListView.SfComboBox` was already in real use before the `DepartmentalStockSales` pilot, in `D:\cp\pp\pawapos-bo\inventory\dialogs\DiaPackingMaster.cs` (`cmb_packing`), with shared helpers already written for it in `PawaUtils.Ctrls` (D:\cp\pp\PawaUtils\Ctrls.cs). Prefer reusing `Ctrls`, don't hand-roll new fill/read logic.

## Official Docs
https://help.syncfusion.com/windowsforms/combobox/gettingstarted

## Namespace / Assembly
- Namespace: `Syncfusion.WinForms.ListView` (control), `Syncfusion.WinForms.ListView.Enums` (DropDownStyle, ComboBoxMode)
- Assembly: `Syncfusion.SfListView.WinForms` (already referenced in `pos.csproj`)

## PawaPos Pattern — use `PawaUtils.Ctrls`, not raw `DataSource` juggling

```csharp
using PawaUtils; // Ctrls

// Designer:
cmbCategory.DropDownStyle = Syncfusion.WinForms.ListView.Enums.DropDownStyle.DropDownList; // read-only, fully qualify — collides with the DropDownStyle *property* name
cmbCategory.SelectedValueChanged += new System.EventHandler(this.cmbCategory_SelectedIndexChanged); // plain EventHandler

// Populate (fetch a DataTable exactly like you would for Db.FillcomboX, then hand it to Ctrls):
var data = Db.getdata("select code,name from category order by code");
Ctrls.FillComboBoxSf(cmbCategory, data, "code", "name", showAll: true, defaultNull: "");
cmbCategory.SelectedIndex = 0;

// Read selected value (mirrors Shared.GetComboXVal for ComboBoxEx):
var code = cmbCategory.SelectedIndex <= 0 ? null : Ctrls.GetSfComboVal(cmbCategory);

// Set selected value programmatically:
Ctrls.SetSfComboVal(cmbCategory, code);
```

`Ctrls.FillComboBoxSf` builds `DataSource` from anonymous `{ Id, Name }` objects and sets `DisplayMember = "Name"` / `ValueMember = "Id"` internally — `Ctrls.GetSfComboVal`/`SetSfComboVal` read/write via that same `Id` property through reflection. Don't bind `DataSource` directly to a `DataTable` unless you also change these helpers.

## Key properties
`SelectedIndex`, `SelectedItem`, `SelectedValue`, `DataSource`, `DisplayMember`, `ValueMember`, `Enabled`, `Font`, `BackColor`/`ForeColor`, `Style` (type `ComboBoxVisualStyle` — e.g. `Style.TokenStyle.CloseButtonBackColor` used in `DiaPackingMaster.Designer.cs`).

## Common Mistakes

**❌ `using Syncfusion.WinForms.ListView.Enums;` then writing bare `DropDownStyle.DropDownList`**
→ Ambiguous/confusing next to the control's own `DropDownStyle` *property* of the same name. The existing codebase always fully qualifies: `Syncfusion.WinForms.ListView.Enums.DropDownStyle.DropDownList`. Match that.

**❌ Reimplementing combo-fill/read logic per form**
→ `PawaUtils.Ctrls` already has `FillComboBoxSf` / `GetSfComboVal` / `SetSfComboVal`; duplicating this logic drifts from the established pattern.

**✅ Always route through `Ctrls` for `SfComboBox` — same as `ComboBoxEx` routes through `Db.FillcomboX` / `Shared.GetComboXVal`.**
