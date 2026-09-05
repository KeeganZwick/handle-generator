// server.js
//
// Handle — TikTok username generator with pluggable availability checks.

'use strict';

const path = require('path');
const fs = require('fs');
const express = require('express');
const compression = require('compression');
const { generate } = require('./lib/generator');
const { buildDefaultChecker } = require('./lib/availability');

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '127.0.0.1';

// Production site URL — single source of truth for absolute canonicals
// in the meta objects below. Update this if the domain ever changes.
const SITE_URL = 'https://gethandlenames.com';

const checker = buildDefaultChecker();
const app = express();

// --- Compression -------------------------------------------------------------
//
// gzip (and brotli if accepted) every text response. ~70% size reduction on
// HTML/CSS/JS, so the network cost of the SPA shell drops from ~340KB to
// ~95KB. The compression middleware is added FIRST so it wraps every
// downstream response, including the per-route HTML and the static assets.
app.use(compression({
  // Skip already-compressed assets (images, fonts). Compression won't help
  // on those and just wastes CPU. By MIME we keep it conservative.
  filter: (req, res) => {
    const ct = res.getHeader('content-type') || '';
    if (ct.match(/image|font|video|audio/)) return false;
    // Default: compress everything else
    return compression.filter(req, res);
  },
  level: 6, // 1-9; 6 is the default zlib level, good speed/ratio balance
  threshold: 512, // Don't compress tiny responses (<512 bytes)
}));

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
      // AdSense requires 'unsafe-inline' for its dynamic injection
      // (and our own nonce-tagged script). The nonce is more specific and
      // is preferred when the browser sees both, but 'unsafe-inline' is
      // the documented fallback AdSense needs.
      `script-src 'self' 'nonce-${nonce}' 'unsafe-inline' https://pagead2.googlesyndication.com https://*.googlesyndication.com https://*.googletagservices.com https://*.google https://*.adtrafficquality.google https://fundingchoicesmessages.google.com https://partner.googleadservices.com https://adservice.google.com`,
      `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com`,
      `font-src 'self' https://fonts.gstatic.com`,
      `img-src 'self' data: https:`,
      `connect-src 'self' https://www.tiktok.com https://*.google.com https://*.doubleclick.net https://*.googlesyndication.com https://pagead2.googlesyndication.com https://*.google https://*.adtrafficquality.google https://fundingchoicesmessages.google.com https://partner.googleadservices.com https://adservice.google.com`,
      `frame-src 'self' https://*.googlesyndication.com https://*.doubleclick.net https://*.google.com https://*.google https://*.adtrafficquality.google https://fundingchoicesmessages.google.com`,
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
  canonical: SITE_URL + '/',
};
app.get('/', (req, res) => {
  res.set('Content-Type', 'text/html; charset=utf-8');
  res.send(stripPerRouteTemplates(rewriteHreflang(
    stripMetaCsp(
      addCspNoncesToInlineScripts(
        injectMeta(loadIndexHtml(), HOME_META, res.locals.cspNonce),
        res.locals.cspNonce
      )
    ),
    'home'
  )));
});

// --- Per-route HTML middleware ----------------------------------------------
//
// Intercepts HTML page requests for the 6 SPA routes (home + 5) in all 18
// languages. Without this, express.static would serve the per-page files
// directly with their hardcoded canonical but stale home-page hreflang.
// This middleware applies the right canonical + hreflang for the current
// route before responding, so crawlers and direct URL hits see consistent
// per-route meta.
//
// Falls through to express.static for non-SPA paths (CSS, JS, images, etc.).
const SPA_PATH = /^\/(?:([a-z]{2})\/)?(?:(home|generator|faq|about|privacy|terms))?\/?$/;
app.use((req, res, next) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') return next();
  const m = req.path.match(SPA_PATH);
  if (!m) return next();

  const lang = m[1] || 'en';
  const route = m[2] || 'home';

  let filePath;
  if (route === 'home') {
    filePath = lang === 'en'
      ? path.join(__dirname, 'public', 'index.html')
      : path.join(__dirname, 'public', lang, 'index.html');
  } else {
    filePath = lang === 'en'
      ? path.join(__dirname, 'public', route, 'index.html')
      : path.join(__dirname, 'public', lang, route, 'index.html');
  }
  if (!fs.existsSync(filePath)) return next();

  let html = fs.readFileSync(filePath, 'utf8');

  // Add the per-request CSP nonce to every <script> tag that doesn't
  // already have one. We have a few small inline scripts in the head
  // (route detection, AdSense config placeholder) that all need the
  // same nonce so the browser lets them run. We use a function
  // callback so we can preserve any existing attributes (e.g. JSON-LD
  // scripts that have type="application/ld+json").
  if (res.locals.cspNonce) {
    const nonceAttr = ' nonce="' + escapeAttr(res.locals.cspNonce) + '"';
    html = html.replace(
      /<script([^>]*)>/g,
      (match, attrs) => /\snonce=/.test(attrs) ? match : '<script' + nonceAttr + attrs + '>'
    );
  }

  // Apply per-route meta (canonical + title + description)
  if (lang === 'en') {
    const meta = route === 'home' ? HOME_META : ROUTE_META[route];
    if (meta) html = injectMeta(html, meta, res.locals.cspNonce);
  } else {
    const localeRouteMeta = LOCALE_META[lang] && LOCALE_META[lang][route];
    if (localeRouteMeta) html = injectMeta(html, localeRouteMeta, res.locals.cspNonce);
  }

  // Add CSP nonce to any other inline scripts (e.g. AdSense config
  // placeholder) that don't already have one.
  html = addCspNoncesToInlineScripts(html, res.locals.cspNonce);

  // Strip the meta CSP from the source HTML. The HTTP header (set by
  // the upstream middleware) is the source of truth for CSP on this
  // Express server. Keeping both would let the meta CSP (which uses
  // an old SHA-256 hash) reject any new inline scripts that get a nonce.
  html = stripMetaCsp(html);

  // Rewrite hreflang to point to the current route
  html = rewriteHreflang(html, route);
  // Strip the inert <template data-page-canonical> and
  // <template data-page-hreflang> blocks. They were placeholders for
  // a client-side router swap that we no longer do.
  html = stripPerRouteTemplates(html);

  res.set('Content-Type', 'text/html; charset=utf-8');
  res.send(html);
});

