"""uSimmics/QucsStudio-Schaltplan (.sch, Format 5.9) aus der Schaltungsbeschreibung erzeugen.

Verbindungen entstehen ueber kurze Draht-Stubs mit Netznamen (Wire-Labels); gleiche Namen
sind in uSimmics elektrisch verbunden.  Masse wird ueber GND-Symbole angeschlossen.
Pin-Geometrie (in uSimmics 5.9 verifiziert, Raster 10):
  R/C/L  : Pin1 (-30,0)  Pin2 (+30,0)
  Diode  : Kathode (-30,0)  Anode (+30,0)
  Vdc/Vac/Pac: Pin1 (0,-30)  Pin2 (0,+30)
  BJT    : Basis (-30,0)  Kollektor (0,-30)  Emitter (0,+30)
Rotation r: Basislage wird r-mal mit (x, y) -> (y, -x) gedreht.
"""

import re

from kl200_circuit import BJT_DEFAULTS, DIODE_DEFAULTS, PARAM, build

STUB = 20

# --------------------------------------------------------------------------
# Werte -> uSimmics-Schreibweise (ohne Einheiten, SI-Praefix)
# --------------------------------------------------------------------------
_PREFIX = {"G": 1e9, "M": 1e6, "k": 1e3, "": 1.0, "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15}


def to_float(s):
    s = str(s).strip().replace("µ", "u")
    m = re.fullmatch(r"([-+0-9.eE]+)\s*([GMkmunpf]?)(?:Ohm|F|H|V|W|Hz|A|s)?", s)
    if not m:
        raise ValueError(f"Wert nicht lesbar: {s!r}")
    return float(m.group(1)) * _PREFIX[m.group(2)]


def fmt(s):
    v = to_float(s)
    if v == 0:
        return "0"
    for p, f in (("G", 1e9), ("k", 1e3), ("", 1.0), ("m", 1e-3), ("u", 1e-6), ("n", 1e-9), ("p", 1e-12), ("f", 1e-15)):
        if abs(v) >= f * 0.9999999:
            x = v / f
            return f"{x:.6g}{p}"
    return f"{v:.6g}"


def fmt_freq(s):
    return f"{to_float(s):.10g}"


# --------------------------------------------------------------------------
# Komponenten-Zeilen
# --------------------------------------------------------------------------
BJT_ORDER = ["Type", "Is", "Nf", "Nr", "Ikf", "Ikr", "Vaf", "Var", "Ise", "Ne", "Isc", "Nc", "Bf", "Br",
             "Rbm", "Irb", "Rc", "Re", "Rb", "Cje", "Vje", "Mje", "Cjc", "Vjc", "Mjc", "Xcjc", "Cjs",
             "Vjs", "Mjs", "Fc", "Tf", "Xtf", "Vtf", "Itf", "Tr", "Temp", "Kf", "Af", "Ffe", "Kb", "Ab",
             "Fb", "Ptf", "Xtb", "Xti", "Eg", "Tnom", "Area"]
DIODE_ORDER = ["Is", "N", "Cj0", "M", "Vj", "Fc", "Cp", "Isr", "Nr", "Rs", "Tt", "Ikf", "Kf", "Af", "Ffe",
               "Bv", "Ibv", "Temp", "Xti", "Eg", "Tbv", "Trs", "Ttt1", "Ttt2", "Tm1", "Tm2", "Tnom"]


def _tok(values, shown=()):
    return "".join(f'"{v}"{1 if i in shown else 0}' for i, v in enumerate(values))


def _num(v):
    # Modellparameter: Zahlen mit SI-Praefix (z.B. "4p", "900p") in Gleitkomma wandeln
    try:
        return f"{to_float(v):.6g}"
    except ValueError:
        return str(v)


def comp_params(c):
    k, p = c["kind"], c["params"]
    if k == "R":
        return _tok([fmt(p["R"]), "26.85", "0.0", "0.0", "26.85", "european", "SIL-2"], {0})
    if k == "C":
        return _tok([fmt(p["C"]), "0"], {0})
    if k == "L":
        return _tok([fmt(p["L"]), "0"], {0})
    if k == "Vdc":
        return _tok([fmt(p["U"]), "battery", "SIL-2"], {0})
    if k == "Diode":
        d = {**DIODE_DEFAULTS, **p}
        return _tok([_num(d[n]) for n in DIODE_ORDER])
    if k == "BJT":
        d = {**BJT_DEFAULTS, **p}
        vals = [d[n] if n == "Type" else _num(d[n]) for n in BJT_ORDER] + ["7.02e-4", "1108.0", "SOT23"]
        return _tok(vals)
    raise ValueError(k)


QTYPE = {"R": "R", "C": "C", "L": "L", "Vdc": "Vdc", "Diode": "Diode", "BJT": "_BJT"}

# Basislage der Pins (Reihenfolge entspricht c["nodes"])
BASE_PINS = {
    "R": [(-30, 0), (30, 0)],
    "C": [(-30, 0), (30, 0)],
    "L": [(-30, 0), (30, 0)],
    "Vdc": [(0, -30), (0, 30)],
    "Vac": [(0, -30), (0, 30)],
    "Pac": [(0, -30), (0, 30)],
    "Diode": [(30, 0), (-30, 0)],  # Anode, Kathode
    "BJT": [(-30, 0), (0, -30), (0, 30)],
}


def rot(pt, r):
    x, y = pt
    for _ in range(r % 4):
        x, y = y, -x
    return x, y


# --------------------------------------------------------------------------
# Layout: Name -> (x, y, Rotation).  Zeilen = Funktionsbloecke.
# --------------------------------------------------------------------------
def layout():
    L = {}
    # Zeile 1: Versorgung
    L.update(V1=(100, 100, 0), D11=(260, 100, 3), Fuse1=(420, 100, 0), C31=(600, 100, 3),
             C29=(720, 100, 3), C30=(840, 100, 3), R12=(960, 100, 3), LED1a=(1080, 100, 1),
             R20=(1200, 100, 3), LED1b=(1320, 100, 1))
    # Zeile 2: VOX-Detektor
    L.update(C9=(100, 300, 0), D7=(280, 300, 3), D6=(440, 300, 2), C11=(600, 300, 3),
             C12=(720, 300, 3), C13=(840, 300, 3), R8=(1000, 300, 0), R19=(1160, 300, 3),
             Tr4=(1320, 300, 0))
    # Zeile 3: Relaissteuerung
    L.update(R18=(100, 500, 3), R17=(260, 500, 0), Tr1=(440, 500, 0), RL1=(600, 500, 3),
             D12=(720, 500, 3), D14=(840, 500, 1), RL2=(960, 500, 3), D13=(1080, 500, 3),
             C14=(1200, 500, 3))
    # Zeile 4: RX-Vorverstaerker
    L.update(R16=(100, 700, 3), C27=(220, 700, 3), R15=(340, 700, 3), D10=(460, 700, 1),
             R13=(580, 700, 3), Tr6=(740, 700, 0), R14=(880, 700, 3), C26=(1000, 700, 3),
             L1=(1160, 700, 0), D8=(1340, 700, 2), D9=(1500, 700, 2), C25=(1680, 700, 0),
             C28=(1860, 700, 0))
    # Zeile 5: PA Eingang und Transistor
    L.update(R9=(100, 900, 0), C15=(280, 900, 0), C16=(440, 900, 3), C17=(560, 900, 3),
             L2=(740, 900, 0), R11=(900, 900, 3), L3=(1020, 900, 3), Tr5=(1180, 900, 0),
             L4=(1340, 900, 3), C18=(1460, 900, 3))
    # Zeile 6: PA Ausgang
    L.update(L5=(100, 1100, 0), C19=(280, 1100, 3), C20=(400, 1100, 3), C21=(520, 1100, 3),
             C23=(700, 1100, 0))
    # Zeile 7: Hilfsbauteile und Quellen
    L.update(Rleak_c25=(100, 1300, 3), Rleak_c28=(220, 1300, 3), Rleak_pa_in=(100, 1300, 3),
             Rleak_pa_out=(220, 1300, 3))
    L.update(P1=(400, 1300, 0), P2=(520, 1300, 0), V2=(400, 1300, 0), Rsrc=(560, 1300, 0),
             Rload=(720, 1300, 3))
    return L


def pin_dir(pt):
    x, y = pt
    return (1 if x > 0 else -1 if x < 0 else 0, 1 if y > 0 else -1 if y < 0 else 0)


def sim_components(mode):
    """Quellen und Analysen je Betriebsart."""
    f = fmt_freq(PARAM["f"])
    items = []  # (kind, name, nodes, tokens-string)
    pin_dbm = PARAM["Pin_dBm"]
    if mode == "rx":
        items.append(("Pac", "P1", ["rtx", "gnd"], f'"1"1"50"1"0 dBm"0"{f}"0"26.85"0"con_2"0'))
        items.append(("Pac", "P2", ["ant", "gnd"], f'"2"1"50"1"0 dBm"0"{f}"0"26.85"0"con_2"0'))
    else:
        items.append(("Vac", "V2", ["vsrc", "gnd"], f'"Vpk"1"{f}"1"0"0"0"0'))
        items.append(("R", "Rsrc", ["vsrc", "rtx"],
                      _tok(["50", "26.85", "0.0", "0.0", "26.85", "european", "SIL-2"], {0})))
        items.append(("R", "Rload", ["ant", "gnd"],
                      _tok(["50", "26.85", "0.0", "0.0", "26.85", "european", "SIL-2"], {0})))
    return items, pin_dbm


def write_sch(mode, path, stop="2 us", points=801):
    comps = build(mode)
    lay = layout()
    lines, wires = [], []
    gnd_done = set()

    def place(kind, name, nodes, tokens, x, y, r, qtype=None):
        qtype = qtype or QTYPE[kind]
        tx, ty = (-26, -45) if r in (0, 2) and kind != "BJT" else (20, -10)
        lines.append(f"{qtype} {name} 1 {x} {y} {tx} {ty} {r} {tokens}")
        for node, base in zip(nodes, BASE_PINS[kind]):
            px, py = rot(base, r)
            ax, ay = x + px, y + py
            if node == "gnd":
                if pin_dir((px, py)) != (0, 1):
                    raise ValueError(f"{name}: GND-Pin nicht unten")
                lines.append(f"GND * 1 {ax} {ay} 0 0 0")
                continue
            dx, dy = pin_dir((px, py))
            ex, ey = ax + dx * STUB, ay + dy * STUB
            wires.append(f'{ax} {ay} {ex} {ey} "{node}" {ex} {ey} 0 ""')

    for c in comps:
        x, y, r = lay[c["name"]]
        place(c["kind"], c["name"], c["nodes"], comp_params(c), x, y, r)

    items, pin_dbm = sim_components(mode)
    for kind, name, nodes, tokens in items:
        x, y, r = lay[name]
        place(kind if kind in BASE_PINS else kind, name, nodes, tokens, x, y, r, qtype=kind)

    # Analysen
    if mode == "rx":
        lines.append('.SP SP1 1 400 1500 0 10 0 "lin"1"1 MHz"1"60 MHz"1"120"1"no"0"1"0"2"0"none"0')
    else:
        lines.append('Eqn Eqn1 1 100 1500 0 10 0 "Pin_dBm=%s="1"Pin_W=1e-3*10^(Pin_dBm/10)="1'
                     '"Vpk=2*sqrt(2*50*Pin_W)="1"yes"0' % pin_dbm)
        lines.append('.TR TR1 1 740 1500 0 10 0 "lin"1"0"1"%s"1"%d"1' % (stop, points))

    diagrams = []
    if mode == "rx":
        diagrams.append(
            '<Rect 1000 1600 400 300 31 #c0c0c0 1 00 1 0 0 0 1 0 1 0 1 0 0 0 315 0 225 "" "" "">\n'
            '\t<Legend 10 -100 0>\n'
            '\t<"dB(S[1,2])" "" #0000ff 1 3 0 0 0 0 "">\n'
            '\t<"dB(S[1,1])" "" #ff0000 1 3 0 0 0 0 "">\n'
            '\t<"dB(S[2,2])" "" #00aa00 1 3 0 0 0 0 "">\n'
            '</Rect>')
    else:
        diagrams.append(
            '<Rect 1000 1600 400 300 31 #c0c0c0 1 00 1 0 0 0 1 0 1 0 1 0 0 0 315 0 225 "" "" "">\n'
            '\t<Legend 10 -100 0>\n'
            '\t<"ant.Vt" "" #0000ff 1 3 0 0 0 0 "">\n'
            '\t<"rtx.Vt" "" #ff0000 1 3 0 0 0 0 "">\n'
            '</Rect>')

    out = ["<QucsStudio Schematic 5.9>", "<Properties>", "View=0,0,2400,2000,0.5,0,0",
           "Grid=10,10,1", "DataSet=*.dat", "DataDisplay=*.dpl", "OpenDisplay=1", "</Properties>",
           "<Symbol>", "</Symbol>", "<Components>"]
    out += lines
    out += ["</Components>", "<Wires>"] + wires + ["</Wires>", "<Diagrams>"] + diagrams + ["</Diagrams>",
            "<Paintings>", "</Paintings>"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
