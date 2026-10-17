from runner import *
J=[]
for pin in (20,26,30,33,37,40):
    J.append(dict(tag=f"e4_jumper_{pin}",pin=str(pin)))
    J.append(dict(tag=f"e4_R9_{pin}",pin=str(pin),param={"R9":"15 Ohm"}))
rs=run_many(J,12)
show(rs,keys=("pout","gain","eff","iin","h2","h3","spur_dbc","vcmax","vswr"))
for r in rs: print(r['tag'],'Zin=%.1f%+.1fj'%(r['zin'].real,r['zin'].imag),'|Vn_a|=%.1f |Vn_c|=%.1f |Vn_o|=%.1f |Vant|=%.1f'%tuple(abs(r['ph'][k]) for k in ('n_a','n_c','n_o','ant')))
