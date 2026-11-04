# SfButton

`Syncfusion.WinForms.Controls.SfButton` is in `Syncfusion.Core.WinForms` and derives from WinForms Button. Audit actual dependencies before replacing a command control.

Use the verified `PawaControls.ThemeManager.StylePrimaryButton`, `StyleSecondaryButton`, `StyleCloseButton`, `StyleAccentButton` or `StyleDestructiveButton` for the action's role. The audited `ThemeManager.Syncfusion.cs` applies SfButton's Style palette through `StyleSyncfusionCommand`, including hover, pressed, focused and disabled states.

SfButton paints from its Style object. A helper setting only inherited BackColor/ForeColor is insufficient. Check the target source and deployed DLL; if the Syncfusion branch is absent, extend the owning shared helper within scope and verify existing callers. Avoid local palettes and guessed APIs. A compatible standard Button is a documented fallback only when the available contract cannot preserve behavior.

Keep captions, mnemonics, semantics, 36px command height, widths and spacing in Designer. Apply the role after broad theming so other actions cannot inherit primary states. Verify inherited properties and actual rendering in every state. Full palettes live in [buttons/dropdowns](buttons-dropdowns.md).
