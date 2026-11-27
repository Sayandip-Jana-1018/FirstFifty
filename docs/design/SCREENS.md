# Screens and flows

Information architecture for web and mobile: every screen's purpose, main components, states, motion and analytics. The product-designer agent owns this file; the product-manager keeps it in step with docs/product/PRD.md.

## Map
Mobile tabs: **Feed**, **Search**, **Tracker**, **Resume**, **Profile**. Web: a left rail with the same five, plus a detail panel on wide screens.

- **Public:** landing, pricing, company page, role page, public job detail, legal pages, waitlist.
- **Signed in:** onboarding, feed, job detail, search, saved, tracker, Resume Studio, alerts, scam check, profile and settings, privacy centre, upgrade.
- **Internal:** admin (sources, jobs, reports, audit log).

## Key flows
1. **First run:** landing, sign in (Google or email code), 18+ and consent, preferences (roles, cities, batch), resume upload (or skip), confirm facts, first feed with match scores, prompt to create an alert.
2. **Find and apply:** feed, filter, job detail, "Apply on company site" (the official page opens), return, "Did you apply?", tracker updated.
3. **Track:** tracker, drag to Online test, set a reminder, notification on the day.
4. **Tailor (Pro):** job detail, "Tailor my resume", review the diff, export PDF, apply.
5. **Alert:** search, save as alert, choose channels, link Telegram (deep link to our bot), first alert arrives, tap opens the job.
6. **Upgrade:** hit a limit or tap Pro, pricing sheet, web checkout (Razorpay), back in the app with Pro active.
7. **Delete account:** profile, privacy centre, delete, confirm, signed out, confirmation email.

## Screens
**Landing (web).** Make people feel the product in 20 seconds and join. The "Signal from noise" scroll story; live counters (jobs today, companies read; real numbers only); how it works; trust (official sources, privacy); pricing teaser; FAQ; waitlist or sign-up. States: reduced motion (posters), slow network (posters first). Events: landing_scene_reached, cta_clicked.

**Onboarding.** A profile in under 2 minutes. Glass step cards with progress, role and city chips, batch picker, resume drop zone, fact confirmation list with inline edits. Motion: the skills helix while parsing (ambient, pausable). States: parse failed (ask for a text PDF), resume skipped. Events: onboarding_step, onboarding_completed.

**Feed.** The daily habit. Sticky glass filter bar, job-card list (FlashList on mobile), freshness badges, mini match orbs, pull to refresh, a "new jobs" toast when fresh postings arrive; swipe-triage mode on mobile. States: filters too narrow (suggest widening), offline (cached list), skeletons while loading. Events: feed_viewed, job_card_opened, swipe_action.

**Job detail.** Decide in 10 seconds, apply in one tap. Header with company mark and source badge, facts grid (experience, location, type, salary if stated), our summary, match explanation (matched and missing skills), "Apply on company site", save, tailor (Pro), report, similar jobs. States: closed (banner plus similar jobs), summary pending (facts only). Events: job_viewed, apply_clicked, tailor_started.

**Search.** Typeahead for roles, companies and skills; recent searches; save as alert. Events: search_performed, alert_created.

**Tracker.** Kanban (paged columns on mobile); cards with company, role, stage date and next action; notes; reminders; manual entries. Events: application_stage_changed.

**Resume Studio.** Radial ATS meter, fix list, fact bank, tailored versions per job with diff and export; Pro gating with a clear preview. Events: ats_checked, tailored_exported.

**Alerts.** Saved searches with channels, frequency and quiet hours; Telegram link status; a "send a test alert" button.

**Scam check (Phase 4).** Paste box, verdict card with signals and advice, "report this to us". Events: scam_check_run.

**Profile, settings, privacy centre.** Preferences, theme and accent, notifications, linked accounts, consents, export data, delete account, grievance contact.

**Upgrade.** Monthly or yearly toggle, what Pro adds, honest terms, cancel anytime; checkout on the web.

**Admin (internal).** Sources table with health, run now and pause; job moderation; reports queue; audit-log viewer.

## States checklist for every screen
Loading, empty, error with retry, offline, partial data, permission denied, success; dark and light; three accents; three viewports; reduced motion; reduced transparency; long text and Hindi-length strings; screen-reader labels.
