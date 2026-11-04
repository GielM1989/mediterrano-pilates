"""Kwaliteitsvraag (vervangt de promotiesok-vergelijking, klantbesluit 04-11-2026): zelfde feiten, geen vergelijking."""
import sys, json, glob
sys.path.insert(0, 'docs/review/dennl')
from aeo_upgrade import add_faqs
NB = "&nbsp;"
Q = {
 "es": ("¿Qué calidad tienen vuestros calcetines antideslizantes?",
        "Es un calcetín antideslizante de verdad, pensado para la clase: suela con agarre de PVC o silicona, corte mid-rise, material verificado según REACH y tu logo tejido o bordado, nunca estampado, para que no se agriete ni se despegue con los lavados. Es el calcetín que tus alumnas llevan en cada clase y por eso lo compran con gusto."),
 "en": ("How good is the quality of your grip socks?",
        "It's a real grip sock, made for class: PVC or silicone grips across the whole sole, a mid-rise cut, material tested to REACH, and your logo woven or embroidered, never printed, so it won't crack or peel in the wash. It's the sock your clients wear in every class, and that's why they're happy to buy it."),
 "de": ("Wie gut ist die Qualität eurer Stoppersocken?",
        "Es ist eine echte Stoppersocke, gemacht für die Stunde: Grip-Noppen aus PVC oder Silikon über die gesamte Sohle, Mid-Rise-Schnitt, Material nach REACH geprüft, und dein Logo eingewebt oder aufgestickt, nie aufgedruckt, damit in der Wäsche nichts reißt oder abblättert. Deine Kundinnen tragen sie in jeder Stunde und genau deshalb kaufen sie sie gern."),
 "nl": ("Hoe goed is de kwaliteit van jullie antislipsokken?",
        "Het is een echte antislipsok, gemaakt voor de les: antislipnopjes van PVC of siliconen over de hele zool, een middelhoge schacht, materiaal getest volgens REACH en je logo in de sok geweven of geborduurd, nooit bedrukt, zodat er in de was niets barst of afbladdert. Je leden dragen hem in elke les, en daarom kopen ze hem graag."),
 "fr": (f"Quelle est la qualité de vos chaussettes antidérapantes{NB}?",
        f"C'est une vraie chaussette antidérapante faite pour le cours{NB}: semelle à picots en PVC ou silicone, coupe mi-haute, matière conforme à REACH et logo tissé ou brodé dans la maille, jamais imprimé, pour un logo qui résiste au lavage. C'est la chaussette que vos élèves portent à chaque séance, et c'est pour cela qu'elles l'achètent volontiers."),
}
PAGES = {
 "es": ["calcetines-antideslizantes-personalizados", "preguntas-frecuentes"],
 "en": ["en/custom-grip-socks", "en/faq"],
 "de": ["de/stoppersocken-mit-logo", "de/faq", "de/merchandise-fuer-yogastudios"],
 "nl": ["nl/antislipsokken-met-logo", "nl/veelgestelde-vragen", "nl/merchandise-voor-yogastudios"],
 "fr": ["fr/chaussettes-antiderapantes-personnalisees", "fr/faq", "fr/produits-personnalises-studios-yoga",
        "fr/produits-personnalises-studios-barre", "fr/produits-personnalises-cabinets-kinesitherapie"],
}
for lang, pages in PAGES.items():
    for p in pages:
        f = f"site/{p}/index.html"
        s = open(f, encoding="utf-8").read()
        s2, n = add_faqs(s, [Q[lang]])
        if n: open(f, "w", encoding="utf-8").write(s2)
        print(f, "+", n)
# Franse woordenboeken: zelfde vraag in _faq_extra, zodat een herbouw hem behoudt
for d in ["socks", "faq", "preguntas-frecuentes", "produits-personnalises-studios-yoga", "produits-personnalises-studios-barre", "produits-personnalises-cabinets-kinesitherapie"]:
    fn = f"docs/review/fr/dict_{d}.json"
    try: j = json.load(open(fn, encoding="utf-8"))
    except FileNotFoundError: continue
    ex = j.setdefault("_faq_extra", [])
    if not any("qualité de vos chaussettes" in x.get("q", "") for x in ex):
        ex.append({"q": Q["fr"][0], "a": Q["fr"][1]})
        json.dump(j, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("woordenboek", fn)
