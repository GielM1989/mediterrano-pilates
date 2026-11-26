# -*- coding: utf-8 -*-
"""Bouwt de handdoekpagina en twee artikelen in IT/FR/ES (26-11-2026).
Sjabloon: bestaand artikel (kit/pack) en bestaande tumblerpagina per taal; head, JSON-LD,
taalkeuze en inhoud tot aan het formulier (MP-FORM) worden vervangen. Idempotent."""
import html, json, os, re, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'site'))
sys.path.insert(0, HERE)
BASE = 'https://mediterranopilates.com'
DATE = '2026-11-26'

T = {lg: importlib.reload(importlib.import_module('teksten_' + lg)) for lg in ('it', 'fr', 'es')}

TPL = {
 'it': {'art': 'it/blog/kit-di-benvenuto-nuove-allieve-pilates/index.html', 'prod': 'it/tumbler-termico-personalizzato/index.html'},
 'fr': {'art': 'fr/blog/kit-de-bienvenue-nouveaux-eleves-pilates/index.html', 'prod': 'fr/gourde-isotherme-personnalisee/index.html'},
 'es': {'art': 'blog/pack-de-bienvenida-alumnas-nuevas-pilates/index.html', 'prod': 'botellas-personalizadas-estudios-pilates/index.html'},
}
HOME = {'es': '/', 'it': '/it/', 'fr': '/fr/'}
BLOG = {'es': '/blog/', 'it': '/it/blog/', 'fr': '/fr/blog/'}
LOCALE = {'es': 'es_ES', 'it': 'it_IT', 'fr': 'fr_FR'}
UI = {
 'it': dict(blog_kicker='<span class="kicker-lead">Blog</span> per gli studi di pilates', date_line='Pubblicato il <time datetime="2026-11-26">26 novembre 2026</time> · A cura di Mediterrano Pilates',
            more='Leggi anche', blog='Blog', cat='Prodotti personalizzati per studi di pilates e yoga'),
 'fr': dict(blog_kicker='<span class="kicker-lead">Blog</span> pour les studios de Pilates', date_line='Publié le <time datetime="2026-11-26">26 novembre 2026</time> · Par Mediterrano Pilates',
            more='À lire aussi', blog='Blog', cat='Produits personnalisés pour studios de Pilates et de yoga'),
 'es': dict(blog_kicker='<span class="kicker-lead">Blog</span> para estudios de pilates', date_line='Publicado el <time datetime="2026-11-26">26 de noviembre de 2026</time> · Por Mediterrano Pilates',
            more='Te puede interesar', blog='Blog', cat='Productos personalizados para estudios de pilates y yoga'),
}
LINKS = {
 'it': {'socks': ('/it/calze-antiscivolo-personalizzate/', 'Calze antiscivolo personalizzate'),
        'towel': ('/it/telo-reformer-personalizzato/', 'Telo per reformer personalizzato'),
        'tumbler': ('/it/tumbler-termico-personalizzato/', 'Tumbler termico personalizzato'),
        'tote': ('/it/tote-bag-personalizzata/', 'Tote bag personalizzata'),
        'prices': ('/it/prezzi-e-margini/', 'Prezzi e margini'),
        'kit': ('/it/blog/kit-di-benvenuto-nuove-allieve-pilates/', 'Kit di benvenuto per i nuovi allievi'),
        'stock': ('/it/blog/aumentare-fatturato-studio-pilates-senza-magazzino/', 'Aumentare il fatturato senza magazzino'),
        'a1': ('/it/blog/aprire-uno-studio-di-pilates/', 'Aprire uno studio di pilates'),
        'a2': ('/it/blog/cosa-vendere-studio-pilates/', 'Cosa vendere alla reception')},
 'fr': {'socks': ('/fr/chaussettes-antiderapantes-personnalisees/', 'Chaussettes antidérapantes personnalisées'),
        'towel': ('/fr/serviette-pilates-reformer-personnalisee/', 'Serviette pour Reformer personnalisée'),
        'tumbler': ('/fr/gourde-isotherme-personnalisee/', 'Gourde isotherme personnalisée'),
        'tote': ('/fr/tote-bag-personnalise/', 'Tote bag personnalisé'),
        'prices': ('/fr/prix-et-marges/', 'Prix et marges'),
        'kit': ('/fr/blog/kit-de-bienvenue-nouveaux-eleves-pilates/', 'Kit de bienvenue pour les nouveaux élèves'),
        'stock': ('/fr/blog/augmenter-chiffre-affaires-studio-pilates-sans-stock/', "Augmenter votre chiffre d'affaires sans stock"),
        'a1': ('/fr/blog/ouvrir-un-studio-de-pilates/', 'Ouvrir un studio de Pilates'),
        'a2': ('/fr/blog/que-vendre-studio-pilates/', "Que vendre à l'accueil")},
 'es': {'socks': ('/calcetines-antideslizantes-personalizados/', 'Calcetines antideslizantes personalizados'),
        'towel': ('/toalla-reformer-personalizada/', 'Toalla para reformer personalizada'),
        'tumbler': ('/botellas-personalizadas-estudios-pilates/', 'Vaso térmico personalizado'),
        'tote': ('/tote-bags-personalizadas-estudios-yoga/', 'Tote bags personalizadas'),
        'prices': ('/precios-y-margenes/', 'Precios y márgenes'),
        'kit': ('/blog/pack-de-bienvenida-alumnas-nuevas-pilates/', 'Pack de bienvenida para alumnos nuevos'),
        'stock': ('/blog/aumentar-ingresos-estudio-pilates-sin-stock/', 'Aumentar ingresos sin stock'),
        'a1': ('/blog/abrir-un-estudio-de-pilates/', 'Cómo abrir un estudio de pilates'),
        'a2': ('/blog/que-vender-estudio-pilates/', 'Qué vender en recepción')},
}
RELATED = {'towel': ['socks', 'tumbler', 'tote', 'prices', 'a1', 'a2'],
           'a1': ['socks', 'towel', 'tumbler', 'kit', 'prices', 'a2'],
           'a2': ['socks', 'towel', 'tumbler', 'tote', 'prices', 'stock', 'a1']}


