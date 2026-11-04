import re,json,html,glob
QS=["Worin unterscheidet sich das von einer günstigen Werbesocke?","Wat is het verschil met een goedkope promotiesok?"]
def plain(t): return html.unescape(re.sub(r'<[^>]+>','',t)).replace('\xa0',' ')
for f in sorted(glob.glob('site/de/**/index.html',recursive=True)+glob.glob('site/nl/**/index.html',recursive=True)):
    s=open(f,encoding='utf-8').read(); o=s
    for q in QS:
        # zichtbaar
        s=re.sub(r'      <details>\n        <summary><span class="qn">\d+</span>'+re.escape(q)+r'</summary>\n        <p>.*?</p>\n      </details>\n','',s,flags=re.S)
        # JSON-LD regel
        s=re.sub(r',\n    \{"@type":"Question","name":"'+re.escape(q)+r'".*?\}\}(?=\n)','',s)
    if s!=o:
        # hernummeren
        c=[0]
        def ren(m): c[0]+=1; return '<span class="qn">%02d</span>'%c[0]
        s=re.sub(r'<span class="qn">\d+</span>',ren,s)
        open(f,'w',encoding='utf-8').write(s); print('promo verwijderd:',f)