// --- Static assets with long-cache + separate per-type config -----------------
//
// express.static is mounted twice with different cache policies:
//   1. /css/ and /js/ → 1 year, immutable. These are content-hashed at
//      build time (or, in our case, versioned by being minified into
//      `*.min.css` / `*.min.js`). When a new version ships, the HTML
//      references a new path and the browser's old cache is bypassed.
//   2. Everything else (HTML, images, sitemap, robots.txt) → 1 hour. HTML
//      changes with every deploy; sitemap updates with new per-locale
//      URLs; 1h is short enough to pick up changes but long enough to
//      keep the network cost down on repeat visits.
// The middleware order matters: the more-specific /css/ and /js/ handlers
// run first; the catch-all express.static runs second for any path that
// didn't match.

const ONE_YEAR = '1y';
const ONE_HOUR = '1h';

// Long-cache static assets: CSS, JS, fonts. These are content-stable;
// new versions ship as new files (style.min.css, *.min.js, etc.) so
// a year-long cache is safe.
app.use('/css', express.static(path.join(__dirname, 'public', 'css'), {
  maxAge: ONE_YEAR,
  immutable: true,
  setHeaders: (res) => {
    res.setHeader('Cache-Control', `public, max-age=${60 * 60 * 24 * 365}, immutable`);
  },
}));
app.use('/js', express.static(path.join(__dirname, 'public', 'js'), {
  maxAge: ONE_YEAR,
  immutable: true,
  setHeaders: (res) => {
    res.setHeader('Cache-Control', `public, max-age=${60 * 60 * 24 * 365}, immutable`);
  },
}));

