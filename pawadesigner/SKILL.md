---
name: pawadesigner
description: Use when designing forms for PawaPos project—before choosing components, layout, or validation patterns
---

# PawaDesigner

## Overview

Form design for PawaPos uses **Syncfusion components exclusively**, leverages **ThemeManager.cs** for all styling and reusable functions, and follows strict format/sizing rules. Design focuses on assessing complexity early to choose the right model, and systematically validating assumptions before implementation.

This skill provides a decision framework for component selection, a complexity rubric for model choice, validation patterns, and mandatory compliance rules.

## Hard Rules (Non-Negotiable)

**These rules are absolute. No exceptions.**

- ✋ **NEVER use DevComponents** (DotNetBar, etc.) — Syncfusion only
- ✋ **NEVER leave forms in Sizeable mode** — Update form's FormBorderStyle to Fixed or FixedToolWindow
- ✋ **Date pickers** — Always format as `dd/MM/yyyy` short date; verify picker loads on init
- ✋ **Styling & reusable functions** → **Always use ThemeManager.cs** (D:\cp\pp\pawapos-shared\ThemeManager.cs)
- ✋ **Self-learning** — When skill receives new constraints via prompt, update skill for future applications

## When to Use

**Use this skill before:**
- Designing any new form (login, data entry, configuration, dialogs)
- Deciding between DotNetBar and Syncfusion components
- Scoping validation and error handling
- Planning accessibility or multi-language support

**Do NOT use for:**
- Tweaking existing forms (style changes, minor refactors)
- Choosing colors or fonts (use pawa-ui-authoring skill for branding)
- Fixing bugs in deployed forms (use systematic-debugging skill first)

## Phase 1: Anchor to ThemeManager & Syncfusion Patterns

**Always start here.** All styling and reusable functions live in ThemeManager.cs.

**Step 1: Review ThemeManager.cs**
```
Location: D:\cp\pp\pawapos-shared\ThemeManager.cs
Purpose: Central repository for all form styling, colors, fonts, and reusable UI functions
Always: Check what's available before creating custom styles
```

**Step 2: Use Semble MCP to find Syncfusion form patterns**
```
Search for existing Syncfusion form implementations:
- "sfForm" OR "SfTextBox" OR "SfComboBox" OR "SfGrid" files
- Look at: Syncfusion component usage, validation patterns, error handling, date format usage
- Document: Component patterns, error presentation style (toast vs MessageBox), validation timing
```

**What to capture from existing Syncfusion forms:**

| Pattern | Example | Why | Reference |
|---------|---------|-----|-----------|
| Form base class | sfForm or inherited from SfForm | Consistency with Syncfusion standards | Recent forms using Syncfusion |
| Input controls | SfTextBox, SfComboBox, SfDateTimePicker | All Syncfusion (NO DevComponents) | Recent forms |
| Error presentation | `Shared.toast()` style, ErrorProvider usage | Defines error UX | Existing Syncfusion form |
| Validation timing | Real-time vs pre-submit vs post-submit | Affects responsiveness | Existing form |
| Date format | dd/MM/yyyy | REQUIRED standard format | ThemeManager or DateTimeFormat constant |
| Label strategy | Hardcoded strings vs localization | Impacts i18n scope | Check for `Shared.GetMessage()` usage |
| Form sizing | FormBorderStyle (Fixed, FixedToolWindow) | NO Sizeable mode by default | Recent forms |

**Document assumptions** from existing patterns:
- Single-factor or multi-factor auth?
- Employee-only or multi-tenant?
- Offline support required?
- Async login or blocking UI?

## Phase 2: Assess Complexity → Select Model

**Before designing, estimate complexity.** This determines whether you need Haiku (simple forms) or Opus (complex multi-step flows).

### Complexity Rubric

| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Fields** | <5 inputs (login form) | 5-15 fields (item master) | 15+ fields (bulk operations) |
| **Validation rules** | Email/required only | Email + domain logic + cross-field | Multi-stage, async validation |
| **Error states** | Generic messages | Field-level + form-level errors | Progressive disclosure, context-aware hints |
| **Async work** | None (all sync) | Single async call (DB lookup) | Multiple async calls, cancellation, timeout handling |
| **Edge cases** | Few (happy path dominant) | Some (empty state, loading state, retry logic) | Many (race conditions, network errors, permission changes mid-form) |
| **Component custom code** | Standard controls only | Custom validation, formatters | Custom components, event handling |
| **Accessibility scope** | Basic (tab order, labels) | WCAG 2.1 AA compliance needed | WCAG AAA, multiple input methods, screen reader testing |
| **Localization** | English only | 2-3 languages (label changes) | RTL support, cultural date/number formats |

