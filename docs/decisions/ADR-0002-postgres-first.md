# ADR-0002: PostgreSQL first; Redpanda and OpenSearch only on measured need

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
Year 1 holds at most a few hundred thousand jobs. PostgreSQL covers full-text search (weighted `tsvector`), fuzzy matching (`pg_trgm`) and vectors (pgvector), and Spring Modulith's JDBC event registry gives us an outbox. Kafka-compatible brokers and OpenSearch each need gigabytes of RAM we don't have on a 12 GB node, and add operations work.

## Decision
PostgreSQL 18 is the system of record and the v1 search engine. Redis handles caches and rate limits. Events use the event publication registry. Redpanda joins when alert fan-out p95 exceeds 60 s or ingestion lag breaks its SLO; OpenSearch joins when search p95 exceeds its budget at target load or we need features PostgreSQL can't give. Each addition needs its own ADR with the numbers.

## Consequences
- Fewer moving parts and one backup story.
- PostgreSQL needs care: indexes, autovacuum tuning, query plans in reviews.
- "Kafka" appears on the resume only if we really needed it, which is the stronger story anyway.

## Alternatives considered
- **Kafka from day one:** memory and operations cost with no load to justify it.
- **OpenSearch from day one:** at least 2-4 GB of RAM for a problem PostgreSQL already solves at our size.

## Revisit when
Any trigger above fires, measured on staging or production.
