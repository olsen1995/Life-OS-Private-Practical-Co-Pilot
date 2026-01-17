Write-Output "🧼 Pre-commit (PowerShell): Running hygiene check..."

# Run hygiene fix + lint script
pwsh ./scripts/check/manifest_hygiene.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Pre-commit check failed."
    exit 1
}

Write-Output "✅ Pre-commit: All checks passed."
exit 0
