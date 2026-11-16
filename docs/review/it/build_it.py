#!/usr/bin/env python3
"""Bouwt de Italiaanse sectie /it/ uit de huidige Franse pagina's (site/fr/).

Bron = de live Franse pagina (incl. alle latere aanpassingen: En bref, Europa-positionering,
tote min. 50, geen kerst). Vertaling per segment: docs/review/it/segs/<pagina>.txt (FR) en
docs/review/it/it/<pagina>.txt (IT), regel voor regel; _common geldt voor alle pagina's.

Gebruik: python3 docs/review/it/build_it.py [pagina ...]   (vanuit de repo-root)
"""
import sys, os, re, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "docs/review/fr"))
sys.path.insert(0, HERE)
import build_fr as B
from pages_it import PAGES

BASE = "https://mediterranopilates.com"
TODAY = "2026-11-16"

# ------------------------------------------------------------- URL-kaart FR -> IT
URL_MAP = {fr.replace("index.html", ""): it for fr, it in PAGES.values()}
URL_MAP.update({
    "/fr/legal.html#mentions-legales": "/it/legal.html#note-legali",
    "/fr/legal.html#confidentialite": "/it/legal.html#privacy",
    "/fr/legal.html#cgv": "/it/legal.html#condizioni",
    "/fr/legal.html#contenu": "/it/legal.html#contenuti",
    "/fr/legal.html#cookies": "/it/legal.html#cookie",
})

def load_pairs(name):
    fr = open(os.path.join(HERE, "segs", name + ".txt"), encoding="utf-8").read().rstrip("\n").split("\n")
    it = open(os.path.join(HERE, "it", name + ".txt"), encoding="utf-8").read().rstrip("\n").split("\n")
    if fr == [""]:
        fr, it = [], []
    assert len(fr) == len(it), f"{name}: {len(fr)} FR-regels, {len(it)} IT-regels"
    out = {}
    for n, (a, b) in enumerate(zip(fr, it), 1):
        if a.startswith("LD "):
            assert b.startswith("LD "), f"{name}:{n} LD-regel niet uitgelijnd: {b[:60]}"
            a, b = a[3:], b[3:]
        out[a] = b
    return out

def map_url(u):
    if u.startswith(BASE):
        return BASE + map_path(u[len(BASE):])
    return map_path(u)

def map_path(p):
    for fr in sorted(URL_MAP, key=len, reverse=True):
        if p == fr or (p.startswith(fr) and p[len(fr):][:1] in ("#", "")):
            return URL_MAP[fr] + p[len(fr):]
    return p

AREA = [{"@type": "Country", "name": "Italia"}, {"@type": "Country", "name": "Svizzera"},
        {"@type": "Country", "name": "Spagna"}, {"@type": "Place", "name": "Europa"}]
AREA_SERVICE = [{"@type": "Country", "name": "Italia"}, {"@type": "Country", "name": "Svizzera"},
                {"@type": "Place", "name": "Europa"}]