**Score each factor (1–3), sum them:**
- **7–12 (Low complexity):** Use **Haiku** — forms with standard validation, minimal async work, existing component patterns
- **13–18 (Medium complexity):** Use **Sonnet** — new component combinations, async validation, multi-step flows
- **19+ (High complexity):** Use **Opus** — multi-async, edge cases, custom components, or significant unknown unknowns

**Example: Login form**
- Fields: 2 (username + password) = 1
- Validation: required + domain check = 1
- Errors: generic toast = 1
- Async: single DB call = 1
- Edge cases: few = 1
- Custom code: none = 1
- Accessibility: basic = 1
- Localization: English only = 1
- **Total: 8 → Use Haiku**

**Example: Item master with SKU lookup + pricing**
- Fields: 12 = 2
- Validation: required + SKU exists + price > 0 + margin constraints = 3
- Errors: field-level + SKU lookup feedback = 2
- Async: SKU lookup, price calculation = 2
- Edge cases: duplicate SKU, price validation rules = 2
- Custom code: SKU formatter, price calculator = 2
- Accessibility: full WCAG AA = 2
- Localization: 3 languages = 2
- **Total: 17 → Use Sonnet**

## Phase 3: Component Selection

**All components are Syncfusion. This is non-negotiable.**

### Syncfusion Component Reference

| Need | Component | Documentation | Notes |
|------|-----------|-----------------|-------|
| Form base | sfForm or inherit SfForm | (in progress) | Always use Syncfusion form base |
| Text input | SfTextBox | (in progress) | Single-line text, numbers, formatted input |
| Multiline text | SfTextBox with multiline | (in progress) | Larger textarea-style input |
| Dropdown/combo | SfComboBox | (in progress) | With search, filtering, remote data source |
| Date picker | SfDateTimePicker | [[pawadesigner-sfdatetimepicker]] | Format: `dd/MM/yyyy`; **CRITICAL: verify picker loads on init** |
| Data grid | SfDataGrid | (in progress) | Sortable, filterable, multi-select rows |
| Button | SfButton | (in progress) | Styled, primary/secondary variants via ThemeManager |
| Checkbox/radio | SfCheckBox, SfRadioButton | (in progress) | Standard form selections |
| Tabs | SfTabControl | (in progress) | Multi-step forms or grouped sections |
| Label | SfLabel | (in progress) | Linked to input controls for accessibility |

