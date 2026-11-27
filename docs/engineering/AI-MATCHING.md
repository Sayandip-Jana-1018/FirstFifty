# Search, matching and AI

## Principles
- Rules and retrieval first, models second: AI only where it clearly beats something simpler.
- Grounded or nothing: generated text about a user only rephrases facts the user confirmed.
- Every model output has an eval, a cost cap and a fallback.
- Load the `claude-api` skill before implementing anything that calls an LLM. Use Spring AI 2.x so providers stay swappable.

## Search
**v1 (Phase 1):** PostgreSQL full-text search on a weighted `tsvector` (title A, company B, skills C, summary D) with `websearch_to_tsquery`, plus `pg_trgm` similarity for typos in titles and companies; filters on indexed columns; ranking = text rank x freshness decay x source quality; keyset pagination.
**v2 (Phase 5):** hybrid retrieval. Lexical candidates plus vector candidates (pgvector HNSW over 384-dimension embeddings of title + skills + summary), merged with reciprocal rank fusion, then reranked with personal signals (profile fit, clicks, saves, hides). Embeddings come from a small open model on our own CPU (ONNX Runtime in the JVM, or a small sidecar), so a query costs nothing. OpenSearch only if numbers demand it (ADR-0002).

## Matching
**v1:** score 0-100 = skills overlap (weighted by how central each skill is to the posting) + experience fit (years asked vs the user's) + location fit + role-family fit. The explanation lists matched and missing skills. Deterministic and explainable.
**v2:** add embedding similarity between the user's confirmed facts and the job; learn the weights from outcomes (saves, applies, hides) with a simple logistic model; keep the explanation.

## Job summaries (in our words)
- Generated the first time a job is viewed, then cached against the job's content hash; regenerated only when the content changes.
- Rules: 2-3 sentences, at most 60 words, plain English, no salary or benefit claims unless they are in the structured facts, no sentences copied from the source.
- The cheapest capable model, batched where possible, under a daily spend cap; on cap or error, show structured facts only.

## Resume parsing and the fact bank
- Text extraction with Apache PDFBox (PDF) and Apache POI (DOCX); scanned images rejected in v1 with a request for a text PDF.
- Rules split sections; an LLM then extracts structured facts (education, experience, projects, achievements, skills) into a strict JSON schema.
- The user confirms or edits every fact before any feature uses it. Confirmed facts are the only input to tailoring.

## Grounded tailoring (Phase 3)
1. **Select** the facts most relevant to the job (keyword overlap plus embeddings).
2. **Rewrite** them into resume lines with structured output: every line carries the ids of the facts it uses.
3. **Validate in code, not in the model:** reject any line that introduces a number, organisation, technology, date, title or claim absent from its source facts; enforce length and tone rules.
4. **Show a diff:** the user accepts or rejects line by line; nothing is saved silently.
5. **Export** a one-page PDF from an ATS-safe template (single column, standard headings, real text, visible links), the same rules as Sayandip's own resume builder.

Evals: a golden set of 50 profile-job pairs plus adversarial cases (tempting numbers in the job, missing skills). Metrics: invented-fact rate (must be 0), keyword-coverage gain, length compliance, and human preference on a sample. They run in CI whenever a prompt or model changes.

Model choice is made in Phase 3 by eval and cost: for example Claude Haiku 5.5 for drafts and Claude Sonnet 5.5 where quality needs it, or a Gemini model if it is cheaper at equal quality. Check current model ids and prices with the `claude-api` skill at that time.

## ATS check
- Keyword coverage of the job's skills and key phrases (the approach in Sayandip's resume builder).
- Format checks: one column, standard headings, no text inside images or tables, readable fonts, length, parseable contact details.
- Output: a score plus specific fixes, never a vague grade.

## Scam check (Phase 4)
Inputs: a URL, a recruiter message or an email. Signals:
- **Domain:** age via RDAP, mismatch with the company's official domains, look-alike domains (edit distance, confusable characters), free email providers posing as HR.
- **Content:** fees or deposits, "training charges", requests for Aadhaar, PAN or bank details before an offer, messaging-app-only contact, urgency, pay far above fresher market rates, offers without interviews.
- **Model:** patterns from Sayandip's ScamRadar project (its XGBoost model and signals), retrained or exported to ONNX.

Output: "looks fine", "be careful" or "likely scam", with the signals and what to do. Never states that a named company is a scam. URL fetching uses the SSRF-safe fetcher (docs/engineering/SECURITY-PRIVACY.md).

## Privacy for AI features
- Separate consent for AI processing, saying plainly that text goes to an AI provider outside India.
- Strip email addresses and phone numbers before sending text to a provider.
- Provider settings: no training on our data; minimal retention where the provider allows it.
- Logs keep token counts and latency, never content.

## Cost controls
Per-user daily limits by plan; a global daily budget (`AI_DAILY_BUDGET_INR`); caching by input hash; the cheapest model that passes evals; an alert at 80% of budget; a graceful fallback when the budget runs out.
