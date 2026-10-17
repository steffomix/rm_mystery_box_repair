from runner import *
J=[dict(tag=f"e3_L5_{l}",pin="33",param={"L5":f"{l} nH"}) for l in (40,50,60,70,80,100,120)]
J+=[dict(tag="e3_L5_60_R9",pin="33",param={"L5":"60 nH","R9":"15 Ohm"}),dict(tag="e3_L5_80_R9",pin="33",param={"L5":"80 nH","R9":"15 Ohm"})]
show(run_many(J,12))
