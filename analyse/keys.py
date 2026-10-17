import sys,time
sys.path.insert(0,'/home/stefan/Dokumente/Coding/rm_italy_kl200_455_rev501/analyse/pylib')
from Xlib import display, X, XK
from Xlib.ext import xtest
d=display.Display()
def key(name,shift=False,ctrl=False):
    k=d.keysym_to_keycode(XK.string_to_keysym(name))
    if ctrl: xtest.fake_input(d,X.KeyPress,d.keysym_to_keycode(XK.string_to_keysym('Control_L')))
    if shift: xtest.fake_input(d,X.KeyPress,d.keysym_to_keycode(XK.string_to_keysym('Shift_L')))
    xtest.fake_input(d,X.KeyPress,k); xtest.fake_input(d,X.KeyRelease,k)
    if shift: xtest.fake_input(d,X.KeyRelease,d.keysym_to_keycode(XK.string_to_keysym('Shift_L')))
    if ctrl: xtest.fake_input(d,X.KeyRelease,d.keysym_to_keycode(XK.string_to_keysym('Control_L')))
    d.sync(); time.sleep(0.3)
if __name__=='__main__':
    for a in sys.argv[1:]:
        key(a)
