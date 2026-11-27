# ADR-0001: Modular monolith with Spring Modulith

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
One founder, an AI engineering team, and one small server at first. Microservices would add network hops, distributed transactions, per-service deploys and tracing overhead with no benefit at our scale. But the system has clear domains (ingestion, search, alerts, billing...) and must stay changeable, and strong boundaries make a better engineering story than a big ball of code.

## Decision
One Spring Boot application split into Spring Modulith modules (listed in docs/engineering/ARCHITECTURE.md). Modules interact only through published APIs and events. `ApplicationModules.verify()` and ArchUnit rules run in CI. Events go through Spring Modulith's event publication registry (a transactional outbox in PostgreSQL).

## Consequences
- Simple deploys and local transactions; one codebase to test.
- Boundaries must be policed continuously (CI checks, architect reviews).
- Scale by replicas; heavy background work (ingestion, alert delivery) can run as separate deployments of the same image with different profiles before any service split.

## Alternatives considered
- **Microservices:** operational overhead far beyond our needs.
- **A plain monolith without enforced boundaries:** rots into coupling within months.

## Revisit when
A module needs independent scaling that profile-based worker deployments can't give, or more than about five engineers work on the code.
