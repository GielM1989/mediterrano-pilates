"""Cookiebeleid: opslag mp_first_touch vermelden (6 talen, idempotent)."""
import sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else 'site'
P = {
 'legal.html': ('para no volver a preguntarte.',
   'para no volver a preguntarte. Si aceptas las cookies analíticas, guardamos también en tu navegador por qué canal llegaste por primera vez a la web, por ejemplo Google o un anuncio (almacenamiento local, clave mp_first_touch, durante 30 días como máximo), para saber qué canal funciona; si las rechazas o retiras tu consentimiento, se borra.'),
 'en/legal.html': ('remembers your language choice. Functional.</li>\n',
   'remembers your language choice. Functional.</li>\n        <li><b>mp_first_touch</b> (local storage in your browser): remembers how you first reached the site (for example via Google or an ad), so that we know which channel works. Retention: up to 30 days. Only with consent; deleted if you decline or withdraw your consent.</li>\n'),
 'de/legal.html': ('merkt sich deine Sprachauswahl. Funktional.</li>\n',
   'merkt sich deine Sprachauswahl. Funktional.</li>\n        <li><b>mp_first_touch</b> (lokaler Speicher deines Browsers): merkt sich, wie du zum ersten Mal auf die Website gekommen bist (zum Beispiel über Google oder eine Anzeige), damit wir wissen, welcher Kanal funktioniert. Speicherdauer: höchstens 30 Tage. Nur mit Einwilligung; wird gelöscht, wenn du ablehnst oder deine Einwilligung widerrufst.</li>\n'),
 'nl/legal.html': ('onthoudt je taalkeuze. Functioneel.</li>\n',
   'onthoudt je taalkeuze. Functioneel.</li>\n        <li><b>mp_first_touch</b> (lokale opslag in je browser): onthoudt hoe je de site voor het eerst bereikte (bijvoorbeeld via Google of een advertentie), zodat we weten welk kanaal werkt. Bewaartermijn: maximaal 30 dagen. Alleen met toestemming; wordt gewist als je weigert of je toestemming intrekt.</li>\n'),
 'fr/legal.html': ("<tr><td>Mesure d'audience</td><td>Google Analytics 4 (Google Ireland Ltd.)</td><td>Requis</td></tr>\n",
   "<tr><td>Mesure d'audience</td><td>Google Analytics 4 (Google Ireland Ltd.)</td><td>Requis</td></tr>\n          <tr><td>Mesure d'audience&nbsp;: canal de votre première visite (par exemple Google ou une annonce), 30&nbsp;jours au maximum</td><td>Stockage local de votre navigateur (clé mp_first_touch)</td><td>Requis</td></tr>\n"),
 'it/legal.html': ('cookie _ga e _ga_*, fino a 2 anni)</td><td>Richiesto</td></tr>\n',
   'cookie _ga e _ga_*, fino a 2 anni)</td><td>Richiesto</td></tr>\n          <tr><td>Statistica: canale della tua prima visita (ad esempio Google o un annuncio), al massimo 30 giorni</td><td>Memoria locale del tuo browser (chiave mp_first_touch)</td><td>Richiesto</td></tr>\n'),
}
for f, (a, b) in P.items():
    p = f'{ROOT}/{f}'; t = open(p, encoding='utf-8').read()
    if 'mp_first_touch' in t: print('al gedaan', p); continue
    assert t.count(a) == 1, (p, t.count(a))
    open(p, 'w', encoding='utf-8').write(t.replace(a, b)); print('bijgewerkt', p)
