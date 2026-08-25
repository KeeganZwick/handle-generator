// lib/availability.js
//
// Pluggable availability-check architecture.
//
// The interface is intentionally tiny so a new backend (oEmbed, direct probe,
// third-party API, headless browser) can be added or swapped without touching
// the route, the cache, or the frontend.
//
// Every checker returns a uniform result envelope so the UI can render the
// status ("Likely available" / "Likely taken" / "Unknown") without caring
// which backend produced it. Confidence is the checker's own self-rating;
// the UI surfaces it as wording, not a numeric score.

'use strict';

const RESULT = {
  LIKELY_AVAILABLE: 'likely_available',
  LIKELY_TAKEN: 'likely_taken',
  UNVERIFIED: 'unverified',
};

class BaseChecker {
  constructor(name) {
    this.name = name;
  }

  // Subclasses MUST return a normalized result. Throwing is allowed and the
  // CompositeChecker will fall through to the next backend.
  async check(handle) {
    throw new Error(`checker "${this.name}" did not implement check()`);
  }

  // Subclasses can override to indicate they're confident in their verdict.
  confidence() {
    return 'medium';
  }

  _result({ handle, status, confidence, profileUrl, profileName, note }) {
    return {
      handle: String(handle || '').toLowerCase(),
      status,
      confidence: confidence || 'medium',
      checkedAt: new Date().toISOString(),
      backend: this.name,
      profileUrl: profileUrl || null,
      profileName: profileName || null,
      note: note || null,
    };
  }
}

// --- Backend: TikTok oEmbed ----------------------------------------------------
//
// URL: https://www.tiktok.com/oembed?url=https://www.tiktok.com/@handle
//
// Returns 200 with JSON { author_name, author_url, ... } for a public,
// resolvable account. Returns 404 (or 400 in some regions) for missing
// handles. No public rate-limit figure is published.
//
// Pros: official-ish endpoint, low scrape footprint, simple status code.
// Cons: no rate-limit transparency; some private accounts return 404 even
// when the handle is technically taken; brief 503 bursts happen during
// edge incidents.
class TikTokOEmbedChecker extends BaseChecker {
  constructor({ timeoutMs = 4000 } = {}) {
    super('tiktok-oembed');
    this.timeoutMs = timeoutMs;
  }

  async check(handle) {
    const h = String(handle || '').trim().toLowerCase();
    if (!h) return this._result({ handle, status: RESULT.UNVERIFIED, note: 'empty handle' });
    if (!/^[a-z0-9._]{2,24}$/.test(h)) {
      return this._result({ handle: h, status: RESULT.UNVERIFIED, note: 'invalid format' });
    }
    const url = `https://www.tiktok.com/oembed?url=${encodeURIComponent(`https://www.tiktok.com/@${h}`)}`;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const res = await fetch(url, {
        method: 'GET',
        signal: controller.signal,
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; HandleBot/0.1; +https://example.com/handle)',
          'Accept': 'application/json',
        },
      });
      if (res.status === 200) {
        const body = await res.json().catch(() => ({}));
        return this._result({
          handle: h,
          status: RESULT.LIKELY_TAKEN,
          confidence: 'medium',
          profileUrl: `https://www.tiktok.com/@${h}`,
          profileName: body.author_name || null,
        });
      }
      if (res.status === 404 || res.status === 400) {
        return this._result({ handle: h, status: RESULT.LIKELY_AVAILABLE, confidence: 'medium' });
      }
      return this._result({ handle: h, status: RESULT.UNVERIFIED, note: `oembed status ${res.status}` });
    } catch (e) {
      return this._result({ handle: h, status: RESULT.UNVERIFIED, note: `oembed ${e.name || 'error'}` });
    } finally {
      clearTimeout(timer);
    }
  }
}

// --- Backend: Direct probe of tiktok.com/@handle ------------------------------
//
// Fetch the profile page and inspect the response. TikTok returns a
// JS-rendered SPA, so a status code alone is not reliable; we look for the
// canonical "couldn't find this account" / empty data signal in the HTML.
//
// Pros: no third-party dependency.
// Cons: brittle (TikTok's HTML changes); higher risk of being rate-limited
// or temporarily blocked from a single egress IP; closer to scraping, which
// is the greyest area of TikTok's TOS. Use as a fallback only.
class TikTokDirectChecker extends BaseChecker {
  constructor({ timeoutMs = 5000 } = {}) {
    super('tiktok-direct');
    this.timeoutMs = timeoutMs;
  }

