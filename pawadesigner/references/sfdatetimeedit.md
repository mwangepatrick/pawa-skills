---
name: pawadesigner-sfdatetimeedit
description: SfDateTimeEdit usage patterns for the Syncfusion-pilot form pattern in PawaPos — the Syncfusion counterpart to references/sfdatetimepicker.md
metadata:
  type: reference
---

# SfDateTimeEdit

**Status: pilot only.** The default PawaPos date input is still the standard .NET `DateTimePicker` — see `[[pawadesigner-datetimepicker]]` (references/sfdatetimepicker.md) for that convention, which still applies everywhere except the pilot form. `SfDateTimeEdit` was adopted for one form — `DepartmentalStockSales.cs`.

There is no Syncfusion WinForms control literally named "SfDateTimePicker" — the real control class is `SfDateTimeEdit`. If you see `SfDateTimePicker` referenced anywhere (including older text in this skill's main SKILL.md "Never use" list), read it as `SfDateTimeEdit`.

## Official Docs
https://help.syncfusion.com/windowsforms/datetimepicker/getting-started
https://help.syncfusion.com/windowsforms/sfdatetimeedit/datetimedisplaypattern (custom format pattern)

## Namespace / Assembly
- Namespace: `Syncfusion.WinForms.Input` (control), `Syncfusion.WinForms.Input.Enums` (`DateTimePattern`), `Syncfusion.WinForms.Input.Events` (`DateTimeValueChangedEventHandler`/`EventArgs`)
- Assembly: `Syncfusion.SfInput.WinForms` (already referenced in `pos.csproj`)

## PawaPos Pattern — same `dd/MM/yyyy` hard rule, different property names

```csharp
using Syncfusion.WinForms.Input;

// Designer:
dtpFrom.DateTimePattern = Syncfusion.WinForms.Input.Enums.DateTimePattern.Custom; // required before Format takes effect
dtpFrom.Format = "dd/MM/yyyy";                                                    // the actual hard-rule format string
dtpFrom.AllowNull = false;                                                        // keeps parity with DateTimePicker, which is never null
dtpFrom.ValueChanged += new Syncfusion.WinForms.Input.Events.DateTimeValueChangedEventHandler(this.DateFilterChanged);

// handler signature — NOT plain EventHandler:
private void DateFilterChanged(object sender, Syncfusion.WinForms.Input.Events.DateTimeValueChangedEventArgs e) { ... }
```

`Value` is `DateTime?` (nullable), unlike `DateTimePicker.Value` which is non-nullable `DateTime`. Read it with `.GetValueOrDefault()` (or check `AllowNull`/null explicitly):

```csharp
var fromDate = dtpFrom.Value.GetValueOrDefault().Date;
```

Setting `dtpFrom.Value = new DateTime(...)` still works fine (implicit conversion to `DateTime?`).

## Common Mistakes

**❌ Setting only `Format = "dd/MM/yyyy"` without `DateTimePattern = Custom`**
→ The custom `Format` string is ignored unless `DateTimePattern` is explicitly `Custom` first; other `DateTimePattern` values (`ShortDate`, `LongDate`, etc.) use their own built-in pattern instead.

**❌ Reading `dtpFrom.Value.Date` directly**
→ Compile error — `Value` is `Nullable<DateTime>`, there's no `.Date` on the nullable itself.

**✅ Use `dtpFrom.Value.GetValueOrDefault().Date`.**

**❌ Wiring `ValueChanged` as a plain `EventHandler`**
→ Compile error — the delegate type is `DateTimeValueChangedEventHandler(object, DateTimeValueChangedEventArgs)`, not `System.EventHandler`.
