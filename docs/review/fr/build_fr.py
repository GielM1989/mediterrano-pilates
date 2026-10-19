#!/usr/bin/env python3
"""
Bouwt een Franse pagina uit de Spaanse bronpagina.

Gebruik:
  python3 docs/review/fr/build_fr.py <es-bron> <fr-doel> <fr-url-pad> <dict_page.json> [--check-only]

Werkwijze:
  1. Segmenten uit de Spaanse pagina halen (zelfde algoritme als extract.py,
     dus de indexen in dict_<pagina>.json blijven geldig).
  2. Elk segment vervangen: eerst dict_page (op index), dan dict_common (op tekst).
  3. JSON-LD: stringwaarden vervangen via dezelfde vertaalparen (plus dict_ld.json),
     URL's ES -> FR, inLanguage/areaServed/knowsLanguage toevoegen.
  4. Kop, hreflang, canonical, og, taalwisselaar, interne URL's, verborgen
     taalveld, JS-strings, rekenmachine, cookies (CNIL, basic consent mode).
  5. Rapport: onvertaalde segmenten, resterend Spaans, JSON-LD geldig,
     FAQ-JSON-LD gelijk aan zichtbare tekst.
"""
import re, sys, json, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BASE = "https://mediterranopilates.com"

# ---------------------------------------------------------------- URL-kaart
URL_MAP = {
    "/": "/fr/",
    "/calcetines-antideslizantes-personalizados/": "/fr/chaussettes-antiderapantes-personnalisees/",
    "/botellas-personalizadas-estudios-pilates/": "/fr/gourde-isotherme-personnalisee/",
    "/tote-bags-personalizadas-estudios-yoga/": "/fr/tote-bag-personnalise/",
    "/aro-de-pilates-personalizado/": "/fr/anneau-de-pilates-personnalise/",
    "/precios-y-margenes/": "/fr/prix-et-marges/",
    "/preguntas-frecuentes/": "/fr/faq/",
    "/como-funciona/": "/fr/comment-ca-marche/",
    "/mockup-gratis/": "/fr/maquette-gratuite/",
    "/sobre-mediterrano-pilates/": "/fr/a-propos-de-mediterrano-pilates/",
    "/merchandising-estudios-yoga/": "/fr/produits-personnalises-studios-yoga/",
    "/merchandising-estudios-barre/": "/fr/produits-personnalises-studios-barre/",
    "/merchandising-clinicas-fisioterapia/": "/fr/produits-personnalises-cabinets-kinesitherapie/",
    "/blog/": "/fr/blog/",
    "/blog/aumentar-ingresos-estudio-pilates-sin-stock/": "/fr/blog/augmenter-chiffre-affaires-studio-pilates-sans-stock/",
    "/blog/fidelizar-alumnas-pilates-productos-marca/": "/fr/blog/fideliser-eleves-pilates-produits-a-votre-logo/",
    "/blog/como-elegir-proveedor-calcetines-personalizados/": "/fr/blog/choisir-fournisseur-chaussettes-antiderapantes-personnalisees/",
    "/blog/cuanto-cuesta-personalizar-calcetines-antideslizantes/": "/fr/blog/prix-chaussettes-antiderapantes-personnalisees/",
    "/blog/regalos-de-navidad-alumnas-pilates/": "/fr/blog/cadeaux-de-noel-eleves-pilates/",
    "/blog/pack-de-bienvenida-alumnas-nuevas-pilates/": "/fr/blog/kit-de-bienvenue-nouveaux-eleves-pilates/",
    "/legal.html#aviso": "/fr/legal.html#mentions-legales",
    "/legal.html#privacidad": "/fr/legal.html#confidentialite",
    "/legal.html#condiciones": "/fr/legal.html#cgv",
    "/legal.html#contenido": "/fr/legal.html#contenu",
    "/legal.html#cookies": "/fr/legal.html#cookies",
    "/legal.html": "/fr/legal.html",
}