def tr_ld(txt, tmap, it_path, faqs, miss):
    o = json.loads(txt)
    t = o.get("@type")
    if t == "FAQPage":
        o["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
        o["inLanguage"] = "it"
        return "\n" + json.dumps(o, ensure_ascii=False, indent=2) + "\n"
    SKIPK = {"@type", "@context", "inLanguage", "priceCurrency", "price", "unitCode", "availability", "businessFunction",
             "datePublished", "dateModified", "email", "telephone", "knowsLanguage", "addressCountry", "legalName", "taxID",
             "vatID", "foundingDate", "isoCode", "name_" }
    def walk(x, key=None):
        if isinstance(x, dict):
            return {k: (v if k in SKIPK else walk(v, k)) for k, v in x.items()}
        if isinstance(x, list):
            return [walk(v, key) for v in x]
        if isinstance(x, str):
            if x.startswith("http") or x.startswith("/"):
                return map_url(x)
            n = B.norm(x)
            if n in tmap:
                return B.norm(html.unescape(tmap[n]))
            if re.search(r"[A-Za-zÀ-ÿ]{3,}", x) and key not in ("@id",):
                miss.append(("LD", key, n[:90]))
            return x
        return x
    o = walk(o)
    if t == "Organization":
        o["url"] = BASE + "/it/"
        o["areaServed"] = AREA
        o["knowsLanguage"] = ["it", "es", "en", "de", "nl", "fr"]
    if t == "WebSite":
        o["url"] = BASE + "/it/"
        o["inLanguage"] = "it"
    if t == "Service":
        o["@id"] = BASE + it_path + "#service"
        o["areaServed"] = AREA_SERVICE
    if "inLanguage" in o:
        o["inLanguage"] = "it" if not isinstance(o["inLanguage"], list) else ["it"]
    if t in ("Article", "BlogPosting"):
        o["datePublished"] = TODAY
        o["dateModified"] = TODAY
    out = json.dumps(o, ensure_ascii=False, indent=2)
    return "\n" + out + "\n"

JS = {
    "'Nous préparons déjà une première proposition pour '": "'Stiamo già preparando una prima proposta per '",
    "'. Vous la recevrez normalement sous 24 heures.'": "'. Di norma la riceverai entro 24 ore.'",
    "'Prepararemos una primera propuesta para '": "'Stiamo già preparando una prima proposta per '",
    "' y normalmente la recibirás en un plazo de 24 horas.'": "'. Di norma la riceverai entro 24 ore.'",
    "'L\\'envoi a échoué. Vérifiez les champs et réessayez, ou écrivez-nous à hola@mediterranopilates.com'": "'Invio non riuscito. Controlla i campi e riprova, oppure scrivici a hola@mediterranopilates.com'",
    "'L\\'envoi a échoué. Vérifiez votre connexion et réessayez, ou écrivez-nous à hola@mediterranopilates.com'": "'Invio non riuscito. Controlla la connessione e riprova, oppure scrivici a hola@mediterranopilates.com'",
    "'No se pudo enviar. Revisa los campos e inténtalo de nuevo, o escríbenos a hola@mediterranopilates.com'": "'Invio non riuscito. Controlla i campi e riprova, oppure scrivici a hola@mediterranopilates.com'",
    "'No se pudo enviar. Revisa tu conexión e inténtalo de nuevo, o escríbenos a hola@mediterranopilates.com'": "'Invio non riuscito. Controlla la connessione e riprova, oppure scrivici a hola@mediterranopilates.com'",
    "'Choisissez au moins un produit.'": "'Scegli almeno un prodotto.'",
    "'Format non pris en charge. Utilisez un fichier PNG, JPG ou SVG.'": "'Formato non supportato. Usa un file PNG, JPG o SVG.'",
    "'Le fichier est trop lourd (7 Mo maximum).'": "'Il file è troppo pesante (max 7 MB).'",
    "'Bonjour Mediterrano Pilates, j\\'ai une question au sujet des produits personnalisés pour mon studio.'": "'Ciao Mediterrano Pilates, ho una domanda sui prodotti personalizzati per il mio studio.'",
    "'Bonjour Mediterrano Pilates, j\\'ai une question au sujet des produits personnalisés pour mon studio de yoga.'": "'Ciao Mediterrano Pilates, ho una domanda sui prodotti personalizzati per il mio studio di yoga.'",
    "'Bonjour Mediterrano Pilates, j\\'ai une question au sujet des produits personnalisés pour mon cabinet de kinésithérapie.'": "'Ciao Mediterrano Pilates, ho una domanda sui prodotti personalizzati per il mio studio di fisioterapia.'",
    "'Envoi en cours…'": "'Invio in corso…'",
    "'Referencia: '": "'Riferimento: '",
    "'.mw-card[data-product=\"Chaussettes antidérapantes\"]'": "'.mw-card[data-product=\"Calze antiscivolo\"]'",
    "'.mw-card[data-product=\"Calcetines antideslizantes\"]'": "'.mw-card[data-product=\"Calze antiscivolo\"]'",
    "remember(a.getAttribute('hreflang')||'fr')": "remember(a.getAttribute('hreflang')||'it')",
    "toLocaleString('fr-FR')": "toLocaleString('de-DE')",  # de-DE groepeert ook 4 cijfers met een punt, zoals gebruikelijk in het Italiaans
    "m=pairs*9.68;": "m=pairs*9.40;",
    "textContent=pct+'\\u00a0%';": "textContent=pct+'%';",
}
ATTR = {
    'data-product="Chaussettes antidérapantes"': 'data-product="Calze antiscivolo"',
    'data-product="Gourde isotherme 1,2 L"': 'data-product="Tumbler termico 1,2 L"',
    'data-product="Toalla reformer Calma"': 'data-product="Telo Reformer Calma"',
    "data-product=\"Calcetines antideslizantes\"": 'data-product="Calze antiscivolo"',
}
COMMENTS = [
    ("/* Mode « basic » (CNIL) : gtag.js ne se charge qu'après « Tout accepter », voir le script cookies en bas de page. */",
     "/* Modalità « basic »: gtag.js si carica solo dopo « Accetta tutto » (linee guida del Garante Privacy), vedi lo script dei cookie in fondo alla pagina. */"),
    ("/* Bandeau cookies conforme à la recommandation CNIL : rien ne se charge avant un choix,\n     « Tout refuser » est aussi simple que « Tout accepter », le choix est conservé 6 mois\n     et peut être modifié à tout moment via le lien « Gestion des cookies » en pied de page. */",
     "/* Banner cookie secondo le linee guida del Garante Privacy (10 giugno 2021): nulla si carica prima di una scelta,\n     « Rifiuta tutto » è semplice quanto « Accetta tutto », la scelta resta valida 6 mesi\n     e si può modificare in qualsiasi momento con il link « Gestione dei cookie » in fondo alla pagina. */"),
    ("/* rien ne se charge */", "/* non si carica nulla */"),
    ("/* /fr/ : boutons du bandeau cookies de même taille et de même visibilité (CNIL) */",
     "/* /it/: pulsanti del banner cookie di uguale dimensione e visibilità (Garante Privacy) */"),
]


COOKIE_BLOCK = """<div class="cookie-bar" id="cookieBar" role="dialog" aria-label="Cookie">
  <button type="button" class="cookie-x" id="cookieClose" aria-label="Chiudi senza accettare">×</button>
  <p>Usiamo cookie tecnici e, solo con il tuo consenso, cookie di statistica (Google Analytics) e di marketing (Meta Pixel). Chiudendo il banner con la X continui a navigare solo con i cookie tecnici. Puoi cambiare idea in qualsiasi momento con “Gestione dei cookie” in fondo alla pagina. <a href="/it/legal.html#cookie">Cookie policy</a> · <a href="/it/legal.html#privacy">Informativa sulla privacy</a>.</p>
  <div class="cookie-choices" id="cookieChoices" hidden>
    <label><input type="checkbox" checked disabled> Necessari (sempre attivi)</label>
    <label><input type="checkbox" id="ckStats"> Statistica (Google Analytics)</label>
    <label><input type="checkbox" id="ckMkt"> Marketing (Meta Pixel)</label>
  </div>
  <div class="cookie-actions">
    <button type="button" class="cookie-btn decline" id="cookieDecline">Rifiuta tutto</button>
    <button type="button" class="cookie-btn decline" id="cookieCustom">Personalizza</button>
    <button type="button" class="cookie-btn accept" id="cookieAccept">Accetta tutto</button>
  </div>
</div>
<script>
(function(){
  /* Banner cookie secondo le linee guida del Garante Privacy (10 giugno 2021): nulla si carica prima di una scelta,
     « Rifiuta tutto » e la X hanno lo stesso peso di « Accetta tutto », « Personalizza » permette di scegliere
     le singole finalità, la scelta resta valida 6 mesi e si può modificare con « Gestione dei cookie » in fondo alla pagina. */
  var KEY='mp_cookie_consent', TS='mp_cookie_consent_ts', MAX_AGE=183*24*60*60*1000;
  var bar=document.getElementById('cookieBar'), box=document.getElementById('cookieChoices');
  var cS=document.getElementById('ckStats'), cM=document.getElementById('ckMkt'), custom=document.getElementById('cookieCustom');
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
    if(typeof window.gtag==='function'){ gtag('consent','update',{'ad_storage':'granted','ad_user_data':'granted','ad_personalization':'granted'}); }
  }
  function wipe(){
    /* revoca: elimina i cookie di Google Analytics e Meta e ricarica la pagina, così nessuno strumento resta attivo */
    document.cookie.split(';').forEach(function(c){ var n=c.split('=')[0].trim();
      if(/^_ga|^_gid|^_fbp|^_fbc/.test(n)){ ['', '; domain='+location.hostname, '; domain=.'+location.hostname.replace(/^www[.]/,'')].forEach(function(d){ document.cookie=n+'=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'+d; }); } });
    location.reload();
  }
  function startGA(){ if(typeof window.MP_loadGA==='function') window.MP_loadGA(); }
  function apply(v){
    if(v==='granted'){ startGA(); startPixel(); }
    else if(v && v.indexOf('custom:')===0){ if(v.indexOf('s1')>-1) startGA(); if(v.indexOf('m1')>-1) startPixel(); }
  }
  function save(v){ try{ localStorage.setItem(KEY,v); localStorage.setItem(TS,String(Date.now())); }catch(e){} }
  function close(){ bar.classList.remove('show'); box.hidden=true; custom.textContent='Personalizza'; }
  var saved=null, ts=0;
  try{ saved=localStorage.getItem(KEY); ts=+localStorage.getItem(TS)||0; }catch(e){}
  if(!ts || (Date.now()-ts)>MAX_AGE){ saved=null; }
  if(saved==='granted' || saved==='denied' || (saved && saved.indexOf('custom:')===0)){ apply(saved); }
  else { bar.classList.add('show'); }
  function running(){ return !!(window.MP_GA_LOADED || window.MP_CONSENT); }
  function refuse(){ var was=running(); save('denied'); close(); if(was) wipe(); }
  document.getElementById('cookieAccept').addEventListener('click',function(){ save('granted'); close(); apply('granted'); });
  document.getElementById('cookieDecline').addEventListener('click',refuse);
  document.getElementById('cookieClose').addEventListener('click',refuse);
  custom.addEventListener('click',function(){
    if(box.hidden){ box.hidden=false; custom.textContent='Salva le scelte'; return; }
    var v='custom:'+(cS.checked?'s1':'s0')+(cM.checked?'m1':'m0');
    var drop=(window.MP_GA_LOADED && !cS.checked) || (window.MP_CONSENT && !cM.checked);
    save(v); close(); if(drop){ wipe(); } else { apply(v); }
  });
  var prefs=document.getElementById('cookiePrefs');
  if(prefs){ prefs.addEventListener('click',function(e){ e.preventDefault(); bar.classList.add('show'); }); }
})();
</script>"""
COOKIE_CSS = """<style>
/* /it/: X di chiusura e scelta per finalità (Garante Privacy) */
.cookie-bar{position:fixed}
.cookie-x{position:absolute;top:6px;right:10px;background:none;border:none;color:rgba(245,238,224,.8);font-size:1.4rem;line-height:1;cursor:pointer;padding:4px 6px}
.cookie-bar p{padding-right:22px}
.cookie-choices{display:flex;flex-wrap:wrap;gap:8px 18px;width:100%;font-size:.85rem;color:rgba(245,238,224,.9)}
.cookie-choices[hidden]{display:none}
.cookie-choices label{display:flex;align-items:center;gap:6px;cursor:pointer}
.cookie-actions{flex-wrap:wrap}
@media (max-width:560px){.cookie-actions .cookie-btn{flex:1 1 30%}.cookie-choices{font-size:.75rem;gap:4px 12px}}
</style>"""
LEGAL_IDS = [('id="mentions-legales"', 'id="note-legali"'), ('id="confidentialite"', 'id="privacy"'),
             ('id="cookies"', 'id="cookie"'), ('id="cgv"', 'id="condizioni"'), ('id="contenu"', 'id="contenuti"')]

def lang_switch(alts, it_url):
    rel = {k: v[len(BASE):] for k, v in alts.items()}
    defaults = {"es": "/", "en": "/en/", "de": "/de/", "nl": "/nl/", "fr": "/fr/"}
    lines = ['    <nav class="lang-switch" aria-label="Lingua">']
    for code in ["es", "en", "de", "nl", "fr", "it"]:
        if code == "it":
            lines.append(f'      <a href="{it_url[len(BASE):]}" class="on" hreflang="it" aria-current="true">IT</a>')
        else:
            lines.append(f'      <a href="{rel.get(code, defaults[code])}" hreflang="{code}">{code.upper()}</a>')
    lines.append("    </nav>")
    return "\n".join(lines)

def visible_faqs(out):
    faqs = []
    for m in re.finditer(r"<details>\s*<summary>(.*?)</summary>\s*(.*?)</details>", out, re.S):
        q = re.sub(r'<span class="qn">.*?</span>', "", m.group(1))
        q = B.norm(html.unescape(re.sub(r"<[^>]+>", "", q)))
        a = B.norm(html.unescape(re.sub(r"<[^>]+>", " ", m.group(2))))
        a = re.sub(r"\s+([.,;:?)])", r"\1", a)
        faqs.append((q, a))
    return faqs

def build(name):
    fr_rel, it_path = PAGES[name]
    src = open(os.path.join(ROOT, "site", fr_rel.lstrip("/")), encoding="utf-8").read()
    tmap = load_pairs("_common")
    tmap.update(load_pairs(name))
    segs = B.extract(src)
    miss = []
    out = src
    ld_slots = []
    for i in sorted(range(len(segs)), key=lambda j: segs[j][1], reverse=True):
        kind, a, b, t = segs[i]
        tt = t.strip()
        if tt.startswith("{"):
            ld_slots.append((a, b))
            continue
        n = B.norm(tt)
        if n in tmap:
            new = tmap[n]
        elif tt in B.SKIP_EXACT or n in B.SKIP_EXACT or n == "IT":
            continue
        else:
            miss.append((kind, n[:90]))
            continue
        if kind != "text":
            new = html.escape(new, quote=True).replace("&#x27;", "'")
        else:
            new = html.escape(new, quote=False)
        lead = t[:len(t) - len(t.lstrip())]
        trail = t[len(t.rstrip()):]
        out = out[:a] + lead + new + trail + out[b:]
    # JSON-LD opnieuw (posities zijn verschoven: zoek de blokken opnieuw)
    faqs = visible_faqs(out)
    def ld_sub(m):
        return '<script type="application/ld+json">' + tr_ld(m.group(1), tmap, it_path, faqs, miss) + "</script>"
    out = re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>', ld_sub, out)
    out = post(out, src, it_path)
    return out, miss, faqs

def post(out, src, it_path):
    it_url = BASE + it_path.replace("index.html", "")
    out = out.replace('<html lang="fr">', '<html lang="it">', 1)
    out = out.replace('lang="fr-FR"', 'lang="it-IT"')
    # Franse typografie terugdraaien
    out = re.sub(r"&nbsp;([%:;?!])", r"\1", out)
    out = re.sub(r" ([%:;?!])", r"\1", out)
    # interne links FR -> IT
    def href(m):
        u = m.group(2)
        return m.group(1) + map_url(u) + '"'
    out = re.sub(r'(href=")((?:' + re.escape(BASE) + r')?/fr/[^"]*)"', href, out)
    out = out.replace('href="/fr/"', 'href="/it/"')
    # canonical + hreflang
    alts = dict(re.findall(r'<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)">', src))
    alts["it"] = it_url
    order = ["es", "en", "de", "nl", "fr", "it", "x-default"]
    links = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{alts[l]}">' for l in order if l in alts)
    out = re.sub(r'<link rel="canonical" href="[^"]+">\n(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+',
                 f'<link rel="canonical" href="{it_url}">\n{links}\n', out, count=1)
    out = re.sub(r'<meta property="og:url" content="[^"]+">', f'<meta property="og:url" content="{it_url}">', out, count=1)
    out = out.replace('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="it_IT">\n<meta property="og:locale:alternate" content="fr_FR">', 1)
    out = re.sub(r'[ \t]*<nav class="lang-switch"[^>]*>[\s\S]*?</nav>', lambda m: lang_switch({k: v for k, v in alts.items() if k != "x-default"}, it_url), out, count=1)
    out = out.replace('<input type="hidden" name="language" value="fr">', '<input type="hidden" name="language" value="it">')
    for k, v in JS.items():
        out = out.replace(k, v)
    for k, v in ATTR.items():
        out = out.replace(k, v)
    for k, v in COMMENTS:
        out = out.replace(k, v)
    if 'id="cookieBar"' in out:
        out, n = re.subn(r'<div class="cookie-bar" id="cookieBar"[\s\S]*?</div>\n</div>\n<script>\n\(function\(\)\{[\s\S]*?</script>', lambda m: COOKIE_BLOCK, out, count=1)
        assert n == 1, "cookieblok niet gevonden"
        out = out.replace("</head>", COOKIE_CSS + "\n</head>", 1)
    out = re.sub(r'<time datetime="\d{4}-\d{2}-\d{2}">', '<time datetime="' + TODAY + '">', out)
    out = out.replace("gtag('consent','update',{'ad_storage':'granted','ad_user_data':'granted','ad_personalization':'granted','analytics_storage':'granted'});",
                      "gtag('consent','update',{'analytics_storage':'granted'}); /* segnali pubblicitari solo con il consenso marketing, vedi startPixel */")
    out = out.replace('>Tote bags<', '>Tote bag<')
    for a, b in LEGAL_IDS:
        out = out.replace(a, b)
    return out

SPOT_FR = [r"\b(vous|votre|vos|nous|avec|pour|les|des|chaussette|élève|maquette|devis|TVA|Suisse|Belgique|Luxembourg|France)\b",
           r"[àâçéèêëîïôûùœ]{1}\w*\b(?<!città)(?<!più)(?<!è)"]

def report(name, out, miss, faqs):
    vis = B.visible_text(out)
    fr_hits = [m.group(0) for m in re.finditer(SPOT_FR[0], vis)]
    print(f"== {name}: onvertaald {len(miss)}, FR-woorden zichtbaar {len(fr_hits)} {sorted(set(fr_hits))[:12]}, FAQ {len(faqs)}, '!' {len(re.findall(r'[^\s!]!', vis))}, '—' {vis.count('—')}")
    for m in miss[:30]:
        print("   ", m)
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', out):
        json.loads(m.group(1))
    left = sorted(set(re.findall(r'href="(/fr/[^"]*)"', out)))
    if left:
        print("    FR-links over:", left)

if __name__ == "__main__":
    names = sys.argv[1:] or list(PAGES)
    for name in names:
        out, miss, faqs = build(name)
        dst = os.path.join(ROOT, "site", PAGES[name][1].lstrip("/"))
        if dst.endswith("/"):
            dst += "index.html"
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write(out)
        report(name, out, miss, faqs)
