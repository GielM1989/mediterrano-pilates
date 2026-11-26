"""Linkregel onderaan elke ES/FR/IT-pagina: links naar de handdoekpagina en de twee nieuwe artikelen (26-11-2026)."""
import re, sys, glob
ROOT = sys.argv[1] if len(sys.argv) > 1 else 'site'
A = {
 '':   [('/toalla-reformer-personalizada/', 'Toalla para reformer con logo'),
        ('/blog/abrir-un-estudio-de-pilates/', 'Cómo abrir un estudio de pilates'),
        ('/blog/que-vender-estudio-pilates/', 'Qué vender en un estudio de pilates')],
 'fr': [('/fr/serviette-pilates-reformer-personnalisee/', 'Serviette pour Reformer à votre logo'),
        ('/fr/blog/ouvrir-un-studio-de-pilates/', 'Ouvrir un studio de Pilates'),
        ('/fr/blog/que-vendre-studio-pilates/', "Que vendre à l'accueil d'un studio")],
 'it': [('/it/telo-reformer-personalizzato/', 'Telo per reformer con logo'),
        ('/it/blog/aprire-uno-studio-di-pilates/', 'Aprire uno studio di pilates'),
        ('/it/blog/cosa-vendere-studio-pilates/', 'Cosa vendere alla reception')],
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
