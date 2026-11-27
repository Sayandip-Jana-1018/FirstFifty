# Business

## Revenue model
| Stream | Who pays | Price (starting guess; test it) | Starts |
|---|---|---|---|
| Pro | Students and freshers | ₹149/month or ₹999/year | Phase 3 |
| Campus | College placement cells | Per student per year, set during the pilot | Phase 5 pilot |
| Employers | Startups and companies | Featured posts, later per verified candidate | Year 2 |

Why this order: students bring the users, so the free tier must be genuinely great; colleges and companies pay more reliably. That is the pattern behind Unstop, Internshala and Superset (docs/research/SOURCES.md).

## Unit economics (Pro)
- Razorpay charges about 2% per payment, plus GST on the fee. Blending monthly and yearly plans, assume about ₹100 per paying user per month after fees, refunds and discounts.
- Marginal cost per Pro user: alerts (near zero), AI tailoring (capped per user per day; global cap `AI_DAILY_BUDGET_INR`), storage (tiny).
- Target conversion: 1.5-3% of monthly active users (Naukri's paying share of job seekers is about 2.6%).

## Costs, year 1
| Item | Cost |
|---|---|
| Google Play developer account | $25 once (about ₹2,100) |
| Apple Developer Program (Phase 5) | $99 a year (about ₹8,500-9,000) |
| Domain | about ₹800-1,200 a year |
| Hosting | ₹0 on Oracle's free tier if it works out (2 Arm cores and 12 GB on free-only accounts since June 2026); otherwise about ₹500-1,500 a month for a small VPS |
| AI usage (summaries and tailoring), capped | about ₹10K a year |
| Email, Telegram, push, monitoring | ₹0-1K on free tiers |
| Razorpay | No fixed fee; about 2% per payment |
| Optional: trademark, launch goodies, a used test Android phone | about ₹4.5K, ₹10-25K, ₹6-8K |

Lean total: about ₹25-35K, or up to about ₹45K if we pay for hosting. Comfortable: ₹60K-1L.

## Revenue scenarios: first 12 months after launch (estimates, not promises)
| Scenario | By month 12 | Year-1 total |
|---|---|---|
| Low | 5K sign-ups, 1.5K monthly active, about 23 paying | ₹15-25K |
| Base | 20K sign-ups, 6K monthly active, about 150 paying, maybe one campus pilot | ₹1.5-2.5L |
| High | 60K sign-ups, 20K monthly active, about 600 paying, 2-3 campus deals | ₹6-10L |

Honest expectation: ₹1-3L in year 1, which covers costs in the base case. Year 2 grows through campus and employer revenue.

## KPIs
| Area | Metric | Target |
|---|---|---|
| Data | Companies covered | 150 (Phase 1), 1,000+ (Phase 5) |
| Data | Freshness lag p95, tier-A sources | under 15 min |
| Data | Duplicate rate | under 1% |
| Growth | Sign-ups, weekly actives | phase targets in ROADMAP |
| Activation | Profile complete and one job saved in the first session | 40%+ |
| Retention | D7 / D30 | 30% / 15% to start; revise with beta data |
| North star | Weekly matched applications per active user | growing week over week |
| Revenue | Pro conversion of monthly actives | 1.5-3% |
| Revenue | Monthly Pro churn | under 8% |
| Trust | Confirmed scam jobs in our feed | 0 |

## Checkpoints (decide with data)
- 60 days after public launch: at least 1,000 active users, or a strategy review (positioning, channels, or a pivot within the space).
- 3 months after Pro launch: conversion of at least 1% of monthly actives, or rework the Pro offer.
- By July 2027: one campus pilot signed, or rethink the college channel.

## Go-to-market
1. **Pre-launch (Phases 0-2):** waitlist on the landing page; Sayandip's LinkedIn build-in-public posts (Claude drafts, he posts); the LPU beta group.
2. **Beta (Phase 2):** 50-100 LPU students, a weekly changelog, fix what hurts.
3. **Launch (Phase 4):** Play Store and web; posts in Indian developer communities (for example r/developersIndia and college groups, following each community's rules); an official, non-spammy Telegram bot; college ambassadors rewarded with Pro months.
4. **SEO (from Phase 2):** company and role pages ("SDE fresher jobs Bengaluru", "Atlassian jobs India") with live, honest data.
5. **Timing:** campus placement season runs August to December, so the product must be mature before August 2027.
6. **Campus (Phase 5):** an LPU pilot first, then 3-5 private universities.

## Legal and admin
- Operate as an individual or sole proprietor until revenue justifies a company.
- GST registration is needed only above ₹20 lakh turnover for services; check again when close.
- Policies (privacy, terms, refunds, grievance officer) go live before taking any payment.
- Sayandip reads his Broadridge contract's outside-work and IP clauses before public launch; work stays on personal time and devices.
- Trademark the name once there is traction.
