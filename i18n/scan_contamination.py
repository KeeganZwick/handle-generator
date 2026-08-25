#!/usr/bin/env python3
"""
Cross-locale contamination scan: for each language's translation file, look
for characters from scripts that don't belong to that language. We catch
stray CJK, Arabic, Cyrillic, Devanagari, Bengali, Urdu, etc. characters
that might have leaked from a different language's translation.

Strategy: for each lang, build a set of "allowed" character ranges. Then
walk the file, and any character outside that set is reported as suspicious
(with the source line, the key it's in, and the line number).

Run as: python3 i18n/scan_contamination.py
"""

import re
import sys
from pathlib import Path

# Unicode ranges by script
SCRIPTS = {
    'latin_extended': (0x00A0, 0x024F),  # Latin-1 + Latin Extended A + B
    'cyrillic':       (0x0400, 0x04FF),
    'cjk':            (0x4E00, 0x9FFF),  # CJK Unified Ideographs (most common)
    'cjk_ext_a':      (0x3400, 0x4DBF),
    'arabic':         (0x0600, 0x06FF),
    'arabic_suppl':    (0x0750, 0x077F),
    'devanagari':     (0x0900, 0x097F),
    'bengali':        (0x0980, 0x09FF),
    'thai':           (0x0E00, 0x0E7F),
    'han_simplified_ext_a': (0x3400, 0x4DBF),
    'hangul':         (0xAC00, 0xD7AF),  # Korean
    'hiragana':       (0x3040, 0x309F),
    'katakana':       (0x30A0, 0x30FF),
    'greek':          (0x0370, 0x03FF),
    'hebrew':         (0x0590, 0x05FF),
    'tibetan':        (0x0F00, 0x0FFF),
    'gujarati':       (0x0A80, 0x0AFF),
    'gurmukhi':       (0x0A00, 0x0A7F),
    'telugu':         (0x0C00, 0x0C7F),
    'tamil':          (0x0B80, 0x0BFF),
    'kannada':        (0x0C80, 0x0CFF),
    'malayalam':      (0x0D00, 0x0D7F),
    'sinhala':        (0x0D80, 0x0DFF),
    'khmer':          (0x1780, 0x17FF),
    'lao':            (0x0E80, 0x0EFF),
    'myanmar':        (0x1000, 0x109F),
    'ethiopic':       (0x1200, 0x137F),
}

# For each locale, define which script sets are EXPECTED (and which
# are explicitly FORBIDDEN = the bug we're hunting).
ALLOWED_FOR_LANG = {
    'en': {'latin_extended'},
    'es': {'latin_extended'},
    'de': {'latin_extended'},
    'fr': {'latin_extended'},
    'it': {'latin_extended'},
    'pt': {'latin_extended'},
    'nl': {'latin_extended'},
    'pl': {'latin_extended'},
    'vi': {'latin_extended'},  # Vietnamese has lots of Latin diacritics but no other scripts
    'id': {'latin_extended'},
    'ms': {'latin_extended'},
    'tl': {'latin_extended'},
    'ru': {'latin_extended', 'cyrillic'},
    'zh': {'latin_extended', 'cjk', 'cjk_ext_a'},
    'hi': {'latin_extended', 'devanagari'},
    'bn': {'latin_extended', 'bengali'},
    'ar': {'latin_extended', 'arabic', 'arabic_suppl'},
    'ur': {'latin_extended', 'arabic', 'arabic_suppl'},
}

# Some chars are universally fine: ASCII control, basic punctuation, digits
# (within ASCII), common symbols. The check below defines "suspicious" as any
# char that is clearly part of a non-Latin script that is NOT in the allowed
# set for that file's language.

def char_script(cp):
    """Return which script this codepoint belongs to, or None if it's common
    (punctuation, digits, ASCII, symbols, etc.)."""
    if cp < 0x0080:
        return None  # ASCII control + basic Latin
    if cp < 0x00A0:
        return None  # C1 controls + Latin-1 punctuation
    for name, (lo, hi) in SCRIPTS.items():
        if lo <= cp <= hi:
            return name
    return None

# The U+0964 DANDA (Devanagari) is shared with Bengali and other Indic
# scripts in actual usage. Unicode standard says U+0964 is Devanagari
# specifically, but in practice Bengali (bn) uses both U+0964 and its
# own U+09ED. We allow U+0964 in all Indic-script langs to avoid false
# positives.
SHARED_INDIC_DANDA = {0x0964, 0x0965}

