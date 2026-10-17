import re,sys
def load(fn):
    t=open(fn).read()
    d={}
    for m in re.finditer(r'<(indep|dep) (\S+)[^>]*>\n(.*?)</\1>',t,re.S):
        vals=[]
        for x in m.group(3).split():
            x=x.strip()
            if not x: continue
            mm=re.match(r'^([+-][0-9.eE+-]+?)([+-])j([0-9.eE+-]+)$',x)
            if mm: vals.append(complex(float(mm.group(1)),float(mm.group(3))*(1 if mm.group(2)=='+' else -1)))
            else: vals.append(float(x))
        d[m.group(2)]=vals
    return d
