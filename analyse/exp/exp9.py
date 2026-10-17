from runner import *
import json, random
A=dict(R9="1 mOhm",L2="85 nH",L5="80 nH")          # Vorher
B=dict(R9="15 Ohm",L2="70 nH",L5="60 nH")          # Nachher (Kandidat)
CAPS=["C15","C16","C17","C18","C19","C20","C21","C23"]
def mc(base,captol,Ltol,n,seed):
    rnd=random.Random(seed); out=[]
    for i in range(n):
        sc={c:1+rnd.uniform(-captol,captol) for c in CAPS}
        sc["L2"]=1+rnd.uniform(-Ltol,Ltol); sc["L5"]=1+rnd.uniform(-Ltol,Ltol)
        out.append(dict(param={**base,"SCALE":sc}))
    return out
J=[]
for k,(name,base,ct) in enumerate((("A",A,0.05),("B",B,0.02))):
    for i,j in enumerate(mc(base,ct,0.10,10,42)):
        J.append(dict(tag=f"e9_mc{name}_{i}",pin="33",stop="30 us",param=j["param"]))
# Temperatur +40 K: N750-Kondensatoren -3 %
N750=["C16","C17","C19","C20"]
J.append(dict(tag="e9_A_warm",pin="33",stop="30 us",param={**A,"SCALE":{c:0.97 for c in N750}}))
J.append(dict(tag="e9_B_N750_warm",pin="33",stop="30 us",param={**B,"SCALE":{c:0.97 for c in N750}}))
J.append(dict(tag="e9_B_N750_cold",pin="33",stop="30 us",param={**B,"SCALE":{c:1.03 for c in N750}}))
for f in ("26 MHz","28 MHz","29.7 MHz"):
    J.append(dict(tag=f"e9_A_f{f.split()[0]}",pin="33",stop="30 us",f=f,param=A))
    J.append(dict(tag=f"e9_B_f{f.split()[0]}",pin="33",stop="30 us",f=f,param=B))
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","h2","h3","spur_dbc","vcmax","vswr"))
json.dump([{k:v for k,v in r.items() if k not in("ph","zin")} for r in rs],open("../analyse/exp/exp9.json","w"),default=float)