// Catch-all static for everything else (HTML, images, favicon, og-image,
// sitemap.xml, robots.txt, ads.txt, per-page files). Short cache.
app.use(express.static(path.join(__dirname, 'public'), {
  extensions: ['html'],
  maxAge: ONE_HOUR,
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
    description: "Free TikTok username generator. Type a keyword, pick a niche and a vibe, get 10–20 unique TikTok username ideas that follow TikTok's rules, and check live availability on TikTok. No signup, no limits.",
    canonical: SITE_URL + '/generator',
  },
  faq: {
    title: 'TikTok Username Generator FAQ — Handle',
    description: "FAQ about the Handle TikTok username generator: how to pick a TikTok username that fits you, how the live availability check works, why verdicts say 'Likely available' and not 'Available', and the best TikTok username ideas for 2026.",
    canonical: SITE_URL + '/faq',
  },
  about: {
    title: 'About Handle — Free TikTok Username Generator',
    description: "About Handle: a free TikTok username generator with a live availability check on TikTok. 17 vibes, 17 niches, 17 languages, no signup. Built for creators, brands, and anyone who wants a handle that actually exists.",
    canonical: SITE_URL + '/about',
  },
  privacy: {
    title: 'Privacy Policy — Handle',
    description: "How Handle handles your data. The short version: nothing identifying is collected, cookies are not set by the core tool, and TikTok's own privacy policy governs what they see in availability-check requests.",
    canonical: SITE_URL + '/privacy',
  },
  terms: {
    title: 'Terms of Service — Handle',
    description: "Terms of Service for Handle, the free TikTok username generator. Includes the no-affiliation-with-TikTok statement, the no-warranty-on-verdicts clause, and the no-trademark-search disclaimer.",
    canonical: SITE_URL + '/terms',
  },
};

// --- Localized per-route meta -----------------------------------------------
//
// For the 17 localized routes (/es/generator, /de/faq, etc.) we have
// per-locale + per-route meta. The localized HTML files are static
// and already carry the right meta for the home page, but on the local
// Node build we can rewrite title/description/canonical per route
// within each locale — same pattern as the English routes above.
const LOCALE_META = {
  es: {
    generator: {
      title: 'Generador de Nombres para TikTok — Handle',
      description: 'Generador gratuito de nombres para TikTok. Escribe una palabra, elige un nicho y un estilo, obtén 10–20 ideas de usuario que cumplen las reglas de TikTok y comprueba disponibilidad en TikTok. Sin registro, sin límites.',
      canonical: SITE_URL + '/es/generator',
    },
    faq: {
      title: 'Preguntas Frecuentes sobre el Generador de Nombres para TikTok — Handle',
      description: 'Preguntas frecuentes sobre el generador de nombres para TikTok de Handle: cómo elegir un nombre que encaje contigo, cómo funciona la verificación de disponibilidad, y las mejores ideas de nombres para TikTok en 2026.',
      canonical: SITE_URL + '/es/faq',
    },
    about: {
      title: 'Sobre Handle — Generador Gratuito de Nombres para TikTok',
      description: 'Sobre Handle: un generador gratuito de nombres para TikTok con verificación de disponibilidad en TikTok. 17 estilos, 17 nichos, 17 idiomas, sin registro.',
      canonical: SITE_URL + '/es/about',
    },
    privacy: {
      title: 'Política de Privacidad — Handle',
      description: 'Cómo trata Handle tus datos. En resumen: no recopilamos datos personales identificables, no usamos cookies para la herramienta principal, y la política de privacidad de TikTok rige sobre lo que ellos ven.',
      canonical: SITE_URL + '/es/privacy',
    },
    terms: {
      title: 'Términos de Servicio — Handle',
      description: 'Términos de Servicio de Handle, el generador gratuito de nombres para TikTok. Incluye la declaración de no afiliación con TikTok, la cláusula de no garantía sobre las verificaciones, y el aviso de no búsqueda de marcas.',
      canonical: SITE_URL + '/es/terms',
    },
  },
  de: {
    generator: {
      title: 'TikTok-Namensgenerator — Handle',
      description: 'Kostenloser TikTok-Namensgenerator. Gib ein Stichwort ein, wähle eine Nische und einen Vibe, erhalte 10–20 TikTok-Nutzernamen-Ideen, die den Regeln entsprechen, und prüfe die Verfügbarkeit auf TikTok. Keine Anmeldung, keine Grenzen.',
      canonical: SITE_URL + '/de/generator',
    },
    faq: {
      title: 'FAQ zum TikTok-Namensgenerator — Handle',
      description: 'Häufige Fragen zum TikTok-Namensgenerator von Handle: wie man einen TikTok-Namen wählt, der zu einem passt, wie die Verfügbarkeitsprüfung funktioniert, und die besten TikTok-Namensideen für 2026.',
      canonical: SITE_URL + '/de/faq',
    },
    about: {
      title: 'Über Handle — Kostenloser TikTok-Namensgenerator',
      description: 'Über Handle: ein kostenloser TikTok-Namensgenerator mit Live-Verfügbarkeitsprüfung auf TikTok. 17 Vibes, 17 Nischen, 17 Sprachen, keine Anmeldung.',
      canonical: SITE_URL + '/de/about',
    },
    privacy: {
      title: 'Datenschutzerklärung — Handle',
      description: 'Wie Handle mit deinen Daten umgeht. Kurz: keine identifizierbaren Daten, keine Cookies im Kerntool, TikToks eigene Datenschutzrichtlinie regelt, was TikTok bei Anfragen sieht.',
      canonical: SITE_URL + '/de/privacy',
    },
    terms: {
      title: 'Nutzungsbedingungen — Handle',
      description: 'Nutzungsbedingungen für Handle, den kostenlosen TikTok-Namensgenerator. Mit der Erklärung zur Nicht-Zugehörigkeit zu TikTok, der Klausel zur Keine-Garantie für Verfügbarkeitsergebnisse und dem Markenrechts-Hinweis.',
      canonical: SITE_URL + '/de/terms',
    },
  },
  fr: {
    generator: {
      title: 'Générateur de Noms TikTok — Handle',
      description: "Générateur gratuit de noms d'utilisateur TikTok. Tapez un mot-clé, choisissez une niche et un style, obtenez 10–20 idées qui respectent les règles de TikTok et vérifiez la disponibilité sur TikTok. Sans inscription, sans limite.",
      canonical: SITE_URL + '/fr/generator',
    },
    faq: {
      title: 'FAQ du Générateur de Noms TikTok — Handle',
      description: "Questions fréquentes sur le générateur de noms TikTok de Handle : comment choisir un nom qui vous correspond, comment fonctionne la vérification de disponibilité, et les meilleures idées de noms TikTok pour 2026.",
      canonical: SITE_URL + '/fr/faq',
    },
    about: {
      title: 'À Propos de Handle — Générateur Gratuit de Noms TikTok',
      description: "À propos de Handle : un générateur gratuit de noms d'utilisateur TikTok avec vérification de disponibilité en direct sur TikTok. 17 styles, 17 niches, 17 langues, sans inscription.",
      canonical: SITE_URL + '/fr/about',
    },
    privacy: {
      title: 'Politique de Confidentialité — Handle',
      description: "Comment Handle traite vos données. En bref : aucune donnée identifiante collectée, aucun cookie pour l'outil principal, et la politique de confidentialité de TikTok s'applique à ce qu'ils voient.",
      canonical: SITE_URL + '/fr/privacy',
    },
    terms: {
      title: "Conditions d'Utilisation — Handle",
      description: "Conditions d'utilisation de Handle, le générateur gratuit de noms TikTok. Inclut la déclaration de non-affiliation avec TikTok, la clause de non-garantie sur les verdicts, et l'avis de non-recherche de marques.",
      canonical: SITE_URL + '/fr/terms',
    },
  },
  it: {
    generator: {
      title: 'Generatore di Nomi TikTok — Handle',
      description: "Generatore gratuito di nomi utente TikTok. Digita una parola chiave, scegli una nicchia e uno stile, ottieni 10–20 idee che rispettano le regole di TikTok e verifica la disponibilità su TikTok. Senza registrazione, senza limiti.",
      canonical: SITE_URL + '/it/generator',
    },
    faq: {
      title: 'FAQ sul Generatore di Nomi TikTok — Handle',
      description: "Domande frequenti sul generatore di nomi TikTok di Handle: come scegliere un nome che ti rappresenta, come funziona il controllo di disponibilità, e le migliori idee di nomi TikTok per il 2026.",
      canonical: SITE_URL + '/it/faq',
    },
    about: {
      title: 'Informazioni su Handle — Generatore Gratuito di Nomi TikTok',
      description: "Informazioni su Handle: un generatore gratuito di nomi utente TikTok con controllo di disponibilità in tempo reale su TikTok. 17 stili, 17 nicchie, 17 lingue, senza registrazione.",
      canonical: SITE_URL + '/it/about',
    },
    privacy: {
      title: 'Informativa sulla Privacy — Handle',
      description: "Come Handle gestisce i tuoi dati. In breve: nessun dato identificativo raccolto, nessun cookie per lo strumento principale, e l'informativa sulla privacy di TikTok si applica a ciò che loro vedono.",
      canonical: SITE_URL + '/it/privacy',
    },
    terms: {
      title: "Termini di Servizio — Handle",
      description: "Termini di servizio di Handle, il generatore gratuito di nomi TikTok. Include la dichiarazione di non affiliazione con TikTok, la clausola di non garanzia sui verdetti, e l'avviso di non ricerca di marchi.",
      canonical: SITE_URL + '/it/terms',
    },
  },
  pt: {
    generator: {
      title: 'Gerador de Nomes TikTok — Handle',
      description: 'Gerador gratuito de nomes de usuário TikTok. Digite uma palavra-chave, escolha um nicho e um estilo, obtenha 10–20 ideias que seguem as regras do TikTok e verifique a disponibilidade no TikTok. Sem cadastro, sem limites.',
      canonical: SITE_URL + '/pt/generator',
    },
    faq: {
      title: 'Perguntas Frequentes sobre o Gerador de Nomes TikTok — Handle',
      description: 'Perguntas frequentes sobre o gerador de nomes TikTok do Handle: como escolher um nome que combine com você, como funciona a verificação de disponibilidade, e as melhores ideias de nomes para TikTok em 2026.',
      canonical: SITE_URL + '/pt/faq',
    },
    about: {
      title: 'Sobre o Handle — Gerador Gratuito de Nomes TikTok',
      description: 'Sobre o Handle: um gerador gratuito de nomes de usuário TikTok com verificação de disponibilidade em tempo real no TikTok. 17 estilos, 17 nichos, 17 idiomas, sem cadastro.',
      canonical: SITE_URL + '/pt/about',
    },
    privacy: {
      title: 'Política de Privacidade — Handle',
      description: 'Como o Handle trata seus dados. Resumindo: nenhum dado identificável é coletado, nenhum cookie para a ferramenta principal, e a política de privacidade do TikTok rege o que eles veem.',
      canonical: SITE_URL + '/pt/privacy',
    },
    terms: {
      title: 'Termos de Serviço — Handle',
      description: 'Termos de serviço do Handle, o gerador gratuito de nomes TikTok. Inclui a declaração de não afiliação com o TikTok, a cláusula de não garantia sobre os veredictos, e o aviso de não pesquisa de marcas.',
      canonical: SITE_URL + '/pt/terms',
    },
  },
  nl: {
    generator: {
      title: 'TikTok Naam Generator — Handle',
      description: "Gratis TikTok gebruikersnaam generator. Typ een trefwoord, kies een niche en een vibe, krijg 10–20 TikTok gebruikersnaam ideeën die aan de regels voldoen, en check de beschikbaarheid op TikTok. Geen account, geen limiet.",
      canonical: SITE_URL + '/nl/generator',
    },
    faq: {
      title: 'Veelgestelde Vragen over de TikTok Naam Generator — Handle',
      description: "Veelgestelde vragen over de TikTok naam generator van Handle: hoe kies je een TikTok naam die bij je past, hoe werkt de beschikbaarheidscheck, en de beste TikTok naam ideeën voor 2026.",
      canonical: SITE_URL + '/nl/faq',
    },
    about: {
      title: 'Over Handle — Gratis TikTok Naam Generator',
      description: "Over Handle: een gratis TikTok naam generator met live beschikbaarheidscheck op TikTok. 17 vibes, 17 niches, 17 talen, geen account nodig.",
      canonical: SITE_URL + '/nl/about',
    },
    privacy: {
      title: 'Privacybeleid — Handle',
      description: "Hoe Handle met je gegevens omgaat. Kort: geen identificeerbare gegevens verzameld, geen cookies voor de kerntool, en TikTok's eigen privacybeleid bepaalt wat zij zien.",
      canonical: SITE_URL + '/nl/privacy',
    },
    terms: {
      title: 'Servicevoorwaarden — Handle',
      description: "Servicevoorwaarden voor Handle, de gratis TikTok naam generator. Bevat de niet-geaffilieerd-met-TikTok verklaring, de geen-garantie-clausule voor de beschikbaarheidsuitspraken, en de geen-handelsmerk-onderzoek disclaimer.",
      canonical: SITE_URL + '/nl/terms',
    },
  },
  pl: {
    generator: {
      title: 'Generator Nazw TikTok — Handle',
      description: 'Darmowy generator nazw użytkownika TikTok. Wpisz słowo kluczowe, wybierz niszę i styl, otrzymaj 10–20 pomysłów na nazwy zgodnych z zasadami TikToka i sprawdź dostępność na TikToku. Bez rejestracji, bez limitów.',
      canonical: SITE_URL + '/pl/generator',
    },
    faq: {
      title: 'FAQ Generatora Nazw TikTok — Handle',
      description: 'Najczęściej zadawane pytania o generator nazw TikTok od Handle: jak wybrać nazwę TikTok, która do Ciebie pasuje, jak działa sprawdzanie dostępności, i najlepsze pomysły na nazwy TikTok na 2026.',
      canonical: SITE_URL + '/pl/faq',
    },
    about: {
      title: 'O Handle — Darmowy Generator Nazw TikTok',
      description: 'O Handle: darmowy generator nazw użytkownika TikTok z bieżącym sprawdzaniem dostępności na TikToku. 17 stylów, 17 nisz, 17 języków, bez rejestracji.',
      canonical: SITE_URL + '/pl/about',
    },
    privacy: {
      title: 'Polityka Prywatności — Handle',
      description: 'Jak Handle obchodzi się z Twoimi danymi. Krótko: żadne dane umożliwiające identyfikację nie są zbierane, żadne pliki cookie nie są ustawiane przez główne narzędzie, a polityka prywatności TikToka reguluje to, co TikTok widzi.',
      canonical: SITE_URL + '/pl/privacy',
    },
    terms: {
      title: 'Warunki Korzystania — Handle',
      description: 'Warunki korzystania z Handle, darmowego generatora nazw TikTok. Zawierają oświadczenie o braku powiązania z TikTokiem, klauzulę o braku gwarancji na wyniki dostępności, oraz zastrzeżenie o braku wyszukiwania znaków towarowych.',
      canonical: SITE_URL + '/pl/terms',
    },
  },
  ru: {
    generator: {
      title: 'Генератор Ников TikTok — Handle',
      description: 'Бесплатный генератор никнеймов для TikTok. Введите ключевое слово, выберите нишу и стиль, получите 10–20 идей, которые соответствуют правилам TikTok, и проверьте доступность в TikTok. Без регистрации, без ограничений.',
      canonical: SITE_URL + '/ru/generator',
    },
    faq: {
      title: 'ЧаВо о Генераторе Ников TikTok — Handle',
      description: 'Часто задаваемые вопросы о генераторе никнеймов TikTok от Handle: как выбрать ник в TikTok, который вам подходит, как работает проверка доступности, и лучшие идеи ников для TikTok в 2026.',
      canonical: SITE_URL + '/ru/faq',
    },
    about: {
      title: 'О Handle — Бесплатный Генератор Ников TikTok',
      description: 'О Handle: бесплатный генератор никнеймов для TikTok с проверкой доступности в реальном времени в TikTok. 17 стилей, 17 ниш, 17 языков, без регистрации.',
      canonical: SITE_URL + '/ru/about',
    },
    privacy: {
      title: 'Политика Конфиденциальности — Handle',
      description: 'Как Handle обращается с вашими данными. Коротко: никакие идентифицирующие данные не собираются, куки не устанавливаются основным инструментом, а собственная политика конфиденциальности TikTok регулирует то, что они видят.',
      canonical: SITE_URL + '/ru/privacy',
    },
    terms: {
      title: 'Условия Использования — Handle',
      description: 'Условия использования Handle, бесплатного генератора ников для TikTok. Включают заявление об отсутствии аффилированности с TikTok, оговорку об отсутствии гарантий на результаты проверки, и отказ от ответственности за поиск товарных знаков.',
      canonical: SITE_URL + '/ru/terms',
    },
  },
  zh: {
    generator: {
      title: 'TikTok 用户名生成器 — Handle',
      description: '免费 TikTok 用户名生成器。输入关键词,选择领域和风格,获得 10–20 个符合 TikTok 规则的用户名创意,并检查 TikTok 上的可用性。无需注册,无使用限制。',
      canonical: SITE_URL + '/zh/generator',
    },
    faq: {
      title: 'TikTok 用户名生成器常见问题 — Handle',
      description: '关于 Handle TikTok 用户名生成器的常见问题:如何选择适合自己的 TikTok 用户名,可用性检查如何工作,以及 2026 年最佳的 TikTok 用户名创意。',
      canonical: SITE_URL + '/zh/faq',
    },
    about: {
      title: '关于 Handle — 免费 TikTok 用户名生成器',
      description: '关于 Handle:一个免费的 TikTok 用户名生成器,可在 TikTok 上实时检查可用性。17 种风格、17 个领域、17 种语言,无需注册。',
      canonical: SITE_URL + '/zh/about',
    },
    privacy: {
      title: '隐私政策 — Handle',
      description: 'Handle 如何处理您的数据。简而言之:不收集任何可识别的个人数据,核心工具不设置 Cookie,TikTok 自己的隐私政策约束他们能看到什么。',
      canonical: SITE_URL + '/zh/privacy',
    },
    terms: {
      title: '服务条款 — Handle',
      description: 'Handle(免费 TikTok 用户名生成器)的服务条款。包括与 TikTok 无关的声明、对可用性结果无保证的条款,以及不进行商标检索的免责声明。',
      canonical: SITE_URL + '/zh/terms',
    },
  },
  vi: {
    generator: {
      title: 'Trình Tạo Tên TikTok — Handle',
      description: 'Trình tạo tên người dùng TikTok miễn phí. Nhập từ khóa, chọn ngách và phong cách, nhận 10–20 ý tưởng tên tuân thủ quy tắc TikTok và kiểm tra tính khả dụng trên TikTok. Không cần đăng ký, không giới hạn.',
      canonical: SITE_URL + '/vi/generator',
    },
    faq: {
      title: 'Câu Hỏi Thường Gặp về Trình Tạo Tên TikTok — Handle',
      description: 'Câu hỏi thường gặp về trình tạo tên TikTok của Handle: cách chọn tên TikTok phù hợp với bạn, cách hoạt động của kiểm tra tính khả dụng, và những ý tưởng tên TikTok hay nhất cho 2026.',
      canonical: SITE_URL + '/vi/faq',
    },
    about: {
      title: 'Về Handle — Trình Tạo Tên TikTok Miễn Phí',
      description: 'Về Handle: một trình tạo tên người dùng TikTok miễn phí với kiểm tra tính khả dụng trực tiếp trên TikTok. 17 phong cách, 17 ngách, 17 ngôn ngữ, không cần đăng ký.',
      canonical: SITE_URL + '/vi/about',
    },
    privacy: {
      title: 'Chính Sách Bảo Mật — Handle',
      description: 'Cách Handle xử lý dữ liệu của bạn. Tóm tắt: không thu thập dữ liệu nhận dạng, không đặt cookie cho công cụ chính, và chính sách bảo mật của TikTok chi phối những gì họ thấy.',
      canonical: SITE_URL + '/vi/privacy',
    },
    terms: {
      title: 'Điều Khoản Dịch Vụ — Handle',
      description: 'Điều khoản dịch vụ của Handle, trình tạo tên TikTok miễn phí. Bao gồm tuyên bố không liên kết với TikTok, điều khoản không bảo đảm cho kết quả kiểm tra, và tuyên bố miễn trừ về tìm kiếm thương hiệu.',
      canonical: SITE_URL + '/vi/terms',
    },
  },
  id: {
    generator: {
      title: 'Generator Nama TikTok — Handle',
      description: 'Generator nama pengguna TikTok gratis. Ketik kata kunci, pilih niche dan vibe, dapatkan 10–20 ide nama yang sesuai aturan TikTok dan periksa ketersediaan di TikTok. Tanpa daftar, tanpa batas.',
      canonical: SITE_URL + '/id/generator',
    },
    faq: {
      title: 'FAQ Generator Nama TikTok — Handle',
      description: 'Pertanyaan umum tentang generator nama TikTok dari Handle: cara memilih nama TikTok yang cocok untuk Anda, cara kerja pengecekan ketersediaan, dan ide nama TikTok terbaik untuk 2026.',
      canonical: SITE_URL + '/id/faq',
    },
    about: {
      title: 'Tentang Handle — Generator Nama TikTok Gratis',
      description: 'Tentang Handle: generator nama pengguna TikTok gratis dengan pengecekan ketersediaan langsung di TikTok. 17 vibe, 17 niche, 17 bahasa, tanpa daftar.',
      canonical: SITE_URL + '/id/about',
    },
    privacy: {
      title: 'Kebijakan Privasi — Handle',
      description: 'Bagaimana Handle menangani data Anda. Singkatnya: tidak ada data teridentifikasi yang dikumpulkan, tidak ada cookie untuk alat utama, dan kebijakan privasi TikTok mengatur apa yang mereka lihat.',
      canonical: SITE_URL + '/id/privacy',
    },
    terms: {
      title: 'Ketentuan Layanan — Handle',
      description: 'Ketentuan layanan untuk Handle, generator nama TikTok gratis. Termasuk pernyataan tidak berafiliasi dengan TikTok, klausul tanpa jaminan untuk hasil ketersediaan, dan penafian tanpa pencarian merek dagang.',
      canonical: SITE_URL + '/id/terms',
    },
  },
  ms: {
    generator: {
      title: 'Penjana Nama TikTok — Handle',
      description: 'Penjana nama pengguna TikTok percuma. Taip kata kunci, pilih niche dan gaya, dapat 10–20 idea nama yang mematuhi peraturan TikTok dan periksa ketersediaan di TikTok. Tanpa daftar, tanpa had.',
      canonical: SITE_URL + '/ms/generator',
    },
    faq: {
      title: 'Soalan Lazim Penjana Nama TikTok — Handle',
      description: 'Soalan lazim tentang penjana nama TikTok dari Handle: cara memilih nama TikTok yang sesuai dengan anda, cara pemeriksaan ketersediaan berfungsi, dan idea nama TikTok terbaik untuk 2026.',
      canonical: SITE_URL + '/ms/faq',
    },
    about: {
      title: 'Tentang Handle — Penjana Nama TikTok Percuma',
      description: 'Tentang Handle: penjana nama pengguna TikTok percuma dengan pemeriksaan ketersediaan langsung di TikTok. 17 gaya, 17 niche, 17 bahasa, tanpa daftar.',
      canonical: SITE_URL + '/ms/about',
    },
    privacy: {
      title: 'Dasar Privasi — Handle',
      description: 'Bagaimana Handle mengendalikan data anda. Ringkasnya: tiada data boleh dikenal pasti dikumpulkan, tiada cookie untuk alat utama, dan dasar privasi TikTok mengawal apa yang mereka lihat.',
      canonical: SITE_URL + '/ms/privacy',
    },
    terms: {
      title: 'Terma Perkhidmatan — Handle',
      description: 'Terma perkhidmatan untuk Handle, penjana nama TikTok percuma. Termasuk pernyataan tidak bergabung dengan TikTok, klausa tanpa jaminan untuk keputusan ketersediaan, dan penafian tanpa carian tanda dagang.',
      canonical: SITE_URL + '/ms/terms',
    },
  },
  tl: {
    generator: {
      title: 'Tagagawa ng Pangalan sa TikTok — Handle',
      description: 'Libreng tagagawa ng username sa TikTok. Mag-type ng keyword, pumili ng niche at vibe, makakakuha ng 10–20 ideya ng username na sumusunod sa mga patakaran ng TikTok at suriin ang availability sa TikTok. Walang signup, walang limitasyon.',
      canonical: SITE_URL + '/tl/generator',
    },
    faq: {
      title: 'Mga Madalas Itanong tungkol sa Tagagawa ng Pangalan sa TikTok — Handle',
      description: 'Mga madalas itanong tungkol sa tagagawa ng pangalan sa TikTok ng Handle: kung paano pumili ng TikTok username na bagay sa iyo, kung paano gumagana ang availability check, at ang mga pinakamagandang ideya ng username sa TikTok para sa 2026.',
      canonical: SITE_URL + '/tl/faq',
    },
    about: {
      title: 'Tungkol sa Handle — Libreng Tagagawa ng Pangalan sa TikTok',
      description: 'Tungkol sa Handle: isang libreng tagagawa ng username sa TikTok na may live availability check sa TikTok. 17 vibes, 17 niches, 17 wika, walang signup.',
      canonical: SITE_URL + '/tl/about',
    },
    privacy: {
      title: 'Patakaran sa Privacy — Handle',
      description: 'Paano hawak ng Handle ang iyong data. Sa maikling salita: walang nakikilalang data ang kinokolekta, walang cookie para sa pangunahing tool, at ang patakaran sa privacy ng TikTok ang umiiral sa kanilang nakikita.',
      canonical: SITE_URL + '/tl/privacy',
    },
    terms: {
      title: 'Mga Tuntunin ng Serbisyo — Handle',
      description: 'Mga tuntunin ng serbisyo para sa Handle, ang libreng tagagawa ng pangalan sa TikTok. Kabilang ang pahayag na hindi kaakibat ang TikTok, ang klausulang walang garantiya sa mga hatol, at ang disclaimer na walang paghahanap ng trademark.',
      canonical: SITE_URL + '/tl/terms',
    },
  },
  hi: {
    generator: {
      title: 'TikTok यूजरनेम जनरेटर — Handle',
      description: 'मुफ्त TikTok यूजरनेम जनरेटर। एक कीवर्ड टाइप करें, एक निश और एक वाइब चुनें, 10–20 अनूठे TikTok यूजरनेम विचार प्राप्त करें जो TikTok के नियमों का पालन करते हैं, और TikTok पर उपलब्धता जांचें। कोई साइनअप नहीं, कोई सीमा नहीं।',
      canonical: SITE_URL + '/hi/generator',
    },
    faq: {
      title: 'TikTok यूजरनेम जनरेटर अक्सर पूछे जाने वाले प्रश्न — Handle',
      description: 'Handle के TikTok यूजरनेम जनरेटर के बारे में अक्सर पूछे जाने वाले प्रश्न: आपके लिए उपयुक्त TikTok यूजरनेम कैसे चुनें, उपलब्धता जांच कैसे काम करती है, और 2026 के लिए सबसे अच्छे TikTok यूजरनेम विचार।',
      canonical: SITE_URL + '/hi/faq',
    },
    about: {
      title: 'Handle के बारे में — मुफ्त TikTok यूजरनेम जनरेटर',
      description: 'Handle के बारे में: TikTok पर लाइव उपलब्धता जांच के साथ एक मुफ्त TikTok यूजरनेम जनरेटर। 17 वाइब, 17 निश, 17 भाषाएं, कोई साइनअप नहीं।',
      canonical: SITE_URL + '/hi/about',
    },
    privacy: {
      title: 'गोपनीयता नीति — Handle',
      description: 'Handle आपके डेटा को कैसे संभालता है। संक्षेप में: कोई पहचान योग्य डेटा एकत्र नहीं किया जाता, मुख्य टूल के लिए कोई कुकी नहीं, और TikTok की अपनी गोपनीयता नीति नियंत्रित करती है कि वे क्या देखते हैं।',
      canonical: SITE_URL + '/hi/privacy',
    },
    terms: {
      title: 'सेवा की शर्तें — Handle',
      description: 'Handle की सेवा की शर्तें, मुफ्त TikTok यूजरनेम जनरेटर। इसमें TikTok के साथ गैर-संबद्धता का बयान, उपलब्धता फैसलों पर कोई गारंटी नहीं की शर्त, और ट्रेडमार्क खोज नहीं करने का अस्वीकरण शामिल है।',
      canonical: SITE_URL + '/hi/terms',
    },
  },
  bn: {
    generator: {
      title: 'TikTok ইউজারনেম জেনারেটর — Handle',
      description: 'বিনামূল্যে TikTok ইউজারনেম জেনারেটর। একটি কীওয়ার্ড টাইপ করুন, একটি নিশ এবং একটি ভাইব নির্বাচন করুন, 10–20টি অনন্য TikTok ইউজারনেম আইডিয়া পান যা TikTok-এর নিয়ম মেনে চলে এবং TikTok-তে প্রাপ্যতা পরীক্ষা করুন। কোনো সাইনআপ নেই, কোনো সীমা নেই।',
      canonical: SITE_URL + '/bn/generator',
    },
    faq: {
      title: 'TikTok ইউজারনেম জেনারেটর প্রায়শই জিজ্ঞাসিত প্রশ্ন — Handle',
      description: 'Handle-এর TikTok ইউজারনেম জেনারেটর সম্পর্কে প্রায়শই জিজ্ঞাসিত প্রশ্ন: আপনার জন্য উপযুক্ত TikTok ইউজারনেম কীভাবে বেছে নেবেন, প্রাপ্যতা পরীক্ষা কীভাবে কাজ করে, এবং 2026-এর জন্য সেরা TikTok ইউজারনেম আইডিয়া।',
      canonical: SITE_URL + '/bn/faq',
    },
    about: {
      title: 'Handle সম্পর্কে — বিনামূল্যে TikTok ইউজারনেম জেনারেটর',
      description: 'Handle সম্পর্কে: TikTok-তে লাইভ প্রাপ্যতা পরীক্ষা সহ একটি বিনামূল্যে TikTok ইউজারনেম জেনারেটর। 17টি ভাইব, 17টি নিশ, 17টি ভাষা, কোনো সাইনআপ নেই।',
      canonical: SITE_URL + '/bn/about',
    },
    privacy: {
      title: 'গোপনীয়তা নীতি — Handle',
      description: 'Handle আপনার ডেটা কীভাবে পরিচালনা করে। সংক্ষেপে: কোনো সনাক্তযোগ্য ডেটা সংগ্রহ করা হয় না, মূল টুলের জন্য কোনো কুকি নেই, এবং TikTok-এর নিজস্ব গোপনীয়তা নীতি নিয়ন্ত্রণ করে তারা কী দেখে।',
      canonical: SITE_URL + '/bn/privacy',
    },
    terms: {
      title: 'সেবার শর্তাবলী — Handle',
      description: 'Handle-এর সেবার শর্তাবলী, বিনামূল্যে TikTok ইউজারনেম জেনারেটর। এতে TikTok-এর সাথে অ-অনুমোদনের বিবৃতি, প্রাপ্যতা ফলাফলের উপর কোনো গ্যারান্টি নেই এমন শর্ত, এবং ট্রেডমার্ক অনুসন্ধান না করার দাবিত্যাগ অন্তর্ভুক্ত।',
      canonical: SITE_URL + '/bn/terms',
    },
  },
  ur: {
    generator: {
      title: 'TikTok یوزر نیم جنریٹر — Handle',
      description: 'مفت TikTok یوزر نیم جنریٹر۔ ایک کلیدی لفظ ٹائپ کریں، ایک نچ اور ایک وائب منتخب کریں، 10-20 انوکھے TikTok یوزر نیم آئیڈیاز حاصل کریں جو TikTok کے قوانین کی پیروی کرتے ہیں، اور TikTok پر دستیابی چیک کریں۔ کوئی سائن اپ نہیں، کوئی حد نہیں۔',
      canonical: SITE_URL + '/ur/generator',
    },
    faq: {
      title: 'TikTok یوزر نیم جنریٹر عمومی سوالات — Handle',
      description: 'Handle کے TikTok یوزر نیم جنریٹر کے بارے میں اکثر پوچھے جانے والے سوالات: آپ کے لیے موزوں TikTok یوزر نیم کا انتخاب کیسے کریں، دستیابی کی جانچ کیسے کام کرتی ہے، اور 2026 کے لیے بہترین TikTok یوزر نیم آئیڈیاز۔',
      canonical: SITE_URL + '/ur/faq',
    },
    about: {
      title: 'Handle کے بارے میں — مفت TikTok یوزر نیم جنریٹر',
      description: 'Handle کے بارے میں: TikTok پر لائیو دستیابی کی جانچ کے ساتھ ایک مفت TikTok یوزر نیم جنریٹر۔ 17 وائب، 17 نچ، 17 زبانیں، کوئی سائن اپ نہیں۔',
      canonical: SITE_URL + '/ur/about',
    },
    privacy: {
      title: 'رازداری کی پالیسی — Handle',
      description: 'Handle آپ کے ڈیٹا کو کیسے ہینڈل کرتا ہے۔ مختصراً: کوئی شناختی ڈیٹا اکٹھا نہیں کیا جاتا، بنیادی ٹول کے لیے کوئی کوکی نہیں، اور TikTok کی اپنی رازداری کی پالیسی اس بات کو کنٹرول کرتی ہے کہ وہ کیا دیکھتے ہیں۔',
      canonical: SITE_URL + '/ur/privacy',
    },
    terms: {
      title: 'سروس کی شرائط — Handle',
      description: 'Handle کی سروس کی شرائط، مفت TikTok یوزر نیم جنریٹر۔ اس میں TikTok کے ساتھ غیر وابستگی کا بیان، دستیابی کے فیصلوں پر کوئی گارنٹی نہ ہونے کی شرط، اور ٹریڈ مارک تلاش نہ کرنے کی دستاویز شامل ہیں۔',
      canonical: SITE_URL + '/ur/terms',
    },
  },
  ar: {
    generator: {
      title: 'مولد أسماء تيك توك — Handle',
      description: 'مولد أسماء مستخدمين تيك توك مجاني. اكتب كلمة مفتاحية، اختر مجالاً وأسلوباً، احصل على 10-20 فكرة اسم مستخدم فريدة تتبع قواعد تيك توك وتحقق من التوفر على تيك توك. بدون تسجيل، بدون حدود.',
      canonical: SITE_URL + '/ar/generator',
    },
    faq: {
      title: 'الأسئلة الشائعة حول مولد أسماء تيك توك — Handle',
      description: 'الأسئلة الشائعة حول مولد أسماء تيك توك من Handle: كيفية اختيار اسم تيك توك يناسبك، وكيف تعمل ميزة التحقق من التوفر، وأفضل أفكار أسماء تيك توك لعام 2026.',
      canonical: SITE_URL + '/ar/faq',
    },
    about: {
      title: 'حول Handle — مولد أسماء تيك توك مجاني',
      description: 'حول Handle: مولد أسماء مستخدمين تيك توك مجاني مع تحقق مباشر من التوفر على تيك توك. 17 أسلوباً، 17 مجالاً، 17 لغة، بدون تسجيل.',
      canonical: SITE_URL + '/ar/about',
    },
    privacy: {
      title: 'سياسة الخصوصية — Handle',
      description: 'كيف يتعامل Handle مع بياناتك. باختصار: لا يتم جمع أي بيانات يمكن تحديد هويتك، ولا يتم تعيين ملفات تعريف ارتباط للأداة الرئيسية، وسياسة الخصوصية الخاصة بـ TikTok تحكم ما يرونه.',
      canonical: SITE_URL + '/ar/privacy',
    },
    terms: {
      title: 'شروط الخدمة — Handle',
      description: 'شروط خدمة Handle، مولد أسماء تيك توك المجاني. يتضمن بيان عدم الانتساب إلى TikTok، وبند عدم الضمان على نتائج التحقق من التوفر، وإخلاء المسؤولية بعدم البحث عن العلامات التجارية.',
      canonical: SITE_URL + '/ar/terms',
    },
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

const SUPPORTED_LOCALES = Object.keys(LOCALE_META);

// Strip the <meta http-equiv="Content-Security-Policy"> from the served
// HTML. The Express server sets a strict CSP via the HTTP header (with
// a per-request nonce), which is more reliable than a meta tag (the
// meta tag is enforced too, but with the static-host SHA-256 hash,
// which doesn't match the new AdSense config inline script that gets
// a nonce). Keeping both active would result in the meta CSP
// rejecting any nonce-tagged script that doesn't match its hash. The
// HTTP header alone is enough on this Express server.
function stripMetaCsp(html) {
  return html.replace(
    /<meta\s+http-equiv=["']Content-Security-Policy["'][^>]*>\n?/i,
    ''
  );
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
  // The static deploy's meta-CSP uses a SHA-256 hash for the route-detection
  // script; the local build uses a nonce. Both work, both block the
  // platform's injected script. The nonce is added here so the route
  // detection runs on per-route requests.
  if (nonce) {
    out = out.replace(
      /<script>(\s*\(function \(\) \{\s*var path = window\.location)/,
      '<script nonce="' + escapeAttr(nonce) + '">$1'
    );
  }
  return out;
}

// Add the per-request CSP nonce to every <script> tag in the HTML that
// doesn't already carry one. We have a few small inline scripts in the
// head (route detection handled above in injectMeta, AdSense config
// placeholder) that all need the nonce so the strict CSP header
// allows them. We use a function callback so we can preserve any
// existing attributes (e.g. JSON-LD scripts that have
// type="application/ld+json"). External scripts (with src=) and scripts
// that already have a nonce are left alone.
function addCspNoncesToInlineScripts(html, nonce) {
  if (!nonce) return html;
  const nonceAttr = ' nonce="' + escapeAttr(nonce) + '"';
  return html.replace(
    /<script([^>]*)>/g,
    (match, attrs) => /\snonce=/.test(attrs) ? match : '<script' + nonceAttr + attrs + '>'
  );
}

function escapeHtml(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function escapeAttr(s) { return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;'); }

// Strip the inert <template data-page-canonical="..."> and
// <template data-page-hreflang="..."> blocks from the served HTML.
// These were placeholders for a client-side router swap that we no
// longer do — the server now injects the right canonical and
// hreflang per request. The templates are inert (browsers don't
// parse link tags inside <template> elements) and were causing
// confusion: rewriteHreflang was rewritting every template in
// place, leaving 6 identical-content templates in the served
// HTML. Removing them entirely is the cleanest fix.
//
// Matches:
//   <template data-page-canonical="X">...</template>
//   <template data-page-hreflang="X">...</template>
function stripPerRouteTemplates(html) {
  return html.replace(
    /<template\s+data-page-(?:canonical|hreflang)="[^"]+">[\s\S]*?<\/template>\s*/g,
    ''
  );
}

// Rewrite every LIVE <link rel="alternate" hreflang="X" href="..."> tag
// in the HTML to point to the same route in each language. This makes
// the served hreflang match the served canonical, which is what Google
// expects for proper multilingual SEO. Preserves the dir="rtl"
// attribute for ar/ur.
//
// `route` is one of: 'home', 'generator', 'faq', 'about', 'privacy', 'terms'.
function rewriteHreflang(html, route) {
  return html.replace(
    /<link rel="alternate" hreflang="([^"]+)"\s+href="[^"]+"([^>]*?)\s*>/g,
    function (match, hreflangLang, trailingAttrs) {
      const isXDefault = hreflangLang === 'x-default';
      const isEn = hreflangLang === 'en' || isXDefault;
      const langPrefix = isEn ? '' : '/' + hreflangLang;
      const routePath = route === 'home' ? '' : '/' + route;
      const newHref = SITE_URL + langPrefix + routePath;
      return '<link rel="alternate" hreflang="' + hreflangLang + '" href="' + newHref + '"' + trailingAttrs + '>';
    }
  );
}

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
  res.send(stripPerRouteTemplates(rewriteHreflang(
    stripMetaCsp(
      addCspNoncesToInlineScripts(
        injectMeta(loadIndexHtml(), meta, res.locals.cspNonce),
        res.locals.cspNonce
      )
    ),
    route
  )));
});

// --- Localized SPA routes (/xx/generator, /xx/faq, etc.) -------------------
//
// Serve the localized index.html for any /xx/route path. If we have
// per-locale per-route meta, inject it on top of the file's home meta.
// This mirrors the English SPA route handler above. The localized
// files live at public/{lang}/index.html.
const LOCALE_SPA_ROUTE = /^\/([a-z]{2})\/(generator|faq|about|privacy|terms)\/?$/;
app.get(LOCALE_SPA_ROUTE, (req, res) => {
  const m = req.path.match(LOCALE_SPA_ROUTE);
  const lang = m[1];
  const route = m[2];
  const localeDir = path.join(__dirname, 'public', lang);
  const localeFile = path.join(localeDir, 'index.html');
  // Fall back to English if the localized file doesn't exist
  if (!fs.existsSync(localeFile)) {
    return res.sendFile(INDEX_HTML_PATH);
  }
  const localeRouteMeta = LOCALE_META[lang] && LOCALE_META[lang][route];
  let html = fs.readFileSync(localeFile, 'utf8');
  if (localeRouteMeta) {
    html = injectMeta(html, localeRouteMeta, res.locals.cspNonce);
  }
  // Add CSP nonces to any inline scripts (route detection + AdSense config)
  html = addCspNoncesToInlineScripts(html, res.locals.cspNonce);
  // Strip the meta CSP (HTTP header is the source of truth on this server)
  html = stripMetaCsp(html);
  res.set('Content-Type', 'text/html; charset=utf-8');
  res.send(stripPerRouteTemplates(rewriteHreflang(html, route)));
});

// --- Localized home pages (/xx/, /xx) ---------------------------------------
const LOCALE_HOME_ROUTE = /^\/([a-z]{2})\/?$/;
app.get(LOCALE_HOME_ROUTE, (req, res) => {
  const lang = req.path.match(LOCALE_HOME_ROUTE)[1];
  if (lang === 'en') {
    return res.redirect(302, '/');
  }
  const localeFile = path.join(__dirname, 'public', lang, 'index.html');
  if (!fs.existsSync(localeFile)) {
    return res.sendFile(INDEX_HTML_PATH);
  }
  let html = fs.readFileSync(localeFile, 'utf8');
  // Add CSP nonces to any inline scripts (route detection + AdSense config)
  html = addCspNoncesToInlineScripts(html, res.locals.cspNonce);
  // Strip the meta CSP (HTTP header is the source of truth on this server)
  html = stripMetaCsp(html);
  res.set('Content-Type', 'text/html; charset=utf-8');
  res.send(stripPerRouteTemplates(rewriteHreflang(html, 'home')));
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
