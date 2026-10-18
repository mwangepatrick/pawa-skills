---
name: pawadesigner-sfnumerictextbox
description: SfNumericTextBox usage patterns for the Syncfusion-pilot form pattern in PawaPos
metadata:
  type: reference
---

# SfNumericTextBox

**Status: pilot only**, used for the disabled numeric summary fields on `DepartmentalStockSales.cs`. The default PawaPos numeric field is still a plain `TextBox` with `TextAlign = Right` — see main SKILL.md's numeric-field hard rule.

## Official Docs
https://help.syncfusion.com/windowsforms/numeric-textbox/gettingstarted

## Namespace / Assembly
- Namespace: `Syncfusion.WinForms.Input`
- Assembly: `Syncfusion.SfInput.WinForms` (already referenced in `pos.csproj`)

## The one fact that matters most: it IS a TextBox

`SfNumericTextBox : System.Windows.Forms.TextBox` — unlike every other Sf* control on the pilot form, this one **inherits the plain TextBox**. Practical consequences:

- `ThemeManager.ApplyModernTheme(form)` already styles it automatically — its `ApplyControlTheme` does `control is TextBox txt` and sets `BackColor`/`ForeColor`/`Font`/`BorderStyle`. No extra styling code needed, unlike `SfButton`/`SfDataGrid`/`SfComboBox`.
- The numeric-field hard rule (`TextAlign = HorizontalAlignment.Right`) and the disabled-field pattern (`Enabled = false`) both work exactly as they would on a plain `TextBox` — same properties, same behavior.
- Setting `.Text` directly (e.g. `txtSummarySales.Text = value.ToString("N2")`) works fine, same as a plain TextBox, without touching the `Value`/`FormatMode` machinery at all.

## PawaPos Pattern

```csharp
// Designer — identical to a plain disabled numeric TextBox:
txtSummarySales.Enabled = false;
txtSummarySales.TabStop = false;
txtSummarySales.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
txtSummarySales.Size = new System.Drawing.Size(105, 22);

// code-behind — plain string assignment, no Value/FormatMode needed for a read-only display field:
txtSummarySales.Text = totalSales.ToString("N2");
```

If a field needs actual numeric *input* (not just read-only display), use `Value` (`double?`) and `MinValue`/`MaxValue`/`FormatMode` instead of `Text` — not needed for the pilot form's disabled summary fields.

## Common Mistakes

**❌ Assuming it needs the same manual styling as `SfButton`/`SfDataGrid`/`SfComboBox`**
→ It doesn't — it's a `TextBox` subclass, so `ApplyModernTheme` already covers it for free.
