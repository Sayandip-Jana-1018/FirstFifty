# Infrastructure and operations

## Hosting (ADR-0006, decided in Phase 0)
| Option | For | Against |
|---|---|---|
| A. Oracle Cloud Always Free (Arm) | ₹0; Hyderabad or Mumbai regions; generous egress | Since 15 June 2026 free-only accounts get 2 OCPUs and 12 GB (was 4 and 24); Pay-As-You-Go accounts reportedly keep 4/24 free (unconfirmed by Oracle); Arm capacity is often scarce; needs a card that passes verification (PIN-only debit cards are often refused); idle free instances can be reclaimed |
| B. Azure for Students credits | Central India region; student offer without a card | credits run out; spend must be watched |
| C. A small VPS in India or Singapore | predictable, quick | about ₹500-1,500 a month |

Everything is Terraform + k3s + Helm, so moving between options takes about a day. Backups always live outside the hosting provider.

## Topology (stage 1)
```
Cloudflare (DNS, CDN, WAF, Turnstile, R2)
  -> origin: k3s on one Arm VM (Traefik ingress; Cloudflare origin certificates)
       namespaces: prod, staging, ops
       prod:    api (2 replicas), web (2 replicas), postgres (StatefulSet with pgvector), redis
       ops:     backups (WAL-G or pgBackRest), Grafana Alloy agent (ships telemetry to Grafana Cloud)
```
Memory plan for a 12 GB node: PostgreSQL 3 GB, Redis 0.5 GB, API 2 x 1.2 GB, web 2 x 0.4 GB, k3s + Traefik 0.8 GB, telemetry agent 0.3 GB, staging (scaled down) 1.5 GB, headroom about 2 GB. Argo CD (about 0.7 GB) joins when memory allows; until then GitHub Actions deploys with `helm upgrade --atomic`.

## CI/CD (GitHub Actions)
1. **Pull request:** build, test and scan (docs/engineering/QUALITY.md).
2. **Merge to `main`:** multi-arch images (linux/arm64 and amd64) with Buildx, tagged with the commit SHA, pushed to GitHub Container Registry, signed with cosign, with an SBOM; deploy to staging; run the API smoke suite.
3. **Tag `vX.Y.Z`:** promote the same image to production after manual approval; run migrations as a Job first; roll out; watch health; roll back automatically if readiness fails.

Actions pinned by commit SHA; production secrets in a GitHub environment that needs approval. If Arm builds under emulation get slow, add a self-hosted runner on the Arm VM for image builds (private repo only). Minutes budget: private repos get 2,000 free Actions minutes a month on GitHub Free (3,000 on GitHub Pro, which the Student Developer Pack includes); path filters, caching and that self-hosted runner keep us inside it.

## Secrets
Local: `.env` (gitignored, written by Sayandip). CI: GitHub encrypted secrets. Cluster: Kubernetes secrets encrypted at rest, managed with SOPS + age (keys held by Sayandip) or Sealed Secrets. Rotate on any suspicion and yearly.

## Backups and disaster recovery
- Continuous WAL archiving plus a daily base backup to Cloudflare R2 (outside the hosting provider), encrypted, kept 35 days.
- Targets: RPO 5 minutes, RTO 1 hour.
- A monthly restore drill into a scratch namespace, timed and written up; the first one in Phase 1.
- Redis is only a cache; losing it must never lose data.

## Observability
- **Metrics:** Micrometer in Prometheus format, shipped by Grafana Alloy to Grafana Cloud (free tier).
- **Traces:** OpenTelemetry from API and web; 10% sampling normally, 100% for errors.
- **Logs:** JSON to stdout, shipped to Grafana Cloud Loki.
- **Errors:** Sentry for API, web and mobile.
- **Uptime:** external checks every minute on the landing page, the API health endpoint and a synthetic search.
- **Dashboards:** API golden signals; ingestion (per-source health, freshness lag); alert pipeline; database (connections, slow queries, bloat, disk); business (sign-ups, actives, Pro).

## SLOs and paging (alerts go to Sayandip's Telegram)
| SLO | Target | Alert when |
|---|---|---|
| API availability | 99.5% a month (stage 1) | error-budget burn over 14x for 5 min, or 6x for 30 min |
| Search latency | p95 under 150 ms | p95 over 300 ms for 10 min |
| Freshness | 95% of tier-A postings within 15 min | lag p95 over 15 min for 30 min |
| Alert delivery | p95 under 60 s | oldest queued message over 5 min |
| Backups | a daily base backup exists | none for 26 h |

Error-budget policy: when a month's budget is spent, feature work pauses for reliability work.

## Runbooks (write each in `docs/runbooks/` the first time it's needed)
High error rate; latency spike; database disk filling; connection pool exhausted; a source failing en masse; webhook failures; certificate or Cloudflare problems; rolling back a deploy; restoring the database; rotating a leaked secret.

## Cost watch
A monthly line in STATUS: hosting, domain, AI spend, other. Alert at 80% of the AI budget. Prefer free tiers that allow commercial use, and read each free tier's terms before relying on it.
