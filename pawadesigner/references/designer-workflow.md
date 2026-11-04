# Designer and Runtime Verification

Read only applicable sections. A successful build, a generated Designer file and an actual Visual Studio Designer load are distinct evidence.

### Golden Rule: Prove Designer Loadability Before Migrating a Form

**Never begin a WinForms control migration until the complete design-time dependency and load path has been audited and proven.** A successful application build or runtime launch is not evidence that the Visual Studio designer can load the form.

Before changing a form, perform this mandatory gate:

1. Confirm the exact solution and project being edited. Record the absolute `.sln`, `.csproj`, form source, and designer paths. Do not infer the project from a similarly named open Visual Studio window.
2. Use the known-good reference project (normally `pawapos-bo`) to compare both `packages.config` and explicit `.csproj` references. For every third-party control, include the complete direct and transitive dependency closure—not just the top-level package. Every required assembly must have the matching version, `HintPath`, and `Private=True`/Copy Local behavior where applicable.
3. Build the exact configuration Visual Studio Designer uses, normally `Debug|Any CPU`, from a clean project state. Verify every required DLL exists in that configuration's actual output directory and that its assembly version matches the reference project. Do not rely on stale DLLs from `bin`, `obj`, another platform, or another project.
4. Check architecture compatibility with the designer host. Visual Studio's modern WinForms designer is 64-bit; an `x86` project or x86-only dependency can fail design-time loading even when the application runs. Keep runtime host architecture requirements separate from the class-library architecture where possible.
5. Ensure the form constructor is design-time safe. Call `InitializeComponent()` first, then return when `LicenseManager.UsageMode == LicenseUsageMode.Designtime` before database access, application-singleton access, device initialization, file I/O, or other runtime startup logic.
6. Keep `*.Designer.cs` conventional and designer-generated: explicit field declarations, explicit control construction, explicit property assignments, and explicit event wiring. Do not use compressed one-line helpers, dynamic-only control factories, inline object graphs, or runtime-only initialization for controls that must be editable in Designer.
7. Test the design-time load path before declaring the migration complete: the form must open in Visual Studio without parser, serialization, missing-assembly, missing-control, or `InitializeComponent` errors. If a third-party control cannot be loaded by the host, use and document a design-time placeholder/runtime control fallback rather than repeatedly adding guessed references.

This gate is mandatory because designer failures commonly appear as misleading secondary errors such as “variable is undeclared or was never assigned.” The first missing assembly or constructor exception is the root signal; all later CodeDom errors are usually cascades.

## Manual Runtime Testing Through Program.cs

When a PawaPos form needs manual runtime testing, add a temporary direct launch
in the application's existing `Program.cs`, following the established GL form
testing pattern. This is the default way to make the form available for the
user's manual test.

- Trace the exact menu action requested by the user and reuse its form class,
  constructor arguments, transaction ID and edition-specific selection. For
  example, Add D/Note uses transaction `162` and `SopTransNoEdit("")`, or
  `SopWTransNoEdit("")` in wholesale mode; `DeliveryNoteInvoice(false)` is the
  separate invoice-conversion screen.
- Place the launch after the existing license, connection/profile, system,
  user, branch and location initialization. Reuse the established test-session
  identity and permissions. Initialize any context normally supplied by
  `Main_Load`, including `PawaPosFin.Main.SetCurrentUser(Pos.CurrentUser)` for
  finance-dependent forms and `Pos.IsWSale` where the menu uses wholesale mode.
- Call `Pos.TransactionMaster` with the menu's transaction ID before constructing
  a transaction-dependent form, handle failed setup, and run the chosen form
  with `Application.Run`. Return after it closes so the normal main window does
  not launch too. Preserve the existing queue/report-service cleanup.
- Finish the source changes, build with the repository's existing script, and
  identify the compiled executable for the user to run. Report build success
  separately from manual flows the user has actually exercised.
