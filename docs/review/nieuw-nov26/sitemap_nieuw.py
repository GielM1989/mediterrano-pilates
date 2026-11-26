# -*- coding: utf-8 -*-
"""Voegt de 9 nieuwe URL's toe aan site/sitemap.xml (met hreflang es/fr/it + x-default es). Idempotent."""
import os
SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'site'))
B = 'https://mediterranopilates.com'
CL = [
 {'es': '/toalla-reformer-personalizada/', 'fr': '/fr/serviette-pilates-reformer-personnalisee/', 'it': '/it/telo-reformer-personalizzato/'},
 {'es': '/blog/abrir-un-estudio-de-pilates/', 'fr': '/fr/blog/ouvrir-un-studio-de-pilates/', 'it': '/it/blog/aprire-uno-studio-di-pilates/'},
 {'es': '/blog/que-vender-estudio-pilates/', 'fr': '/fr/blog/que-vendre-studio-pilates/', 'it': '/it/blog/cosa-vendere-studio-pilates/'},
]
p = os.path.join(SITE, 'sitemap.xml'); t = open(p, encoding='utf-8').read(); add = ''
for c in CL:
    for lg in ('es', 'fr', 'it'):
        if f'<loc>{B}{c[lg]}</loc>' in t:
            continue
        alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{B}{c[l]}" />' for l in ('es', 'fr', 'it'))
        alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{B}{c["es"]}" />'
        add += f'  <url>\n    <loc>{B}{c[lg]}</loc>\n    <lastmod>2026-11-26</lastmod>{alts}\n  </url>\n'
t = t.replace('</urlset>', add + '</urlset>')
open(p, 'w', encoding='utf-8').write(t); print(t.count('<url>'))
