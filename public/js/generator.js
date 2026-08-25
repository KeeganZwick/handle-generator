// /public/js/generator.js
//
// Generator page logic. Talks to window.__handleClient (see client-shim.js),
// which in turn either hits the real /api/* endpoints (local build) or runs
// everything client-side (static deploy).

(function () {
  'use strict';

  const els = {
    keyword: document.getElementById('keyword'),
    category: document.getElementById('category'),
    count: document.getElementById('count'),
    vibes: document.getElementById('vibes'),
    generateBtn: document.getElementById('generate-btn'),
    recheckBtn: document.getElementById('recheck-btn'),
    results: document.getElementById('results'),
    status: document.getElementById('status-text'),
    summary: document.getElementById('results-summary'),
    disclaimer: document.getElementById('disclaimer'),
  };

  const state = {
    vibe: 'cool',
    lastResults: [],
    checking: false,
  };

  // Per-locale UI strings (window.__handleStringsByLocale from strings.js).
  // Falls back to English if no per-locale object is found.
  function S(key) {
    const locale = (window.__handleClient && window.__handleClient.locale) || 'en';
    const map = window.__handleStringsByLocale || {};
    const dict = map[locale] || map.en || {};
    return dict[key] || (map.en && map.en[key]) || key;
  }

  // Apply localized text to the form labels, placeholders, and buttons
  // that the static template ships in English. We do this on load and
  // also after router applies a route change (so the language switcher
  // can re-translate in-place when the URL changes).
  function applyGeneratorStrings() {
    if (els.keyword) {
      const label = els.keyword.closest('.field')?.querySelector('label');
      if (label) label.textContent = S('label_keyword');
      els.keyword.placeholder = S('placeholder_keyword');
    }
    const help = document.querySelector('[data-i18n="help_keyword"]');
    if (help) help.textContent = S('help_keyword');
    const nicheLabel = document.querySelector('[data-i18n="label_niche"]');
    if (nicheLabel) nicheLabel.textContent = S('label_niche');
    const countLabel = document.querySelector('[data-i18n="label_count"]');
    if (countLabel) countLabel.textContent = S('label_count');
    const vibeLabel = document.querySelector('[data-i18n="label_vibe"]');
    if (vibeLabel) vibeLabel.textContent = S('label_vibe');
    if (els.generateBtn) els.generateBtn.textContent = S('btn_generate');
    if (els.recheckBtn) els.recheckBtn.textContent = S('btn_recheck');
    const freeTag = document.querySelector('[data-i18n="free_tag"]');
    if (freeTag) freeTag.textContent = S('free_tag');
  }

  // In preview mode (static deploy, no Node backend) the live check is a
  // stub. Hide Re-check — clicking it would do nothing — and soften the
  // banner copy so it explains why every result says "Unknown" instead of
  // pretending it's a transient network error.
  const isPreview = !!(window.__handleClient && window.__handleClient.isPreview);
  if (isPreview && els.recheckBtn) {
    els.recheckBtn.hidden = true;
  }

  function setVibe(name) {
    state.vibe = name;
    if (!els.vibes) return;
    els.vibes.querySelectorAll('.vibe-chip').forEach((chip) => {
      const isActive = chip.getAttribute('data-vibe') === name;
      chip.classList.toggle('is-active', isActive);
      chip.setAttribute('aria-checked', isActive ? 'true' : 'false');
    });
  }
  if (els.vibes) {
    els.vibes.addEventListener('click', (e) => {
      const chip = e.target.closest('.vibe-chip');
      if (!chip) return;
      setVibe(chip.getAttribute('data-vibe'));
    });
    els.vibes.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      const chip = e.target.closest('.vibe-chip');
      if (!chip) return;
      e.preventDefault();
      setVibe(chip.getAttribute('data-vibe'));
    });
  }

  // Strip characters that aren't allowed in a TikTok handle before
  // sending to the generator. The HTML <input> also has maxlength=24
  // and pattern="[a-zA-Z0-9._]{0,24}" so this is a defense-in-depth
  // trim for pasted / typed values; we never want a 30-char string
  // or an emoji making it to the generator.
  function sanitizeKeyword(s) {
    return String(s || '').toLowerCase().replace(/[^a-z0-9._]/g, '').slice(0, 24);
  }

  async function generate() {
    if (!els.generateBtn) return;
    if (!window.__handleClient) {
      els.status.textContent = S('status_loading');
      return;
    }
    els.generateBtn.disabled = true;
    els.status.textContent = S('status_generating');
    if (els.summary) { els.summary.hidden = true; els.summary.textContent = ''; }
    if (els.disclaimer) { els.disclaimer.hidden = true; els.disclaimer.textContent = ''; }
    try {
      const out = window.__handleClient.generate({
        keyword: sanitizeKeyword(els.keyword.value),
        category: els.category.value,
        vibe: state.vibe,
        count: parseInt(els.count.value, 10) || 12,
      });
      state.lastResults = (out.handles || []).map((h) => ({ handle: h, status: 'pending' }));
      renderResults();
      renderSummary();
      if (els.recheckBtn) els.recheckBtn.disabled = false;
      els.status.textContent = out.handles.length
        ? S('status_names_ready').replace('{N}', String(out.handles.length))
        : S('status_no_names');
      await checkAll();
    } catch (e) {
      els.status.textContent = S('status_error');
    } finally {
      els.generateBtn.disabled = false;
    }
  }
  if (els.generateBtn) {
    els.generateBtn.addEventListener('click', generate);
  }
  if (els.keyword) {
    els.keyword.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); generate(); }
    });
  }
  if (els.recheckBtn) {
    els.recheckBtn.addEventListener('click', () => {
      state.lastResults = state.lastResults.map((r) => ({ ...r, status: 'pending' }));
      renderResults();
      checkAll();
    });
  }

  async function checkOne(handle) {
    if (!window.__handleClient) return { handle, status: 'unverified', checkedAt: new Date().toISOString(), backend: 'no-client', note: 'shim not loaded' };
    return window.__handleClient.check(handle);
  }

  async function checkAll() {
    if (state.checking || !state.lastResults.length) return;
    state.checking = true;
    els.status.textContent = S('status_checking');

    const queue = state.lastResults.slice();
    const workers = Array.from({ length: 4 }, () => (async () => {
      while (queue.length) {
        const next = queue.shift();
        if (!next) return;
        const result = await checkOne(next.handle);
        const idx = state.lastResults.findIndex((r) => r.handle === result.handle);
        if (idx >= 0) {
          state.lastResults[idx] = { ...state.lastResults[idx], ...result };
          renderRow(idx);
          renderSummary();
        }
      }
    })());
    await Promise.all(workers);

    state.checking = false;
    const verified = state.lastResults.filter((r) => r.status === 'likely_available' || r.status === 'likely_taken').length;
    const unverified = state.lastResults.filter((r) => r.status === 'unverified').length;
    if (verified > 0 && unverified === 0) {
      els.status.textContent = S('status_done');
    } else if (verified > 0 && unverified > 0) {
      els.status.textContent = isPreview
        ? S('status_partial_preview').replace('{N}', String(unverified))
        : S('status_partial_live').replace('{N}', String(unverified));
    } else {
      els.status.textContent = isPreview
        ? S('status_all_unverified_preview')
        : S('status_all_unverified_live');
    }
    renderSummary();
    renderDisclaimer();
  }

  // Compact per-row status. The bulk of the verdict lives in the top
  // summary so the list rows stay calm and the primary action (Open on
  // TikTok) doesn't compete with a colored pill.
  //
  // The internal `status: 'unverified'` code from the server is kept as
  // the data-model value (so we don't have to touch the API contract);
  // we only change the user-facing label to "Unknown" — same quiet
  // text-plus-dot styling, just the word the user reads.
  function statusPill(result) {
    if (!result || result.status === 'pending') {
      return '<span class="status status-pending"><span class="dot dot-pending"></span>' + escapeHtml(S('verdict_checking')) + '</span>';
    }
    if (result.status === 'likely_available') {
      return '<span class="status status-available" title="' + escapeAttr(S('verdict_title_available')) + '"><span class="dot dot-available"></span>' + escapeHtml(S('verdict_likely_available')) + '</span>';
    }
    if (result.status === 'likely_taken') {
      return '<span class="status status-taken" title="' + escapeAttr(S('verdict_title_taken')) + '"><span class="dot dot-taken"></span>' + escapeHtml(S('verdict_likely_taken')) + '</span>';
    }
    return '<span class="status status-unverified" title="' + escapeAttr(S('verdict_title_unknown')) + '"><span class="dot dot-unverified"></span>' + escapeHtml(S('verdict_unknown')) + '</span>';
  }

  function tiktokLink(handle) {
    return 'https://www.tiktok.com/@' + encodeURIComponent(handle);
  }

  function shortTime(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    // Use the browser's locale for time format (12h vs 24h based on the
    // user's OS / browser setting) and the browser's local timezone. The
    // page language is a separate concern — the user expects to see the
    // time as it is "for them, right now", not in a language-locked
    // timezone. This is the same pattern used by most time-display UI
    // (e.g. Gmail's inbox timestamps).
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function renderRow(idx) {
    const row = els.results.querySelector('[data-idx="' + idx + '"]');
    if (!row) return;
    const r = state.lastResults[idx];
    row.classList.toggle('is-checking', r.status === 'pending');
    const pill = row.querySelector('.status');
    const meta = row.querySelector('.meta');
    if (pill) pill.outerHTML = statusPill(r);
    if (meta) {
      const t = shortTime(r.checkedAt);
      const cached = r.cached ? S('result_meta_cached') : '';
      const justNow = S('result_meta_just_now');
      const checked = S('result_meta_checked');
      const disclaimer = S('result_meta_disclaimer');
      const sep = cached ? ' · ' + cached : '';
      meta.textContent = checked + ' ' + (t || justNow) + ' — ' + disclaimer + sep;
    }
  }

  function renderResults() {
    if (!els.results) return;
    els.results.innerHTML = '';
    state.lastResults.forEach((r, idx) => {
      const row = document.createElement('div');
      row.className = 'result' + (r.status === 'pending' ? ' is-checking' : '');
      row.setAttribute('data-idx', String(idx));
      const t = shortTime(r.checkedAt);
      const justNow = S('result_meta_just_now');
      const checked = S('result_meta_checked');
      const disclaimer = S('result_meta_disclaimer');
      const metaText = checked + ' ' + (t || justNow) + ' — ' + disclaimer;
      row.innerHTML =
        '<div style="flex:1;min-width:0">' +
          '<div class="handle">@' + escapeHtml(r.handle) + '</div>' +
          '<div class="meta">' + escapeHtml(metaText) + '</div>' +
        '</div>' +
        '<div class="status">' + statusPill(r) + '</div>' +
        '<div class="actions">' +
          '<button class="btn-ghost btn-sm" type="button" data-action="copy" data-handle="' + escapeAttr(r.handle) + '">' + escapeHtml(S('btn_copy')) + '</button>' +
          '<a class="btn-primary btn-sm" href="' + tiktokLink(r.handle) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(S('btn_open_tiktok')) + '</a>' +
        '</div>';
      els.results.appendChild(row);
    });
  }

  // Top-of-results summary so the user gets a count, not 12 identical
  // colored pills screaming at them. "Unknown" is the user-facing
  // label for results where the check couldn't run (preview mode or
  // a transient failure on the live check); the internal status code
  // is still 'unverified' so the API contract doesn't have to change.
  function renderSummary() {
    if (!els.summary) return;
    if (!state.lastResults.length) { els.summary.hidden = true; els.summary.textContent = ''; return; }
    const total = state.lastResults.length;
    const pending = state.lastResults.filter((r) => !r.status || r.status === 'pending').length;
    const avail = state.lastResults.filter((r) => r.status === 'likely_available').length;
    const taken = state.lastResults.filter((r) => r.status === 'likely_taken').length;
    const unver = state.lastResults.filter((r) => r.status === 'unverified').length;

    const nameWord = total === 1 ? S('summary_name') : S('summary_names');
    if (pending === total) {
      els.summary.textContent = S('summary_checking_template').replace('{N}', String(total)).replace('{name}', nameWord);
    } else {
      const parts = [];
      if (avail) parts.push(S('summary_likely_available').replace('{N}', String(avail)));
      if (taken) parts.push(S('summary_likely_taken').replace('{N}', String(taken)));
      if (unver) parts.push(S('summary_unknown').replace('{N}', String(unver)));
      if (pending) parts.push(S('summary_checking').replace('{N}', String(pending)));
      const prefix = S('summary_names') ? total + ' ' + nameWord + S('summary_separator') : '';
      els.summary.textContent = prefix + (parts.length ? parts.join(' · ') : S('summary_no_verdicts'));
    }
    els.summary.hidden = false;
  }

  function renderDisclaimer() {
    if (!els.disclaimer) return;
    const unverified = state.lastResults.filter((r) => r.status === 'unverified').length;
    if (unverified === 0) { els.disclaimer.hidden = true; els.disclaimer.textContent = ''; return; }
    if (isPreview) {
      const body = S('disclaimer_preview_body');
      // Replace the static "Unknown" with the localized verdict label so the
      // user sees their own language for the result state name.
      const unknown = S('verdict_unknown');
      const openBtn = S('btn_open_tiktok').replace(' ↗', '');
      const bodyLocalized = body
        .replace(/"Unknown"/g, '"' + unknown + '"')
        .replace(/"Open on TikTok"/g, '"' + openBtn + '"');
      els.disclaimer.innerHTML = '<strong>' + escapeHtml(S('disclaimer_preview')) + '</strong> ' + bodyLocalized;
    } else {
      const body = S('disclaimer_headsup_body')
        .replace('{X}', String(unverified))
        .replace('{N}', String(state.lastResults.length));
      const unknown = S('verdict_unknown');
      const openBtn = S('btn_open_tiktok').replace(' ↗', '');
      const bodyLocalized = body
        .replace(/"Unknown"/g, '"' + unknown + '"')
        .replace(/"Open on TikTok"/g, '"' + openBtn + '"');
      els.disclaimer.innerHTML = '<strong>' + escapeHtml(S('disclaimer_headsup')) + '</strong> ' + bodyLocalized;
    }
    els.disclaimer.hidden = false;
  }

  if (els.results) {
    els.results.addEventListener('click', async (e) => {
      const btn = e.target.closest('button[data-action="copy"]');
      if (!btn) return;
      const handle = btn.getAttribute('data-handle') || '';
      try {
        await navigator.clipboard.writeText('@' + handle);
        const orig = btn.textContent;
        btn.textContent = S('btn_copied');
        setTimeout(() => { btn.textContent = orig; }, 1200);
      } catch (err) {
        btn.textContent = S('result_copy_failed');
      }
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function escapeAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
  }

  // Apply localized strings on first load and after every route change
  // (so the language switcher can re-translate in-place when the URL
  // changes — though the static deploy currently does a full reload on
  // locale change, this is the right shape if we ever switch to SPA).
  applyGeneratorStrings();
  document.addEventListener('routechange', applyGeneratorStrings);
})();
