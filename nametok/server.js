// server.js
//
// Handle — TikTok username generator with pluggable availability checks.

'use strict';

const path = require('path');
const fs = require('fs');
const express = require('express');
const { generate } = require('./lib/generator');
const { buildDefaultChecker } = require('./lib/availability');

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';

const checker = buildDefaultChecker();
const app = express();

// --- Content-Security-Policy --------------------------------------------------
//
// Defense-in-depth on the local Node build. The static deploy uses a
// <meta http-equiv="Content-Security-Policy"> in index.html so it works
// without a server. The local build can set a strict header on every
// response, with a per-request nonce that whitelists our own inline
// scripts and blocks any injected inline script (like the static-host
// platform's "Created by MiniMax Agent" injection, if it were ever
// applied to the local build).
//
// `'self'` allows our /js/* and /css/* external scripts/styles.
// No `'unsafe-inline'` for scripts — only our own inline <script>s with
// a matching nonce may execute.
function makeNonce() {
  return require('crypto').randomBytes(16).toString('base64');
}
app.use((req, res, next) => {
  const nonce = makeNonce();
  res.locals.cspNonce = nonce;
  res.set(
    'Content-Security-Policy',
    [
      `default-src 'self'`,
      `script-src 'self' 'nonce-${nonce}'`,
      `style-src 'self' 'unsafe-inline'`,
      `img-src 'self' data: https:`,
      `connect-src 'self' https://www.tiktok.com`,
      `base-uri 'self'`,
      `form-action 'self'`,
      `frame-ancestors 'none'`,
    ].join('; ')
  );
  next();
});

app.use(express.json({ limit: '32kb' }));

// --- Home (/) ----------------------------------------------------------------
//
// Must be registered BEFORE the static middleware so the static file
// server doesn't intercept / with the raw index.html (no nonce = blocked
// by the strict CSP we set above).
const HOME_META = {
  title: 'Handle — Free TikTok Username Generator with Availability Check',
  description: 'Generate unique TikTok username ideas and check live availability on TikTok. Free, no signup, no limits.',
  canonical: '/',
};
app.get('/', (req, res) => {
  res.set('Content-Type', 'text/html; charset=utf-8');
  res.send(injectMeta(loadIndexHtml(), HOME_META, res.locals.cspNonce));
});

app.use(express.static(path.join(__dirname, 'public'), {
  extensions: ['html'],
  maxAge: '1h',
}));

// --- API: generate -----------------------------------------------------------
//
// POST /api/generate
// body: { keyword, category, vibe, count }
// returns: { handles: [...], rulesVersion, rules }
app.post('/api/generate', (req, res) => {
  try {
    const { keyword, category, vibe, count } = req.body || {};
    const out = generate({ keyword, category, vibe, count: Math.min(Math.max(count | 0 || 12, 1), 24) });
    res.json(out);
  } catch (e) {
    res.status(500).json({ error: 'generate_failed', message: e.message });
  }
});

// --- API: check -------------------------------------------------------------
//
// POST /api/check
// body: { handle, platform }
// returns: normalized availability envelope
//
// Rate limit: simple in-process token bucket. 60 checks / minute / IP.
// This is intentionally conservative — TikTok's anti-abuse will throttle
// (or temporarily block) an egress IP that hammers the oEmbed endpoint,
// so a single bad client can take the whole site down. If you put this
// on a public server, raise the cap, add per-handle debouncing on the
// client, and consider queueing checks to a worker.
app.post('/api/check', async (req, res) => {
  try {
    const handle = String((req.body || {}).handle || '').trim();
    if (!handle) {
      return res.status(400).json({ error: 'empty_handle' });
    }
    if (!/^[a-z0-9._]{2,24}$/.test(handle.toLowerCase())) {
      return res.status(400).json({ error: 'invalid_format' });
    }
    if (!bucketAllow(req.ip)) {
      return res.status(429).json({ error: 'rate_limited' });
    }
    const result = await checker.check(handle);
    res.json(result);
  } catch (e) {
    res.status(500).json({ error: 'check_failed', message: e.message });
  }
});

// --- Lightweight in-memory rate limiter --------------------------------------

const BUCKETS = new Map();
const RATE_LIMIT = { capacity: 60, refillPerSec: 1 };
function bucketAllow(key) {
  const now = Date.now();
  const b = BUCKETS.get(key) || { tokens: RATE_LIMIT.capacity, last: now };
  const elapsed = (now - b.last) / 1000;
  b.tokens = Math.min(RATE_LIMIT.capacity, b.tokens + elapsed * RATE_LIMIT.refillPerSec);
  b.last = now;
  if (b.tokens < 1) {
    BUCKETS.set(key, b);
    return false;
  }
  b.tokens -= 1;
  BUCKETS.set(key, b);
  return true;
}

// --- Per-route meta ----------------------------------------------------------
//
// The static deploy can't inject per-route meta (no server, single HTML
// file). The local Node build can: we read public/index.html once, cache
// it, and on /generator, /faq, /about, /privacy, /terms rewrite the
// <title>, <meta name="description">, and <link rel="canonical"> tags
// in place. Home is served straight from the static middleware with
// the meta it shipped with.

