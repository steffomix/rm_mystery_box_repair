import sys,subprocess,os
sys.path.insert(0,'/tmp/qb'); sys.path.insert(0,'.')
import numpy as np
from netlist import netlist
from rd import load
os.environ['LD_LIBRARY_PATH']='/tmp/qb/inst/lib'
mode=sys.argv[1]
open(f'/tmp/qb/run/{mode}_sp.net','w').write(netlist(mode,'sp',sweep=("1 MHz","60 MHz",60)))
r=subprocess.run(['/tmp/qb/inst/bin/qucsator_rf','-i',f'/tmp/qb/run/{mode}_sp.net','-o',f'/tmp/qb/run/{mode}_sp.dat'],capture_output=True,text=True)
print(r.stderr[-300:])
d=load(f'/tmp/qb/run/{mode}_sp.dat')
f=np.array(d['frequency']);s21=np.array(d['S[1,2]']);s11=np.array(d['S[1,1]']);s22=np.array(d['S[2,2]'])
db=lambda x:round(20*np.log10(abs(x)),2)
for i in range(0,60,6): print(f[i]/1e6, db(s21[i]), db(s11[i]), db(s22[i]))