**When unsure about a component:**
1. Check [Syncfusion WindowsForms official docs](https://help.syncfusion.com/windowsforms/form/getting-started)
2. Learn the official API and patterns
3. Create/update a component sub-reference (see sub-references/ folder)
4. Link it in the table above

This builds local documentation as the project grows.

### Styling Pattern

**All colors, fonts, spacing → ThemeManager.cs**

**DO NOT:**
- ❌ Create custom color constants in form code
- ❌ Hard-code font names or sizes
- ❌ Invent new button styles

**DO:**
- ✅ Call `ThemeManager.ApplyStyle(control)` or equivalent
- ✅ Use `ThemeManager.GetColor("primary")` for dynamic colors
- ✅ Leverage ThemeManager's reusable functions for button styling, spacing, fonts

**Red flag:** If you're hand-coding colors or fonts, you should be calling ThemeManager instead.

## Phase 4: Validation & Error State Pattern

**Build a validation matrix before writing code.**

### Error State Taxonomy

| State | Trigger | Message | UI | Recoverable |
|-------|---------|---------|-----|-------------|
| **Empty field** | User leaves field empty on blur | "Field name is required" | ErrorProvider + red border + icon | Yes (user fills field) |
| **Invalid format** | User enters "abc" in email field | "Enter a valid email (name@domain.com)" | ErrorProvider + hint | Yes (user corrects) |
| **Async validation fail** | SKU lookup returns 0 rows | "SKU not found. Check inventory." | Field-level error + info icon | Yes (user corrects SKU) |
| **Cross-field constraint** | Start date > end date | "End date must be after start date" | Form-level message + both fields highlighted | Yes (user reorders) |
| **Server-side reject** | DB insert fails (duplicate key) | "This item already exists. Duplicate item codes are not allowed." | Toast + form disabled until corrected | Yes (form stays open for retry) |
| **Permission deny** | User lacks role for operation | "You don't have permission to add items. Contact admin." | Toast or MessageBox (user can't fix) | No (close form) |
| **Network timeout** | Server doesn't respond in 5s | "Connection timeout. Check your network and try again." | Toast + retry button | Yes (user retries) |

**Rule: Generic errors for security, specific errors for usability.**
- Bad password → "Wrong username or password" (don't reveal which field)
- SKU not found → "SKU XYZ not found. Check inventory or create new item" (specific, actionable)

### Validation Timing Strategy

| Timing | When | Example | Pro | Con |
|--------|------|---------|-----|-----|
| **Real-time (TextChanged)** | As user types | Char-by-char validation (max length, allowed chars) | Immediate feedback | Can feel "judgy"; disable for expensive checks |
| **On blur (field exit)** | User leaves field | Email format, SKU existence check | Good UX; catches mistakes before form submit | Slightly delayed feedback |
| **On submit (button click)** | User clicks save | All fields validated; cross-field checks | One pass catches all errors | User might submit incomplete form |
| **Async post-submit** | After server acknowledges | Duplicate key check, business rule violations | Server is source of truth | Requires error recovery (retry, rollback) |

## Phase 5: Design Checklist Before Implementation

**Before writing a single line of code, answer these:**

- [ ] **Scope:** How many fields? Estimated validation complexity? (Use rubric above)
- [ ] **Model choice:** Complexity score = ___ → Using **Haiku / Sonnet / Opus**
- [ ] **Component toolkit:** Verified all components are Syncfusion (sfForm, SfTextBox, SfComboBox, etc.)?
- [ ] **ThemeManager:** Reviewed ThemeManager.cs? Planning to use for all styling/colors/fonts?
- [ ] **Date pickers:** All date input fields use SfDateTimePicker with format `dd/MM/yyyy`? Verified picker loads?
- [ ] **Form sizing:** Form.FormBorderStyle set to Fixed or FixedToolWindow (NOT Sizeable)?
- [ ] **Existing patterns:** Researched ≥3 existing Syncfusion forms? Documented pattern (error style, validation timing)?
- [ ] **Error taxonomy:** Built error state matrix? Identified server-side vs client-side checks?
- [ ] **Validation timing:** Real-time for fields? Pre-submit for all? Async for expensive checks?
- [ ] **Accessibility:** Tab order mapped? Labels linked to inputs? Keyboard shortcuts documented?
- [ ] **Localization:** Hard-coded strings? Or using `Shared.GetMessage()`?
- [ ] **Security assumptions:** Single-factor or multi-factor? Employee-only? Offline support?
- [ ] **Testing plan:** How will I test validation? Edge cases identified?
- [ ] **No DevComponents:** Verified form uses ONLY Syncfusion (no DotNetBar, no DevComponents)?

## Common Mistakes

**❌ Using DevComponents (DotNetBar) instead of Syncfusion**
→ HARD RULE VIOLATION — Creates tech debt, inconsistent with team direction

**✅ Use ONLY Syncfusion components: sfForm, SfTextBox, SfComboBox, SfDateTimePicker, SfDataGrid**

---

**❌ Leaving form in Sizeable mode by default**
→ HARD RULE VIOLATION — Forms must have fixed size; sets FormBorderStyle to FixedToolWindow or Fixed

**✅ Always set Form.FormBorderStyle = FormBorderStyle.Fixed or FormBorderStyle.FixedToolWindow**

---

**❌ Date picker without dd/MM/yyyy format**
→ Users confused by format; inconsistent with project standard

**✅ Always use SfDateTimePicker with format string `dd/MM/yyyy`; verify picker loads on form init**

---

**❌ Hand-coding colors, fonts, spacing**
→ Breaks consistency; duplicates ThemeManager logic; breaks theme updates

**✅ Call ThemeManager.cs functions for all styling—colors, fonts, spacing. Never hard-code UI constants.**

---

**❌ Designing without researching existing Syncfusion forms**
→ Creates inconsistent UI; new patterns contradict codebase

**✅ Use Semble MCP to find 3+ existing Syncfusion forms first; document their choices**

---

**❌ Over-validating in real-time**
→ Form feels sluggish (async SKU lookups on every keystroke)

**✅ Real-time validation for format only (email regex, max length); async validation only on blur or submit**

---

**❌ Using MessageBox for all errors**
→ Blocks user; feels hostile. Can't see form while error is displayed.

**✅ Layered approach: ErrorProvider (field-level) + toast (form-level) + MessageBox (critical only)**

---

**❌ Generic error messages everywhere**
→ User can't fix the error ("Invalid input")

**✅ Be specific: "SKU must be 5–10 digits. You entered 'abc' which is invalid."**

---

**❌ Forgetting accessibility (no labels, tab order broken, no keyboard shortcuts)**
→ Keyboard users blocked; screen readers confused

**✅ Checklist: Link labels to controls in Designer.cs; test tab order (Tab key navigates logically); document keyboard shortcuts**

## Model Selection Quick Reference

When complexity assessment feels uncertain or multi-step:
- **Haiku:** Login forms, simple data entry (5 fields, sync validation)
- **Sonnet:** Item masters, search forms, moderate async work
- **Opus:** Wizards, bulk operations, many unknowns, or custom component design

**Permission rule:** You can choose based on assessed complexity. If form is genuinely complex (19+), use Opus. If simple (≤12), Haiku is fine. Sonnet is default for 13–18.

## Semble MCP Workflows

**Finding existing patterns:**
```
Search the codebase for:
- "class Frm" (form definitions)
- "ErrorProvider" or "Shared.toast" (error handling patterns)
- "Shared.GetMessage" (i18n usage)
- "async" + "Validate" (async validation examples)
- Component usages (DotNetBar controls, Syncfusion refs)
```

**When you find a similar form:**
- Copy its error handling pattern (don't invent new ones)
- Reuse its validation structure (don't duplicate logic)
- Reference its accessibility markup (tab order, labels)

---

## Self-Learning: New Constraints & Component Documentation

### Adding New Constraints

**When you provide new constraints or rules via prompt, this skill MUST self-update for future applications.**

**Examples of self-learning triggers:**
- "New hard rule: all buttons must have icons from IconSet X"
- "All forms must now validate asynchronously with CancellationToken"
- "Update date format to ISO 8601 for new locale support"
- "All SfDataGrid usage must paginate after 500 rows"

**When you identify a gap or add a constraint, notify the skill:** "pawadesigner should now..." → Skill automatically updates this SKILL.md file to reflect the new requirement.

### Building Local Component Documentation

**When unsure about a Syncfusion component:**

1. **Check official Syncfusion docs:** https://help.syncfusion.com/windowsforms/form/getting-started
2. **Learn from the docs** — understand component API, common patterns, best practices
3. **Create a component sub-reference** — document the component's PawaPos usage patterns locally
4. **Link from main skill** — reference the sub-doc in this skill's component table

**Sub-reference structure:**

```
skills/pawadesigner/
  SKILL.md                          (main skill)
  references/
    sftextbox.md                    (component reference)
    sfdatetimepicker.md
    sfdatagrid.md
    sfcombobox.md
```

**Sub-reference template:**

```markdown
---
name: pawadesigner-sftextbox
description: SfTextBox usage patterns for PawaPos forms
---

# SfTextBox

## Official Docs
https://help.syncfusion.com/windowsforms/textbox/getting-started

## PawaPos Patterns

### Basic Usage
[Code example: creating SfTextBox in form]

### Validation
[Code example: TextChanged event, async validation]

### Styling with ThemeManager
[Code example: applying theme to SfTextBox]

### Common Mistakes
[Pitfalls specific to PawaPos usage]
```

**Benefit:** Over time, you'll have a library of components with:
- Official Syncfusion knowledge (condensed)
- PawaPos-specific patterns (code examples)
- Integration with ThemeManager (local styling standards)
- Common mistakes (learned from real usage)

---

**See also:** pawa-ui-authoring (branding & visual standards), systematic-debugging (fixing broken forms)
