// /public/js/consent.js
//
// Two small jobs, both first-paint-friendly:
//   1. Strip the platform-injected "Created by MiniMax Agent" floating ball
//      from the DOM. CSS already hides it; this is the belt-and-suspenders
//      removal so screen readers and tab order skip it, and so it can't
//      reappear if the host's CSS changes.
//   2. Show a slim cookie consent banner on first visit, remember the
//      dismissal in localStorage, and never show it again on repeat visits.
//
// The banner is a fixed-position slim bar at the bottom of the viewport.
// It does NOT overlay the main content with a full-screen modal — it sits
// in its own row at the bottom edge, like the cookie bars on every other
// ad-supported site in 2026.

(function () {
  'use strict';

  var STORAGE_KEY = 'handle.cookieConsent.v1';

  // --- 1. Remove the platform-injected floating ball -------------------------

  function stripAttribution() {
    // The host injects this with a literal id; cover the common variants.
    var selectors = [
      '#minimax-floating-ball',
      '[id*="minimax-"]',
      '[class*="minimax-ball"]',
    ];
    selectors.forEach(function (sel) {
      try {
        document.querySelectorAll(sel).forEach(function (el) {
          if (el && el.parentNode) el.parentNode.removeChild(el);
        });
      } catch (e) {
        // selector might be invalid in very old browsers; safe to ignore
      }
    });
  }

  // Run once now (in case the platform's script ran before us) and then
  // again after DOMContentLoaded for the case where the platform's script
  // runs after page load.
  stripAttribution();
  document.addEventListener('DOMContentLoaded', stripAttribution);
  // Also catch a late injection by watching for new nodes briefly.
  if (typeof MutationObserver !== 'undefined') {
    var mo = new MutationObserver(function (mutations) {
      for (var i = 0; i < mutations.length; i++) {
        var added = mutations[i].addedNodes;
        for (var j = 0; j < added.length; j++) {
          var n = added[j];
          if (!n || n.nodeType !== 1) continue;
          var id = n.id || '';
          var cls = n.className || '';
          if (typeof id === 'string' && id.indexOf('minimax') !== -1) {
            if (n.parentNode) n.parentNode.removeChild(n);
          } else if (typeof cls === 'string' && cls.indexOf && cls.indexOf('minimax') !== -1) {
            if (n.parentNode) n.parentNode.removeChild(n);
          }
        }
      }
    });
    // Defer observe() until body exists — DOMContentLoaded guarantees it.
    document.addEventListener('DOMContentLoaded', function () {
      mo.observe(document.documentElement, { childList: true, subtree: true });
      // Stop watching after a few seconds; the platform's script runs once
      // per page load and there's no point keeping the observer alive.
      setTimeout(function () { mo.disconnect(); }, 8000);
    });
  }

  // --- 2. Cookie consent banner ----------------------------------------------

  function alreadyConsented() {
    try { return localStorage.getItem(STORAGE_KEY) === 'accepted'; }
    catch (e) { return false; }
  }

  function rememberConsent() {
    try { localStorage.setItem(STORAGE_KEY, 'accepted'); }
    catch (e) {
      // localStorage might be disabled (Safari private mode, etc). The
      // banner will re-show next visit, which is the conservative behavior.
    }
  }

  function S(key) {
    var locale = (window.__handleClient && window.__handleClient.locale) || 'en';
    var map = window.__handleStringsByLocale || {};
    var dict = map[locale] || map.en || {};
    return dict[key] || (map.en && map.en[key]) || key;
  }

  function buildBanner() {
    var bar = document.createElement('div');
    bar.className = 'cookie-consent';
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Cookie consent');
    // Use the locale's "Read the privacy policy" link. We default to a
    // generic English fallback if the localized version isn't available.
    var map = window.__handleStringsByLocale || {};
    var locale = (window.__handleClient && window.__handleClient.locale) || 'en';
    var privacyLinkText = (map[locale] && map[locale].footer_privacy) || 'Privacy Policy';
    var privacyHref = '/' + (locale === 'en' ? '' : locale + '/') + 'privacy';
    bar.innerHTML =
      '<div class="cookie-consent__text">' +
        S('consent_text') + ' ' +
        '<a href="' + privacyHref + '" data-nav="privacy">' + privacyLinkText + '</a>.' +
      '</div>' +
      '<button class="cookie-consent__btn" type="button" data-action="dismiss">' + S('consent_dismiss') + '</button>';
    return bar;
  }

  function show() {
    if (alreadyConsented()) return;
    if (!document.body) return;
    var bar = buildBanner();
    document.body.appendChild(bar);
    var btn = bar.querySelector('[data-action="dismiss"]');
    if (!btn) return;
    btn.addEventListener('click', function () {
      rememberConsent();
      loadAdSense();
      // Smooth fade-out so it doesn't just snap away
      bar.style.transition = 'opacity 180ms, transform 180ms';
      bar.style.opacity = '0';
      bar.style.transform = 'translateY(8px)';
      setTimeout(function () {
        if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
      }, 200);
    });
  }

  // --- 3. AdSense loading (gated on consent) ---------------------------------
  //
  // The AdSense auto-ads script is NOT loaded on page load. Instead, the
  // HTML has a placeholder config object (window.__handleAdSense) and
  // inert <ins class="adsbygoogle"> slots in the body. When the user
  // clicks the consent banner (or has already consented from a previous
  // visit), this function:
  //   1. Injects the AdSense library script with the publisher ID
  //   2. Calls (adsbygoogle = window.adsbygoogle || []).push({}) for each
  //      ad slot to tell AdSense "fill this one"
  //
  // If the user never consents, the slots stay inert. No script runs, no
  // cookies are set by AdSense, no ad requests leave the browser.

  var ADSENSE_SCRIPT_LOADED = false;

  function loadAdSense() {
    if (ADSENSE_SCRIPT_LOADED) return;
    var cfg = window.__handleAdSense;
    if (!cfg || !cfg.client) return;
    ADSENSE_SCRIPT_LOADED = true;

    // 1. Inject the AdSense library
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + encodeURIComponent(cfg.client);
    s.crossOrigin = 'anonymous';
    s.setAttribute('data-handle-adsense', '1');
    document.head.appendChild(s);

    // 2. Push each existing ad slot
    function pushSlots() {
      try {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) { /* AdSense not loaded yet */ }
    }
    if (document.readyState === 'complete') {
      pushSlots();
    } else {
      window.addEventListener('load', pushSlots);
    }
  }

  // If the user has already consented (returning visit), load immediately
  // after DOMContentLoaded. The slots in the body are already there; the
  // script just needs to be present so AdSense can fill them.
  if (alreadyConsented()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', loadAdSense);
    } else {
      loadAdSense();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', show);
  } else {
    show();
  }
})();
