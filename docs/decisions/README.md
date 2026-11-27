# Decision records (ADRs)

One file per decision that is expensive to reverse. Create one with `/adr <title>`. Never rewrite an accepted decision: supersede it with a new ADR and link both ways.

| ADR | Title | Status | Date |
|---|---|---|---|
| [0001](ADR-0001-modular-monolith.md) | Modular monolith with Spring Modulith | Accepted | 2026-11-24 |
| [0002](ADR-0002-postgres-first.md) | PostgreSQL first; Redpanda and OpenSearch only on measured need | Accepted | 2026-11-24 |
| [0003](ADR-0003-official-sources-only.md) | Official sources only; summary, facts and a link | Accepted | 2026-11-24 |
| [0004](ADR-0004-monorepo.md) | Monorepo: pnpm + Turborepo, Gradle for the backend | Accepted | 2026-11-24 |
| [0005](ADR-0005-expo-mobile.md) | Expo and React Native for mobile, Android first | Accepted | 2026-11-24 |
| [0006](ADR-0006-hosting.md) | Portable self-hosting on k3s; provider chosen in Phase 0 | Proposed | 2026-11-24 |
| [0007](ADR-0007-payments.md) | Web checkout with Razorpay; in-app billing decided later | Accepted (web) | 2026-11-24 |
| [0008](ADR-0008-motion-in-house.md) | Motion and 3D built in-house | Accepted | 2026-11-24 |
| [0009](ADR-0009-grounded-ai.md) | Grounded AI only, provider-agnostic | Accepted | 2026-11-24 |
| [0010](ADR-0010-sql-first.md) | SQL-first persistence with JdbcClient and Flyway | Accepted | 2026-11-24 |
| [0011](ADR-0011-no-blockchain.md) | No blockchain | Accepted | 2026-11-24 |

Next numbers: the brand name (Phase 0), then hosting's final choice supersedes or accepts 0006.
