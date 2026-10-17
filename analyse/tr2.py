import sys,subprocess,os,time,json
sys.path.insert(0,'/tmp/qb'); sys.path.insert(0,'.')
import numpy as np
import kl200_circuit as kc
ov=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
kc.MODEL['MRF455'].update(ov)
from netlist import netlist
from rd import load
os.environ['LD_LIBRARY_PATH']='/tmp/qb/inst/lib'
pin=sys.argv[1]; stop=sys.argv[2]
open('/tmp/qb/run/x.net','w').write(netlist('tx','tr',pin=pin,stop=stop,points=int(float(stop.split()[0])*500)+1))
t=time.time()
r=subprocess.run(['/tmp/qb/inst/bin/qucsator_rf','-i','/tmp/qb/run/x.net','-o','/tmp/qb/run/x.dat'],capture_output=True,text=True)
print('t=%.1fs rc=%d'%(time.time()-t, r.returncode), [l for l in (r.stderr+r.stdout).splitlines() if 'ERROR' in l])
d=load('/tmp/qb/run/x.dat'); t_=np.array(d['time']); print('tend',t_[-1])
f0=27.185e6;T=1/f0
if t_[-1]>8e-6:
    tg=np.linspace(t_[-1]-6*T,t_[-1],1200,endpoint=False)
    def fund(v):
        vg=np.interp(tg,t_,v); return [abs(np.mean(vg*np.exp(-2j*np.pi*h*f0*tg)))*(1 if h==0 else 2) for h in range(6)]
    va=fund(d['ant.Vt']); print('Vant',np.round(va,2),'Pout',va[1]**2/100,'H2/H3 dBc',[round(20*np.log10(va[h]/va[1]+1e-12),1) for h in (2,3)])
    print('Iin DC', -np.mean(np.interp(tg,t_,d['V1.It'])))
