# G01 — Setup Steps and Answers to the Kick-off Questions

- **Date:** 19 Oct 2026
- **Related:** AGENTS.md §4.0, §4.1, §6.3–6.5, §14, §15 · DECISIONS D-019 to D-027

## 1. Owner steps (do once, in order)

1. **Install GitHub CLI and log in, then start Docker Desktop.** In PowerShell:
   ```
   winget install GitHub.cli
   gh auth login
   ```
2. **Copy the four updated skills into place** (gate-kickoff, gate-review, gate-close, qa-engineer). In PowerShell:
   ```
   cd C:\Users\60073\Python\New_Stat_Forge_v2
   Copy-Item -Recurse -Force claude_updates\* .claude\
   Remove-Item -Recurse claude_updates
   ```
3. **Restart Claude Code** in `C:\Users\60073\Python\New_Stat_Forge_v2` and paste the reply in §2.

## 2. Reply to paste into Claude Code (answers to its G01 questions)

```
Answers to your G01 questions (see AGENTS.md §14–15 and DECISIONS D-023 to D-027):
1. Repo: use the EXISTING private repo https://github.com/Raghustatics/StatForge_Project_Management.git as origin. Do not create a new one. I have installed gh and run gh auth login.
   Push policy: never push main or the gate branch before I record PASS. Exception: temporary ci-check/G01-* branches may be pushed only to prove TC-01.4 and TC-01.9, then deleted, and noted in the session log.
2. Yes: commit sources/88_Templates/Project Phase Template v0.1.xlsx (my own material, private repo). Keep sources/Business_Cases_Examples git-ignored.
3. Yes: Node 24 LTS. DECISIONS D-026 is already logged.
4. Docker Desktop is running. Yes to uv python install 3.14 and corepack enable pnpm. Yes to pre-commit and gitleaks as uv/standalone tools, not system-wide.
Also: AGENTS.md changed (§4.0 owner scenarios, §4.1 TDD enforcement, §6.3–6.5 skills/prompts, §14 Git, §15 session logs) and G01 now includes TC-01.6 to TC-01.10. Re-read AGENTS.md and the G01 gate-map section, then re-issue the updated G01 kick-off brief with the owner questionnaire. Start a session log for today.
```

## 3. What happens next

- Claude Code re-issues the G01 brief: scope, test cases TC-01.1 to TC-01.10, files, risks, the S1–S6 validation outline, and the owner questionnaire.
- You review the brief. If anything is unclear, use OWNER_PROMPTS.md #2 ("explain in business terms").
- You say "Go for G01", OWNER_PROMPTS.md #3.
- Build follows test-first order: RED tests → GREEN code → `/gate-review` with its evidence pack.
- You run your validation script (S1–S6, ≤ 45 minutes) and record PASS or FAIL in `docs/GATE_LOG.md`.
- After PASS, `/gate-close` merges, tags and pushes to GitHub, and confirms CI is green.
