#!/usr/bin/env python3
"""Haalt alle vertaalbare segmenten uit de Franse pagina's (bron voor /it/).
Schrijft docs/review/it/segs/<naam>.txt (per pagina, alleen paginaspecifieke segmenten)
en segs/_common.txt (segmenten die op 3+ pagina's voorkomen). JSON-LD-strings die niet
als zichtbaar segment bestaan, komen erbij met prefix LD."""
import sys, os, re, json, glob, html, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "docs/review/fr"))
import build_fr as B
from pages_it import PAGES
OUT = os.path.join(ROOT, "docs/review/it/segs"); os.makedirs(OUT, exist_ok=True)
SKIP = B.SKIP_EXACT | {"IT", "Mediterrano Pilates · Made for Pilates & Yoga culture."}
def ld_strings(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("@type", "@context", "@id", "url", "image", "logo", "sameAs", "item", "inLanguage", "priceCurrency",
                     "price", "unitCode", "availability", "businessFunction", "datePublished", "dateModified", "email",
                     "telephone", "knowsLanguage", "addressCountry", "contentUrl", "mainEntityOfPage", "legalName", "taxID",
                     "vatID", "foundingDate", "minValue", "maxValue", "value", "position", "totalTime", "isoCode"):
                continue
            ld_strings(v, acc)
    elif isinstance(o, list):
        for v in o: ld_strings(v, acc)
    elif isinstance(o, str):
        if not o.startswith("http") and re.search(r"[A-Za-zÀ-ÿ]{3,}", o):
            acc.append(o)
per, freq = {}, collections.Counter()
for name, (fr, it) in PAGES.items():
    s = open(os.path.join(ROOT, "site", fr.lstrip("/"))).read()
    segs = B.extract(s)
    vis = []
    for k, a, b, t in segs:
        tt = t.strip()
        if tt.startswith("{") or tt in SKIP: continue
        vis.append(B.norm(tt))
    ld = []
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', s):
        o = json.loads(m.group(1))
        if o.get("@type") == "FAQPage": continue   # wordt opnieuw opgebouwd uit de zichtbare FAQ
        ld_strings(o, ld)
    visset = set(vis)
    ld = [B.norm(x) for x in ld if B.norm(x) not in visset]
    uniq = list(dict.fromkeys(vis + ["LD " + x for x in ld]))
    per[name] = uniq
    for u in set(uniq): freq[u] += 1
common = [u for u, n in freq.items() if n >= 3]
cs = set(common)
open(os.path.join(OUT, "_common.txt"), "w").write("\n".join(common) + "\n")
tot = 0
for name, uniq in per.items():
    own = [u for u in uniq if u not in cs]
    tot += sum(len(u) for u in own)
    open(os.path.join(OUT, name + ".txt"), "w").write("\n".join(own) + "\n")
    print(name, len(own), sum(len(u) for u in own))
print("common", len(common), sum(len(u) for u in common), "own total", tot)
