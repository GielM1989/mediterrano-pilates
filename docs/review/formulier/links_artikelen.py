"""Interne links naar de twee artikelen met de minste links (gids + tote) in de linkregel onderaan elke pagina."""
import re, sys, glob
ROOT = sys.argv[1] if len(sys.argv) > 1 else 'site'
A = {
 '':   [('/blog/calcetines-antideslizantes-para-pilates/', 'Calcetines antideslizantes para pilates'),
        ('/blog/tote-bag-personalizada-estudio-pilates-yoga/', 'Tote bag personalizada para tu estudio')],
 'en': [('/en/blog/branded-grip-socks-for-your-studio/', 'Branded grip socks for your studio'),
        ('/en/blog/custom-tote-bags-with-studio-logo/', 'Custom tote bags with your studio logo')],
 'de': [('/de/blog/socken-mit-logo-besticken-lassen/', 'Pilates-Socken mit Logo besticken lassen'),
        ('/de/blog/stofftasche-mit-logo-fuer-dein-studio/', 'Stofftasche mit Logo für dein Studio')],
 'nl': [('/nl/blog/antislipsokken-voor-pilates/', 'Antislipsokken voor pilates'),
        ('/nl/blog/tote-bag-met-logo-voor-je-studio/', 'Tote bag met logo voor je studio')],
 'fr': [('/fr/blog/chaussettes-de-pilates-personnalisees/', 'Chaussettes de pilates personnalisées'),
        ('/fr/blog/tote-bag-personnalise-logo-studio-pilates/', 'Tote bag personnalisé avec votre logo')],
 'it': [('/it/blog/calze-pilates-personalizzate/', 'Calze da pilates personalizzate'),
        ('/it/blog/tote-bag-personalizzata-logo-studio-pilates/', 'Tote bag personalizzata con il tuo logo')],
}
STYLE = 'color:var(--cream);text-decoration:underline'
n = 0
for lang, arts in A.items():
    base = f'{ROOT}/{lang + "/" if lang else ""}'
    for f in sorted(glob.glob(base + '**/index.html', recursive=True)):
        rel = f[len(ROOT):]
        if not lang and re.match(r'/(en|de|nl|fr|it)/', rel): continue
        t = open(f, encoding='utf-8').read()
        m = re.search(r'(<!-- MP-FORM:links -->.*?)(</p>)(\s*</div></section><!-- /MP-FORM:links -->)', t, re.S)
        if not m: continue
        par = m.group(1); add = ''
        self_url = rel.replace('index.html', '')
        for url, label in arts:
            if url == self_url or f'href="{url}"' in par: continue
            add += f' · <a href="{url}" style="{STYLE}">{label}</a>'
        if not add: continue
        # na de laatste bloglink invoegen, anders aan het eind
        bl = list(re.finditer(r'<a href="' + re.escape(f'/{lang + "/" if lang else ""}blog/') + r'[^"]+"[^>]*>.*?</a>', par))
        if bl:
            e = bl[-1].end(); par = par[:e] + add + par[e:]
        else:
            par = par + add
        t = t[:m.start()] + par + m.group(2) + m.group(3) + t[m.end():]
        open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'links: {n} pagina\'s bijgewerkt')
