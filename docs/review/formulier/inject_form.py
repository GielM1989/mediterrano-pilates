"""Zet het mockupformulier van de homepage (per taal) op alle inhoudspagina's.

Idempotent: draai na elke wijziging aan het formulier op een homepage opnieuw, ook na een herbouw van /it/ of /fr/.
- vervangt het groene CTA-blok onderaan (of een ouder formulier) door het formulier van de homepage;
- behoudt de losse links uit dat CTA-blok (terug naar home, verwante pagina) eronder;
- knoppen naar /taal/#mockup-form springen naar het formulier op dezelfde pagina;
- voegt de CSS-regels van het formulier toe die op de pagina ontbreken.
Gebruik: python3 docs/review/formulier/inject_form.py [site]
"""
import re, sys, glob, os
sys.path.insert(0, os.path.dirname(__file__))
from cssdiff import rules, style_text, norm

ROOT = sys.argv[1] if len(sys.argv) > 1 else 'site'
LANGS = ['', 'en', 'de', 'nl', 'fr', 'it']
START, END = '<!-- MP-FORM:start (gegenereerd door docs/review/formulier/inject_form.py) -->', '<!-- MP-FORM:end -->'
CSS_START, CSS_END = '<style data-mp-form-css>', '</style><!-- /mp-form-css -->'
FORM_SEL = re.compile(r'\.(mw-[\w-]+|mockup-wizard|op-form|form-card|wa-alt[\w-]*|btn-wa[\w-]*|success[\w-]*|founder-note|form-note|hidden-field)\b|#(mockup-form|mockupWizard|success)\b')
SCRIPT_MARKERS = ['/* formulier */', '/* form */\n  var form = document.getElementById(\'lead-form\')', "var wizard = document.getElementById('mockupWizard')", 'var map = {utm_source', 'data-mp="first-touch"']
OLD_FORM_SCRIPT = '/* UTM, referrer y referencia de la solicitud */'

def home_parts(lang):
    t = open(f'{ROOT}/{lang + "/" if lang else ""}index.html', encoding='utf-8').read()
    m = re.search(r'<section class="sheet green" id="mockup-form">.*?\n</section>', t, re.S)
    sec = m.group(0)
    sec = re.sub(r'\s*<div class="wrap">\s*<img class="foot-mark".*?</footer>\s*</div>', '', sec, flags=re.S)
    sec = re.sub(r'((?:src|srcset)=")(?:\.\./)*images/', r'\1/images/', sec)
    sec = re.sub(r'(srcset="[^"]*?)(?:, ?)(?:\.\./)*images/', r'\1, /images/', sec)
    # op de homepage houdt de onderruimte plek vrij voor het voetlogo; hier niet nodig
    sec = sec.replace('<div class="form-section">', '<div class="form-section" style="padding-bottom:48px">', 1)
    bad = re.findall(r'(?:href|src|srcset)="(?!/|https?:|#|mailto:|tel:|data:)([^"]+)"', sec)
    assert not bad, (lang, bad)
    scripts = []
    for s in re.finditer(r'<script[^>]*>.*?</script>', t, re.S):
        if any(k in s.group(0) for k in SCRIPT_MARKERS): scripts.append(s.group(0))
    assert len(scripts) == 4, (lang, len(scripts))
    # de sticky mobiele knop bestaat alleen op de homepage: zonder die knop niets doen
    scripts = [x.replace('function onScroll(){\n', 'function onScroll(){\n    if (!bar || !formSec) return;\n', 1) for x in scripts]
    css = [r for r in rules(style_text(t)) if FORM_SEL.search(r[1])]
    return sec, scripts, (css, root_vars(t))

def targets(lang):
    base = f'{ROOT}/{lang + "/" if lang else ""}'
    out = []
    for f in sorted(glob.glob(base + '**/index.html', recursive=True)):
        rel = f[len(ROOT) + 1:]
        if not lang and re.match(r'(en|de|nl|fr|it)/', rel): continue
        if rel in (f'{lang + "/" if lang else ""}index.html', f'{lang + "/" if lang else ""}blog/index.html'): continue
        out.append(f)
    return out

def root_vars(t):
    return dict(re.findall(r'(--[\w-]+)\s*:\s*([^;}]+)', ''.join(re.findall(r':root\s*\{[^}]*\}', style_text(t)))))

