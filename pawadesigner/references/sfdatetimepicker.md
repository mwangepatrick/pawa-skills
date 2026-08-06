---
name: pawadesigner-datetimepicker
description: DateTimePicker usage patterns for PawaPos—format, validation, Designer integration
---

# DateTimePicker (Standard .NET)

**Critical component for all date input in PawaPos.** Enforces `dd/MM/yyyy` format project-wide using standard .NET DateTimePicker.

## Official Docs
[Microsoft DateTimePicker Documentation](https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.datetimepicker)

## PawaPos Hard Rule

**All date pickers must:**
- Format: `dd/MM/yyyy` (short date, day-month-year via `CustomFormat` property)
- Designed in Visual Studio Designer (not dynamic code)
- Associated Label for accessibility (via tab order)
- Use ThemeManager.ApplyModernTheme(form) for consistent theming

## Designer Setup

**In Visual Studio Designer:**
1. Drag `DateTimePicker` from Toolbox onto form
2. Set properties in Designer:
   - **Name:** `_datePickerFrom` (use underscore prefix)
   - **Format:** Set to `Short`
   - **CustomFormat:** `dd/MM/yyyy`
   - **Size/Position:** Use Anchors for responsive layout
   - **Value:** (Optional) Leave default or set to DateTime.Today

**In Form Constructor (after InitializeComponent):**
```csharp
public MyForm : SfForm
{
    private DateTimePicker _datePickerFrom;
    
    public MyForm()
    {
        InitializeComponent();  // Designer-generated code
        
        // Ensure picker has valid value
        _datePickerFrom.Value = DateTime.Today;
        
        // Apply theme (colors/fonts/styling handled by ThemeManager)
        ThemeManager.ApplyModernTheme(this);
    }
}
```

**No need to set Format/CustomFormat in code** — Designer properties persist and are verified at runtime.

## Validation Patterns

### Client-Side Validation (Pre-Submit)

**Validate date value on button click:**
```csharp
private void SubmitButton_Click(object sender, EventArgs e)
{
    // Verify picker has a value
    if (_datePickerFrom.Value == null || _datePickerFrom.Value == DateTime.MinValue)
    {
        errorProvider.SetError(_datePickerFrom, "Please select a date");
        return;
    }
    
    // Check date is in valid range (example: not in future)
    if (_datePickerFrom.Value > DateTime.Today)
    {
        errorProvider.SetError(_datePickerFrom, "Date cannot be in the future");
        return;
    }
    
    // Date is valid; clear error
    errorProvider.SetError(_datePickerFrom, "");
    SaveForm();
}
```

### Async Server-Side Validation (Post-Submit)

**Validate date with database after user clicks save:**
```csharp
private async void SubmitButton_Click(object sender, EventArgs e)
{
    // Client-side check first
    if (_datePickerFrom.Value > DateTime.Today)
    {
        errorProvider.SetError(_datePickerFrom, "Date cannot be in the future");
        return;
    }
    
    // Convert to string for DB (always dd/MM/yyyy format)
    string dateString = _datePickerFrom.Value.ToString("dd/MM/yyyy");
    
    // Server-side validation (e.g., date in allowed business range)
    bool isValid = await ValidateDateRangeAsync(dateString);
    
    if (!isValid)
    {
        Shared.toast("Date is outside allowed business range (01/01/2025 - 31/12/2025)");
        return;
    }
    
    // Date is valid; save form
    SaveForm();
}
```

## Styling with ThemeManager

**ThemeManager handles DateTimePicker styling automatically** when you call `ThemeManager.ApplyModernTheme(this)` in the form constructor.

```csharp
public MyForm : SfForm
{
    private DateTimePicker _datePickerFrom;
    
    public MyForm()
    {
        InitializeComponent();
        
        // This single call styles all controls including DateTimePicker
        ThemeManager.ApplyModernTheme(this);
        
        // No additional styling needed for DateTimePicker
    }
}
```

**Never hand-code DateTimePicker colors or fonts** — ThemeManager applies brand colors at runtime.

## Accessibility

**In Designer, pair DateTimePicker with a Label:**
1. Drag `Label` before `DateTimePicker` in the form
2. Set Label text to field name (e.g., "From Date:")
3. Set `Label.Text = "From Date:"`
4. Set **Tab order** so Label (TabIndex=10) comes before DateTimePicker (TabIndex=11)

```csharp
// Designer sets these; you verify in constructor
_labelFromDate.Text = "From Date:";
_labelFromDate.TabIndex = 10;
_datePickerFrom.TabIndex = 11;
```

**Screen readers use tab order** to associate labels with inputs. Label MUST come before DateTimePicker in tab order for accessibility.

## Common Mistakes

**❌ Not setting CustomFormat in Designer**
```csharp
// In Designer, only set Format to "Short" but forget CustomFormat
picker.Format = DateTimePickerFormat.Short;  // Uses Windows locale (might be "d/M/yyyy")
```
→ Date format varies by machine; breaks in other locales; inconsistent with dd/MM/yyyy requirement