def esc(s):
    return html.escape(s, quote=False)


def fr_typo(s):
    # harde spatie voor ; : ? ! % € en na « / voor » (Franse typografie)
    s = re.sub(r' ([;:?!%€»])', ' \\1', s)
    s = s.replace('« ', '« ')
    return s


def txt(lg, s):
    s = esc(s)
    if lg == 'fr':
        s = fr_typo(s)
    return s.replace(' ', '&nbsp;')


def table(lg, head, rows):
    h = ''.join(f'<th>{txt(lg, c)}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td>{txt(lg, c)}</td>' for c in r) + '</tr>' for r in rows)
    return f'<div class="tblwrap"><table>\n      <thead><tr>{h}</tr></thead>\n      <tbody>{b}</tbody>\n    </table></div>'


def faq_html(lg, title, faq, width=None):
    w = f' style="max-width:{width}"' if width else ''
    items = ''.join(f'''
      <details>
        <summary><span class="qn">{i:02d}</span>{txt(lg, q)}</summary>
        <p>{txt(lg, a)}</p>
      </details>''' for i, (q, a) in enumerate(faq, 1))
    return f'''<div class="faq-section" id="faq" style="padding-top:24px">
  <div class="wrap"{w}>
    <h2>{txt(lg, title)}</h2>
    <div class="faq">{items}
    </div>
  </div>
</div>
'''


def related(lg, page):
    L = LINKS[lg]
    lis = ''.join(f'<li><a href="{L[k][0]}" style="color:var(--terra-2);font-weight:700;text-decoration:underline">{txt(lg, L[k][1])}</a></li>' for k in RELATED[page])
    return f'<h2 style="margin-top:44px">{UI[lg]["more"]}</h2>\n    <ul>{lis}</ul>'


