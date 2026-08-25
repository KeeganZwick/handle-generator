#!/usr/bin/env python3
"""
Inject the result-card strings (verdict pills, action buttons, meta text,
summary line, disclaimer) from i18n/results_strings.py into public/js/strings.js,
preserving every existing key and value untouched.

We add the new keys as a single new section ("// Result cards") right before
the closing brace of each locale block. This keeps the file diff-friendly and
makes the additions easy to audit.

Idempotent: re-running the script is a no-op because we tag the new block
with a sentinel comment that we search for first.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
STRINGS_JS = ROOT.parent / 'public' / 'js' / 'strings.js'

# Import the translations
import sys
sys.path.insert(0, str(ROOT))
from results_strings import RESULTS

SENTINEL = '  // [results_strings.py injected block]'
SENTINEL_END = '  // [/results_strings.py]'

# Escape single quotes for JS single-quoted string literals
def js_escape(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")

# Build the JS chunk for one locale.
# We pick a key-order that groups things logically for readability.
KEY_ORDER = [
    # Verdict pills
    'verdict_checking',
    'verdict_likely_available',
    'verdict_likely_taken',
    'verdict_unknown',
    'verdict_title_available',
    'verdict_title_taken',
    'verdict_title_unknown',
    # Action buttons
    'btn_open_tiktok',
    # Per-row meta
    'result_meta_checked',
    'result_meta_just_now',
    'result_meta_disclaimer',
    'result_meta_cached',
    'result_copy_failed',
    # Summary line above the results
    'summary_checking_template',
    'summary_name',
    'summary_names',
    'summary_separator',
    'summary_likely_available',
    'summary_likely_taken',
    'summary_unknown',
    'summary_checking',
    'summary_no_verdicts',
    # Disclaimer block
    'disclaimer_preview',
    'disclaimer_preview_body',
    'disclaimer_headsup',
    'disclaimer_headsup_body',
    # Status text under the Generate button (also user-facing)
    'status_loading',
    'status_generating',
    'status_names_ready',
    'status_no_names',
    'status_checking',
    'status_done',
    'status_partial_preview',
    'status_partial_live',
    'status_all_unverified_preview',
    'status_all_unverified_live',
    'status_error',
]

def build_chunk(locale):
    lines = [SENTINEL, '  // Result card UI (verdict pills, action buttons, meta, summary, disclaimer)']
    data = RESULTS[locale]
    for key in KEY_ORDER:
        val = data[key]
        lines.append(f"    {key}: '{js_escape(val)}',")
    lines.append(SENTINEL_END)
    return '\n'.join(lines)

# Read the file
src = STRINGS_JS.read_text(encoding='utf-8')

# If we've already injected, remove the old injected block first (idempotent)
# Pattern: from SENTINEL through SENTINEL_END (both lines), inclusive.
old_block_re = re.compile(
    re.escape(SENTINEL) + r'.*?' + re.escape(SENTINEL_END) + r'\n?',
    re.DOTALL
)
new_src = old_block_re.sub('', src)
if new_src != src:
    print(f'Removed previous injection ({len(src) - len(new_src)} bytes)')

# Now inject into each locale block
LANGS = ['en', 'es', 'de', 'fr', 'it', 'pt', 'nl', 'pl', 'ru',
         'zh', 'vi', 'id', 'ms', 'tl', 'hi', 'bn', 'ur', 'ar']

for lang in LANGS:
    # Find the start of the block: "  lang: {"
    start_re = re.compile(rf'  {lang}:\s*\{{')
    start_match = start_re.search(new_src)
    if not start_match:
        print(f'✗ {lang}: block start not found')
        continue
    start = start_match.start()
    # Find the matching "  }," or "  }" close after start. The locale blocks
    # are at the same indent level (2 spaces), so we search for the next
    # "\n  }," at column 2 (preceded only by spaces).
    end_re = re.compile(r'\n  \},?\n')
    end_match = end_re.search(new_src, start)
    if not end_match:
        print(f'✗ {lang}: block end not found')
        continue
    block = new_src[start:end_match.start()]
    chunk = build_chunk(lang)
    new_block = block + '\n\n' + chunk + '\n  },\n'
    new_src = new_src[:start] + new_block + new_src[end_match.end():]
    print(f'✓ {lang}: injected {len(KEY_ORDER)} keys')

STRINGS_JS.write_text(new_src, encoding='utf-8')
print(f'\nWrote {len(new_src):,} bytes to {STRINGS_JS}')
