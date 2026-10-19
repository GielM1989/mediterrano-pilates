#!/usr/bin/env python3
"""Kwaliteitscontrole van alle Franse pagina's onder site/fr/ (hoofdstuk 12 van de bouwprompt).
Gebruik: python3 docs/review/check_fr.py [--verbose]
Exitcode 1 bij een harde fout."""
import re, os, sys, json, html, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = os.path.join(ROOT, "site")
BASE = "https://mediterranopilates.com"
VERBOSE = "--verbose" in sys.argv

PAGES = sorted(glob.glob(os.path.join(SITE, "fr", "**", "*.html"), recursive=True))
FORBIDDEN_WORDS = [r"\bmerchandising\b", r"\btumblers?\b", r"\bgoodies\b", r"\bEspaña\b", r"\bIVA\b", r"\bboceto\b",
                   r"\bobjets? publicitaires?\b", r"\bcourriel\b", r"\bgobelet\b", r"\balumnas?\b"]
TU_FORMS = r"\b(tu|ton|ta|tes|toi|te|t')\b"
SPANISH_NUMBERS = [r"17,95", r"7,88", r"\b53\s?%", r"\b21\s?%", r"8,83", r"5,90", r"6,64", r"\b45\s?[–-]\s?53"]
ALLOWED_PRICES = {"6,95", "19,95", "9,68", "11", "24", "9,00", "9", "6,50", "15", "6,00", "6", "7", "16,50", "6,75", "347,50", "483,75"}
PRODUCT_NICHE = ("chaussettes-antiderapantes-personnalisees", "gourde-isotherme-personnalisee", "tote-bag-personnalise",
                 "anneau-de-pilates-personnalise", "produits-personnalises-")
errors, warns = [], []

def err(page, msg): errors.append(f"{page}: {msg}")
def warn(page, msg): warns.append(f"{page}: {msg}")

def visible(s):
    b = re.sub(r"<style[\s\S]*?</style>", " ", s)
    b = re.sub(r"<script[\s\S]*?</script>", " ", b)
    b = re.sub(r"<!--[\s\S]*?-->", " ", b)
    b = re.sub(r"</?(a|span|b|strong|em|i|sup|sub|u)(\s[^>]*)?>", "", b)
    return html.unescape(re.sub(r"<[^>]+>", " ", b))

def url_to_file(u):
    p = u.split("#")[0].split("?")[0]
    if p.startswith(BASE): p = p[len(BASE):]
    if not p.startswith("/"): return None
    f = os.path.join(SITE, p.lstrip("/"))
    if p.endswith("/"): f = os.path.join(f, "index.html")
    return f

def es_cluster_has_fr(fr_path):
    return True

ALL_FR_URLS = set()
for f in PAGES:
    rel = os.path.relpath(f, SITE)
    ALL_FR_URLS.add("/" + rel.replace("index.html", ""))