**✅ Set both in Designer:**
1. `Format = Short` (dropdown in Designer properties)
2. `CustomFormat = "dd/MM/yyyy"` (text field in Designer properties)

---

**❌ Using SfDateTimePicker instead of DateTimePicker**
```csharp
// ❌ WRONG
SfDateTimePicker picker = new SfDateTimePicker();
```
→ Not Designer-compatible; not in project pattern; no ThemeManager styling exists

**✅ Use standard DateTimePicker:**
```csharp
// ✅ CORRECT
// Drag DateTimePicker from Toolbox in Designer; it's the standard .NET control
```

---

**❌ Forgetting to initialize picker.Value**
```csharp
// Picker value is uninitialized; shows as blank or MinValue
_datePickerFrom.Value;  // Could be DateTime.MinValue
```
→ Picker appears empty; confuses users; may crash validation code

**✅ Set value in constructor:**
```csharp
public MyForm()
{
    InitializeComponent();
    _datePickerFrom.Value = DateTime.Today;  // Default to today
}
```

---

**❌ Mixing date formats in same form**
```csharp
_dateFrom.CustomFormat = "d/M/yyyy";      // Short
_dateTo.CustomFormat = "dd/MM/yyyy";      // Long
```
→ Inconsistent UX; confuses users; violates hard rule

**✅ Use same CustomFormat everywhere:**
```csharp
// In Designer, set CustomFormat = "dd/MM/yyyy" for ALL DateTimePickers
```

---

**❌ Displaying picker.Value.ToString() without format**
```csharp
lblDate.Text = _datePickerFrom.Value.ToString();  // Uses system locale; might be "m/d/yyyy"
```
→ Users in dd/mm/yyyy region see wrong format

**✅ Always use format string:**
```csharp
lblDate.Text = _datePickerFrom.Value.ToString("dd/MM/yyyy");  // Consistent format
```

---

**❌ Creating DateTimePicker in code instead of Designer**
```csharp
// ❌ WRONG — Dynamic control creation
var picker = new DateTimePicker() { Format = DateTimePickerFormat.Short };
this.Controls.Add(picker);
```
→ Hard to maintain; hard to visualize layout; violates Designer-first rule

**✅ Design in Visual Studio Designer:**
```
1. Open Form in Designer
2. Drag DateTimePicker from Toolbox
3. Set properties in Designer (Name, Format, CustomFormat)
4. Reference in constructor: this.InitializeComponent(); // Auto-generated
```

## Testing Checklist

**Before form ships:**

- [ ] **Designer properties set:**
  - [ ] Name: `_datePickerFromDate` (or similar, with underscore prefix)
  - [ ] Format: `Short` (dropdown)
  - [ ] CustomFormat: `dd/MM/yyyy` (text field)
  - [ ] Value: DateTime.Today (or appropriate default)

- [ ] **Runtime behavior:**
  - [ ] Picker displays value in `dd/MM/yyyy` format on form load
  - [ ] User can click picker, select date from calendar, and value updates
  - [ ] Format persists after user selection (still shows `dd/MM/yyyy`)

- [ ] **Validation:**
  - [ ] ErrorProvider shows error when date is invalid (outside range, future date, etc.)
  - [ ] Error message is specific and actionable ("Date must be before today" not "Invalid date")
  - [ ] Validation fires on button click (pre-submit), not while user is typing

- [ ] **Accessibility:**
  - [ ] Label exists before picker in tab order
  - [ ] Tab order: Label (TabIndex=N) → DateTimePicker (TabIndex=N+1) → next field
  - [ ] Screen reader can read label + understand it's associated with date input

- [ ] **Database integration:**
  - [ ] Value converts correctly to string for DB: `ToString("dd/MM/yyyy")`
  - [ ] Blank/null dates handled gracefully (validation prevents submission)
  - [ ] Date range queries use correct format

- [ ] **Theming:**
  - [ ] `ThemeManager.ApplyModernTheme(this)` called in constructor
  - [ ] Picker inherits theme colors (background, text, borders)
  - [ ] No hand-coded colors or fonts in picker code

## Real-World Example

**PlPaymentStatus.cs (reference form):**
- Lines 12–13: DateTimePicker controls (`_from`, `_to`)
- Lines 75–76: Default values set (today and 1 month ago)
- Line 33: ThemeManager.ApplyModernTheme(this) applies styling
- Lines 62–63: Pickers added to filter FlowLayoutPanel with labels

Study this form as your template.

## PawaPos References

- Main skill: [[pawadesigner]]
- Example form: PlPaymentStatus.cs (D:\cp\pp\pawapos-bo\purchase_ledger\enquiries\)
- Theme integration: ThemeManager.cs (D:\cp\pp\pawapos-shared\ThemeManager.cs)
