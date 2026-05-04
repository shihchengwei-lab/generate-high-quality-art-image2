param(
    [string]$Source,
    [string]$Destination,
    [switch]$SkipDryRun
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $Source) {
    $Source = Join-Path $repoRoot ".agents\skills\generate-high-quality-art-image2"
}
if (-not $Destination) {
    $Destination = Join-Path $env:USERPROFILE ".codex\skills\generate-high-quality-art-image2"
}

$sourceFull = (Resolve-Path -LiteralPath $Source).Path
$skillsRoot = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
$skillsRootFull = (Resolve-Path -LiteralPath $skillsRoot).Path
$destFull = [System.IO.Path]::GetFullPath($Destination)

if (-not $destFull.StartsWith($skillsRootFull + [System.IO.Path]::DirectorySeparatorChar)) {
    throw "Refusing to sync outside Codex skills root: $destFull"
}

New-Item -ItemType Directory -Force -Path $destFull | Out-Null

$robocopyArgs = @(
    $sourceFull,
    $destFull,
    "/MIR",
    "/XD", "__pycache__", ".pytest_cache", "_install_test_outputs",
    "/XF", "*.pyc"
)

& robocopy @robocopyArgs | Out-Host
if ($LASTEXITCODE -gt 7) {
    throw "robocopy failed with exit code $LASTEXITCODE"
}

$required = @(
    "SKILL.md",
    "scripts\build_prompt.py",
    "scripts\generate_direct.py",
    "scripts\lib\spec_contract.py",
    "scripts\lib\reference_roles.py",
    "scripts\lib\prompt_scorer.py",
    "assets\sample_debug_spec.yaml"
)

foreach ($rel in $required) {
    $path = Join-Path $destFull $rel
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing installed file: $path"
    }
}

$front = Get-Content -LiteralPath (Join-Path $destFull "SKILL.md") -TotalCount 4
if ($front[0] -ne "---") {
    throw "SKILL.md missing frontmatter fence."
}
if (-not ($front | Where-Object { $_ -eq "name: generate-high-quality-art-image2" })) {
    throw "SKILL.md missing expected skill name."
}

$installedScripts = Join-Path $destFull "scripts"
python -m compileall -q $installedScripts

if (-not $SkipDryRun) {
    $out = Join-Path $env:TEMP "codex-skill-install-check-generate-high-quality-art-image2"
    if (Test-Path -LiteralPath $out) {
        Remove-Item -LiteralPath $out -Recurse -Force
    }
    python (Join-Path $destFull "scripts\generate_direct.py") `
        --spec (Join-Path $destFull "assets\sample_debug_spec.yaml") `
        --out $out `
        --dry-run
    if ($LASTEXITCODE -ne 0) {
        throw "Installed dry-run failed."
    }
    Remove-Item -LiteralPath $out -Recurse -Force
}

Get-ChildItem -LiteralPath $destFull -Recurse -Directory -Filter "__pycache__" |
    ForEach-Object { Remove-Item -LiteralPath $_.FullName -Recurse -Force }

Write-Output "Synced and verified local Codex skill: $destFull"
Write-Output "Restart Codex to pick up the updated installed skill."

exit 0
