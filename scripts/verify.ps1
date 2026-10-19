<#
.SYNOPSIS
  StatForge verification (AGENTS.md §4.1): lint, types, tests, traceability.
.DESCRIPTION
  -Mode Hook  fast checks, run by the Claude Code Stop hook.
  -Mode Full  adds coverage gates, build, secret scan, RED/GREEN proof, and the
              integration + e2e tests (the compose stack must be up).
  -IncludeColdStart  also runs the timed clean-pull cold start (TC-01.1).
  -Only <step>       runs just the named step(s). -List prints the step names.
  Every step prints [PASS] or [FAIL]; the script exits 1 if any step failed.
  Works in Windows PowerShell 5.1 and pwsh. Keep this file ASCII-only (PS 5.1 reads
  BOM-less files as ANSI).
#>
param(
    [ValidateSet("Hook", "Full")][string]$Mode = "Full",
    [switch]$IncludeColdStart,
    [string[]]$Only,
    [switch]$List
)
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Dash = [char]0x2014
Set-Location (Split-Path -Parent $PSScriptRoot)

function Step([string]$Name, [string]$Tool, [string[]]$Arguments) {
    [pscustomobject]@{ Name = $Name; Tool = $Tool; Arguments = $Arguments }
}

$web = @("--filter", "@statforge/web")
$steps = @(
    (Step "ruff-check" "uv" @("run", "ruff", "check", ".")),
    (Step "ruff-format" "uv" @("run", "ruff", "format", "--check", ".")),
    (Step "mypy" "uv" @("run", "mypy"))
)
if ($Mode -eq "Hook") {
    $steps += @(
        (Step "pytest" "uv" @("run", "pytest", "-q")),
        (Step "web-lint" "pnpm" ($web + "lint")),
        (Step "web-typecheck" "pnpm" ($web + "typecheck")),
        (Step "web-test" "pnpm" ($web + "test")),
        (Step "tc-trace" "uv" @("run", "python", "scripts/tc_trace.py"))
    )
}
else {
    $steps += @(
        (Step "pytest-coverage" "uv" @("run", "pytest", "-q", "--cov", "--cov-fail-under=85")),
        (Step "web-lint" "pnpm" ($web + "lint")),
        (Step "web-typecheck" "pnpm" ($web + "typecheck")),
        (Step "web-coverage" "pnpm" ($web + "test:coverage")),
        (Step "web-build" "pnpm" ($web + "build")),
        (Step "tc-trace" "uv" @("run", "python", "scripts/tc_trace.py")),
        (Step "red-green" "uv" @("run", "python", "scripts/red_green_check.py")),
        (Step "gitleaks" "gitleaks" @("git", ".", "--config", ".gitleaks.toml", "--redact", "--exit-code", "1")),
        (Step "integration" "uv" @("run", "pytest", "-q", "-m", "integration and not slow")),
        (Step "e2e" "pnpm" ($web + "e2e"))
    )
    if ($IncludeColdStart) {
        $steps += (Step "cold-start" "uv" @("run", "pytest", "-q", "-m", "slow"))
    }
}

if ($List) {
    $steps | ForEach-Object { $_.Name }
    exit 0
}

# Self-test steps exist only for scripts/tests/test_verify_ps1.py (never listed).
$selftests = @(
    (Step "tc-trace-selftest" "uv" @("run", "python", "scripts/tc_trace.py", "--help")),
    (Step "always-fail-selftest" "uv" @("run", "python", "-c", "raise SystemExit(1)"))
)
if ($Only) {
    $known = $steps + $selftests
    $unknown = $Only | Where-Object { $known.Name -notcontains $_ }
    if ($unknown) {
        Write-Output "Unknown step: $($unknown -join ', ')"
        exit 1
    }
    $steps = $known | Where-Object { $Only -contains $_.Name }
}

$failed = @()
foreach ($step in $steps) {
    if (-not (Get-Command $step.Tool -ErrorAction SilentlyContinue)) {
        Write-Output "[FAIL] $($step.Name): $($step.Tool) not found $Dash see README `"Setup`""
        $failed += $step.Name
        continue
    }
    $global:LASTEXITCODE = 0
    $stepArgs = $step.Arguments
    $output = & $step.Tool @stepArgs 2>&1 | ForEach-Object { "$_" }
    if ($LASTEXITCODE -eq 0) {
        Write-Output "[PASS] $($step.Name)"
    }
    else {
        $lines = @($output | Where-Object { $_.Trim() })
        $hint = $lines | Where-Object { $_ -match "(?i)error|fail|missing" } | Select-Object -First 1
        if (-not $hint) { $hint = $lines | Select-Object -Last 1 }
        Write-Output "[FAIL] $($step.Name): $hint"
        $lines | Select-Object -Last 15 | ForEach-Object { Write-Output "    $_" }
        $failed += $step.Name
    }
}

if ($failed.Count -gt 0) {
    Write-Output "verify: FAIL ($($failed -join ', '))"
    exit 1
}
Write-Output "verify: PASS"
exit 0
