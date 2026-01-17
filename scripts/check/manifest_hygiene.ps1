<#
.SYNOPSIS
    Full manifest hygiene pass: fix, then lint.
.DESCRIPTION
    - Auto-fixes .manifest file key order
    - Then lints for formatting and structure
    - Can be used in --check (CI) mode
.PARAMETER Check
    If specified, only checks; does not auto-fix
#>

param(
    [switch]$Check
)

$fixScript = Join-Path $PSScriptRoot "..\fix\manifest_order_fix.ps1"
$lintScript = Join-Path $PSScriptRoot "..\lint\manifest_lint.ps1"

# Run the fixer (unless --check is passed)
if (-not $Check) {
    Write-Output "🔧 Running manifest_order_fix.ps1..."
    pwsh $fixScript
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Fix script failed."
        exit 1
    }
}
else {
    Write-Output "🔍 Running manifest_order_fix.ps1 --check..."
    pwsh $fixScript --check
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ manifest files are not in canonical order."
        exit 1
    }
}

# Always run linter next
Write-Output "🔍 Running manifest_lint.ps1..."
pwsh $lintScript
if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Lint check failed."
    exit 1
}

Write-Output "`n✅ Manifest hygiene checks passed!"
