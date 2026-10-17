exec(open('experiments/exp7.py').read().split("V=[")[0])
V=[("C26=680p",{"C26":"680 pF"}),("C26=1n_R14=220",{"C26":"1 nF","R14":"220 Ohm"}),("C26=1n_R15=22k",{"C26":"1 nF","R15":"22 kOhm"}),
   ("C26=1n_R14=220_R15=15k",{"C26":"1 nF","R14":"220 Ohm","R15":"15 kOhm"}),("C26=680p_R14=150",{"C26":"680 pF","R14":"150 Ohm"}),
   ("C26=1n_R14=330",{"C26":"1 nF","R14":"330 Ohm"}),("C26=2.2n_R14=330",{"C26":"2.2 nF","R14":"330 Ohm"}),("R14=47_C26=470p_R13=4.7k",{"R14":"47 Ohm","R13":"4.7 kOhm"})]
for name,ov in V:
    d,err=run_sp("e7b_"+name.replace("=","_"),"rx",param={"OV":ov},start="1 MHz",stop="100 MHz",points=100)
    r=analyse(d)
    print(f"{name:26s} G27={r['g27']:.1f} G26-30=[{r['g_26_30'][0]:.1f},{r['g_26_30'][1]:.1f}] S22_27={r['s22_27']:.2f} S22max={r['s22max']:.2f}@{r['s22max_f']:.0f}MHz")