# Unicode block for the Ideographic Description, CJK Symbols, CJK Compatibility
# We treat anything in the CJK ranges as cjk-script and ignore for non-zh langs
IGNORE_FOR_LATIN = set([
    'cjk', 'cjk_ext_a', 'cyrillic', 'arabic', 'arabic_suppl', 'devanagari',
    'bengali', 'hangul', 'hiragana', 'katakana', 'greek', 'hebrew',
    'tibetan', 'gujarati', 'gurmukhi', 'telugu', 'tamil', 'kannada',
    'malayalam', 'sinhala', 'khmer', 'lao', 'myanmar', 'ethiopic',
    'thai', 'han_simplified_ext_a',
])

def scan_text(text, lang, source_name=''):
    """Return a list of (line, col, char, script) tuples for suspicious chars."""
    allowed = ALLOWED_FOR_LANG[lang]
    findings = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        script = char_script(cp)
        if script is None:
            continue  # punctuation, digits, ASCII, symbols - fine
        if script in allowed:
            continue  # expected for this lang
        # Special case: latin_extended is in all "latin" langs
        if script == 'latin_extended':
            continue
        # This character is from a script NOT in the allowed set for this lang.
        findings.append((text.count('\n', 0, i) + 1, i - (text.rfind('\n', 0, i) + 1), ch, script))
    return findings

def scan_file(path, lang):
    """Scan a file for stray characters. Returns list of findings."""
    try:
        text = path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return None
    return scan_text(text, lang, str(path))

# Source files to scan
SOURCE_FILES = [
    ('i18n/body_translations.py', 'multi'),
    ('i18n/page_strings.py', 'multi'),
    ('i18n/extra_strings.py', 'multi'),
    ('i18n/options_strings.py', 'multi'),
    ('i18n/per_page_seo.py', 'multi'),
    ('i18n/pages_translations.py', 'tier1'),
    ('i18n/pages_translations_tier2.py', 'tier2'),
    ('i18n/results_strings.py', 'multi'),
    ('i18n/legal_translations.py', 'en'),
    ('i18n/legal_translations_filled.py', 'multi'),
    ('public/js/strings.js', 'multi'),
    ('public/js/titles.js', 'multi'),
]

# A multi-tier file has separate dicts per lang. We need to find each lang's
# block and scan only that block against that lang's allowed set.
# A tier1 file has Tier 1 langs (es, de, fr, it, pt, nl, pl, ru).
# A tier2 file has Tier 2 langs (zh, vi, id, ms, tl, hi, bn, ur, ar).
# An en file has only English.

TIER1_LANGS = ['es', 'de', 'fr', 'it', 'pt', 'nl', 'pl', 'ru']
TIER2_LANGS = ['zh', 'vi', 'id', 'ms', 'tl', 'hi', 'bn', 'ur', 'ar']
ALL_LANGS = ['en'] + TIER1_LANGS + TIER2_LANGS  # 18 langs

# Built per-locale index.html files to also scan
BUILT_FILES = [
    (Path('public/index.html'), 'en'),
    (Path('public/es/index.html'), 'es'),
    (Path('public/de/index.html'), 'de'),
    (Path('public/fr/index.html'), 'fr'),
    (Path('public/it/index.html'), 'it'),
    (Path('public/pt/index.html'), 'pt'),
    (Path('public/nl/index.html'), 'nl'),
    (Path('public/pl/index.html'), 'pl'),
    (Path('public/ru/index.html'), 'ru'),
    (Path('public/zh/index.html'), 'zh'),
    (Path('public/vi/index.html'), 'vi'),
    (Path('public/id/index.html'), 'id'),
    (Path('public/ms/index.html'), 'ms'),
    (Path('public/tl/index.html'), 'tl'),
    (Path('public/hi/index.html'), 'hi'),
    (Path('public/bn/index.html'), 'bn'),
    (Path('public/ur/index.html'), 'ur'),
    (Path('public/ar/index.html'), 'ar'),
]


