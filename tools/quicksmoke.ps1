#requires -Version 7.0
<#
Life OS — QuickSmoke (Tier 2: Core Integrity)
Dependency-free PowerShell 7 script.

Checks:
1) Core files exist (architecture floor)
2) instructions/Instructions.txt exists and is non-trivial (>=2000 chars)
3) canon/CANON_MANIFEST.json exists and parses as JSON
4) Placeholder drift scan (TODO/FIXME/TBD/<INSERT/REPLACE ME) in instructions + manifest
5) Manifest-referenced paths exist in repo (robust extraction):
   - Any property named "path"
   - Any string value that looks like a repo-relative path (ignores URLs)
   - Normalizes slashes, rejects absolute paths and ../ traversal
   - Skips repo identifiers like "owner/repo" ONLY when they do NOT look like file paths (no dots)
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Fail([string]$Message) {
  Write-Host "FAIL: $Message" -ForegroundColor Red
  exit 1
}

function Ok([string]$Message) {
  Write-Host "OK: $Message" -ForegroundColor Green
}

# Repo root is parent of /tools
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$InstructionsPath = Join-Path $RepoRoot "instructions\Instructions.txt"
$ManifestPath     = Join-Path $RepoRoot "canon\CANON_MANIFEST.json"

Write-Host "Life OS QuickSmoke running..." -ForegroundColor Cyan
Write-Host "Repo root: $RepoRoot"
Write-Host ""

# 0) Tier-2: Core files MUST exist
$coreFiles = @(
  "knowledge/00_LifeOS_Constitution.md",
  "knowledge/01_ModeRouter.md",
  "instructions/Instructions.txt",
  "canon/CANON_MANIFEST.json"
)

$missingCore = @()
foreach ($f in $coreFiles) {
  $full = Join-Path $RepoRoot $f
  if (-not (Test-Path $full)) { $missingCore += $f }
}

if ($missingCore.Count -gt 0) {
  Write-Host "Missing core file(s):" -ForegroundColor Yellow
  $missingCore | ForEach-Object { Write-Host " - $_" }
  Fail ("{0} core file(s) missing. Restore before continuing." -f $missingCore.Count)
}
Ok "Core files exist (Tier-2 floor)"

# 1) Instructions exists and length check
if (-not (Test-Path $InstructionsPath)) {
  Fail "Missing file: instructions/Instructions.txt"
}

$instr = Get-Content $InstructionsPath -Raw
if ($instr.Trim().Length -lt 2000) {
  Fail "Instructions.txt too short (<2000 chars). Found $($instr.Trim().Length)."
}
Ok "Instructions.txt exists and length looks good ($($instr.Trim().Length) chars)"

# 2) Manifest exists and parses
if (-not (Test-Path $ManifestPath)) {
  Fail "Missing file: canon/CANON_MANIFEST.json"
}

try {
  $manifestRaw = Get-Content $ManifestPath -Raw
  $manifest = $manifestRaw | ConvertFrom-Json
} catch {
  Fail "canon/CANON_MANIFEST.json is not valid JSON: $($_.Exception.Message)"
}
Ok "Canon manifest exists and parses"

# 3) Placeholder drift scan (instructions + manifest)
$placeholderPatterns = @("TODO","FIXME","TBD","<INSERT","REPLACE ME")
$hits = Select-String -Path $InstructionsPath, $ManifestPath -Pattern $placeholderPatterns -SimpleMatch -ErrorAction SilentlyContinue
if ($hits) {
  Write-Host "Placeholder hits found:" -ForegroundColor Yellow
  $hits | ForEach-Object { Write-Host (" - {0}:{1}: {2}" -f $_.Path, $_.LineNumber, $_.Line.Trim()) }
  Fail "Resolve placeholder tokens before shipping."
}
Ok "No placeholder tokens detected in instructions/manifest"

# 4) Discover and validate manifest-referenced paths (robust extraction)
$paths = New-Object System.Collections.Generic.List[string]

function LooksLikeRepoSlug([string]$p) {
  # "owner/repo" (two segments) with no dots anywhere
  return ($p -match '^[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+$' -and -not ($p -match '\.'))
}

function Add-Path([string]$p) {
  if ([string]::IsNullOrWhiteSpace($p)) { return }
  $p = $p.Trim()

  # Ignore URLs
  if ($p -match '^\w+://') { return }

  # Normalize slashes
  $p = $p -replace '\\','/'

  # Skip repo identifiers like "owner/repo" (only if it doesn't look like a file path)
  if (LooksLikeRepoSlug $p) { return }

  # Reject absolute paths or traversal
  if ($p.StartsWith("/") -or $p -match '^[A-Za-z]:/' -or $p.Contains("../") -or $p.Contains("..\")) {
    Fail "Unsafe/absolute path found in manifest: $p"
  }

  # Only keep candidates that look path-like:
  # - contains a slash (folder separator), OR
  # - ends with a likely file extension
  if ($p.Contains('/') -or $p -match '\.[A-Za-z0-9]{1,8}$') {
    $paths.Add($p)
  }
}

function Walk($node) {
  if ($null -eq $node) { return }

  if ($node -is [System.Management.Automation.PSCustomObject]) {
    foreach ($prop in $node.PSObject.Properties) {
      if ($prop.Name -ieq "path" -and $prop.Value -is [string]) {
        Add-Path $prop.Value
      }
      Walk $prop.Value
    }
    return
  }

  if ($node -is [hashtable]) {
    foreach ($k in $node.Keys) {
      $v = $node[$k]
      if ($k -ieq "path" -and $v -is [string]) { Add-Path $v }
      Walk $v
    }
    return
  }

  if ($node -is [System.Collections.IEnumerable] -and -not ($node -is [string])) {
    foreach ($item in $node) { Walk $item }
    return
  }

  if ($node -is [string]) { Add-Path $node }
}

Walk $manifest

$uniquePaths = $paths | Sort-Object -Unique

if (-not $uniquePaths -or $uniquePaths.Count -eq 0) {
  Fail "No candidate file paths discovered in canon/CANON_MANIFEST.json. If expected, adjust extraction rules."
}

Ok ("Discovered {0} candidate path(s) in manifest" -f $uniquePaths.Count)

$missing = @()
foreach ($p in $uniquePaths) {
  $full = Join-Path $RepoRoot $p
  if (-not (Test-Path $full)) { $missing += $p }
}

if ($missing.Count -gt 0) {
  Write-Host "Missing paths referenced by manifest:" -ForegroundColor Yellow
  $missing | ForEach-Object { Write-Host " - $_" }
  Fail ("{0} manifest-referenced path(s) are missing." -f $missing.Count)
}

Ok "All manifest-referenced paths exist"

Write-Host ""
Write-Host "PASS: QuickSmoke completed successfully" -ForegroundColor Green
exit 0
