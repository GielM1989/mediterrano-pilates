#!/usr/bin/env python3
"""Meldt gewijzigde pagina's bij IndexNow (Bing, Yandex, Seznam, Naver, Yep).
Gebruik:
  python3 scripts/indexnow.py --diff <oude-sha> <nieuwe-sha>   # alleen gewijzigde/verwijderde pagina's
  python3 scripts/indexnow.py --all                            # alle URL's uit site/sitemap.xml
  python3 scripts/indexnow.py --urls https://... https://...   # losse URL's
Optie --dry-run toont alleen de lijst. Verwijderde pagina's worden ook gemeld: IndexNow
ziet dan de 301/404 en werkt de index sneller bij."""
import json, re, subprocess, sys, urllib.request

HOST = "mediterranopilates.com"
BASE = "https://" + HOST
KEY = "2c71ed55357f6c58aa0102ea6ac34f3e"
SKIP = re.compile(r"(^|/)(404|__forms)\.html$")

def path_to_url(p):
    if not p.startswith("site/") or not p.endswith(".html") or SKIP.search(p):
        return None
    rel = p[len("site"):]
    rel = rel[:-len("index.html")] if rel.endswith("index.html") else rel
    return BASE + rel

def from_diff(a, b):
    out = subprocess.run(["git", "diff", "--name-only", a, b, "--", "site/"], capture_output=True, text=True, check=True).stdout.split()
    urls = [u for u in map(path_to_url, out) if u]
    if any(p in ("site/sitemap.xml", "site/llms.txt") for p in out):
        urls.append(BASE + "/")
    return sorted(set(urls))

def from_sitemap():
    return sorted(set(re.findall(r"<loc>([^<]+)</loc>", open("site/sitemap.xml", encoding="utf-8").read())))

def submit(urls):
    for i in range(0, len(urls), 10000):
        body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"{BASE}/{KEY}.txt", "urlList": urls[i:i + 10000]}).encode()
        req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print("IndexNow antwoord:", r.status)
        except urllib.error.HTTPError as e:
            print("IndexNow fout:", e.code, e.read()[:300])
            if e.code not in (200, 202):
                sys.exit(1)

if __name__ == "__main__":
    a = sys.argv[1:]
    dry = "--dry-run" in a
    a = [x for x in a if x != "--dry-run"]
    if a[:1] == ["--diff"]:
        urls = from_diff(a[1], a[2])
    elif a[:1] == ["--all"]:
        urls = from_sitemap()
    elif a[:1] == ["--urls"]:
        urls = a[1:]
    else:
        sys.exit(__doc__)
    print(f"{len(urls)} URL's:"); print("\n".join(urls))
    if urls and not dry:
        submit(urls)
