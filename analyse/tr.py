import sys,subprocess,os,time
sys.path.insert(0,'/tmp/qb'); sys.path.insert(0,'.')
import numpy as np
from netlist import netlist
from rd import load
os.environ['LD_LIBRARY_PATH']='/tmp/qb/inst/lib'
pin=sys.argv[1]; stop=sys.argv[2] if len(sys.argv)>2 else '12 us'
open('/tmp/qb/run/tx_tr.net','w').write(netlist('tx','tr',pin=pin,stop=stop,points=int(float(stop.split()[0])*500)+1))
t=time.time()
r=subprocess.run(['/tmp/qb/inst/bin/qucsator_rf','-i','/tmp/qb/run/tx_tr.net','-o','/tmp/qb/run/tx_tr.dat'],capture_output=True,text=True)
print('t=%.1fs'%(time.time()-t), r.returncode); print('\n'.join(l for l in (r.stderr+r.stdout).splitlines() if 'rror' in l or 'WARN' in l or 'NOTIFY' in l)[-500:])
d=load('/tmp/qb/run/tx_tr.dat')
t_=np.array(d['time'])
print(len(t_), [k for k in d if k.endswith('.Vt')][:5])
f0=27.185e6;T=1/f0
def fund(v):
    m=t_>t_[-1]-6*T
    tt=t_[m];vv=np.array(v)[m]
    # Fourier ueber exakt 6 Perioden (nicht-aequidistant: Interpolation)
    tg=np.linspace(t_[-1]-6*T,t_[-1],6*200,endpoint=False)
    vg=np.interp(tg,t_,v)
    out=[]
    for h in range(0,6):
        c=np.mean(vg*np.exp(-2j*np.pi*h*f0*tg))*(1 if h==0 else 2)
        out.append(abs(c))
    return out
vant=fund(d['ant.Vt']);vin=fund(d['rtx.Vt'])
print('Vant harmonics (V pk):',np.round(vant,2))
P=lambda v:v**2/100
print('Pout W:',P(vant[1]),' harm dBc:',[round(20*np.log10(vant[h]/vant[1]+1e-12),1) for h in (2,3,4,5)])
Vcc=np.mean(np.interp(np.linspace(t_[-1]-6*T,t_[-1],1200),t_,d['vcc.Vt']))
print('Vcc avg',Vcc,'Iin avg A', -np.mean(np.interp(np.linspace(t_[-1]-6*T,t_[-1],1200),t_,d['V1.It'])) if 'V1.It' in d else None)
vr=fund(d['rtx.Vt']); print('Vrtx pk',vr[1],' Pfwd approx (Vsrc/2)^2/100')
