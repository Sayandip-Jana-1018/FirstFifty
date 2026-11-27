# How the team works

Claude is the whole engineering team; the agents in `.claude/agents/` are specialists Claude briefs and checks. Every session follows this operating model.

## Roles
| Hat | Agent | Owns |
|---|---|---|
| Tech lead and orchestrator | main session | plan, priorities, briefs, integration, talking to Sayandip |
| Product | product-manager | specs, acceptance criteria, scope cuts, metrics |
| Design | product-designer | flows, screens, tokens, design reviews |
| Motion | motion-artist | scroll stories, 3D, shaders, Blender assets |
| Architecture | architect | boundaries, data model, APIs, ADRs |
| Backend | backend-engineer | Spring Boot features |
| Ingestion | ingestion-engineer | connectors and the job pipeline |
| AI | ai-engineer | ranking, matching, tailoring, scam check, evals |
| Web | web-engineer | Next.js app and glass components |
| Mobile | mobile-engineer | Expo app and builds |
| Quality | qa-engineer | tests, E2E, load tests, bug triage |
| Security and privacy | security-auditor | threat models and reviews |
| Operations | sre | infra, CI/CD, deploys, observability, incidents |
| Release | release-manager | versions, changelogs, store listings, launch checklists |
| Records | scribe | STATUS, phase reports, decision log |
| Growth | growth-marketer | go-to-market, SEO content, store listing, referral loops, experiments |

## Feature lifecycle
1. **Spec** (product-manager): user story, acceptance criteria, non-goals, analytics events, an entry in docs/product/PRD.md.
2. **Design** (product-designer; motion-artist when it moves): every state (loading, empty, error, offline, success), both themes, three viewports; a motion spec if anything animates.
3. **Architecture check** (architect) when the change touches module boundaries, the schema, public APIs, security-sensitive flows or performance budgets. ADR if it is expensive to reverse.
4. **Build** (an engineer agent or the main session): tests first for logic, small commits, a feature flag if risky.
5. **Quality gate** (`/quality-gate`): everything in docs/engineering/QUALITY.md for the touched areas.
6. **Reviews:** qa-engineer for test depth; security-auditor for auth, payments, uploads, personal data, URL fetching and admin; product-designer for anything visible (`/design-review`); architect for boundaries and schema.
7. **Merge, release, measure:** squash-merge, deploy, watch the dashboards, compare with the spec's metric.
8. **Record** (`/checkpoint`): STATUS, decisions, follow-ups.

## Definition of ready
Acceptance criteria written; designs cover every state; API contract sketched; analytics events named; risks noted; needed keys and accounts available, or the task is marked blocked in STATUS with the reason.

## Definition of done
- Code, tests and docs land in the same change.
- `/quality-gate` green; no new warnings in the touched modules.
- Accessible: WCAG 2.2 AA checks pass; keyboard and screen-reader paths tried.
- Within performance budgets.
- Security checklist done for sensitive areas.
- Telemetry in place: metrics, logs, traces, product events.
- STATUS updated.

## Git
- Trunk-based; `main` is always deployable.
- Short-lived branches: `feat/...`, `fix/...`, `chore/...`, `docs/...`, `exp/...`.
- Conventional Commits, for example `feat(ingestion): add Ashby connector`. End commit messages with the attribution lines the harness specifies.
- Pull requests even when working solo: CI is the reviewer of record; squash-merge.
- Tags `vX.Y.Z` for releases; the mobile build number increments automatically (EAS).
- Never commit secrets, generated native folders, build output or large binaries (Git LFS for `assets-src/`).

## Parallel work
- Independent features can run in parallel agents, each in its own git worktree.
- Never two agents on the same files. The orchestrator integrates.
- Long research or wide code reading goes to an agent; only its conclusion comes back to the main context.

## Briefing an agent
Goal; why it matters; files and docs to read first; constraints (budgets, rules, versions); definition of done; what to return (summary, files changed, test results, open questions). One task per brief; never a vague "improve X".

## Phase gates (`/phase-close`)
1. Check every exit criterion in docs/ROADMAP.md against evidence.
2. Full regression, load test against the SLO table, ZAP baseline scan.
3. Reviews: security-auditor, product-designer (screenshots), architect (drift from ARCHITECTURE.md).
4. scribe writes the phase report from `docs/phase-reports/TEMPLATE.md` and updates STATUS and the decision index.
5. Sayandip reads the summary and signs off in chat.

## Bugs
| Severity | Meaning | Response |
|---|---|---|
| P0 | Outage, data loss or leak, payments broken | Drop everything; fix or roll back; write an incident note |
| P1 | A core flow broken for many users | Fix within a day |
| P2 | Degraded experience with a workaround | Next working session |
| P3 | Cosmetic | Batch with design polish |

Flaky tests are quarantined within a day and fixed within a week, never silently retried into green.

## Working with Sayandip
- He signs in, pays, verifies and decides; Claude does the rest (CLAUDE.md).
- One decision at a time, with a recommendation and the trade-off in a line each.
- While a phase runs, a weekly summary: shipped, numbers, next, what's needed from him.
- From 11 Jan 2027 batch his to-dos for evenings and weekends.

## Usage limits
Claude's plan has usage limits. Keep the main context lean, give agents complete briefs instead of back-and-forth, use cheaper models for mechanical work (scribe and release-manager already do), checkpoint often, and never start a big refactor at the end of a session.
