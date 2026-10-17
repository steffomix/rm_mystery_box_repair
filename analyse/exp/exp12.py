from runner import *
B=dict(R9="15 Ohm",L2="70 nH",L5="60 nH")
J=[dict(tag=f"e12_C18_{c}_{p}",pin=str(p),stop="30 us",param={**B,"OV":{"C18":f"{c} pF"}}) for c in (470,680) for p in (33,37)]
J+=[dict(tag=f"e12_C18_390_f{f}",pin="33",stop="30 us",f=f"{f} MHz",param={**B,"OV":{"C18":"390 pF"}}) for f in (26,28,29.7)]
J+=[dict(tag=f"e12_C18_390_L5_{l}",pin="37",stop="30 us",param={**B,"L5":f"{l} nH","OV":{"C18":"390 pF"}}) for l in (50,70)]
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","h2","h3","vcmax","vswr"))
