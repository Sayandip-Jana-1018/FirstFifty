# Hosting research for ADR-0006 (November 2026)

Prepared 28 Nov 2026 by the SRE agent. Every price below was read on 28 Nov 2026 unless another date is shown. Sayandip decides; this file recommends.

How prices were read: Vultr from its public plans API, Linode from its public types API, Azure from the Azure Retail Prices API, the rest from the providers' own pricing pages. Conversion rates (open.er-api.com, 27 Nov 2026): 1 USD = 92.52 INR; 1 EUR = about 101.5 INR. Prices exclude tax unless stated. Indian GST of 18% is assumed where a provider bills it; confirm at checkout.

Rule used for "facts": a number with no source note comes from the provider's own page. Estimates are labelled "estimate" and must be replaced by measurements in Phase 1 (CLAUDE.md: measure, don't claim).

---

## 1. Memory budget

What has to run (Phases 1-4): k3s (single node), PostgreSQL 18 with pgvector and pg_trgm, Redis 8, API (Java 25, virtual threads), Next.js standalone, ingestion workers, OpenTelemetry/Alloy agent, backup agent (WAL archiving), staging.

All figures are estimates from reasoning and the sources listed under the table. Two profiles:

| Component | Lean (prod only, 1 replica each) | Planned (matches ADR-0006 and INFRA-OPS.md) | Reasoning |
|---|---|---|---|
| PostgreSQL 18 + pgvector | 1.5 GB | 3.0 GB | shared_buffers about 25% of the budget; the rest is OS page cache. pgvector says HNSW indexes need not fit in memory but perform better if they do; builds are fast only if the graph fits in `maintenance_work_mem`, which must be capped so a build cannot starve the node. Halfvec or binary quantization shrink the index if needed. |
| Redis 8 | 0.25 GB | 0.5 GB | Cache only, with `maxmemory` set; the idle footprint is tiny. |
| API (JVM) | 1 x 0.9 GB | 2 x 1.0 GB | Heap capped at about 60% of the container limit, plus metaspace, code cache, thread stacks and direct buffers. Lean mode adds a transient 0.9 GB while a rollout surge pod runs. |
| Ingestion workers | 0 (runs inside the API process via db-scheduler) | 1 x 0.8 GB | Separate deployment only when ingestion load or isolation needs it (ARCHITECTURE.md stage 2). |
| Next.js standalone | 1 x 0.35 GB | 2 x 0.35 GB | Node SSR servers sit around 150-350 MB under light load. |
| k3s + Traefik + CoreDNS + metrics | 0.8 GB | 0.9 GB | k3s documents 2 CPU cores and 2 GB RAM as the minimum for a server node, for k3s and its packaged components alone. |
| OTel collector / Alloy | 0.25 GB | 0.3 GB | Metrics, traces and logs shipped to Grafana Cloud. |
| Backup agent (WAL-G or pgBackRest) | 0.1 GB | 0.2 GB | Base-backup runs add a short burst. |
| OS and kernel | 0.4 GB | 0.5 GB | |
| Staging (scaled down) | 0 (ephemeral in CI, or on the laptop) | 1.5 GB | From INFRA-OPS.md. |
| **Subtotal** | **about 4.6 GB (5.5 GB during a rollout)** | **about 10.4 GB** | |
| Headroom and page cache | 2.5 GB or more on 8 GB | 1.6 GB on 12 GB | |

Result:
- **4 GB is too small.** k3s alone needs 2 GB; Postgres and a JVM do not fit beside it.
- **8 GB is the floor**, and only in lean mode (one replica of each, no staging on the node, worker inside the API). A rolling deploy briefly needs a second API pod.
- **12 GB is the comfortable Stage 1 size**, and is what ADR-0006's memory plan assumes.
- **16 GB** gives room for Argo CD (about 0.7 GB), staging and a bigger Postgres cache. Redpanda (stage 2) and OpenSearch (stage 3) would each need a larger node or a second node.
- CPU: 4 vCPU is the practical minimum for Postgres plus two JVMs plus Node plus ingestion bursts. 2 vCPU works for the closed beta only.

Sources: k3s requirements page (docs.k3s.io/installation/requirements); pgvector README (github.com/pgvector/pgvector), which also confirms Postgres 18 support and HNSW limits (2,000 dimensions for `vector`, 4,000 for `halfvec`). Component sizes are my estimates.

---

## 2. Comparison

