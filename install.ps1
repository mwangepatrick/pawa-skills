# pawa-skills Installation Script
# Installs all skills to local Claude Code skills directory

param(
    [switch]$Symlink = $false,  # Use symlink instead of copy
    [switch]$Force = $false      # Overwrite existing installations
)

$ErrorActionPreference = "Stop"

# Paths
$skillsDir = Split-Path -Parent $PSCommandPath
$claudeSkillsDir = "$env:USERPROFILE\.claude\skills"
$agentsSkillsDir = "$env:USERPROFILE\.agents\skills"

# Determine target directory (prefer .agents/skills for cross-CLI compatibility)
$targetDir = if (Test-Path $agentsSkillsDir) { $agentsSkillsDir } else { $claudeSkillsDir }

Write-Host "pawa-skills Installation" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Source:      $skillsDir"
Write-Host "Install to:  $targetDir"
Write-Host "Symlink:     $Symlink"
Write-Host ""

# Create target directory if needed
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

# Install each skill
$skills = Get-ChildItem -Path $skillsDir -Directory | Where-Object { Test-Path "$_.FullName\SKILL.md" }

if ($skills.Count -eq 0) {
    Write-Host "No skills found to install (looking for SKILL.md files)" -ForegroundColor Yellow
    exit 1
}

foreach ($skill in $skills) {
    $skillName = $skill.Name
    $skillSource = $skill.FullName
    $skillTarget = Join-Path $targetDir $skillName

    Write-Host "Installing: $skillName" -ForegroundColor Yellow

    # Handle existing installation
    if (Test-Path $skillTarget) {
        if ($Force) {
            Write-Host "  Removing existing installation..."
            Remove-Item -Path $skillTarget -Recurse -Force | Out-Null
        } else {
            Write-Host "  ✓ Already installed at $skillTarget (use -Force to overwrite)" -ForegroundColor Green
            continue
        }
    }

    # Install via symlink or copy
    if ($Symlink) {
        try {
            New-Item -ItemType SymbolicLink -Path $skillTarget -Target $skillSource -Force | Out-Null
            Write-Host "  ✓ Symlink created" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Symlink failed (requires admin): $_" -ForegroundColor Red
            Write-Host "  Falling back to copy..." -ForegroundColor Yellow
            Copy-Item -Path $skillSource -Destination $skillTarget -Recurse -Force
            Write-Host "  ✓ Copied instead" -ForegroundColor Green
        }
    } else {
        Copy-Item -Path $skillSource -Destination $skillTarget -Recurse -Force
        Write-Host "  ✓ Copied to $skillTarget" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart Claude Code (if running)"
Write-Host "2. Skills will be available in your projects"
Write-Host "3. Mention 'form design' or type '/pawadesigner' to use"
Write-Host ""
Write-Host "Uninstall: Remove directories from $targetDir" -ForegroundColor Gray
