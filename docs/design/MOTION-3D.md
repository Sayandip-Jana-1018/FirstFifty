# Motion and 3D

Motion is how this product feels expensive. It must also feel instant, stay smooth on a mid-range Android phone (think ₹15,000), and never get in the way of finding a job. The motion-artist agent owns this file.

## Three levels of motion
| Level | Where | Character |
|---|---|---|
| Cinematic | landing scroll story, onboarding intro, offer celebration | 3D scenes, scroll-scrubbed sequences, shaders |
| Expressive | match reveal, swipe triage, tracker moves, the match orb | spring physics, glass light play, short particle moments |
| Functional | navigation, sheets, toasts, list updates | fast, quiet, consistent; under 300 ms |

## Motion tokens
| Token | Value | Use |
|---|---|---|
| `duration.instant` | 100 ms | press feedback, toggles |
| `duration.quick` | 180 ms | small transitions, tooltips |
| `duration.base` | 240 ms | most UI transitions |
| `duration.slow` | 400 ms | sheets, page transitions |
| `duration.cinematic` | 800-1,600 ms | hero beats (never blocking input) |
| `ease.standard` | cubic-bezier(0.2, 0, 0, 1) | most movement |
| `ease.emphasized` | cubic-bezier(0.05, 0.7, 0.1, 1) | arrivals that should feel alive |
| `ease.exit` | cubic-bezier(0.3, 0, 1, 1) | leaving the screen |
| `spring.snappy` | stiffness 400, damping 30 | buttons, chips |
| `spring.gentle` | stiffness 170, damping 26 | cards, sheets |
| `spring.bouncy` | stiffness 260, damping 18 | celebrations only |
| `stagger.list` | 30 ms per item, at most 8 items | list entrances |

Mapped to GSAP eases, Motion springs, Reanimated `withSpring` configs and CSS variables. Calibrate the springs in Phase 0 by feel on a real phone.

## Infinite and ambient motion
Sayandip wants things that spin, roll and scroll endlessly. Allowed patterns:
- the match orb's slow rotation and drifting light;
- a slowly turning 3D ring or carousel of job cards (landing);
- a continuous marquee of company names (text, not logos, in marketing);
- a skills helix (a DNA-style spiral) during onboarding;
- ambient gradient or light-field drift behind the glass.

Rules: at most one ambient loop in view at a time on mobile, two on desktop; loops are seamless; they pause off screen, when the tab is hidden, under reduced motion, under Save-Data and on low-tier devices; anything that moves for more than 5 seconds has a visible pause control (WCAG 2.2.2); loops animate only transforms, opacity or shader uniforms.

## The hero: "Signal from noise" (landing scroll story)
About 6 viewport heights of scroll on desktop and 5 on mobile. Text is real HTML layered over the canvas, so it stays readable, selectable and accessible at every step.

| # | Scroll | Scene | Technique | Copy (placeholder) |
|---|---|---|---|---|
| 1 | 0-0.8 vh | A storm of job cards streams past in depth; fake ones glitch and flicker red | React Three Fiber instanced meshes (hundreds of cards in one draw call), depth fog | "Thousands of job posts. Half of them aren't real." |
| 2 | 0.8-1.8 vh | A beam of light sweeps the storm; fake cards crack and shatter into glass shards that fall away | shards pre-fractured in Blender (Cell Fracture), moved along GSAP-driven, physics-like curves; transmission material on the high tier | "We only read companies' own hiring systems." |
| 3 | 1.8-2.8 vh | The real cards fly together and fuse into one Liquid Glass card | instanced morph into a single card; refraction shader with chromatic edges | "Every job verified at the source." |
| 4 | 2.8-3.6 vh | The card flips to "posted 4 min ago · 96% match" and the match orb spins up | scroll-driven flip, orb shader, counter animation | "Minutes old. Ranked for you." |
| 5 | 3.6-4.6 vh | A resume page slides in and morphs line by line into a tailored version while the ATS meter fills | DOM text animated with SplitText over a glass sheet | "Your facts. Never invented." |
| 6 | 4.6-6 vh | An offer letter lands on the glass with a soft burst of light particles | Blender-made envelope (real-time model or rendered frames), GPU particles | "Be among the first fifty." with the waitlist call to action |

Camera: one continuous dolly through the scenes, no hard cuts. ScrollTrigger scrubs one master timeline with a label per scene, so beats can be tuned without rewriting code.

Fallbacks: high tier gets real-time 3D; mid tier gets frame-sequence versions of scenes 1-3 (rendered in Blender) and 2D versions of 4-6; low tier and reduced motion get static posters with fades; without JavaScript, a static page with the same copy.

