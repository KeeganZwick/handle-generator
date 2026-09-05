// /public/js/router.js
//
// Client-side router for the static deploy.
//
// The static host serves the same index.html for any path (SPA fallback),
// so the URL is the source of truth for which "page" to show. The router
// intercepts in-app nav clicks, updates history, swaps the visible section,
// and keeps the document title in sync. Browser back/forward is handled
// via popstate.
//
// Locale support: URLs can be /xx/route (e.g. /es/generator, /de/faq).
// The router strips the /xx/ prefix for route matching and re-adds it
// for navigation, so a click on "Generator" while on /es/ navigates to
// /es/generator instead of /generator. The TITLES map is looked up by
// the current URL's locale: the per-page window.__handleTitles takes
// precedence (each localized file sets its own), but if the static
// host serves the wrong index.html (it does — SPA fallback means
// /es/generator gets the English index.html), we fall back to
// window.__handleTitlesByLocale from /js/titles.js, which has all 17
// locales' titles. Final fallback is the English DEFAULT_TITLES.

(function () {
  'use strict';

  var DEFAULT_TITLES = {
    home: 'TikTok Username Generator — Free Username Ideas & Availability Check | Handle',
    generator: 'TikTok Username Generator — Free Username Ideas & Availability Check | Handle',
    faq: 'FAQ — TikTok Username Generator | Handle',
    about: 'About — Handle',
    privacy: 'Privacy Policy — Handle',
    terms: 'Terms of Service — Handle',
    '404': 'Page not found — Handle',
  };

  var KNOWN_LOCALES = new Set([
    'es','de','fr','it','pt','nl','pl','ru','zh','vi','id','ms','tl','hi','bn','ur','ar'
  ]);

  function getTitles(locale) {
    // 1. Per-page titles (set by each localized index.html).
    if (typeof window !== 'undefined' && window.__handleTitles) {
      return window.__handleTitles;
    }
    // 2. Per-locale titles (loaded by /js/titles.js — works even when
    //    the CDN serves the wrong index.html due to SPA fallback).
    if (typeof window !== 'undefined'
        && window.__handleTitlesByLocale
        && locale
        && window.__handleTitlesByLocale[locale]) {
      return window.__handleTitlesByLocale[locale];
    }
    // 3. English defaults.
    return DEFAULT_TITLES;
  }

  function splitLocale(path) {
    var m = path.match(/^\/([a-z]{2})(\/.*)?$/);
    if (m && KNOWN_LOCALES.has(m[1])) {
      return { locale: m[1], rest: m[2] || '/' };
    }
    return { locale: '', rest: path };
  }

  function pathToRoute(path) {
    var sp = splitLocale(path);
    var p = sp.rest;
    if (p === '/generator' || p === '/generator/') return 'generator';
    if (p === '/faq' || p === '/faq/') return 'faq';
    if (p === '/about' || p === '/about/') return 'about';
    if (p === '/privacy' || p === '/privacy/') return 'privacy';
    if (p === '/terms' || p === '/terms/') return 'terms';
    if (p === '/' || p === '') return 'home';
    return null;
  }

  function currentLocale() {
    return splitLocale(window.location.pathname).locale;
  }

  function routeToPath(route, locale) {
    var prefix = locale && locale !== 'en' ? '/' + locale : '';
    if (route === 'home') return prefix + '/';
    return prefix + '/' + route;
  }

  function applyRoute(route, opts) {
    var locale = currentLocale();
    document.body.setAttribute('data-route', route);
    var titles = getTitles(locale);
    document.title = titles[route] || titles.home;
    swapPageMeta(route);
    // Hreflang is no longer swapped at runtime — v18.3 strips the
    // <template data-page-hreflang> blocks in server.js, so the served
    // HTML already has the right 19 live hreflang tags. There's nothing
    // to swap on SPA navigation either (the template is gone).
    // Canonical is no longer swapped at runtime — v18.2 emits per-page
    // static canonicals in the build output (one HTML file per route),
    // so the served file already has the correct absolute URL.
    document.querySelectorAll('.nav a[data-nav]').forEach(function (a) {
      a.classList.toggle('is-active', a.getAttribute('data-nav') === route);
    });
    // Update hrefs on internal links to include the locale prefix
    document.querySelectorAll('a[data-nav]').forEach(function (a) {
      var route = a.getAttribute('data-nav');
      if (route) a.setAttribute('href', routeToPath(route, locale));
    });
    if (opts && opts.scrollTop) {
      window.scrollTo(0, 0);
    }
    document.dispatchEvent(new CustomEvent('routechange', { detail: { route: route, locale: locale } }));
  }

  // Per-page SEO swap. The build script emits a <template data-page-meta="X">
  // for each of the 6 routes. On route change, we copy the active template's
  // <title>, <meta name="description">, and <meta property="og:*"> into the
  // document head, replacing the previous page's tags.
  function swapPageMeta(route) {
    var tmpl = document.querySelector('template[data-page-meta="' + route + '"]');
    if (!tmpl) return;
    // Remove the previous page's meta tags (they're marked with a data-active attribute)
    document.querySelectorAll('head [data-page-meta-active]').forEach(function (el) {
      el.parentNode.removeChild(el);
    });
    // Clone the template's children into the head
    var content = tmpl.content;
    var frag = document.importNode(content, true);
    Array.prototype.forEach.call(frag.children, function (el) {
      el.setAttribute('data-page-meta-active', route);
      document.head.appendChild(el);
    });
  }

  // Per-page hreflang swap. REMOVED in v18.3: server.js strips the
  // <template data-page-hreflang> blocks from the served HTML, so the
  // document already has the right 19 live hreflang tags. There's no
  // template to query and nothing to swap on route change.
  // (swapPageHreflang function intentionally removed — see v18.3)

  // Per-page canonical swap. REMOVED in v18.2: the build now emits
  // per-page static canonicals in the output (one HTML file per route),
  // each with the correct absolute URL hardcoded. The served file
  // already has the right canonical, so no client-side swap is needed.
  // Direct URL access (/es/generator) returns the right file; SPA
  // navigation keeps the canonical of the originally-loaded file (which
  // is a known trade-off in exchange for SEO robustness with zero JS
  // dependence on the canonical).

  // (swapPageCanonical function intentionally removed — see v18.2)

  function onLinkClick(e) {
    var a = e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href) return;
    // Only intercept our own in-app links. Anything else (mailto, http(s)://,
    // #anchor, language switcher links, unknown future routes) is left alone.
    if (!/^\/(en|es|de|fr|it|pt|nl|pl|ru|zh|vi|id|ms|tl|hi|bn|ur|ar)?\/?(generator|faq|about|privacy|terms)?\/?$/.test(href)) return;
    // Same-tab only; let modifier-clicks open in a new tab.
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target && a.target !== '_self') return;

    e.preventDefault();
    var route = pathToRoute(href);
    if (route === null) return; // shouldn't happen given the regex above
    var hrefSp = splitLocale(href);
    // Determine target locale: prefer data-lang attribute (lang switcher
    // links always set it), then href locale, then '/ → en' (the root
    // path is the English home, not the current locale), then current
    // locale, then default to 'en'. This fixes the bug where clicking
    // English from a non-English page did an SPA navigation instead of
    // reloading to /.
    var dataLang = a.getAttribute('data-lang');
    var targetLocale = dataLang || hrefSp.locale || (href === '/' || href === '' ? 'en' : '') || currentLocale() || 'en';
    var currentPath = pathToRoute(window.location.pathname);
    var currentLoc = currentLocale();

    // Locale change: do a full page reload so the static host serves the
    // correct localized index.html. SPA pushState would change the URL
    // but the body content would stay in the old locale because we're
    // already on a single rendered page.
    if (targetLocale !== currentLoc) {
      window.location.href = href;
      return;
    }
    // Same locale, just a route change (or same route): do SPA navigation.
    if (route === currentPath) {
      applyRoute(route, { scrollTop: true });
      return;
    }
    history.pushState({ route: route, locale: targetLocale }, '', routeToPath(route, targetLocale));
    applyRoute(route, { scrollTop: true });
  }

  document.addEventListener('click', onLinkClick);
  window.addEventListener('popstate', function () {
    var sp = splitLocale(window.location.pathname);
    var route = pathToRoute(window.location.pathname) || '404';
    applyRoute(route, { scrollTop: false });
  });

  // --- Language switcher -------------------------------------------------
  //
  // The switcher uses <details>/<summary> for keyboard and screen reader
  // accessibility, but we also wire an explicit click handler so the
  // toggle is reliable across browsers, close on outside click, and
  // close on Escape. We also update the "current language" label to
  // reflect the page's actual locale (e.g. "DE" while on /de/).

  function initLangSwitch() {
    var d = document.querySelector('details.lang-switch[data-lang-switch]');
    if (!d) return;
    var summary = d.querySelector('summary');
    if (!summary) return;
    var current = d.querySelector('[data-lang-current]');
    var links = d.querySelectorAll('.lang-switch__menu a[data-lang]');

    // Explicit toggle on summary click. We call preventDefault to stop
    // the browser's default <details> toggle and do it ourselves, which
    // lets us coordinate with click-outside and Escape.
    summary.addEventListener('click', function (e) {
      e.preventDefault();
      var isOpen = d.hasAttribute('open');
      if (isOpen) {
        d.removeAttribute('open');
      } else {
        d.setAttribute('open', '');
      }
    });

    // Close on click outside the switcher.
    document.addEventListener('click', function (e) {
      if (!d.hasAttribute('open')) return;
      if (d.contains(e.target)) return;
      d.removeAttribute('open');
    });

    // Close on Escape.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && d.hasAttribute('open')) {
        d.removeAttribute('open');
        summary.focus();
      }
    });

    // Update the "current" label to the active locale (uppercase code).
    var locale = currentLocale();
    if (current && locale) {
      current.textContent = locale.toUpperCase();
    }

    // Mark the active link in the menu as aria-current.
    links.forEach(function (a) {
      if (a.getAttribute('data-lang') === (locale || 'en')) {
        a.setAttribute('aria-current', 'true');
      }
    });
  }

  // --- Footer + locale-aware text localizer ---------------------------------
  //
  // The English index.html ships with English text in the footer, the
  // consent banner, the fonts section, and a few other static places.
  // When the page is served from /de/ or /es/ the server returns the
  // localized index.html (which already has the right text inline) — but
  // when the static CDN serves the English index.html for /xx/route paths
  // (its SPA fallback), we re-apply the locale's text from
  // window.__handleStringsByLocale.

  function S(key) {
    var locale = currentLocale() || 'en';
    var map = window.__handleStringsByLocale || {};
    var dict = map[locale] || map.en || {};
    return dict[key] || (map.en && map.en[key]) || key;
  }

  function applyLocaleText() {
    // Find every [data-i18n] element and update its text content to the
    // matching per-locale string. Skips elements inside the lang switcher
    // (those have hard-coded native names that don't need re-translation).
    // Keys listed in HTML_KEYS may contain HTML tags (e.g. <strong>); for
    // those we set innerHTML so the tags render. All other keys go through
    // textContent to keep them as plain text.
    var HTML_KEYS = { help_vibe: 1, help_your_text: 1 };
    var nodes = document.querySelectorAll('[data-i18n]');
    nodes.forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      var val = S(key);
      if (!val) return;
      if (HTML_KEYS[key]) {
        if (val !== el.innerHTML) el.innerHTML = val;
      } else {
        if (val !== el.textContent) el.textContent = val;
      }
    });
    // Also handle [data-i18n-placeholder] for input/textarea placeholders.
    var phNodes = document.querySelectorAll('[data-i18n-placeholder]');
    phNodes.forEach(function (el) {
      var key = el.getAttribute('data-i18n-placeholder');
      var val = S(key);
      if (val && val !== el.placeholder) {
        el.placeholder = val;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initLangSwitch();
    applyLocaleText();
    var route = pathToRoute(window.location.pathname) || '404';
    applyRoute(route, { scrollTop: false });
  });
})();
