from runner import *
import numpy as np
C=dict(R9="15 Ohm",L2="70 nH",L5="60 nH",OV={"C18":"470 pF"})
J=[dict(tag=f"e15_C_f{f}_33",pin="33",stop="30 us",f=f"{f} MHz",param=C) for f in (26,26.965,27.405,28,29,29.7)]
show(run_many(J,12),keys=("pout","gain","eff","h2","h3","vcmax","vswr"))
# Kondensatorbelastung bei 5 W (nutzt e13_C_nom_37)
f0=27.185e6; w=2*np.pi*f0
caps={"C15":(100e-12,("n_in","n_a")),"C16":(220e-12,("n_a",None)),"C17":(270e-12,("n_a",None)),"C18":(470e-12,("n_c",None)),
      "C19":(220e-12,("n_o",None)),"C20":(270e-12,("n_o",None)),"C21":(120e-12,("n_o",None)),"C23":(1e-9,("n_o","ant"))}
d=load_dat(WORK/"e13_C_nom_37.dat"); r=analyse_tr(d,f0,37); ph=r["ph"]; ph[None]=0
tc=tm=0
for n,(Cv,(a,b)) in caps.items():
    v=abs(ph[a]-ph[b]); i=w*Cv*v/np.sqrt(2); pc=0.5*v**2*w*Cv*2e-3; pm=0.5*v**2*w*Cv*5e-4; tc+=pc; tm+=pm
    print("%-4s Vpk=%5.1f V Irms=%4.2f A P_keramik=%4.0f mW P_glimmer=%3.0f mW"%(n,v,i,pc*1e3,pm*1e3))
print("Summe Keramik %.0f mW, Glimmer %.0f mW"%(tc*1e3,tm*1e3))
dv=abs(ph["rtx"]-ph["n_in"]); print("R9: dV=%.1f V P=%.2f W"%(dv,dv**2/30))
