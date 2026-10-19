<#
.SYNOPSIS
  Run a test command that is expected to FAIL and save its output as RED evidence
  (AGENTS.md §4.1): docs/evidence/<gate>/red/<UTC yyyyMMddTHHmmssZ>_<Tc>.txt
.EXAMPLE
  scripts/capture_red.ps1 -Tc "TC-01.2" -Command "uv run pytest apps/api/tests -q"
#>
param(
    [Parameter(Mandatory = $true)][string]$Tc,
    [Parameter(Mandatory = $true)][string]$Command
)
$ErrorActionPreference = "Continue"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$gate = (& uv run python -c "import sys, pathlib; sys.path.insert(0, 'scripts'); import tc_trace; print(tc_trace.active_gate(pathlib.Path('docs/GATE_LOG.md')))").Trim()
$stamp = (Get-Date).ToUniversalTime().ToString("yyyyMMdd'T'HHmmss'Z'")
$dir = Join-Path $root "docs/evidence/$gate/red"
New-Item -ItemType Directory -Force $dir | Out-Null
$file = Join-Path $dir "$($stamp)_$Tc.txt"

$header = "RED evidence for $Tc ($gate) at $stamp UTC`nCommand: $Command`n"
$global:LASTEXITCODE = 0
$output = & (Join-Path $PSHOME "powershell.exe") -NoProfile -Command $Command 2>&1 | Out-String
$code = $LASTEXITCODE
($header + $output + "`nExit code: $code") | Out-File -FilePath $file -Encoding utf8
Write-Output $output

if ($code -eq 0) {
    Remove-Item $file
    Write-Output "Expected a failing run for $Tc - this is not RED evidence."
    exit 1
}
Write-Output "RED evidence saved: $file"
exit 0
