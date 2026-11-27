# ADR-0006: Portable self-hosting on k3s; provider chosen in Phase 0

- Status: Proposed
- Date: 2026-11-24
- Deciders: Sayandip (money), Claude (engineering)

## Context
The original plan assumed Oracle Cloud's Always Free Arm allowance of 4 OCPUs and 24 GB. On 15 June 2026 Oracle changed its documentation to 2 OCPUs and 12 GB for free-only accounts, without an announcement; support reportedly told users that Pay-As-You-Go accounts keep 4/24 at no charge, which Oracle has not confirmed (InfoQ, July 2026). Arm capacity is often scarce, and Indian users report that PIN-only debit cards fail verification. Vercel's Hobby plan forbids commercial use.

## Decision (proposed)
Run on a portable stack (Terraform, k3s, Helm) behind Cloudflare, with backups in Cloudflare R2 whatever the provider. Pick the provider in Phase 0:
1. **Oracle Cloud Always Free** in Hyderabad or Mumbai, if Sayandip can create an Arm instance (2/12 on a free account, or 4/24 if a Pay-As-You-Go upgrade really keeps it free).
2. Otherwise a **small VPS** in India or Singapore (about ₹500-1,500 a month): predictable.
3. **Azure for Students credits** (Central India) as a bridge if his student pack has them.

## Consequences
- Stage 1 is a single node, so the availability target is 99.5%; the memory plan is in docs/engineering/INFRA-OPS.md.
- Moving providers is a day's work, not a rewrite.

## Alternatives considered
- **Managed platforms (Vercel, Render, Railway):** free tiers forbid commercial use or sleep; paid tiers cost more than a VPS.
- **Kubernetes on a big cloud:** control-plane and load-balancer costs.

## Revisit when
The provider changes its terms, capacity fails, or we move to a 99.9% target (stage 4).
