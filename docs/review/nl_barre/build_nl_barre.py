#!/usr/bin/env python3
"""Bouwt /nl/merchandise-voor-barrestudios/ op basis van de Nederlandse yogapagina (kop, navigatie,
mockupformulier, footer, scripts) en body_nl.html (hero t/m FAQ, vertaald en aangepast van de Franse
barrepagina). FAQPage-JSON-LD wordt uit de zichtbare FAQ gegenereerd, zodat beide altijd gelijk zijn.
Werkt ook hreflang (ES/FR/NL), taalwisselaars, sitemap en llms.txt bij. Idempotent.
Gebruik: python3 docs/review/nl_barre/build_nl_barre.py  (vanuit de repo-root)"""
import html, json, os, re

BASE = "https://mediterranopilates.com"
SLUG = "/nl/merchandise-voor-barrestudios/"
ES, FR = "/merchandising-estudios-barre/", "/fr/produits-personnalises-studios-barre/"
SRC = "site/nl/merchandise-voor-yogastudios/index.html"
OUT = "site" + SLUG + "index.html"
BODY = os.path.join(os.path.dirname(__file__), "body_nl.html")

TITLE = "Merchandise voor barrestudio's | Mediterrano Pilates"
DESC = ("Antislipsokken met het logo van je barrestudio, geweven of geborduurd, om aan je leden te verkopen. "
        "Vanaf 50 paar, gratis mockup binnen 24 uur.")
OG_TITLE = "Merchandise voor barrestudio's · Mediterrano Pilates"
IMG = BASE + "/images/product-sokken.jpg"
IMG_ALT = "Terracotta antislipsokken met het logo van een barrestudio"


def plain(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t)).replace(" ", " ").strip()


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def build():
    s = open(SRC, encoding="utf-8").read()
    body = open(BODY, encoding="utf-8").read()
    esc = lambda t: html.escape(t, quote=True).replace("&#x27;", "&#x27;")

    # --- kop: title, description, og, canonical, hreflang
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(TITLE, quote=False)}</title>", s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*(">)', lambda m: m.group(1) + esc(DESC) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(">)', lambda m: m.group(1) + esc(DESC) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(">)', lambda m: m.group(1) + esc(OG_TITLE) + m.group(2), s, count=1)
    s = s.replace(BASE + "/nl/merchandise-voor-yogastudios/", BASE + SLUG)
    s = s.replace(BASE + "/images/product-tote.jpg", IMG)
    s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(">)', lambda m: m.group(1) + esc(IMG_ALT) + m.group(2), s, count=1)
    hre = (f'<link rel="alternate" hreflang="es" href="{BASE}{ES}">\n'
           f'<link rel="alternate" hreflang="nl" href="{BASE}{SLUG}">\n'
           f'<link rel="alternate" hreflang="fr" href="{BASE}{FR}">\n'
           f'<link rel="alternate" hreflang="x-default" href="{BASE}{ES}">\n')
    s = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n)+', hre, s, count=1)

    # --- body: hero t/m FAQ vervangen
    a = s.index('<header class="hero" id="top">')
    b = s.index('<section class="sheet green" id="mockup-form">')
    s = s[:a] + body + s[b:]

    # --- JSON-LD: Breadcrumb, Service, FAQPage
    faqs = [(plain(q), plain(ans)) for q, ans in re.findall(
        r'<summary><span class="qn">\d+</span>(.*?)</summary>\s*<p>(.*?)</p>', body, re.S)]
    crumbs = ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Mediterrano Pilates", "item": BASE + "/nl/"},
        {"@type": "ListItem", "position": 2, "name": "Merchandise voor barrestudio's", "item": BASE + SLUG}]})
    service = ld({"@context": "https://schema.org", "@type": "Service", "@id": BASE + SLUG + "#service",
        "name": "Antislipsokken met logo voor barrestudio's",
        "serviceType": "Merchandise met logo voor barrestudio's",
        "description": ("Mediterrano Pilates personaliseert antislipsokken, tumblers, tote bags en pilatesringen met het "
                        "logo van barrestudio's, om aan hun leden te verkopen. Logo op de sokken "
                        "geweven of geborduurd, kleur afgestemd op Pantone, minimale bestelling 50 paar, gratis mockup "
                        "binnen 24 uur en gratis verzending binnen heel Europa."),
        "url": BASE + SLUG, "image": IMG, "provider": {"@id": BASE + "/#organization"},
        "brand": {"@type": "Brand", "name": "Mediterrano Pilates"},
        "audience": {"@type": "BusinessAudience", "name": "Barrestudio's, barre fitness en studio's die barre met pilates combineren"},
        "areaServed": {"@type": "GeoShape", "name": "Worldwide"},
        "offers": {"@type": "Offer", "url": BASE + SLUG, "priceCurrency": "EUR", "price": "6.95",
                   "eligibleQuantity": {"@type": "QuantitativeValue", "minValue": 50, "unitCode": "PR"},
                   "availability": "https://schema.org/InStock", "businessFunction": "https://schema.org/Sell",
                   "description": "Indicatieve inkoopprijs per paar antislipsokken met logo, exclusief btw. Minimale bestelling 50 paar. Tote bags, tumblers en pilatesringen op offerte."}})
    faqld = ld({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in faqs]})
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
    assert len(blocks) == 3, len(blocks)
    s = s[:blocks[0].start()] + crumbs + "\n" + service + "\n" + faqld + s[blocks[-1].end():]

    # --- taalwisselaar
    sw = (f'      <a href="{ES}" hreflang="es">ES</a>\n'
          f'      <a href="/en/" hreflang="en">EN</a>\n'
          f'      <a href="/de/" hreflang="de">DE</a>\n'
          f'      <a href="{SLUG}" class="on" hreflang="nl" aria-current="true">NL</a>\n'
          f'      <a href="{FR}" hreflang="fr">FR</a>\n')
    s = re.sub(r'(<nav class="lang-switch" aria-label="Taal">\n)(.*?)(    </nav>)', lambda m: m.group(1) + sw + m.group(3), s, count=1, flags=re.S)

    # --- formulier en tracking
    s = s.replace('value="/nl/merchandise-voor-yogastudios/"', f'value="{SLUG}"')
    s = s.replace('placeholder="Yogastudio De Linde"', 'placeholder="Barrestudio De Linde"')
    s = s.replace("merchandise voor mijn yogastudio.", "merchandise voor mijn barrestudio.")
    s = s.replace("yogastudios-nl", "barrestudios-nl").replace("'MP-YOGA-'", "'MP-BARRE-'")
    fys = '<a href="/nl/merchandise-voor-fysiotherapiepraktijken/" style="color:var(--cream);text-decoration:underline">Voor fysiotherapiepraktijken</a>'
    yog = ' · <a href="/nl/merchandise-voor-yogastudios/" style="color:var(--cream);text-decoration:underline">Voor yogastudio\'s</a>'
    if yog not in s:
        s = s.replace(fys, fys + yog, 1)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(s)
    print("geschreven:", OUT, "FAQ:", len(faqs))