const ROUTE_META = {
  generator: {
    title: 'TikTok Username Generator — Handle',
    description: "Free TikTok username generator. Type a keyword, pick a niche and a vibe, get 10–20 handle ideas that follow TikTok's rules, and check availability on TikTok. No signup, no limits.",
    canonical: '/generator',
  },
  faq: {
    title: 'FAQ — Handle',
    description: "Frequently asked questions about the Handle TikTok username generator: how the availability check works, what the rules are, and how to pick a handle that won't get taken.",
    canonical: '/faq',
  },
  about: {
    title: 'About — Handle',
    description: "About Handle: a free TikTok username generator that does the boring part for you — checking which names are actually available on TikTok.",
    canonical: '/about',
  },
  privacy: {
    title: 'Privacy Policy — Handle',
    description: "How Handle handles your data. The short version: nothing identifying is collected, cookies are not set by the core tool, and TikTok's own privacy policy governs what they see in availability-check requests.",
    canonical: '/privacy',
  },
  terms: {
    title: 'Terms of Service — Handle',
    description: "Terms of Service for Handle, the free TikTok username generator. Includes the no-affiliation-with-TikTok statement, the no-warranty-on-verdicts clause, and the no-trademark-search disclaimer.",
    canonical: '/terms',
  },
};

const INDEX_HTML_PATH = path.join(__dirname, 'public', 'index.html');
let cachedIndexHtml = null;
function loadIndexHtml() {
  if (cachedIndexHtml === null) {
    cachedIndexHtml = fs.readFileSync(INDEX_HTML_PATH, 'utf8');
  }
  return cachedIndexHtml;
}

function injectMeta(html, meta, nonce) {
  let out = html.replace(/<title>[^<]*<\/title>/, '<title>' + escapeHtml(meta.title) + '</title>');
  out = out.replace(
    /<meta name="description" content="[^"]*">/,
    '<meta name="description" content="' + escapeAttr(meta.description) + '">'
  );
  out = out.replace(
    /<link rel="canonical" href="[^"]*">/,
    '<link rel="canonical" href="' + escapeAttr(meta.canonical) + '">'
  );
  out = out.replace(
    /<meta property="og:title" content="[^"]*">/,
    '<meta property="og:title" content="' + escapeAttr(meta.title) + '">'
  );
  out = out.replace(
    /<meta property="og:description" content="[^"]*">/,
    '<meta property="og:description" content="' + escapeAttr(meta.description) + '">'
  );
  // Add the nonce to the inline route-detection script so the strict
  // CSP header we set above allows it. The static deploy's meta-CSP
  // uses a SHA-256 hash; the local build uses a nonce. Both work,
  // both block the platform's injected script.
  if (nonce) {
    out = out.replace(
      /<script>(\s*\(function \(\) \{\s*var path = window\.location)/,
      '<script nonce="' + escapeAttr(nonce) + '">$1'
    );
  }
  return out;
}

function escapeHtml(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function escapeAttr(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;'); }

// --- SPA fallback ------------------------------------------------------------
//
// The frontend is a single-page app: one index.html with six sections that
// the client-side router toggles. /generator, /faq, /about, /privacy,
// /terms are real URLs (browser back/forward, shareable, bookmarkable)
// but they all serve the same index.html. This catch-all makes that work
// in local dev exactly like it does on the static deploy host, with the
// right per-route meta so crawlers and `view-source:` see something
// route-specific.

const SPA_ROUTE = /^\/(generator|faq|about|privacy|terms)\/?$/;
app.get(SPA_ROUTE, (req, res) => {
  const route = req.path.replace(/^\/|\/$/g, '');
  const meta = ROUTE_META[route];
  if (!meta) {
    return res.sendFile(INDEX_HTML_PATH);
  }
  res.set('Content-Type', 'text/html; charset=utf-8');
  res.send(injectMeta(loadIndexHtml(), meta, res.locals.cspNonce));
});

// --- 404 catch-all -----------------------------------------------------------
//
// Anything we don't recognize gets a real 404 status code (good for search
// engines) with the SPA index.html — the client-side router will detect
// the unknown path and show the in-page 404 section.
app.get(/.*/, (req, res) => {
  if (req.method !== 'GET') return res.status(404).end();
  res.status(404);
  res.set('Content-Type', 'text/html; charset=utf-8');
  res.sendFile(INDEX_HTML_PATH);
});

// --- Server ------------------------------------------------------------------

app.listen(PORT, HOST, () => {
  console.log(`Handle listening on http://${HOST}:${PORT}`);
  console.log(`  Home:      http://${HOST}:${PORT}/`);
  console.log(`  Generator: http://${HOST}:${PORT}/generator`);
  console.log(`  FAQ:       http://${HOST}:${PORT}/faq`);
  console.log(`  About:     http://${HOST}:${PORT}/about`);
  console.log(`  Privacy:   http://${HOST}:${PORT}/privacy`);
  console.log(`  Terms:     http://${HOST}:${PORT}/terms`);
});
