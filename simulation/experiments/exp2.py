from runner import *
J=[]
for le in ("1 nH","2 nH","3 nH","4 nH"):
    for rb in ("0.1","0.5"):
        J.append(dict(tag=f"e2_le{le[0]}_rb{rb}",pin="33",param={"Le5":le},model={"Rb":rb}))
show(run_many(J,12))