def link_alternates():
    """hreflang NL toevoegen aan de ES- en FR-barrepagina en hun taalwisselaar."""
    for f, lang in (("site" + ES + "index.html", "es"), ("site" + FR + "index.html", "fr")):
        s = open(f, encoding="utf-8").read()
        tag = f'<link rel="alternate" hreflang="nl" href="{BASE}{SLUG}">\n'
        if tag not in s:
            s = s.replace(f'<link rel="alternate" hreflang="x-default"', tag + '<link rel="alternate" hreflang="x-default"', 1)
        # taalwisselaar: NL-link naar de barrepagina
        s = re.sub(r'<a href="/nl/[^"]*" hreflang="nl">NL</a>', f'<a href="{SLUG}" hreflang="nl">NL</a>', s)
        if f'href="{SLUG}" hreflang="nl">NL<' not in s:
            # ES-pagina heeft geen NL-link: invoegen voor FR
            s = s.replace(f'<a href="{FR}" hreflang="fr">FR</a>', f'<a href="{SLUG}" hreflang="nl">NL</a>\n      <a href="{FR}" hreflang="fr">FR</a>', 1)
        open(f, "w", encoding="utf-8").write(s)


def sitemap():
    f = "site/sitemap.xml"
    s = open(f, encoding="utf-8").read()
    alt = f'    <xhtml:link rel="alternate" hreflang="nl" href="{BASE}{SLUG}" />\n'
    fr_alt = f'    <xhtml:link rel="alternate" hreflang="fr" href="{BASE}{FR}" />\n'
    # alternates op ES- en FR-barre-url
    def add_alt(block):
        return block if alt in block else block.replace(fr_alt, alt + fr_alt)
    s = re.sub(r"  <url>\n    <loc>" + re.escape(BASE + ES) + r"</loc>.*?</url>", lambda m: add_alt(m.group(0)), s, count=1, flags=re.S)
    s = re.sub(r"  <url>\n    <loc>" + re.escape(BASE + FR) + r"</loc>.*?</url>", lambda m: add_alt(m.group(0)), s, count=1, flags=re.S)
    if f"<loc>{BASE}{SLUG}</loc>" not in s:
        entry = ("  <!-- Nichepagina: barrestudio's (NL) -->\n  <url>\n"
                 f"    <loc>{BASE}{SLUG}</loc>\n    <lastmod>2026-11-04</lastmod>\n"
                 f'    <xhtml:link rel="alternate" hreflang="es" href="{BASE}{ES}" />\n' + alt + fr_alt +
                 f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{ES}" />\n'
                 "    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n")
        s = s.replace("</urlset>", entry + "</urlset>")
    open(f, "w", encoding="utf-8").write(s)


def llms():
    f = "site/llms.txt"
    s = open(f, encoding="utf-8").read()
    line = f"- [Merchandise voor barrestudio's]({BASE}{SLUG})"
    if line in s:
        return
    m = re.search(r"- \[[^\]]*\]\(" + re.escape(BASE) + r"/nl/merchandise-voor-yogastudios/\)[^\n]*\n", s)
    if m:
        s = s[:m.end()] + line + ": antislipsokken met logo voor barrestudio's, vanaf 50 paar.\n" + s[m.end():]
    else:
        print("llms.txt: NL-yogaregel niet gevonden, handmatig toevoegen")
    open(f, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    build(); link_alternates(); sitemap(); llms()