### 2.1 Summary table

| Option | Monthly cost (4 vCPU / 8 GB class) | Monthly cost (12-16 GB class) | CPU / RAM, arch | Region | Main risk |
|---|---|---|---|---|---|
| A. Oracle Always Free | 0 | 0 | 2 Arm OCPU / 12 GB (A1) | Hyderabad or Mumbai (home region, permanent) | Silent policy changes (already cut once); Arm capacity; idle reclaim; account termination |
| B. Azure for Students | uses the $100 credit: about $33/mo (₹3,030) for 2 vCPU / 8 GB Arm | about $65/mo (₹6,050) for 4 vCPU / 16 GB Arm | Arm B-series (burstable) | Central India | Credit lasts about 3 months or less; student eligibility ends with graduation |
| C. GitHub Student Pack hosting | n/a | n/a | n/a | n/a | DigitalOcean credit appears withdrawn; Azure is the only compute credit left |
| D1. OVHcloud VPS (Mumbai) | VPS-2 (4 vCPU / 8 GB): ₹810 ex-GST (about ₹956) | VPS-3 (6 vCPU / 12 GB): ₹1,160 ex-GST (about ₹1,369); VPS-4 (8 vCPU / 24 GB): ₹2,240 (about ₹2,643) | x86 | Mumbai (page contradicts itself, see below) | Mumbai availability per plan unconfirmed; 1 TB traffic quota then 10 Mbps; Terraform cannot order VPS |
| D2. Vultr | Cloud Compute 4 vCPU / 8 GB: $40 (₹3,700); High Performance AMD or Intel 4 vCPU / 8 GB: $48 (₹4,440) | 6 vCPU / 16 GB: $80 (₹7,400); HP 8 vCPU / 16 GB: $96 (₹8,880) | x86 | Mumbai, Bangalore, Delhi, Singapore | Price is 3-4 times the budget line; per-region price can differ in the control panel |
| D3. DigitalOcean | $48 (₹4,440) | 8 vCPU / 16 GB: $96 (₹8,880) | x86 | Bangalore | Same price tier as Vultr |
| D4. Akamai Linode | $48 (₹4,440) | 6 vCPU / 16 GB: $96 (₹8,880) | x86 | Mumbai, Chennai, Singapore | Same price tier; Mumbai at base price (the API lists a surcharge only for Jakarta) |
| D5. Hetzner Singapore | CPX32 4 vCPU / 8 GB: EUR 49.49 ex-VAT (₹5,025), 2 TB traffic | CPX42 8 vCPU / 16 GB: EUR 93.99 (₹9,540), 3 TB | x86 (AMD only in Singapore) | Singapore | Most expensive Hetzner location, lowest traffic quota, overage rate shown on the page looks wrong (EUR 7.40 per TB per hour) so treat overage as unknown |
| D6. AWS Lightsail | 4 vCPU / 8 GB (Compute Optimized): $84 (₹7,770). General Purpose 2 vCPU / 8 GB: $44 (₹4,070) | 4 vCPU / 16 GB: $84 (₹7,770) | x86 | Mumbai | Mumbai includes half the listed transfer; overage priced per GB |
| D7. Contabo | Cloud VPS 4 (4 vCPU / 8 GB): EUR 4.40 incl. VAT (₹447) | Cloud VPS 6 (12 GB): EUR 6.00 (₹609); Cloud VPS 8 (8 vCPU / 24 GB): EUR 11.20 (₹1,137) | x86, shared and oversold by design | India (Mumbai), Singapore | Page text was fragmentary, verify prices; noisy neighbours; 200 Mbit port; headline prices tied to long terms |

### 2.2 A. Oracle Cloud Always Free

