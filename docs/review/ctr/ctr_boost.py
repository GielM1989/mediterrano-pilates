#!/usr/bin/env python3
"""CTR/positie-boost voor pagina's die al op pagina 1 van Google staan (GSC 16-11-2026).
Titel/description, sectie op de zoekterm, FAQ (zichtbaar = JSON-LD), interne links, Pantone-claims.
Idempotent. Gebruik: python3 docs/review/ctr/ctr_boost.py (vanuit repo-root)."""
import re, sys, os, html
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "dennl"))
from aeo_upgrade import add_faqs

def rd(p): return open("site/" + p, encoding="utf-8").read()
def wr(p, s): open("site/" + p, "w", encoding="utf-8").write(s)

def set_meta(s, title, desc, og_title=None):
    s = re.sub(r"<title>.*?</title>", "<title>" + html.escape(title, quote=False) + "</title>", s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + html.escape(desc) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + html.escape(desc) + m.group(2), s, count=1)
    if og_title:
        s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + html.escape(og_title) + m.group(2), s, count=1)
    return s

def rep(s, a, b, must=True):
    if b in s and a not in s: return s
    if must: assert s.count(a) >= 1, a[:80]
    return s.replace(a, b)

def section_before(s, h2_start, block):
    if block.split("\n")[2] in s: return s
    i = s.index(h2_start); j = s.rindex('<section class="sheet', 0, i)
    return s[:j] + block + "\n\n" + s[j:]

def sec(h2, paras):
    ps = "\n".join(f'    <p style="margin-top:16px;max-width:44em">{p}</p>' for p in paras)
    return ('<section class="sheet cream">\n  <div class="wrap" style="padding-top:48px;padding-bottom:8px">\n'
            f'    <h2>{h2}</h2>\n{ps}\n  </div>\n</section>')

# ---------- 1. ES barre
p = "merchandising-estudios-barre/index.html"; s = rd(p)
s = set_meta(s, "Calcetines de barre antideslizantes con tu logo",
    "Calcetines de barre antideslizantes con el logo de tu estudio, tejido o bordado. Desde 50 pares, boceto gratis en 24 h y envío gratis a toda Europa.",
    "Calcetines de barre con el logo de tu estudio · Mediterrano Pilates")
s = rep(s, "Logo tejido o bordado, color igualado por Pantone,", "Logo tejido o bordado, color lo más cercano posible al código Pantone,")
s = rep(s, "<li>Color igualado a tu marca por código Pantone, el estándar del sector gráfico.</li>", "<li>Color lo más cercano posible al código Pantone de tu marca, el estándar del sector gráfico.</li>")
s = section_before(s, "<h2>Barre, pilates, Lagree o megaformer:", sec(
    'Qué calcetines se usan en barre, <span class="fx">y por qué con tu logo.</span>',
    ["En barre se entrena con calcetines antideslizantes: pliés, relevés y trabajo de equilibrio en la barra, sobre un suelo liso que pide agarre. Por eso muchos estudios de barre los piden en clase, y tus alumnas ya los compran en una tienda de deporte o por internet.",
     "Un buen calcetín de barre tiene agarre de PVC o silicona en toda la suela, un corte mid-rise que no se baja durante la clase y un tejido fino que deja sentir el suelo. Con el logo de tu estudio tejido o bordado, ese mismo calcetín se vende en tu recepción, y cada alumna lleva tu marca a la barra, a casa y a Instagram."]))
s, n1 = add_faqs(s, [
    ("¿Qué calcetines se necesitan para hacer barre?", "Calcetines antideslizantes con agarre de PVC o silicona en toda la suela y un corte mid-rise que se mantiene en su sitio durante pliés y relevés. Mediterrano Pilates los personaliza con el logo de tu estudio de barre, tejido o bordado, desde 50 pares."),
    ("¿Son iguales los calcetines de barre y los de pilates?", "En la práctica, sí: es el mismo calcetín, con agarre en toda la suela y corte mid-rise. Por eso un estudio que combina barre y pilates puede pedir un solo modelo con su logo para todas sus clases, desde 50 pares."),
])
wr(p, s); print("barre ES faq+", n1)

