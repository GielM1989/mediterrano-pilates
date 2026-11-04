"""Taalreview ronde 2 (FR/ES/EN), zichtbaar + JSON-LD + FR-dicts + bronscripts. Idempotent."""
import glob, re
P = [
 # FR
 ("Validez votre maquette gratuite <span class=\"fx\">avant le 15 novembre.</span>", "Validez votre maquette gratuite <span class=\"fx\">au plus tard le 15 novembre.</span>"),
 ('"45": "avant le 15 novembre."', '"45": "au plus tard le 15 novembre."'),
 ("validez votre maquette gratuite avant le 15 novembre", "validez votre maquette gratuite au plus tard le 15 novembre"),
 ("Validez votre maquette avant le 15 novembre.", "Validez votre maquette au plus tard le 15 novembre."),
 ("Oui. Nous travaillons depuis l'Espagne avec des studios de toute l'Europe, et la livraison est gratuite dans toute l'Europe, France, Belgique et Luxembourg compris.",
  "Oui. Nous expédions depuis l'Espagne, et la livraison est gratuite dans toute l'Europe, y compris en France, en Belgique et au Luxembourg."),
 ("Nous expédions depuis l'Espagne dans toute l'Europe, livraison gratuite comprise, y compris la France, la Belgique, le Luxembourg et la Suisse.",
  "Nous expédions gratuitement depuis l'Espagne dans toute l'Europe, y compris en France, en Belgique, au Luxembourg et en Suisse."),
 ("Nous expédions depuis l'Espagne dans toute l'Europe, livraison gratuite comprise, et aussi hors d'Europe sur devis.",
  "Nous expédions gratuitement depuis l'Espagne dans toute l'Europe, et hors d'Europe sur devis."),
 ("y compris la France, la Belgique, le Luxembourg et la Suisse", "y compris en France, en Belgique, au Luxembourg et en Suisse"),
 ("hors de l'Union européenne, comme la Suisse, le Royaume-Uni ou la Norvège,", "hors de l'Union européenne, par exemple vers la Suisse, le Royaume-Uni ou la Norvège,"),
 ("la TVA à l'importation (8,1 %) et les frais de dédouanement restent toujours à la charge du destinataire.",
  "la TVA à l'importation (8,1 %), les droits de douane éventuels et les frais de dédouanement restent toujours à la charge du destinataire."),
 ("À l'importation, la TVA suisse et les éventuels frais de dédouanement sont à la charge du destinataire, dans tous les cas.",
  "À l'importation, la TVA suisse, les droits de douane éventuels et les frais de dédouanement sont toujours à la charge du destinataire."),
 ("Chaque produit à votre logo est une visibilité sans frais d'annonce.", "Chaque produit à votre logo vous offre de la visibilité, sans frais publicitaires."),
 ("Chaque chaussette avec votre logo est une visibilité sans frais d'annonce.", "Chaque chaussette à votre logo vous offre de la visibilité, sans frais publicitaires."),
 ("Chaque chaussette à votre logo est une visibilité sans frais d'annonce (source", "Chaque chaussette à votre logo vous offre de la visibilité, sans frais publicitaires (source"),
 ("est une visibilité sans frais d'annonce.", "vous offre de la visibilité, sans frais publicitaires."),
 ("une visibilité sans frais d'annonce", "une visibilité sans frais publicitaires"),
 ("Le kit travaille aussi vers l'extérieur.", "Le kit fait aussi connaître votre studio au-delà de ses murs."),
 ("Une nouvelle élève qui se promène avec votre tote bag présente votre studio à la suivante.", "Une nouvelle élève qui se promène avec votre tote bag fait découvrir votre studio autour d'elle."),
 ("il continue en outre à travailler après Noël : l'élève le porte à chaque cours et sur chaque photo.", "il continue à faire connaître votre studio après Noël : l'élève le porte à chaque cours, et on le voit sur chaque photo."),
 ("se voit dans la rue, au travail et en faisant les courses", "se voit dans la rue, au travail et au marché"),
 ("la référence du secteur graphique", "la référence des professionnels de l'impression"),
 ("nous l'appliquons de la manière la mieux adaptée à chaque produit.", "nous l'appliquons avec la technique adaptée à chaque produit."),
 ("jamais imprimé, pour un logo qui résiste au lavage.", "jamais imprimé, pour qu'il résiste aux lavages."),
 ("à partir de la validation de la maquette, la commande arrive donc dans votre studio à la mi-décembre.", "à partir de la validation de la maquette. Votre commande peut donc arriver dans votre studio à la mi-décembre."),
 ("et nous préparons un devis sur mesure.", "et nous vous préparons un devis sur mesure."),
 # ES
 ("<h2>Aprueba tu boceto gratis <span class=\"fx\">antes del 15 de noviembre.</span></h2>", "<h2>Aprueba tu boceto gratuito <span class=\"fx\">como muy tarde el 15 de noviembre.</span></h2>"),
 ("aprueba tu boceto gratis antes del 15 de noviembre", "aprueba tu boceto gratuito como muy tarde el 15 de noviembre"),
 ("Aprueba tu boceto antes del 15 de noviembre.", "Aprueba tu boceto como muy tarde el 15 de noviembre."),
 ("Trabajamos desde España con estudios de toda Europa.", "Enviamos desde España a estudios de toda Europa."),
 ("como a Suiza, Reino Unido o Noruega", "como a Suiza, al Reino Unido o a Noruega"),
 ("corte mid-rise", "caña media"),
 ("el envío es gratuito a toda Europa, sin excepciones.", "el envío es gratuito a toda Europa."),
 # EN
 ("The Christmas gift that works best in a Pilates or yoga studio", "A Christmas gift that works well in a Pilates or yoga studio"),
 ("around €6.95 for a pair of grip socks, for example.", "around €6.95 (excl. VAT) for a pair of grip socks, for example."),
 ("the mockup needs to be approved by mid-November to have everything", "the mockup needs to be approved by 15 November to have everything"),
 ("Yes. Most of the studios we work with are in Spain and elsewhere in Europe, and shipping is free across Europe, including the UK.", "Yes. We're based in Spain and shipping is free across Europe, including the UK."),
 ("Yes, free of charge, just as we do across the rest of Europe. For deliveries outside the EU, such as to Switzerland, the UK or Norway, import VAT, duties and customs clearance costs are always paid by the recipient. We're based in Spain and work with studios all over Europe.",
  "Yes, and free of charge, as everywhere else in Europe. Ireland is in the EU, so there is nothing more to pay. For the UK, as for other destinations outside the EU, such as Switzerland or Norway, import VAT, duties and customs clearance costs are always paid by the recipient. We're based in Spain and ship to studios all over Europe."),
 ("no hidden costs from our side", "no hidden costs on our side"),
 ("Approve later and it may still arrive in time, but that's no longer in your hands.", "Approve later and it may still arrive in time, but that becomes less certain."),
]
def variants(a, b):
    out = [(a, b)]
    for sp in ("&nbsp;", " "):
        fa, fb = a, b
        for ch in (":", ";", "%", "?"):
            fa = fa.replace(" " + ch, sp + ch); fb = fb.replace(" " + ch, sp + ch)
        if fa != a: out.append((fa, fb))
    for x, y in list(out):
        if "'" in x: out.append((x.replace("'", "&#39;"), y.replace("'", "&#39;"))); out.append((x.replace("'", "’"), y.replace("'", "’")))
    return out
files = glob.glob("site/**/*.html", recursive=True) + glob.glob("docs/review/fr/*.json") + glob.glob("docs/review/fr/*.py") + ["docs/review/import_duties.py"]
hits = {a: 0 for a, _ in P}
for f in files:
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in P:
        for x, y in variants(a, b):
            if x in s and (y not in s or x not in y):
                hits[a] += s.count(x); s = s.replace(x, y)
    if s != o: open(f, "w", encoding="utf-8").write(s)
for a, n in hits.items():
    if not n: print("0x:", a[:70])
print("klaar")
