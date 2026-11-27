# Product analytics and experiments

## Principles
- Measure what decisions need, nothing more.
- No personal data in events, ever.
- No analytics before consent (server-side operational metrics are separate and contain no personal data).
- One definition per metric, written here.

## Tool (decided in Phase 2, with an ADR)
Default: PostHog Cloud on its free tier (events, funnels, retention, feature flags), with IP anonymisation, session replay off, and the script loaded only after analytics consent. Alternative: self-hosted Umami or Plausible for page analytics plus our own events table. Business-critical events (sign-up, apply click, subscription changes) are also sent server-side, so ad blockers don't distort the core numbers. Check current free-tier limits and terms when deciding.

## Event naming
- `object_action` in snake_case: `job_viewed`, `apply_clicked`.
- Standard properties: `platform` (web, android, ios), `app_version`, `plan` (free, pro), experiment variants.
- The user id is a hashed internal id.
- Never: email, name, phone, resume text, raw search queries, precise location.

## Core events
signup_started, signup_completed, onboarding_completed, resume_uploaded, facts_confirmed, feed_viewed, job_viewed, apply_clicked (the north-star input), job_saved, application_stage_changed, alert_created, alert_delivered (server), alert_clicked, limit_hit, upgrade_viewed, checkout_started, subscription_activated (server), subscription_cancelled (server), referral_sent, referral_converted, scam_check_run, account_deleted. Each feature's events are listed with it in docs/product/PRD.md.

## Funnels and dashboards
1. **Activation:** landing viewed, sign-up completed, onboarding completed, first job saved.
2. **North star:** weekly matched applications (apply clicks on jobs we matched) per weekly active user.
3. **Alerts:** delivered, clicked, apply clicked.
4. **Money:** limit hit, upgrade viewed, checkout started, subscription activated; monthly churn.
5. **Retention:** D1, D7 and D30 cohorts by sign-up week and channel.
Data-quality numbers (freshness, coverage, dedup) live in Grafana, not in product analytics.

## Experiments
Hypothesis, primary metric, minimum sample, at least one full week, one change at a time, behind a feature flag. Results go in `docs/experiments/<date>-<name>.md`, including failures. No dark-pattern tests.

## Attribution
UTM parameters on every campaign link; referral codes; an optional "how did you hear about us?" question in onboarding.

## Consent
Consent is recorded in the `consents` table with the notice version; withdrawing stops tracking immediately and removes the analytics identifier.
