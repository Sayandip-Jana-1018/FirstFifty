# Launch checklists

## Web (Phase 2 beta, Phase 4 public)
- [ ] Domain, DNS and email authentication (SPF, DKIM, DMARC).
- [ ] Privacy policy, terms, refund and cancellation policy, grievance officer and cookie notice published and linked from every footer.
- [ ] Consent flows and the privacy centre (export, delete) tested end to end.
- [ ] Lighthouse budgets green on landing, feed and job detail; real-user Web Vitals collection on.
- [ ] Error tracking, uptime checks, dashboards and Telegram alerts live.
- [ ] Backups proven by a restore drill.
- [ ] Rate limits, Turnstile and WAF rules active.
- [ ] Load test at 10x the expected peak passed (public launch).
- [ ] Support email and an FAQ page.
- [ ] Analytics events verified, with no personal data in them.

## Google Play (Phases 3-4)
- [ ] Play Console personal account created and identity verified (Sayandip).
- [ ] Google Play App Signing on; the upload key kept safe outside the repo.
- [ ] Targets API level 36; minimal permissions (notifications), each justified.
- [ ] Store listing: name, short and full description (never "guaranteed job"), 512x512 icon, 1024x500 feature graphic, 6-8 designed phone screenshots, privacy policy URL, support email.
- [ ] Data safety form matches what the app really collects and shares.
- [ ] Content rating questionnaire; target audience 18+; ads declaration (none).
- [ ] Account deletion inside the app, plus a web URL for deletion requests.
- [ ] Closed test: at least 12 testers opted in for 14 continuous days; opt-ins tracked daily; feedback collected.
- [ ] Pre-launch report reviewed (crashes, accessibility, security warnings).
- [ ] Production release with a staged rollout (10%, 50%, 100%) while watching the crash-free rate.

## Apple App Store (Phase 5)
- [ ] Apple Developer Program (Sayandip).
- [ ] Sign in with Apple alongside Google sign-in.
- [ ] In-app account deletion.
- [ ] Privacy nutrition labels; no tracking.
- [ ] Review notes with a demo account; a TestFlight round with real users first.
- [ ] In-app payments follow the App Store rules in force at the time (check India's situation; ADR).

## Payments go-live (Phase 3)
- [ ] Razorpay KYC approved and Subscriptions enabled.
- [ ] Plans created in test mode; the full flow tested (subscribe, renew, fail, retry, cancel, refund) with webhooks.
- [ ] Webhook secret set; signature checks and idempotency tested.
- [ ] Sayandip adds the live keys and makes one small real payment, then refunds it.
- [ ] Receipts and cancellation visible; the pricing page matches what is charged.

## Chrome Web Store (Phase 5)
- [ ] Developer account; single-purpose description; minimal permissions; privacy practices disclosed; the extension never submits a form by itself.

## Launch day (Phase 4)
- [ ] Risky changes frozen 48 hours before; an on-call plan for the day.
- [ ] Posts drafted for Sayandip (LinkedIn, communities); he publishes them.
- [ ] Dashboards open, rollback rehearsed, status page ready.
