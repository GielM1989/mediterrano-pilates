#!/usr/bin/env python3
"""Pas lijsten (oud, nieuw) toe op alle waarden van de actieve woordenboeken (niet op sleutels).
Gebruik: apply_fixes.py fixes_X.py   (bestand met FIXES = [(oud, nieuw), ...], regex via ('re:...', nieuw))"""
import json, glob, re, sys, importlib.util, os
STALE = {'dict_prix-et-marges.json','dict_faq.json','dict_comment-ca-marche.json','dict_maquette-gratuite.json','dict_a-propos-de-mediterrano-pilates.json'}
spec = importlib.util.spec_from_file_location("fx", sys.argv[1]); fx = importlib.util.module_from_spec(spec); spec.loader.exec_module(fx)
# varianten met gewone spatie voor JSON-LD (daar staat &nbsp; als spatie)
for old, new in list(fx.FIXES):
    if '&nbsp;' in old and not old.startswith('re:'): fx.FIXES.append((old.replace('&nbsp;',' '), new.replace('&nbsp;',' ')))
here = os.path.dirname(os.path.abspath(__file__))
files = [f for f in sorted(glob.glob(os.path.join(here, 'dict_*.json'))) if os.path.basename(f) not in STALE]
data = {f: json.load(open(f, encoding='utf-8')) for f in files}
counts = [0] * len(fx.FIXES)
def sub(v):
    for i, (old, new) in enumerate(fx.FIXES):
        if old.startswith('re:'):
            nv, n = re.subn(old[3:], new, v)
        else:
            n = v.count(old); nv = v.replace(old, new)
        if n: counts[i] += n; v = nv
    return v
def walk(x):
    if isinstance(x, dict):
        for k in list(x):
            x[k] = walk(x[k])
        return x
    if isinstance(x, list):
        return [walk(v) for v in x]
    if isinstance(x, str):
        return sub(x)
    return x
changed = 0
for f, d in data.items():
    before = json.dumps(d, ensure_ascii=False, sort_keys=True)
    walk(d)
    if json.dumps(d, ensure_ascii=False, sort_keys=True) != before:
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); changed += 1
for i, (old, new) in enumerate(fx.FIXES):
    if counts[i] == 0: print('NIET GEVONDEN:', old[:90])
print('bestanden gewijzigd:', changed, '| toegepast:', sum(1 for c in counts if c), '/', len(counts))