# links naar barre vanaf ES-sokkenpagina en ES-blog
p = "calcetines-antideslizantes-personalizados/index.html"; s = rd(p)
anchor = 'Los calcetines antideslizantes son obligatorios en la mayoría de clases de pilates y yoga con reformer o mat, así que tus alumnas ya los compran, en algún sitio.'
link = ' ¿Tienes un estudio de barre? Mira nuestros <a href="/merchandising-estudios-barre/" style="color:inherit;text-decoration:underline">calcetines de barre con logo</a>.'
if 'calcetines de barre con logo</a>' not in s:
    i = s.index(anchor); j = s.index("</p>", i); s = s[:j] + link + s[j:]
wr(p, s)
p = "blog/calcetines-antideslizantes-para-pilates/index.html"; s = rd(p)
if 'calcetines de barre</a>' not in s:
    m = re.search(r'(<p style="max-width:none;color:#4c554d;margin-bottom:18px">Un calcetín antideslizante lleva una suela de agarre.*?)(</p>)', s, re.S)
    s = s[:m.end(1)] + ' Lo mismo vale para los <a href="/merchandising-estudios-barre/" style="color:inherit;text-decoration:underline">calcetines de barre</a>.' + s[m.end(1):]
wr(p, s)

# ---------- 2. DE Stoppersocken
p = "de/stoppersocken-mit-logo/index.html"; s = rd(p)
s = set_meta(s, "Stoppersocken mit Logo für Pilates-Studios · ab 50 Paar",
    "Pilates-Socken mit eingewebtem oder aufgesticktem Logo deines Studios. Ab 50 Paar, kostenloses Mockup in 24 Std. und Gratisversand in ganz Europa.",
    "Stoppersocken mit Logo für Pilates-Studios · Mediterrano Pilates")
s = rep(s, "Eingewebtes oder besticktes Logo, exakter Farbabgleich nach Pantone,", "Eingewebtes oder besticktes Logo, Farbe so nah wie möglich am Pantone-Code,")
s = s.replace("Ja. Wir gleichen deine Markenfarbe exakt per Pantone-Code ab, dem Standard der Grafikbranche.", "Ja. Wir treffen deine Markenfarbe so nah wie möglich am Pantone-Code, dem Standard der Grafikbranche.")
s = section_before(s, "<h2>Produkt<span class=\"fx\">details.</span></h2>", sec(
    'Logo einweben oder besticken lassen: <span class="fx">was zu deinem Studio passt.</span>',
    ["Bei unseren Stoppersocken wird dein Logo nicht aufgedruckt, sondern direkt in die Socke eingewebt (Jacquard) oder aufgestickt. Ein Druck kann auf einer Sportsocke nach vielen Wäschen rissig werden, ein eingewebtes oder gesticktes Logo hält. Eingewebt liegt das Logo flach im Strickbild, gestickt ist es leicht erhaben. Welche Variante zu deinem Logo passt, siehst du im kostenlosen Mockup, bevor du dich entscheidest.",
     "So tragen deine Kundinnen Pilates-Socken mit deinem Logo statt mit dem einer fremden Marke: ab 50 Paar, mit Grip aus PVC oder Silikon auf der ganzen Sohle und in der Farbe deines Studios, so nah wie möglich am Pantone-Code. Für Physiotherapie-Praxen gibt es eine eigene Seite: <a href=\"/de/merchandising-fuer-physiotherapie-praxen/\" style=\"color:inherit;text-decoration:underline\">Socken für Physiotherapeuten mit Praxislogo</a>."]))
s, n2 = add_faqs(s, [
    ("Kann ich mein Logo in Socken einweben lassen?", "Ja. Wir weben dein Logo direkt in die Socke ein (Jacquard) oder sticken es auf, ganz wie du möchtest, nie gedruckt. Ab 50 Paar, mit kostenlosem Mockup in 24 Stunden."),
    ("Was ist der Unterschied zwischen eingewebtem und gesticktem Logo?", "Eingewebt ist das Logo Teil des Strickbilds und liegt flach in der Socke. Gestickt liegt es leicht erhaben auf. Beide halten häufiges Waschen aus. Welche Variante besser zu deinem Logo passt, zeigt dir das kostenlose Mockup."),
])
wr(p, s); print("stoppersocken faq+", n2)

