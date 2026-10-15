#!/usr/bin/env python3
"""Maakt per Spaanse pagina een todo-bestand: segmentindex -> Spaanse tekst (alleen wat nog vertaald moet worden)."""
import sys, json, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_fr import extract, SKIP_EXACT, norm, HERE, ROOT
common = json.load(open(os.path.join(HERE, "dict_common.json"), encoding="utf-8"))
ld = json.load(open(os.path.join(HERE, "dict_ld.json"), encoding="utf-8"))
src = sys.argv[1]; out = sys.argv[2]
s = open(os.path.join(ROOT, src), encoding="utf-8").read()
segs = extract(s)
todo = {}; ldtodo = []
for i, (kind, a, b, t) in enumerate(segs):
    tt = t.strip()
    if tt.startswith("{"):
        o = json.loads(tt)
        def walk(x):
            if isinstance(x, dict):
                for v in x.values(): walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
            elif isinstance(x, str) and len(x) > 12 and not x.startswith("http") and norm(x) not in {norm(k) for k in common} and norm(x) not in {norm(k) for k in ld}:
                ldtodo.append(x)
        walk(o); continue
    if tt in common or tt in SKIP_EXACT: continue
    if kind == "content" and tt in ("product", "article", "website"): continue
    todo[str(i)] = (kind + ": " if kind != "text" else "") + t
# numerieke segmenten (worden door extract overgeslagen): cijfers die mogelijk Frans moeten worden
body = re.sub(r"<style[\s\S]*?</style>", lambda m: " "*len(m.group(0)), s)
body = re.sub(r"<script[\s\S]*?</script>", lambda m: " "*len(m.group(0)), body)
numeric = sorted(set(m.group(1).strip() for m in re.finditer(r">([^<>]+)<", body)
                     if re.search(r"\d", m.group(1)) and re.fullmatch(r"[\s\d.,:;€%·|/()\-+&;#]*", m.group(1).strip())))
words = sum(len(v.split()) for v in todo.values())
json.dump({"_src": src, "_todo": todo, "_ld_strings": sorted(set(ldtodo)), "_numeric_segments": numeric}, open(os.path.join(ROOT, out), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(src, len(segs), "segmenten;", len(todo), "te vertalen;", words, "woorden;", len(set(ldtodo)), "ld-strings")
