#!/usr/bin/env python3
"""Fase D: voegt hreflang fr en een FR-link in de taalwisselaar toe aan bestaande ES/EN/DE/NL-pagina's.
Alleen toevoegen; per bestand wordt gecontroleerd dat elk patroon precies één keer voorkomt.
Gebruik: add_fr_links.py [--apply]"""
import re, sys, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_fr import URL_MAP
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
BASE = "https://mediterranopilates.com"
apply = "--apply" in sys.argv
rep = {"changed": 0, "skipped_done": 0, "no_map": [], "problems": []}
files = [f for f in sorted(glob.glob(os.path.join(root, "site/**/*.html"), recursive=True))
         if "/site/fr/" not in f]
for f in files:
    rel = os.path.relpath(f, root)
    s = open(f, encoding="utf-8").read()
    m = re.search(r'<link rel="alternate" hreflang="es" href="([^"]+)">', s)
    if not m:
        continue
    path = m.group(1).replace(BASE, "")
    fr = URL_MAP.get(path)
    if not fr:
        rep["no_map"].append((rel, path)); continue
    if 'hreflang="fr"' in s:
        rep["skipped_done"] += 1; continue
    xd = re.findall(r'<link rel="alternate" hreflang="x-default" href="[^"]+">', s)
    if len(xd) != 1:
        rep["problems"].append((rel, f"x-default x{len(xd)}")); continue
    new = s.replace(xd[0], f'<link rel="alternate" hreflang="fr" href="{BASE}{fr}">\n' + xd[0], 1)
    nav = re.findall(r'<nav class="lang-switch"[^>]*>.*?</nav>', new, re.S)
    if len(nav) == 1:
        block = nav[0]
        lines = block.split("\n")
        links = [l for l in lines if "hreflang=" in l and l.strip().startswith("<a ")]
        if not links:
            rep["problems"].append((rel, "geen links in nav")); continue
        indent = re.match(r"\s*", links[-1]).group(0) if links[-1].startswith(" ") else "      "
        indent = "      "
        nb = block.replace("</nav>", "") .rstrip()
        nb = nb + f'\n{indent}<a href="{fr}" hreflang="fr">FR</a>\n    </nav>'
        new = new.replace(block, nb, 1)
    elif len(nav) > 1:
        rep["problems"].append((rel, f"nav x{len(nav)}")); continue
    rep["changed"] += 1
    if apply:
        open(f, "w", encoding="utf-8").write(new)
print({k: (v if not isinstance(v, list) else len(v)) for k, v in rep.items()})
for x in rep["no_map"][:20]: print("geen FR-tegenhanger:", x)
for x in rep["problems"][:20]: print("PROBLEEM:", x)
