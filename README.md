# pawa-skills

A collection of reusable Claude Code skills for PawaPos and related projects. Built by [mwangepatrick](https://github.com/mwangepatrick).

## Skills in This Collection

### 1. [pawadesigner](./pawadesigner/)
Form design skill for PawaPos project—design Syncfusion-based forms with hard rules for components, styling, date formats, and accessibility.

**Use when:** Designing any form (login, data entry, configuration, dialogs)

**Key features:**
- Complexity assessment rubric (Haiku/Sonnet/Opus model selection)
- Syncfusion component reference with sub-documentation
- Validation pattern taxonomy
- ThemeManager.cs integration
- Hard rules enforcement (no DevComponents, no Sizeable mode, dd/MM/yyyy dates)

**Sub-references:**
- [SfDateTimePicker](./pawadesigner/references/sfdatetimepicker.md) — Date picker patterns, validation, accessibility

---

## Installation

### Option A: Manual Installation (Quick)

1. Clone this repo:
   ```bash
   git clone https://github.com/mwangepatrick/pawa-skills.git D:\cp\pp\pawa-skills
   ```

2. Create symlink to global skills directory:
   ```bash
   # PowerShell (Admin)
   New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\pawadesigner" -Target "D:\cp\pp\pawa-skills\pawadesigner" -Force
   ```

   **OR** copy directly:
   ```bash
   xcopy "D:\cp\pp\pawa-skills\pawadesigner" "$env:USERPROFILE\.claude\skills\pawadesigner" /E /I
   ```

3. Verify installation:
   ```bash
   ls $env:USERPROFILE\.claude\skills\pawadesigner
   # Should show: SKILL.md, references/
   ```

### Option B: Automated Installation (Recommended)

Run the install script:
```bash
cd D:\cp\pp\pawa-skills
./install.ps1
```

(Script coming soon — manually install for now)

---

## Usage

In Claude Code, the skills are automatically available when installed locally.

**Example:** Type `/pawadesigner` or mention "form design" and Claude will suggest the skill.

**Updating skills:**
```bash
cd D:\cp\pp\pawa-skills
git pull origin main
# Reinstall if needed
```

---

## Contributing

To add new skills or improve existing ones:

1. Create a new skill directory: `D:\cp\pp\pawa-skills/<skill-name>/`
2. Follow the structure:
   ```
   <skill-name>/
     SKILL.md              # Main skill file (required)
     references/
       <component-1>.md    # Optional sub-references
       <component-2>.md
   ```
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Add pawadesigner skill"
   git push origin main
   ```

---

## Structure

```
pawa-skills/
  README.md                    (this file)
  LICENSE                      (coming soon)
  .gitignore
  pawadesigner/
    SKILL.md                   (main skill)
    references/
      sfdatetimepicker.md      (component sub-reference)
  <future-skills>/
    SKILL.md
    references/
```

---

## License

(To be decided — MIT, CC-BY, or internal use only?)

---

## Support

For issues, questions, or contributions: Create an issue on GitHub or reach out to mwangepatrick.

---

**Last updated:** 2026-08-06  
**Skills installed:** 1 (pawadesigner)
