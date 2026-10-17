import sys,subprocess,os,time
sys.path.insert(0,'/tmp/qb'); sys.path.insert(0,'.')
import numpy as np
from netlist import netlist
from rd import load
os.environ['LD_LIBRARY_PATH']='/tmp/qb/inst/lib'
pin=sys.argv[1]
open('/tmp/qb/run/tx_hb.net','w').write(netlist('tx','hb',pin=pin,n=int(sys.argv[2]) if len(sys.argv)>2 else 5))
t=time.time()
r=subprocess.run(['/tmp/qb/inst/bin/qucsator_rf','-i','/tmp/qb/run/tx_hb.net','-o','/tmp/qb/run/tx_hb.dat'],capture_output=True,text=True)
print(time.time()-t, r.returncode); print((r.stderr+r.stdout)[-600:])
