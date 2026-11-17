#!/usr/bin/env python3
"""Klantbesluit 16-11-2026: kleur = exact volgens Pantone (niet 'zo dicht mogelijk').
Past alle talen aan (site/*.html), plus de FR-bron en IT-teksten van de IT-build. Idempotent."""
import re, glob
R = [  # (regex, vervanging)
 # FR
 (r"au plus près de son code Pantone", "exactement d'après son code Pantone"),
 (r"au plus près du code Pantone", "exactement d'après le code Pantone"),
 (r"au plus près de votre code Pantone", "exactement d'après votre code Pantone"),
 (r"une couleur du produit au plus près de la vôtre", "une couleur du produit identique à la vôtre"),
 # ES
 (r"lo más cerca posible del código Pantone", "de forma exacta según el código Pantone"),
 (r"lo más cerca posible de su código Pantone", "de forma exacta según su código Pantone"),
 (r"lo más cercano posible al código Pantone", "exacto según el código Pantone"),
 # DE
 (r"Farbe so nah wie möglich an deiner Markenfarbe, abgestimmt auf den Pantone-Code, den Standard", "Farbe exakt auf deine Markenfarbe abgestimmt, per Pantone-Code, dem Standard"),
 (r"so nah wie möglich am Pantone-Code", "exakt nach Pantone-Code"),
 (r"und treffen deine Farbe so nah wie möglich", "und treffen deine Farbe exakt"),
 (r"so nah wie möglich ab\b", "exakt ab"),
 # NL
 (r"zo dicht mogelijk bij je Pantone-code", "exact volgens je Pantone-code"),
 # IT
 (r"il più vicino possibile al", "esattamente in base al"),
 (r"il più vicino possibile a quello", "identico a quello"),
 (r"nel colore più vicino al tuo", "nel tuo colore esatto"),
]
files = glob.glob("site/**/*.html", recursive=True) + glob.glob("docs/review/it/segs/*.txt") + glob.glob("docs/review/it/it/*.txt")
tot = 0
for f in files:
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in R:
        s, n = re.subn(a, b, s); tot += n
    if s != o: open(f, "w", encoding="utf-8").write(s)
print("vervangen:", tot)
