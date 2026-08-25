# Handle

A free TikTok username generator that does the boring part for you: checking which names are actually available. Built as the MVP for a search-first, ad-supported creator-tools site.

> **Brand rename note:** This project was previously called "NameTok" in earlier iterations. The code, copy, package, and docs have all been updated; if you have old links, bookmarks, or analytics referring to the old name, those still work at the same URL paths — only the visible brand is now **Handle**.

## Quick start

```bash
cd handle
npm install
npm start
```

Then open <http://localhost:3000>. Pages:

- `/` — Home
- `/generator` — The tool
- `/faq` — FAQ (placeholder copy, write your own)
- `/about` — About (placeholder copy, write your own)
- `/privacy` — Privacy Policy
- `/terms` — Terms of Service
- Anything else → in-page 404 section (real `404` status from the Node server)

Requires Node.js 18+ (uses the built-in `fetch`).

## What's in the MVP

- **A working multi-page site** (Home, Generator, FAQ, About, Privacy, Terms) with a real top-nav, not a single-page scroll. Static deploys use a single `index.html` with section toggling; the local Node build serves route-specific meta so crawlers and `view-source:` see something useful.
- **A generator** that takes a keyword, a niche, and a vibe, then returns 10–20 handle ideas that respect TikTok's current username rules. 17 themed vibes + 3 mode switches (none / random / unique).
- **A live availability check** that probes TikTok (and is pluggable for the other platforms later). Verdicts read "Likely available" / "Likely taken" / "Unknown" — never a confident "Available".
- **A Unicode font converter** under the generator for the "tiktok name fonts" keyword.
- **A real 404 page** — server returns a `404` status, the SPA shows an in-page section with links to the actual pages.
- **Standard SEO hygiene**: per-page title/description/canonical, Open Graph + Twitter Card, SoftwareApplication schema on the tool page, an OG image and favicon.
- **Honest affiliation copy** — "not affiliated with TikTok / ByteDance" appears in the home hero, the generator section, the FAQ, the About, the Terms, and the footer. "TikTok" is a trademark of ByteDance Ltd; we say so.
- **AdSense prerequisites in place**: Privacy and Terms pages, an `ads.txt` at the root with a placeholder publisher ID, and the affiliation disclaimer. Add the real AdSense publisher ID to `public/ads.txt` before applying.
- **Rate-limited** check endpoint (60/min/IP, configurable) and **format-validated** handle input on both the client (HTML pattern) and the server (regex).
- **Placeholder copy** on the About and FAQ pages, clearly marked — for you to write. Privacy and Terms drafts are also working drafts that need a lawyer's review before going public.

Everything else from the original plan (long-form blog, programmatic SEO pages, email capture, social channels) is deliberately not in this MVP. The MVP proves the core engine. The rest is built on top once this works.

## File layout

```
handle/
├── server.js                 # Express server + API routes + per-route meta + 404
├── lib/
│   ├── availability.js       # Pluggable availability checker
│   └── generator.js          # Wordlist + pattern engine
├── public/
│   ├── index.html            # The whole SPA in one file (six sections, English)
│   ├── {lang}/index.html     # Localized SPA for each of 17 languages
│   ├── favicon.svg           # Brand mark
│   ├── og-image.svg          # 1200×630 Open Graph image
│   ├── ads.txt               # AdSense placeholder
│   ├── css/style.css
│   └── js/
│       ├── client-shim.js    # window.__handleClient surface
│       ├── titles.js         # Per-locale titles (loaded by router)
│       ├── router.js         # Client-side router (5 known routes + 404, locale-aware)
│       ├── fonts.js          # Unicode font converter
│       ├── generator.js      # Generator page logic
│       └── consent.js        # Cookie consent banner
├── i18n/
│   └── build.py              # Build script: English template → 17 localized files
├── package.json
└── README.md
```

## How the availability check works

This is the part the user prompt asked me to research, not silently pick. So here are the realistic options and the trade-offs, in order of how much I recommend each for a real public deployment.

