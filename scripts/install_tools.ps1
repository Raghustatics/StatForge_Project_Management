<#
.SYNOPSIS
  Install the standalone developer tools StatForge needs (AGENTS.md §8, D-026):
  gitleaks (pinned, SHA-256 verified) into $env:USERPROFILE\.local\bin, and
  pre-commit as a uv tool. Nothing is installed system-wide.
#>
$ErrorActionPreference = "Stop"
$GitleaksVersion = "8.30.1"
$BinDir = Join-Path $env:USERPROFILE ".local\bin"
New-Item -ItemType Directory -Force $BinDir | Out-Null

$exe = Join-Path $BinDir "gitleaks.exe"
$current = if (Test-Path $exe) { (& $exe version).Trim() } else { "" }
if ($current -ne $GitleaksVersion) {
    $base = "https://github.com/gitleaks/gitleaks/releases/download/v$GitleaksVersion"
    $zipName = "gitleaks_$($GitleaksVersion)_windows_x64.zip"
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("gitleaks-" + [guid]::NewGuid())
    New-Item -ItemType Directory $tmp | Out-Null
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest "$base/$zipName" -OutFile (Join-Path $tmp $zipName) -UseBasicParsing
        Invoke-WebRequest "$base/gitleaks_$($GitleaksVersion)_checksums.txt" -OutFile (Join-Path $tmp "sums.txt") -UseBasicParsing
        $expected = (Get-Content (Join-Path $tmp "sums.txt") | Where-Object { $_ -match [regex]::Escape($zipName) }).Split(" ")[0]
        $actual = (Get-FileHash (Join-Path $tmp $zipName) -Algorithm SHA256).Hash.ToLower()
        if (-not $expected -or $actual -ne $expected.ToLower()) {
            throw "gitleaks checksum mismatch (expected $expected, got $actual) - not installed"
        }
        Expand-Archive (Join-Path $tmp $zipName) -DestinationPath $tmp -Force
        Copy-Item (Join-Path $tmp "gitleaks.exe") $exe -Force
    }
    finally {
        Remove-Item -Recurse -Force $tmp
    }
}
Write-Output ("gitleaks " + (& $exe version).Trim() + " at $exe")

# uv reports progress on stderr; PowerShell 5.1 would treat that as an error under "Stop".
$ErrorActionPreference = "Continue"
& uv tool install "pre-commit>=4" 2>&1 | Out-String | Write-Output
if ($LASTEXITCODE -ne 0) {
    # A dangling tool environment (e.g. its Python was removed) blocks reinstall; clear it once.
    & uv tool uninstall pre-commit 2>&1 | Out-String | Write-Output
    & uv tool install "pre-commit>=4" 2>&1 | Out-String | Write-Output
}
if ($LASTEXITCODE -ne 0) { Write-Output "pre-commit install failed (exit $LASTEXITCODE)"; exit 1 }
Write-Output "Done. Make sure $BinDir is on your PATH."