- **Limits now:** 2 OCPUs and 12 GB total for Ampere A1 (1,500 OCPU-hours and 9,000 GB-hours a month), usable as one instance or two of 1 OCPU. Plus 2 AMD micro VMs (1/8 OCPU, 1 GB each), 200 GB block and boot storage, 5 volume backups, 10 TB outbound a month. Source: Oracle Always Free docs (docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm), read 28 Nov 2026. The page carries no effective date for the compute limits.
- **The June 2026 change:** InfoQ (July 2026) reports the cut from 4 OCPU / 24 GB took effect on 15 June 2026, with no Oracle announcement. Free-only accounts above the new limits had instances shut down until resized. Forum posts mention enforcement landing on 18 August 2026 and instances being administratively disabled.
- **Pay-As-You-Go:** Users report support emails saying PAYG accounts keep 4 OCPU / 24 GB at no charge. Oracle has not confirmed this and its docs do not distinguish account types (InfoQ). Oracle says upgrading does not charge for Always Free resources; only usage above the limits is billed. Treat 4/24 on PAYG as unconfirmed and do not plan on it.
- **Warning from the docs and press:** if an oversized instance is ever terminated (maintenance, outage, user error), it may be impossible to recreate it above the new limit. Forum users also report being unable to create any A1 instance in any region after terminating one.
- **Capacity:** Oracle's own docs say "out of host capacity" is a temporary shortage; try another availability domain, wait or upgrade. Forum threads show repeated A1 capacity failures in Mumbai (India West) and Hyderabad, including a July 2025 Hyderabad report and a 2023 report that Hyderabad refused Ampere instances. These are anecdotes, not measurements of current capacity. The only way to know is to try.
- **Idle reclamation:** an Always Free instance is idle if, over 7 days, the 95th-percentile CPU is below 20%, network is below 20%, and (A1 only) memory is below 20%. Our stack would hold well over 20% of 12 GB, so this is a low risk, but it is a documented rule.
- **Card for Indian users:** sign-up needs a card for verification. Forum posts show many "unable to complete sign up" failures, and Oracle staff and users cite prepaid cards, cards issued in a different country from the sign-up address, and VPN or network blocks. I found no official statement about RuPay or PIN-only debit cards; the existing ADR note that they are refused is anecdotal. Best odds: a Visa or Mastercard credit card, or a debit card with online and international payments enabled, with billing address matching the card.
- **Home region** cannot be changed, and Always Free compute must be created there.
- **Fit:** 12 GB matches the ADR memory plan, but 2 Arm cores is tight for Postgres plus two JVMs plus Node. Fine for the closed beta, not for load tests at the Phase 5 target.

### 2.3 B. Azure for Students

- **Credit:** $100, valid 12 months, not usable on Azure Marketplace offers. No credit card needed to sign up. Full-time university students only, one account per person, school email needed (azure.microsoft.com/en-us/free/students, read 28 Nov 2026).
- **Also free for new customers, 12 months:** 750 hours each of B1s, B2pts v2 and B2ats v2 VMs, 750 hours of Azure Database for PostgreSQL B1MS with 32 GB. The B2pts v2 is a small burstable Arm VM (I believe 2 vCPU / 4 GB; confirm in the portal). Useful for a staging or ops helper, not for the whole stack.
- **Central India prices (Azure Retail Prices API, Linux, pay-as-you-go, 28 Nov 2026):** B2ps_v2 (2 vCPU / 8 GB Arm) $0.0448 per hour (about $32.7 a month, ₹3,030); B4ps_v2 (4 vCPU / 16 GB Arm) $0.0896 per hour (about $65.4 a month, ₹6,050); B4as_v2 (4 vCPU / 16 GB x86) $0.0984 per hour (about $71.8 a month). Disk, public IP and egress are extra.
- **What $100 buys:** roughly 3 months of a 2 vCPU / 8 GB VM, or about 1.5 months of 4 vCPU / 16 GB, before disk and egress. It is a bridge, not a platform.
- **When credit ends:** Microsoft emails first. You can move to pay-as-you-go (and keep the free monthly amounts); otherwise the subscription and its products are disabled. Disabled means a hard stop for production, so never run production only on the credit.
- **Eligibility risk:** the offer renews while you are a student. Sayandip is a final-year student until 10 Jan 2027, so renewal or re-verification after graduation is doubtful. Do not build on it past January 2027.
- **Good use:** the monthly restore drill and load-test runs, which need a big VM for a few hours. Hourly billing makes that cheap.

### 2.4 C. GitHub Student Developer Pack (active until 10 Feb 2028)

