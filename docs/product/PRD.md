# Product requirements

Releases map to phases (docs/ROADMAP.md). Every feature has a user story, acceptance criteria (AC) and analytics events. The product-manager agent keeps this file current; scope changes get a line in the change log at the bottom.

## Free vs Pro (starting point; test it)
| Capability | Free | Pro (₹149/month or ₹999/year) |
|---|---|---|
| Verified feed, search, filters | Yes | Yes |
| Job detail and official apply link | Yes | Yes |
| Tracker | Up to 25 active applications | Unlimited |
| Match explanations | 3 a day | Unlimited |
| Alerts | Daily digest (Telegram, email) | Instant (Telegram, push, email) |
| ATS check | 1 a day | Unlimited |
| Tailored resumes | 1 a month | Unlimited, within fair use |
| Scam check | 3 a day | Unlimited |
| Themes | 1 accent | All accents |

## R1: Web V1 (Phases 1-2)

### F1 Verified job feed
Story: as a student, I want one feed of real tech jobs from official sources, newest first, so I apply early and never waste time on fakes.
AC:
- Every job comes from a registered official source. The card shows company, title, city or remote, experience asked, a source badge (for example "Greenhouse · official") and "first seen N min ago".
- Filters: city (Bengaluru, Hyderabad, Pune, Chennai, Delhi NCR, Mumbai, Kolkata, Remote India, Other), experience (fresher, 0-1, 1-3 years), role family (backend, frontend, full stack, mobile, DevOps/SRE/cloud, data, ML/AI, QA, security), company type (product, startup, service), posted within (1 hour, 24 hours, 7 days).
- Sort: newest, or best match when signed in.
- A job closed at the source leaves the feed within one poll cycle.
- Feed API p95 under 150 ms; infinite scroll with keyset pagination.
Events: feed_viewed, filter_changed, job_card_opened.

### F2 Job detail
Story: as a student, I want the key facts at a glance and one tap to the official application.
AC: title, company, locations, experience asked, skills, employment type, salary only if the source states it, first-seen and source-posted dates, our 2-3 line summary, structured facts, "Apply on company site" (opens the official URL), save, report a problem, similar jobs. No description text copied from the source.
Events: job_viewed, apply_clicked, job_saved, job_reported.

### F3 Search
AC: keyword search over title, company and skills with typo tolerance ("kuberentes" finds Kubernetes roles); combines with filters; p95 under 150 ms.
Events: search_performed (query length and result count only; never the raw query in analytics).

### F4 Accounts
AC: Google sign-in and email one-time code; 18+ confirmation and consent screen at sign-up; sessions survive restarts; sign out of all devices.
Events: signup_started, signup_completed (method), login.

### F5 Profile and fact bank
Story: as a student, I upload my resume once and confirm what it says, so everything else uses true facts.
AC: upload PDF or DOCX up to 5 MB; parsed into education, experience, projects, skills and achievements; the user confirms or edits each fact; preferences for cities, role families, graduation year and remote. The resume is stored encrypted; the original can be downloaded or deleted.
Events: resume_uploaded, facts_confirmed, preferences_saved.

### F6 Match score v1
AC: 0-100 per job for signed-in users with a profile; the explanation lists matched skills, missing skills, experience fit and location fit; a score is never shown without its explanation.
Events: match_explained_viewed.

### F7 Saved jobs and tracker
AC: kanban columns Saved, Applied, Online test, Interview, Offer, Rejected; drag or tap to move; notes, dates and a next-action reminder; manual entries for jobs found elsewhere.
Events: application_stage_changed.

### F8 Alerts
AC: save any search as an alert; channels Telegram (linked through our bot) and email; Free gets a daily digest, Pro gets instant alerts; quiet hours; never the same job twice to the same person; one-tap unsubscribe in every message.
Events: alert_created, alert_delivered, alert_clicked.

### F9 Privacy centre
AC: see what we store; download it (JSON); delete the account (immediate sign-out, data erased within 30 days, backups roll off within 35 days); manage consents; grievance contact.
Events: data_export_requested, account_deleted.

### F10 Landing, pricing and legal
AC: scroll-story landing that meets the budgets in docs/design/MOTION-3D.md; pricing page with honest terms; privacy policy, terms, refund and cancellation policy, grievance officer, cookie notice.

### F11 Admin console (internal)
AC: source health (last success, errors, jobs found), enable or disable a source, re-run it, hide or flag a job, user-reports queue, an audit trail of admin actions.

## R2: Android app and Pro (Phase 3)
- **F12 Android app:** feed, detail, search, tracker, alerts, profile; offline reading of the last feed and the tracker; deep links from alerts; push notifications. AC: cold start under 2.5 s and 60 fps feed scrolling on a mid-range phone.
- **F13 Resume Studio:** ATS check (keyword coverage against a job, format checks) and a tailored resume per job built only from confirmed facts, shown as a diff to accept or reject line by line, exported as a one-page PDF. AC: zero invented facts on the eval set; every line links to its source fact.
- **F14 Pro subscription:** monthly and yearly plans through Razorpay (UPI AutoPay and cards); manage and cancel in two taps; receipts; entitlements apply within seconds of payment; idempotent webhooks.
- **F15 Swipe triage (mobile):** swipe right to save, left to hide, up to open the apply page; undo.

## R3: Public launch (Phase 4)
- **F16 Scam check:** paste a link, recruiter message or email and get "looks fine", "be careful" or "likely scam", with reasons and what to do next. Never accuses a named company; findings are phrased as signals.
- **F17 Referrals:** invite friends; both get a Pro week when the friend completes a profile.
- **F18 SEO pages at scale:** company and role pages with live counts and our facts.
- **F19 Notification centre** on web and in the app.

## R4: Scale and grow (Phase 5)
- **F20 iOS app** with Sign in with Apple and native Liquid Glass on iOS 26+.
- **F21 Chrome extension:** autofills official application forms (Greenhouse, Lever, Ashby and Workday first) from confirmed facts; the user presses Submit.
- **F22 Campus dashboard:** with student consent, placement cells see anonymised activity and outcomes, push curated off-campus jobs and export reports.
- **F23 Personalised ranking v2.**
- **F24 Company prep pages:** links to official engineering blogs and interview guides; no copied content.

## Non-goals
Auto-apply, scraping LinkedIn, Naukri, Indeed or Glassdoor, republishing full job descriptions, chat or social feeds, paid placement guarantees, ads in the first year.

## Change log
- 24 Nov 2026: first version (planning session).
