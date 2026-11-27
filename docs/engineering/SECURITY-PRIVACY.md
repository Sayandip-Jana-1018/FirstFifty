# Security and privacy

Targets: OWASP ASVS 5.0 level 2 for the API and web app; OWASP MASVS L1 for mobile; India's Digital Personal Data Protection (DPDP) Act 2023 with the DPDP Rules notified in November 2025 (the main obligations apply from about May 2027; we comply from day one).

## Threat model (summary)
| Asset | Threats | Key controls |
|---|---|---|
| Accounts and sessions | credential stuffing, session theft, CSRF | passwordless sign-in, rate limits, Turnstile on sign-up, HttpOnly cookies, CSRF tokens, refresh-token rotation with reuse detection |
| Resumes and the fact bank | breach, insider access, leaks to AI providers | envelope encryption, least privilege, AI consent, redaction, audit log |
| Payments | forged webhooks, replay, price tampering | HMAC signature checks, idempotent processing by event id, server-side amounts only |
| Scam-check URL fetching | SSRF into our network, DNS rebinding | the SSRF-safe fetcher below |
| Resume uploads | malicious files, parser exploits, decompression bombs | type sniffing, size limits, parsing in a sandboxed worker with timeouts |
| Admin console | privilege escalation | separate role, Google sign-in with 2-step verification, IP allowlist or Tailscale, every action audited |
| Ingestion | poisoned content (script injection in job text) | strip HTML to text, encode on output, CSP |
| Supply chain | malicious dependencies or CI actions | pinned versions, Renovate/Dependabot, Trivy, SBOM, signed images, actions pinned by commit SHA |

## Application controls
- Deny by default; every `/me/**` resource checks ownership, with an IDOR test for each.
- Validation at the API edge, encoding in clients; text from sources is never rendered as HTML.
- Rate limits per IP, user and device on auth, search, scam check, uploads and AI.
- Cloudflare WAF rules, and Turnstile on sign-up, email-code requests and the scam check.
- Security headers on the web (docs/engineering/WEB.md).
- Secrets only from the environment or the cluster secret store; never in code, logs or the repo (gitleaks in hooks and CI).

## SSRF-safe fetcher (scam check, link previews)
Only `http` and `https` on ports 80 and 443; resolve DNS ourselves and refuse private, loopback, link-local, multicast and cloud-metadata ranges (IPv4 and IPv6); pin the resolved IP for the connection; re-check every redirect hop (at most 3); 5 s timeout; 2 MB body cap; no cookies; a dedicated egress identity.

## Data protection
- **In transit:** TLS everywhere, including Cloudflare to origin (origin certificates).
- **At rest:** resumes encrypted with AES-256-GCM using a per-file data key, wrapped by a key-encryption key in the cluster secret store (rotatable via `kek_version`); encrypted volumes and backups.
- **Minimisation:** we never collect phone numbers, addresses, photos, government IDs, or caste or religion data.
- **Logs:** no personal data, tokens, resume text or payment details; user ids hashed.
- **Access:** production data only through audited admin paths; never copied to laptops.

## DPDP compliance checklist
- [ ] A clear notice in plain English (Hindi later): data collected, purposes, rights, how to complain.
- [ ] Consent that is free, specific, informed and itemised (core service, AI processing, marketing email, analytics), recorded with the notice version, and as easy to withdraw as to give.
- [ ] Purpose limitation and minimisation as above.
- [ ] Users 18+ only (age confirmation at sign-up); no processing of children's data.
- [ ] Rights: access (export), correction, erasure, grievance redressal and nomination, tracked in `data_requests` with deadlines.
- [ ] A grievance officer contact published on the site and in the app.
- [ ] Reasonable security safeguards (this document) and records of processing.
- [ ] Breach response: inform the Data Protection Board and affected users without delay, with a detailed report within the deadline in the Rules (72 hours at the time of writing; confirm the text when writing the incident runbook).
- [ ] Processors (hosting, email, AI, payments, analytics) bound by contracts or terms that limit their use of data; listed below.
- [ ] Retention enforced by scheduled jobs (docs/engineering/DATA-MODEL.md).
- [ ] Cross-border transfers only to countries the government has not restricted; recheck when a list is published.

## Incident response
Severities SEV1 (data leak, payments, total outage) to SEV3. Steps: contain, assess scope, preserve evidence (audit and access logs), fix, notify (users and the Board when personal data is affected), write a blameless report in `docs/incidents/`, track follow-ups. Sayandip is told immediately for SEV1 and SEV2.

## Security testing cadence
| When | What |
|---|---|
| Every pull request | CodeQL or Semgrep, dependency scan, Trivy on images, gitleaks, authorisation tests |
| Every phase close | OWASP ZAP baseline scan on staging, security-auditor review of changed areas, threat-model refresh |
| Before public launch | focused manual testing of auth, uploads, payments, admin and SSRF; all high findings fixed |

## Processors (fill in as they are chosen)
| Processor | Purpose | Data | Region |
|---|---|---|---|
| Cloudflare | CDN, WAF, DNS, storage | traffic metadata, files | global |
| Hosting provider (ADR-0006) | servers | all application data | India preferred |
| Email provider (Phase 1) | login codes, alerts | email address, message content | - |
| LLM provider (Phases 2-3) | summaries, parsing, tailoring | job text; resume text with consent, redacted | - |
| Razorpay | payments | payment data (we store ids only) | India |
| Sentry, Grafana Cloud | errors, telemetry | technical data, hashed ids | - |
