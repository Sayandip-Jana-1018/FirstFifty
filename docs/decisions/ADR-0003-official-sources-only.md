# ADR-0003: Official sources only; summary, facts and a link

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
Trust is the product. Big portals' terms forbid scraping, and their listings carry the very spam we promise to remove. Applicant-tracking systems such as Greenhouse publish public job-board APIs, but the job descriptions belong to the employers.

## Decision
Ingest only from companies' official hiring systems and careers pages. Never LinkedIn, Naukri, Indeed, Glassdoor or anything behind a login or forbidden by robots.txt or terms. Show our own short summary, structured facts and a link to the official posting. Store full text privately for 30 days, only for matching and reprocessing. Offer companies an opt-out and takedown path, and stop polling on request.

## Consequences
- Coverage is limited to companies whose boards we can find, so discovery is ongoing work.
- Summaries cost money, so they are generated lazily on first view and cached.
- A clear, defensible trust story for users, companies and interviewers.

## Alternatives considered
- **Scraping aggregators:** legal risk and lower quality.
- **Buying third-party job feeds:** stale, costly, and still unverified.

## Revisit when
A company offers a partner feed, or legal advice changes.
