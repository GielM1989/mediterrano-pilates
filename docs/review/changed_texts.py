"""Verzamelt per taal alle zichtbare tekstsegmenten die nieuw of gewijzigd zijn t.o.v. origin/main (voor taalreview)."""
import subprocess,re,html,sys,collections
files=[f for f in subprocess.run(['git','diff','--name-only','origin/main','--','site/'],capture_output=True,text=True).stdout.split()]
files+= [f for f in subprocess.run(['git','ls-files','--others','--exclude-standard','site/'],capture_output=True,text=True).stdout.split()]
def segs(s):
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',s,flags=re.S)
    out=[]
    for m in re.finditer(r'<(p|li|h1|h2|h3|summary|span class="perk"|title)[^>]*>(.*?)</\1?[a-z0-9]*>',s,re.S):
        t=html.unescape(re.sub(r'<[^>]+>','',m.group(2))).replace('\xa0',' ')
        t=re.sub(r'\s+',' ',t).strip()
        if len(t)>12: out.append(t)
    for m in re.finditer(r'<meta name="description" content="([^"]*)"',s): out.append(html.unescape(m.group(1)))
    return out
by=collections.defaultdict(collections.OrderedDict)
for f in files:
    if not f.endswith('.html'): continue
    lang=(re.match(r'site/(en|de|nl|fr)/',f) or [None,'es'])[1]
    new=open(f,encoding='utf-8').read()
    old=subprocess.run(['git','show','origin/main:'+f],capture_output=True,text=True).stdout
    olds=set(segs(old))
    for t in segs(new):
        if t not in olds: by[lang].setdefault(t,f)
for lang,d in by.items():
    with open(f'{sys.argv[1]}/review_{lang}.txt','w') as o:
        for t,f in d.items(): o.write(f'[{f}]\n{t}\n\n')
    print(lang,len(d),sum(len(t) for t in d))