def get_blocks_for_file(path, file_type):
    """Return list of (lang, start, end) for each lang block in the file."""
    if not path.exists():
        return []
    src = path.read_text(encoding='utf-8')
    blocks = []
    if file_type == 'en':
        # Whole file is English
        blocks.append(('en', 0, len(src)))
    elif file_type in ('multi',):
        # Look for `lang: {` patterns; body is between { and the next `},\n  <next>:` or `},\n}`
        # Generic approach: scan for lines matching `  <lang>: {` and find the matching `}`
        for lang in ALL_LANGS:
            # Match "  lang: {" but not within strings
            m = re.search(rf'^\s*{re.escape(lang)}:\s*\{{', src, re.MULTILINE)
            if m:
                start = m.end()
                # Find matching close brace at column 2 (indent level of the lang key)
                # Walk forward and track brace depth
                depth = 1
                i = start
                while i < len(src) and depth > 0:
                    c = src[i]
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                    i += 1
                blocks.append((lang, start, i))
    elif file_type in ('tier1',):
        for lang in TIER1_LANGS:
            m = re.search(rf'^\s*{re.escape(lang)}:\s*\{{', src, re.MULTILINE)
            if m:
                start = m.end()
                depth = 1
                i = start
                while i < len(src) and depth > 0:
                    c = src[i]
                    if c == '{': depth += 1
                    elif c == '}': depth -= 1
                    i += 1
                blocks.append((lang, start, i))
    elif file_type in ('tier2',):
        for lang in TIER2_LANGS:
            m = re.search(rf'^\s*{re.escape(lang)}:\s*\{{', src, re.MULTILINE)
            if m:
                start = m.end()
                depth = 1
                i = start
                while i < len(src) and depth > 0:
                    c = src[i]
                    if c == '{': depth += 1
                    elif c == '}': depth -= 1
                    i += 1
                blocks.append((lang, start, i))
    return blocks

def find_suspicious(text, lang):
    """Find all suspicious characters in text, return list of (line, col, char, script)."""
    findings = []
    line = 1
    col = 0
    # Strip out the language switcher block — it intentionally shows every
    # language name in its own native script, which would otherwise be flagged
    # as cross-locale contamination on every page.
    scrubbed = re.sub(
        r'<details class="lang-switch".*?</details>',
        '',
        text,
        flags=re.DOTALL,
    )
    # Also strip hreflang blocks (they contain native lang names in <html lang="ar">)
    scrubbed = re.sub(
        r'<template data-page-hreflang="[^"]+">.*?</template>',
        '',
        scrubbed,
        flags=re.DOTALL,
    )
    # And the lang switcher mobile variant
    scrubbed = re.sub(
        r'<details class="lang-switch-mobile[^"]*".*?</details>',
        '',
        scrubbed,
        flags=re.DOTALL,
    )
    text = scrubbed

    for ch in text:
        col += 1
        if ch == '\n':
            line += 1
            col = 0
            continue
        cp = ord(ch)
        if cp in SHARED_INDIC_DANDA and lang in ('bn', 'hi', 'ur', 'ar'):
            continue  # U+0964/0965 danda is shared across Indic scripts
        script = char_script(cp)
        if script is None:
            continue
        allowed = ALLOWED_FOR_LANG[lang]
        if script in allowed:
            continue
        if script == 'latin_extended':
            continue
        findings.append((line, col, ch, script))
    return findings

def main():
    total_findings = 0
    print('Cross-locale contamination scan')
    print('=' * 100)
    print()

    # Scan source files (where each lang is in a dict block)
    for filepath, file_type in SOURCE_FILES:
        path = Path(filepath)
        if not path.exists():
            continue
        blocks = get_blocks_for_file(path, file_type)
        for lang, start, end in blocks:
            text = path.read_text(encoding='utf-8')[start:end]
            findings = find_suspicious(text, lang)
            if findings:
                # Group consecutive findings in same line
                by_line = {}
                for line, col, ch, script in findings:
                    by_line.setdefault(line, []).append((col, ch, script))
                print(f'✗ {filepath} [{lang}]: {len(findings)} stray characters found')
                for line, cols_chars in sorted(by_line.items()):
                    chars = ', '.join(f'"{ch}" ({script}, U+{ord(ch):04X})' for col, ch, script in cols_chars[:5])
                    print(f'    line {line}: {chars}')
                    if len(cols_chars) > 5:
                        print(f'    ... and {len(cols_chars) - 5} more on this line')
                total_findings += len(findings)
                print()

    # Also scan the built per-locale index.html files (whole file is one lang)
    for path, lang in BUILT_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        findings = find_suspicious(text, lang)
        if findings:
            by_line = {}
            for line, col, ch, script in findings:
                by_line.setdefault(line, []).append((col, ch, script))
            print(f'✗ {path} [{lang}]: {len(findings)} stray characters found')
            for line, cols_chars in sorted(by_line.items()):
                chars = ', '.join(f'"{ch}" ({script}, U+{ord(ch):04X})' for col, ch, script in cols_chars[:5])
                print(f'    line {line}: {chars}')
                if len(cols_chars) > 5:
                    print(f'    ... and {len(cols_chars) - 5} more on this line')
            total_findings += len(findings)
            print()

    if total_findings == 0:
        print('✓ No cross-locale contamination found in any source file')
    else:
        print(f'Total: {total_findings} stray characters across all source files')

if __name__ == '__main__':
    main()