  async check(handle) {
    const h = String(handle || '').trim().toLowerCase();
    if (!h) return this._result({ handle, status: RESULT.UNVERIFIED, note: 'empty handle' });
    if (!/^[a-z0-9._]{2,24}$/.test(h)) {
      return this._result({ handle: h, status: RESULT.UNVERIFIED, note: 'invalid format' });
    }
    const url = `https://www.tiktok.com/@${h}`;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const res = await fetch(url, {
        method: 'GET',
        redirect: 'follow',
        signal: controller.signal,
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml',
          'Accept-Language': 'en-US,en;q=0.9',
        },
      });
      const text = await res.text();
      const looksMissing = /couldn['’]?t find this account|user not found|page not available/i.test(text);
      const looksHydrated = /"uniqueId":"[^"]+"/.test(text) || /"userInfo":\s*\{/.test(text);
      if (looksMissing) {
        return this._result({ handle: h, status: RESULT.LIKELY_AVAILABLE, confidence: 'low' });
      }
      if (looksHydrated) {
        return this._result({ handle: h, status: RESULT.LIKELY_TAKEN, confidence: 'low' });
      }
      return this._result({ handle: h, status: RESULT.UNVERIFIED, note: 'direct probe inconclusive' });
    } catch (e) {
      return this._result({ handle: h, status: RESULT.UNVERIFIED, note: `direct ${e.name || 'error'}` });
    } finally {
      clearTimeout(timer);
    }
  }
}

// --- Cache wrapper ------------------------------------------------------------
//
// Same key in the same window returns the prior result and adds
// `cached: true` so the UI can show "(cached)".
class CacheWrapper {
  constructor(inner, { ttlMs = 5 * 60 * 1000, maxEntries = 1000 } = {}) {
    this.inner = inner;
    this.ttlMs = ttlMs;
    this.maxEntries = maxEntries;
    this.cache = new Map();
  }
  get name() { return `${this.inner.name}+cache`; }
  async check(handle) {
    const key = String(handle || '').toLowerCase();
    const now = Date.now();
    const cached = this.cache.get(key);
    if (cached && now - cached.ts < this.ttlMs) {
      return { ...cached.result, cached: true };
    }
    const result = await this.inner.check(handle);
    if (this.cache.size >= this.maxEntries) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, { ts: now, result });
    return result;
  }
}

// --- Composite: try each backend in order ------------------------------------
class CompositeChecker {
  constructor(checkers) {
    this.checkers = checkers;
  }
  get name() { return this.checkers.map(c => c.name).join('>'); }
  async check(handle) {
    let lastResult = null;
    for (const checker of this.checkers) {
      try {
        const result = await checker.check(handle);
        if (result && result.status !== RESULT.UNVERIFIED) return result;
        lastResult = result;
      } catch (e) {
        // ignore and try next
      }
    }
    return lastResult || {
      handle: String(handle || '').toLowerCase(),
      status: RESULT.UNVERIFIED,
      confidence: 'low',
      checkedAt: new Date().toISOString(),
      backend: this.name,
      note: 'all backends failed',
    };
  }
}

// --- Default wiring -----------------------------------------------------------
//
// Try oEmbed first (lighter footprint, less scraping-like). If it returns
// UNVERIFIED (e.g. 5xx, network blip, 429), fall through to direct probe.
// Cache successful results for 5 minutes; cache UNVERIFIED for 30 seconds so
// transient failures don't pin a false "Unable to verify" for too long.
function buildDefaultChecker() {
  return new CompositeChecker([
    new CacheWrapper(new TikTokOEmbedChecker(), { ttlMs: 5 * 60 * 1000 }),
    new CacheWrapper(new TikTokDirectChecker(), { ttlMs: 30 * 1000 }),
  ]);
}

module.exports = {
  BaseChecker,
  TikTokOEmbedChecker,
  TikTokDirectChecker,
  CacheWrapper,
  CompositeChecker,
  buildDefaultChecker,
  RESULT,
};
