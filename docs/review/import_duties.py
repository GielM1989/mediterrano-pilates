#!/usr/bin/env python3
"""Sitebreed: invoerbtw, invoerrechten en inklaringskosten buiten de EU zijn altijd voor de ontvanger.

Klantbesluit 04-11-2026: "de invoer-btw buiten Europa zoals Zwitserland en het VK is nooit voor ons;
geef dat altijd duidelijk aan op mijn site."

Werkt op: alle verzend- en verborgen-kostenvragen (zichtbaar + FAQPage-JSON-LD) in alle talen,
de feitenblokken, de juridische pagina's, llms.txt en de Franse woordenboeken (zodat een
herbouw van /fr/ de tekst behoudt). Idempotent.
Gebruik: python3 docs/review/import_duties.py   (vanuit de repo-root)
"""
import glob, html, json, re

STD = {
    "es": "Para envíos fuera de la UE, como a Suiza, al Reino Unido o a Noruega, el IVA de importación, los aranceles y los gastos de aduana corren siempre a cargo del destinatario.",
    "en": "For deliveries outside the EU, such as to Switzerland, the UK or Norway, import VAT, duties and customs clearance costs are always paid by the recipient.",
    "de": "Bei Lieferungen in Länder außerhalb der EU, etwa in die Schweiz, nach Großbritannien oder Norwegen, trägt der Empfänger immer die Einfuhrumsatzsteuer, Zölle und Verzollungskosten.",
    "nl": "Bij leveringen buiten de EU, zoals naar Zwitserland, het Verenigd Koninkrijk of Noorwegen, zijn invoer-btw, invoerrechten en inklaringskosten altijd voor rekening van de ontvanger.",
    "fr": "Pour les livraisons hors de l'Union européenne, par exemple vers la Suisse, le Royaume-Uni ou la Norvège, la TVA à l'importation, les droits de douane et les frais de dédouanement sont toujours à la charge du destinataire.",
}
# oude, zwakkere zinnen die verdwijnen (met voorafgaande spatie)
OLD = [
    " For UK orders, import VAT and duties may apply.",
    " Bei Lieferungen in die Schweiz trägt der Empfänger die Einfuhrumsatzsteuer und die Verzollungskosten, sofern im Angebot nichts anderes steht.",
    " Pour la Suisse, la TVA à l'importation et les frais de dédouanement restent à la charge du destinataire, sauf mention contraire dans le devis.",
    " Pour la Suisse, la TVA à l'importation (8,1 %) et les frais de dédouanement sont à la charge du destinataire, sauf mention contraire dans le devis.",
    " Pour la Suisse, la TVA à l'importation (8,1 %) et les frais de dédouanement sont à la charge du destinataire, sauf mention contraire dans le devis.",
]
# vragen waarvan het antwoord de zin moet bevatten
Q_KEYS = ["Enviáis fuera", "Hacéis envíos", "costes ocultos", "Do you ship", "hidden costs",
          "Versendet ihr", "Liefert ihr", "Leveren jullie", "Verzenden jullie", "Is de verzending gratis",
          "verborgen kosten", "Livrez-vous", "frais cachés", "coûts cachés"]


def lang_of(path):
    m = re.match(r"site/(en|de|nl|fr)/", path)
    return m.group(1) if m else "es"


def plain(t):
    return html.unescape(re.sub(r"<[^>]+>", "", t)).replace(" ", " ")


def transform(ans, lang):
    new = ans
    for o in OLD:
        new = new.replace(o, "").replace(o.replace(" ", "&nbsp;", 0), "")
    new = new.replace(" Pour la Suisse, la TVA à l'importation (8,1&nbsp;%) et les frais de dédouanement sont à la charge du destinataire, sauf mention contraire dans le devis.", "")
    if STD[lang] not in plain(new):
        new = new.rstrip() + " " + STD[lang]
    return new


def fix_faqs(s, lang):
    pat = re.compile(r'(<summary><span class="qn">\d+</span>)(.*?)(</summary>\s*<p>)(.*?)(</p>)', re.S)
    changes = []
    def rep(m):
        q = plain(m.group(2))
        if not any(k in q for k in Q_KEYS):
            return m.group(0)
        a = m.group(4)
        na = transform(a, lang)
        if na != a:
            changes.append((plain(a), plain(na)))
        return m.group(1) + m.group(2) + m.group(3) + na + m.group(5)
    s = pat.sub(rep, s)
    for old, new in changes:
        oj = json.dumps(old, ensure_ascii=False)[1:-1]
        nj = json.dumps(new, ensure_ascii=False)[1:-1]
        if oj in s:
            s = s.replace(oj, nj)
        else:
            # JSON-LD kan het antwoord met andere spaties/escapes hebben: zoek genormaliseerd
            for mm in re.finditer(r'"text":\s*"((?:[^"\\]|\\.)*)"', s):
                if json.loads('"' + mm.group(1) + '"').replace(" ", " ").strip() == old.strip():
                    s = s[:mm.start(1)] + nj + s[mm.end(1):]
                    break
            else:
                print("   JSON-LD niet gevonden:", old[:70])
    return s, len(changes)


