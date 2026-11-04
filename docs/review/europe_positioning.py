"""Klantbesluit 04-11-2026: 'We werken met studio's door heel Europa en erbuiten, maar zijn een Spaans bedrijf.'
Positioneringszinnen in 5 talen, zonder aantallen; plus vertrouwenszin bij 'Wie zit er achter'. Idempotent."""
import glob, html, json, re
P = [
 # ---------- NL
 ("Mediterrano Pilates verzendt vanuit Spanje naar pilates-, yoga- en barrestudio's en fysiotherapiepraktijken in heel Europa, ook in Nederland en België.",
  "Mediterrano Pilates is een Spaans bedrijf en werkt met pilates-, yoga- en barrestudio's en fysiotherapiepraktijken in heel Europa en daarbuiten, ook in Nederland en België."),
 ("Mediterrano Pilates verzendt vanuit Spanje naar pilates-, yoga- en barrestudio's in heel Europa, ook in Nederland, België en Luxemburg.",
  "Mediterrano Pilates is een Spaans bedrijf en werkt met pilates-, yoga- en barrestudio's in heel Europa en daarbuiten, ook in Nederland, België en Luxemburg."),
 ("Mediterrano Pilates zit in Valencia en verzendt gratis naar heel Europa, dus ook naar Nederland en België.",
  "Mediterrano Pilates zit in Valencia en werkt met studio's in heel Europa en daarbuiten. De verzending is gratis binnen heel Europa, dus ook naar Nederland en België."),
 ("Mediterrano Pilates zit in Valencia en werkt met pilates- en yogastudio's in Spanje en de rest van Europa.",
  "Mediterrano Pilates zit in Valencia en werkt met pilates- en yogastudio's in heel Europa en daarbuiten."),
 ("<h2>We leveren aan studio's in heel <span class=\"fx\">Europa.</span></h2>", "<h2>We werken met studio's in <span class=\"fx\">heel Europa en daarbuiten.</span></h2>"),
 ("<h2>We verzenden naar studio's in <span class=\"fx\">heel Europa.</span></h2>", "<h2>We werken met studio's in <span class=\"fx\">heel Europa en daarbuiten.</span></h2>"),
 ("<h2>We werken met praktijken in <span class=\"fx\">heel Europa.</span></h2>", "<h2>We werken met praktijken in <span class=\"fx\">heel Europa en daarbuiten.</span></h2>"),
 ("We verzenden gratis vanuit Spanje naar heel Europa, dus ook naar Nederland, België en Luxemburg, en op aanvraag ook naar landen buiten Europa.",
  "We werken vanuit Spanje met studio's in heel Europa en daarbuiten. De verzending is gratis binnen heel Europa, dus ook naar Nederland, België en Luxemburg, en buiten Europa leveren we op aanvraag."),
 ("We verzenden vanuit Spanje gratis naar studio's in heel Europa, ook naar Nederland en België.",
  "We werken vanuit Spanje met studio's in heel Europa en daarbuiten. De verzending is gratis binnen heel Europa, ook naar Nederland en België."),
 ("We verzenden vanuit Spanje naar heel Europa, ook naar Nederland en België, en de verzending is gratis binnen heel Europa.",
  "We werken vanuit Spanje met studio's in heel Europa en daarbuiten, ook in Nederland en België, en de verzending is gratis binnen heel Europa."),
 ("We verzenden vanuit Spanje naar studio's en praktijken in heel Europa, en de verzending is gratis binnen heel Europa.",
  "We werken vanuit Spanje met studio's en praktijken in heel Europa en daarbuiten, en de verzending is gratis binnen heel Europa."),
 ("We verzenden vanuit Spanje naar studio's in heel Europa, en de verzending is gratis binnen heel Europa.",
  "We werken vanuit Spanje met studio's in heel Europa en daarbuiten, en de verzending is gratis binnen heel Europa."),
 ("We verzenden vanuit Spanje naar studio's in heel Europa, ook naar Nederland en België.", "We werken vanuit Spanje met studio's in heel Europa en daarbuiten, ook in Nederland en België."),
 ("We verzenden vanuit Spanje naar studio's in heel Europa, ook in Nederland en België.", "We werken vanuit Spanje met studio's in heel Europa en daarbuiten, ook in Nederland en België."),
 ("We verzenden vanuit Spanje naar studio's in heel Europa.", "We werken vanuit Spanje met studio's in heel Europa en daarbuiten."),
 ("We verzenden vanuit Spanje, en op aanvraag ook buiten Europa.", "We werken vanuit Spanje met studio's in heel Europa en daarbuiten; buiten Europa leveren we op aanvraag."),
 ("We verzenden vanuit Valencia naar heel Europa, en de verzending is gratis binnen heel Europa.", "We werken vanuit Valencia met studio's in heel Europa en daarbuiten, en de verzending is gratis binnen heel Europa."),
 ("We zitten in Valencia en verzenden naar heel Europa.", "We zitten in Valencia en werken met studio's in heel Europa en daarbuiten."),
 # ---------- DE
 ("Mediterrano Pilates versendet von Spanien aus an Pilates- und Yogastudios in ganz Europa, kostenlos und ohne versteckte Kosten.",
  "Mediterrano Pilates ist ein spanisches Unternehmen und arbeitet mit Pilates- und Yogastudios in ganz Europa und darüber hinaus. Der Versand innerhalb Europas ist kostenlos und ohne versteckte Kosten."),
 ("Mediterrano Pilates versendet von Spanien aus an Pilates-, Yoga- und Barre-Studios sowie Physiotherapie-Praxen in ganz Europa, kostenlos und ohne versteckte Kosten.",
  "Mediterrano Pilates ist ein spanisches Unternehmen und arbeitet mit Pilates-, Yoga- und Barre-Studios sowie Physiotherapie-Praxen in ganz Europa und darüber hinaus. Der Versand innerhalb Europas ist kostenlos und ohne versteckte Kosten."),
 ("Mediterrano Pilates versendet von Spanien aus in ganz Europa, und der Versand ist kostenlos, ohne versteckte Kosten.",
  "Mediterrano Pilates arbeitet von Spanien aus mit Studios in ganz Europa und darüber hinaus, und der Versand innerhalb Europas ist kostenlos, ohne versteckte Kosten."),
 ("<h2>Wir liefern in <span class=\"fx\">ganz Europa.</span></h2>", "<h2>Wir arbeiten in <span class=\"fx\">ganz Europa und darüber hinaus.</span></h2>"),
 ("Wir sitzen in Spanien und liefern in ganz Europa.", "Wir sitzen in Spanien und arbeiten mit Studios in ganz Europa und darüber hinaus."),
 ("Wir versenden von Spanien aus an Studios und Praxen in ganz Europa, und der Versand ist kostenlos, auch nach Deutschland, Österreich und in die Schweiz.",
  "Wir arbeiten von Spanien aus mit Studios und Praxen in ganz Europa und darüber hinaus, und der Versand innerhalb Europas ist kostenlos, auch nach Deutschland, Österreich und in die Schweiz."),
 ("Wir versenden von Spanien aus in ganz Europa, und der Versand ist kostenlos, auch nach Deutschland, Österreich und in die Schweiz.",
  "Wir arbeiten von Spanien aus mit Studios in ganz Europa und darüber hinaus, und der Versand innerhalb Europas ist kostenlos, auch nach Deutschland, Österreich und in die Schweiz."),
 ("Wir versenden von Spanien aus in ganz Europa, und der Versand ist kostenlos.", "Wir arbeiten von Spanien aus mit Studios in ganz Europa und darüber hinaus, und der Versand innerhalb Europas ist kostenlos."),
 ("Wir versenden von Spanien aus kostenlos an jedes Studio in Europa.", "Wir arbeiten von Spanien aus mit Studios in ganz Europa und darüber hinaus, und der Versand an jedes Studio in Europa ist kostenlos."),
 ("Wir versenden von Spanien aus in ganz Europa.", "Wir arbeiten von Spanien aus mit Studios in ganz Europa und darüber hinaus."),
 ("Vor allem Spanien, expandierend in ganz Europa, mit kostenlosem Versand in ganz Europa", "Ganz Europa und darüber hinaus, von Spanien aus, mit kostenlosem Versand in ganz Europa"),
 ("Hauptmarkt: Spanien, mit Expansion in ganz Europa und kostenlosem Versand in ganz Europa.", "Ein spanisches Unternehmen, das mit Studios in ganz Europa und darüber hinaus arbeitet, mit kostenlosem Versand in ganz Europa."),
 # ---------- EN
 ("Mediterrano Pilates works mainly with Pilates and yoga studios in Spain and is expanding across Europe.", "Mediterrano Pilates is a Spanish company working with Pilates and yoga studios across Europe and beyond."),
 ("Mediterrano Pilates works mainly with Pilates, yoga and barre studios and physiotherapy clinics in Spain, and is expanding across Europe.", "Mediterrano Pilates is a Spanish company working with Pilates, yoga and barre studios and physiotherapy clinics across Europe and beyond."),
 ("We work mainly with Pilates and yoga studios in Spain, we're expanding across Europe, and we ship free to studios throughout Europe, including the UK.",
  "We're a Spanish company working with Pilates and yoga studios across Europe and beyond, and we ship free to studios throughout Europe, including the UK."),
 ("We work mainly with studios and clinics in Spain and across Europe, and shipping is free across Europe, including the UK.",
  "We work with studios and clinics across Europe and beyond from our base in Spain, and shipping is free across Europe, including the UK."),
 ("We work mainly with studios in Spain and across Europe, and shipping is free across Europe, including the UK.",
  "We work with studios across Europe and beyond from our base in Spain, and shipping is free across Europe, including the UK."),
 ("We work mainly with studios in Spain, we're expanding across Europe, and we ship free to studios throughout Europe, including the UK.",
  "We work with studios across Europe and beyond from our base in Spain, and we ship free to studios throughout Europe, including the UK."),
 ("We work mostly with studios in Spain and the rest of Europe, and shipping is free across Europe, including the UK.",
  "We work with studios across Europe and beyond from our base in Spain, and shipping is free across Europe, including the UK."),
 ("We work mainly with studios in Spain and are expanding across Europe.", "We work with studios across Europe and beyond from our base in Spain."),
 ("We work mainly with studios in Spain and across Europe.", "We work with studios across Europe and beyond from our base in Spain."),
 ("<h2>We work with studios across <span class=\"fx\">Europe.</span></h2>", "<h2>We work with studios across <span class=\"fx\">Europe and beyond.</span></h2>"),
 ("<h2>We work with clinics across <span class=\"fx\">Europe.</span></h2>", "<h2>We work with clinics across <span class=\"fx\">Europe and beyond.</span></h2>"),
 ("We're based in Spain and ship to studios all over Europe.", "We're based in Spain and work with studios across Europe and beyond."),
 ("We're based in Spain and shipping is free across Europe, including the UK.", "We're based in Spain, work with studios across Europe and beyond, and shipping is free across Europe, including the UK."),
 ("Mainly Spain, expanding across Europe, with free shipping throughout Europe", "Across Europe and beyond, from Spain, with free shipping throughout Europe"),
 ("for Pilates and yoga studios in Spain and across Europe.", "for Pilates and yoga studios across Europe and beyond."),
 ("Main market: Spain, expanding across Europe, with free shipping across Europe (including the UK).", "A Spanish company working with studios across Europe and beyond, with free shipping across Europe (including the UK)."),
 # ---------- ES
 ("En Mediterrano Pilates trabajamos principalmente con estudios de pilates y yoga en España, estamos ampliando a toda Europa y enviamos gratis a estudios de toda Europa.",
  "Mediterrano Pilates es una empresa española que trabaja con estudios de pilates y yoga de toda Europa y de fuera de ella, y el envío es gratuito a toda Europa."),
 ("En Mediterrano Pilates trabajamos principalmente con estudios de pilates, yoga y barre en España, estamos ampliando a toda Europa y enviamos gratis a estudios de toda Europa.",
  "Mediterrano Pilates es una empresa española que trabaja con estudios de pilates, yoga y barre de toda Europa y de fuera de ella, y el envío es gratuito a toda Europa."),
 ("En Mediterrano Pilates trabajamos principalmente con estudios de pilates, yoga y barre y con clínicas de fisioterapia en España, estamos ampliando a toda Europa y enviamos gratis a centros de toda Europa.",
  "Mediterrano Pilates es una empresa española que trabaja con estudios de pilates, yoga y barre y con clínicas de fisioterapia de toda Europa y de fuera de ella, y el envío es gratuito a toda Europa."),
 ("Enviamos desde España a estudios de toda Europa.", "Trabajamos desde España con estudios de toda Europa y de fuera de ella."),
 ("<h2>Trabajamos con estudios de <span class=\"fx\">toda Europa.</span></h2>", "<h2>Trabajamos con estudios de <span class=\"fx\">toda Europa y de fuera de ella.</span></h2>"),
 ("<h2>Trabajamos con centros de <span class=\"fx\">toda Europa.</span></h2>", "<h2>Trabajamos con centros de <span class=\"fx\">toda Europa y de fuera de ella.</span></h2>"),
 ("Trabajamos principalmente con estudios en España, estamos ampliando a toda Europa, y enviamos gratis a estudios de toda Europa.",
  "Trabajamos desde España con estudios de toda Europa y de fuera de ella, y el envío es gratuito a toda Europa."),
 ("Trabajamos principalmente con estudios en España, ampliando a toda Europa.", "Trabajamos desde España con estudios de toda Europa y de fuera de ella."),
 ("Trabajamos sobre todo con estudios españoles y europeos, y el envío es gratuito a toda Europa", "Trabajamos desde España con estudios de toda Europa y de fuera de ella, y el envío es gratuito a toda Europa"),
 ("Trabajamos sobre todo con estudios y clínicas en España y Europa, y el envío es gratuito a toda Europa", "Trabajamos desde España con estudios y clínicas de toda Europa y de fuera de ella, y el envío es gratuito a toda Europa"),
 ("Principalmente España, ampliando a toda Europa, con envío gratuito a toda Europa", "Toda Europa y fuera de ella, desde España, con envío gratuito a toda Europa"),
 ("para estudios de pilates y yoga de España y del resto de Europa, con envío gratis a toda Europa.", "para estudios de pilates y yoga de toda Europa y de fuera de ella, con envío gratis a toda Europa."),
 ("Mercado principal: España. Envío gratuito a toda Europa.", "Empresa española que trabaja con estudios de toda Europa y de fuera de ella. Envío gratuito a toda Europa."),
 # ---------- FR
 ("Chez Mediterrano Pilates, nous livrons depuis l'Espagne les studios de Pilates et de yoga de toute l'Europe, avec une livraison gratuite, y compris en France, en Belgique, au Luxembourg et en Suisse.",
  "Mediterrano Pilates est une entreprise espagnole qui travaille avec des studios de Pilates et de yoga dans toute l'Europe et au-delà, avec une livraison gratuite en Europe, y compris en France, en Belgique, au Luxembourg et en Suisse."),
 ("Mediterrano Pilates s'adresse depuis l'Espagne aux studios de", "Depuis l'Espagne, Mediterrano Pilates travaille avec des studios de"),
 (" dans toute l'Europe, et livre en France", " dans toute l'Europe et au-delà, et livre en France"),
 ("Nous expédions depuis l'Espagne dans toute l'Europe, et la livraison est gratuite en France",
  "Nous travaillons depuis l'Espagne avec des studios de toute l'Europe et au-delà, et la livraison est gratuite en France"),
 ("Nous expédions depuis l'Espagne, et la livraison est gratuite dans toute l'Europe, y compris en France, en Belgique et au Luxembourg.",
  "Nous travaillons depuis l'Espagne avec des studios de toute l'Europe et au-delà, et la livraison est gratuite dans toute l'Europe, y compris en France, en Belgique et au Luxembourg."),
 ("Nous expédions gratuitement depuis l'Espagne dans toute l'Europe, et hors d'Europe sur devis.",
  "Nous travaillons depuis l'Espagne avec des studios de toute l'Europe et au-delà. La livraison est gratuite dans toute l'Europe, et hors d'Europe sur devis."),
 ("Nous expédions gratuitement depuis l'Espagne dans toute l'Europe, y compris en France, en Belgique, au Luxembourg et en Suisse.",
  "Nous travaillons depuis l'Espagne avec des studios de toute l'Europe et au-delà, et la livraison est gratuite dans toute l'Europe, y compris en France, en Belgique, au Luxembourg et en Suisse."),
 ("<h2>Nous livrons les studios de <span class=\"fx\">toute l'Europe.</span></h2>", "<h2>Nous travaillons avec des studios de <span class=\"fx\">toute l'Europe et au-delà.</span></h2>"),
 ("<h2>Nous travaillons avec des cabinets de <span class=\"fx\">toute l'Europe.</span></h2>", "<h2>Nous travaillons avec des cabinets de <span class=\"fx\">toute l'Europe et au-delà.</span></h2>"),
]
TRUST = {
 "Wie zit er achter Mediterrano Pilates?": "Steeds meer pilates-, yoga- en barrestudio's in heel Europa en daarbuiten verkopen hun eigen merkproducten via Mediterrano Pilates.",
 "Wer steckt hinter Mediterrano Pilates?": "Immer mehr Pilates-, Yoga- und Barre-Studios in ganz Europa und darüber hinaus verkaufen ihre eigenen Markenprodukte über Mediterrano Pilates.",
 "Who is behind Mediterrano Pilates?": "A growing number of Pilates, yoga and barre studios across Europe and beyond sell their own branded products through Mediterrano Pilates.",
 "¿Quién está detrás de Mediterrano Pilates?": "Cada vez más estudios de pilates, yoga y barre de toda Europa y de fuera de ella venden sus propios productos de marca con Mediterrano Pilates.",
 "Qui se trouve derrière Mediterrano Pilates ?": "De plus en plus de studios de Pilates, de yoga et de barre, dans toute l'Europe et au-delà, vendent leurs propres produits à leur marque avec Mediterrano Pilates.",
}
def plain(t): return html.unescape(re.sub(r"<[^>]+>", "", t)).replace(" ", " ").strip()
def var(a, b):
    out = [(a, b)]
    for x, y in list(out):
        if "'" in x: out += [(x.replace("'", "&#39;"), y.replace("'", "&#39;")), (x.replace("'", "’"), y.replace("'", "’"))]
    return out
