from runner import *
import numpy as np
for name,ov in (("basis",{}),("opt",{"C26":"2.2 nF","R14":"330 Ohm"}),("opt2",{"C26":"1 nF","R14":"220 Ohm"})):
    d,err=run_sp("e7c_"+name,"rx",param={"OV":ov},start="20 MHz",stop="35 MHz",points=16,noise=True)
    print(name,err,[k for k in d if 'F' in k or 'NF' in k or 'noise' in k.lower()][:8])
    f=np.array(d['frequency']); 
    for k in d:
        if k in('F','NF','Nf'): 
            print(k,[round(10*np.log10(abs(x)),2) if k=='F' else round(abs(x),2) for x in d[k]][:16])
