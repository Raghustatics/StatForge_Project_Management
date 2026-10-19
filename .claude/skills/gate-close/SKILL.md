---
name: gate-close
description: Close a StatForge gate after the owner has recorded PASS: commit remaining evidence and session logs, merge the gate branch into main, tag, push to the private GitHub repo, verify CI, and log it. Use only when the owner says the gate passed or asks to close or push a gate.
---

# Gate close (after owner PASS only)

## Preconditions (stop if any fails)

- `docs/GATE_LOG.md` shows **PASS** or **PASS WITH CONDITIONS** for the gate, written by the owner. Agents never write it.
- `gh auth status` succeeds and `origin` = `https://github.com/Raghustatics/StatForge_Project_Management.git`.
- The full test suite passes on the gate branch, and `scripts/verify.ps1` is green.

## Steps

1. Write the closing session log in `docs/sessions/` (AGENTS.md §15), and update `docs/TROUBLESHOOTING.md` if needed.
2. Run gitleaks on the staged changes. Confirm nothing under `sources/Business_Cases_Examples/`, no `.env` and no dataset contents are staged.
3. Commit the remaining files: `docs(Gxx): evidence, session logs, gate close`.
4. `git switch main` then `git merge --no-ff gate/Gxx-<name> -m "gate(Gxx): PASS — <name>"`.
5. `git tag -a gate-Gxx-pass -m "Gxx passed <date>"`.
6. `git push origin main gate/Gxx-<name> gate-Gxx-pass`.
7. Wait for GitHub Actions on `main`: `gh run list --branch main --limit 1`, then `gh run watch`.
   - **Green:** record the commit SHA and CI run link in the Gate Log evidence column (`docs(Gxx): record CI link`, then push).
   - **Red:** don't touch history. Open a fix on a new branch `fix/Gxx-ci`, tell the owner, and treat it as a gate condition.
8. Delete any leftover `ci-check/Gxx-*` branches (remote and local) and note this in the session log.
9. Report to the owner: SHA, tag, CI result, and the next gate's name. Then suggest `/gate-kickoff`.

## Never

- force-push
- rebase pushed commits
- push before PASS
- push secrets, the Minitab datasets or Altius data
