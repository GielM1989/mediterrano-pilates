#!/usr/bin/env python3
"""Koppelt /it/ aan de rest van de site. Alleen toevoegingen, idempotent.
1. hreflang it op alle pagina's buiten /it/ waarvan de FR-tegenhanger een IT-versie heeft;
2. "IT" in elke taalwisselaar buiten /it/ (naar de IT-tegenhanger, anders /it/);
3. sitemap: it-alternates + IT-URL's (zonder fysio-noindex en legal);
4. llms.txt: Italiaanse sectie + entiteitsalinea + margeregel;
5. taalsuggestiebalk op de ES-home: Italiaans."""
import re, os, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
sys.path.insert(0, HERE)
from build_it import URL_MAP, BASE
NOINDEX = {"/it/prodotti-personalizzati-studi-fisioterapia/", "/it/legal.html"}
def it_for(fr_path):
    return URL_MAP.get(fr_path)
n_href = n_nav = 0
for f in sorted(glob.glob(os.path.join(ROOT, "site/**/*.html"), recursive=True)):
    if "/site/it/" in f: continue
    s = open(f, encoding="utf-8").read(); o = s
    m = re.search(r'<link rel="alternate" hreflang="fr" href="([^"]+)">', s)
    it = it_for(m.group(1).replace(BASE, "")) if m else None
    if it and 'hreflang="it"' not in s:
        s = s.replace(m.group(0), m.group(0) + f'\n<link rel="alternate" hreflang="it" href="{BASE}{it}">', 1); n_href += 1
    navs = re.findall(r'<nav class="lang-switch"[^>]*>.*?</nav>', s, re.S)
    if len(navs) == 1 and 'hreflang="it"' not in navs[0]:
        tgt = it or "/it/"
        nb = re.sub(r'\n(\s*)</nav>$', f'\n      <a href="{tgt}" hreflang="it">IT</a>\n\\1</nav>', navs[0])
        s = s.replace(navs[0], nb, 1); n_nav += 1
    if s != o: open(f, "w", encoding="utf-8").write(s)
print("hreflang it:", n_href, "taalwisselaars:", n_nav)
# sitemap
p = os.path.join(ROOT, "site/sitemap.xml"); s = open(p, encoding="utf-8").read()
if 'hreflang="it"' not in s:
    blocks = re.findall(r"  <url>.*?</url>\n", s, re.S); new = []
    for b in blocks:
        m = re.search(r'<xhtml:link rel="alternate" hreflang="fr" href="([^"]+)" />', b)
        if not m: continue
        frp = m.group(1).replace(BASE, ""); it = it_for(frp)
        if not it or it in NOINDEX: continue
        nb = b.replace(m.group(0), m.group(0) + f'\n    <xhtml:link rel="alternate" hreflang="it" href="{BASE}{it}" />', 1)
        s = s.replace(b, nb, 1)
        if re.search(r"<loc>([^<]+)</loc>", b).group(1) == BASE + frp:
            ib = re.sub(r"<loc>[^<]+</loc>", f"<loc>{BASE}{it}</loc>", nb, 1)
            ib = re.sub(r"<lastmod>[^<]+</lastmod>", "<lastmod>2026-11-16</lastmod>", ib, 1)
            new.append(ib)
    s = s.replace("</urlset>", "  <!-- Sezione italiana /it/ (16-11-2026) -->\n" + "".join(new) + "</urlset>", 1)
    open(p, "w", encoding="utf-8").write(s); print("sitemap IT-URL's:", len(new))
# llms.txt
p = os.path.join(ROOT, "site/llms.txt"); s = open(p, encoding="utf-8").read()
if "## Italiano" not in s:
    ent = ("Mediterrano Pilates è il partner degli studi di pilates e yoga per i loro prodotti personalizzati. Personalizziamo calze antiscivolo, "
           "tumbler termici e tote bag con il logo del tuo studio, perché tu li venda alle tue allieve. Calze antiscivolo da 50 paia, mockup gratuito "
           "in 24 ore, spedizione gratuita in tutta Europa (Italia compresa). Lavoriamo dalla Spagna con studi di tutta Europa e non solo. "
           "Marchio di Ecomtierra Group SL (Spagna).\n\n")
    anchor = "Los calcetines de Mediterrano Pilates son"
    assert s.count(anchor) == 1
    s = s.replace(anchor, ent + anchor, 1)
    socks = ("Le calze di Mediterrano Pilates sono calze antiscivolo tecniche per la lezione, con suola con grip in PVC o silicone, taglio a metà polpaccio, "
             "materiale verificato secondo REACH e logo intessuto (jacquard) o ricamato nella calza, mai stampato.\n\n")
    a2 = "## Key facts"
    s = s.replace(a2, socks + a2, 1)
    fr_line = re.search(r"  - France: [^\n]*\n", s).group(0)
    s = s.replace(fr_line, fr_line + "  - Italy: €19.95 incl. 22% IVA, margin €9.40 (57%). Prices in the Italian section are shown \"IVA esclusa\" and \"IVA inclusa\".\n", 1)
    titles = {}
    for name, (frf, it) in __import__("pages_it").PAGES.items():
        if it in NOINDEX: continue
        h = open(os.path.join(ROOT, "site", it.lstrip("/"), "index.html"), encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", h).group(1).replace(" · Mediterrano Pilates", "")
        titles[it] = ("Home (italiano)" if it == "/it/" else "Blog (italiano)" if it == "/it/blog/" else ("Blog: " + t if "/blog/" in it else t))
    sec = "\n## Italiano\n\n" + "".join(f"- [{t}]({BASE}{u})\n" for u, t in titles.items())
    m = re.search(r"## Français\n\n(?:- [^\n]*\n)+", s)
    s = s[:m.end()] + sec + s[m.end():]
    open(p, "w", encoding="utf-8").write(s); print("llms.txt: Italiano toegevoegd,", len(titles), "pagina's")
# taalsuggestie ES-home
p = os.path.join(ROOT, "site/index.html"); s = open(p, encoding="utf-8").read()
if "primary.indexOf('it')===0" not in s:
    old = "    } else if(primary.indexOf('de')===0){"
    assert s.count(old) == 1
    s = s.replace(old, "    } else if(primary.indexOf('it')===0){\n      target='/it/'; code='it';\n      msg='Sembra che tu preferisca l\\'italiano. Vuoi vedere questa pagina in italiano?';\n      btnLabel='Vedi in italiano';\n" + old, 1)
    open(p, "w", encoding="utf-8").write(s); print("taalbalk ES-home: it toegevoegd")
