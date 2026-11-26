# -*- coding: utf-8 -*-
"""Zet de twee nieuwe artikelen bovenaan het blogoverzicht (ES/FR/IT), kaart + BlogPosting. Idempotent."""
import os, sys, json, html, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SITE = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'site'))
IDX = {'it': 'it/blog/index.html', 'fr': 'fr/blog/index.html', 'es': 'blog/index.html'}
MORE = {'it': "Leggi l'articolo →", 'fr': "Lire l'article →", 'es': 'Leer el artículo →'}
for lg, f in IDX.items():
    T = importlib.import_module('teksten_' + lg)
    p = os.path.join(SITE, f); t = open(p, encoding='utf-8').read()
    if lg == 'it':
        t = t.replace('"inLanguage": "fr"', '"inLanguage": "it"')  # bestaande fout in het IT-overzicht
    cards = ''; posts = ''
    for d in (T.a1, T.a2):
        if d['slug'] in t:
            continue
        kort = d['kort'].split('. ')[0] + '.'
        cards += f'''      <article style="border:1px solid rgba(46,64,52,.14);border-radius:16px;padding:28px 30px">
        <h2 style="margin:0 0 10px"><a href="{d['slug']}" style="color:inherit;text-decoration:none">{html.escape(d['h1a'] + ' ' + d['h1b'], quote=False)}</a></h2>
        <p style="max-width:none;color:#4c554d;margin-bottom:14px">{html.escape(d['intro'], quote=False)}</p>
        <a href="{d['slug']}" style="color:#AC512C;font-weight:700;text-decoration:underline">{MORE[lg]}</a>
      </article>
'''
        posts += '    ' + json.dumps({'@type': 'BlogPosting', 'headline': d['title'], 'url': 'https://mediterranopilates.com' + d['slug'],
                                     'datePublished': '2026-11-26', 'dateModified': '2026-11-26', 'inLanguage': lg}, ensure_ascii=False) + ',\n'
    if cards:
        a = '<div style="display:grid;gap:28px">\n'
        assert t.count(a) == 1
        t = t.replace(a, a + cards, 1)
        b = '"blogPost": [\n'
        assert t.count(b) == 1
        t = t.replace(b, b + posts, 1)
    open(p, 'w', encoding='utf-8').write(t); print(f, bool(cards))
