"""Ronde 3 + terugdraaien tote-minimum (merk-en-feiten: tumblers/totes/ringen op offerte, geen vast minimum)."""
import glob
P = [
 ("Bij Mediterrano Pilates is de minimale bestelling 50 paar antislipsokken of 50 tote bags. Voor tumblers en pilatesringen maken we een offerte op maat.",
  "Bij Mediterrano Pilates is de minimale bestelling 50 paar antislipsokken. Voor tumblers, tote bags en pilatesringen maken we een offerte op maat."),
 ("Voor tote bags is het minimum 50 stuks. Voor tumblers en pilatesringen leggen we het aantal vast in de offerte.", "Voor tumblers, tote bags en pilatesringen leggen we het aantal vast in de offerte."),
 ("Voor antislipsokken 50 paar en voor tote bags 50 stuks. Voor tumblers en pilatesringen is er geen vast minimum:", "Voor antislipsokken 50 paar. Voor tumblers, tote bags en pilatesringen is er geen vast minimum:"),
 ("Tote bags vanaf 50 stuks; tumblers en pilatesringen op offerte.", "Tote bags, tumblers en pilatesringen op offerte."),
 ("Bei Mediterrano Pilates liegt die Mindestbestellmenge bei 50 Paar Stoppersocken und 50 Tote Bags. Für Tumbler und Pilates-Ringe gibt es keine feste Mindestmenge,",
  "Bei Mediterrano Pilates liegt die Mindestbestellmenge bei 50 Paar Stoppersocken. Für Tumbler, Tote Bags und Pilates-Ringe gibt es keine feste Mindestmenge,"),
 ("Votre commande arrive donc dans votre studio à la mi-décembre.", "Votre commande peut donc arriver dans votre studio à la mi-décembre."),
 ("un caña media, hasta por encima del tobillo,", "un calcetín de caña media, hasta por encima del tobillo,"),
 ("así que el pedido llega a tu estudio a mediados de diciembre.", "así que el pedido puede llegar a tu estudio a mediados de diciembre."),
 ("Approve later and it may still arrive in time, but we can no longer guarantee it.", "Approve later and it may still arrive in time, but that becomes less certain."),
 ("For the UK, as for other deliveries outside the EU such as Switzerland or Norway,", "For the UK, as for other destinations outside the EU, such as Switzerland or Norway,"),
]
files = glob.glob("site/**/*.html", recursive=True) + glob.glob("docs/review/**/*.py", recursive=True) + glob.glob("docs/review/**/*.json", recursive=True) + glob.glob("docs/review/**/*.html", recursive=True)
hits = {a: 0 for a, _ in P}
for f in files:
    if f.endswith("lang_fixes_round3.py"): continue
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in P:
        if a in s: hits[a] += s.count(a); s = s.replace(a, b)
    if s != o: open(f, "w", encoding="utf-8").write(s)
for a, n in hits.items(): print(n, a[:70])
