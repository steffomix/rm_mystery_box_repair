import sys,time
sys.path.insert(0,'/home/stefan/Dokumente/Coding/rm_italy_kl200_455_rev501/analyse/pylib')
from Xlib import display, X
from Xlib.ext import xtest
d=display.Display()
def click(x,y,double=False):
    xtest.fake_input(d,X.MotionNotify,x=x,y=y); d.sync(); time.sleep(0.2)
    for _ in range(2 if double else 1):
        xtest.fake_input(d,X.ButtonPress,1); xtest.fake_input(d,X.ButtonRelease,1); d.sync(); time.sleep(0.1)
    time.sleep(0.5)
if __name__=='__main__':
    click(int(sys.argv[1]),int(sys.argv[2]),len(sys.argv)>3)
