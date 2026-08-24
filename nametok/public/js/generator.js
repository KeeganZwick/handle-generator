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
      els.status.textContent = 'Loading… try again in a second.';
      return;
    }
    els.generateBtn.disabled = true;
    els.status.textContent = 'Generating…';
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
        ? `${out.handles.length} names ready, checking availability on TikTok…`
        : 'No names — try a different keyword or category.';
      await checkAll();
    } catch (e) {
      els.status.textContent = 'Something went wrong generating names. Try again.';
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
    els.status.textContent = 'Checking availability on TikTok…';

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
      els.status.textContent = 'Done. Click any name to open it on TikTok.';
    } else if (verified > 0 && unverified > 0) {
      els.status.textContent = isPreview
        ? `${verified} could not be checked from this preview — click any name to verify on TikTok directly.`
        : `${unverified} could not be checked (transient). Click any name to verify on TikTok directly.`;
    } else {
      els.status.textContent = isPreview
        ? 'Preview deploy — the live check needs the local Node backend. Click any name to verify on TikTok directly.'
        : 'Could not reach TikTok right now. Click any name to verify it directly.';
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
      return '<span class="status status-pending"><span class="dot dot-pending"></span>checking…</span>';
    }
    if (result.status === 'likely_available') {
      return '<span class="status status-available" title="Likely available — confirm on TikTok"><span class="dot dot-available"></span>likely free</span>';
    }
    if (result.status === 'likely_taken') {
      return '<span class="status status-taken" title="Likely taken — TikTok returned a live profile"><span class="dot dot-taken"></span>likely taken</span>';
    }
    return '<span class="status status-unverified" title="Availability could not be verified — click the name to confirm on TikTok"><span class="dot dot-unverified"></span>unknown</span>';
  }

  function tiktokLink(handle) {
    return 'https://www.tiktok.com/@' + encodeURIComponent(handle);
  }

  function shortTime(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    if (isNaN(d.getTime())) return '';
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
      const cached = r.cached ? '(cached)' : '';
      meta.innerHTML = 'Checked ' + (t || 'just now') + ' — availability can change at any time' + (cached ? ' · ' + cached : '');
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
      row.innerHTML =
        '<div style="flex:1;min-width:0">' +
          '<div class="handle">@' + escapeHtml(r.handle) + '</div>' +
          '<div class="meta">Checked ' + (t || 'just now') + ' — availability can change at any time</div>' +
        '</div>' +
        '<div class="status">' + statusPill(r) + '</div>' +
        '<div class="actions">' +
          '<button class="btn-ghost btn-sm" type="button" data-action="copy" data-handle="' + escapeAttr(r.handle) + '">Copy</button>' +
          '<a class="btn-primary btn-sm" href="' + tiktokLink(r.handle) + '" target="_blank" rel="noopener noreferrer">Open on TikTok ↗</a>' +
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

    if (pending === total) {
      els.summary.textContent = `Checking ${total} ${total === 1 ? 'name' : 'names'} against TikTok…`;
    } else {
      const parts = [];
      if (avail) parts.push(`${avail} likely available`);
      if (taken) parts.push(`${taken} likely taken`);
      if (unver) parts.push(`${unver} unknown`);
      if (pending) parts.push(`${pending} checking…`);
      els.summary.textContent = `${total} ${total === 1 ? 'name' : 'names'} — ` + (parts.length ? parts.join(' · ') : 'no verdicts yet');
    }
    els.summary.hidden = false;
  }

  function renderDisclaimer() {
    if (!els.disclaimer) return;
    const unverified = state.lastResults.filter((r) => r.status === 'unverified').length;
    if (unverified === 0) { els.disclaimer.hidden = true; els.disclaimer.textContent = ''; return; }
    if (isPreview) {
      els.disclaimer.innerHTML = '<strong>Preview deploy.</strong> The live availability check needs the local Node backend (<code>npm install &amp;&amp; npm start</code>). Every result here will read "Unknown" until then. Each "Open on TikTok" link goes straight to the live profile page, so you can verify by eye.';
    } else {
      els.disclaimer.innerHTML = '<strong>Heads up.</strong> We could not reach TikTok\'s check endpoint for ' + unverified + ' of these ' + state.lastResults.length + ' handles (the result shows "Unknown" for each). Each "Open on TikTok" link goes straight to the profile page so you can confirm by eye. Try Re-check in a minute.';
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
        btn.textContent = 'Copied';
        setTimeout(() => { btn.textContent = orig; }, 1200);
      } catch (err) {
        btn.textContent = 'Copy failed';
      }
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function escapeAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
  }
})();
