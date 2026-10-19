# Troubleshooting Log

- Check this file before debugging.
- Add a row after any fix that took more than one attempt (AGENTS.md §15).

| Date | Gate | Symptom | Root cause | Fix | Prevention (test / check / doc) |
|---|---|---|---|---|---|
| 2026-10-19 | Setup | Remote tools can't write into `.claude/` on the owner's laptop | Protected folder for remote sessions | Files staged in `claude_setup/` or `claude_updates/`; owner copies them with PowerShell | Use the staging folder plus a copy command for any `.claude` change made from claude.ai |
| 2026-10-19 | Setup | `Get-Command` resolves npm tools to `.ps1` scripts | npm installs both `.ps1` and `.cmd` shims | None needed; if the LSP plugin reports "Executable not found", check the `.cmd` shim and PATH | `/plugin` → Errors tab check at session start |
| 2026-10-19 | Setup | `winget install GitHub.cli` fails with exit code 1602; `gh` not recognised | The installer was cancelled: the UAC admin prompt was declined, closed or timed out | Re-run and accept the UAC prompt, or use `winget install GitHub.cli --scope user`; open a new terminal so PATH refreshes | G01 kick-off verifies `gh --version` and `gh auth status` before any push |
