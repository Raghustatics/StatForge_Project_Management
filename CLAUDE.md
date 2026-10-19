@AGENTS.md

# Claude Code specifics

- **Start of every session:**
  - read `docs/GATE_LOG.md` to find the active gate
  - run `/gate-kickoff` before any work on a new gate
- **Plan Mode:** use it (Shift+Tab) for every gate kick-off and any multi-file change; exit only after the owner says "go".
- **Skills:** invoke the skills named in AGENTS.md §4–§5 with the Skill tool. If a skill is not installed, follow the Fallback column and say so in your report.
- **Subagents:** use the agents in `.claude/agents/` for independent review. The agent that wrote the code never reviews it.
- **Parallel work:** only for independent tasks inside the active gate (`superpowers:dispatching-parallel-agents`, git worktrees).
- **Permissions:**
  - never run destructive commands (`rm -rf`, `git reset --hard`, `git push --force`, `docker system prune`) without explicit owner approval
  - never touch `sources/` or `C:\Users\60073\Python\Project_Management`
- **Gate status:** never write PASS in `docs/GATE_LOG.md`; only the owner does.
- **Memory:** put durable project facts in `docs/` (DECISIONS, PORTING, RISKS), not in chat history.
