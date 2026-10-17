import sys,subprocess,os,json,itertools
sys.path.insert(0,'/tmp/qb'); sys.path.insert(0,'/home/stefan/Dokumente/Coding/rm_italy_kl200_455_rev501/simulation')
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import kl200_circuit as kc
from netlist import netlist
from rd import load
os.environ['LD_LIBRARY_PATH']='/tmp/qb/inst/lib'
f0=27.185e6;T=1/f0
def run(tag,param,pin,model=None,stop="8 us",f="27.185 MHz"):
    kc.PARAM.update(param)
    if model: kc.MODEL['MRF455'].update(model)
    return tag
def job(args):
    tag,param,pin,model,stop,f=args
    # jede Variante in eigenem Prozess (Modulzustand!)
    code=f"""
import sys,json
sys.path.insert(0,'/home/stefan/Dokumente/Coding/rm_italy_kl200_455_rev501/simulation')
import kl200_circuit as kc
kc.PARAM.update({json.dumps(param)}); kc.MODEL['MRF455'].update({json.dumps(model or {})})
from netlist import netlist
print(netlist('tx','tr',pin='{pin}',stop='{stop}',points=int(float('{stop}'.split()[0])*400)+1,f='{f}'))
"""
    net=subprocess.run(['python3','-c',code],capture_output=True,text=True).stdout
    nf=f'/tmp/qb/run/s_{tag}.net'; open(nf,'w').write(net)
    r=subprocess.run(['/tmp/qb/inst/bin/qucsator_rf','-i',nf,'-o',nf[:-4]+'.dat'],capture_output=True,text=True)
    err=[l for l in (r.stderr+r.stdout).splitlines() if 'ERROR' in l]
    d=load(nf[:-4]+'.dat'); t=np.array(d['time'])
    fr=float(f.split()[0])*1e6; Tn=1/fr
    tg=np.linspace(t[-1]-6*Tn,t[-1],1200,endpoint=False)
    def fund(v):
        vg=np.interp(tg,t,v); return [abs(np.mean(vg*np.exp(-2j*np.pi*h*fr*tg)))*(1 if h==0 else 2) for h in range(6)]
    va=fund(d['ant.Vt']); iin=-np.mean(np.interp(tg,t,d['V1.It']))
    pin_w=1e-3*10**(float(pin)/10)
    pout=va[1]**2/100
    n=16; tg2=np.arange(t[-1]*0.6,t[-1],Tn/n); vv=np.interp(tg2,t,d['ant.Vt']); npr=len(vv)//n
    envp=np.abs(vv[:npr*n].reshape(npr,n)@np.exp(-2j*np.pi*np.arange(n)/n))*2/n
    ripple=(envp.max()-envp.min())/envp.mean()
    wins=[]
    for frac in (0.25,0.5,0.75):
        te=t[-1]*frac; tw=np.linspace(te-6*Tn,te,1200,endpoint=False)
        vg=np.interp(tw,t,d['ant.Vt']); wins.append(round((abs(np.mean(vg*np.exp(-2j*np.pi*fr*tw)))*2)**2/100,1))
    return dict(tag=tag,tend=t[-1]*1e6,err=err,ripple=ripple,pout=pout,gain=10*np.log10(max(pout,1e-9)/pin_w),eff=pout/(iin*13.8),iin=iin,h2=20*np.log10(va[2]/va[1]+1e-12),h3=20*np.log10(va[3]/va[1]+1e-12))
if __name__=='__main__':
    jobs=json.loads(sys.argv[1])
    with ThreadPoolExecutor(8) as ex:
        for r in ex.map(job,[(j['tag'],j.get('param',{}),j.get('pin','33'),j.get('model'),j.get('stop','8 us'),j.get('f','27.185 MHz')) for j in jobs]):
            print({k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items()})
