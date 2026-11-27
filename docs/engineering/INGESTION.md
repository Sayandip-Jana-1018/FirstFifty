# Ingestion engine

The heart of the product: a fresh, deduplicated, honest index of tech jobs in India from official sources only. The Python scanner in `reference/job-hunt-engine/` is the working prototype (about 13,500 postings per run from 120+ boards); this module is its production successor.

## Service levels
| Measure | Target |
|---|---|
| Tier-A sources polled | every 10-15 min |
| Tier-B sources polled | every 30-60 min |
| Quiet sources (no change in 7 days) | every 3-6 h |
| New posting searchable after the first poll that sees it | p95 under 2 min |
| End-to-end freshness, tier A | 95% of new postings searchable within 15 min of appearing at the source |
| Daily source success rate | at least 98% |
| Duplicate rate (hand-checked sample) | under 1% |
| False mass closures | 0 |

## Sources (from the scanner)
| ATS or source | Endpoint pattern | Notes |
|---|---|---|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/{slug}/jobs` and `/jobs/{id}` | public JSON; detail call for the description |
| Lever | `api.lever.co/v0/postings/{slug}?mode=json` | public JSON |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true` | often includes pay |
| SmartRecruiters | `api.smartrecruiters.com/v1/companies/{slug}/postings?country=in` | detail endpoint per posting |
| Workday | POST `https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs` | throttles hard (429): circuit breaker per tenant and a global Workday budget |
| Oracle HCM | `recruitingCEJobRequisitions` REST | host per tenant |
| Amazon | `amazon.jobs/en/search.json` | filter by country and category |
| Microsoft | `apply.careers.microsoft.com/api/pcsx/search` | throttles; polite intervals |
| Google | careers search page (HTML) | parse defensively; honour robots.txt |
| Atlassian | `/endpoint/careers/listings` | JSON |
| Workable | `apply.workable.com/api/v1/widget/accounts/{slug}` | JSON |
| Recruitee | `{slug}.recruitee.com/api/offers/` | JSON |

Never LinkedIn, Naukri, Indeed, Glassdoor, or anything behind a login or forbidden by robots.txt or terms.

## Connector contract
```java
public interface SourceConnector {
  AtsType type();
  Listing list(SourceRef source, FetchContext ctx);   // every open posting, summary level
  Optional<PostingDetail> detail(SourceRef source, String externalId, FetchContext ctx);
}
```
`FetchContext` carries the per-host rate-limited HTTP client, conditional-request state (ETag, Last-Modified), the deadline and a metrics recorder. Connectors only translate: no scheduling, persistence or retries of their own.

## Pipeline
1. **Schedule:** one recurring db-scheduler task per source; interval from tier and recent activity; ±20% jitter; exponential backoff after failures; at most 1-2 concurrent requests per host; a global limit (virtual threads plus a semaphore, starting at 64).
2. **List:** conditional GET where supported; a 304 ends the run cheaply.
3. **Diff:** external ids against open jobs for the source: new, changed (content hash), missing.
4. **Detail:** fetch only new or changed postings; cache by content hash.
5. **Normalise** (below).
6. **Classify:** India relevance, role family, seniority, tech or non-tech.
7. **Dedup** (below).
8. **Upsert** the canonical job and its `job_events`; store the raw payload; publish `JobUpserted` through the outbox.
9. **Close:** missing from 2 consecutive successful listings, or a detail 404, closes the job, unless the listing looks broken (safety rails).

## Normalisation (ported from jobscan.py, then extended)
- **Title:** strip decorations and extra whitespace; keep a normalised form for search and dedup (`title_norm`).
- **Seniority and fit:** the scanner's regexes (senior, intern, new grad, non-tech titles) become rule tables with unit tests built from real titles; years asked parsed from descriptions into `min_years`.
- **Location:** city alias table (Bengaluru/Bangalore/BLR, Gurugram/Gurgaon, Delhi NCR, Noida, Mumbai/Bombay, Chennai/Madras, Kolkata/Calcutta, Hyderabad, Pune ...), "India - Remote", multi-location postings.
- **Skills:** a dictionary of about 500 skills with aliases (k8s to Kubernetes, Postgres to PostgreSQL), matched on word boundaries.
- **Salary:** only when the source states it (Ashby compensation, explicit LPA or currency ranges); never inferred.
- **Employment and remote type:** structured fields first, text second.

## Deduplication
- **Exact:** unique (`source_id`, `external_id`).
- **Cross-source** (the same role on two systems): candidates share company and normalised city; compare SimHash of `title_norm` + company + the first 1,000 characters of the description; Hamming distance 3 or less merges them into one canonical job that keeps both sources.
- **Reposts:** a closed job reappearing with the same canonical key within 30 days reopens rather than duplicating.
- A weekly hand-check of 200 random jobs; the duplicate rate goes in the phase report.

## Safety rails
- A source returning zero jobs, or under 30% of its usual count, never closes jobs on the first occurrence; it needs a confirming second run and is flagged for review.
- Schema validation on every response; an unexpected shape fails that source's run only.
- Per-host and per-ATS budgets; `Retry-After` honoured; a 429 opens the circuit with backoff.
- The User-Agent names the product and a contact URL (never a personal email).
- robots.txt fetched and cached for HTML sources.

## Discovery
- Phase 1: seed about 150 companies from `reference/job-hunt-engine/companies.json`.
- Then: verify ATS slugs for companies from funding news, curated lists and user suggestions. Every new source passes admin approval with an official-domain check (the company's careers page links to that board).
- Target 1,000+ companies by Phase 5, prioritised by hiring volume in India.

## Legal and ethics
Official public endpoints only. We show our summary, structured facts and a link to the official posting. Full descriptions are stored privately for 30 days, only for matching and reprocessing. Companies can opt out or request takedown by email, and we stop polling on request.

## Porting map from the scanner
| jobscan.py | Java |
|---|---|
| `s_greenhouse`, `d_greenhouse` | `GreenhouseConnector` |
| `s_lever` | `LeverConnector` |
| `s_ashby` | `AshbyConnector` |
| `s_smartrecruiters`, `d_smartrecruiters` | `SmartRecruitersConnector` |
| `s_workday`, `d_workday`, the `WD_STATE` circuit breaker | `WorkdayConnector` with a Resilience4j breaker per tenant |
| `s_amazon`, `s_microsoft`, `s_atlassian`, `s_google`, `s_oracle` | one connector each |
| `s_workable`, `s_recruitee` | `WorkableConnector`, `RecruiteeConnector` |
| `clean`, `loc_class`, `title_ok`, `min_years` and the regexes | the `normalise` package with table-driven tests |
| `score` (Sayandip's personal ranking) | not ported; product ranking lives in search and matching |
| `companies.json` | a Flyway seed migration plus an admin import |

Port behaviour, not code: each connector gets fixtures recorded once from the live endpoint (WireMock), contract tests and a property test for its parser. `/new-connector` scaffolds all of it.

## Metrics and alerts
Per source: runs, successes, failures by reason, latency, postings listed, new, changed, closed. Global: freshness-lag histogram, queue depth, dedup merges, closure-guard trips. Alerts: a tier-A source failing for 1 hour; global success under 95% for 30 minutes; freshness lag p95 over 15 minutes.

## Admin operations
Run a source now; pause or disable it; reprocess a job from its raw payload; see the last error and a response sample.
