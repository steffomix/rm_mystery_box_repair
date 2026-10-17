from runner import *
J=[dict(tag="e1_basis",pin="33"),
   dict(tag="e1_nodrive",pin="-20"),
   dict(tag="e1_R9_15",pin="33",param={"R9":"15 Ohm"}),
   dict(tag="e1_R9_15_nodrive",pin="-20",param={"R9":"15 Ohm"}),
   dict(tag="e1_Le2n",pin="33",param={"Le5":"2 nH"}),
   dict(tag="e1_Le5n",pin="33",param={"Le5":"5 nH"}),
   dict(tag="e1_Rb1",pin="33",model={"Rb":"1","Rc":"0.3","Re":"0.1"}),
   dict(tag="e1_Cjc100",pin="33",model={"Cjc":"100p","Cje":"500p"}),
   dict(tag="e1_L2_50",pin="33",param={"L2":"50 nH"}),
   dict(tag="e1_L2_130",pin="33",param={"L2":"130 nH"})]
show(run_many(J,10))