ART_CSS = """<style data-mp-art-css>
.art table{width:100%;border-collapse:collapse;margin:6px 0 26px;font-size:.95rem}
.art th,.art td{padding:10px 12px;border-bottom:1px solid rgba(46,64,52,.14);text-align:left;vertical-align:top;color:#4c554d}
.art th{background:var(--green);color:var(--cream);font-weight:700}
.art tr:nth-child(even) td{background:rgba(46,64,52,.04)}
.art ol,.art ul{margin:0 0 22px 22px;color:#4c554d;max-width:none}
.art li{margin-bottom:10px;line-height:1.55}
.art .tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.art .en-bref ul{margin:0}
</style>"""
P = 'style="max-width:none;color:#4c554d;margin-bottom:18px"'


def body_towel(lg, d):
    kort = ''.join(f'<li>{txt(lg, x)}</li>' for x in d['kort'])
    stap = ''.join(f'<li><strong>{txt(lg, a)}</strong> {txt(lg, b)}</li>' for a, b in d['stap'])
    return f'''<header class="hero" id="top">
  <div class="wrap">
    <span class="kicker"><span class="kicker-lead">{txt(lg, d['kicker_a'])}</span> {txt(lg, d['kicker_b'])}</span>
    <h1>{txt(lg, d['h1a'])} <span class="fx">{txt(lg, d['h1b'])}</span></h1>
    <p class="sub">{txt(lg, d['sub'])}</p>
    <p style="margin-top:28px"><a class="btn" href="#mockup-form">{txt(lg, d['cta'])}</a></p>
  </div>
</header>

<section class="sheet cream art">
  <div class="wrap" style="padding-top:8px;padding-bottom:8px">
    <div class="en-bref" style="background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:24px 28px;max-width:44em;margin-bottom:40px">
      <p style="font-weight:800;color:var(--green);margin-bottom:10px;letter-spacing:.02em">{txt(lg, d['kort_h'])}</p>
      <ul style="margin:0;padding-left:1.1em;line-height:1.6;font-size:.97rem">{kort}</ul>
    </div>
    <div style="max-width:760px">
    <picture><source srcset="/images/product-towel.webp" type="image/webp"><img src="/images/product-towel.jpg" width="900" height="1200" alt="{txt(lg, d['h1a'] + ' ' + d['h1b'])}" style="width:100%;max-width:420px;height:auto;border-radius:20px;margin:0 0 32px" loading="lazy"></picture>
    <h2>{txt(lg, d['h2_1'])}</h2>
    <p {P}>{txt(lg, d['p_1'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_2'])}</h2>
    {table(lg, d['tab_h'], d['tab'])}
    <h2 style="margin-top:44px">{txt(lg, d['h2_3'])}</h2>
    <p {P}>{txt(lg, d['p_3'])}</p>
    {table(lg, d['staf_h'], d['staf'])}
    <p {P}>{txt(lg, d['p_3b'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_4'])}</h2>
    <ol>{stap}</ol>
    {related(lg, 'towel')}
    </div>
  </div>
</section>

''' + faq_html(lg, d['faq_h'], d['faq'])


