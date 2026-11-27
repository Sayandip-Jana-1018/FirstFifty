---
name: design-review
description: Screenshot-based design review of a FirstFifty screen or route across themes, accents, viewports and motion settings, judged against the Liquid Glass 2.0 system. Use after building or changing any visible UI.
argument-hint: "<route or screen name>"
---

Target: $ARGUMENTS

1. Make sure the app is running. Web: start the dev server or a production build and open it in the built-in browser pane. Mobile: install the latest build on the emulator or phone (`/build-apk`).
2. Capture screenshots: viewports 360x800, 390x844 and 1440x900 for web (the device screen for mobile); dark and light; the brand accent plus one other; reduced motion on; reduced transparency on; one empty and one error state if reachable. Save them in `docs/design/reviews/<date>-<target>/`.
3. Brief the product-designer agent with the screenshot paths, the relevant spec and docs/design/DESIGN-SYSTEM.md. Ask for a verdict and an issue list by severity, with fixes in token terms.
4. Fix blockers and majors (or hand them to the web-engineer or mobile-engineer), capture again, and record the outcome in a README inside the review folder.
