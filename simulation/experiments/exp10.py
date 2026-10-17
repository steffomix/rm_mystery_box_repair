from runner import *
import numpy as np, json
f0=27.185e6; w=2*np.pi*f0
caps={"C15":(100e-12,("n_in","n_a")),"C16":(220e-12,("n_a",None)),"C17":(270e-12,("n_a",None)),"C18":(120e-12,("n_c",None)),
      "C19":(220e-12,("n_o",None)),"C20":(270e-12,("n_o",None)),"C21":(120e-12,("n_o",None)),"C23":(1e-9,("n_o","ant"))}
def stress(datfile,pin):
    d=load_dat(datfile); r=analyse_tr(d,f0,pin,tail=8e-6)
    ph=r["ph"]; ph[None]=0
    res={}
    for n,(C,(a,b)) in caps.items():
        v=abs(ph[a]-ph[b]); i=w*C*v/np.sqrt(2)
        res[n]=dict(vpk=v,irms=i,p_ceramic=0.5*v**2*w*C*2e-3,p_mica=0.5*v**2*w*C*5e-4)
    return r,res
for name,fn,pin in (("A_5W",WORK/"e4_jumper_37.dat",37),("B_5W",WORK/"e8_37_L2_70_L5_60.dat",37),("A_2W",WORK/"e4_jumper_33.dat",33),("B_2W",WORK/"e8_33_L2_70_L5_60.dat",33)):
    r,res=stress(fn,pin)
    print(name,"Pout=%.1f W"%r["pout"],"Vc_max=%.0f"%r["vcmax"])
    tot_c=sum(v["p_ceramic"] for v in res.values()); tot_m=sum(v["p_mica"] for v in res.values())
    for n,v in res.items(): print("  %-4s Vpk=%5.1f V  Irms=%4.2f A  P_ker=%5.0f mW  P_mica=%4.0f mW"%(n,v["vpk"],v["irms"],v["p_ceramic"]*1e3,v["p_mica"]*1e3))
    print("  Summe Verlust Keramik %.0f mW / Glimmer %.0f mW"%(tot_c*1e3,tot_m*1e3))
