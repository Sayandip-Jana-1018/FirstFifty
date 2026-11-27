# Backend conventions (Spring Boot)

## Baseline
Java 25 (LTS), Spring Boot 4.2.x, Spring Framework 7, Spring Modulith 2.x, Gradle Kotlin DSL with a version catalog and Java toolchains (foojay resolver, so the right JDK is provisioned automatically). Pin every version; Renovate or Dependabot proposes upgrades. Verify current versions with the Context7 docs tools before pinning. Never install a JDK system-wide or change JAVA_HOME on Sayandip's PC: the wrapper runs on his user JAVA_HOME (JDK 21) and the toolchain downloads JDK 25 into `~/.gradle/jdks` (CLAUDE.md, Machine facts).

## Package layout (per module)
```
<root>.<module>
  api/            the module's public surface: records, interfaces, events (the only thing other modules may use)
  web/            REST controllers, request and response DTOs, mappers
  application/    use cases, transactions, orchestration
  domain/         domain types and rules (avoid Spring imports here)
  infrastructure/ repositories (JdbcClient), HTTP clients, external adapters
```
`<root>` follows the brand's domain, decided in Phase 0. Don't create Java packages before that.

## Language and style
- Records for DTOs, events and value objects; sealed interfaces for closed hierarchies; pattern-matching switches; `var` only where the type is obvious.
- Null-safety with JSpecify (`@NullMarked` packages), checked by NullAway (run nightly if it slows PR builds too much).
- Spotless with palantir-java-format; no wildcard imports.
- No Lombok.
- Constructor injection only; no field injection; no mutable static state.

## REST API
- Base path `/api/v1`; plural nouns (`/jobs`, `/jobs/{id}`, `/me/applications`).
- JSON in camelCase; timestamps ISO-8601 UTC (`Instant`); money in paise (`long`).
- Errors as RFC 9457 problem details (`application/problem+json`) with a stable `type` URI and an `errorCode`; never stack traces.
- Jakarta Validation on DTOs; unknown enum values rejected.
- Cursor pagination (`?cursor=...&limit=...`, max 50) for feeds and search; no offset pagination on large tables.
- `Idempotency-Key` header required on POSTs that move money or send messages; responses stored for 24 h.
- `ETag` and `Cache-Control` on public reads, correct `Vary`; private data never cached at the edge.
- OpenAPI generated with springdoc (confirm Boot 4.2 support in Phase 1); the spec is a build artifact, diffed for breaking changes in CI.
- Additive changes within v1; breaking changes mean `/api/v2` plus a deprecation window, because old mobile builds stay in the wild.

## Persistence (ADR-0010)
- Flyway migrations `V<yyyyMMddHHmm>__<what>.sql`; never edit an applied migration.
- SQL-first with Spring's `JdbcClient` and records; one repository per aggregate; SQL next to its repository.
- Constraints in the database (NOT NULL, CHECK, UNIQUE, FK) as the last line of defence.
- Every hot-path query has an index and an `EXPLAIN (ANALYZE, BUFFERS)` note in its pull request.
- Short transactions that never wrap remote calls.
- Batched bulk writes; keyset pagination for scans.
- HikariCP sized to the database's cores (start at 10 connections per instance); statement timeout 2 s for API queries, longer for batch work.

## Concurrency
- Virtual threads on (`spring.threads.virtual.enabled=true`); limit concurrency with semaphores and bulkheads, not thread pools.
- No `synchronized` around blocking I/O; use `ReentrantLock` where a lock is needed.
- Background and scheduled work through db-scheduler (persistent and cluster-safe).

## Events
- Domain events are records in the publishing module's `api` package.
- Published with `ApplicationEventPublisher` inside the transaction; consumed with `@ApplicationModuleListener` (async, transactional, persisted by the event publication registry).
- Listeners are idempotent; they may run more than once.
- Incomplete publications are retried on startup and by a scheduled job; alert if any stay incomplete for over 10 minutes.

## External calls and resilience
- `RestClient` on the JDK `HttpClient` (HTTP/2; 2 s connect and 10 s read timeouts by default).
- Resilience4j per external host: circuit breaker, retry with exponential backoff and jitter (idempotent calls only), bulkhead, time limiter.
- Every external call has a timeout, a metric and a log line with the trace id.

## Caching and rate limits
- Caffeine for small per-instance caches (configuration, taxonomies); Redis for shared caches (popular feed pages, match results).
- Versioned cache keys (`v1:feed:{hash}`), short TTLs (30-120 s for feeds), event-driven invalidation where it matters.
- Bucket4j on Redis: per-IP, per-user and per-device limits on auth, search, scam check and AI endpoints; 429 responses carry `Retry-After`.

## Security in code
Spring Security, deny by default; ownership checks on every `/me/**` resource; CSRF protection for cookie sessions; strict CORS; secrets only from the environment. Details: docs/engineering/SECURITY-PRIVACY.md.

## Observability in code
- Micrometer metrics with low-cardinality tags; OpenTelemetry traces; JSON logs carrying `traceId`, `spanId`, a hashed `userId` and the module name.
- Never log personal data, tokens, resume content or payment details.
- Health groups: liveness (the process) and readiness (database, Redis); readiness turns false at the start of shutdown.

## Testing
Unit tests for domain rules; slice tests for web and repositories; Testcontainers (PostgreSQL, Redis) for integration, with reuse across a run; `ApplicationModules.verify()` and ArchUnit rules; WireMock fixtures for every external API; behaviour-describing test names (`rejectsDuplicatePostingFromSameSource`). Full strategy: docs/engineering/QUALITY.md.

## Configuration
Twelve-factor: environment variables, bound to validated `@ConfigurationProperties` records; profiles `local`, `test`, `staging`, `prod`; no secrets in `application.yml`.

## Operations
Graceful shutdown; migrations run as a separate job before rollout; database-backed feature flags (cached) for risky features.
