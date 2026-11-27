---
name: new-connector
description: Scaffold and test a new FirstFifty job-source connector (an ATS type or a company careers API) with recorded fixtures, contract tests and normalisation checks, following docs/engineering/INGESTION.md. Runs in the ingestion-engineer agent.
argument-hint: "<ats-type or company>"
context: fork
agent: ingestion-engineer
background: false
---

Source to add: $ARGUMENTS

1. Confirm it is an official source (the company's own ATS board or careers API) that robots.txt and the terms allow. If not, stop and report why.
2. Find the endpoint pattern (the table in docs/engineering/INGESTION.md, reference/job-hunt-engine/jobscan.py, or the ATS's public docs). Fetch one live response politely and save it as a WireMock fixture in the connector's test resources, keeping only job data.
3. Implement the `SourceConnector` (list and detail) as a pure translator and register it.
4. Tests: a contract test against the fixture; a property test for the parser; normalisation cases for its titles and locations; failure fixtures (429, 500, malformed JSON, empty list).
5. Add the source to the registry with a tier and poll interval; run it locally or on staging and watch the success rate and counts.
6. Update INGESTION.md with any quirks.

Report: files changed, test results, observed counts and success rate, quirks, follow-ups.