def css_block(page, css, hvars=None):
    pv = root_vars(re.sub(re.escape(CSS_START) + '.*?' + re.escape(CSS_END), '', page, flags=re.S))
    vmiss = {k: v for k, v in (hvars or {}).items() if k not in pv}
    present = {(m, norm(s), norm(b)) for m, s, b in rules(style_text(re.sub(re.escape(CSS_START) + '.*?' + re.escape(CSS_END), '', page, flags=re.S)))}
    miss = [r for r in css if (r[0], norm(r[1]), norm(r[2])) not in present]
    if not miss and not vmiss: return ''
    out = [':root{' + ';'.join(f'{k}:{v.strip()}' for k, v in vmiss.items()) + '}'] if vmiss else []; media = None
    for m, s, b in miss:
        if m != media:
            if media: out.append('}')
            if m: out.append(m + '{')
            media = m
        out.append(f'{s}{{{b}}}')
    if media: out.append('}')
    return CSS_START + '\n'.join(out) + CSS_END

def inject(f, lang, sec, scripts, css):
    t = open(f, encoding='utf-8').read(); orig = t
    pre = f'/{lang}/' if lang else '/'
    if '<!-- MP-FORM:placeholder -->' in t:
        a = t.index('<!-- MP-FORM:placeholder -->'); e = '<!-- /MP-FORM:placeholder -->'; b = t.index(e) + len(e)
        links = '\n    '.join(re.findall(r'<p[^>]*>.*?</p>', t[a:b], re.S))
        t = t[:a] + '@@MPFORM@@' + t[b:]
    elif START in t:
        a = t.index(START); b = t.index(END) + len(END)
        block_old = t[a:b]
        keep = re.search(r'<!-- MP-FORM:links -->(.*?)<!-- /MP-FORM:links -->', block_old, re.S)
        links = '\n    '.join(re.findall(r'<p[^>]*>.*?</p>', keep.group(1), re.S)) if keep else ''
        t = t[:a] + '@@MPFORM@@' + t[b:]
    else:
        m = re.search(r'<section class="sheet green" id="mockup-form">.*?\n</section>', t, re.S)
        links = ''
        if m:
            t = t[:m.start()] + '@@MPFORM@@' + t[m.end():]
            # oude formulierscript weg (anders twee keer verwerken bij versturen)
            t = re.sub(r'<script>\s*\(function\(\)\{\s*' + re.escape(OLD_FORM_SCRIPT) + r'.*?</script>\n?', '', t, flags=re.S)
        else:
            ms = list(re.finditer(r'<section class="sheet green">(.*?)</section>', t, re.S))
            assert ms, f
            g = ms[-1]
            ps = [p for p in re.findall(r'<p[^>]*>.*?</p>', g.group(1), re.S)
                  if re.search(r'href="', p) and '#mockup-form' not in p]
            links = '\n    '.join(ps)
            t = t[:g.start()] + '@@MPFORM@@' + t[g.end():]
    link_html = ''
    if links.strip():
        link_html = ('<!-- MP-FORM:links --><section class="sheet green"><div class="wrap" style="padding-bottom:40px;text-align:center">\n    '
                     + links.strip() + '\n  </div></section><!-- /MP-FORM:links -->\n')
    block = START + '\n' + sec + '\n' + link_html + '\n'.join(scripts) + '\n' + END
    t = t.replace('@@MPFORM@@', block)
    assert t.count('id="lead-form"') == 1 and t.count('id="mockup-form"') == 1, f
    # knoppen naar het formulier op de homepage -> formulier op deze pagina
    t = t.replace(f'href="{pre}#mockup-form"', 'href="#mockup-form"')
    if lang == '': t = t.replace('href="/index.html#mockup-form"', 'href="#mockup-form"')
    # ontbrekende formulier-CSS
    t = re.sub(re.escape(CSS_START) + '.*?' + re.escape(CSS_END) + r'\n?', '', t, flags=re.S)
    cb = css_block(t, css[0], css[1])
    if cb: t = t.replace('</head>', cb + '\n</head>', 1)
    if t != orig: open(f, 'w', encoding='utf-8').write(t); return True
    return False

def strip_for_translation(t):
    """Voor build_it/build_fr: vervang het gegenereerde blok door alleen de vertaalbare links (placeholder)."""
    if START not in t: return t
    a = t.index(START); b = t.index(END) + len(END)
    keep = re.search(r'<!-- MP-FORM:links -->(.*?)<!-- /MP-FORM:links -->', t[a:b], re.S)
    ps = '\n'.join(re.findall(r'<p[^>]*>.*?</p>', keep.group(1), re.S)) if keep else ''
    return t[:a] + '<!-- MP-FORM:placeholder -->' + ps + '<!-- /MP-FORM:placeholder -->' + t[b:]

def run(langs=LANGS):
    n = 0; total = 0
    for lang in langs:
        sec, scripts, css = home_parts(lang)
        for f in targets(lang):
            total += 1
            if inject(f, lang, sec, scripts, css): n += 1
    print(f'formulier: {n} van {total} pagina\'s bijgewerkt')

if __name__ == '__main__':
    run()