# hreflang-clusters: FR-pad -> {taal: pad}
def cluster_for(fr_path, es_src_text):
    """Leest de bestaande alternates uit de ES-bron en voegt fr toe."""
    alts = dict(re.findall(r'<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)">', es_src_text))
    alts["fr"] = BASE + fr_path
    return alts

# ------------------------------------------------------------ segmentatie
def extract(s):
    def mask(m): return "\x00" * len(m.group(0))
    body = re.sub(r"<style[\s\S]*?</style>", mask, s)
    body = re.sub(r"<script(?![^>]*ld\+json)[\s\S]*?</script>", mask, body)
    segs = []
    for m in re.finditer(r">([^<>\x00]+)<", body):
        t = m.group(1)
        if t.strip() and not re.fullmatch(r"[\s\d.,:;€%·|/()\-+&;#]*", t.strip()):
            segs.append(["text", m.start(1), m.end(1), t])
    for attr in ["alt", "placeholder", "content", "aria-label", "title", "data-name", "value"]:
        for m in re.finditer(r'\b' + attr + r'="([^"]+)"', body):
            t = m.group(1)
            if attr == "content" and (t.startswith("http") or t in ("width=device-width, initial-scale=1", "es_ES", "website", "summary_large_image", "nosniff", "noindex,follow")):
                continue
            if attr == "value" and not re.search(r"[a-zA-Záéíóúñ]{3,}", t):
                continue
            if re.search(r"[a-zA-Záéíóúñ]{2,}", t):
                segs.append([attr, m.start(1), m.end(1), t])
    return segs

SKIP_EXACT = {"ES", "EN", "DE", "NL", "FR", "→", "M", "xgv1e0t17c8focq9tix8hhuctxu291",
              "width=device-width, initial-scale=1.0", "Mediterrano Pilates", "mockup-aanvraag",
              "hola@mediterranopilates.com", "REACH", "Pantone", "Instagram", "LinkedIn", "WhatsApp",
              "Tote bag", "Tote bags", "+", "Ecomtierra Group SL", "Mediterrano", "Pilates", "product", "article", "Giel Mallens"}

def norm(t):
    t = html.unescape(t).replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()

# ------------------------------------------------------------------ JSON-LD
def translate_ld(txt, trmap, fr_path, page_extra, faq_extra=None):
    o = json.loads(txt)
    def tr_str(v):
        if v.startswith("http"):
            return map_url(v)
        n = norm(v)
        if n in trmap:
            return norm(html.unescape(trmap[n]))
        return v
    def walk(x):
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        if isinstance(x, list):
            return [walk(v) for v in x]
        if isinstance(x, str):
            return tr_str(x)
        return x
    o = walk(o)
    t = o.get("@type")
    if t == "Organization":
        o["url"] = BASE + "/fr/"
        o["areaServed"] = [
            {"@type": "Country", "name": "France"},
            {"@type": "Country", "name": "Belgique"},
            {"@type": "Country", "name": "Luxembourg"},
            {"@type": "Country", "name": "Suisse"},
            {"@type": "Country", "name": "Espagne"},
            {"@type": "Place", "name": "Europe"},
        ]
        o["knowsLanguage"] = ["fr", "es", "en", "de", "nl"]
    if t == "WebSite":
        o["url"] = BASE + "/fr/"
        if "inLanguage" in o and "fr" not in o["inLanguage"]:
            o["inLanguage"] = o["inLanguage"] + ["fr"]
    if t == "Service":
        o["@id"] = BASE + fr_path + "#service"
        o["areaServed"] = [
            {"@type": "Country", "name": "France"},
            {"@type": "Country", "name": "Belgique"},
            {"@type": "Country", "name": "Luxembourg"},
            {"@type": "Country", "name": "Suisse"},
            {"@type": "Place", "name": "Europe"},
        ]
        o["inLanguage"] = "fr"
    if t == "FAQPage" and faq_extra:
        for item in faq_extra:
            o["mainEntity"].append({"@type": "Question", "name": norm(html.unescape(item["q"])),
                                    "acceptedAnswer": {"@type": "Answer", "text": norm(html.unescape(item["a"]))}})
    if t in ("FAQPage", "Article", "BlogPosting", "Product", "WebPage", "CollectionPage", "AboutPage"):
        o.setdefault("inLanguage", "fr")
    if t in ("Article", "BlogPosting", "Blog", "CollectionPage") and str(o.get("inLanguage","")).startswith("es"):
        o["inLanguage"] = "fr"
    for k, v in (page_extra.get(t) or {}).items():
        o[k] = v
    out = json.dumps(o, ensure_ascii=False, indent=2)
    out = re.sub(r'("inLanguage": *)"es(-ES)?"', r'\1"fr"', out)
    return "\n" + out + "\n"

