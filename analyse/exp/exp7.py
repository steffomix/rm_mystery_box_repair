from runner import *
import numpy as np, json
def analyse(d):
    f=np.array(d['frequency']); S=lambda i,j:np.array(d[f'S[{i},{j}]'])
    s11,s12,s21,s22=S(1,1),S(1,2),S(2,1),S(2,2)
    delta=s11*s22-s12*s21
    K=(1-abs(s11)**2-abs(s22)**2+abs(delta)**2)/(2*abs(s12*s21))
    mu=(1-abs(s11)**2)/(abs(s22-delta*np.conj(s11))+abs(s12*s21))
    mu2=(1-abs(s22)**2)/(abs(s11-delta*np.conj(s22))+abs(s12*s21))
    i=np.argmin(abs(f-27.2e6))
    band=(f>=1e6)&(f<=100e6)
    return dict(g27=20*np.log10(abs(s12[i])), s22_27=20*np.log10(abs(s22[i])), s11_27=20*np.log10(abs(s11[i])),
                s22max=20*np.log10(abs(s22[band]).max()), s22max_f=f[band][np.argmax(abs(s22[band]))]/1e6,
                Kmin=K[band].min(), Kmin_f=f[band][np.argmin(K[band])]/1e6, mumin=min(mu[band].min(),mu2[band].min()),
                gmax=20*np.log10(abs(s12[band]).max()), g_26_30=(20*np.log10(abs(s12[(f>=26e6)&(f<=30e6)])).min(),20*np.log10(abs(s12[(f>=26e6)&(f<=30e6)])).max()))
V=[("basis",{}),("R14=47",{"R14":"47 Ohm"}),("R14=68",{"R14":"68 Ohm"}),("R14=150",{"R14":"150 Ohm"}),("R14=220",{"R14":"220 Ohm"}),
   ("C26=100p",{"C26":"100 pF"}),("C26=1n",{"C26":"1 nF"}),("C28=100p",{"C28":"100 pF"}),("C28=33p",{"C28":"33 pF"}),
   ("C25=330p",{"C25":"330 pF"}),("C25=47p",{"C25":"47 pF"}),("R16=220",{"R16":"220 Ohm"}),("R15=22k",{"R15":"22 kOhm"}),("R13=4.7k",{"R13":"4.7 kOhm"})]
out={}
for name,ov in V:
    d,err=run_sp("e7_"+name.replace("=","_"),"rx",param={"OV":ov},start="1 MHz",stop="100 MHz",points=100)
    r=analyse(d); out[name]=r
    print(f"{name:10s} G27={r['g27']:.1f} dB  G26-30=[{r['g_26_30'][0]:.1f},{r['g_26_30'][1]:.1f}] S11={r['s11_27']:.1f} S22={r['s22_27']:.1f}  S22max={r['s22max']:.1f}@{r['s22max_f']:.0f}MHz Kmin={r['Kmin']:.2f}@{r['Kmin_f']:.0f} mu_min={r['mumin']:.2f}")
