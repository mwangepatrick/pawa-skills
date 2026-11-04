# Action Form Modes

Preserve the existing workflow and field layout. State selectors represent modes that the form owns; they do not authorize adding new modes or rearranging a parent-controlled line editor. An existing immediate Delete remains a final destructive command.

### Golden Rule: Standardize Action-Form State Buttons

All action/data-entry forms—not reports—must separate **state-selection buttons** from **command buttons**.

- Put `New`, `Edit`, and `Delete` state buttons in a single row at the top of the input-controls box, above the first input row and inside the form's normal layout boundary. If the buttons sit outside a group box, move the input group down far enough to leave a deliberate gap; never let the buttons overlap the group border or caption.
- Center the state-button row against the input box, not against the whole form. Calculate the starting X position from the box width: `boxLeft + (boxWidth - totalButtonRowWidth) / 2`. Use equal button widths and equal gaps unless the labels require an intentional variation.
- Use the shared `PawaStateButton` control from `D:\cp\pp\pawa-controls\PawaControls`, with `PawaStateButtonGroup` and `PawaFormState` for mutual exclusion and state coordination. Do not create form-specific painted button variants.
- State buttons always have a white background with a solid border and matching text. Inactive state: 1px border and normal text. Active state: stronger/thicker border and bold text. Hover/pressed feedback may darken the border/text but must never fill the button with a color.
- Default state colors are New = blue/teal, Edit = amber/orange, and Delete = red. The color communicates the selected form mode; it does not mean that the operation has already been committed.
- New, Edit, and Delete are mutually exclusive. Selecting one activates it and deactivates the others. Delete must enter delete state only and wait for the existing form workflow; preserve patterns such as `PrepareDelete(); SendKeys.Send("{F11}");`. Never commit a destructive delete from a state-selector click; an existing immediate-delete action must be represented as a separate destructive command.
- Preserve command behavior while enforcing the mandatory button roles below: Save remains orange, Cancel/Close black, and supporting Export/Print/Reset grey. Existing inconsistent styling is not an exception.
- State buttons must remain editable in Visual Studio Designer, use explicit designer fields/properties, and be independent of Syncfusion so they cannot introduce another third-party design-time dependency.
- State-button captions must expose keyboard mnemonics in the Designer, using labels such as `&New`, `&Edit`, and `&Delete`; keep the mnemonic unique within the action row.

For a standard action form, the layout should read:

```text
        [ New ]    [ Edit ]    [ Delete ]
┌─ Input Details ───────────────────────────────┐
│ Label:      [________________________]         │
│ Label:      [________________________]         │
│                         [Save] [Close]         │
└───────────────────────────────────────────────┘
```
