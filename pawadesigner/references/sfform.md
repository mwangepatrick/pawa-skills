---
name: pawadesigner-sfform
description: SfForm base class usage for the Syncfusion-pilot form pattern in PawaPos
metadata:
  type: reference
---

# SfForm

**Status: pilot only.** The default PawaPos form base class is still plain `Form` (see main SKILL.md hard rules). `SfForm` was adopted for one form — `DepartmentalStockSales.cs` (D:\cp\pp\pawapos-bo\pos_ledger\) — as an explicit, scoped experiment. Don't switch other forms to `SfForm` without the same explicit decision; if it becomes the project default, update the main SKILL.md hard rule, not just this file.

## Official Docs
https://help.syncfusion.com/windowsforms/sfform/getting-started

## Namespace / Assembly
- Namespace: `Syncfusion.WinForms.Controls`
- Assemblies: `Syncfusion.Core.WinForms`, `Syncfusion.Shared.Base` (both already referenced in `pos.csproj`; `Syncfusion.Shared.Base` is **not** referenced in `PawaShared.csproj` — add it there first if `SfForm` is ever used in a pawapos-shared form)

## PawaPos Pattern

```csharp
using Syncfusion.WinForms.Controls;

public partial class MyForm : SfForm
{
    public MyForm()
    {
        InitializeComponent();
        Icon = System.Drawing.Icon.ExtractAssociatedIcon(Application.ExecutablePath);
        ThemeManager.ApplyModernTheme(this);  // still applies — SfForm : Form
    }
}
```

`SfForm` inherits directly from `System.Windows.Forms.Form`, so `FormBorderStyle`, `ClientSize`, `MinimumSize`, `StartPosition`, `Icon`, and `ThemeManager.ApplyModernTheme(this)` all work unchanged — it's a drop-in base class swap.

## Verified facts (checked via assembly reflection + docs, 2026-08-11)
- No `SfSkinManager` is used anywhere in this codebase, so `SfForm` renders with its default (native-ish) chrome, not a custom skinned title bar — visually close to a plain `Form`.
- `SfForm.Style` (type `FormVisualStyle`) exposes title-bar colors/border styling if a custom look is ever wanted — left untouched on the pilot form.
- Constructor is parameterless, same as `Form`.

## Common Mistakes

**❌ Assuming ThemeManager auto-styles SfForm-specific chrome**
→ `ApplyModernTheme` only sets `BackColor`/`ForeColor`/`Font`/Escape-to-close on the form itself and recurses into child controls by type-check (`is Button`, `is TextBox`, etc.) — it has no `SfForm`-specific branch, but doesn't need one since `SfForm` picks up the base `Form` properties fine.

**✅ No extra work needed** beyond the normal `ApplyModernTheme(this)` call.
