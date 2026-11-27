# Quality: tests, gates and budgets

"Flawless" means every change is tested at the right level, every budget is measured, and nothing ships on hope.

## Test pyramid
| Layer | Backend | Web | Mobile |
|---|---|---|---|
| Unit | JUnit 5 + AssertJ; jqwik property tests for parsers and normalisers | Vitest + Testing Library | Jest + React Native Testing Library |
| Integration | Testcontainers (PostgreSQL, Redis); WireMock for every external API | API client against a mocked API (MSW) | - |
| Contract | OpenAPI diff in CI; connector fixture tests | the generated client compiles against the spec | same |
| Architecture | `ApplicationModules.verify()`, ArchUnit | ESLint boundary rules | ESLint boundary rules |
| End to end | API smoke suite on staging | Playwright on a production build | Maestro on the emulator or phone |
| Visual | - | Playwright screenshots (both themes, animations off) | adb screenshots for review |
| Accessibility | - | axe in Playwright; manual NVDA pass per release | TalkBack pass per release |
| Performance | k6 load tests | Lighthouse CI; FPS probe for the hero | Flashlight or the profiler on a real phone |
| Security | CodeQL or Semgrep, dependency and image scans, authorisation tests | CSP check, dependency scan | dependency scan |
| Mutation (nightly) | PIT on normalisation, billing, entitlements | - | - |

Coverage: at least 80% of lines in domain and application packages; every branch in billing, entitlements, tailoring validation and the SSRF fetcher. Coverage is a floor, not the goal.

## Every pull request (CI must be green)
- Build, format check, lint, type check.
- Unit, integration and contract tests for the touched areas (keep the backend suite under 10 minutes).
- Module verification and architecture rules.
- Playwright smoke on a production build and Lighthouse CI budgets for web changes.
- gitleaks, dependency scan, Trivy on built images (no unfixed HIGH or CRITICAL).
- OpenAPI breaking-change check.

## Every phase (`/phase-close`)
- Full regression on staging, the Maestro suite on a device, a manual exploratory pass.
- k6 scenarios against the SLO table below.
- OWASP ZAP baseline; security-auditor review.
- Design-review screenshots: 3 viewports (360x800 Android, 390x844 iPhone, 1440x900 desktop) x 2 themes x reduced motion on and off.
- Docs updated; phase report written.

## Backend SLOs
| Endpoint or flow | Target |
|---|---|
| `GET /api/v1/jobs` (feed with filters) | p95 under 150 ms; p99 under 400 ms |
| `GET /api/v1/search` | p95 under 150 ms (Phase 1); under 100 ms at 500 rps (Phase 5) |
| `GET /api/v1/jobs/{id}` | p95 under 80 ms |
| Auth endpoints | p95 under 300 ms |
| Error rate under load | under 0.1% |
| Alert fan-out (new job to sent) | p95 under 60 s |

## Load-test scenarios (`tools/loadtest/`, run with the `grafana/k6` Docker image)
1. **anonymous-browse:** feed pages and job details with realistic think time.
2. **search-mix:** a recorded mix of queries and filters.
3. **signed-in-day:** feed, save, tracker moves, match explanations.
4. **launch-spike:** 10x the expected launch peak for 15 minutes.
5. **alert-fanout:** 1,000 new jobs against 50K saved searches.
6. **soak:** 2 hours at expected peak, to catch leaks.

Results go to `docs/perf/<date>-<scenario>.md` with the commit, environment, numbers and graphs.

## Chaos drills (staging; production only after launch, carefully)
Kill an API pod under load; kill Redis (the API must degrade, not die); add 300 ms of database latency; make a source return 500s, 429s and malformed JSON; restore the database from backup into a fresh namespace and time it.

## Client budgets
Web: docs/engineering/WEB.md. Mobile: docs/engineering/MOBILE.md. The hero: docs/design/MOTION-3D.md.

## Release checklist (every production release)
- Changelog written; version tagged.
- Migrations reviewed for locks and backward compatibility (expand, migrate, contract).
- Feature flags set; rollback plan written (previous image tag, flag off).
- Dashboards and alerts watched for 30 minutes after deploy.

## Bug policy
Severities and response times are in docs/WORKFLOW.md. Every P0 or P1 fix ships with a test that would have caught it.
