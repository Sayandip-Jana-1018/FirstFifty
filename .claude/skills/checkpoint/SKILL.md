---
name: checkpoint
description: Save progress on FirstFifty. Runs fast checks, updates docs/STATUS.md, makes sure decisions are recorded, then commits and pushes to the private repo. Use before ending a session, before the context gets long, and after finishing a meaningful piece of work.
argument-hint: "[short note]"
---

Note from the caller: $ARGUMENTS

1. Summarise what changed since the last checkpoint (`git diff --stat`, finished tasks).
2. Run fast checks for the touched areas (`/quality-gate`, or at least build and unit tests). Never commit failing code to `main`; on a feature branch, unfinished work may be committed with a `wip:` prefix, and you say so.
3. Update `docs/STATUS.md` (use the scribe agent for big updates): dated done items, ordered next items, waiting on Sayandip, blockers, pending decisions, metrics with their sources.
4. If a decision that is expensive to reverse was made, make sure an ADR exists (`/adr`).
5. Commit with a Conventional Commit message ending with the attribution lines the harness specifies, and push the branch to the private GitHub repo (pre-approved in CLAUDE.md). Never commit secrets.
6. Tell Sayandip in 3 lines: what's saved, what's next, what you need from him.
