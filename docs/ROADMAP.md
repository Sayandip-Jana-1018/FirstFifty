# Roadmap

Six phases from an empty folder (24 Nov 2026) to a launched, growing product by July 2027. Dates are targets: scope moves before quality does. Every phase ends with `/phase-close`: gates, reviews, a phase report in docs/phase-reports/, and Sayandip's sign-off.

| Phase | Dates (target) | Outcome |
|---|---|---|
| 0. Foundation and proof | 25 Nov - 7 Dec 2026 | Hero motion demo approved; name chosen; repo, CI and dev stack ready |
| 1. Engine | 8 - 27 Dec 2026 | A fresh, deduplicated, searchable index of official tech jobs, with alerts |
| 2. Web V1 and private beta | 28 Dec 2026 - 10 Jan 2027 | Real students using the web app daily before the internship starts |
| 3. Android app and Pro | 11 Jan - 7 Mar 2027 | Phone app through Play's closed test; first paying users |
| 4. Public launch | 8 - 31 Mar 2027 | Open to everyone; SLOs hold through the launch spike |
| 5. Scale and grow | Apr - Jul 2027 | iOS, Chrome extension, campus pilot, ranking v2, resume-grade numbers |

From 11 Jan 2027 Sayandip is at Broadridge: Claude works whenever he opens a session, and asks of him are batched for evenings and weekends. If LPU exams fall in December, Phases 1 and 2 shift by the exam weeks; the 10 Jan beta is the date to protect.

## Phase 0: Foundation and proof (25 Nov - 7 Dec 2026)
**Goal:** prove the visual bar first, then set up everything so the build is fast and safe.

Must:
- 0.1 **Git first:** `git init`, first commit of this plan, private GitHub repo under the codename (renaming a repo later is easy; renaming code packages is not, so the monorepo scaffold waits for the name).
- 0.2 **Hero motion demo** in `prototypes/hero-demo` (Vite + React + React Three Fiber + GSAP): the "signal from noise" scroll story in docs/design/MOTION-3D.md, with Blender-made assets, meeting the budgets there, with reduced-motion and low-end fallbacks. Shown to Sayandip in the browser next to 2-3 of the reference sites he liked.
- 0.3 **Naming workshop** (docs/design/BRAND.md): 10 candidates, then a shortlist of 3 with domain availability, IP India trademark search, Play Store and App Store name checks and social handles. Sayandip picks; ADR; he buys the domain.
- 0.4 **Hosting decision** (ADR-0006): Sayandip tries Oracle Cloud in Hyderabad or Mumbai and reports the limits the console shows; Claude compares with student credits and a small VPS and recommends; he decides.
- 0.5 **Monorepo scaffold** (after the name): pnpm + Turborepo, Gradle wrapper, EditorConfig, Prettier, ESLint, Spotless, lefthook (gitleaks and formatters), PR template, Renovate or Dependabot.
- 0.6 **CI skeleton** on GitHub Actions: web, backend and mobile placeholders that build and test; required checks on `main`.
- 0.7 **Local dev stack:** `infra/docker/compose.yaml` with PostgreSQL 18 + pgvector, Redis 8 and Mailpit; one command to start, one to reset.
- 0.8 **Design archaeology:** read SplitIT (local clone at `C:\Users\Sayan\Desktop\Projects\SplitX`, read-only; ask Sayandip to add the folder) for its 16 colour themes, 5 glass kinds, WebGL glass engine and Skia glass; produce `packages/design-tokens` v1 and calibrate docs/design/DESIGN-SYSTEM.md.
- 0.9 **Backend skeleton:** Spring Boot 4.2 on Java 25 with empty Modulith modules, a health endpoint, Flyway, one Testcontainers test and a multi-arch Dockerfile, green in CI.

Exit criteria:
- Sayandip approves the demo, and it meets its budget numbers (recorded in the phase report with how they were measured).
- Name chosen and domain bought, or explicitly deferred by him.
- On his machine `pnpm install && pnpm dev` runs the web placeholder and `./gradlew bootRun` runs the backend; CI is green on `main`.
- Tokens v1 merged; ADRs recorded for name and hosting.

## Phase 1: Engine (8 - 27 Dec 2026)
**Goal:** a backend that keeps a fresh, deduplicated, searchable index of official tech jobs in India, and tells users when a match appears.