## Phase 0 demo: acceptance
- Built in `prototypes/hero-demo` (Vite + React + React Three Fiber + drei + GSAP) and deployable as a static site.
- LCP under 2.5 s in Chrome's mobile emulation with 4x CPU slowdown and Fast 4G; the LCP element is the headline, never the canvas.
- 3D code and assets load after first paint.
- During scroll: 55+ fps average on the laptop GPU; 50+ fps under 4x CPU slowdown on the high tier, otherwise the mid-tier fallback switches in by itself.
- Mobile assets under 2.5 MB; zero layout shift.
- The full fallback ladder and a visible pause control for ambient motion.
- Evidence in the Phase 0 report: a short screen recording, Lighthouse scores and a performance trace.
- Side-by-side review with 2-3 of Sayandip's reference screenshots in docs/design/references/ (he picks which); he decides whether it's a "wow".

## Techniques (what the reference sites use, and where we use each)
| Technique | What it is | We use it for |
|---|---|---|
| Scroll-scrubbed frame sequence | a rendered video as numbered images, drawn on a canvas at the frame that matches the scroll position (the AirPods-page trick) | photoreal-looking 3D on mid-tier devices; product-style hero moments |
| Cursor-driven frames | showing the frame closest to the cursor (a character that looks around) | perhaps a mascot later; not core |
| Play once, then freeze | a short clip that ends on a still | onboarding intro, celebrations |
| Real-time 3D (three.js, React Three Fiber) | live scenes with lights and materials | the hero storm, shards, card and orb on high-tier devices |
| Shaders (GLSL) | GPU programs for dissolves, refraction, halftone, noise | glass refraction, transitions, backgrounds |
| CSS 3D and small WebGL components | rings, carousels, tunnels, tilt cards, particle globes | section transitions, the job-card ring, a "companies we read" globe |
| Kinetic type | split, animated text (GSAP SplitText) | headlines, the resume morph |

## Asset pipeline
1. **Model** in Blender 5.3 through the Blender connector: glass card, shards (Cell Fracture), match orb, resume sheet, envelope and offer letter, abstract light fields. Sayandip keeps Blender open with the MCP add-on during these sessions.
2. **Materials and light:** glass BSDF with dispersion for renders; HDRIs from Poly Haven (CC0).
3. **Render** frame sequences with Cycles + OptiX on the RTX 4050 (EEVEE for drafts). `.blend` sources live in `assets-src/` under Git LFS; renders are gitignored and reproducible.
4. **Real-time export:** glTF 2.0 with Meshopt or Draco geometry compression and KTX2 (Basis) textures, processed with gltf-transform, within the budgets below.
5. **Frame encoding:** AVIF with a WebP fallback, in two sizes (desktop, mobile); at most 120 frames per sequence on desktop and 60 on mobile; progressive loading (every 4th frame first, then the rest); decoding off the main thread (`createImageBitmap`, OffscreenCanvas in a worker).
6. **AI-generated assets** only from tools whose licences allow commercial use; each asset's source and licence recorded in `assets/LICENSES.md`.
7. **Never:** real brands' products, real people, copyrighted characters.

## Performance budgets
| Budget | Mobile | Desktop |
|---|---|---|
| LCP element | text or a poster image, never the canvas | same |
| 3D code (lazy, gzip) | under 350 KB | under 350 KB |
| Hero assets | under 2.5 MB | under 5 MB |
| Frames per sequence | at most 60 | at most 120 |
| Frame rate while scrolling | 50+ fps on the high tier, or fall back | 55+ fps |
| Device pixel ratio | clamped to 1-1.5 | clamped to 1-2 |
| GPU memory | under 300 MB | under 600 MB |

Adaptive quality: GPU tier detection (for example the `detect-gpu` library) plus a live FPS monitor (drei's `PerformanceMonitor`) that steps quality down (fewer shards, no transmission, lower DPR, switch to frames) before users notice.

## Motion in the mobile app
Reanimated 4 on the UI thread for everything interactive; gesture-driven swipe cards on `spring.gentle`; shared-element transitions from card to detail; Skia shaders for the orb and glass; haptics mapped to meaning (a light tick on save, a success pattern when the apply page opens, a warning on scam risk). No live WebGL scenes inside the app: cinematic moments (onboarding intro, offer celebration) use pre-rendered sequences or Skia 2.5D effects.

## Testing motion
Visual regression with animations disabled; FPS and long-task traces of the landing page in CI (Playwright with the Chrome DevTools Protocol); Lighthouse budgets; a manual pass on a mid-range Android phone before each release.
