$ErrorActionPreference = "Stop"

Write-Host "Running QuickSmoke Checks..."

# Resolve repo root reliably.
# Script path: lifeos/tools/quicksmoke.ps1
# Repo root is two levels up.
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")

# Sanity check: ensure we found the actual repo root
$RootSentinel = Join-Path $RepoRoot "render.yaml"
if (!(Test-Path $RootSentinel)) {
    Write-Host "Repo root sentinel not found: $RootSentinel"
    Write-Host "RepoRoot resolved to: $RepoRoot"
    exit 1
}

Write-Host "RepoRoot: $RepoRoot"

# Required files that define the current working system
$RequiredPaths = @(
    "knowledge/00_LifeOS_Constitution.md",
    "knowledge/01_ModeRouter.md",
    "instructions/Instructions.txt",
    "public/.well-known/openapi.json",
    "scripts/ci/validate_openapi.py",
    "lifeos/canon/integrity_contract.json",
    "canon_baselines/snapshot_hash.txt",
    "canon_baselines/digest_hash.txt"
)

$failures = 0

Write-Host ""
Write-Host "Checking required paths..."

foreach ($rel in $RequiredPaths) {
    $abs = Join-Path $RepoRoot $rel
    if (!(Test-Path $abs)) {
        Write-Host "MISSING: $rel"
        $failures++
    }
    else {
        Write-Host "Found:   $rel"
    }
}

if ($failures -gt 0) {
    Write-Host ""
    Write-Host "QuickSmoke FAILED - $failures required file(s) missing."
    exit 1
}

Write-Host ""
Write-Host "Validations..."

# 1) OpenAPI JSON must be valid JSON
$OpenApiPath = Join-Path $RepoRoot "public/.well-known/openapi.json"
Write-Host "Validating OpenAPI JSON..."
python -m json.tool $OpenApiPath > $null

# 2) OpenAPI contract validator (repo-specific)
Write-Host "Running OpenAPI validator..."
$ValidatorPath = Join-Path $RepoRoot "scripts/ci/validate_openapi.py"
python $ValidatorPath

Write-Host ""
Write-Host "QuickSmoke PASSED."
exit 0
