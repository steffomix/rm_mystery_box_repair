from runner import *
import json
J=[]
for pin in (33,37):
    for l2 in (60,70,85):
        for l5 in (60,70,80):
            J.append(dict(tag=f"e8_{pin}_L2_{l2}_L5_{l5}",pin=str(pin),param={"R9":"15 Ohm","L2":f"{l2} nH","L5":f"{l5} nH"}))
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","iin","h2","h3","spur_dbc","vcmax","vswr"))
json.dump([{k:(v if not isinstance(v,(complex,dict,np.generic)) else None) for k,v in r.items() if k not in("ph","zin")} for r in rs],open("experiments/results/exp8.json","w"),default=float)
