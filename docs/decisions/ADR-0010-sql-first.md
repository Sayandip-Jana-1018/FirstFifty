# ADR-0010: SQL-first persistence with JdbcClient and Flyway

- Status: Accepted
- Date: 2026-11-24
- Deciders: Claude

## Context
Our hottest queries use PostgreSQL features directly: weighted full-text search, trigram similarity, pgvector, jsonb and keyset pagination. ORMs hide the SQL, invite N+1 queries and fight these features. Integration tests run against real PostgreSQL (Testcontainers), so SQL is verified anyway.

## Decision
Spring's `JdbcClient` with records for mapping, Flyway for schema, no JPA or Hibernate. Revisit jOOQ if query composition becomes complex.

## Consequences
- Explicit, fast, reviewable queries, and a good performance story.
- More mapping code to write; consistency enforced by conventions in docs/engineering/BACKEND.md.

## Alternatives considered
- **JPA/Hibernate:** convenience for CRUD at the cost of control on hot paths.
- **jOOQ:** type-safe SQL, but code generation adds build complexity we don't need yet.
- **Spring Data JDBC:** fine for simple aggregates; weaker for our query-heavy reads.

## Revisit when
Repository code grows repetitive enough that jOOQ would halve it.
