# SfForm

`Syncfusion.WinForms.Controls.SfForm` is the required form base. It inherits WinForms Form, so fixed borders, ClientSize, docking, Icon and shared ThemeManager methods remain applicable.

Required assemblies are `Syncfusion.Core.WinForms` and `Syncfusion.Shared.Base`. Audit actual versions, transitive dependencies, Copy Local and host architecture before migration; see [Designer workflow](designer-workflow.md). An x86 runtime build is not proof of 64-bit design-host compatibility.

Keep a parameterless design-safe constructor. Start with `InitializeComponent()` and guard runtime database/device/application access with `LicenseManager.UsageMode == LicenseUsageMode.Designtime`. Extract the application executable icon only at runtime.

Use `PawaControls.ThemeManager.ApplyModernTheme(this)` and verified shared control/command helpers. Native-looking title-bar chrome is expected unless a shared theme configures it. Changing the base class does not authorize local skinning or rearranging the user's fields.
