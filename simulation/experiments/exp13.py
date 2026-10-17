from runner import *
import json, random, statistics as st
A=dict(R9="1 mOhm",L2="85 nH",L5="80 nH")
C=dict(R9="15 Ohm",L2="70 nH",L5="60 nH")
CAPS=["C15","C16","C17","C18","C19","C20","C21","C23"]
def mc(base,ov,captol,Ltol,n,seed):
    rnd=random.Random(seed); out=[]
    for i in range(n):
        sc={c:1+rnd.uniform(-captol,captol) for c in CAPS}
        sc["L2"]=1+rnd.uniform(-Ltol,Ltol); sc["L5"]=1+rnd.uniform(-Ltol,Ltol)
        out.append(dict(param={**base,"OV":ov,"SCALE":sc}))
    return out
J=[]
for name,base,ov,ct in (("A",A,{},0.05),("C",C,{"C18":"470 pF"},0.02)):
    for i,j in enumerate(mc(base,ov,ct,0.10,10,7)):
        J.append(dict(tag=f"e13_mc{name}_{i}",pin="37",stop="30 us",param=j["param"]))
J.append(dict(tag="e13_C_nom_37",pin="37",stop="30 us",param={**C,"OV":{"C18":"470 pF"}}))
J.append(dict(tag="e13_C_nom_40",pin="40",stop="30 us",param={**C,"OV":{"C18":"470 pF"}}))
J.append(dict(tag="e13_C_nom_30",pin="30",stop="30 us",param={**C,"OV":{"C18":"470 pF"}}))
J.append(dict(tag="e13_C_nom_26",pin="26",stop="30 us",param={**C,"OV":{"C18":"470 pF"}}))
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","h2","h3","vcmax","vswr"))
json.dump([{k:v for k,v in r.items() if k not in("ph","zin")} for r in rs],open("experiments/results/exp13.json","w"),default=float)
for n in ('A','C'):
    xs=[x for x in rs if x['tag'].startswith('e13_mc'+n)]
    for k in ('pout','vswr','vcmax','eff','h2','h3'):
        v=[x[k] for x in xs]; print(n,k,'min %.2f max %.2f mean %.2f sd %.2f'%(min(v),max(v),st.mean(v),st.pstdev(v)))
