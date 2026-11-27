# ADR-0009: Grounded AI only, provider-agnostic

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
Resume and application tools tempt users and products to inflate facts, which damages users and our reputation. LLM prices and capabilities change quickly.

## Decision
LLMs are reached only through Spring AI 2.x. Uses: lazy job summaries, resume fact extraction, grounded tailoring and scam-check explanations. Generated text about a user may only rephrase facts the user confirmed; a validator in code rejects anything ungrounded; the user approves every line. AI processing needs its own consent, and contact details are stripped before text leaves our servers. Evals run in CI; spend is capped per user and per day.

## Consequences
- Providers can be swapped by configuration.
- Eval sets have to be built and kept current.
- Marketing never claims more than the product does.

## Alternatives considered
- **Free-form AI resume writing:** fast to build, and harmful.

## Revisit when
A model or price change makes another provider better on our evals, or any eval regresses.
