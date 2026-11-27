# Hero demo: shared spec and asset contract

The single source of truth shared by the two motion-artist builds of the Phase 0 hero demo ("Signal from noise", docs/design/MOTION-3D.md). The orchestrator owns this file; ask before changing it, and report any deviation.

## Who owns what
| Build | Owns (writes only here) |
|---|---|
| hero-assets (Blender) | `assets-src/hero/**`, `prototypes/hero-demo/public/hero/**`, `assets/LICENSES.md` |
| hero-web (web app) | everything else under `prototypes/hero-demo/` (including `evidence/`), and `.claude/launch.json` |

Nobody runs state-changing git commands (add, commit, checkout, switch, stash, reset, branch); the orchestrator commits. Nobody touches `reference/`, `.env*`, other docs, or Sayandip's SplitIT folder.

## Look
- Dark first. Page background `ink-950 #05060A`, raised `ink-900 #0A0D18`, depth fog and glow tint `indigo #2B2F77` (subtle).
- One provisional brand hue, **signal teal `#3BE8C4`**, used sparingly (beam tint, verified glow, match orb, focus, primary button). It must be a single variable on each side (CSS custom property, a shader uniform, one Blender material colour) because the real brand hue is chosen with the name.
- Fake ("noise") cards: `danger #FF3B4E` glitch and flicker. Text `#F2F5FA` primary, `#AAB2C5` secondary.
- Glass: hairline gradient border (about 30% to 5% white), soft rim light, refraction and chromatic dispersion only on the single hero card (`glass.prism`); frosted panels elsewhere.
- The visual bar is Sayandip's references (inspiration only, never copied or shipped): `docs/design/references/inspiration/4.png` (AirPods particle ring, parrot site), `8.png` (fruit burst), `9.png` (container with huge type layered in front of and behind it). What makes them premium: one hero object, dramatic light, huge display type layered in depth around the object, particle bursts, generous negative space. Ours must feel as premium while fitting a careers product.
- Never: real brands, logos or products; real people; downloaded textures, HDRIs or models; add-on or extension installs. Light procedurally (area lights, emissive strips, in-scene Lightformers on the web).

## Storyboard and copy (placeholder copy, use exactly)
About 6 viewport heights of scroll on desktop and 5 on mobile; one continuous camera dolly, no hard cuts; one GSAP master timeline with labels `s1`-`s6`.

| Beat | Scroll | Scene | Copy |
|---|---|---|---|
| s1 | 0-0.8 vh | A storm of job cards streams past in depth; fake ones glitch and flicker red | **h1:** "Thousands of job posts. Not all of them are real." |
| s2 | 0.8-1.8 vh | A beam of light sweeps the storm; fake cards crack and shatter into glass shards that fall away | "We only read companies' own hiring systems." |
| s3 | 1.8-2.8 vh | The real cards fly together and fuse into one Liquid Glass card | "Every job verified at the source." |
| s4 | 2.8-3.6 vh | The card flips to its back and the match orb spins up | "Minutes old. Ranked for you." Card back (an example card, tagged "Example"): "Backend Engineer · Java, Spring Boot", "Bengaluru", "posted 4 min ago", "96% match" |
| s5 | 3.6-4.6 vh | A resume on a glass sheet morphs line by line into a tailored version while the ATS meter fills | "Your facts. Never invented." Each tailored line carries a small tag naming the fact it came from |
| s6 | 4.6-6 vh | An offer letter lands on the glass with a soft burst of light particles | "Be among the first fifty." with a "Join the waitlist" button |

Copy note: the storyboard's original s1 line said "Half of them aren't real". We can't prove that number, and the brand rules forbid unsupported claims, so the line is "Not all of them are real."
Nav: the wordmark "FirstFifty" (the codename) and a "Join the waitlist" button that scrolls to s6. Footer: "Prototype · Phase 0 demo". The waitlist form sends nothing (demo): on submit it says "Demo only: nothing was sent. The waitlist opens soon."

## Asset contract (hero-assets delivers, hero-web consumes)
Units are glTF metres, Y up, the front of every object faces +Z (towards the camera), and every object is centred at the origin unless stated otherwise. Everything lives under `prototypes/hero-demo/public/hero/` and is served from `/hero/...`.

