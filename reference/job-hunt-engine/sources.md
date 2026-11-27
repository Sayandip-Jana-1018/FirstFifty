# Where the jobs are (researched 21 Nov 2026)

Rule: platforms are for DISCOVERY. Applications go only through the employer's official careers
domain or its ATS (greenhouse.io, lever.co, ashbyhq.com, myworkdayjobs.com, smartrecruiters.com,
oraclecloud.com, amazon.jobs, careers.microsoft.com, google.com/about/careers, ...). That rule alone
removes fake jobs, recruiter scams and dead aggregator links.

## Layer 1: official job boards, scanned automatically every day (jobscan.py)
About 110 companies read straight from their hiring systems (see companies.json). Postings appear here
hours or days before they are reshared on LinkedIn or Telegram, and they are live by definition.
Verified working on 21 Nov 2026: Greenhouse (Databricks, Stripe, Rubrik, Okta, Zscaler, Pure Storage,
Coinbase, Airbnb, Glean, Anthropic, MongoDB, Datadog, Toast, Razorpay, Groww, IMC, Graviton, ...), Lever (Meesho,
CRED, Zeta, Paytm, ...), Ashby (OpenAI, Snowflake, Sarvam AI, Tekion, Atlan, ClickHouse, ...), SmartRecruiters
(ServiceNow, Arista, Wise, Grab, Swiggy, Freshworks), Amazon, Microsoft, Google, Atlassian, Oracle, JPMorgan.
Workday (NVIDIA, Salesforce, Adobe, Walmart, PayPal, Nutanix, Cohesity, ...) works but throttles this network;
the scanner backs off and the daily review covers gaps by web search.

## Layer 2: companies with no public feed, checked by the daily review
Uber, Apple, Goldman Sachs, D. E. Shaw (Hyderabad), Arcesium (Hyderabad/Bengaluru), Flipkart, PhonePe, Rippling,
Intuit, Cisco, Visa, American Express, Media.net, Confluent, Postman, Zepto, Myntra, Juspay, BrowserStack,
Dream Sports, Games24x7, Meta, LinkedIn. URLs in companies.json -> browser_check.

## Layer 3: 2027-batch aggregators (discovery only, verify on the official site)
- jobgrid.in/batch/2027
- careersat.tech/jobs/batch/2027
- freshershunt.in/off-campus-drive-jobs/
- offcampusjobs4u.com/2027-batch-off-campus-jobs/
- jobsnet.in/2027-batch
These are noisy and full of mass-recruiter roles, but they surface off-campus drives (Cisco, Qualcomm, Stripe
new-grad, Salesforce, Rubrik, ...) that are worth cross-checking.

## Layer 4: platforms that need Sayandip signed in (Claude in Chrome)
| Platform | Why it is worth it | How we use it |
|---|---|---|
| Wellfound | Funded startups, salary and equity shown upfront, founders read applications | daily search: Bengaluru/Hyderabad/remote India, entry level, salary >= 20L |
| Instahyre | Recruiters at product companies reach out; skews to higher pay | keep profile sharp, expected CTC 22L+, check invites |
| Cutshort | Startup and product roles with salary bands | profile + check matches |
| Hirist.tech | Tech-only board, cleaner than Naukri | search SDE 0-2 yrs, Bengaluru/Hyderabad |
| LinkedIn | Still the biggest index of postings | discovery only: "past 24 hours", entry level; apply on company site. No bots on LinkedIn: it bans automation |
| Naukri | Recruiters search it for inbound calls | keep profile updated weekly; do not mass-apply |
| YC Work at a Startup | Indian YC startups, direct to founders | weekly check |
| Unstop / HackerEarth | Hiring challenges and off-campus drives for the 2027 batch | weekly check for challenges from target companies |

## The channel that beats all of these: referrals
For 20+ LPA roles a referral is worth more than any portal. The daily review lists LPU alumni or people at each
shortlisted company to contact, and drafts a short referral request. Sayandip sends it himself (Claude never sends
messages on his behalf without an explicit OK).

## What to skip
Mass-application bots, "pay to apply" sites, Telegram links that go to non-official forms, anything asking for a fee,
Aadhaar/PAN or bank details before an offer letter.