BLOCK_FIXES = [
    # Duitse feitenblokken
    ("Gratisversand in ganz Europa, auch nach Deutschland, Österreich und in die Schweiz. Mediterrano Pilates ist eine Marke der Ecomtierra Group SL (Spanien).",
     "Gratisversand in ganz Europa, auch nach Deutschland, Österreich und in die Schweiz. Außerhalb der EU, etwa in der Schweiz, trägt der Empfänger immer Einfuhrumsatzsteuer, Zölle und Verzollungskosten. Mediterrano Pilates ist eine Marke der Ecomtierra Group SL (Spanien)."),
    # Franse feitenblokken
    ("Livraison gratuite dans toute l'Europe, y compris en France, en Belgique, au Luxembourg et en Suisse. Mediterrano Pilates est une marque d'Ecomtierra Group SL (Espagne).",
     "Livraison gratuite dans toute l'Europe, y compris en France, en Belgique, au Luxembourg et en Suisse. Hors de l'Union européenne, comme en Suisse, la TVA à l'importation, les droits de douane et les frais de dédouanement sont toujours à la charge du destinataire. Mediterrano Pilates est une marque d'Ecomtierra Group SL (Espagne)."),
]

LEGAL_FIXES = {
    "site/legal.html": [("Los posibles aranceles o impuestos de importación en el país de destino corren por cuenta del cliente.",
                         "Los posibles aranceles o impuestos de importación en el país de destino corren por cuenta del cliente. En envíos fuera de la UE, como a Suiza, al Reino Unido o a Noruega, el IVA de importación, los aranceles y los gastos de aduana corren siempre a cargo del cliente.")],
    "site/en/legal.html": [("For orders to the United Kingdom, this includes import VAT and any customs duties.",
                            "For deliveries outside the EU, such as to Switzerland, the United Kingdom or Norway, import VAT, duties and customs clearance costs are always paid by the customer.")],
    "site/de/legal.html": [("Etwaige Zölle oder Einfuhrabgaben im Bestimmungsland trägt der Kunde.",
                            "Bei Lieferungen in Länder außerhalb der EU, etwa in die Schweiz, nach Großbritannien oder Norwegen, trägt der Kunde immer die Einfuhrumsatzsteuer, Zölle und Verzollungskosten.")],
    "site/nl/legal.html": [("Eventuele invoerrechten of importbelastingen in het land van bestemming zijn voor rekening van de klant.",
                            "Eventuele invoerrechten of importbelastingen in het land van bestemming zijn voor rekening van de klant. Bij leveringen buiten de EU, zoals naar Zwitserland, het Verenigd Koninkrijk of Noorwegen, zijn invoer-btw, invoerrechten en inklaringskosten altijd voor rekening van de klant.")],
    "site/fr/legal.html": [(", sauf accord contraire indiqué dans le devis.", ", dans tous les cas."),
                           ("Les éventuels droits de douane et taxes à l'importation dans le pays de destination sont à la charge du client.",
                            "Les éventuels droits de douane et taxes à l'importation dans le pays de destination sont à la charge du client. Pour les livraisons hors de l'Union européenne, par exemple vers la Suisse, le Royaume-Uni ou la Norvège, la TVA à l'importation, les droits de douane et les frais de dédouanement sont toujours à la charge du client.")],
    "docs/review/fr/build_legal_fr.py": [(", sauf accord contraire indiqué dans le devis.", ", dans tous les cas."),
                           ("Les éventuels droits de douane et taxes à l'importation dans le pays de destination sont à la charge du client.",
                            "Les éventuels droits de douane et taxes à l'importation dans le pays de destination sont à la charge du client. Pour les livraisons hors de l'Union européenne, par exemple vers la Suisse, le Royaume-Uni ou la Norvège, la TVA à l'importation, les droits de douane et les frais de dédouanement sont toujours à la charge du client.")],
    "site/llms.txt": [("(for UK orders, import VAT and duties may apply)",
                       "(outside the EU, for example Switzerland, the UK or Norway, import VAT, duties and customs clearance costs are always paid by the recipient)")],
}


def apply_pairs(path, pairs):
    s = open(path, encoding="utf-8").read(); o = s
    for a, b in pairs:
        if b in s:
            continue
        if a not in s:
            print("   niet gevonden in", path, ":", a[:60]); continue
        s = s.replace(a, b)
    if s != o:
        open(path, "w", encoding="utf-8").write(s)
    return s != o


def fr_dicts():
    """Zelfde transformatie op de Franse woordenboekwaarden (bron van /fr/)."""
    n = 0
    for f in glob.glob("docs/review/fr/dict_*.json"):
        d = json.load(open(f, encoding="utf-8"))
        def walk(v):
            nonlocal n
            if isinstance(v, str):
                if any(o.strip() in v for o in OLD) or "sauf mention contraire dans le devis" in v:
                    n += 1
                    return transform(v, "fr")
                for a, b in BLOCK_FIXES[1:]:
                    if a in v and b not in v:
                        n += 1
                        v = v.replace(a, b)
                return v
            if isinstance(v, list):
                return [walk(x) for x in v]
            if isinstance(v, dict):
                return {k: walk(x) for k, x in v.items()}
            return v
        nd = walk(d)
        if nd != d:
            json.dump(nd, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return n


def main():
    total = 0
    for f in sorted(glob.glob("site/**/*.html", recursive=True)):
        s = open(f, encoding="utf-8").read(); o = s
        s, n = fix_faqs(s, lang_of(f))
        for a, b in BLOCK_FIXES:
            if a in s and b not in s:
                s = s.replace(a, b)
        if s != o:
            open(f, "w", encoding="utf-8").write(s); total += 1
            print(f"{f}: {n} antwoorden")
    for p, pairs in LEGAL_FIXES.items():
        if apply_pairs(p, pairs):
            print(p, ": juridisch/llms bijgewerkt")
    print("Franse woordenboekwaarden aangepast:", fr_dicts())
    print("pagina's gewijzigd:", total)


if __name__ == "__main__":
    main()
