---
name: phase-close
description: Close a FirstFifty phase. Checks every exit criterion against evidence, runs the full gates (regression, load test, security scan, design review), writes the phase report, updates the docs and asks Sayandip to sign off. Use when a phase's exit criteria look met.
---

1. Find the current phase in `docs/STATUS.md` and list its exit criteria from `docs/ROADMAP.md`.
2. Gather evidence for each criterion: test runs, dashboards, load-test files, screenshots. No evidence means not met.
3. Run the phase gates from `docs/engineering/QUALITY.md`: full regression, k6 scenarios against the SLOs (`/load-test`), a ZAP baseline scan, `/design-review` on the key screens. Ask the security-auditor and architect agents to review what changed during the phase.
4. Fix blockers, or record them as exceptions with a plan and a date.
5. Have the scribe agent write `docs/phase-reports/phase-<n>-<name>.md` from the template and update `docs/STATUS.md`, `docs/RISKS.md` and the ADR index.
6. Send Sayandip the 5-line summary, the exceptions and the next phase's first tasks, and ask him to sign off. Record his sign-off in the report.