def body_article(lg, d, page):
    head = f'''<header class="hero" id="top">
  <div class="wrap">
    <span class="kicker">{UI[lg]['blog_kicker']}</span>
    <h1>{txt(lg, d['h1a'])} <span class="fx">{txt(lg, d['h1b'])}</span></h1>
    <p class="sub">{txt(lg, d['intro'])}</p>
    <p style="margin-top:28px"><a class="btn" href="#mockup-form">{txt(lg, T[lg].towel['cta'])}</a></p>
    <p class="post-date" style="margin-top:16px;font-size:.86rem;opacity:.78">{UI[lg]['date_line']}</p>
  </div>
</header>

<section class="sheet cream art">
  <div class="wrap" style="padding:48px 0 8px;max-width:760px">
    <h2>{txt(lg, d['kort_h'])}</h2>
    <p {P}>{txt(lg, d['kort'])}</p>
'''
    if page == 'a1':
        plan = ''.join(f'<li><strong>{txt(lg, a)}</strong> {txt(lg, b)}</li>' for a, b in d['plan'])
        chk = ''.join(f'<li>{txt(lg, x)}</li>' for x in d['check'])
        mid = f'''
    <h2 style="margin-top:44px">{txt(lg, d['h2_1'])}</h2>
    <p {P}>{txt(lg, d['p_1a'])}</p>
    <p {P}>{txt(lg, d['p_1b'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_2'])}</h2>
    {table(lg, d['tab_h'], d['tab'])}
    <p {P}>{txt(lg, d['p_2'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_3'])}</h2>
    <ol>{plan}</ol>
    <p {P}>{txt(lg, d['p_3'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_4'])}</h2>
    <p {P}>{txt(lg, d['p_4'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_5'])}</h2>
    <ul>{chk}</ul>
'''
    else:
        drie = ''.join(f'<li><strong>{txt(lg, a)}</strong> {txt(lg, b)}</li>' for a, b in d['drie'])
        tips = ''.join(f'<li><strong>{txt(lg, a)}</strong> {txt(lg, b)}</li>' for a, b in d['tips'])
        mid = f'''
    <h2 style="margin-top:44px">{txt(lg, d['h2_1'])}</h2>
    <p {P}>{txt(lg, d['p_1'])}</p>
    <ol>{drie}</ol>
    <h2 style="margin-top:44px">{txt(lg, d['h2_2'])}</h2>
    {table(lg, d['tab_h'], d['tab'])}
    <p {P}>{txt(lg, d['p_2'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_3'])}</h2>
    <p {P}>{txt(lg, d['p_3'])}</p>
    <h2 style="margin-top:44px">{txt(lg, d['h2_4'])}</h2>
    <ul>{tips}</ul>
'''
    tail = f'''    {related(lg, page)}
  </div>
</section>

''' + faq_html(lg, d['faq_h'], d['faq'], '760px')
    return head + mid + tail


def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + '\n</script>'


