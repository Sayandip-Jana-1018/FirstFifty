# ADR-0007: Web checkout with Razorpay; in-app billing decided later

- Status: Accepted for the web; Android decision in Phase 3, iOS in Phase 5
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
Razorpay charges about 2% and supports subscriptions with UPI AutoPay, which Indian students use. Digital subscriptions sold inside store apps must follow store billing rules (Google Play and Apple charge service fees; small-developer rates are about 15%), and India's competition cases around store billing were unresolved in late 2026.

## Decision
Sell Pro on the web through Razorpay Subscriptions (UPI AutoPay and cards). Entitlements live in our backend, so the apps unlock Pro for signed-in subscribers. At the start of Phase 3, choose for Android between: no in-app purchase and no steering; Google Play Billing; or Play's alternative or user-choice billing where it is available in India, after reading Play's policies in force at that time. Decide iOS the same way in Phase 5.

## Consequences
- Lower fees on the web.
- The apps must follow each store's anti-steering rules exactly.
- Webhook handling must be idempotent and verified (docs/engineering/SECURITY-PRIVACY.md).

## Alternatives considered
- **Store billing only:** higher fees on every sale and more platform lock-in.

## Revisit when
Phase 3 starts, Phase 5 starts, or store policies in India change.
