# Status

_Last updated: 28 Nov 2026 by Claude (Phase 0, session 1; stopped early because Sayandip's usage limit was near)._
Update this file at every `/checkpoint`. Keep it short: it is read at the start of every session.

## Current phase
**Phase 0: Foundation and proof** (target 25 Nov - 7 Dec 2026). 0.1 done; 0.2, 0.3, 0.4 and 0.8 started.

## Done
- 24 Nov 2026: project folder created with the full plan (docs, decision records, agent team, project skills). The Python job scanner is copied to `reference/job-hunt-engine/`.
- 28 Nov 2026 (0.1): git initialised on `main`; private repo https://github.com/Sayandip-Jana-1018/FirstFifty created and pushed. `.gitattributes` added (line endings, binaries, Git LFS for `assets-src/` sources and phase evidence).
- 28 Nov 2026 (0.2): hero demo spec and asset contract: `prototypes/hero-demo/ASSET-CONTRACT.md` (who owns which files, palette, storyboard and copy, GLB/frame/poster contract, budgets). Copy fix: s1 now says "Not all of them are real"; the storyboard's "Half of them aren't real" was a claim we can't prove.
- 28 Nov 2026 (0.4): hosting research: `docs/research/HOSTING-2026-11.md`. Recommends OVH VPS-3 in Mumbai (6 vCPU / 12 GB, about ₹1,370 a month with GST), fallback Vultr 4 vCPU / 8 GB in Mumbai (about ₹3,700). **Unverified:** whether OVH sells VPS-3 in Mumbai (its own pages disagree). Check before recommending.

## In progress (stopped mid-way on 28 Nov; restart from these notes)
| Task | On disk | Restart with |
|---|---|---|
| 0.2 Hero demo: Blender assets (motion-artist) | `assets-src/hero/package.json` and lockfile (gltf-transform 4.5.1, meshoptimizer 1.2.0, sharp 0.35.5); the scripts it names are not written yet. No .blend, GLBs or renders | Re-brief a motion-artist from ASSET-CONTRACT.md: GLBs first, then the s1-s3 frame sequence, then posters and stills |
| 0.2 Hero demo: web app (motion-artist) | Nothing yet (it had only read docs and checked APIs) | Re-brief from ASSET-CONTRACT.md: Vite + React + R3F + drei + GSAP, static-first HTML, tier ladder, measurement scripts, a dev-only `review.html` beside references 4.png, 8.png and 9.png |
| 0.3 Naming workshop (growth-marketer) | Nothing yet (it was checking 31 raw candidates) | Re-brief; output `docs/design/naming/WORKSHOP.md`. Then a product-designer makes glass logo mocks for the 3 finalists (Sayandip asked for a unique name and a logo) |
| 0.8 SplitIT archaeology and token draft (product-designer) | Nothing yet | Re-brief; outputs `docs/design/SPLITIT-ARCHAEOLOGY.md` and a DTCG JSON draft in `packages/design-tokens/tokens/`. Never read SplitX's `.env*` files |

Lesson: four agents at once used the plan's limit fast. Next session run at most two at a time, hero assets and hero web first.

## Next, in order
1. Hero demo (0.2): assets and web app, a final measurement pass, then show Sayandip in the browser beside references 4, 8 and 9 for his "wow" verdict.
2. Naming workshop (0.3) and logo mocks: shortlist of 3, Sayandip decides, ADR, he buys the domain.
3. Hosting (0.4): verify OVH Mumbai, then one recommendation to Sayandip; ADR-0006 accepted or superseded.
4. Monorepo scaffold, CI, local dev stack (0.5-0.7, after the name).
5. SplitIT archaeology, then tokens v1 (0.8).
6. Backend skeleton: Spring Boot 4.2 on Java 25, green in CI (0.9).

## Notes for the next session
- Blender 5.3 has been open with the MCP add-on (enabled copy: `bl_ext.user_default.mcp`). `execute_blender_code` works and OptiX on the RTX 4050 is confirmed. The `*_for_cli` tools fail without a BLENDER_PATH environment variable, which we don't set. Run `"/c/Program Files/Blender Foundation/Blender 5.3/blender.exe" -b file.blend --python script.py` from Bash instead. Start a new file in his session only if it is unsaved and unchanged.
- The SplitX folder is granted read-only through `request_directory`. It contains a `.env` that must never be read.
- On 28 Nov Docker Desktop was running (29.4.2). No Android device is connected; none is needed before Phase 3.

## Waiting on Sayandip (from docs/SETUP.md, "Do now")
- [x] `gh auth login` (signed in as Sayandip-Jana-1018)
- [ ] Docker Desktop starts with Windows
- [ ] One Android emulator, or USB debugging on his phone (needed from Phase 3)
- [x] Blender ready with the MCP add-on (connected on 28 Nov)
- [x] GitHub Student Developer Pack: verified, benefits active until 10 Feb 2028 (GitHub Pro included)
- [ ] Cloudflare account (needed when the domain is bought)
- [ ] Expo account
- [ ] What his Broadridge contract says about outside work and IP

## Blockers
None.

## Decisions pending
| Decision | Needed by | Owner |
|---|---|---|
| Brand name (and logo) | end of Phase 0 | Sayandip (Claude shortlists) |
| Hosting provider | start of Phase 1 | Sayandip (Claude recommends; draft: OVH VPS-3 Mumbai, pending a check) |
| Email provider | Phase 1 | Claude |
| Android in-app billing approach | Phase 3 | Sayandip (Claude recommends) |

## Metrics
Fill from dashboards once things are live. Never type a number here that no test or dashboard produced.

| Metric | Value | Source | Date |
|---|---|---|---|
| Companies ingesting | - | - | - |
| Active jobs | - | - | - |
| Weekly active users | - | - | - |
