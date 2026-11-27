# Reference: the job-hunt scanner (read-only)

Copied on 24 Nov 2026 from Sayandip's personal job-hunt skill (`C:\Users\Sayan\.claude\skills\job-hunt\jobhunt`). It is the working prototype of FirstFifty's ingestion engine: one run reads about 13,500 postings from 120+ official job boards.

- `jobscan.py`: source fetchers (`s_greenhouse`, `s_lever`, `s_ashby`, `s_smartrecruiters`, `s_workday` with its circuit breaker, `s_amazon`, `s_microsoft`, `s_atlassian`, `s_google`, `s_oracle`, `s_workable`, `s_recruitee`), detail fetchers, title, location and years-asked filters, and a personal ranking (`score`) that is not part of the product.
- `companies.json`: about 120 API sources with tiers, Workday tenants, a browser-check list, and skipped categories with reasons.
- `sources.md`: notes on which job platforms are worth using and why.

Its filters are tuned to Sayandip's own search (his cities, roles and pay bar). The product covers all tech roles and Indian cities, so port the behaviour, not the filters' choices (docs/engineering/INGESTION.md, "Porting map").

Don't edit these files; the live copy belongs to the job-hunt skill.
