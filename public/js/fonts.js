// /public/js/fonts.js
//
// Unicode font converter for the "tiktok name fonts" keyword.
//
// Maps a-z, A-Z, 0-9, and a few punctuation marks into a set of styled
// Unicode ranges. Output is the same length as input (good for bios).
// Some glyphs (e.g. in the circled set) only exist for A-Z and 0-9, so we
// fall back to the original character for unsupported inputs.

(function () {
  'use strict';

  // Each style is a function string -> string.
  const STYLES = [
    {
      name: 'Small caps',
      key: 'smallcaps',
      map: {
        a: 'ᴀ', b: 'ʙ', c: 'ᴄ', d: 'ᴅ', e: 'ᴇ', f: 'ꜰ', g: 'ɢ', h: 'ʜ', i: 'ɪ', j: 'ᴊ',
        k: 'ᴋ', l: 'ʟ', m: 'ᴍ', n: 'ɴ', o: 'ᴏ', p: 'ᴘ', q: 'ǫ', r: 'ʀ', s: 'ꜱ', t: 'ᴛ',
        u: 'ᴜ', v: 'ᴠ', w: 'ᴡ', x: 'x', y: 'ʏ', z: 'ᴢ',
        A: 'ᴀ', B: 'ʙ', C: 'ᴄ', D: 'ᴅ', E: 'ᴇ', F: 'ꜰ', G: 'ɢ', H: 'ʜ', I: 'ɪ', J: 'ᴊ',
        K: 'ᴋ', L: 'ʟ', M: 'ᴍ', N: 'ɴ', O: 'ᴏ', P: 'ᴘ', Q: 'ǫ', R: 'ʀ', S: 'ꜱ', T: 'ᴛ',
        U: 'ᴜ', V: 'ᴠ', W: 'ᴡ', X: 'x', Y: 'ʏ', Z: 'ᴢ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
      },
    },
    {
      name: 'Bold serif',
      key: 'bold',
      map: {
        a: '𝐚', b: '𝐛', c: '𝐜', d: '𝐝', e: '𝐞', f: '𝐟', g: '𝐠', h: '𝐡', i: '𝐢', j: '𝐣',
        k: '𝐤', l: '𝐥', m: '𝐦', n: '𝐧', o: '𝐨', p: '𝐩', q: '𝐪', r: '𝐫', s: '𝐬', t: '𝐭',
        u: '𝐮', v: '𝐯', w: '𝐰', x: '𝐱', y: '𝐲', z: '𝐳',
        A: '𝐀', B: '𝐁', C: '𝐂', D: '𝐃', E: '𝐄', F: '𝐅', G: '𝐆', H: '𝐇', I: '𝐈', J: '𝐉',
        K: '𝐊', L: '𝐋', M: '𝐌', N: '𝐍', O: '𝐎', P: '𝐏', Q: '𝐐', R: '𝐑', S: '𝐒', T: '𝐓',
        U: '𝐔', V: '𝐕', W: '𝐖', X: '𝐗', Y: '𝐘', Z: '𝐙',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗',
      },
    },
    {
      name: 'Italic',
      key: 'italic',
      map: {
        a: '𝘢', b: '𝘣', c: '𝘤', d: '𝘥', e: '𝘦', f: '𝘧', g: '𝘨', h: '𝘩', i: '𝘪', j: '𝘫',
        k: '𝘬', l: '𝘭', m: '𝘮', n: '𝘯', o: '𝘰', p: '𝘱', q: '𝘲', r: '𝘳', s: '𝘴', t: '𝘵',
        u: '𝘶', v: '𝘷', w: '𝘸', x: '𝘹', y: '𝘺', z: '𝘻',
        A: '𝘈', B: '𝘉', C: '𝘊', D: '𝘋', E: '𝘌', F: '𝘍', G: '𝘎', H: '𝘏', I: '𝘐', J: '𝘑',
        K: '𝘒', L: '𝘓', M: '𝘔', N: '𝘕', O: '𝘖', P: '𝘗', Q: '𝘘', R: '𝘙', S: '𝘚', T: '𝘛',
        U: '𝘜', V: '𝘝', W: '𝘞', X: '𝘟', Y: '𝘠', Z: '𝘡',
      },
    },
    {
      name: 'Script',
      key: 'script',
      map: {
        a: '𝒶', b: '𝒷', c: '𝒸', d: '𝒹', e: '𝑒', f: '𝒻', g: '𝑔', h: '𝒽', i: '𝒾', j: '𝒿',
        k: '𝓀', l: '𝓁', m: '𝓂', n: '𝓃', o: '𝑜', p: '𝓅', q: '𝓆', r: '𝓇', s: '𝓈', t: '𝓉',
        u: '𝓊', v: '𝓋', w: '𝓌', x: '𝓍', y: '𝓎', z: '𝓏',
        A: '𝒜', B: '𝐵', C: '𝒞', D: '𝒟', E: '𝐸', F: '𝐹', G: '𝒢', H: '𝐻', I: '𝐼', J: '𝒥',
        K: '𝒦', L: '𝐿', M: '𝑀', N: '𝒩', O: '𝒪', P: '𝒫', Q: '𝒬', R: '𝑅', S: '𝒮', T: '𝒯',
        U: '𝒰', V: '𝒱', W: '𝒲', X: '𝒳', Y: '𝒴', Z: '𝒵',
      },
    },
    {
      name: 'Bold script',
      key: 'bold_script',
      map: {
        a: '𝓪', b: '𝓫', c: '𝓬', d: '𝓭', e: '𝓮', f: '𝓯', g: '𝓰', h: '𝓱', i: '𝓲', j: '𝓳',
        k: '𝓴', l: '𝓵', m: '𝓶', n: '𝓷', o: '𝓸', p: '𝓹', q: '𝓺', r: '𝓻', s: '𝓼', t: '𝓽',
        u: '𝓾', v: '𝓿', w: '𝔀', x: '𝔁', y: '𝔂', z: '𝔃',
        A: '𝓐', B: '𝓑', C: '𝓒', D: '𝓓', E: '𝓔', F: '𝓕', G: '𝓖', H: '𝓗', I: '𝓘', J: '𝓙',
        K: '𝓚', L: '𝓛', M: '𝓜', N: '𝓝', O: '𝓞', P: '𝓟', Q: '𝓠', R: '𝓡', S: '𝓢', T: '𝓣',
        U: '𝓤', V: '𝓥', W: '𝓦', X: '𝓧', Y: '𝓨', Z: '𝓩',
      },
    },
    {
      name: 'Fraktur',
      key: 'fraktur',
      map: {
        a: '𝔞', b: '𝔟', c: '𝔠', d: '𝔡', e: '𝔢', f: '𝔣', g: '𝔤', h: '𝔥', i: '𝔦', j: '𝔧',
        k: '𝔨', l: '𝔩', m: '𝔪', n: '𝔫', o: '𝔬', p: '𝔭', q: '𝔮', r: '𝔯', s: '𝔰', t: '𝔱',
        u: '𝔲', v: '𝔳', w: '𝔴', x: '𝔵', y: '𝔶', z: '𝔷',
        A: '𝔄', B: '𝔅', C: 'ℭ', D: '𝔇', E: '𝔈', F: '𝔉', G: '𝔊', H: 'ℌ', I: 'ℑ', J: '𝔍',
        K: '𝔎', L: '𝔏', M: '𝔐', N: '𝔑', O: '𝔒', P: '𝔓', Q: '𝔔', R: 'ℜ', S: '𝔖', T: '𝔗',
        U: '𝔘', V: '𝔙', W: '𝔚', X: '𝔛', Y: '𝔜', Z: 'ℨ',
      },
    },
    {
      name: 'Circled',
      key: 'circled',
      map: {
        a: 'ⓐ', b: 'ⓑ', c: 'ⓒ', d: 'ⓓ', e: 'ⓔ', f: 'ⓕ', g: 'ⓖ', h: 'ⓗ', i: 'ⓘ', j: 'ⓙ',
        k: 'ⓚ', l: 'ⓛ', m: 'ⓜ', n: 'ⓝ', o: 'ⓞ', p: 'ⓟ', q: 'ⓠ', r: 'ⓡ', s: 'ⓢ', t: 'ⓣ',
        u: 'ⓤ', v: 'ⓥ', w: 'ⓦ', x: 'ⓧ', y: 'ⓨ', z: 'ⓩ',
        A: 'Ⓐ', B: 'Ⓑ', C: 'Ⓒ', D: 'Ⓓ', E: 'Ⓔ', F: 'Ⓕ', G: 'Ⓖ', H: 'Ⓗ', I: 'Ⓘ', J: 'Ⓙ',
        K: 'Ⓚ', L: 'Ⓛ', M: 'Ⓜ', N: 'Ⓝ', O: 'Ⓞ', P: 'Ⓟ', Q: 'Ⓠ', R: 'Ⓡ', S: 'Ⓢ', T: 'Ⓣ',
        U: 'Ⓤ', V: 'Ⓥ', W: 'Ⓦ', X: 'Ⓧ', Y: 'Ⓨ', Z: 'Ⓩ',
        '0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④',
        '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨',
      },
    },
    {
      name: 'Squared',
      key: 'squared',
      map: {
        A: '🅰', B: '🅱', C: '🅲', D: '🅳', E: '🅴', F: '🅵', G: '🅶', H: '🅷', I: '🅸', J: '🅹',
        K: '🅺', L: '🅻', M: '🅼', N: '🅽', O: '🅾', P: '🅿', Q: '🆀', R: '🆁', S: '🆂', T: '🆃',
        U: '🆄', V: '🆅', W: '🆆', X: '🆇', Y: '🆈', Z: '🆉',
      },
    },
    {
      name: 'Strikethrough',
      key: 'strikethrough',
      map: makeCombiner('\u0336'),
    },
    {
      name: 'Underline',
      key: 'underline',
      map: makeCombiner('\u0332'),
    },
    {
      name: 'Reverse (flip)',
      key: 'reverse',
      map: makeReverse(),
    },
  ];

  function makeCombiner(mark) {
    return new Proxy({}, {
      get(_, char) { return char + mark; },
    });
  }
  function makeReverse() {
    const pairs = {
      a: 'ɐ', b: 'q', c: 'ɔ', d: 'p', e: 'ǝ', f: 'ɟ', g: 'ƃ', h: 'ɥ', i: 'ᴉ', j: 'ɾ',
      k: 'ʞ', l: '˥', m: 'ɯ', n: 'u', o: 'o', p: 'd', q: 'b', r: 'ɹ', s: 's', t: 'ʇ',
      u: 'n', v: 'ʌ', w: 'ʍ', x: 'x', y: 'ʎ', z: 'z',
      A: '∀', B: 'ꓭ', C: 'Ɔ', D: 'p', E: 'Ǝ', F: 'Ⅎ', G: 'פ', H: 'H', I: 'I', J: 'ſ',
      K: 'ʞ', L: '˥', M: 'W', N: 'N', O: 'O', P: 'Ԁ', Q: 'Q', R: 'ɹ', S: 'S', T: '⊥',
      U: '∩', V: 'Λ', W: 'M', X: 'X', Y: '⅄', Z: 'Z',
      '0': '0', '1': 'Ɩ', '2': 'ᄅ', '3': 'Ɛ', '4': 'ㄣ', '5': 'ϛ', '6': '9', '7': 'ㄥ', '8': '8', '9': '6',
      '.': '˙', ',': "'", '?': '¿', '!': '¡',
    };
    return pairs;
  }

  function applyStyle(text, style) {
    let out = '';
    for (const ch of text) {
      if (style.map && style.map[ch] != null) out += style.map[ch];
      else if (style.map && typeof style.map.get === 'function' && style.map.get(ch) != null) out += style.map.get(ch);
      else out += ch;
    }
    return out;
  }

  // Per-locale name map for the font styles. window.__handleStringsByLocale
  // is set by strings.js; we look up each style's display name from a
  // mapping table so the names follow the page's locale.
  const NAME_KEYS = {
    smallcaps: 'font_smallcaps',
    bold: 'font_bold',
    italic: 'font_italic',
    script: 'font_script',
    bold_script: 'font_bold_script',
    fraktur: 'font_fraktur',
    circled: 'font_circled',
    squared: 'font_squared',
    strikethrough: 'font_strikethrough',
    underline: 'font_underline',
    reverse: 'font_reverse',
  };
  function S(key) {
    const locale = (window.__handleClient && window.__handleClient.locale) || 'en';
    const map = window.__handleStringsByLocale || {};
    const dict = map[locale] || map.en || {};
    return dict[key] || (map.en && map.en[key]) || key;
  }

  function init() {
    const input = document.getElementById('font-input');
    const grid = document.getElementById('font-grid');
    if (!input || !grid) return;

    // Localize the static labels around the input
    const yourTextLabel = document.querySelector('[data-i18n="label_your_text"]');
    if (yourTextLabel) yourTextLabel.textContent = S('label_your_text');
    if (input) {
      const help = input.closest('.field')?.querySelector('.help');
      if (help) help.textContent = S('help_your_text');
    }
    const heading = document.querySelector('[data-i18n="fonts_heading"]');
    if (heading) heading.textContent = S('fonts_heading');
    const desc = document.querySelector('[data-i18n="fonts_desc"]');
    if (desc) desc.textContent = S('fonts_desc');

    function render(value) {
      const v = value || '';
      grid.innerHTML = '';
      STYLES.forEach((style) => {
        const row = document.createElement('div');
        row.className = 'font-row';
        const sample = applyStyle(v, style);
        const name = S(NAME_KEYS[style.key] || 'font_' + style.key);
        row.innerHTML =
          '<span class="name">' + name + '</span>' +
          '<span class="sample">' + (sample || '<span style="color:var(--ink-mute)">(empty)</span>') + '</span>' +
          '<button class="btn-ghost" type="button" data-sample="' + escapeAttr(sample) + '">' + S('btn_copy') + '</button>';
        grid.appendChild(row);
      });
    }

    grid.addEventListener('click', async (e) => {
      const btn = e.target.closest('button[data-sample]');
      if (!btn) return;
      const text = btn.getAttribute('data-sample') || '';
      try {
        await navigator.clipboard.writeText(text);
        const orig = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(() => { btn.textContent = orig; }, 1200);
      } catch (err) {
        btn.textContent = 'Copy failed';
      }
    });

    function escapeAttr(s) {
      return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    input.addEventListener('input', (e) => render(e.target.value));
    render(input.value);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
