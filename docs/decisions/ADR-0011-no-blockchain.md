# ADR-0011: No blockchain

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
Blockchain came up as a possible trend to include. No user problem in this product needs a shared, trustless ledger; it would add cost, complexity and regulatory noise.

## Decision
No blockchain. Where we need tamper evidence (the audit log), an append-only, hash-chained PostgreSQL table does the job (the pattern from Sayandip's SalVage project).

## Consequences
Less to build and explain; the security story rests on proven controls.

## Revisit when
A concrete user problem appears that a shared ledger solves better than a database.
