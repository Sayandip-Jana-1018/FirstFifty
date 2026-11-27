# ADR-0008: Motion and 3D built in-house

- Status: Accepted
- Date: 2026-11-24
- Deciders: Sayandip, Claude

## Context
Sayandip shared reference sites (scroll-scrubbed product shots, cursor-driven characters, real-time 3D stores, shader dissolves, glass components) and a paid template library. The effects come from a handful of techniques: frame sequences on a canvas, cursor-driven frames, play-once clips, real-time three.js, shaders, CSS/WebGL 3D components and kinetic type. GSAP, including ScrollTrigger and SplitText, has been free for commercial use since April 2025. The library's visuals (food, drinks, animals, people) don't fit a careers brand, and templates look like every other subscriber's site. We have a Blender connector and an RTX 4050 for rendering.

## Decision
Build all motion ourselves: GSAP and ScrollTrigger, three.js with React Three Fiber and drei, custom shaders, Rive or Lottie where a designed micro-animation fits, Reanimated and Skia on mobile. Assets come from Blender (through the connector) and from AI tools whose licences allow commercial use, recorded in `assets/LICENSES.md`. No paid template subscriptions. No real brands' products or real people.

## Consequences
- We own a distinctive look.
- Performance budgets and fallbacks must be enforced (docs/design/MOTION-3D.md).
- An asset pipeline (Blender, glTF compression, frame encoding) has to be built and maintained.

## Alternatives considered
- **Template library subscription:** generic results and visuals that don't fit; useful at most as a reference.

## Revisit when
The Phase 0 demo fails Sayandip's "wow" test. Then one month of a reference subscription (about $29) for study is acceptable.
