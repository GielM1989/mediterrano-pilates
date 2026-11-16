import json,sys
SEL_C={2,3,4,7,9,10,13,14,15,17,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,42}
def norm_page(p): return p.replace('.txt','').split('/')[-1]
L={}
def lines(pg):
    if pg not in L: L[pg]=open(f'it/{pg}.txt').read().rstrip('\n').split('\n')
    return L[pg]
conf=[]
def apply(entries,tag):
    n=0
    for i,e in entries:
        pg=norm_page(e['page']); 
        if pg in ('index.html',) or 'site/' in e['page'] or '(' in e['page']: conf.append((tag,i,e['page'],'non-txt')); continue
        if not e.get('new'): continue
        ls=lines(pg); ln=e.get('line')
        if ln and 0<ln<=len(ls) and ls[ln-1]==e['old']:
            ls[ln-1]=e['new']; n+=1; continue
        # exact full-line elsewhere / substring
        hits=[k for k,l in enumerate(ls) if e['old'] in l]
        if len(hits)==1 and e['old']!=ls[hits[0]] and len(e['new'])<len(e['old'])+400 and ln and e['old']!=e['new']:
            conf.append((tag,i,pg,ln,'substring-only',e['old'][:70]))
        else: conf.append((tag,i,pg,ln,'nomatch',e['old'][:70]))
    print(tag,'applied',n)
B=json.load(open('review_B.json')); A=json.load(open('review_A.json')); C=json.load(open('review_C.json'))
apply(list(enumerate(B)),'B'); apply(list(enumerate(A)),'A'); apply([(i,c) for i,c in enumerate(C) if i in SEL_C],'C')
for pg,ls in L.items(): open(f'it/{pg}.txt','w').write('\n'.join(ls)+'\n')
json.dump(conf,open('conflicts.json','w'),ensure_ascii=False,indent=1)
print(len(conf),'conflicts'); [print(c) for c in conf]
