# Mandatory Button and Dropdown Standards

These rules apply to every new or modified PawaPos form, including listings,
reports, dialogs, and data-entry forms. Existing mismatches are migration work,
not examples to copy. Do not declare a touched form compliant while leaving
its buttons or dropdown labels inconsistent with these rules.

## Button roles

Use exactly these six semantic families. Select the role explicitly; never
infer it from a control name or automatically make every button primary.

| Family | Required appearance | Purpose |
| --- | --- | --- |
| Primary | Solid orange `#FF6633`, white bold text, no border | Save, Submit, and the main Apply/Refresh action |
| Secondary / utility | Grey `#C8C8C8`, dark `#333333` regular text, thin `#DCDCDC` border | Export, Print, Reset, and supporting actions |
| Close / Cancel | Solid black `#000000`, white bold text, thin black border | Close a page, dismiss a dialog, cancel editing |
| Service / tools | Solid blue `#0078D4`, white bold text, no border; visible dropdown arrow when opening a menu | Online M-Pesa, integrations, and tool menus |
| State selection | White fill at all times; matching colored text/outline: New `#007ACC`, Edit `#CD7800`, Delete `#C00000` | Choose a form mode; 1px regular inactive, 2px bold active; use `PawaStateButton` and `PawaStateButtonGroup` |
| Destructive command | Solid red `#C83232`, white bold text | Explicit final Delete, Remove, or Void operation; never use for merely selecting Delete mode |

Give the principal command priority; do not color supporting Export/Print/Reset
buttons orange to match historical forms. Keep the same action in the same
family throughout the application. A supporting Refresh is secondary when a
different operation is the principal command.

## Shared appearance and interaction states

- Use flat, square command buttons, Verdana 8, and a 36px logical command height.
  State selectors retain their shared control sizing and outline behavior.
- Centralize spacing and minimum widths; align equal-role buttons and use equal
  gaps. Expand widths for long labels without truncation. Explicit Designer
  dimensions must agree with the shared runtime sizing and same-row alignment.
- All styles must define normal, hover, pressed, disabled, and visible keyboard
  focus states. Hover/pressed feedback stays within the role's color family.
  Primary hover is `#E6501E`, pressed `#C83C14`; Close hover is `#282828`,
  pressed `#464646`. Define missing palettes centrally before using them.
- Disabled command buttons use a clear grey background and readable muted text,
  regardless of their enabled role. A disabled service button must not remain
  blue with unexplained dark text. State selectors remain white with grey
  outlines/text when disabled. Disabled controls must not execute actions.
- Keep keyboard mnemonics, focus cues, tab order, and existing action semantics.
- Use the project's referenced `ThemeManager` and shared controls. Do not add
  form-local colors, fonts, painted variants, or styling exceptions. Custom
  buttons such as `PawaButton` must implement these same role/state tokens.
- Audit theme application order: a later role helper must fully replace all
  earlier styling. Secondary and blue buttons must never inherit an orange
  pressed background. Do not assume `ForeColor = White` controls disabled text.
- Verify the actual source/DLL before calling helpers. Primary, secondary,
  close, and accent helpers exist in the audited shared source; a destructive
  helper and complete disabled-state treatment are requirements to implement
  centrally, not APIs to invent in a form.

## Dropdown display labels and underlying values

- Every choice shown in every dropdown must be FULL UPPERCASE, both in the
  expanded list and after selection. This includes static choices, database
  lookups, enum-backed choices, dynamic additions, and editable combo boxes.
- Separate the human-readable display label from the underlying value/code.
  Use `DisplayMember` / `ValueMember`, a display/value item, or the audited
  equivalent supported by the actual control. Never expose a raw enum name,
  database field name, or internal value as the label when it is not meaningful.
- Example: display `PARTIALLY RECEIVED` while retaining `PartiallyReceived`,
  `Partially Received`, or a numeric code as the original underlying value.
  Display `ALL` while retaining the existing sentinel value used by filtering.
- Uppercase the presentation label, not the stored value. Preserve case-sensitive
  identifiers, selected-value comparisons, queries, persistence, and exports'
  established contracts. Do not uppercase database records as a presentation fix.
- Logic must read the underlying selected value, not the uppercased display text.
  If existing logic compares `Text`, migrate that comparison to the value with
  the display change. `CharacterCasing` alone does not uppercase bound choices.
- Test initial selection, opening the list, changing selection, reset/reload,
  and dynamic choices. Confirm labels remain uppercase and the original values
  still drive the same filtering and saving behavior.

## Required review checks

Reject a form change if Export changes family between pages, Close is grey,
blue/grey commands flash orange when pressed, disabled commands retain their
enabled fill, Delete mode commits immediately, or any dropdown displays mixed
case or substitutes its label for the underlying value. Verify Designer and
runtime rendering, all button states, keyboard operation, and dropdown value
preservation; document checks that could not be performed.