Read from education.github.com/pack and its Cloud tag on 28 Nov 2026:
- Microsoft Azure: $100 credit, no stated duration on the pack page (see B).
- Visual Studio Dev Essentials: one year of Azure services with a $200 credit for the first month.
- Heroku: $13 a month credit for 24 months (a PaaS; does not fit a k3s plan).
- Appwrite: Education plan, 6 months, listed as a $40 a month value.
- Datadog: Pro monitoring for 10 servers, 2 years. New Relic: free while a student.
- Namecheap: free .me domain and SSL; Name.com free domain on select extensions.
- **DigitalOcean is not listed under the Cloud tag.** Secondary reports (It's FOSS, Linux Magazine, a third-party aggregator) say DigitalOcean stopped participating in 2026; other sources still showed a $200 for one year offer. I found no official notice. Treat the DigitalOcean credit as not available; Sayandip can check once at education.github.com/pack and in his DigitalOcean billing page before ruling it out.
- No pack offer provides a free always-on server big enough for this stack.

### 2.5 D. Small VPS options

Latency note: I could not measure latency to these providers reliably (my test endpoints appeared to be anycast or proxied, so the numbers were impossible and are discarded). General expectation, an estimate: Mumbai, Bangalore, Delhi and Chennai origins reach most Indian users in tens of milliseconds; Singapore adds roughly 40-70 ms more. Cloudflare caches anonymous feeds at the edge, so origin distance mostly affects signed-in API calls. Measure with a k6 run from India once a server exists.

| Provider | Plan (4 vCPU / 8 GB unless noted) | USD or local price | INR | Arch | Transfer | Backups and snapshots | Notes |
|---|---|---|---|---|---|---|---|
| OVHcloud | VPS-2 4 vCPU / 8 GB / 75 GB NVMe | ₹810 ex-GST | about ₹956 with 18% GST | x86 | Asia-Pacific VPS: 1 TB a month, then capped at 10 Mbps. The India plan cards say "unlimited", but the page says that excludes Asia-Pacific datacentres | Daily backup of the previous 24 hours included, rolling 7 days; optional premium backup; snapshot promotions | Mumbai, Singapore and Sydney are listed as APAC VPS locations; the same page also says OVHcloud has no datacentres in India. The 2023 press release announced a Mumbai datacentre, so Mumbai probably exists; confirm in the order configurator |
| OVHcloud | VPS-3 6 vCPU / 12 GB / 100 GB NVMe | ₹1,160 ex-GST | about ₹1,369 | x86 | 1 TB then 10 Mbps | same | Matches the ADR 12 GB plan; whether VPS-3 is offered in Mumbai is not confirmed |
| Vultr | Cloud Compute vc2-4c-8gb, 160 GB, 4 TB | $40 | ₹3,700 | x86 | 4 TB | Automatic backups and snapshots available (prices not read) | Mumbai, Bangalore, Delhi, Singapore. Hourly billing, official Terraform provider |
| Vultr | High Performance AMD or Intel 4 vCPU / 8 GB, 180 GB | $48 | ₹4,440 | x86 | 6 TB | same | Faster CPU than Cloud Compute |
| Vultr | vc2-6c-16gb 6 vCPU / 16 GB / 320 GB, or HP 8 vCPU / 16 GB / 350 GB | $80 or $96 | ₹7,400 or ₹8,880 | x86 | 5 TB or 8 TB | same | |
| DigitalOcean | Basic 4 vCPU / 8 GiB, 160 GiB | $48 | ₹4,440 | x86 | 5,000 GiB | Backups 20% weekly or 30% daily of the Droplet price; snapshots $0.06 per GB a month | Bangalore. No 4 vCPU / 16 GB Basic plan; 8 vCPU / 16 GiB is $96 |
| Akamai Linode | Linode 8 GB, 4 vCPU, 160 GB | $48 | ₹4,440 | x86 | 5 TB | Backup price not read | Mumbai, Chennai, Singapore. 16 GB plan has 6 vCPU for $96. Overage $0.005 per GB |
| Hetzner | CPX32 4 vCPU / 8 GB, 160 GB NVMe | EUR 49.49 ex-VAT | about ₹5,025 | x86 AMD | 2 TB in Singapore (20 TB in the EU) | Backups and snapshots available (prices not read) | Singapore is the priciest location. A CPX42 8 vCPU / 16 GB is EUR 93.99 |
| AWS Lightsail | Compute Optimized 4 vCPU / 8 GB, 320 GB | $84 | ₹7,770 | x86 | 6 TB, but Mumbai includes half | Snapshots $0.05 per GB a month | General Purpose 8 GB has only 2 vCPUs at $44. IPv6-only bundles are $1.50-4 cheaper but are a poor fit behind Cloudflare to origin |
| Contabo | Cloud VPS 4 4 vCPU / 8 GB, 100 GB SSD | EUR 4.40 incl. VAT | about ₹447 | x86 | Not stated for Cloud VPS; 200 Mbit port | Snapshots 1 included; Auto Backup add-on (price not shown) | India (Mumbai) and Singapore listed. Fragmentary page; cheapest by far, but shared and oversold; hold off for production |

Vultr prices are the list `monthly_cost` from Vultr's public plans API; Vultr says some regions may price differently, so the control panel decides. Plans for 4 vCPU / 8 GB are available in all four of its Indian and Singapore locations per the API.

### 2.6 Risks by option

| Option | Account termination | Capacity | Egress costs | Lock-in |
|---|---|---|---|---|
| Oracle | Forum reports of free accounts terminated or A1 instances disabled; policy changed silently once already | Arm often out of capacity in Mumbai and Hyderabad | 10 TB free, so low | Low (portable k3s); home region fixed |
| Azure | Disabled when credit ends; eligibility ends with studenthood | Normal | Egress is billed after the free amount | Low |
| Vultr, DO, Linode, Lightsail, Hetzner | Normal commercial accounts; fraud screening on new accounts can delay activation | Plans are on demand | Quotas large enough for our traffic (API plus a cached site) | Low |
| OVHcloud VPS | Normal | Plans stock-dependent per region | 1 TB quota then 10 Mbps cap; ample for an API behind Cloudflare, but alert on usage | VPS ordering is not Terraform-friendly (a manual order, then Terraform or Ansible takes over); confirm the current provider capability |
| Contabo | Normal | Normal | Cheap | Terraform provider exists but the platform is slower; performance variance |

---

## 3. Recommendation

**Primary: OVHcloud VPS-3 (6 vCPU / 12 GB, Mumbai), about ₹1,160 ex-GST, about ₹1,370 with GST, billed monthly with no commitment.** It is the cheapest paid option that fits the 12 GB memory plan and stays inside the ARCHITECTURE.md cost line of ₹0-1,500 a month. If Mumbai does not appear for VPS-3 in the order screen, stop and do not pick Singapore blindly; use the fallback.

**Fallback: Vultr Cloud Compute 4 vCPU / 8 GB in Mumbai, Bangalore or Delhi, $40 a month (about ₹3,700), hourly billing, official Terraform provider.** Costs about 2.7 times the primary, but gives infrastructure-as-code, snapshots, and one region choice among three Indian cities. A 6 vCPU / 16 GB plan is $80 a month if memory proves tight. Vultr is stronger on the SRE rules (IaC, hourly billing, easy teardown) than OVH; the price is the whole case for OVH.

**Free extras, not dependencies:**
1. Try creating an Oracle A1 instance (2 OCPU / 12 GB) in a Hyderabad or Mumbai account. If it works, use it for staging, the monthly restore drill and a warm spare; never for production alone, given the June 2026 policy change.
2. Use Azure for Students ($100 credit, Central India) for restore drills and load-test runs only, before January 2027.

Why not the free options as the platform: Oracle changed its terms without notice once, Arm capacity is uncertain, and its A1 rules say an instance recreated after termination may be capped lower. Azure's credit lasts about 3 months and ends with student status. Production should not sit on either.

**Cost impact:** the ₹0 line in BUSINESS.md and SETUP.md becomes about ₹1,370 a month (about ₹16,400 a year) with the primary, or about ₹3,700 a month (about ₹44,400 a year, plus GST if charged) with the fallback. Backups in Cloudflare R2 cost almost nothing at our size: the free tier is 10 GB a month, extra storage is $0.015 per GB-month, egress is free, and Class A operations cost $4.50 per million. WAL archiving makes many small writes, so watch the operation count (estimate: still under a dollar a month at launch size).

**When to revisit:** the server runs above 70% memory or CPU for a week; ingestion or load tests need more than 12 GB; OVH Mumbai proves unreliable; the 99.5% target moves to 99.9% (second node).

### Things I could not verify

- Whether OVHcloud sells VPS-3 in Mumbai today, and whether its Mumbai quota is 1 TB and then 10 Mbps (the page conflicts with itself).
- Payment methods OVH India accepts, and the actual GST line at checkout.
- Whether the Oracle PAYG 4/24 claim holds, and current A1 capacity in Hyderabad and Mumbai.
- Whether DigitalOcean's student credit still redeems.
- Contabo's exact India and Singapore prices and terms (the page text was fragmentary).
- Vultr regional price differences, backup prices, and Akamai and Hetzner backup prices.
- Latency and throughput from Sayandip's network and from real users (not measured).
- Component memory figures in section 1 are estimates until Phase 1 load tests.

---

## 4. What Sayandip does (primary: OVHcloud)

You do not need to buy anything today. Hosting is needed at the start of Phase 1. These steps cost nothing until step 4.

1. **Decide the money.** Say yes or no to about ₹1,370 a month (or ₹3,700 for the fallback).
2. **Try the free options first (optional, 20 minutes, no cost).**
   - Oracle: sign up at oracle.com/cloud/free with a Visa or Mastercard (credit card, or a debit card with online and international payments on); pick home region Hyderabad or Mumbai (permanent). In Compute, create an instance with shape VM.Standard.A1.Flex, 2 OCPU, 12 GB, Ubuntu LTS (aarch64), and paste your SSH public key. If you see "out of host capacity", try each availability domain once and tell Claude. Do not upgrade to Pay-As-You-Go without asking Claude and telling it the cost.
   - Azure for Students: sign up at azure.microsoft.com/en-us/free/students with your college email; choose Central India for any VM; set a budget alert in Cost Management.
3. **Make an SSH key** (public half only goes to the host). In Git Bash: `ssh-keygen -t ed25519 -C "firstfifty-prod"`. Claude never needs the private key. Keep it, back it up, and set a passphrase.
4. **Order the primary at the start of Phase 1.** At ovhcloud.com/en-in create an account, choose VPS-3, location Mumbai, an Ubuntu LTS image, monthly billing with no commitment, and your SSH public key. You type the card details and any OTP yourself. If Mumbai is not offered for VPS-3, stop and tell Claude; do not choose another location.
5. **Do not paste secrets in chat.** If OVH emails a root password, tell Claude only that it arrived; Claude will give the exact hardening commands (key-only login, no root password, firewall allowing only Cloudflare IPs on 80/443 and your IP for SSH).
6. **Cloudflare R2:** create a bucket (for example `firstfifty-backups`) and an API token limited to that bucket; put the token in your local `.env` as Claude names the variables. Claude will never see the values.

**Tell Claude afterwards (no secrets):**
- the provider, plan and region you ordered (and the price shown ex-GST and with GST);
- the server's public IP address;
- that SSH works with your key;
- whether the Oracle and Azure attempts worked, and any error text;
- the R2 bucket name.

Claude then writes ADR-0006 as Accepted, adds the Terraform or order notes to INFRA-OPS.md, installs k3s with a pinned version, sets up Cloudflare, Traefik and backups, and runs the first timed restore drill.

---

## Sources (read 28 Nov 2026)

- Oracle Always Free resources: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- InfoQ, Oracle free tier limits: https://infoq.com/news/2026/07/oracle-cloud-free-tier-limits/
- Linuxiac and Korben coverage of the A1 cut (secondary): linuxiac.com, korben.info
- Oracle Customer Connect and forums threads on sign-up errors and A1 capacity: community.oracle.com, forums.oracle.com
- Azure for Students: https://azure.microsoft.com/en-us/free/students
- Azure Retail Prices API: https://prices.azure.com/api/retail/prices
- GitHub Student Developer Pack: https://education.github.com/pack and https://education.github.com/pack?tag=Cloud
- DigitalOcean pricing: https://www.digitalocean.com/pricing/droplets ; student-credit reports: It's FOSS (itsfoss.com/news/digitalocean-open-source-credits-end/), Linux Magazine
- Vultr plans API: https://api.vultr.com/v2/plans
- Akamai pricing: https://www.akamai.com/cloud/pricing/cpu ; Linode API: https://api.linode.com/v4/linode/types and /v4/regions
- Hetzner: https://www.hetzner.com/cloud/regular-performance/ and https://docs.hetzner.com/cloud/general/locations/
- OVHcloud: https://www.ovhcloud.com/en-in/vps/ and https://www.ovhcloud.com/en-in/vps/vps-india/
- AWS Lightsail: https://aws.amazon.com/lightsail/pricing/
- Contabo: https://contabo.com/en/vps/ and https://contabo.com/en/locations/india
- k3s requirements: https://docs.k3s.io/installation/requirements
- pgvector: https://github.com/pgvector/pgvector
- Cloudflare R2 pricing: https://developers.cloudflare.com/r2/pricing/
- Exchange rates: https://open.er-api.com/v6/latest/USD (27 Nov 2026)
