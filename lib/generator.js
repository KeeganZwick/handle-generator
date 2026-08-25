// lib/generator.js
//
// TikTok username generator.
//
// Deterministic, no LLM. Wordlist + pattern engine, runs in milliseconds and
// costs nothing to operate. Every candidate is filtered against the
// current published TikTok username rules BEFORE it is returned.
//
// Current TikTok username rules (as of 2026-08-23, verify before launch):
//   - 2 to 24 characters
//   - letters, numbers, periods (.), underscores (_)
//   - case-insensitive
//   - cannot start or end with a period
//   - no consecutive periods
//   - cannot start or end with an underscore
// Sources: Hootsuite 100+ TikTok username ideas, QuickCounterTools 2026
// guide, HandleGrab 2026 rules. TikTok can change these at any time —
// re-verify on every release.

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

// Themed vibes: a curated pool of prefixes and suffixes for each.
const VIBE_TRAITS = {
  aesthetic:   { prefixes: ['soft', 'glow', 'lune', 'velvet', 'moss', 'opal', 'wild', 'honey'],  suffixes: ['core', 'daze', 'glow', 'muse', 'peach', 'aura', 'wisp', 'hymn'] },
  funny:       { prefixes: ['oops', 'noodle', 'pasta', 'waffle', 'oof', 'beep', 'sir', 'dude'],  suffixes: ['lol', 'oof', 'nope', 'yeet', 'haha', 'wut', 'bruh', 'oink'] },
  professional:{ prefixes: ['the', 'real', 'studio', 'pro', 'top'],                            suffixes: ['hq', 'lab', 'co', 'studio', 'pro', 'group', 'club', 'works'] },
  edgy:        { prefixes: ['void', 'grim', 'riot', 'venom', 'cold', 'iron', 'static', 'low'],  suffixes: ['xx', '666', 'grim', 'riot', 'ash', 'cult', 'wrath', 'raw'] },
  cute:        { prefixes: ['tiny', 'mini', 'sugar', 'bunny', 'peach', 'kitty', 'pom', 'cozy'], suffixes: ['bear', 'bean', 'bub', 'pie', 'kin', 'boo', 'puff', 'pop'] },
  mysterious:  { prefixes: ['odd', 'hex', 'crypt', 'veil', 'gray', 'lost', 'echo', 'nine'],    suffixes: ['xx', 'crypt', 'grey', 'veil', 'void', 'wisp', 'lore', 'oak'] },
  cool:        { prefixes: ['big', 'king', 'ace', 'gold', 'fly', 'vip', 'top', 'boss'],         suffixes: ['vibes', 'mode', 'crew', 'club', 'hq', 'life', 'era', 'wins'] },
  // New themed vibes
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

// Themed vibe keys, derived from the table above.
const THEMED_VIBES = Object.keys(VIBE_TRAITS);

// Generation mode switches — these are NOT themed word banks.
//   'none'   — skip the themed prefix/suffix pool entirely; use only
//              keyword + niche combinations and the structural patterns.
//   'random' — for each candidate, pick a random themed vibe, so a single
//              batch can mix vibes rather than sticking to one.
//   'unique' — bias toward the structural/unusual patterns (vowel-drop,
//              digit-append, doubled-keyword, underscore-join, plus a few
//              new ones), not a themed vocabulary.
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
  business:   ['hq', 'co', 'group', 'team', 'brand', 'firm', 'studio', 'co', 'group', 'pro'],
  general:    ['daily', 'vibes', 'era', 'life', 'world', 'story', 'space', 'zone', 'lab', 'house'],
};

// --- Validation ---------------------------------------------------------------