- Keep the direct launch available while the user tests. Before a normal release,
  remove only the temporary startup override and restore normal startup,
  preserving unrelated `Program.cs` edits. A runtime launch does not establish
  Visual Studio Designer compatibility.

## Form Refactor Audit Rule

When changing or modernizing an existing form, audit the complete form before
editing it. Inspect the form code, designer file, project references, event
handlers, data-binding methods, and every control already present.

For each control, identify whether a supported Syncfusion equivalent exists in
the project’s referenced assemblies. When one exists, replace the control and
update its designer declaration, properties, events, selection APIs, and
data-binding code. Do not replace controls mechanically: if no compatible
equivalent is installed or the replacement would remove behavior, retain the
original control, document the exception, and identify the dependency or API
work needed for a later migration.

Preserve validation, keyboard shortcuts, database queries, sorting, filtering,
selection behavior, formatting, row highlighting, enabled/read-only states,
layout, and user feedback.

For checkbox fields, use `Syncfusion.Windows.Forms.Tools.CheckBoxAdv` when
`Syncfusion.Tools.Windows.dll` is referenced. Do not use
`Syncfusion.Windows.Forms.ThemedCheckButton` as a checkbox replacement: it is
a themed button and can render button-style or unreliable checkbox visuals.

## Post-Refactor Regression Audit

After changing a form, perform a before-versus-after audit and explicitly check:

- Every original control and named field still exists or has a documented replacement.
- Checkbox fields use `CheckBoxAdv`, not `ThemedCheckButton`; verify checked and unchecked visuals as well as the `Checked` value.
- All original events remain wired to handlers with compatible event arguments.
- Every button uses its mandated semantic family; normal/hover/pressed/disabled/focus states, command height, spacing, and Designer/runtime sizing match [Mandatory Button and Dropdown Standards](buttons-dropdowns.md).
- Every dropdown's expanded and selected labels are uppercase and human-readable; original values, selection/reset behavior, filtering and saving are preserved independently of display text.
- Shared capabilities are reused; shared extensions remain compatible with existing callers, and required DLL rebuild/deployment steps are reported.
- Every feedback path on the touched form uses verified PawaUtils.Dialogs APIs, including unchanged handlers; success, errors, validation, confirmations, cancellation, owner and UI-thread behavior are verified or explicitly reported as unverified.
- Save, refresh, close, lookup, validation, and navigation flows remain intact.
- Data-binding fields, column mappings, sorting, filtering, selection, and row counts work.
- Formatting, fonts, colors, enabled/read-only states, tab order, anchors, and fixed-size behavior are preserved or intentionally changed.
- Grid behavior still works: hidden identifiers, fill columns, human-readable headers, timestamp formats, and conditional row styling.
- Receipt/detail listings retain full-row mouse and keyboard selection, brand selection/current-cell colors and alternating rows; selected rows remain readable over conditional styling.
- Disabled display fields skip Tab navigation, keep the intended left/right alignment and center their text after showing, loading values, and font/size/handle changes. Copyable read-only fields remain usable.
- Receipt payment display and export both omit zero amounts while retaining positive payments and negative refunds; unrelated grids keep meaningful zero values.
- The designer opens without parser, serialization, missing-method, or missing-control errors.
- Custom `PawaControls` controls used by the form have a verified project reference, matching output DLL, design-time-safe constructor, and successful Designer instantiation.
- The project compiles and the relevant form is exercised manually.

The final report must list behavior that could not be verified, retained WinForms
controls, and known differences from the pre-refactor form.

## Validation and handoff

Use ErrorProvider for field validation and verified PawaUtils.Dialogs APIs for feedback. Validate formats locally, database lookups on blur and cross-field/business rules before submit. Suppress Leave validation during programmatic reset/loading/cancellation. Preserve input and recovery behavior after failures.

At handoff separate implementation, successful checks and unverified behavior. Include retained controls and reasons, executable/DLL prerequisites, temporary startup overrides, actual Designer-load results, rendered interaction states, screen fit and DPI checks. Do not describe a form as usable before prerequisites are applied.
