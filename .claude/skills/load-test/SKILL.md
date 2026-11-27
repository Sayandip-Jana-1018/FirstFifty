---
name: load-test
description: Run a FirstFifty k6 load-test scenario against local or staging, compare the results with the SLO table, and record them in docs/perf/. Use at phase gates, before launches and after performance-sensitive changes.
argument-hint: "[scenario] [local|staging]"
---

Scenario and target: $ARGUMENTS (default: search-mix against staging).

1. Read the SLO table and scenario list in `docs/engineering/QUALITY.md` and open `tools/loadtest/<scenario>.js`.
2. Never target production unless Sayandip approved it explicitly in this session.
3. Run k6 in Docker. In Git Bash on Windows, stop path mangling: `MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W)/tools/loadtest:/scripts" grafana/k6 run /scripts/<scenario>.js -e BASE_URL=<target>`. Encode the SLOs as k6 thresholds so a breach fails the run.
4. Capture p50, p95 and p99 latency per endpoint, throughput and error rate, plus resource graphs from Grafana for the same window.
5. Write `docs/perf/<YYYY-MM-DD>-<scenario>.md`: commit SHA, environment, data size, results against the SLOs, graphs or links, findings, follow-ups.
6. If an SLO fails, add a task to STATUS with the suspected cause, and investigate with the architect or backend-engineer agents.
