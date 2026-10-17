from runner import *
J=[dict(tag=f"e6_L2_{l}",pin="33",param={"L2":f"{l} nH"}) for l in (40,60,85,110,140,180,240)]
J+=[dict(tag=f"e6_L2_{l}_R9",pin="33",param={"L2":f"{l} nH","R9":"15 Ohm"}) for l in (85,140,180)]
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","iin","h2","h3","spur_dbc","vcmax","vswr"))
for r in rs: print(r['tag'],'Zin=%.1f%+.1fj'%(r['zin'].real,r['zin'].imag),'|Vn_a|=%.1f'%abs(r['ph']['n_a']))
