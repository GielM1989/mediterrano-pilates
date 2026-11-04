"""Klantbesluit 04-11-2026: tote bags minimaal 50 stuks; tumblers en pilatesringen op offerte. Alle talen. Idempotent."""
import glob
P = [
 # NL
 ("Tote bags, tumblers en pilatesringen op offerte.", "Tote bags vanaf 50 stuks; tumblers en pilatesringen op offerte."),
 ("Tote bags, tumblers en ringen op offerte.", "Tote bags vanaf 50 stuks; tumblers en ringen op offerte."),
 ("Tumblers, tote bags en pilatesringen op offerte.", "Tote bags vanaf 50 stuks; tumblers en pilatesringen op offerte."),
 ("Voor tote bags, tumblers en pilatesringen leggen we het aantal vast in de offerte.", "Voor tote bags is het minimum 50 stuks; voor tumblers en pilatesringen leggen we het aantal vast in de offerte."),
 ("Voor tote bags, tumblers en ringen leggen we het aantal vast in de offerte.", "Voor tote bags is het minimum 50 stuks; voor tumblers en ringen leggen we het aantal vast in de offerte."),
 ("Voor tumblers, tote bags en pilatesringen is er geen vast minimum:", "Voor tote bags is het minimum 50 stuks. Voor tumblers en pilatesringen is er geen vast minimum:"),
 ("Voor tumblers, tote bags en pilatesringen leggen we het aantal vast in de offerte.", "Voor tote bags is het minimum 50 stuks; voor tumblers en pilatesringen leggen we het aantal vast in de offerte."),
 ("Voor tumblers, tote bags en pilatesringen maken we een offerte op maat, afhankelijk van het aantal.", "Voor tote bags is het minimum 50 stuks; voor tumblers en pilatesringen maken we een offerte op maat, afhankelijk van het aantal."),
 ("Voor tumblers, tote bags en pilatesringen maken we een offerte op maat.", "Voor tote bags is het minimum 50 stuks; voor tumblers en pilatesringen maken we een offerte op maat."),
 ("Voor tumblers, tote bags en pilatesringen staat het aantal in de offerte.", "Voor tote bags is het minimum 50 stuks; voor tumblers en pilatesringen staat het aantal in de offerte."),
 ("Voor tumblers, tote bags en ringen laat je ons weten aan hoeveel stuks je denkt, en we maken een offerte op maat.", "Voor tote bags is het minimum 50 stuks. Voor tumblers en ringen laat je ons weten aan hoeveel stuks je denkt, en we maken een offerte op maat."),
 ("voor tumblers, tote bags en pilatesringen krijg je een offerte op maat, afhankelijk van het aantal.", "voor tote bags is het minimum 50 stuks en voor tumblers en pilatesringen krijg je een offerte op maat, afhankelijk van het aantal."),
 ("voor tumblers, tote bags en pilatesringen krijg je een offerte op maat.", "voor tote bags is het minimum 50 stuks en voor tumblers en pilatesringen krijg je een offerte op maat."),
 ("voor tumblers, tote bags en pilatesringen staat het aantal in de offerte.", "voor tote bags is het minimum 50 stuks en voor tumblers en pilatesringen staat het aantal in de offerte."),
 # DE
 ("Bei Tote Bags, Tumblern und Ringen wird die Menge im Angebot festgelegt.", "Tote Bags gibt es ab 50 Stück; bei Tumblern und Ringen wird die Menge im Angebot festgelegt."),
 ("Bei Tumblern, Stofftaschen und Pilates-Ringen sagst du uns einfach, an wie viele Stück du denkst, und wir erstellen dir ein individuelles Angebot.", "Stofftaschen gibt es ab 50 Stück. Bei Tumblern und Pilates-Ringen sagst du uns einfach, an wie viele Stück du denkst, und wir erstellen dir ein individuelles Angebot."),
 ("Für Tote Bags, Tumbler und Ringe wird die Menge individuell im Angebot festgelegt.", "Tote Bags gibt es ab 50 Stück; für Tumbler und Ringe wird die Menge individuell im Angebot festgelegt."),
 ("Für Trinkflaschen, Taschen und Pilates-Ringe erstellen wir ein individuelles Angebot je nach Menge.", "Tote Bags gibt es ab 50 Stück; für Tumbler und Pilates-Ringe erstellen wir ein individuelles Angebot je nach Menge."),
 ("Für Trinkflaschen, Taschen und Ringe sag uns einfach, an wie viele Stück du denkst, und wir erstellen ein individuelles Angebot.", "Tote Bags gibt es ab 50 Stück. Für Tumbler und Ringe sag uns einfach, an wie viele Stück du denkst, und wir erstellen ein individuelles Angebot."),
 ("Für Tumbler, Tote Bags und Pilates-Ringe gibt es keine feste Mindestmenge, die Menge legen wir im Angebot fest.", "Tote Bags gibt es ab 50 Stück. Für Tumbler und Pilates-Ringe gibt es keine feste Mindestmenge, die Menge legen wir im Angebot fest."),
 ("Für Tumbler, Tote Bags und Ringe wird die Menge individuell im Angebot festgelegt.", "Tote Bags gibt es ab 50 Stück; für Tumbler und Ringe wird die Menge individuell im Angebot festgelegt."),
 ("Für Tumbler, Tote Bags und Ringe wird die Menge im Angebot festgelegt.", "Tote Bags gibt es ab 50 Stück; für Tumbler und Ringe wird die Menge im Angebot festgelegt."),
 ("Tote Bags, Tumbler und Ringe nach individuellem Angebot.", "Tote Bags ab 50 Stück; Tumbler und Ringe nach individuellem Angebot."),
 ("Tumbler, Tote Bags und Ringe nach individuellem Angebot.", "Tote Bags ab 50 Stück; Tumbler und Ringe nach individuellem Angebot."),
 ("die Mindestbestellung bei Stoppersocken liegt bei 50 Paar, mit individuellem Angebot für Trinkflaschen, Taschen und Ringe;", "die Mindestbestellung liegt bei 50 Paar Stoppersocken und 50 Tote Bags, mit individuellem Angebot für Tumbler und Ringe;"),
 ("die Mindestbestellung für Stoppersocken liegt bei 50 Paar, für Trinkflaschen, Taschen und Ringe wird ein individuelles Angebot je nach Menge erstellt.", "die Mindestbestellung liegt bei 50 Paar Stoppersocken und 50 Tote Bags, für Tumbler und Ringe wird ein individuelles Angebot je nach Menge erstellt."),
 ("für Tumbler, Tote Bags und Ringe wird die Menge im Angebot festgelegt.", "für Tote Bags gilt ein Minimum von 50 Stück, für Tumbler und Ringe wird die Menge im Angebot festgelegt."),
 # EN
 ("For tumblers, tote bags and Pilates rings, just tell us roughly how many you have in mind and we'll put together a tailored quote.", "Tote bags start at 50 units. For tumblers and Pilates rings, just tell us roughly how many you have in mind and we'll put together a tailored quote."),
 ("For tumblers, tote bags and Pilates rings, the quantity is set in your quote.", "Tote bags start at 50 units; for tumblers and Pilates rings, the quantity is set in your quote."),
 ("For tumblers, tote bags and Pilates rings, we put together a tailored quote based on quantity.", "Tote bags start at 50 units. For tumblers and Pilates rings, we put together a tailored quote based on quantity."),
 ("Mediterrano Pilates works with a minimum order of 50 pairs for grip socks, and a tailored quote for tumblers, tote bags and Pilates rings.", "Mediterrano Pilates has a minimum order of 50 pairs for grip socks and 50 units for tote bags, with a tailored quote for tumblers and Pilates rings."),
 ("Tote bags, tumblers and rings quoted individually.", "Tote bags from 50 units; tumblers and rings quoted individually."),
 ("Tumblers, tote bags and rings quoted individually.", "Tote bags from 50 units; tumblers and rings quoted individually."),
 ("for tumblers, tote bags and Pilates rings, the quantity is set in your quote.", "tote bags start at 50 units, and for tumblers and Pilates rings the quantity is set in your quote."),
 ("for tumblers, tote bags and Pilates rings, we prepare a quote based on the quantity you need.", "tote bags start at 50 units, and for tumblers and Pilates rings we prepare a quote based on the quantity you need."),
 ("the minimum order for grip socks is 50 pairs, with a tailored quote for tumblers, tote bags and Pilates rings;", "the minimum order is 50 pairs for grip socks and 50 units for tote bags, with a tailored quote for tumblers and Pilates rings;"),
 # FR (geen nieuwe ' ;' om &nbsp;-problemen te vermijden)
 ("Mediterrano Pilates travaille avec un minimum de commande de 50 paires pour les chaussettes antidérapantes, et sur devis pour les gourdes isothermes, les tote bags et les anneaux de Pilates.", "Chez Mediterrano Pilates, le minimum de commande est de 50 paires pour les chaussettes antidérapantes et de 50 unités pour les tote bags. Les gourdes isothermes et les anneaux de Pilates sont sur devis."),
 ("Pour les gourdes isothermes, les tote bags et les anneaux de Pilates, indiquez-nous le nombre d'unités que vous avez en tête et nous vous préparons un devis sur mesure.", "Pour les tote bags, le minimum est de 50 unités. Pour les gourdes isothermes et les anneaux de Pilates, indiquez-nous le nombre d'unités que vous avez en tête et nous vous préparons un devis sur mesure."),
 ("Pour les gourdes isothermes, les tote bags et les anneaux de Pilates, nous préparons un devis sur mesure selon la quantité.", "Pour les tote bags, le minimum est de 50 unités. Pour les gourdes isothermes et les anneaux de Pilates, nous préparons un devis sur mesure selon la quantité."),
 ("Pour les gourdes isothermes, les tote bags et les anneaux, la quantité est définie dans le devis.", "Pour les tote bags, le minimum est de 50 unités. Pour les gourdes isothermes et les anneaux, la quantité est définie dans le devis."),
 ("Pour les tote bags, les gourdes isothermes et les anneaux, la quantité est définie dans le devis.", "Pour les tote bags, le minimum est de 50 unités. Pour les gourdes isothermes et les anneaux, la quantité est définie dans le devis."),
 ("Pour les tote bags, les gourdes isothermes et les anneaux, la quantité est fixée dans le devis.", "Pour les tote bags, le minimum est de 50 unités. Pour les gourdes isothermes et les anneaux, la quantité est fixée dans le devis."),
 ("Gourdes isothermes, tote bags et anneaux sur devis.", "Tote bags dès 50 unités, gourdes isothermes et anneaux sur devis."),
 ("Tote bags, gourdes isothermes et anneaux sur devis.", "Tote bags dès 50 unités, gourdes isothermes et anneaux sur devis."),
 ("le minimum de commande est de 50 paires pour les chaussettes, avec un devis sur mesure pour les gourdes isothermes, les tote bags et les anneaux", "le minimum de commande est de 50 paires pour les chaussettes et de 50 unités pour les tote bags, avec un devis sur mesure pour les gourdes isothermes et les anneaux"),
 ("le minimum de commande est de 50 paires pour les chaussettes, et pour les gourdes isothermes, les tote bags et les anneaux nous préparons un devis sur mesure selon la quantité.", "le minimum de commande est de 50 paires pour les chaussettes et de 50 unités pour les tote bags, et pour les gourdes isothermes et les anneaux nous préparons un devis sur mesure selon la quantité."),
 ("pour les gourdes isothermes, les tote bags et les anneaux, la quantité est définie dans le devis.", "pour les tote bags, le minimum est de 50 unités, et pour les gourdes isothermes et les anneaux, la quantité est définie dans le devis."),
]
def var(a, b):
    out = [(a, b)]
    for x, y in list(out):
        if "'" in x: out += [(x.replace("'", "&#39;"), y.replace("'", "&#39;")), (x.replace("'", "’"), y.replace("'", "’"))]
    return out
files = (glob.glob("site/**/*.html", recursive=True) + ["site/llms.txt"] + glob.glob("docs/review/fr/*.json") + glob.glob("docs/review/fr/*.py")
         + ["docs/review/dennl/content.py", "docs/review/nl_parity.py", "docs/review/nl_barre/body_nl.html", "docs/review/nl_barre/build_nl_barre.py"])
hits = {a: 0 for a, _ in P}
for f in files:
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in P:
        for x, y in var(a, b):
            if x in s: hits[a] += s.count(x); s = s.replace(x, y)
    if s != o: open(f, "w", encoding="utf-8").write(s)
for a, n in hits.items():
    if not n: print("0x:", a[:80])
