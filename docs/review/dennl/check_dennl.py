import re,json,html,glob,sys
pages=[p for p in glob.glob('site/de/**/index.html',recursive=True)+glob.glob('site/nl/**/index.html',recursive=True)]
bad=0
def norm(t): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',t)).replace('\xa0',' ')).strip()
for f in sorted(pages):
    s=open(f,encoding='utf-8').read()
    lds=[]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try: lds.append(json.loads(b))
        except Exception as e: print('JSON FOUT',f,e); bad+=1
    faq=[o for o in lds if isinstance(o,dict) and o.get('@type')=='FAQPage']
    vis=re.findall(r'<summary><span class="qn">\d+</span>(.*?)</summary>\s*<p>(.*?)</p>',s,re.S)
    if faq:
        ld=[(q['name'],q['acceptedAnswer']['text']) for q in faq[0]['mainEntity']]
        vq=[(norm(q),norm(a)) for q,a in vis]
        lq=[(norm(q),norm(a)) for q,a in ld]
        if vis and vq!=lq:
            print('FAQ MISMATCH',f,len(vq),len(lq))
            for a,b in zip(vq,lq):
                if a!=b: print('  V:',a[1][:120]); print('  L:',b[1][:120]); break
            bad+=1
        nums=[int(n) for n in re.findall(r'<span class="qn">(\d+)</span>',s)]
        if vis and nums!=list(range(1,len(nums)+1)): print('NUMMERING',f,nums); bad+=1
    body=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S)
    txt=html.unescape(re.sub(r'<[^>]+>',' ',body))
    if '—' in txt: print('STREEP',f); bad+=1
    if re.search(r'[A-Za-zäöüé]!',txt): print('UITROEP',f,re.findall(r'.{20}[A-Za-z]!',txt)[:2]); bad+=1
    t=re.search(r'<title>(.*?)</title>',s); 
    if t and len(html.unescape(t.group(1)))>60: print('TITEL>60',f,len(t.group(1)))
print('klaar, problemen:',bad)
