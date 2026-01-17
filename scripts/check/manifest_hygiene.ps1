param(
    [switch]$Check
)

Write-Output "🔧 Running manifest_order_fix.ps1..."
$fixScript = Join-Path $PSScriptRoot "..\fix\manifest_order_fix.ps1"
$fixScript = Resolve-Path $fixScript

if (-not $Check) {
    pwsh $fixScript
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Fix script failed."
        exit 1
    }
} else {
    pwsh $fixScript --check
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Manifest files are not in canonical order."
        exit 1
    }
}

Write-Output "🔍 Running manifest_lint.ps1..."
$lintScript = Join-Path $PSScriptRoot "..\lint\manifest_lint.ps1"
$lintScript = Resolve-Path $lintScript

pwsh $lintScript
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Lint check failed."
    exit 1
}

Write-Output "`n✅ Manifest hygiene checks passed."
exit 0
