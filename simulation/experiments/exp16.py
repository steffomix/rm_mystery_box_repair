exec(open('experiments/exp7.py').read().split("V=[")[0])
for name,ov in (("opt C26=1.8n",{"C26":"1.8 nF","R14":"330 Ohm"}),("opt C26=2.2n",{"C26":"2.2 nF","R14":"330 Ohm"}),("opt C26=2.7n",{"C26":"2.7 nF","R14":"330 Ohm"}),("opt C26=2.2n R14=390",{"C26":"2.2 nF","R14":"390 Ohm"}),("opt C26=2.2n R14=270",{"C26":"2.2 nF","R14":"270 Ohm"}),("opt C26=1.5n R14=330",{"C26":"1.5 nF","R14":"330 Ohm"})):
    d,err=run_sp("e16_"+name.replace(" ","_"),"rx",param={"OV":ov},start="1 MHz",stop="100 MHz",points=100)
    r=analyse(d)
    print(f"{name:22s} G27={r['g27']:.1f} G26-30=[{r['g_26_30'][0]:.1f},{r['g_26_30'][1]:.1f}] S22_27={r['s22_27']:.2f} S22max={r['s22max']:.2f}@{r['s22max_f']:.0f}MHz")