def schemas(lg, page, d, url):
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Mediterrano Pilates', 'item': BASE + HOME[lg]}]
    if page != 'towel':
        crumbs.append({'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + BLOG[lg]})
    crumbs.append({'@type': 'ListItem', 'position': len(crumbs) + 1, 'name': d['title'], 'item': url})
    out = [jsonld({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': crumbs})]
    if page == 'towel':
        out.append(jsonld({'@context': 'https://schema.org', '@type': 'Product', '@id': url + '#product',
            'name': d['title'], 'image': BASE + '/images/product-towel.jpg', 'description': d['desc'],
            'brand': {'@type': 'Brand', 'name': 'Mediterrano Pilates'}, 'category': UI[lg]['cat'],
            'offers': {'@type': 'Offer', 'url': url, 'priceCurrency': 'EUR', 'price': '11.95',
                       'availability': 'https://schema.org/InStock', 'businessFunction': 'https://schema.org/Sell',
                       'eligibleQuantity': {'@type': 'QuantitativeValue', 'minValue': 50, 'unitCode': 'C62'}},
            'inLanguage': lg}))
    else:
        out.append(jsonld({'@context': 'https://schema.org', '@type': 'Article', 'headline': d['title'],
            'description': d['desc'], 'inLanguage': lg, 'image': BASE + '/images/og-image.jpg',
            'author': {'@type': 'Organization', 'name': 'Mediterrano Pilates'},
            'publisher': {'@type': 'Organization', 'name': 'Mediterrano Pilates', 'url': BASE + HOME[lg]},
            'mainEntityOfPage': url, 'datePublished': DATE, 'dateModified': DATE}))
    out.append(jsonld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in d['faq']]}))
    return '\n'.join(out)


def build(lg, page):
    d = getattr(T[lg], page)
    url = BASE + d['slug']
    tpl = open(os.path.join(SITE, TPL[lg]['prod' if page == 'towel' else 'art']), encoding='utf-8').read()
    # head: titel en meta
    tpl = re.sub(r'<title>.*?</title>', f'<title>{esc(d["title"])}</title>', tpl, count=1, flags=re.S)
    tpl = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(d["desc"])}">', tpl, count=1)
    tpl = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(d["title"])} · Mediterrano Pilates">', tpl, count=1)
    tpl = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{html.escape(d["desc"])}">', tpl, count=1)
    tpl = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', tpl, count=1)
    if page == 'towel':
        tpl = re.sub(r'(<meta property="og:image" content=")[^"]*(">)', r'\g<1>' + BASE + r'/images/product-towel.jpg\2', tpl, count=1)
        tpl = re.sub(r'(<meta name="twitter:image" content=")[^"]*(">)', r'\g<1>' + BASE + r'/images/product-towel.jpg\2', tpl, count=1)
        tpl = re.sub(r'<meta property="og:image:width" content="\d+">', '<meta property="og:image:width" content="900">', tpl, count=1)
        tpl = re.sub(r'<meta property="og:image:height" content="\d+">', '<meta property="og:image:height" content="1200">', tpl, count=1)
        tpl = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{html.escape(d["title"])}">', tpl, count=1)
    tpl = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', tpl, count=1)
    # hreflang: alleen es/fr/it + x-default (es)
    cluster = {l: BASE + getattr(T[l], page)['slug'] for l in ('es', 'fr', 'it')}
    hl = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{cluster[l]}">' for l in ('es', 'fr', 'it'))
    hl += f'\n<link rel="alternate" hreflang="x-default" href="{cluster["es"]}">'
    tpl = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]*">\n?)+', hl + '\n', tpl, count=1)
    # og:locale:alternate: alleen de andere twee talen van dit cluster
    alts = '\n'.join(f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in ('es', 'fr', 'it') if l != lg)
    tpl = re.sub(r'(<meta property="og:locale:alternate" content="[^"]+">\n?)+', alts + '\n', tpl, count=1)
    # JSON-LD vervangen
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>\n?', tpl, flags=re.S))
    s, e = blocks[0].start(), blocks[-1].end()
    tpl = tpl[:s] + schemas(lg, page, d, url) + '\n' + tpl[e:]
    # taalkeuze
    def ls(m):
        lines = []
        for l, lab in (('es', 'ES'), ('en', 'EN'), ('de', 'DE'), ('nl', 'NL'), ('fr', 'FR'), ('it', 'IT')):
            href = getattr(T[l], page)['slug'] if l in T else f'/{l}/'
            on = ' class="on"' if l == lg else ''
            cur = ' aria-current="true"' if l == lg else ''
            lines.append(f'      <a href="{href}"{on} hreflang="{l}"{cur}>{lab}</a>')
        return m.group(1) + '\n' + '\n'.join(lines) + '\n    </nav>'
    tpl = re.sub(r'(<nav class="lang-switch" aria-label="[^"]*">).*?</nav>', ls, tpl, count=1, flags=re.S)
    if page == 'towel' and 'data-mp-art-css' not in tpl:
        tpl = tpl.replace('</head>', ART_CSS + '\n</head>', 1)
    # inhoud tot het formulier
    i = tpl.index('<header class="hero"')
    j = tpl.index('<!-- MP-FORM:start')
    body = body_towel(lg, d) if page == 'towel' else body_article(lg, d, page)
    tpl = tpl[:i] + body + '\n' + tpl[j:]
    # geen link naar de pagina zelf in de linkregel onderaan
    tpl = re.sub(r' · <a href="' + re.escape(d['slug']) + r'" [^>]*>[^<]*</a>', '', tpl)
    out = os.path.join(SITE, d['slug'].strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(tpl)
    return out


if __name__ == '__main__':
    for lg in ('it', 'fr', 'es'):
        for page in ('towel', 'a1', 'a2'):
            print(build(lg, page))