def map_url(u):
    if u.startswith(BASE):
        p = u[len(BASE):]
        for es in sorted(URL_MAP, key=len, reverse=True):
            if p == es or (p.startswith(es) and es != "/" and p[len(es):] in ("#product", "#service", "#article", "#faq", "#webpage")):
                return BASE + URL_MAP[es] + p[len(es):]
        return u
    return u

# ----------------------------------------------------------------- hoofd
def build(src_path, dst_path, fr_path, dict_page_path, check_only=False):
    s = open(src_path, encoding="utf-8").read()
    # Fase D voegde aan de bronpagina's een FR-hreflang en een FR-knop toe; die mogen de segmentindexen niet verschuiven.
    s = re.sub(r'\n[ \t]*<a href="[^"]*" hreflang="fr">FR</a>', '', s)
    s = re.sub(r'<link rel="alternate" hreflang="fr" href="[^"]*">\n', '', s)
    common = json.load(open(os.path.join(HERE, "dict_common.json"), encoding="utf-8"))
    ld_extra = json.load(open(os.path.join(HERE, "dict_ld.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "dict_ld.json")) else {}
    page = json.load(open(dict_page_path, encoding="utf-8")) if dict_page_path and os.path.exists(dict_page_path) else {}
    page_extra = page.get("_ld", {})

    segs = extract(s)
    # vertaalkaart voor JSON-LD (zichtbare tekst -> FR)
    trmap = {}
    for i, (kind, a, b, t) in enumerate(segs):
        fr = page.get(str(i))
        if fr is None:
            fr = common.get(t.strip())
        if fr is not None:
            trmap[norm(t)] = fr
    for k, v in ld_extra.items():
        trmap[norm(k)] = v
    for k, v in page.get("_ld_map", {}).items():
        trmap[norm(k)] = v
    for k, v in common.items():
        trmap.setdefault(norm(k), v)

    missing = []
    out = s
    # van achter naar voren vervangen zodat posities geldig blijven
    for i in sorted(range(len(segs)), key=lambda j: segs[j][1], reverse=True):
        kind, a, b, t = segs[i]
        if t.strip().startswith("{"):
            new = translate_ld(t, trmap, fr_path, page_extra, page.get("_faq_extra"))
            out = out[:a] + new + out[b:]
            continue
        fr = page.get(str(i))
        if fr is None:
            fr = common.get(t.strip())
        if fr is None:
            if t.strip() not in SKIP_EXACT:
                missing.append((i, kind, t.strip()[:100]))
            continue
        lead = t[:len(t) - len(t.lstrip())]
        trail = t[len(t.rstrip()):]
        if kind != "text":
            assert '"' not in fr, f"dubbele aanhalingstekens in attribuut {i}: {fr}"
        out = out[:a] + lead + fr + trail + out[b:]

    out = postprocess(out, s, fr_path, page)

    report = check(out, missing, fr_path)
    if not check_only:
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        open(dst_path, "w", encoding="utf-8").write(out)
        print(f"geschreven: {dst_path} ({len(out)} tekens)")
    return report

# ------------------------------------------------------------ nabewerking
JS_STRINGS = {
    "'Ya estamos preparando una primera propuesta para '": "'Nous préparons déjà une première proposition pour '",
    "'. Normalmente la recibirás en un plazo de 24 horas.'": "'. Vous la recevrez normalement sous 24 heures.'",
    "'No se ha podido enviar. Revisa los campos e inténtalo de nuevo, o escríbenos a hola@mediterranopilates.com'": "'L\\'envoi a échoué. Vérifiez les champs et réessayez, ou écrivez-nous à hola@mediterranopilates.com'",
    "'No se ha podido enviar. Revisa tu conexión e inténtalo de nuevo, o escríbenos a hola@mediterranopilates.com'": "'L\\'envoi a échoué. Vérifiez votre connexion et réessayez, ou écrivez-nous à hola@mediterranopilates.com'",
    "'Elige al menos un producto.'": "'Choisissez au moins un produit.'",
    "'Formato no admitido. Usa PNG, JPG o SVG.'": "'Format non pris en charge. Utilisez un fichier PNG, JPG ou SVG.'",
    "'El archivo pesa demasiado (máx. 7 MB).'": "'Le fichier est trop lourd (7 Mo maximum).'",
    "'Hola Mediterrano Pilates, tengo una pregunta sobre el merchandising para mi estudio.'": "'Bonjour Mediterrano Pilates, j\\'ai une question au sujet des produits personnalisés pour mon studio.'",
    "'Hola Mediterrano Pilates, tengo una pregunta sobre el merchandising para mi estudio de yoga.'": "'Bonjour Mediterrano Pilates, j\\'ai une question au sujet des produits personnalisés pour mon studio de yoga.'",
    "'Hola Mediterrano Pilates, tengo una pregunta sobre el merchandising para mi clínica de fisioterapia.'": "'Bonjour Mediterrano Pilates, j\\'ai une question au sujet des produits personnalisés pour mon cabinet de kinésithérapie.'",
    "'Enviando…'": "'Envoi en cours…'",
    "'.mw-card[data-product=\"Calcetines antideslizantes\"]'": "'.mw-card[data-product=\"Chaussettes antidérapantes\"]'",
    "remember(a.getAttribute('hreflang')||'es')": "remember(a.getAttribute('hreflang')||'fr')",
}
DATA_PRODUCT = {
    'data-product="Calcetines antideslizantes"': 'data-product="Chaussettes antidérapantes"',
    'data-product="Tumbler premium"': 'data-product="Gourde isotherme 1,2 L"',
    'data-product="Tote bag"': 'data-product="Tote bag"',
    'data-product="Aro de pilates"': 'data-product="Anneau de Pilates"',
}

GA_BASIC = """<script>
window.MP_GA_ID = 'G-Q9SY1F5KKF';
window.dataLayer = window.dataLayer || [];
function gtag(){ dataLayer.push(arguments); }
window.gtag = gtag;
gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied'});
/* Mode « basic » (CNIL) : gtag.js ne se charge qu'après « Tout accepter », voir le script cookies en bas de page. */
window.MP_loadGA = function(){
  if (window.MP_GA_LOADED) return;
  window.MP_GA_LOADED = true;
  gtag('consent','update',{'ad_storage':'granted','ad_user_data':'granted','ad_personalization':'granted','analytics_storage':'granted'});
  gtag('js', new Date());
  gtag('config', window.MP_GA_ID);
  var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+window.MP_GA_ID;document.head.appendChild(s);
};
</script>"""

COOKIE_SCRIPT = """<script>
(function(){
  /* Bandeau cookies conforme à la recommandation CNIL : rien ne se charge avant un choix,
     « Tout refuser » est aussi simple que « Tout accepter », le choix est conservé 6 mois
     et peut être modifié à tout moment via le lien « Gestion des cookies » en pied de page. */
  var KEY='mp_cookie_consent', TS='mp_cookie_consent_ts', MAX_AGE=183*24*60*60*1000;
  var bar=document.getElementById('cookieBar');
  function startPixel(){
    if(window.MP_PIXEL_ID && !window.MP_CONSENT){
      window.MP_CONSENT=true;
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
      n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
      document,'script','https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', window.MP_PIXEL_ID);
      fbq('track','PageView');
    }
  }
  function grantAll(){ if(typeof window.MP_loadGA==='function') window.MP_loadGA(); startPixel(); }
  function save(v){ try{ localStorage.setItem(KEY,v); localStorage.setItem(TS,String(Date.now())); }catch(e){} }
  var saved=null, ts=0;
  try{ saved=localStorage.getItem(KEY); ts=+localStorage.getItem(TS)||0; }catch(e){}
  if(!ts || (Date.now()-ts)>MAX_AGE){ saved=null; }
  if(saved==='granted'){ grantAll(); }
  else if(saved==='denied'){ /* rien ne se charge */ }
  else { bar.classList.add('show'); }
  document.getElementById('cookieAccept').addEventListener('click',function(){
    save('granted'); bar.classList.remove('show'); grantAll();
  });
  document.getElementById('cookieDecline').addEventListener('click',function(){
    save('denied'); bar.classList.remove('show');
  });
  var prefs=document.getElementById('cookiePrefs');
  if(prefs){ prefs.addEventListener('click',function(e){ e.preventDefault(); bar.classList.add('show'); }); }
})();
</script>"""

FR_STYLE = """<style>
/* /fr/ : boutons du bandeau cookies de même taille et de même visibilité (CNIL) */
.cookie-btn.decline{background:var(--cream);color:#22261F;border:1.5px solid var(--cream)}
.cookie-btn.decline:hover{background:#fff;color:#22261F}
.cookie-actions .cookie-btn{min-width:150px;text-align:center}
</style>"""

def postprocess(out, src, fr_path, page=None):
    page = page or {}
    fr_url = BASE + fr_path
    # letterlijke vervangingen (cijfers in numerieke segmenten, enz.)
    for old, new in page.get("_replace", []):
        if old not in out:
            print("WAARSCHUWING: _replace niet gevonden:", old[:60])
        out = out.replace(old, new)
    # invoegingen (feitenblok "En bref" enz.)
    for ins in page.get("_inserts", []):
        if "after" in ins:
            assert out.count(ins["after"]) == 1, "marker niet uniek: " + ins["after"][:60]
            out = out.replace(ins["after"], ins["after"] + ins["html"], 1)
        else:
            assert out.count(ins["before"]) == 1, "marker niet uniek: " + ins["before"][:60]
            out = out.replace(ins["before"], ins["html"] + ins["before"], 1)
    # extra FAQ-items (zichtbaar; JSON-LD krijgt dezelfde tekst in translate_ld)
    extra = page.get("_faq_extra", [])
    if extra:
        # bij meerdere FAQ-blokken (FAQ-pagina): achteraan het laatste blok, doornummeren vanaf het eerste
        first = out.index('<div class="faq">')
        start = out.rindex('<div class="faq">')
        n = len(re.findall(r'<details>', out[first:start + out[start:].index("\n    </div>")]))
        block = ""
        for k, item in enumerate(extra, start=n + 1):
            block += f'      <details>\n        <summary><span class="qn">{k:02d}</span>{item["q"]}</summary>\n        <p>{item["a"]}</p>\n      </details>\n'
        end = start + out[start:].index("\n    </div>")
        out = out[:end + 1] + block + out[end + 1:]
    # html lang
    out = out.replace('<html lang="es">', '<html lang="fr">', 1)
    # taalsuggestiebalk (alleen op ES-home) verwijderen
    out = re.sub(r"<!-- ============ TAALKEUZE ============[\s\S]*?</script>\n?", "", out, count=1)
    # relatieve assets -> absoluut
    out = re.sub(r'(href|src|srcset)="(images|fonts)/', r'\1="/\2/', out)
    out = re.sub(r"url\('(fonts|images)/", r"url('/\1/", out)
    # Franse typografie: fijne spatie voor ? na een span (bijv. "personnaliser</span>?")
    out = out.replace("</span>?<", "</span>&nbsp;?<")
    out = re.sub(r">(\+?\d+)%<", r">\1&nbsp;%<", out)
    out = re.sub(r"(?<=[>\s(])(\d+(?:[,.]\d+)?) (%|€)(?=[\s.,;:)<])", r"\1&nbsp;\2", out)
    # (niet binnen JSON-LD: daar hoort geen HTML in)
    parts = re.split(r'(<script type="application/ld\+json">[\s\S]*?</script>)', out)
    out = "".join(p if p.startswith('<script type="application/ld+json">') else re.sub(r"(>[^<]*?)\b1er novembre", r"\g<1>1<sup>er</sup> novembre", p) for p in parts)
    out = out.replace('href="/#', 'href="/fr/#')
    out = out.replace('href="/"', 'href="/fr/"').replace('href="./"', 'href="/fr/"').replace('href="en/"', 'href="/en/"').replace('href="de/"', 'href="/de/"')
    # interne URL's ES -> FR (langste eerst)
    for es in sorted(URL_MAP, key=len, reverse=True):
        if es == "/":
            continue
        out = out.replace(f'href="{es}"', f'href="{URL_MAP[es]}"')
        out = out.replace(f'href="{BASE}{es}"', f'href="{BASE}{URL_MAP[es]}"')
    # canonical + hreflang
    alts = cluster_for(fr_path, src)
    order = ["es", "en", "de", "nl", "fr", "x-default"]
    links = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{alts[l]}">' for l in order if l in alts)
    out = re.sub(r'<link rel="canonical" href="[^"]+">\n(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+',
                 f'<link rel="canonical" href="{fr_url}">\n{links}\n', out, count=1)
    out = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{fr_url}">', out, count=1)
    out = out.replace('<meta property="og:locale" content="es_ES">',
                      '<meta property="og:locale" content="fr_FR">\n<meta property="og:locale:alternate" content="es_ES">\n<meta property="og:locale:alternate" content="en_GB">\n<meta property="og:locale:alternate" content="de_DE">\n<meta property="og:locale:alternate" content="nl_NL">', 1)
    # taalwisselaar
    def lang_switch(m):
        cur = {"es": alts.get("es", BASE + "/"), "en": alts.get("en", BASE + "/en/"), "de": alts.get("de", BASE + "/de/"), "nl": alts.get("nl", BASE + "/nl/"), "fr": fr_url}
        rel = {k: v[len(BASE):] for k, v in cur.items()}
        lines = [f'    <nav class="lang-switch" aria-label="Langue">']
        for code in ["es", "en", "de", "nl", "fr"]:
            if code == "fr":
                lines.append(f'      <a href="{rel[code]}" class="on" hreflang="fr" aria-current="true">FR</a>')
            else:
                lines.append(f'      <a href="{rel[code]}" hreflang="{code}">{code.upper()}</a>')
        lines.append("    </nav>")
        return "\n".join(lines)
    out = re.sub(r'[ \t]*<nav class="lang-switch"[^>]*>[\s\S]*?</nav>', lang_switch, out, count=1)
    # verborgen taalveld
    out = out.replace('<input type="hidden" name="language" value="es">', '<input type="hidden" name="language" value="fr">')
    # JS-strings
    for k, v in JS_STRINGS.items():
        out = out.replace(k, v)
    for k, v in DATA_PRODUCT.items():
        out = out.replace(k, v)
    # rekenmachine: marge per paar en locale
    out = out.replace("toLocaleString('de-DE')", "toLocaleString('fr-FR')")
    out = out.replace("m=pairs*7.88;", "m=pairs*9.68;")
    out = out.replace("textContent=pct+'%';", "textContent=pct+'\\u00a0%';")
    # GA: basic consent mode
    out = re.sub(r"<script>\nwindow\.MP_GA_ID = 'G-Q9SY1F5KKF';[\s\S]*?</script>", GA_BASIC, out, count=1)
    # cookie-script
    out = re.sub(r"<script>\n\(function\(\)\{\n  var KEY='mp_cookie_consent';[\s\S]*?</script>", COOKIE_SCRIPT, out, count=1)
    # extra stijl voor gelijke knoppen
    out = out.replace("</head>", FR_STYLE + "\n</head>", 1)
    # footerlink cookies
    out = out.replace('id="cookiePrefs">Cookies</a>', 'id="cookiePrefs">Gestion des cookies</a>')
    # overige meta-/lang-sporen
    out = out.replace('lang="es-ES"', 'lang="fr-FR"')
    return out

# ------------------------------------------------------------------ controle
SPANISH_MARKERS = [r"¿", r"¡", r"\bel estudio\b", r"\btu logo\b", r"\btus\b", r"\bpara\b", r"\bcon\b", r"\bpor\b",
                   r"\bdel\b", r"\bgratis\b", r"\bcalcetin", r"\balumna", r"\bboceto\b", r"\bprecio", r"\benvío",
                   r"\bmargen\b", r"\bnosotros\b", r"\bestudio de pilates\b", r"\bsin compromiso\b", r"\bIVA\b"]

def visible_text(out):
    body = re.sub(r"<style[\s\S]*?</style>", " ", out)
    body = re.sub(r"<script[\s\S]*?</script>", " ", body)
    body = re.sub(r"<!--[\s\S]*?-->", " ", body)
    return html.unescape(re.sub(r"<[^>]+>", " ", body))

def check(out, missing, fr_path):
    rep = {"missing": missing, "spanish": [], "ld_ok": True, "faq_match": None, "em_dash": 0, "exclaim": 0}
    vis = visible_text(out)
    for pat in SPANISH_MARKERS:
        for m in re.finditer(pat, vis):
            ctx = vis[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
            rep["spanish"].append((pat, re.sub(r"\s+", " ", ctx)))
    rep["em_dash"] = vis.count("—")
    rep["exclaim"] = len(re.findall(r"[^\s!]!", vis))
    # JSON-LD
    faq_q, faq_a = [], []
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', out):
        try:
            o = json.loads(m.group(1))
        except Exception as e:
            rep["ld_ok"] = False
            rep.setdefault("ld_err", []).append(str(e))
            continue
        if o.get("@type") == "FAQPage":
            for q in o["mainEntity"]:
                faq_q.append(norm(q["name"]))
                faq_a.append(norm(q["acceptedAnswer"]["text"]))
    if faq_q:
        # vergelijking zonder spaties: tags in het zichtbare antwoord (links, <sup>) geven extra spaties
        visn = norm(vis).replace(" ", "")
        rep["faq_match"] = [(q, q.replace(" ", "") in visn) for q in faq_q] + [(a[:60], a.replace(" ", "") in visn) for a in faq_a]
    # resterende ES-URL's
    rep["es_urls"] = sorted(set(re.findall(r'href="(/(?!fr/|en/|de/|nl/|images/|fonts/|legal)[a-z0-9-]+/[^"]*)"', out)))
    rep["lang"] = re.search(r'<html lang="([a-z]+)">', out).group(1)
    rep["canonical"] = re.search(r'<link rel="canonical" href="([^"]+)">', out).group(1)
    rep["hreflang"] = re.findall(r'hreflang="([a-z-]+)" href=', out)
    return rep

def print_report(rep):
    print(f"lang={rep['lang']} canonical={rep['canonical']} hreflang={rep['hreflang']}")
    print(f"onvertaald: {len(rep['missing'])}")
    for m in rep["missing"]:
        print("   ", m)
    print(f"Spaanse sporen: {len(rep['spanish'])}")
    for m in rep["spanish"][:40]:
        print("   ", m)
    print(f"JSON-LD geldig: {rep['ld_ok']} {rep.get('ld_err','')}")
    if rep["faq_match"] is not None:
        bad = [q for q, ok in rep["faq_match"] if not ok]
        print(f"FAQ JSON-LD = zichtbaar: {len(bad)==0} ({len(rep['faq_match'])} gecontroleerd)")
        for b in bad:
            print("    MISMATCH:", b)
    print(f"ES-URL's over: {rep['es_urls']}")
    print(f"gedachtestreepjes: {rep['em_dash']}  uitroeptekens: {rep['exclaim']}")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    src, dst, fr_path, dpage = args[0], args[1], args[2], (args[3] if len(args) > 3 else None)
    rep = build(os.path.join(ROOT, src), os.path.join(ROOT, dst), fr_path, os.path.join(ROOT, dpage) if dpage else None,
                check_only="--check-only" in sys.argv)
    print_report(rep)