Must:
- **Ingestion** (docs/engineering/INGESTION.md): connectors for Greenhouse, Lever, Ashby, SmartRecruiters, Workday, Workable and Recruitee, plus the scanner's custom ones (Amazon, Microsoft, Google, Oracle HCM, Atlassian), ported from `reference/job-hunt-engine/jobscan.py` with fixture-based contract tests; db-scheduler; per-host politeness; Resilience4j; source health; company registry seeded from `companies.json`.
- **Normalisation and dedup:** titles, seniority, years asked, Indian city parsing, skills, employment type, remote; exact and near-duplicate detection; closure detection.
- **Catalog and search API v1:** PostgreSQL full-text + trigram + filters, keyset pagination; job detail with our structured facts and the official link.
- **Identity v1:** Google sign-in and email one-time codes; web sessions and mobile tokens.
- **Alerts v1:** saved searches delivered by Telegram and email, deduplicated, with quiet hours.
- **Admin:** source-health endpoints and a small internal page.
- **Infra:** server provisioned with Terraform, k3s, a staging namespace, WAL backups to object storage, one restore drill.
- **Observability:** metrics, traces, JSON logs, dashboards, alerts to Sayandip's Telegram.
- **Load-test baseline** with k6.

Exit criteria:
- At least 150 companies ingesting; at least 98% source success over 72 hours; freshness SLO met for tier-A sources.
- Duplicate rate under 1% on a hand-checked sample of 200 jobs.
- Search p95 under 150 ms at 200 requests/s on staging, with zero errors.
- Restore drill done, with the measured recovery time recorded.
- Security review: no open high-severity findings.

## Phase 2: Web V1 and private beta (28 Dec 2026 - 10 Jan 2027)
**Goal:** real students use it daily before the internship starts.

Must:
- Landing page with the production version of the scroll story; pricing page (Pro waitlist); privacy, terms, refund and grievance-contact pages; consent banner.
- App: onboarding (profile, preferences, resume upload parsed into a fact bank the user confirms), feed with filters and freshness badges, job detail, save, tracker (kanban), match score v1 with missing skills, alert settings, privacy centre (export, delete).
- SEO: company and role pages rendered on the server; sitemap.
- Production deploy behind Cloudflare, uptime checks, error tracking, analytics that respect consent.
- Private beta: 50-100 LPU students through a Telegram group; feedback form; weekly changelog.

Should: dark and light modes with 4 accent themes; keyboard shortcuts on desktop.
Could: Hindi UI strings scaffolded (not translated yet).

Exit criteria:
- Web Vitals budgets met on landing and feed (Lighthouse CI and real-user data).
- 50+ weekly active beta users; activation (profile complete and one job saved) of at least 40%.
- No open P0 or P1 bugs; uptime at least 99.5% over the last 7 days.
- DPDP basics live: notice, consent, export, deletion, grievance contact.

## Phase 3: Android app and Pro (11 Jan - 7 Mar 2027)
**Goal:** a daily habit on phones, and the first revenue.

Must:
- Expo app, Android first: feed with swipeable glass cards, job detail, tracker, push alerts, Resume Studio with the ATS check, offline cache, deep links, Skia glass and the match orb, haptics.
- Grounded resume tailoring with a diff view, an eval suite and cost caps (docs/engineering/AI-MATCHING.md).
- Pro plan: Razorpay Subscriptions on the web, entitlements in the backend; ADR on in-app billing for Android.
- Play Console: store listing, data safety form, content rating, closed test with at least 12 testers for 14 days in a row. A signed APK for direct installs, and an AAB for Play.
- Redpanda only if alert fan-out or ingestion lag numbers require it (ADR with the numbers).

Exit criteria:
- Closed test completed; crash-free sessions at least 99.5%; cold start under 2.5 s on a mid-range phone.
- Payments work end to end in test mode, then live, with idempotent webhook handling proven by tests.
- Tailoring evals: zero invented facts on the 50-case golden set.

## Phase 4: Public launch (8 - 31 Mar 2027)
**Goal:** open to everyone, and survive the spike.

Must:
- Play Store production release (staged rollout); web open to all; scam check v1; referral loop.
- Launch kit: LinkedIn build-in-public posts drafted for Sayandip, Reddit and Telegram posts, a college ambassador kit, a press page.
- Readiness: load test at 10x the expected launch peak, chaos drill (kill pods, restore the database), runbooks, on-call alerts, status page.

Exit criteria:
- Launched; SLOs held through launch week without exhausting the error budget.
- Checkpoint 60 days after launch: 1,000 active users means continue as planned; fewer means a strategy review (docs/product/BUSINESS.md).

## Phase 5: Scale and grow (Apr - Jul 2027)
**Goal:** resume-grade numbers and the second revenue line.

Must:
- iOS app through TestFlight to the App Store, with Sign in with Apple.
- Chrome extension (Manifest V3) that autofills official application forms; the user presses Submit.
- Campus dashboard pilot with LPU's placement cell.
- Search ranking v2: lexical plus embeddings (pgvector) plus click feedback; OpenSearch if the numbers call for it.
- Scale: 1,000+ companies, a second node, a 99.9% availability target, a load test at 500 requests/s with p95 under 100 ms.
- Three engineering blog posts: ingestion at scale, deduplication, grounded AI.

Targets (not promises): 10K users, ₹50K monthly revenue, and measured numbers for Sayandip's resume line.

## Running through every phase
Security reviews, docs, design polish, growth experiments, cost watch and dependency updates (docs/WORKFLOW.md).
