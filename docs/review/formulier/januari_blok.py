"""Januari-blok (tijdelijk): homepage (na de hero) en welkomstpakket-artikel (boven het formulier), 6 talen.
Verdwijnt vanzelf op 16-12-2026 (script in het blok); daarna kan het met --verwijder uit de HTML.
Idempotent. Gebruik: python3 docs/review/formulier/januari_blok.py [--verwijder]"""
import re, sys
ROOT = 'site'
START, END = '<!-- MP-JANUARI:start (tijdelijk, verdwijnt vanzelf op 16-12-2026) -->', '<!-- MP-JANUARI:end -->'
T = {
 '':   ('Para enero', '¿Alumnas nuevas en enero? Aprueba tu diseño antes del 15 de diciembre.',
        'Muchos estudios reciben alumnas nuevas en enero. La producción y la entrega tardan unas 4 semanas desde que apruebas y pagas el presupuesto. Si lo cierras antes del 15 de diciembre, tendrás tu pedido en el estudio hacia mediados de enero. El boceto es gratis y lo recibes en 24 horas.',
        'Pide tu boceto gratis', 'blog/pack-de-bienvenida-alumnas-nuevas-pilates'),
 'en': ('For January', 'New clients in January? Approve your design by 15 December.',
        'Many studios welcome new clients in January. Production and delivery take around 4 weeks once you have approved and paid the quote. If you do that by 15 December, your order will be in your studio by mid-January. The mockup is free and arrives within 24 hours.',
        'Request your free mockup', 'blog/welcome-pack-for-new-pilates-clients'),
 'de': ('Für Januar', 'Neue Kundinnen im Januar? Gib dein Design bis zum 15. Dezember frei.',
        'Viele Studios gewinnen im Januar neue Kundinnen. Produktion und Lieferung dauern etwa 4 Wochen, nachdem du das Angebot freigegeben und bezahlt hast. Erledigst du das bis zum 15. Dezember, ist deine Bestellung etwa Mitte Januar in deinem Studio. Das Mockup ist kostenlos und kommt innerhalb von 24 Stunden.',
        'Gratis-Mockup anfordern', 'blog/willkommenspaket-fuer-neue-kundinnen'),
 'nl': ('Voor januari', 'Nieuwe leden in januari? Keur je ontwerp goed vóór 15 december.',
        "Veel studio's krijgen in januari nieuwe leden. Productie en levering duren ongeveer 4 weken nadat je de offerte hebt goedgekeurd en betaald. Rond je dat af vóór 15 december, dan heb je je bestelling rond half januari in je studio. De mockup is gratis en krijg je binnen 24 uur.",
        'Vraag je gratis mockup aan', 'blog/welkomstpakket-nieuwe-pilatesleden'),
 'fr': ('Pour janvier', 'De nouvelles élèves en janvier&nbsp;? Validez votre design avant le 15&nbsp;décembre.',
        'Beaucoup de studios accueillent de nouvelles élèves en janvier. La production et la livraison prennent environ 4&nbsp;semaines après la validation et le paiement du devis. Si vous le faites avant le 15&nbsp;décembre, votre commande arrivera dans votre studio vers la mi-janvier. La maquette est gratuite et vous la recevez sous 24&nbsp;heures.',
        'Demandez votre maquette gratuite', 'blog/kit-de-bienvenue-nouveaux-eleves-pilates'),
 'it': ('Per gennaio', 'Nuove allieve a gennaio? Approva il tuo design entro il 15 dicembre.',
        "Molti studi accolgono nuove allieve a gennaio. Produzione e consegna richiedono circa 4 settimane dall'approvazione e dal pagamento del preventivo. Se lo fai entro il 15 dicembre, avrai il tuo ordine in studio verso metà gennaio. Il mockup è gratuito e lo ricevi entro 24 ore.",
        'Richiedi il tuo mockup gratuito', 'blog/kit-di-benvenuto-nuove-allieve-pilates'),
}
def block(k, h, p, btn):
    return (f'{START}\n<section class="sheet cream" id="januari">\n  <div class="wrap" style="padding-top:28px;padding-bottom:28px">\n'
      '    <div style="background:#fff;border:1.5px solid var(--line);border-left:6px solid var(--terra);border-radius:18px;padding:22px 24px;display:flex;flex-wrap:wrap;gap:16px 28px;align-items:center;justify-content:space-between">\n'
      '      <div style="flex:1 1 420px;min-width:0">\n'
      f'        <p style="margin:0 0 6px;font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--terra-2)">{k}</p>\n'
      f'        <h2 style="margin:0 0 8px;font-size:1.35rem;line-height:1.25;max-width:none">{h}</h2>\n'
      f'        <p style="margin:0;color:var(--ink);line-height:1.55">{p}</p>\n'
      '      </div>\n'
      f'      <a class="btn" href="#mockup-form" style="flex:0 1 auto;max-width:100%;white-space:normal;text-align:center">{btn}</a>\n'
      '    </div>\n  </div>\n'
      '  <script>(function(){var s=document.currentScript.closest("section");if(Date.now()>=Date.UTC(2026,11,16))s.remove();})();</script>\n'
      f'</section>\n{END}\n')
rm = '--verwijder' in sys.argv
for lang, (k, h, p, btn, art) in T.items():
    pre = f'{ROOT}/{lang + "/" if lang else ""}'
    for f, where in ((pre + 'index.html', 'home'), (pre + art + '/index.html', 'art')):
        t = open(f, encoding='utf-8').read(); o = t
        t = re.sub(r'\n?' + re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '\n', t, flags=re.S)
        if not rm:
            b = block(k, h, p, btn)
            if where == 'home':
                i = t.index('</header>') + len('</header>\n'); t = t[:i] + b + t[i:]
            else:
                i = t.index('<!-- MP-FORM:start'); t = t[:i] + b + t[i:]
        if t != o: open(f, 'w', encoding='utf-8').write(t); print('bijgewerkt', f)
