# Form Layout Fit and Reachable Commands

Mandatory for every new or modified form, listing, report and dialog. It exists
because fixed-size forms were authored taller than small screens, so the command
buttons (positioned absolutely below the fields) ended up off-screen and could
not be reached. Keep this rule beside the button standards in
`buttons-dropdowns.md`; it does not change button roles, colors or states.

## The rule

A form must fit the smallest supported screen, and its commands must never be
hideable.

1. **Height budget.** A fixed-size form, including its title bar, must fit a
   1366x768 screen at 100% scaling. Target a `ClientSize` height of 640 logical
   px or less. Also verify at 125% and 150% scaling on a 1920x1080 screen.
2. **One spacing scale.** Use the same vertical rhythm on every form: 28px
   inputs, a 36px row pitch, a 16px outer margin, and labels offset so they
   centre on the input (label top = input top + (input height - label height) / 2,
   which is +5 for a 22px label beside a 28px input). Command buttons keep the
   shared 36px height. Take the values from `ThemeManager`; do not eyeball them
   per form. If the constants are not centralised yet, add them there instead of
   repeating literals in a Designer file.
3. **No dead space.** The last visible control sits one margin (16px) above its
   container edge. Do not size containers "just in case". Hidden placeholder
   controls (`Visible = false`, 1px size) must not drive layout height; delete
   them when nothing references them, otherwise keep them inside the container.
   Multi-line inputs are 44px (about three lines of Verdana 8) unless the
   workflow needs more.
4. **Commands live in a footer.** Put Save, Close, Reset and the status text in a
   bottom-docked footer panel, not at absolute positions below the content.
   Put the fields in a fill-docked body panel with `AutoScroll = true`. If the
   content outgrows the screen the body scrolls and the commands stay reachable.
   This is the future-proof part: it holds however many fields are added later.
5. **Overflow safety net.** In the constructor, after `InitializeComponent()`,
   cap the form height at `Screen.FromControl(this).WorkingArea.Height`
   (guard the call for design time, like the other constructor-only code).
6. **Same-row alignment.** Same-row controls share a height and are centred by
   computed offset (see Row Alignment in `SKILL.md`). A date editor beside
   28px text boxes is also 28px, not its 21px default.

## Review checks

Reject a form change when any of these is true:

- A command button's bottom edge is below the height budget, or a command can be
  hidden by a smaller screen or higher DPI scaling.
- Commands are positioned absolutely under the fields instead of in a footer.
- A container has more than one margin of empty space below its last control.
- Row pitch, input height or margins differ from the shared scale without a
  stated reason.
- The form was not checked at the budget size and at 125% / 150% scaling, and
  the report does not say so.

## Verification

- Compute the height budget from the Designer values; do not assume.
- Open the form in the Designer and at runtime at 100%, 125% and 150%.
- Confirm the footer stays visible and the body scrolls when the window is made
  shorter than the content.
- Report which of these checks could not be performed.

## Notes for existing forms

Existing oversize forms are migration work, not examples to copy. When a touched
form already has a footer-less layout, compacting (rules 2 and 3) is the minimum;
moving the commands into a footer (rule 4) is the durable fix.

Worked example: the Receive Payment form (`cashTransaction`) was 776px tall with
buttons at y=720-756 on a fixed, non-scrolling window. Compacting the 40-44px
row steps to 36px, trimming a 632px panel to 516px and removing a 40px empty
band took it to 636px. The footer-and-scroll-panel change was the remaining
step.
