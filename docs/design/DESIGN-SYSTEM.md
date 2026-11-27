# Liquid Glass 2.0: the design system

Design is Sayandip's favourite part of this product and its first impression. This system keeps it consistent, accessible and fast on every platform. The product-designer agent owns this file. Values marked "calibrate" are set in Phase 0 against SplitIT's implementation and real screenshots.

## Principles
1. **Content first, glass second.** Glass frames and floats; it never competes with the job information.
2. **Light is the brand.** Refraction, specular rims and soft caustics carry the identity, not heavy colour or decoration.
3. **Depth with purpose.** Layers mean something: base content, floating controls, sheets, alerts. Nothing floats without a reason.
4. **Calm by default, cinematic by moment.** The feed is quiet and fast; the landing page, onboarding, match reveal and offer celebration are where motion performs.
5. **Accessible glass.** Text contrast is measured against the worst background behind it; reduced transparency, reduced motion and high contrast each get a first-class look.
6. **Native feel per platform.** One identity, platform-correct behaviour: gestures, navigation, haptics, system glass on iOS 26+.
7. **Performance is design.** A beautiful frame that drops to 30 fps on a mid-range phone is a bad design.

## What we inherit from SplitIT
SplitIT ships a Liquid Glass UI with 16 colour themes and 5 kinds of glass, in dark and light, drawn on the web by its own WebGL engine (with coins that turn and split) and on mobile with Skia. Phase 0 reads its code (local clone at `C:\Users\Sayan\Desktop\Projects\SplitX`, read-only) and records here which recipes we keep, what we change, and why. Don't copy blindly: this product is denser (long lists of jobs rather than a few balances), so readability rules are stricter.

## Token architecture
- Three tiers: **primitives** (raw values such as `blue.500`, `blur.24`), **semantic** (meaning, such as `surface.glass.frost`, `text.primary`, `status.verified`), **component** (`jobCard.background`, `tabBar.blur`). Components use only semantic or component tokens.
- Source format: W3C Design Tokens (DTCG JSON) in `packages/design-tokens`, built with Style Dictionary into CSS variables (web), a Tailwind 4 theme, and a TypeScript theme object for React Native and Skia.
- Modes: `dark` (default) and `light`; accents via `data-accent` on the web and a theme context on mobile; motion and transparency preferences are modes too.

## Colour
- **Neutrals:** a cool "ink" ramp for dark backgrounds and a "mist" ramp for light (11 steps each; calibrate).
- **Brand hue:** chosen with the name in Phase 0. Directions to explore: signal green (verified, go), electric indigo (tech, depth), aurora teal (calm, trust). One hue, used sparingly: primary actions, the match orb, focus.
- **Status:** `verified` (green), `fresh` (a live-pulse colour for "first seen minutes ago"), `warning` (amber), `danger` for scam risk (red), `info` (blue). Status is never shown by colour alone; there is always an icon or a label.
- **Accent themes:** 8 in v1 (extendable to 16 like SplitIT), each a tested set of tint, glow and gradient stops for both modes. Free users get the brand accent; Pro unlocks all.
- **Backgrounds:** slow gradient meshes or blurred 3D light fields behind the glass (one full cycle no faster than 20 s), paused under reduced motion.

## Glass materials
| Material | Use | Look | Web | Android | iOS 26+ |
|---|---|---|---|---|---|
| `glass.clear` | floating controls (tab bar, segmented control, action button) | light blur, strong edge refraction, crisp specular rim | tier A WebGL refraction, B blur + SVG displacement, C blur | Skia refraction shader | system glass (expo-glass-effect) |
| `glass.frost` | cards over busy backgrounds (job cards, sheets) | heavier blur, gentle grain, soft rim | B or C (A only for hero cards) | Skia blur, no refraction | system glass or blur |
| `glass.tint` | primary actions, selected states | accent-tinted frost with an inner glow | B or C | Skia blur + tint | tinted system glass |
| `glass.prism` | hero moments only (match orb, landing scenes) | refraction plus chromatic dispersion at the edges, caustic highlights | A only (falls back to tint) | Skia shader on high-tier devices, otherwise tint | custom Skia |
| `glass.solid` | reduced transparency, low-end devices, dense tables | opaque, same radius, border and shadow language | all | all | all |

Parameters per material (calibrate): blur radius, saturation boost, refraction strength (displacement scale), rim width and intensity, inner shadow, grain amount, tint opacity, a 1 px gradient hairline border (about 30% to 5% white in dark mode), drop shadow.

