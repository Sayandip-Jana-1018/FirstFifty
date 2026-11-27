# Risk register

Reviewed at every `/phase-close`. L = likelihood, I = impact (H/M/L).

| ID | Risk | L | I | Mitigation | Owner | Trigger to act |
|---|---|---|---|---|---|---|
| R1 | Broadridge contract restricts outside work or claims IP | M | H | Sayandip reads the clauses now; personal time and devices only; written permission if required; never Broadridge code, data or accounts | Sayandip | Before public launch at the latest |
| R2 | Sources block us or change formats | H | M | One adapter per ATS, polite rates, backoff, circuit breakers, health alerts, fixture tests, spread-out polling | ingestion-engineer | Any source under 95% success for 24 h |
| R3 | Copyright or terms complaints about job data | M | M | Our own summary + facts + link only; opt-out and takedown email; honour robots.txt and terms | product-manager | Any complaint |
| R4 | Free hosting shrinks or disappears (Oracle cut its free Arm allowance in June 2026) | H | M | Portable Terraform + k3s setup; budget for a VPS; backups stored off-provider | sre | Provider notice or capacity errors |
| R5 | Play Store review or closed-test delays | M | M | Recruit 15-20 testers early; policy checklist; account deletion and data safety ready before submission | release-manager | Rejection or tester drop-off |
| R6 | Students won't pay | H | M | A great free tier; Pro sells time and edge; the campus revenue line | product-manager | Conversion under 1% after 3 months |
| R7 | AI costs or hallucinations | M | H | Lazy summaries, caps, caching, cheap models, grounded tailoring with a validator and evals | ai-engineer | Daily spend over budget; any invented fact in evals |
| R8 | Data breach | L | H | Encryption, least privilege, security reviews, dependency scanning, an incident plan with DPDP timelines | security-auditor | Any high-severity finding |
| R9 | Founder time during the internship | H | M | Scope cuts by release; Claude batches his asks; automate everything | Claude | Two weeks with blocked items |
| R10 | Seasonality, and churn once users get hired | H | M | Alumni mode, referrals, early-career switchers as a second segment | product-manager | Monthly actives drop over 30% |
| R11 | Fast followers copy features | M | L | Speed, data quality, brand, campus relationships | Sayandip | - |
| R12 | Motion ambition hurts performance | M | H | Budgets in CI, tiered fallbacks, frame sequences instead of live 3D on low-end devices | motion-artist | A budget breach in CI |
| R13 | Payment KYC delays | M | M | Start Razorpay KYC during Phase 2 | Sayandip | KYC not done 2 weeks before Pro |
| R14 | Scope creep | H | M | PRD release cuts; product-manager owns the cut line | product-manager | A phase slipping more than a week |
| R15 | Claude usage limits slow the build | M | M | Lean context, complete agent briefs, checkpoints, cheaper models for mechanical work | Claude | Repeated limit hits in a week |
| R16 | Android developer verification goes global in 2027 | H | L | Distribute through Play (verified account); adb installs stay allowed for testing | release-manager | Google announces India dates |
