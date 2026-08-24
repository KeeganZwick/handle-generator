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
// Sections are hidden by CSS (see the [data-page-section] rule in
// index.html). The router sets body[data-route] to control which one
// is visible.

(function () {
  'use strict';

  const TITLES = {
    home: 'Handle — Free TikTok Username Generator with Availability Check',
    generator: 'TikTok Username Generator — Handle',
    faq: 'FAQ — Handle',
    about: 'About — Handle',
    privacy: 'Privacy Policy — Handle',
    terms: 'Terms of Service — Handle',
    '404': 'Page not found — Handle',
  };

  const KNOWN_ROUTES = new Set(['home', 'generator', 'faq', 'about', 'privacy', 'terms']);

  function pathToRoute(path) {
    if (path === '/generator' || path === '/generator/') return 'generator';
    if (path === '/faq' || path === '/faq/') return 'faq';
    if (path === '/about' || path === '/about/') return 'about';
    if (path === '/privacy' || path === '/privacy/') return 'privacy';
    if (path === '/terms' || path === '/terms/') return 'terms';
    if (path === '/' || path === '') return 'home';
    return null; // unknown → 404
  }

  function routeToPath(route) {
    if (route === 'home') return '/';
    return '/' + route;
  }

  function applyRoute(route, opts) {
    document.body.setAttribute('data-route', route);
    document.title = TITLES[route] || TITLES.home;
    document.querySelectorAll('.nav a[data-nav]').forEach((a) => {
      a.classList.toggle('is-active', a.getAttribute('data-nav') === route);
    });
    if (opts && opts.scrollTop) {
      window.scrollTo(0, 0);
    }
    document.dispatchEvent(new CustomEvent('routechange', { detail: { route } }));
  }

  function onLinkClick(e) {
    const a = e.target.closest('a');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href) return;
    // Only intercept our own in-app links. Anything else (mailto, http(s)://,
    // #anchor, unknown future routes) is left alone — the browser will do the
    // right thing, and unknown paths will land on the 404 section via the
    // initial render below.
    if (!/^\/(generator|faq|about|privacy|terms)?\/?$/.test(href)) return;
    // Same-tab only; let modifier-clicks open in a new tab.
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (a.target && a.target !== '_self') return;

    e.preventDefault();
    const route = pathToRoute(href);
    if (route === null) return; // shouldn't happen given the regex above
    if (route === pathToRoute(window.location.pathname)) {
      applyRoute(route, { scrollTop: true });
      return;
    }
    history.pushState({ route }, '', routeToPath(route));
    applyRoute(route, { scrollTop: true });
  }

  document.addEventListener('click', onLinkClick);
  window.addEventListener('popstate', () => {
    const route = pathToRoute(window.location.pathname) || '404';
    applyRoute(route, { scrollTop: false });
  });

  // Set the initial route on first paint, in case the inline script in
  // <head> didn't get a chance to run (it does, but this is a no-op
  // safety net for the case where JS is delayed).
  document.addEventListener('DOMContentLoaded', () => {
    const route = pathToRoute(window.location.pathname) || '404';
    applyRoute(route, { scrollTop: false });
  });
})();