| Backend | What it does | Pros | Cons | Recommended? |
|--------|-------------|------|------|-------------|
| **TikTok oEmbed** (`https://www.tiktok.com/oembed?url=https://www.tiktok.com/@handle`) | Returns 200 with profile metadata for a public account, 404 for a missing handle. | Official-ish endpoint, no scraping, simple to integrate, low IP-block risk. | No published rate limit; can be flaky in regional edge incidents; private accounts return 404 even when the handle is "taken." | **Yes, this is the default.** |
| **Direct probe of `tiktok.com/@handle`** | Fetch the profile URL and parse the HTML for hydration data or "couldn't find this account". | No third-party dependency; works when oEmbed is down. | Brittle (TikTok's HTML changes often); closer to scraping, grey area of TikTok's TOS; higher block risk from a single egress IP. | **Use only as a fallback** when oEmbed returns UNVERIFIED. Don't lead with it. |
| **Server-side headless browser (Puppeteer/Playwright)** | Real browser load, full JS execution, scrape profile data. | Highest accuracy; can detect private accounts; works on the modern SPA. | Heavy (RAM/CPU), expensive, and TikTok's anti-bot protections are aggressive; high TOS exposure; the wrong move at this scale. | **No, not for a single-name generator.** Reach for this only if you're building a brand-monitoring product where 100% accuracy justifies the cost. |
| **Third-party API (namewastaken, socialcal, socialfetch, apify sync-network)** | A paid or freemium service does the probe and returns JSON. | Cross-platform out of the box; less code to maintain. | Cost at scale (most are paid or rate-limited at the free tier); another vendor to depend on; a service you don't control is a service that can shut down. | **No for the MVP.** Re-evaluate if/when we ship the cross-platform check beyond TikTok. |
| **Client-side fetch from the user's browser** | `fetch('https://www.tiktok.com/@x')` from page JS. | Free, no server cost. | CORS blocks the response; TikTok doesn't send CORS headers; brittle. | **No.** |

### What the MVP does today

The default checker is a `CompositeChecker` that:

1. Tries `TikTokOEmbedChecker` first.
2. Falls back to `TikTokDirectChecker` only if the oEmbed result is `unverified`.
3. Wraps each in a 5-minute cache (30 seconds for `unverified`, so transient failures don't pin a false "Unknown" for too long).

Every result includes a `checkedAt` ISO timestamp and a `backend` field so the UI can show "Checked 2 min ago · via tiktok-oembed" — and so you can audit the upstream answer.

### The interface is the important part

`lib/availability.js` exposes a `BaseChecker` class with a single `check(handle)` method that returns a normalized result envelope:

```js
{
  handle: 'fitnesslab',
  status: 'likely_available' | 'likely_taken' | 'unverified',
  confidence: 'high' | 'medium' | 'low',
  checkedAt: '2026-08-24T18:30:00.000Z',
  backend: 'tiktok-oembed',
  profileUrl: 'https://www.tiktok.com/@fitnesslab' | null,
  profileName: 'Fitness Lab' | null,
  note: 'oembed status 503' | null,
}
```

The internal status code stays `unverified` (so the API contract doesn't change); the user-facing label reads "Unknown" everywhere.

To swap in a new backend, implement `BaseChecker`, drop it into the composite, and you're done. The route, the cache, the frontend — none of it changes.

### Honesty in the UI

The frontend never claims certainty. It says **Likely available** / **Likely taken** / **Unknown**, with a timestamp, and shows a direct "Open on TikTok" link on every row. If both backends fail, an amber banner appears at the top of the result list and the user is told to confirm manually. There is no path to a confident "Available" that is wrong by the time they click.

### Rate limiting

The MVP includes a simple in-process token bucket: 60 checks per minute per IP. Plenty for local single-user testing. If you put this on a public server, raise it (or remove it) and consider queueing checks to a worker rather than blocking the request thread. The server also rejects any handle that doesn't match `^[a-z0-9._]{2,24}$` before it ever reaches the upstream — defense in depth against the client being bypassed.

## TikTok rules we currently enforce

The generator validates every candidate before returning it. Current rules baked in (verify before launch — TikTok can change them):

- 2 to 24 characters
- Lowercase letters, digits, `.`, `_`
- No leading or trailing period
- No consecutive periods
- No leading or trailing underscore
- Case-insensitive (handles are stored lowercase)

These are loaded in `lib/generator.js` as the exported `RULES` object, so they're easy to update in one place. The keyword input on the generator page enforces the same 24-character cap via HTML `maxlength` + `pattern`, and `generator.js` re-sanitizes the value on submit.

## SEO

Each page sets:

- Title tag, meta description, canonical URL
- Open Graph + Twitter Card tags (with a 1200×630 OG image at `/og-image.svg`)
- Per-page `<link rel="canonical">`

The Generator page also ships a `SoftwareApplication` schema (JSON-LD) so Google can render the tool as a rich result. Update the `featureList` as the tool evolves.

## Localization (17 languages)

The site ships in 17 languages: English (default) + Spanish, German, French, Italian, Portuguese, Dutch, Polish, Russian, Chinese, Vietnamese, Indonesian, Malay, Tagalog, Hindi, Bengali, Urdu, Arabic. Each language has its own URL prefix (`/es/`, `/de/`, etc.) and its own `<html lang>`, `<title>`, meta description, og:locale, and hreflang alternates.

**Tier 1 (8 languages, fully localized):** Spanish, German, French, Italian, Portuguese, Dutch, Polish, Russian. The SEO-critical strings (title, meta, h1, lede, primary CTA, generator h1, 404 h1), the navigation labels, and the per-route titles are all translated.

**Tier 2 (9 languages, meta + nav localized, body in English):** Chinese, Vietnamese, Indonesian, Malay, Tagalog, Hindi, Bengali, Urdu, Arabic. The title, meta description, html lang/dir, og:locale, and navigation labels are translated. The body content (FAQ answers, About, etc.) stays in English so a professional translator can review and fill in the body without re-doing the meta.

**To spot-check Tier 2 quality:** the meta descriptions and titles are short, contextual translations. They're meant to be correct enough to index properly in those markets, but they're not professional-grade. If a particular language is important for your launch, hire a native speaker to review the meta + body before going live on a real domain.

**RTL support:** Arabic (`ar`) and Urdu (`ur`) get `dir="rtl"` on the `<html>` element so the layout flips correctly. The CSS uses logical properties (margin-inline-start, etc.) where it matters, but a thorough RTL pass would benefit from a native reviewer.

**How the static deploy handles localized routes:** The CDN serves `public/{lang}/index.html` for `/{lang}/` and falls back to `public/index.html` (English) for `/{lang}/{route}` paths (e.g. `/es/generator`). The client-side router detects the locale from the URL and uses `/js/titles.js` to look up the per-locale title for the page being viewed, so the browser tab always shows the right title even when the static fallback served the English index.html.

**Re-running the build:** `python3 i18n/build.py` reads `public/index.html` (English) and writes `public/{lang}/index.html` for each of the 17 locales. The translations live in `i18n/build.py` as `TIER1` and `TIER2` dicts; to add or improve a translation, edit the relevant language's dict and re-run.

## AdSense prerequisites

This is the checklist for going live with Google AdSense. Everything except the publisher ID is in place.

| Item | Where | Status |
|------|-------|--------|
| Privacy Policy | `/privacy` | ✅ Drafted, **needs lawyer review** |
| Terms of Service | `/terms` | ✅ Drafted, **needs lawyer review** |
| Affiliation disclaimer | Home hero, generator section, About, Terms, footer | ✅ Visible on every page |
| `ads.txt` at the root | `public/ads.txt` | ✅ Placeholder; replace `pub-0000000000000000` with your real AdSense publisher ID |
| Substantive content | About / FAQ / blog | ⚠️ Placeholders — fill these in before applying |
| Navigation | Top nav links to Privacy, Terms, About, FAQ, Home | ✅ Present |

### Replace the publisher ID

Edit `public/ads.txt` and put your real AdSense publisher ID on the `google.com` line. Format: `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fecaa2a87f`. The `placeholder` line is harmless and can stay until you get the real entry.

## Brand & trademark

- "Handle" is the brand. It is **not** affiliated with, endorsed by, or sponsored by TikTok or ByteDance Ltd. "TikTok" is a trademark of ByteDance Ltd; we use it descriptively (the tool checks usernames on TikTok) under fair use.
- The brand is a generic English word. It is unclaimed in most TLDs as of writing, but check USPTO and EUIPO before you commit.
- A "not affiliated" disclaimer appears on the home hero, the generator section, the FAQ, the About, the Terms, and the footer. We don't use the TikTok logo or wordmark anywhere. The pink brand color is our own choice and isn't meant to mimic TikTok.

## What the MVP doesn't do (yet)

- **Cross-platform checks** — the architecture is there (`BaseChecker` is platform-agnostic) but only TikTok is wired. Instagram, YouTube, and X are next.
- **Blog and pSEO pages** — explicitly out of scope. The plan is in the report that came with this build.
- **Email capture / newsletter** — not in the MVP.
- **AdSense / Ezoic placement** — the ad slots aren't placed. The page is structured to drop in display units without redesigning the layout. Update `public/ads.txt` with the real publisher ID before applying.
- **Authorship / E-E-A-T signals** — there are no author bios, no `Person` schema, no about-entity behind a real name yet. Add these before you start chasing ranking.

## Known gotchas

- The sandbox where this was built couldn't reach TikTok's oEmbed endpoint directly (network restrictions), so the live check is unverified-in-sandbox. Run it on a normal network and it should work.
- Some fonts in the Unicode converter fall back to the original character for inputs the Unicode range doesn't cover (e.g. cyrillic, emoji, accented Latin). That's intentional.
- TikTok's rules can change. The `RULES` object in `lib/generator.js` is the single source of truth; update it in one place.
- The Privacy Policy and Terms of Service are working drafts, not legal advice. Have a lawyer review them before going public.
- The `ads.txt` currently has `pub-0000000000000000` as a placeholder. AdSense will reject the file until that's replaced.
