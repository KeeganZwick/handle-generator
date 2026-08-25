// /public/js/client-shim.js
//
// Canonical client-side surface for Handle.
//
// Exposes `window.__handleClient = { generate, check, isPreview }`.
//
//   generate({keyword, category, vibe, count})
//     Pure JS, mirrors lib/generator.js. Always available, even in the
//     static deploy.
//
//   check(handle)
//     Tries the real /api/check (works in the local Node build). If the
//     network call fails, returns a clearly-labeled preview-mode verdict
//     so the static deploy stays honest instead of faking a result.
//
// The previous version of this file patched window.fetch, which broke
// when the static host's SPA fallback returned 200 for any unknown path.
// The page's generator.js would then call fetch, the shim would pass it
// through, the real response would be HTML, and JSON parsing would fail.
// Pushing the API surface into a global object sidesteps the whole
// detection-vs-misdirection problem.

(function () {
  'use strict';

  const RULES = {
    minLen: 2,
    maxLen: 24,
    allowed: /^[a-z0-9._]+$/,
    noLeadingPeriod: true,
    noTrailingPeriod: true,
    noConsecutivePeriods: true,
    noLeadingUnderscore: true,
    noTrailingUnderscore: true,
  };

  const VIBE_TRAITS = {
    aesthetic:   { prefixes: ['soft', 'glow', 'lune', 'velvet', 'moss', 'opal', 'wild', 'honey'],  suffixes: ['core', 'daze', 'glow', 'muse', 'peach', 'aura', 'wisp', 'hymn'] },
    funny:       { prefixes: ['oops', 'noodle', 'pasta', 'waffle', 'oof', 'beep', 'sir', 'dude'],  suffixes: ['lol', 'oof', 'nope', 'yeet', 'haha', 'wut', 'bruh', 'oink'] },
    professional:{ prefixes: ['the', 'real', 'studio', 'pro', 'top'],                            suffixes: ['hq', 'lab', 'co', 'studio', 'pro', 'group', 'club', 'works'] },
    edgy:        { prefixes: ['void', 'grim', 'riot', 'venom', 'cold', 'iron', 'static', 'low'],  suffixes: ['xx', '666', 'grim', 'riot', 'ash', 'cult', 'wrath', 'raw'] },
    cute:        { prefixes: ['tiny', 'mini', 'sugar', 'bunny', 'peach', 'kitty', 'pom', 'cozy'], suffixes: ['bear', 'bean', 'bub', 'pie', 'kin', 'boo', 'puff', 'pop'] },
    mysterious:  { prefixes: ['odd', 'hex', 'crypt', 'veil', 'gray', 'lost', 'echo', 'nine'],    suffixes: ['xx', 'crypt', 'grey', 'veil', 'void', 'wisp', 'lore', 'oak'] },
    cool:        { prefixes: ['big', 'king', 'ace', 'gold', 'fly', 'vip', 'top', 'boss'],         suffixes: ['vibes', 'mode', 'crew', 'club', 'hq', 'life', 'era', 'wins'] },
    chill:       { prefixes: ['slow', 'lazy', 'soft', 'lofi', 'mellow', 'easy', 'calm', 'drift'], suffixes: ['vibe', 'wave', 'haze', 'drift', 'cozy', 'cloud', 'mood', 'breeze'] },
    smart:       { prefixes: ['genius', 'brainy', 'clever', 'wise', 'sage', 'shrewd', 'keen', 'sharp'], suffixes: ['mind', 'logic', 'lab', 'wit', 'spark', 'edge', 'think', 'iq'] },
    romantic:    { prefixes: ['sweet', 'tender', 'velvet', 'rose', 'sugar', 'heart', 'soft', 'lush'], suffixes: ['heart', 'rose', 'kiss', 'love', 'dear', 'dove', 'honey', 'petal'] },
    powerful:    { prefixes: ['king', 'queen', 'royal', 'alpha', 'prime', 'boss', 'top', 'apex'],  suffixes: ['reign', 'era', 'crown', 'rule', 'force', 'mode', 'dom', 'wins'] },
    gaming:      { prefixes: ['glitch', 'rage', 'clutch', 'pro', 'god', 'fps', 'respawn', 'spawn'], suffixes: ['gg', 'op', 'clutch', 'main', 'boss', 'win', 'god', 'rage'] },
    techy:       { prefixes: ['cyber', 'proto', 'neon', 'data', 'byte', 'dev', 'stack', 'loop'],  suffixes: ['dev', 'lab', 'ops', 'core', 'net', 'sys', 'data', 'tech'] },
    spooky:      { prefixes: ['crypt', 'haunt', 'ghost', 'bone', 'dead', 'eerie', 'witch', 'dusk'], suffixes: ['spook', 'haunt', 'grave', 'doom', 'shade', 'dark', 'hex', 'crypt'] },
    retro:       { prefixes: ['vintage', 'retro', 'throwback', 'classic', '80s', 'analog', 'old', 'neon'], suffixes: ['retro', 'vintage', 'vibe', 'classic', 'wave', 'tv', 'tape', 'rewind'] },
    wholesome:   { prefixes: ['sunny', 'happy', 'bright', 'kind', 'gentle', 'sweet', 'warm', 'cozy'], suffixes: ['joy', 'hug', 'smile', 'heart', 'shine', 'glow', 'sun', 'cheer'] },
    fantasy:     { prefixes: ['mage', 'elf', 'dragon', 'arcane', 'mystic', 'rune', 'fae', 'realm'],   suffixes: ['quest', 'realm', 'arcane', 'myth', 'rune', 'spell', 'craft', 'sage'] },
  };

  const THEMED_VIBES = Object.keys(VIBE_TRAITS);
  const MODE_VIBES = { none: 1, random: 1, unique: 1 };

  const NICHE_WORDS = {
    fitness:    ['fit', 'lift', 'gym', 'sweat', 'core', 'flex', 'run', 'pump', 'lean', 'pulse'],
    food:       ['bites', 'eats', 'yum', 'cook', 'chef', 'kitchen', 'spice', 'bake', 'taste', 'plate'],
    beauty:     ['glow', 'lashes', 'blush', 'tint', 'satin', 'gloss', 'velvet', 'rose', 'shade', 'bloom'],
    fashion:    ['style', 'fit', 'drip', 'label', 'thread', 'wear', 'couture', 'denim', 'silk', 'edit'],
    gaming:     ['plays', 'loot', 'pixel', 'quest', 'arcade', 'rage', 'clutch', 'spawn', 'respawn', 'noob'],
    tech:       ['code', 'dev', 'stack', 'byte', 'git', 'node', 'cloud', 'data', 'api', 'sql'],
    travel:     ['wander', 'voyage', 'trip', 'nomad', 'roam', 'globe', 'trail', 'tide', 'horizon', 'compass'],
    pets:       ['paws', 'furr', 'pup', 'kitty', 'bark', 'meow', 'wags', 'snout', 'whiskers', 'pounce'],
    dance:      ['moves', 'beat', 'groove', 'rhythm', 'step', 'flow', 'spin', 'vibe', 'jam', 'drop'],
    comedy:     ['joke', 'punch', 'gag', 'snort', 'wink', 'yeet', 'oof', 'lmao', 'bruh', 'face'],
    music:      ['tune', 'beat', 'note', 'chord', 'vibe', 'rhythm', 'loop', 'wave', 'bass', 'muse'],
    art:        ['ink', 'sketch', 'canvas', 'hue', 'brush', 'line', 'studio', 'frame', 'palette', 'craft'],
    education:  ['learn', 'study', 'notes', 'class', 'mind', 'spark', 'logic', 'idea', 'quiz', 'lab'],
    finance:    ['cents', 'stack', 'fund', 'capital', 'save', 'invest', 'wallet', 'ledger', 'cents', 'mint'],
    parenting:  ['mama', 'papa', 'mini', 'tiny', 'crew', 'house', 'tribe', 'cubs', 'nest', 'crew'],
    business:   ['hq', 'co', 'group', 'team', 'team', 'firm', 'studio', 'co', 'group', 'pro'],
    general:    ['daily', 'vibes', 'era', 'life', 'world', 'story', 'space', 'zone', 'lab', 'house'],
  };

  function isValidHandle(s) {
    if (typeof s !== 'string') return false;
    const h = s.toLowerCase();
    if (h.length < RULES.minLen || h.length > RULES.maxLen) return false;
    if (!RULES.allowed.test(h)) return false;
    if (RULES.noLeadingPeriod && h.startsWith('.')) return false;
    if (RULES.noTrailingPeriod && h.endsWith('.')) return false;
    if (RULES.noConsecutivePeriods && h.includes('..')) return false;
    if (RULES.noLeadingUnderscore && h.startsWith('_')) return false;
    if (RULES.noTrailingUnderscore && h.endsWith('_')) return false;
    return true;
  }

  function dedupe(arr) { return Array.from(new Set(arr)); }
  function pickFrom(arr, rng) { return arr[Math.floor(rng() * arr.length)]; }

  function structuralPatterns(kw, nicheWords, rng, count) {
    const out = [];
    if (!kw) return out;
    if (kw.length >= RULES.minLen) out.push(kw);
    for (let i = 0; i < Math.max(2, count); i++) out.push(kw + pickFrom(nicheWords, rng));
    for (let i = 0; i < Math.max(1, Math.floor(count / 2)); i++) out.push(pickFrom(nicheWords, rng) + kw);
    const sameStart = nicheWords.filter((w) => w[0] === kw[0]);
    if (sameStart.length) {
      out.push(kw + pickFrom(sameStart, rng));
      if (count >= 2) out.push(kw + pickFrom(sameStart, rng));
    }
    return out;
  }

  function themedPatterns(kw, traits, rng, count) {
    const out = [];
    if (!traits) return out;
    if (!kw) {
      for (let i = 0; i < count; i++) out.push(pickFrom(traits.prefixes, rng) + pickFrom(NICHE_WORDS.general, rng));
      for (let i = 0; i < count; i++) out.push(pickFrom(NICHE_WORDS.general, rng) + pickFrom(traits.suffixes, rng));
      return out;
    }
    for (let i = 0; i < Math.max(1, Math.floor(count / 2)); i++) {
      const pre = pickFrom(traits.prefixes, rng);
      if (pre !== kw) out.push(pre + kw);
    }
    for (let i = 0; i < count; i++) out.push(kw + pickFrom(traits.suffixes, rng));
    return out;
  }

  function unusualPatterns(kw, nicheWords, rng, weight) {
    const out = [];
    if (!kw) return out;
    const w = weight || 1;
    if (kw.length >= 5) {
      for (let i = 0; i < w; i++) out.push(kw.replace(/[aeiou]/, ''));
    }
    if (kw.length <= 18) {
      for (let i = 0; i < w; i++) out.push(kw + (Math.floor(rng() * 90) + 10));
    }
    if (kw.length <= 18) {
      for (let i = 0; i < w; i++) out.push(kw + '_' + pickFrom(nicheWords, rng));
    }
    if (kw.length * 2 <= RULES.maxLen) {
      for (let i = 0; i < w; i++) out.push(kw + kw);
    }
    if (w >= 2) {
      const stylings = ['x', 'z', 'q', 'j', 'v'];
      for (let i = 0; i < w; i++) out.push(pickFrom(stylings, rng) + kw);
      if (kw.length >= 3) {
        const flipped = kw[kw.length - 1] + kw.slice(1, -1) + kw[0];
        out.push(flipped);
      }
      const leetMap = { a: '@', e: '3', i: '1', o: '0', s: '5' };
      let leet = '';
      for (const ch of kw) leet += (leetMap[ch] || ch);
      if (leet !== kw) out.push(leet);
    }
    return out;
  }

  function resolveVibeForCandidate(vibe, rng) {
    if (vibe === 'random') return THEMED_VIBES[Math.floor(rng() * THEMED_VIBES.length)];
    return vibe;
  }

  function resolveTraits(vibe) {
    if (!vibe || MODE_VIBES[vibe]) return null;
    if (VIBE_TRAITS[vibe]) return VIBE_TRAITS[vibe];
    return VIBE_TRAITS.cool;
  }

  function generate({ keyword, category, vibe, count = 12 } = {}) {
    const kw = String(keyword || '').toLowerCase().replace(/[^a-z0-9]/g, '');
    const cat = NICHE_WORDS[category] ? category : 'general';
    const nicheWords = NICHE_WORDS[cat];
    const rng = Math.random;
    const candidates = [];

    if (kw) {
      for (const c of structuralPatterns(kw, nicheWords, rng, 4)) candidates.push(c);

      if (vibe === 'unique') {
        candidates.push(...unusualPatterns(kw, nicheWords, rng, 3));
        for (const v of THEMED_VIBES) {
          candidates.push(...themedPatterns(kw, VIBE_TRAITS[v], rng, 1));
        }
      } else if (vibe === 'random') {
        for (let i = 0; i < 10; i++) {
          const v = resolveVibeForCandidate('random', rng);
          candidates.push(...themedPatterns(kw, VIBE_TRAITS[v], rng, 1));
        }
        candidates.push(...unusualPatterns(kw, nicheWords, rng, 1));
      } else {
        const traits = resolveTraits(vibe);
        if (traits) candidates.push(...themedPatterns(kw, traits, rng, 5));
        candidates.push(...unusualPatterns(kw, nicheWords, rng, 1));
      }
    } else {
      if (vibe === 'random') {
        for (let i = 0; i < 8; i++) {
          const v = resolveVibeForCandidate('random', rng);
          candidates.push(...themedPatterns(null, VIBE_TRAITS[v], rng, 1));
        }
      } else if (vibe === 'unique') {
        for (let i = 0; i < 6; i++) candidates.push(pickFrom(nicheWords, rng) + pickFrom(nicheWords, rng));
        for (let i = 0; i < 6; i++) {
          const v = pickFrom(THEMED_VIBES, rng);
          candidates.push(...themedPatterns(null, VIBE_TRAITS[v], rng, 1));
        }
      } else {
        const traits = resolveTraits(vibe);
        if (traits) candidates.push(...themedPatterns(null, traits, rng, 8));
        else for (let i = 0; i < 10; i++) candidates.push(pickFrom(nicheWords, rng) + pickFrom(nicheWords, rng));
      }
    }

    const valid = dedupe(candidates.map((c) => String(c).toLowerCase()).filter(isValidHandle));
    for (let i = valid.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [valid[i], valid[j]] = [valid[j], valid[i]];
    }
    return { handles: valid.slice(0, count), rulesVersion: '2026-08-24', rules: RULES };
  }

  function checkStub(handle, note) {
    return {
      handle: String(handle || '').toLowerCase(),
      status: 'unverified',
      confidence: 'low',
      checkedAt: new Date().toISOString(),
      backend: 'preview-no-backend',
      profileUrl: null,
      profileName: null,
      note: note || 'preview deploy — run locally for the live availability check',
    };
  }

  async function check(handle) {
    if (!handle) return checkStub(handle, 'empty handle');
    try {
      const res = await fetch('/api/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ handle }),
      });
      if (res.ok) {
        const ct = res.headers.get('content-type') || '';
        if (ct.indexOf('application/json') >= 0) {
          const data = await res.json();
          if (data && data.status) return data;
        }
      }
    } catch (e) {
      // Network failure, SPA-fallback HTML, CORS — all fall through here.
    }
    return checkStub(handle);
  }

  function detectLocale() {
    var p = (typeof window !== 'undefined' && window.location && window.location.pathname) || '/';
    var m = p.match(/^\/([a-z]{2})(\/|$)/);
    if (m && ['es','de','fr','it','pt','nl','pl','ru','zh','vi','id','ms','tl','hi','bn','ur','ar'].indexOf(m[1]) !== -1) {
      return m[1];
    }
    return 'en';
  }

  window.__handleClient = {
    generate,
    check,
    isPreview: false,
    locale: detectLocale(),
  };

  (async function () {
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ping: 1 }),
      });
      const ct = res.headers.get('content-type') || '';
      if (res.ok && ct.indexOf('application/json') >= 0) {
        window.__handleClient.isPreview = false;
        return;
      }
    } catch (e) {
      // fall through
    }
    window.__handleClient.isPreview = true;
    document.addEventListener('DOMContentLoaded', showPreviewBanner);
  })();

  function showPreviewBanner() {
    const banner = document.createElement('div');
    banner.style.cssText = [
      'position:fixed', 'bottom:14px', 'left:14px', 'right:14px',
      'max-width:680px', 'margin:0 auto',
      'background:#fff5e0', 'border:1px solid #f0e2b0',
      'border-radius:12px', 'padding:10px 14px',
      'font-family:var(--font)', 'font-size:13px', 'color:#92590f',
      'z-index:9999', 'box-shadow:0 8px 24px -10px rgba(0,0,0,.15)',
      'text-align:center',
    ].join(';');
    banner.innerHTML = '<strong>Preview deploy.</strong> Generation works in the browser; the live availability check needs the local Node backend — <code>npm install &amp;&amp; npm start</code>. Every result will read "Unknown" until then.';
    document.body.appendChild(banner);
  }
})();