# DE-blog besticken
p = "de/blog/socken-mit-logo-besticken-lassen/index.html"; s = rd(p)
s = set_meta(s, "Socken mit Logo besticken oder einweben lassen",
    "Socken mit Logo besticken oder einweben lassen: der Unterschied, Mindestmenge ab 50 Paar und ein kostenloses Mockup in 24 Std. für dein Pilates-Studio.")
wr(p, s)

# ---------- 3. DE Physio
p = "de/merchandising-fuer-physiotherapie-praxen/index.html"; s = rd(p)
s = set_meta(s, "Socken für Physiotherapeuten: Stoppersocken mit Praxislogo",
    "Stoppersocken mit dem Logo deiner Physiopraxis, zum Verkauf an deine Patientinnen und Patienten. Ab 50 Paar, Mockup in 24 Std., Gratisversand in Europa.",
    "Socken für Physiotherapeuten mit Praxislogo · Mediterrano Pilates")
s = rep(s, "<li>Farbe exakt nach deiner Marke abgestimmt, per Pantone-Code, dem Standard der Grafikbranche.</li>", "<li>Farbe so nah wie möglich an deiner Marke, per Pantone-Code, dem Standard der Grafikbranche.</li>")
s, n3 = add_faqs(s, [
    ("Welche Socken eignen sich für die Physiotherapie?", "Für Übungen auf der Matte, auf glattem Boden oder am Reformer eignen sich Stoppersocken mit Grip aus PVC oder Silikon auf der ganzen Sohle und Mid-Rise-Schnitt. Mediterrano Pilates fertigt sie mit dem Logo deiner Praxis, ab 50 Paar."),
])
wr(p, s); print("physio faq+", n3)

# ---------- 4. Tote bag
p = "tote-bags-personalizadas-estudios-yoga/index.html"; s = rd(p)
s = set_meta(s, "Tote bag de pilates con el logo de tu estudio",
    "Tote bag de pilates de algodón con el logo de tu estudio de pilates o yoga, desde 50 unidades. Boceto gratis en 24 h y envío gratis a toda Europa.",
    "Tote bag de pilates con el logo de tu estudio · Mediterrano Pilates")
s = rep(s, "color exacto igualado por Pantone.", "color lo más cercano posible al código Pantone.")
s = s.replace("Sí. El color de tu marca se iguala de forma exacta por código Pantone, el estándar del sector gráfico.", "Sí. El color de tu marca se reproduce lo más cerca posible de su código Pantone, el estándar del sector gráfico.")
s = s.replace("✳ Con tu logo, a tu estilo, y color exacto igualado por Pantone.", "✳ Con tu logo, a tu estilo, y color lo más cercano posible al código Pantone.")
s, n4 = add_faqs(s, [
    ("¿Qué es una tote bag de pilates?", "La bolsa de algodón con la que tus alumnas llevan a clase la esterilla, la ropa de cambio y la botella. Mediterrano Pilates la personaliza con el logo de tu estudio desde 50 unidades, con boceto gratis en 24 horas."),
])
wr(p, s); print("tote faq+", n4)
p = "blog/tote-bag-personalizada-estudio-pilates-yoga/index.html"; s = rd(p)
s = set_meta(s, "Tote bag personalizada para tu estudio de pilates o yoga",
    "Tote bag de pilates personalizada con el logo de tu estudio: material, pedido mínimo de 50 unidades y cómo conseguir tu boceto gratis en 24 horas.")
wr(p, s)
p = "en/custom-tote-bags/index.html"; s = rd(p)
s = set_meta(s, "Custom Pilates tote bags with your studio's logo",
    "Cotton canvas Pilates tote bag with your studio's logo, from 50 units. Free mockup in 24 hours and free shipping across Europe.")
wr(p, s)
