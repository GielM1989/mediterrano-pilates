#!/usr/bin/env python3
"""Print, as JSON, the segments of a Spanish source page that still need a French translation.

Usage: python3 docs/review/fr/segs_todo.py site/<page>/index.html [--all]
Output: {"<index>": {"kind": "text|alt|placeholder|content|aria-label|title|data-name|value", "es": "<Spanish text>"}}
Indexes are the keys to use in dict_<page>.json. Segments already covered by dict_common.json are omitted
unless --all is given (then they appear with "fr" filled in, for context).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_fr import extract, SKIP_EXACT, ROOT

common = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dict_common.json"), encoding="utf-8"))
src = sys.argv[1]
s = open(os.path.join(ROOT, src), encoding="utf-8").read()
out = {}
for i, (kind, a, b, t) in enumerate(extract(s)):
    ts = t.strip()
    if ts.startswith("{"):
        continue
    if ts in common or ts in SKIP_EXACT:
        if "--all" in sys.argv:
            out[str(i)] = {"kind": kind, "es": ts, "fr": common.get(ts, ts)}
        continue
    out[str(i)] = {"kind": kind, "es": ts}
print(json.dumps(out, ensure_ascii=False, indent=1))