function isValidTikTokHandle(s) {
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

// --- Pattern engine -----------------------------------------------------------

function dedupe(arr) { return Array.from(new Set(arr)); }

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function pickFrom(arr, rng) { return arr[Math.floor(rng() * arr.length)]; }

// Pattern families ------------------------------------------------------------

function structuralPatterns(kw, nicheWords, rng, count) {
  const out = [];
  if (!kw) return out;

  if (kw.length >= RULES.minLen) out.push(kw);

  // keyword + niche word, niche + keyword
  for (let i = 0; i < Math.max(2, count); i++) out.push(kw + pickFrom(nicheWords, rng));
  for (let i = 0; i < Math.max(1, Math.floor(count / 2)); i++) out.push(pickFrom(nicheWords, rng) + kw);

  // Alliterative: keyword + niche word starting with the same letter
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
  // weight is 1 for normal generation, > 1 for the "unique" mode.
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

  // Heavy weights unlock the rarer patterns.
  if (w >= 2) {
    // Single-letter prefix (x_, z_, q_, j_, v_) — these read as intentionally stylized.
    const stylings = ['x', 'z', 'q', 'j', 'v'];
    for (let i = 0; i < w; i++) out.push(pickFrom(stylings, rng) + kw);

    // Letter-flip: swap the first and last character of the keyword.
    if (kw.length >= 3) {
      const flipped = kw[kw.length - 1] + kw.slice(1, -1) + kw[0];
      out.push(flipped);
    }

    // Leet substitutions. Only some — anything that would break TikTok's
    // character rules is filtered later, so this is a safe pre-pass.
    const leetMap = { a: '@', e: '3', i: '1', o: '0', s: '5' };
    let leet = '';
    for (const ch of kw) leet += (leetMap[ch] || ch);
    if (leet !== kw) out.push(leet);
  }

  return out;
}

function resolveVibeForCandidate(vibe, rng) {
  if (vibe === 'random') {
    return THEMED_VIBES[Math.floor(rng() * THEMED_VIBES.length)];
  }
  return vibe;
}

function resolveTraits(vibe) {
  if (!vibe || MODE_VIBES[vibe]) return null;
  if (VIBE_TRAITS[vibe]) return VIBE_TRAITS[vibe];
  return VIBE_TRAITS.cool;
}

// --- Public entry point -------------------------------------------------------

function generate({ keyword, category, vibe, count = 12, seed } = {}) {
  const kw = String(keyword || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  const cat = NICHE_WORDS[category] ? category : 'general';
  const nicheWords = NICHE_WORDS[cat];
  const rng = seed != null ? mulberry32(seed) : Math.random;
  const candidates = [];

  if (kw) {
    // Always-run structural patterns (keyword + niche combos, alliterative)
    for (const c of structuralPatterns(kw, nicheWords, rng, 4)) candidates.push(c);

    if (vibe === 'unique') {
      // Bias hard toward the structural/unusual patterns and sprinkle
      // themed patterns across all vibes.
      candidates.push(...unusualPatterns(kw, nicheWords, rng, 3));
      for (const v of THEMED_VIBES) {
        candidates.push(...themedPatterns(kw, VIBE_TRAITS[v], rng, 1));
      }
    } else if (vibe === 'random') {
      // For each themed candidate, pick a random vibe per item.
      for (let i = 0; i < 10; i++) {
        const v = resolveVibeForCandidate('random', rng);
        candidates.push(...themedPatterns(kw, VIBE_TRAITS[v], rng, 1));
      }
      // Light unusual pass to keep things from being all themed.
      candidates.push(...unusualPatterns(kw, nicheWords, rng, 1));
    } else {
      // 'none' or a specific themed vibe
      const traits = resolveTraits(vibe);
      if (traits) {
        candidates.push(...themedPatterns(kw, traits, rng, 5));
      }
      // Always allow the structural patterns + a touch of the unusual,
      // so a single batch has some variety even with a themed vibe.
      candidates.push(...unusualPatterns(kw, nicheWords, rng, 1));
    }
  } else {
    // No keyword — pure niche + vibe combos.
    if (vibe === 'random') {
      for (let i = 0; i < 8; i++) {
        const v = resolveVibeForCandidate('random', rng);
        candidates.push(...themedPatterns(null, VIBE_TRAITS[v], rng, 1));
      }
    } else if (vibe === 'unique') {
      // Heavier structural — double up on niche+niche combos.
      for (let i = 0; i < 6; i++) candidates.push(pickFrom(nicheWords, rng) + pickFrom(nicheWords, rng));
      for (let i = 0; i < 6; i++) {
        const v = pickFrom(THEMED_VIBES, rng);
        candidates.push(...themedPatterns(null, VIBE_TRAITS[v], rng, 1));
      }
    } else {
      const traits = resolveTraits(vibe);
      if (traits) {
        candidates.push(...themedPatterns(null, traits, rng, 8));
      } else {
        // 'none' with no keyword: just niche combinations
        for (let i = 0; i < 10; i++) candidates.push(pickFrom(nicheWords, rng) + pickFrom(nicheWords, rng));
      }
    }
  }

  // Filter to TikTok rules, dedupe (case-insensitive), shuffle, return N
  const valid = dedupe(candidates.map((c) => String(c).toLowerCase()).filter(isValidTikTokHandle));
  for (let i = valid.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [valid[i], valid[j]] = [valid[j], valid[i]];
  }

  return {
    handles: valid.slice(0, count),
    rulesVersion: '2026-08-23',
    rules: RULES,
  };
}

module.exports = {
  generate,
  isValidTikTokHandle,
  RULES,
  VIBE_TRAITS,
  THEMED_VIBES,
  MODE_VIBES,
  NICHE_WORDS,
};
