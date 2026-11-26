import json,sys
sys.path.insert(0,'.')
import bron_nl as B
def walk(o,p,out):
    if isinstance(o,str): out.append((p,o))
    elif isinstance(o,list):
        for i,x in enumerate(o): walk(x,p+[i],out)
    elif isinstance(o,dict):
        for k,v in o.items(): walk(v,p+[k],out)
res={}
for lg in ['it','fr','es']:
    c=B.C[lg]; out=[]
    for name,fn in [('towel',B.handdoek),('a1',B.artikel1),('a2',B.artikel2)]:
        walk(fn(c),[name],out)
    res[lg]=out
json.dump({lg:[[p,t] for p,t in v] for lg,v in res.items()},open('segs_nl.json','w'),ensure_ascii=False,indent=0)
for lg in res: print(lg,len(res[lg]))
# unique texts across langs for the shared parts