Rules:
- Text on glass sits on a scrim or tint that guarantees 4.5:1 contrast against the worst plausible backdrop; verified with automated screenshots on the busiest backgrounds.
- Never stack more than two glass layers; a third becomes `glass.solid`.
- Refraction (tier A and `glass.prism`) appears on at most two elements per screen.

## Depth and elevation
Layers: `base` 0, `raised` 1 (cards), `floating` 2 (tab bar, action button), `overlay` 3 (sheets, menus), `modal` 4, `toast` 5. Each layer has a shadow token (softer and larger as it rises) and a blur step. 3D scenes use real depth (parallax, perspective) consistent with these layers.

## Shape
Radius scale: 6 (chips), 10 (inputs), 16 (cards), 22 (sheets), 28 (hero cards), full (pills, the orb). Continuous, squircle-like corners where the platform supports them (natively on iOS; CSS `corner-shape` where available), plain radii elsewhere. Concentric rule: inner radius = outer radius - padding.

## Typography
- **UI typeface:** Inter or Geist (both under the SIL Open Font License). Pick one in Phase 0 by testing dense job lists at 13-15 px.
- **Display typeface:** one characterful open-licence face for hero headlines and big numbers, chosen with the brand.
- **Numerals:** tabular figures for counts, scores and salaries.
- **Scale (fluid, with `clamp`):** 12, 13, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72. Line height 1.2 for display, 1.45 for body.
- **Indian languages (later):** Noto Sans Devanagari and Bengali as fallbacks when Hindi and Bengali interfaces arrive.

## Spacing and layout
4-point grid; spacing tokens 2, 4, 8, 12, 16, 20, 24, 32, 40, 56, 80. Breakpoints 360, 600, 900, 1200, 1440. Mobile-first; safe areas respected; reading width capped near 72 characters. Desktop app layout: left rail, feed column, detail panel.

## Iconography and illustration
One icon set (Lucide under ISC, or Phosphor under MIT) at a consistent stroke; custom 3D glass icons from Blender for hero moments and empty states; no stock photos of people; company logos only to identify an employer.

## Components
Each in every state (default, hover, pressed, focus, disabled, loading, error):
GlassSurface (the base), Button (primary/tint, secondary/frost, ghost, destructive), IconButton, Chip and FilterPill, SearchField with suggestions, SegmentedControl, floating TabBar, NavBar, BottomSheet (snap points), Modal, Toast, Tooltip, **JobCard** (new, seen, saved, applied, closed; swipeable on mobile), **MatchOrb** (0-100, refracting, slowly rotating, with an accessible text value), **FreshnessBadge** (live pulse under 60 minutes), **SourceBadge** ("Greenhouse · official"), kanban column and card, **AtsMeter** (radial, with a fix list), ProgressRing, Skeleton (glass shimmer), EmptyState, ErrorState, OfflineBanner, Avatar, CompanyMark (logo or monogram), Paywall card, pricing toggle, form fields, Toggle, Checkbox, Radio, Slider, DatePicker, small charts.

## States and feedback
Skeletons, not spinners, while loading. Empty states teach the next action. Errors say what happened and what to do, with a retry. Offline is a calm banner. Success gets a small, fast celebration (a glow or particles under 600 ms); the big celebration is saved for offers.

## Accessibility
- WCAG 2.2 AA everywhere; AAA contrast for body text where possible.
- Focus ring: 2 px in the brand colour with a 2 px contrasting offset, visible on any glass.
- Touch targets at least 44x44 pt (iOS) and 48x48 dp (Android).
- `prefers-reduced-motion`: movement becomes fades; ambient loops stop.
- `prefers-reduced-transparency` and the mobile OS setting: switch to `glass.solid`.
- `prefers-contrast: more`: stronger borders, solid surfaces.
- Screen readers: the orb, meters and charts have text equivalents; every icon button has a label.

## Quality bar
Every screen must look intentional in dark and light, x 3 accents, x 3 viewports (360x800, 390x844, 1440x900), x reduced motion on and off. `/design-review` produces the screenshot grid; Playwright screenshot tests catch regressions.

## Phase 0 tasks
1. Design archaeology on SplitIT; record the findings here.
2. Choose the UI and display typefaces; test dense lists.
3. Tokens v1 (primitives, semantic, the five materials, both modes, 4 accents) in `packages/design-tokens`.
4. A component gallery page showing every material over the three busiest backgrounds, to calibrate contrast.
