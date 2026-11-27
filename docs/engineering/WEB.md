# Web app (Next.js)

## Baseline
Next.js 16.x App Router, React 19.2, TypeScript strict, Tailwind CSS 4 driven by `packages/design-tokens`, TanStack Query on the client, Zod at the edges, and the generated `packages/api-client`. Check exact current versions (`npm view next version`) and pin them.

## Structure
```
apps/web/
  app/
    (marketing)/   landing (scroll story), pricing, about, legal pages: static or revalidated
    (seo)/         companies/[slug], jobs/[role]-[city]: server-rendered, revalidated every few minutes
    (app)/         feed, job/[id], tracker, resume, alerts, settings, privacy: the signed-in app
    api/           tiny route handlers only (health, revalidation hook); business logic lives in the Spring API
  components/      app components built on packages/glass-web
  motion/          GSAP timelines and React Three Fiber scenes (lazy chunks)
  lib/             API client wrapper, auth helpers, analytics, feature flags
```

## Rendering strategy
| Surface | Strategy | Why |
|---|---|---|
| Landing, pricing, legal | static, rebuilt on deploy | fastest first load; edge-cached |
| Company and role pages | server-rendered with revalidation (2-10 min) | SEO with fresh counts |
| App screens | server components for the shell, client components for interaction | fast first paint, rich interaction |
| Public job detail | server-rendered, edge-cached | shared links open instantly |

## Data and auth
- Server components call the API with the user's session cookie forwarded; client components use TanStack Query with cursor pagination and optimistic updates for save, hide and tracker moves.
- The API is the only source of truth; the web app holds no business rules.
- Auth: a cookie session issued by the API on the parent domain (`api.` and `app.` subdomains), `HttpOnly`, `Secure`, `SameSite=Lax`, with a CSRF token on mutating requests.

## Styling and glass
- Tailwind 4 theme generated from the design tokens: a CSS variable for every token, dark and light, accent themes switched by `data-accent`.
- Glass from `packages/glass-web`: tier A, WebGL refraction for hero elements; tier B, CSS `backdrop-filter` plus an SVG displacement filter where the browser supports it; tier C, plain blur or solid. The tier is picked at runtime from capability and GPU checks (docs/design/DESIGN-SYSTEM.md).

## Motion
- GSAP + ScrollTrigger for scroll stories and timelines; Lenis smooth scrolling on the landing page only, never inside the app.
- three.js + React Three Fiber + drei for 3D, always in lazy chunks loaded after first paint, inside `<Suspense>` with a poster fallback.
- Motion (formerly Framer Motion) for component transitions; the View Transitions API for route changes where supported.
- Respect `prefers-reduced-motion`, `prefers-reduced-transparency`, Save-Data and low-end tiers (docs/design/MOTION-3D.md).

## Performance budgets (Lighthouse CI on every pull request)
| Metric | Landing | App routes |
|---|---|---|
| LCP (mobile, 4G, mid-range) | under 2.5 s | under 2.0 s |
| INP | under 200 ms | under 200 ms |
| CLS | under 0.1 | under 0.05 |
| Initial JS (gzip) | under 250 KB | under 180 KB |
| 3D chunk (lazy, gzip) | under 350 KB | not used |
| Hero assets on mobile | under 2.5 MB | - |

Images as AVIF/WebP through `next/image`; fonts self-hosted and subset with `font-display: swap`; nothing shifts the layout after load.

## Accessibility
WCAG 2.2 AA: visible focus rings on glass, keyboard paths for everything, skip links, ARIA only where HTML can't do the job, labels for the match orb and ATS meter, a pause control for any animation longer than 5 seconds, axe checks in CI, and a manual screen-reader pass (NVDA) per release.

## SEO
Metadata API for titles, descriptions and Open Graph images (generated per company and role page); sitemap and robots; canonical URLs; breadcrumb and organisation structured data. No `JobPosting` structured data unless a page meets Google's requirements (we show summaries, not full descriptions).

## Security headers
Content-Security-Policy with nonces and `frame-ancestors 'none'`, HSTS, `Referrer-Policy: strict-origin-when-cross-origin`, a restrictive `Permissions-Policy`, `X-Content-Type-Options: nosniff`.

## Testing
Vitest + Testing Library for components and hooks; Playwright end to end on a production build (sign-in, feed, filters, save, tracker, privacy export and delete); axe checks; Playwright screenshot comparisons of key screens in both themes with animations off; Lighthouse CI budgets.

## Deployment
A standalone Node server image on the k3s cluster behind Cloudflare (ADR-0006). Not on Vercel's Hobby plan, which forbids commercial use. Static assets cached immutably for a long time; public HTML cached briefly at the edge.
