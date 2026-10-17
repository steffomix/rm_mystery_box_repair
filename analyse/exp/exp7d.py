from runner import *
from runner import _prepare, _simulate
for name,ov in (("basis",{}),("opt",{"C26":"2.2 nF","R14":"330 Ohm"})):
    net=_prepare("rx","dc",{"OV":ov},None)
    dat,err=_simulate("e7d_"+name,net); d=load_dat(dat)
    print(name,err,{k:round(d[k][0],3) for k in ("Tr6.Ice","Tr6.Vce","Tr6.Vbe","em6.V","q.V","col6.V","V1.I")})
