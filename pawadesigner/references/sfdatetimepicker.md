---
name: pawadesigner-sfdatetimepicker
description: SfDateTimePicker usage patterns for PawaPos—format, validation, theming
---

# SfDateTimePicker

**Critical component for all date input in PawaPos.** Enforces `dd/MM/yyyy` format project-wide.

## Official Docs
[Syncfusion SfDateTimePicker Getting Started](https://help.syncfusion.com/windowsforms/datetimepicker/getting-started)

## PawaPos Hard Rule

**All date pickers must:**
- Format: `dd/MM/yyyy` (short date, day-month-year)
- Verify picker loads and displays correctly on form init
- Use ThemeManager for styling
- Have associated SfLabel for accessibility

## Basic Usage

```csharp
// In Designer or form constructor
SfDateTimePicker picker = new SfDateTimePicker();
picker.Format = "dd/MM/yyyy";
picker.CustomFormat = "dd/MM/yyyy";
picker.Dock = DockStyle.Top;
picker.Margin = new Padding(5);

// Ensure picker has valid initial value
if (picker.Value == DateTime.MinValue)
    picker.Value = DateTime.Today;

this.Controls.Add(picker);
```

## Validation Patterns

### Format Validation (TextChanged)
```csharp
private void picker_ValueChanged(object sender, EventArgs e)
{
    // SfDateTimePicker handles format internally
    // No additional validation needed if CustomFormat is set
    // Verify Value is not MinValue after user interaction
    
    if (picker.Value == DateTime.MinValue)
    {
        errorProvider.SetError(picker, "Please select a date");
    }
    else
    {
        errorProvider.SetError(picker, "");
    }
}
```

### Async Server-Side Validation (Post-Submit)
```csharp
private async void ApplyButton_Click(object sender, EventArgs e)
{
    // Picker value is DateTime; convert to string for DB
    string dateString = picker.Value.ToString("dd/MM/yyyy");
    
    // Validate on server (e.g., date in allowed range)
    bool isValid = await ValidateDateAsync(dateString);
    
    if (!isValid)
    {
        Shared.toast("Date is outside allowed range");
        return;
    }
    
    // Save...
}
```

## Styling with ThemeManager

```csharp
// In form constructor after InitializeComponent()
ThemeManager.ApplyModernTheme(this);
ThemeManager.StyleSfDateTimePicker(picker);  // Apply theme colors, fonts, borders
```

## Accessibility

**Always pair with SfLabel:**

```csharp
SfLabel lblDate = new SfLabel();
lblDate.Text = "Invoice Date:";
lblDate.AssociatedControl = picker;  // Links label to picker for screen readers

this.Controls.Add(lblDate);
this.Controls.Add(picker);
```

**Tab order:** Set `TabIndex` so picker follows its label:
```csharp
lblDate.TabIndex = 10;
picker.TabIndex = 11;
```

## Common Mistakes

**❌ Not setting CustomFormat**
```csharp
picker.Format = "d";  // Relies on Windows locale
```
→ Date format varies by machine; breaks in other locales

**✅ Always set CustomFormat explicitly**
```csharp
picker.CustomFormat = "dd/MM/yyyy";
picker.Format = "dd/MM/yyyy";
```

---

**❌ Picker.Value == null without checking**
```csharp
DateTime date = picker.Value;  // Could be MinValue; not null-safe
```
→ Crashes if Value is uninitialized; sends MinValue to DB

**✅ Validate before using**
```csharp
if (picker.Value != DateTime.MinValue && picker.Value >= DateTime.Today)
{
    // Safe to use picker.Value
}
```

---

**❌ Displaying picker.Value.ToString() directly in UI**
```csharp
lblDate.Text = picker.Value.ToString();  // Uses system locale; might be en-US
```
→ Users in dd/mm/yyyy region see wrong format

**✅ Use formatted string**
```csharp
lblDate.Text = picker.Value.ToString("dd/MM/yyyy");  // Always consistent
```

---

**❌ Forgetting to initialize picker.Value on form load**
```csharp
SfDateTimePicker picker = new SfDateTimePicker();
// picker.Value is DateTime.MinValue; shows as blank
```
→ Picker appears empty; confuses users

**✅ Set a default value**
```csharp
picker.Value = DateTime.Today;  // Default to today
// Or: picker.Value = DateTime.Parse("01/01/2025", new System.Globalization.CultureInfo("en-GB"));
```

---

**❌ Mixing date formats in same form**
```csharp
picker1.Format = "d";    // System locale
picker2.Format = "dd/MM/yyyy";  // Manual format
```
→ Inconsistent UX; confuses users

**✅ Use same CustomFormat everywhere**
```csharp
picker1.CustomFormat = "dd/MM/yyyy";
picker2.CustomFormat = "dd/MM/yyyy";
```

## Testing Checklist

- [ ] Picker displays value in `dd/MM/yyyy` format on load
- [ ] User can select date from calendar; format persists
- [ ] Validation fires if date is invalid (before today, outside range, etc.)
- [ ] Error message displays with ErrorProvider
- [ ] Label associated with picker (accessibility)
- [ ] Tab order correct (label → picker → next field)
- [ ] Value converts correctly to string for DB (`ToString("dd/MM/yyyy")`)
- [ ] Picker has ThemeManager styling applied

## PawaPos References

- Main skill: [[pawadesigner]]
- Related: [[pawadesigner-sftextbox]] (for numeric validation patterns)
- Theme integration: ThemeManager.cs (D:\cp\pp\pawapos-shared\ThemeManager.cs)
