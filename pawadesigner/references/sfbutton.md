---
name: pawadesigner-sfbutton
description: SfButton usage patterns for the Syncfusion-pilot form pattern in PawaPos
metadata:
  type: reference
---

# SfButton

**Status: not just a pilot** — `Syncfusion.WinForms.Controls.SfButton` was already in real use before the `DepartmentalStockSales` pilot, in `DiaPackingMaster.Designer.cs` and `CustomerPerfomance.Designer.cs`. The default PawaPos button is still a plain `Button` styled via `ThemeManager.StylePrimaryButton`/`StyleSecondaryButton` — see main SKILL.md.

## Official Docs
https://help.syncfusion.com/windowsforms/button/getting-started

## Namespace / Assembly
- Namespace: `Syncfusion.WinForms.Controls`
- Assembly: `Syncfusion.Core.WinForms` (already referenced in `pos.csproj`)

## It IS a Button, but rendering needs `.Style` too

`SfButton : System.Windows.Forms.Button` — so `ThemeManager.StylePrimaryButton(SfButton)`/`StyleSecondaryButton(SfButton)` compile and run fine (they take a `Button` parameter), setting the base `BackColor`/`ForeColor`/`Font`/`FlatStyle`/`Height`. **But** `SfButton` paints itself from its own `Style` sub-object (`Style.BackColor`, `Style.ForeColor`, ...), not directly from the base `Button.BackColor` — every existing local usage (`DiaPackingMaster.Designer.cs`) sets both together. Skipping `.Style.*` risks the button rendering with default/unstyled colors even after `ThemeManager.StylePrimaryButton()` runs.

`ThemeManager.cs` (in `pawapos-shared`) has no `SfButton`-aware branch today (adding one requires a `Syncfusion.Core.WinForms` reference in `PawaShared.csproj`, which it doesn't have) — until/unless that's added, set `.Style.BackColor`/`.Style.ForeColor` manually in the form, reusing `ThemeManager.BrandColors.*`/`UIColors.*` tokens rather than inventing new color literals:

```csharp
ThemeManager.StylePrimaryButton(btnRefresh);  // base Button styling — Font, Height, FlatStyle, etc.
btnRefresh.Style.BackColor = ThemeManager.BrandColors.Orange;
btnRefresh.Style.ForeColor = System.Drawing.Color.White;
```

## Common Mistakes

**❌ Calling only `ThemeManager.StylePrimaryButton(sfButton)` and expecting the orange fill to show**
→ May render unstyled — `SfButton`'s custom paint logic reads `.Style.BackColor`, not the base `Button.BackColor`, in at least some render states.

**✅ Always pair `ThemeManager.StylePrimaryButton()`/`StyleSecondaryButton()` with an explicit `.Style.BackColor`/`.Style.ForeColor` set, reusing `ThemeManager` color tokens.**
