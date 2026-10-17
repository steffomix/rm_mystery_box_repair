"""Erzeugt aus kl200_circuit.py die uSimmics-Schaltplaene (und optional Netzlisten).

Aufruf:  python3 build.py
Ausgabe: kl200_rx.sch / kl200_tx.sch (Vorher) und kl200_rx_opt.sch / kl200_tx_opt.sch (Nachher)
"""

from pathlib import Path

import kl200_circuit as kc
from schematic import write_sch

OUT = Path(__file__).resolve().parent

if __name__ == "__main__":
    for mode in ("rx", "tx"):
        write_sch(mode, OUT / f"kl200_{mode}.sch")  # Vorher (IST: R9 = Drahtbruecke)
    saved = dict(kc.PARAM)
    kc.PARAM.update(kc.OPTIMIERT)
    for mode in ("rx", "tx"):
        write_sch(mode, OUT / f"kl200_{mode}_opt.sch")  # Nachher
    kc.PARAM.clear()
    kc.PARAM.update(saved)
    print("geschrieben: kl200_{rx,tx}.sch (vorher) und kl200_{rx,tx}_opt.sch (nachher)")
