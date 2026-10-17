from runner import *
J=[]
for l in (30,40,50,60,70):
    J.append(dict(tag=f"e5_L5_{l}_37",pin="37",param={"L5":f"{l} nH"}))
for l in (30,40,50):
    J.append(dict(tag=f"e5_L5_{l}_40",pin="40",param={"L5":f"{l} nH"}))
J.append(dict(tag="e5_L5_40_noC18",pin="37",param={"L5":"40 nH"},model={}))
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","iin","h2","h3","vcmax","vswr"))
