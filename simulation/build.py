"""Erzeugt aus kl200_circuit.py die uSimmics-Schaltplaene (und optional Netzlisten).

Aufruf:  python3 build.py
Ausgabe: kl200_rx.sch (Empfang, S-Parameter) und kl200_tx.sch (Senden, Transient)
"""

from pathlib import Path

from schematic import write_sch

OUT = Path(__file__).resolve().parent

if __name__ == "__main__":
    write_sch("rx", OUT / "kl200_rx.sch")
    write_sch("tx", OUT / "kl200_tx.sch")
    print("geschrieben:", OUT / "kl200_rx.sch", OUT / "kl200_tx.sch")
