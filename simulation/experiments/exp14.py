from runner import *
C=dict(R9="15 Ohm",L2="70 nH",L5="60 nH")
OV={"C18":"470 pF"}
J=[dict(tag="e14_ref",pin="33",stop="30 us",param={**C,"OV":OV})]
for l3 in ("1 uH","10 uH"): J.append(dict(tag=f"e14_L3_{l3.replace(' ','')}",pin="33",stop="30 us",param={**C,"L3":l3,"OV":OV}))
for l4 in ("0.2 uH","0.6 uH","1.5 uH"): J.append(dict(tag=f"e14_L4_{l4.replace(' ','')}",pin="33",stop="30 us",param={**C,"L4":l4,"OV":OV}))
show(run_many(J,12),keys=("pout","gain","eff","h2","h3","vcmax","vswr"))
