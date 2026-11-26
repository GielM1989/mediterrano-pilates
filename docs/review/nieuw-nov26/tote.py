# -*- coding: utf-8 -*-
"""Tote bag sitebreed: goedkoopste model Sol vanaf 7,45 € excl. btw (prijs bij 50 stuks), adviesprijs 14,95–19,95 €
(klantbesluit 26-11-2026). Marges per land met de eigen btw. Zinnen over de tote worden herschreven;
kassabonnen en tabellen krijgen het voorbeeld Sol 7,45 € → 19,95 €."""
import os, re, sys, glob
SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'site'))
N = r'(?:\s|&nbsp;| )?'
L = {
 'it': dict(m='4,80–8,90 €', pct='39–54%'), 'es': dict(m='4,91–9,04 €', pct='40–55%'),
 'en': dict(m='€4.91–9.04', pct='40–55%'), 'nl': dict(m='€ 4,91–9,04', pct='40–55%'),
 'de': dict(m='5,11–9,31 €', pct='41–56 %'), 'fr': dict(m='5,01–9,18&nbsp;€', pct='40–55&nbsp;%'),
}
KEY = re.compile(r'tote|tasche|bag|sac\b|borsa|bolsa', re.I)


def lang_of(rel):
    m = re.match(r'(en|de|nl|fr|it)/', rel)
    return m.group(1) if m else 'es'


def sent_bounds(t, s, e):
    a = max(t.rfind(c, 0, s) for c in '<>"')
    mm = [m.end() for m in re.finditer(r'(?<!\d)[.;!?](?=\s)', t[a:s])]
    a = a + (mm[-1] if mm else 0)
    ends = [i for i in (t.find(c, e) for c in '<"') if i != -1]
    b = min(ends) if ends else len(t)
    m2 = re.search(r'(?<!\d)[.!?](?=\s|$)', t[e:b])
    if m2:
        b = e + m2.end()
    return a, b


def fix_sentence(lg, w):
    c = L[lg]
    if lg == 'en':
        w = re.sub(r'€' + N + r'6\.50', '€7.45', w); w = re.sub(r'€' + N + r'15(?![\d.,])', '€14.95–19.95', w)
        w = re.sub(r'€' + N + r'5\.90', c['m'], w)
    elif lg == 'nl':
        w = re.sub(r'€' + N + r'6,50', '€ 7,45', w); w = re.sub(r'€' + N + r'15(?![\d,])', '€ 14,95–19,95', w)
        w = re.sub(r'€' + N + r'5,90', c['m'], w)
    else:
        sp = '&nbsp;' if '&nbsp;' in w else ' '
        w = re.sub(r'6,50' + N + '€', '7,45' + sp + '€', w); w = re.sub(r'(?<![\d,–])15' + N + '€', '14,95–19,95' + sp + '€', w)
        w = re.sub(r'(5,80|5,90|6,00|6,11)' + N + '€', c['m'], w)
    w = re.sub(r'\b(4[5-9])' + N + '%', c['pct'], w)
    return w


def run():
    tot = 0
    for f in glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True):
        rel = os.path.relpath(f, SITE); lg = lang_of(rel)
        t = open(f, encoding='utf-8').read(); o = t
        # JSON-LD van de tote-productpagina's
        if re.search(r'tote|stofftasche', rel, re.I):
            t = t.replace('"price": "6.50"', '"price": "7.45"')
        # kassabon / prijstabel: rij met Tote bag
        t = re.sub(r'(Tote bag</span><span class="rc-in">)(6,50(?:&nbsp;| )€|€(?:&nbsp;| )?6[.,]50)(</span><span class="rc-out">)(15(?:&nbsp;| )€|€(?:&nbsp;| )?15)',
                   lambda m: m.group(1) + m.group(2).replace('6,50', '7,45').replace('6.50', '7.45') + m.group(3) + m.group(4).replace('15', '19,95' if lg != 'en' else '19.95'), t)
        # zinnen
        out = []; pos = 0
        pat = re.compile(r'€' + N + r'6[.,]50(?!\d)|(?<![\d,.])6,50' + N + '€')
        for m in pat.finditer(t):
            if m.start() < pos:
                continue
            a, b = sent_bounds(t, m.start(), m.end())
            a = max(a, pos); w = t[a:b]
            if not KEY.search(w):
                # tabelcel in een rij met tote: kijk naar de rij
                row_s = t.rfind('<tr', 0, m.start()); row_e = t.find('</tr>', m.end())
                if row_s != -1 and row_e != -1 and KEY.search(t[row_s:row_e]) and row_e - row_s < 1500:
                    row = t[row_s:row_e]
                    row2 = re.sub(r'>(\s*)(6,50(?:&nbsp;| )?€|€(?:&nbsp;| )?6[.,]50)(\s*)<', lambda x: '>' + x.group(1) + x.group(2).replace('6,50', '7,45').replace('6.50', '7.45') + x.group(3) + '<', row)
                    row2 = re.sub(r'>(\s*)(≈?\s*15(?:&nbsp;| )?€|€(?:&nbsp;| )?15|≈?€15)(\s*)<', lambda x: '>' + x.group(1) + ('€14.95–19.95' if lg == 'en' else ('€ 14,95–19,95' if lg == 'nl' else '14,95–19,95 €')) + x.group(3) + '<', row2)
                    row2 = re.sub(r'(≈?\s*)(5,80|5,90|6,00|6,11)(?:&nbsp;| )?€(\s*\(\d\d(?:&nbsp;| )?%\))?|€5\.90(\s*\(\d\d%\))?|€(?:&nbsp;| )?5,90(\s*\(\d\d%\))?',
                                  lambda x: '≈' + L[lg]['m'] + ' (' + L[lg]['pct'] + ')', row2)
                    out.append(t[pos:row_s]); out.append(row2); pos = row_e
                continue
            out.append(t[pos:a]); out.append(fix_sentence(lg, w)); pos = b
        out.append(t[pos:]); t = ''.join(out)
        # welkomstpakket-sommen (sokken + tote; + tumbler)
        t = re.sub(r'13,45', '14,40', t); t = re.sub(r'24,45', '25,40', t)
        t = re.sub(r'€13\.45', '€14.40', t); t = re.sub(r'€24\.45', '€25.40', t)
        if t != o:
            open(f, 'w', encoding='utf-8').write(t); tot += 1
    print('tote: bestanden bijgewerkt', tot)


if __name__ == '__main__':
    run()