### `card.glb`
- One mesh node `Card`: a rounded-rectangle glass slab, width 1.6, height 1.0, thickness 0.035, corner radius 0.09, a small bevel on the front and back edges. Transforms applied.
- UV0 on the front face maps the card's bounding box: `u = (x + 0.8) / 1.6`, `v = (y + 0.5) / 1.0`. The back face uses the same mapping mirrored in u, so a texture reads correctly from behind. Edges get any sensible UVs.
- Under 2,000 triangles. A simple PBR material is fine; the web replaces it.

### `shards.glb`
- The same card pre-fractured into 24 pieces (20-28 allowed): mesh nodes `Shard_00` to `Shard_NN`, no parent transforms.
- Each node's translation is that shard's centroid in card space; its vertices are local to that centroid. Assembled at their translations, the shards rebuild the card exactly.
- Voronoi-style cuts perpendicular to the card face (a slight random tilt is welcome), with seeds denser around an impact point at card-space `(0.38, 0.12)`, so shards are smaller near the impact.
- Front-face UVs continue the card's mapping, so the card's face texture carries across the shards. Inner cut faces have their own UV region or none.
- Under 8,000 triangles in total.

### `envelope.glb`
- Node `Envelope` (the body), width 1.4, height 0.9, thickness about 0.02, centred at the origin.
- Child node `Flap` with its origin on the hinge line at the top edge of the body; it opens by rotating about its local X axis (0 = closed).
- Child node `Letter`: a paper sheet slightly smaller than the body, inside it, that can slide up along +Y.
- Under 5,000 triangles.

### Frame sequence (mid tier, beats s1-s3 only)
- `frames/desktop/0001.avif` ... `0120.avif` and the same names in `.webp`: 1280x720, 120 frames.
- `frames/mobile/0001.avif` ... `0060.avif` and `.webp`: 540x960 portrait, 60 frames.
- Frame 1 is the start of s1; the last frame is the end of s3: the fused glass card centred, seen front-on, so the 2D versions of s4-s6 can continue from it.

### Posters and stills (low tier, reduced motion, and the mid tier's s4-s6)
- `posters/poster-1`, `poster-2`, `poster-3` (the s1, s2 and s3 midpoints): `-desktop` at 1600x900 and `-mobile` at 720x1280, each in `.avif` and `.webp`, for example `posters/poster-1-desktop.avif`.
- `stills/card-front` (the hero glass card, three-quarter view, transparent background, 1200 px wide) and `stills/envelope` (the envelope with the letter peeking out, transparent background, 1200 px wide), each in `.avif` and `.webp`.

### `manifest.json`
```json
{
  "version": 1,
  "glb": { "card": "/hero/card.glb", "shards": "/hero/shards.glb", "envelope": "/hero/envelope.glb" },
  "glbCompression": "meshopt",
  "shardCount": 24,
  "sequence": {
    "covers": ["s1", "s2", "s3"],
    "desktop": { "frames": 120, "width": 1280, "height": 720, "path": "/hero/frames/desktop/", "pad": 4, "formats": ["avif", "webp"], "bytes": { "avif": 0, "webp": 0 } },
    "mobile": { "frames": 60, "width": 540, "height": 960, "path": "/hero/frames/mobile/", "pad": 4, "formats": ["avif", "webp"], "bytes": { "avif": 0, "webp": 0 } }
  },
  "posters": { "poster-1": { "desktop": "/hero/posters/poster-1-desktop", "mobile": "/hero/posters/poster-1-mobile", "formats": ["avif", "webp"] } },
  "stills": { "card-front": { "path": "/hero/stills/card-front", "width": 1200, "height": 0, "formats": ["avif", "webp"] } },
  "bytes": { "glbTotal": 0 }
}
```
Write the manifest as soon as the GLBs exist (with only the `glb` keys), then extend it as the sequence and posters land. hero-web must work with any subset: entries that are missing fall back to procedural placeholders.

## Budgets (docs/design/MOTION-3D.md)
| Budget | Mobile | Desktop |
|---|---|---|
| Hero assets a visitor downloads | under 2.5 MB | under 5 MB |
| GLBs combined | target under 300 KB | same |
| Frames per sequence | at most 60 | at most 120 |
| 3D code (lazy, gzip) | under 350 KB | under 350 KB |
| Initial JS (gzip) | under 250 KB | under 250 KB |
| LCP | under 2.5 s (Lighthouse mobile), headline text is the LCP element | same |
| CLS | 0 | 0 |
| FPS while scrolling | 50+ on the high tier, or the auto-fallback switches to mid | 55+ |
| Device pixel ratio | clamped to 1-1.5 | clamped to 1-2 |
| GPU memory | under 300 MB | under 600 MB |
