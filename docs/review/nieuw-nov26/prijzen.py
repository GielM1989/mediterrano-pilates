# -*- coding: utf-8 -*-
"""Adviesprijs sokken als bandbreedte op alle pagina's (klantbesluit 26-11-2026).
IT/ES 14,95–17,95 €; DE/NL/EN/FR 17,95–19,95 €. Marges per land met de eigen btw.
Werkwijze: per prijsvermelding wordt het tekststuk tussen twee grenzen (tag, aanhalingsteken of zinseinde)
bekeken. Gaat het over de sokkenprijs in lopende tekst, dan worden prijs, marge, percentage en het
totaal voor 50 paar door de bandbreedte vervangen. Losse tabelcellen, kassabonnen en rekenhulpen zijn
voorbeelden en worden apart behandeld (bij IT met 17,95 €). Tote-zinnen worden overgeslagen.
"""
import os, re, sys, glob
SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'site'))
NB = r'(?:\s|&nbsp;| )?'

CFG = {
 'it': dict(dirs=['it'], price=r'19,95' + NB + '€', prange='14,95–17,95 €',
            rep=[(r'9,40' + NB + '€', '5,30–7,76 €'), (r'≈' + NB + r'57' + NB + '%', '≈43–53%'), (r'circa il 57' + NB + '%', 'circa il 43–53%'),
                 (r'\(57' + NB + r'%\)', '(43–53%)'), (r'intorno al 57' + NB + '%', 'intorno al 43–53%'), (r'470,12' + NB + '€', '265–388 €')]),
 'es': dict(dirs=None, price=r'17,95' + NB + '€', prange='14,95–17,95 €',
            rep=[(r'7,88' + NB + '€', '5,41–7,88 €'), (r'≈' + NB + r'53' + NB + '%', '≈44–53%'), (r'\(53' + NB + r'%\)', '(44–53%)'), (r'un 53' + NB + '%', 'un 44–53%'),
                 (r'394,24' + NB + '€', '270–394 €')]),
 'en': dict(dirs=['en'], price=r'€' + NB + r'19\.95', prange='€17.95–19.95',
            rep=[(r'€' + NB + r'9\.54', '€7.88–9.54'), (r'≈' + NB + r'58' + NB + '%', '≈53–58%'), (r'\(58' + NB + r'%\)', '(53–58%)'), (r'around 58' + NB + '%', 'around 53–58%'),
                 (r'€' + NB + r'476\.88', '€394–477'), (r'€' + NB + r'477(?![\d.])', '€394–477')]),
 'de': dict(dirs=['de'], price=r'19,95' + NB + '€', prange='17,95–19,95 €',
            rep=[(r'9,81' + NB + '€', '8,13–9,81 €'), (r'≈' + NB + r'59' + NB + '%', '≈54–59 %'), (r'\(59' + NB + r'%\)', '(54–59 %)'), (r'rund 59' + NB + '%', 'rund 54–59 %'),
                 (r'490,35' + NB + '€', '407–490 €'), (r'490,50' + NB + '€', '407–490 €')]),
 'nl': dict(dirs=['nl'], price=r'€' + NB + r'19,95', prange='€ 17,95–19,95',
            rep=[(r'€' + NB + r'9,54', '€ 7,88–9,54'), (r'≈' + NB + r'58' + NB + '%', '≈53–58%'), (r'\(58' + NB + r'%\)', '(53–58%)'), (r'ongeveer 58' + NB + '%', 'ongeveer 53–58%'),
                 (r'€' + NB + r'476,88', '€ 394–477'), (r'€' + NB + r'16,49', '€ 14,83–16,49')]),
 'fr': dict(dirs=['fr'], price=r'19,95' + NB + '€', prange='17,95–19,95&nbsp;€',
            rep=[(r'9,68' + NB + '€', '8,01–9,68&nbsp;€'), (r'≈' + NB + r'58' + NB + '%', '≈54–58&nbsp;%'), (r'\(58' + NB + r'%\)', '(54–58&nbsp;%)'), (r'environ 58' + NB + '%', 'environ 54–58&nbsp;%'),
                 (r'483,75' + NB + '€', '400–484&nbsp;€')]),
}
TOTE = re.compile(r'tote|tasche|Tasche|bag|Bag|sac |borsa|bolsa|Sol\b', re.I)


def bounds(t, s, e):
    a = max(t.rfind(c, 0, s) for c in '<>"')
    m = [m.end() for m in re.finditer(r'(?<!\d)[.;!?](?=\s)', t[a:s])]
    a = a + (m[-1] if m else 0)
    ends = [i for i in (t.find(c, e) for c in '<"') if i != -1]
    b = min(ends) if ends else len(t)
    m2 = re.search(r'(?<!\d)[.!?](?=\s)', t[e:b])
    if m2:
        b = e + m2.end()
    return a, b


def run(lg, files=None):
    c = CFG[lg]; pr = re.compile(c['price']); changed = {}
    if not files and c['dirs'] is None:
        files = [f for f in glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True)
                 if not re.match(r'(en|de|nl|fr|it)/', os.path.relpath(f, SITE))]
    files = files or [f for d in c['dirs'] for f in glob.glob(os.path.join(SITE, d, '**', 'index.html'), recursive=True)]
    for f in files:
        t = open(f, encoding='utf-8').read(); out = []; pos = 0; n = 0
        for m in pr.finditer(t):
            if m.start() < pos:
                continue
            if re.search(r'\d(?:\s|&nbsp;)?(?:–|-|à|a)(?:\s|&nbsp;)?(?:€(?:\s|&nbsp;)?)?$', t[max(0, m.start() - 14):m.start()]):
                continue  # al een bandbreedte
            a, b = bounds(t, m.start(), m.end())
            if a < pos:
                a = pos
            win = t[a:b]
            text_only = re.sub(r'\s', '', win)
            # losse cel / bon / rekenhulp: geen marge of zinscontext -> overslaan (apart)
            if TOTE.search(win) or not re.search(r'[A-Za-zÀ-ÿ]{4,}', win.replace(m.group(0), '')):
                continue
            new = pr.sub(c['prange'], win)
            for p, r in c['rep']:
                new = re.sub(p, r, new)
            out.append(t[pos:a]); out.append(new); pos = b; n += 1
        if n:
            out.append(t[pos:]); t = ''.join(out)
            open(f, 'w', encoding='utf-8').write(t); changed[os.path.relpath(f, SITE)] = n
    return changed


if __name__ == '__main__':
    for lg in sys.argv[1:] or CFG:
        ch = run(lg)
        print(lg, sum(ch.values()), 'in', len(ch), 'bestanden')
