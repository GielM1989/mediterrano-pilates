#!/usr/bin/env python3
"""Fase D: fr toevoegen aan hreflang-alternates in site/sitemap.xml en de 20 indexeerbare FR-URL's toevoegen."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_fr import URL_MAP
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
BASE = "https://mediterranopilates.com"
p = os.path.join(root, "site/sitemap.xml")
s = open(p, encoding="utf-8").read()
if 'hreflang="fr"' in s: sys.exit("sitemap bevat al fr; niets gedaan")
blocks = re.findall(r"  <url>.*?</url>\n", s, re.S)
LASTMOD = "2026-10-19"
new_blocks, fr_blocks, out = [], [], s
for b in blocks:
    m = re.search(r'<xhtml:link rel="alternate" hreflang="es" href="([^"]+)" />', b)
    if not m: continue
    es_path = m.group(1).replace(BASE, "")
    fr = URL_MAP.get(es_path)
    if not fr or "legal" in fr: continue
    xd = re.findall(r'    <xhtml:link rel="alternate" hreflang="x-default"[^\n]*\n', b)
    assert len(xd) == 1, (es_path, "x-default")
    fr_line = f'    <xhtml:link rel="alternate" hreflang="fr" href="{BASE}{fr}" />\n'
    nb = b.replace(xd[0], fr_line + xd[0], 1)
    out = out.replace(b, nb, 1)
    # FR-blok: kopie van het ES-blok met fr-loc
    loc = re.search(r"<loc>([^<]+)</loc>", b).group(1)
    if loc == BASE + es_path:   # alleen het ES-blok zelf wordt gekopieerd
        fb = re.sub(r"<loc>[^<]+</loc>", f"<loc>{BASE}{fr}</loc>", nb, 1)
        fb = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{LASTMOD}</lastmod>", fb, 1)
        fr_blocks.append(fb)
out = out.replace("</urlset>", "\n" + "\n".join(fr_blocks).rstrip("\n") + "\n\n</urlset>", 1)
open(p, "w", encoding="utf-8").write(out)
print("alternates toegevoegd, FR-URL's:", len(fr_blocks))
