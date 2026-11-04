"""Kerst sitebreed weg (klantbesluit 04-11-2026: 'kerst red ik niet meer, haal het overal weg').
Kerstblogs naar docs/archive/kerst-2026/ (terug te zetten volgend seizoen) + 301 naar het welkomstpakket-artikel."""
import glob, json, os, re, shutil, html as H
B = "https://mediterranopilates.com"
XMAS = {  # kerstblog -> welkomstpakket (zelfde taal)
 "/blog/regalos-de-navidad-alumnas-pilates/": "/blog/pack-de-bienvenida-alumnas-nuevas-pilates/",
 "/en/blog/christmas-gifts-for-pilates-clients/": "/en/blog/welcome-pack-for-new-pilates-clients/",
 "/de/blog/weihnachtsgeschenke-fuer-pilates-kundinnen/": "/de/blog/willkommenspaket-fuer-neue-kundinnen/",
 "/nl/blog/kerstcadeaus-voor-pilatesleden/": "/nl/blog/welkomstpakket-nieuwe-pilatesleden/",
 "/fr/blog/cadeaux-de-noel-eleves-pilates/": "/fr/blog/kit-de-bienvenue-nouveaux-eleves-pilates/",
}
# 1. archiveren en verwijderen
for u in XMAS:
    src = "site" + u
    if os.path.isdir(src):
        dst = "docs/archive/kerst-2026" + u
        os.makedirs(os.path.dirname(dst.rstrip("/")), exist_ok=True)
        if os.path.exists(dst): shutil.rmtree(dst)
        shutil.copytree(src, dst); shutil.rmtree(src); print("gearchiveerd", u)
# 2. redirects
t = open("netlify.toml", encoding="utf-8").read()
for u, to in XMAS.items():
    if f'from = "{u}"' not in t:
        t += f'\n[[redirects]]\n  from = "{u}"\n  to = "{to}"\n  status = 301\n  force = true\n'
        t += f'\n[[redirects]]\n  from = "{u.rstrip("/")}"\n  to = "{to}"\n  status = 301\n  force = true\n'
open("netlify.toml", "w", encoding="utf-8").write(t)

def renumber_and_drop_faq(s, qpat):
    """Verwijder FAQ-vraag (zichtbaar + JSON-LD) waarvan de vraag qpat matcht; hernummer."""
    m = re.search(r'\s*<details>\s*<summary><span class="qn">\d+</span>(?:(?!</summary>).)*' + qpat + r'(?:(?!</details>).)*</details>', s, re.S | re.I)
    if not m: return s, False
    s = s[:m.start()] + s[m.end():]
    # JSON-LD: compacte regel of pretty
    for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        if '"FAQPage"' not in mm.group(1): continue
        data = json.loads(mm.group(1))
        ents = data["mainEntity"]
        keep = [e for e in ents if not re.search(qpat, e["name"], re.I)]
        if len(keep) == len(ents): break
        body = mm.group(1)
        if '\n    {"@type":"Question"' in body:  # compact formaat: regel weghalen
            lines = body.split("\n")
            lines = [l for l in lines if not (l.strip().startswith('{"@type":"Question"') and re.search(qpat, json.loads(l.strip().rstrip(","))["name"], re.I))]
            body = "\n".join(lines)
            body = re.sub(r",(\s*\])", r"\1", body)
        else:
            data["mainEntity"] = keep
            body = "\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        s = s[:mm.start(1)] + body + s[mm.end(1):]
        break
    n = [0]
    def num(x):
        n[0] += 1; return f'<span class="qn">{n[0]:02d}</span>'
    s = re.sub(r'<span class="qn">\d+</span>', num, s)
    return s, True

SENT = [
 (" Los mismos productos sirven también como regalo de bienvenida o de Navidad; tienes ideas", " Los mismos productos sirven también como regalo de bienvenida; tienes ideas"),
 (" The same products also work as a welcome gift or at Christmas; there are ideas", " The same products also work as a welcome gift; there are ideas"),
 (" Dieselben Produkte eignen sich auch als Willkommensgeschenk oder zu Weihnachten; Ideen", " Dieselben Produkte eignen sich auch als Willkommensgeschenk; Ideen"),
 (" Les mêmes produits servent aussi de cadeau de bienvenue ou de Noël&nbsp;; vous trouverez", " Les mêmes produits servent aussi de cadeau de bienvenue&nbsp;; vous trouverez"),
 (" Dezelfde producten werken ook als welkomstcadeau of met kerst; ideeën", " Dezelfde producten werken ook als welkomstcadeau; ideeën"),
]
XQ = r"(Navidad|Christmas|Weihnacht|Noël|kerst)"
for f in glob.glob("site/**/*.html", recursive=True):
    s = open(f, encoding="utf-8").read(); o = s
    for u in XMAS:
        ua = re.escape(u)
        s = re.sub(r'\s*·\s*<a href="' + ua + r'"[^>]*>[^<]*</a>', "", s)
        s = re.sub(r'<a href="' + ua + r'"[^>]*>[^<]*</a>\s*·\s*', "", s)
        # blogindex-kaart
        s = re.sub(r'\s*<article[^>]*>\s*<h2[^>]*><a href="' + ua + r'".*?</article>', "", s, flags=re.S)
        # blogindex JSON-LD BlogPosting
        s = re.sub(r',?\s*\{\s*"@type": "BlogPosting",\s*"headline": "[^"]*",\s*"url": "' + re.escape(B + u) + r'"[^}]*\}', "", s)
        s = re.sub(r'(\[)\s*,', r'\1', s)
    # ticker-items en urgentieregels
    s = re.sub(r'\s*<span><span class="pulse"></span><b>(Kerst|Navidad|Christmas|Weihnachten|Noël)[^<]*</b>.*?</span><span class="tk-sep">·</span>', "", s)
    s = re.sub(r'\s*<p class="hook-urgency">(?:(?!</p>).)*(Navidad|Christmas|Weihnacht|Noël|kerst)(?:(?!</p>).)*</p>', "", s, flags=re.I)
    for a, b in SENT: s = s.replace(a, b)
    # kerst-FAQ
    while True:
        s, done = renumber_and_drop_faq(s, XQ)
        if not done: break
    if s != o: open(f, "w", encoding="utf-8").write(s); print("bijgewerkt", f)
# sitemap
sm = open("site/sitemap.xml", encoding="utf-8").read()
for u in XMAS:
    sm = re.sub(r"\s*(<!--[^>]*-->\s*)?<url>\s*<loc>" + re.escape(B + u) + r"</loc>.*?</url>", "", sm, flags=re.S)
    sm = re.sub(r'\s*<xhtml:link rel="alternate" hreflang="[^"]+" href="' + re.escape(B + u) + r'" />', "", sm)
open("site/sitemap.xml", "w", encoding="utf-8").write(sm)
ll = open("site/llms.txt", encoding="utf-8").read()
ll = "\n".join(l for l in ll.split("\n") if not any(B + u in l for u in XMAS))
open("site/llms.txt", "w", encoding="utf-8").write(ll)
