---
name: resume-work
description: Start-of-session briefing for FirstFifty. Reads docs/STATUS.md, the current roadmap phase, open decisions and the git state, then tells Sayandip where things stand and starts the next task. Use at the start of every session and after any context reset.
---

Get oriented before doing anything else.

1. Read `docs/STATUS.md`, the current phase in `docs/ROADMAP.md`, `docs/decisions/README.md`, and the newest file in `docs/phase-reports/` if there is one.
2. Check the repo: `git status --short`, `git log --oneline -10`, the current branch, and open pull requests (`gh pr list`, if the GitHub CLI is signed in). If the folder is not a git repo yet, the first task is `git init` (Phase 0).
3. Look at "Waiting on Sayandip" in STATUS. Ask him only about the items the next task needs, with exact steps.
4. Reply to Sayandip in at most 8 lines: the phase and progress, what happened last, the next 3 tasks, and what you need from him (one line each).
5. Start the first task unless he redirects you.
