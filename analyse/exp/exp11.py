from runner import *
B=dict(R9="15 Ohm",L2="70 nH",L5="60 nH")
J=[dict(tag=f"e11_C18_{c}_{p}",pin=str(p),stop="30 us",param={**B,"OV":{"C18":f"{c} pF"}}) for c in (180,270,390) for p in (33,37)]
rs=run_many(J,6)
show(rs,keys=("pout","gain","eff","h2","h3","vcmax","vswr"))
