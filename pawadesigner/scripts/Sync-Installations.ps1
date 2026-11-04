param(
    [string]$SourcePath = (Split-Path $PSScriptRoot -Parent),
    [string[]]$DestinationPaths = @(
        (Join-Path $env:USERPROFILE '.codex\skills\pawadesigner'),
        (Join-Path $env:USERPROFILE '.claude\skills\pawadesigner')
    )
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath $SourcePath).Path
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
    throw 'Source must be a pawadesigner skill folder containing SKILL.md.'
}
$files = @(Get-ChildItem -LiteralPath $source -Recurse -File)
foreach ($destinationPath in $DestinationPaths) {
    $destination = [IO.Path]::GetFullPath($destinationPath)
    if ($destination.TrimEnd('\') -eq $source.TrimEnd('\')) { continue }
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($source.Length).TrimStart('\')
        $target = Join-Path $destination $relative
        New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $target -Force
        if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $target).Hash) {
            throw "Installed file differs: $target"
        }
    }
    Write-Output "Verified $($files.Count) skill files: $destination"
}