def add_trust(s):
    pat = re.compile(r'(<summary><span class="qn">\d+</span>)(.*?)(</summary>\s*<p>)(.*?)(</p>)', re.S)
    changes = []
    def rep(m):
        q = plain(m.group(2))
        t = TRUST.get(q)
        if not t or plain(t) in plain(m.group(4)): return m.group(0)
        na = m.group(4).rstrip() + " " + t
        changes.append((plain(m.group(4)), plain(na)))
        return m.group(1) + m.group(2) + m.group(3) + na + m.group(5)
    s = pat.sub(rep, s)
    for old, new in changes:
        done = False
        for mm in re.finditer(r'"text":\s*"((?:[^"\\]|\\.)*)"', s):
            if json.loads('"' + mm.group(1) + '"').replace(" ", " ").strip() == old:
                s = s[:mm.start(1)] + json.dumps(new, ensure_ascii=False)[1:-1] + s[mm.end(1):]; done = True; break
        if not done: print("   JSON-LD niet gevonden:", old[:60])
    return s
files = glob.glob("site/**/*.html", recursive=True) + ["site/llms.txt", "docs/review/dennl/content.py", "docs/review/nl_parity.py", "docs/review/nl_barre/body_nl.html"] + glob.glob("docs/review/fr/*.json")
hits = {a: 0 for a, _ in P}
for f in files:
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in P:
        for x, y in var(a, b):
            if x in s and y not in s.replace(x, ""):
                hits[a] += s.count(x); s = s.replace(x, y)
            elif x in s:
                hits[a] += s.count(x); s = s.replace(x, y)
    if f.endswith(".html") and f.startswith("site/"): s = add_trust(s)
    if s != o: open(f, "w", encoding="utf-8").write(s)
# llms.txt: NL/FR-alinea aanvullen
ll = open("site/llms.txt", encoding="utf-8").read()
for a, b in [("gratis verzending binnen Europa. Een merk van Ecomtierra Group SL (Spanje).", "gratis verzending binnen Europa. We werken met studio's in heel Europa en daarbuiten. Een merk van Ecomtierra Group SL (Spanje)."),
             ("(France, Belgique, Luxembourg, Suisse et au-delà). Marque d'Ecomtierra Group SL (Espagne).", "(France, Belgique, Luxembourg, Suisse et au-delà). Nous travaillons avec des studios de toute l'Europe et au-delà. Marque d'Ecomtierra Group SL (Espagne).")]:
    if b not in ll: ll = ll.replace(a, b)
open("site/llms.txt", "w", encoding="utf-8").write(ll)
for a, n in hits.items():
    if not n: print("0x:", a[:90])