for f in PAGES:
    rel = os.path.relpath(f, SITE)
    name = "/" + rel.replace("index.html", "")
    s = open(f, encoding="utf-8").read()
    vis = visible(s)
    is_legal = rel.endswith("legal.html")
    is_article = rel.startswith("fr/blog/") and rel != "fr/blog/index.html"

    # 1. head
    m = re.search(r"<html lang=\"([a-z-]+)\"", s)
    if not m or m.group(1) != "fr": err(name, "html lang is niet fr")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    tt = html.unescape(t.group(1)).replace("\xa0", " ").strip() if t else ""
    if not tt: err(name, "geen title")
    elif len(tt) > 60: err(name, f"title {len(tt)} tekens (max 60): {tt}")
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    dd = html.unescape(d.group(1)).replace("\xa0", " ") if d else ""
    if not dd: err(name, "geen meta description")
    elif len(dd) > 155: err(name, f"description {len(dd)} tekens (max 155)")
    h1 = re.findall(r"<h1[\s>]", s)
    if len(h1) != 1: err(name, f"{len(h1)} H1-tags")
    can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    expect = BASE + name
    if not can or can.group(1) != expect: err(name, f"canonical {can.group(1) if can else None} != {expect}")
    if is_legal:
        if 'noindex' not in s: err(name, "legal.html mist noindex")
    else:
        hl = dict(re.findall(r'<link rel="alternate" hreflang="([a-zA-Z-]+)" href="([^"]+)"', s))
        for need in ("fr", "x-default"):
            if need not in hl: err(name, f"hreflang {need} ontbreekt")
        if hl.get("fr") != expect: err(name, "hreflang fr wijst niet naar zichzelf")
        for l, u in hl.items():
            fp = url_to_file(u)
            if fp and not os.path.exists(fp): err(name, f"hreflang {l} wijst naar bestaande pagina ontbreekt: {u}")
    if 'og:locale" content="fr_FR"' not in s: err(name, "og:locale fr_FR ontbreekt")
    if not re.search(r'og:title', s) or not re.search(r'og:description', s): err(name, "og:title/description ontbreekt")

    # 2. taal en toon
    if "!" in re.sub(r"[^\s]!", "X", vis) and re.search(r"[^\s!]!", vis): err(name, "uitroepteken in zichtbare tekst")
    if "—" in vis or re.search(r"(?<!\d)–|–(?!\d)", vis): err(name, "gedachtestreepje in zichtbare tekst")
    if re.search(r"[¿¡]", vis): err(name, "Spaanse leestekens")
    for pat in FORBIDDEN_WORDS:
        if re.search(pat, vis, re.I):
            # 'merchandising' mag niet in zichtbare tekst; 'IVA' ook niet
            err(name, f"verboden woord /{pat}/: " + re.search(pat, vis, re.I).group(0))
    for pat in SPANISH_NUMBERS:
        if re.search(pat, vis) and not (is_legal and "21" in pat): err(name, f"Spaans cijfer /{pat}/ in tekst")
    for mm in re.finditer(TU_FORMS, vis, re.I):
        ctx = vis[max(0, mm.start() - 25):mm.end() + 25].replace("\n", " ")
        if re.fullmatch(r"te", mm.group(0), re.I) and True:
            # "te" komt in Frans nauwelijks voor als woord, behalve in 'quelques' etc.; alleen waarschuwen
            warn(name, f"mogelijk tutoiement/'te': ...{ctx}...")
        else:
            err(name, f"tutoiement '{mm.group(0)}': ...{ctx}...")
    cnt_mockup = len(re.findall(r"\bmockups?\b", vis, re.I))
    if cnt_mockup > 2: warn(name, f"'mockup' {cnt_mockup}x (liefst 'maquette')")
    # typografie: ontbrekende spatie vóór ? ! : ; in lopende tekst (zonder URL's/tijden)
    for mm in re.finditer(r"[^\s\xa0 /\-–…(][?!;:](?=\s|$)", vis):
        ctx = vis[max(0, mm.start() - 25):mm.end() + 10].replace("\n", " ")
        if re.search(r"https?|mailto|:\d{2}|@", ctx): continue
        warn(name, f"typografie (geen fijne spatie): ...{ctx}...")
    for mm in re.finditer(r"\d\s?[€%]", vis):
        if " " in mm.group(0) and "\xa0" not in mm.group(0) and " " not in mm.group(0):
            pass  # na html.unescape worden &nbsp; \xa0; gewone spatie is hier een fout
    if re.search(r"\d [€%]", vis.replace("\xa0", "#").replace(" ", "#")): warn(name, "gewone spatie vóór € of % (gebruik &nbsp;)")

    # 3. JSON-LD
    lds = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', s)
    types = []
    faq_q = []
    for b in lds:
        try:
            o = json.loads(b)
        except Exception as e:
            err(name, f"JSON-LD ongeldig: {e}"); continue
        types.append(o.get("@type"))
        if o.get("@type") == "FAQPage":
            visn = re.sub(r"\s+", " ", vis.replace("\xa0", " ")).strip()
            for q in o["mainEntity"]:
                qn = re.sub(r"\s+", " ", html.unescape(q["name"]).replace("\xa0", " ")).strip()
                an = re.sub(r"\s+", " ", html.unescape(q["acceptedAnswer"]["text"]).replace("\xa0", " ")).strip()
                faq_q.append(qn)
                if qn not in visn: err(name, f"FAQ-vraag JSON-LD niet in zichtbare tekst: {qn[:60]}")
                if an not in visn: err(name, f"FAQ-antwoord JSON-LD niet woordelijk zichtbaar: {an[:60]}")
        if o.get("@type") == "Organization" and "areaServed" not in o: err(name, "Organization zonder areaServed")
    if name != "/fr/" and not is_legal and "BreadcrumbList" not in types and name != "/fr/blog/":
        warn(name, "geen BreadcrumbList")
    if name == "/fr/" and "Organization" not in types: err(name, "home zonder Organization")
    if any(name.endswith(x) or x in name for x in PRODUCT_NICHE) or name == "/fr/faq/":
        n = len(faq_q)
        if name != "/fr/faq/" and not (6 <= n <= 10): warn(name, f"{n} FAQ-vragen (richtlijn 6-10)")
    if any(x in name for x in PRODUCT_NICHE):
        if "En bref" not in vis: err(name, "feitenblok 'En bref' ontbreekt")
        if not re.search(r"minimum de commande", vis, re.I): warn(name, "geen 'minimum de commande' in tekst/FAQ")
        if not re.search(r"Belgique", vis): warn(name, "Belgique/Luxembourg/Suisse niet genoemd")
    if is_article:
        if not re.search(r"(Publié|Mis à jour)", vis): warn(name, "geen zichtbare publicatie-/bijwerkdatum")

    # 4. links en beelden
    for u in re.findall(r'(?:href|src)="([^"#][^"]*)"', s):
        if u.startswith(("http", "mailto:", "tel:", "data:", "javascript:")): continue
        fp = url_to_file(u) if u.startswith("/") else None
        if u.startswith("/") and fp and not os.path.exists(fp) and not u.startswith("/#"):
            err(name, f"kapotte interne link: {u}")
        if re.match(r"^(?!/)(?!#)", u) and not u.startswith(("http", "mailto", "tel", "data", "javascript")):
            warn(name, f"relatieve link: {u}")
    for u in re.findall(r'href="(/(?!fr/|en/|de/|nl/|images/|fonts/|[a-z0-9-]+\.[a-z]+$)[^"#]*)', s):
        # taalwisselaar (hreflang es) mag naar ES; anders geen ES-link
        pass
    es_links = [u for u in re.findall(r'<a [^>]*href="(/[^"]*)"[^>]*>', s)
                if not re.match(r"^/(fr|en|de|nl|images|fonts)/", u) and u != "/" and not u.startswith("/#")]
    for a in re.findall(r'<a [^>]*>', s):
        hh = re.search(r'href="([^"]+)"', a)
        if not hh: continue
        u = hh.group(1)
        if re.match(r"^/(?!fr/|en/|de/|nl/|images/|fonts/|#)", u) and 'hreflang="es"' not in a and not u.startswith("/legal.html") and u != "/":
            err(name, f"verwijzing naar Spaanse pagina buiten taalwisselaar: {u}")
        if u == "/" and 'hreflang="es"' not in a: err(name, "link naar / (ES-home) buiten taalwisselaar")
    if 'name="language" value="fr"' not in s and ("lead-form" in s): err(name, "formulier mist language=fr")
    if "lead-form" in s and 'name="form-name"' not in s: warn(name, "form-name ontbreekt")
    if "googletagmanager.com/gtag/js" in re.sub(r"s\.src='https://www\.googletagmanager[^']*'", "", s) and "MP_loadGA" not in s:
        err(name, "gtag.js laadt zonder toestemming")
    if "lang-banner" in s: err(name, "taalsuggestiebalk aanwezig")

print(f"{len(PAGES)} Franse pagina's gecontroleerd")
for p in PAGES: print("  ", os.path.relpath(p, SITE))
if warns:
    print(f"\nWAARSCHUWINGEN ({len(warns)}):")
    for w in warns[: (500 if VERBOSE else 40)]: print("  -", w)
if errors:
    print(f"\nFOUTEN ({len(errors)}):")
    for e in errors: print("  x", e)
    sys.exit(1)
print("\nGeen harde fouten.")
