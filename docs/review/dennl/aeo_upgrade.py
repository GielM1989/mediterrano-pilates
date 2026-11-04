#!/usr/bin/env python3
"""AEO-upgrade van de Duitse en Nederlandse product- en nichepagina's naar Frans niveau.

Per pagina: (1) feitenblok bovenaan ("Kurz gesagt" / "In het kort"), (2) extra FAQ-vragen,
zichtbaar en in FAQPage-JSON-LD, (3) aangepaste antwoorden, (4) tekstvervangingen voor
overdreven claims. Idempotent: een pagina met het feitenblok-marker wordt overgeslagen
voor stap 1, en een vraag die al bestaat wordt niet nog eens toegevoegd.

Gebruik: python3 docs/review/dennl/aeo_upgrade.py  (vanuit de repo-root)
"""
import html, json, re, sys
from content import PAGES

SITE = "site/"
BLOCK_TMPL = (
    '    <div class="en-bref" style="background:#fff;border:1.5px solid var(--line);border-radius:20px;'
    'padding:24px 28px;max-width:44em;margin-bottom:40px">\n'
    '      <p style="font-weight:800;color:var(--green);margin-bottom:10px;letter-spacing:.02em">{title}</p>\n'
    '      <ul style="margin:0;padding-left:1.1em;line-height:1.6;font-size:.97rem">\n{items}'
    '      </ul>\n    </div>\n')


def plain(t):
    """Zichtbare HTML-tekst naar JSON-LD-tekst (geen tags, geen entiteiten, gewone spaties)."""
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).replace(" ", " ")


def jdump(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def add_block(s, title, bullets):
    if 'class="en-bref"' in s:
        return s, False
    h = s.find("</header>")
    m = re.compile(r'<div class="wrap" style="padding:[^"]*">\n').search(s, h)
    if h < 0 or not m:
        raise SystemExit("geen invoegpunt gevonden")
    items = "".join(f"        <li>{b}</li>\n" for b in bullets)
    block = BLOCK_TMPL.format(title=title, items=items)
    return s[: m.end()] + block + s[m.end():], True


def visible_questions(s):
    return [html.unescape(re.sub(r"<[^>]+>", "", q)).strip()
            for q in re.findall(r'<summary><span class="qn">\d+</span>(.*?)</summary>', s, re.S)]


def add_faqs(s, faqs):
    existing = visible_questions(s)
    added = 0
    for q, a in faqs:
        if plain(q) in existing:
            continue
        n = len(visible_questions(s)) + 1
        item = (f'      <details>\n        <summary><span class="qn">{n:02d}</span>{q}</summary>\n'
                f'        <p>{a}</p>\n      </details>\n')
        # invoegen na de laatste </details> binnen .faq (het blok sluit met '</details>\n    </div>')
        start = s.rfind('<div class="faq">')  # laatste groep (FAQ-pagina's hebben er meerdere)
        end_faq = s.find("</details>\n    </div>", start)
        if start < 0 or end_faq < 0:
            raise SystemExit("einde faq-blok niet gevonden")
        pos = end_faq + len("</details>\n")
        s = s[:pos] + item + s[pos:]
        # JSON-LD
        ld = jdump({"@type": "Question", "name": plain(q),
                    "acceptedAnswer": {"@type": "Answer", "text": plain(a)}})
        m = None
        for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            if '"FAQPage"' in mm.group(1):
                m = mm
                break
        if not m:
            raise SystemExit("geen FAQPage-JSON-LD")
        body = m.group(1)
        close = body.rfind("]")
        prev = body[:close].rstrip()
        newbody = prev + ",\n    " + ld + "\n  " + body[close:]
        s = s[: m.start(1)] + newbody + s[m.end(1):]
        added += 1
    return s, added


def set_answer(s, question, new_answer):
    """Vervang het antwoord op een bestaande vraag, zichtbaar en in JSON-LD."""
    pat = re.compile(r'(<summary><span class="qn">\d+</span>' + re.escape(question) +
                     r'</summary>\s*<p>)(.*?)(</p>)', re.S)
    m = pat.search(s)
    if not m:
        return s, False
    old_plain = plain(m.group(2))
    s = s[: m.start(2)] + new_answer + s[m.end(2):]
    old_json = json.dumps(old_plain, ensure_ascii=False)[1:-1]
    new_json = json.dumps(plain(new_answer), ensure_ascii=False)[1:-1]
    if old_json not in s:
        raise SystemExit(f"JSON-LD-antwoord niet gevonden voor: {question}")
    s = s.replace(old_json, new_json, 1)
    return s, True


def main():
    report = []
    for path, spec in PAGES.items():
        f = SITE + path + "/index.html"
        s = open(f, encoding="utf-8").read()
        orig = s
        for old, new in spec.get("replace", []):
            if old in s:
                s = s.replace(old, new)
            elif new not in s:
                report.append(f"  NIET GEVONDEN in {path}: {old[:60]}")
        if spec.get("block"):
            s, did = add_block(s, spec["block"][0], spec["block"][1])
        for q, a in spec.get("answers", []):
            s, ok = set_answer(s, q, a)
            if not ok and a not in s:
                report.append(f"  vraag niet gevonden in {path}: {q}")
        s, n = add_faqs(s, spec.get("faqs", []))
        if s != orig:
            open(f, "w", encoding="utf-8").write(s)
        report.append(f"{path}: {'gewijzigd' if s != orig else 'ongewijzigd'}, +{n} vragen")
    print("\n".join(report))


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    main()
