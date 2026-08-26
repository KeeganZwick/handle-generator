#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate sitemap.xml listing every page in every language, with hreflang
xhtml:link annotations so Google understands the lang/page relationships.

Output: /workspace/nametok/public/sitemap.xml
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from per_page_seo import PAGES, url_for, LANG_ORDER

ALL_LANGS = ['en'] + LANG_ORDER  # 18 total

# Canonical base URL — change this to your live domain.
# Trailing slash for home, no trailing slash for other routes.
BASE_URL = 'https://gethandlenames.com'

# Output
SITEMAP_PATH = Path(__file__).parent.parent / 'public' / 'sitemap.xml'


def build_sitemap():
    """Build the sitemap.xml content."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    lines.append('')

    for page in PAGES:
        # For each (lang, page) combination, emit a <url> block with:
        # - <loc>: the canonical URL
        # - <xhtml:link rel="alternate" hreflang="X">: 18 alternates
        # - <xhtml:link rel="alternate" hreflang="x-default">: English default
        for lang in ALL_LANGS:
            path = url_for(lang, page)
            loc = BASE_URL + path
            lines.append('  <url>')
            lines.append(f'    <loc>{loc}</loc>')
            # Emit xhtml:link alternates in a stable order: en first, then 17 langs
            for hreflang_lang in ALL_LANGS:
                alt_path = url_for(hreflang_lang, page)
                alt_loc = BASE_URL + alt_path
                lines.append(
                    f'    <xhtml:link rel="alternate" '
                    f'hreflang="{hreflang_lang}" '
                    f'href="{alt_loc}"/>'
                )
            # x-default
            x_default_path = url_for('en', page)
            x_default_loc = BASE_URL + x_default_path
            lines.append(
                f'    <xhtml:link rel="alternate" '
                f'hreflang="x-default" '
                f'href="{x_default_loc}"/>'
            )
            lines.append('  </url>')

    lines.append('</urlset>')
    lines.append('')
    return '\n'.join(lines)


def build_robots_txt():
    """Build robots.txt pointing to the sitemap."""
    return f"""# robots.txt for Handle
User-agent: *
Allow: /

# Submit all language versions
Sitemap: {BASE_URL}/sitemap.xml
"""


def main():
    sitemap = build_sitemap()
    SITEMAP_PATH.write_text(sitemap, encoding='utf-8')
    print(f'Wrote {SITEMAP_PATH} ({len(sitemap)} bytes, '
          f'{len(PAGES) * len(ALL_LANGS)} URLs)')

    # Also write robots.txt
    robots_path = Path(__file__).parent.parent / 'public' / 'robots.txt'
    robots_path.write_text(build_robots_txt(), encoding='utf-8')
    print(f'Wrote {robots_path}')


if __name__ == '__main__':
    main()
