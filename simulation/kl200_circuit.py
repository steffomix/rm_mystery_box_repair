"""RM Italy KL 200/P Rel. 5.04 - Schaltungsbeschreibung (Single Source of Truth).

Aus dieser Beschreibung werden erzeugt:
  * Qucs-Netzliste (.net) fuer qucsator_rf  -> netlist.py
  * uSimmics/QucsStudio-Schaltplan (.sch)    -> schematic.py / build.py

Alle Netznamen entsprechen der Schaltung `images/schaltung_v5.04.png`.
Bauteilwerte stammen aus `bauteilliste.md`; nicht dokumentierte Werte (Spulen,
Transistor- und Relaismodelle) sind als ANNAHME markiert und stehen zentral in PARAM.
"""

# --------------------------------------------------------------------------
# Parameter (Annahmen stehen als Kommentar dabei)
# --------------------------------------------------------------------------
import re

# Optimierte Bauteilwerte ("Nachher"), Begruendung siehe analyse-bericht.md
OPTIMIERT = {
    "R9": "15 Ohm",           # Drahtbruecke -> 15 Ohm laut Bauteilliste
    "L2": "70 nH",            # Ziel-Induktivitaet (vorher Annahme 85 nH)
    "L5": "60 nH",            # Ziel-Induktivitaet (vorher Annahme 80 nH)
    "OV": {"C18": "470 pF", "R14": "330 Ohm", "C26": "2.2 nF"},
}

PARAM = {
    "OV": {},                 # Analyse: Bauteilwerte ueberschreiben
    "SCALE": {},              # Analyse: Bauteilwerte skalieren (Toleranz/Temperatur)
    "Vbat": "13.8 V",
    "Fuse_R": "10 mOhm",      # ANNAHME: 12 A Schmelzsicherung, Kaltwiderstand
    "Rcoil": "360 Ohm",       # ANNAHME: Finder 30.22 12 V, ~0.4 W Spule
    "L1": "10 uH",            # Bauteilliste
    # L2-L5: Induktivitaeten sind nicht dokumentiert. Abschaetzung (Wheeler, Luftspule) aus den
    # Wickeldaten des aelteren Handbuchs RN-kl200p v3.1.0 (history/):
    #   3 Wdg. d=8 mm, Draht 0,8 mm  -> ca. 80-95 nH   (L2 ANRA 289)
    #   3 Wdg. d=8 mm, Draht 1,2 mm  -> ca. 75-80 nH   (L5 ANRA 289/3)
    #  12 Wdg. d=6 mm, Draht 1,0 mm  -> ca. 0,35 uH    (L4 ANRA 455)
    "L2": "85 nH",
    "L3": "3 uH",             # ANNAHME: VK200 Ferritdrossel
    "L4": "0.35 uH",
    "L5": "80 nH",
    "Le5": "3 nH",           # ANNAHME: Emitter-Zuleitung/Bonddraht Tr5; ohne (0) schwingt das Modell bei Grosssignal
    "R9": "1 mOhm",          # Platine IST: Drahtbruecke statt 15 Ohm (SOLL laut Bauteilliste: 15 Ohm)
    "f": "27.185 MHz",        # CB Kanal 19 (nur Arbeitspunkt der Simulation)
    "Pin_dBm": "33",          # 2 W Treiberleistung
}

# --------------------------------------------------------------------------
# Halbleitermodelle (ANNAHMEN, grobe Naeherungen typischer Datenblattwerte)
# --------------------------------------------------------------------------
MODEL = {
    "1N4148": dict(Is="2.52e-9", N="1.752", Cj0="4p", M="0.4", Vj="0.5", Rs="0.568", Tt="20n", Bv="100"),
    "1N4007": dict(Is="76.9p", N="1.45", Cj0="26.5p", M="0.333", Vj="0.5", Rs="0.0342", Tt="4.32u", Bv="1000"),
    "1N5400": dict(Is="30n", N="1.8", Cj0="60p", M="0.4", Vj="0.5", Rs="0.02", Tt="2u", Bv="50"),
    "LED": dict(Is="1e-18", N="2", Cj0="30p", M="0.33", Vj="0.75", Rs="3", Tt="1n", Bv="5"),
    "BC547": dict(Type="npn", Is="1.8e-14", Nf="1", Nr="1", Ikf="0.14", Vaf="80", Ise="5e-14",
                  Ne="1.46", Bf="400", Br="35", Rb="10", Rc="1", Re="0.6", Cje="11p", Vje="0.5",
                  Mje="0.33", Cjc="4p", Vjc="0.5", Mjc="0.33", Tf="0.5n", Tr="10n"),
    "BF199": dict(Type="npn", Is="2e-15", Nf="1", Nr="1", Vaf="50", Bf="100", Br="5", Rb="20",
                  Rc="5", Re="1", Cje="2p", Vje="0.7", Mje="0.33", Cjc="0.7p", Vjc="0.6",
                  Mjc="0.33", Tf="0.25n", Tr="5n"),
    # ANNAHME: Typische MRF455/MS1051-Groessenordnung (60 W, 12.5 V, 30 MHz)
    # Orientiert an SD1446/MRF455-Datenblaettern: Cob ~250-300 pF, hFE >= 10, Ic max ~12 A,
    # eta ~55 %. Die Serienwiderstaende sind so gewaehlt, dass der Wirkungsgrad realistisch bleibt.
    "MRF455": dict(Type="npn", Is="1e-12", Nf="1", Nr="1", Ikf="8", Vaf="50", Bf="50", Br="5",
                   Rb="0.1", Rc="0.12", Re="0.03", Cje="900p", Vje="0.75", Mje="0.33",
                   Cjc="250p", Vjc="0.75", Mjc="0.4", Tf="0.4n", Tr="5n"),
}


# Vollstaendige Parameterlisten in der Reihenfolge der uSimmics/Qucs-Dialoge.
BJT_DEFAULTS = dict(
    Type="npn", Is="1e-16", Nf="1", Nr="1", Ikf="0", Ikr="0", Vaf="0", Var="0", Ise="0", Ne="1.5",
    Isc="0", Nc="2", Bf="100", Br="1", Rbm="0", Irb="0", Rc="0", Re="0", Rb="0", Cje="0",
    Vje="0.75", Mje="0.33", Cjc="0", Vjc="0.75", Mjc="0.33", Xcjc="1", Cjs="0", Vjs="0.75",
    Mjs="0", Fc="0.5", Tf="0", Xtf="0", Vtf="0", Itf="0", Tr="0", Temp="26.85", Kf="0", Af="1",
    Ffe="1", Kb="0", Ab="1", Fb="1", Ptf="0", Xtb="0", Xti="3", Eg="1.11", Tnom="26.85", Area="1",
)
DIODE_DEFAULTS = dict(
    Is="1e-15", N="1", Cj0="10f", M="0.5", Vj="0.7", Fc="0.5", Cp="0", Isr="0", Nr="2", Rs="0",
    Tt="0", Ikf="0", Kf="0", Af="1", Ffe="1", Bv="0", Ibv="1e-3", Temp="26.85", Xti="3", Eg="1.11",
    Tbv="0", Trs="0", Ttt1="0", Ttt2="0", Tm1="0", Tm2="0", Tnom="26.85", Area="1",
)


_PREFIX = {"G": 1e9, "M": 1e6, "k": 1e3, "": 1.0, "m": 1e-3, "u": 1e-6, "n": 1e-9, "p": 1e-12, "f": 1e-15}


def to_float(s):
    """'4.7 kOhm' -> 4700.0 (Einheiten werden ignoriert)."""
    m = re.fullmatch(r"([-+0-9.eE]+)\s*([GMkmunpf]?)(?:Ohm|F|H|V|W|Hz|A|s)?", str(s).strip().replace("µ", "u"))
    if not m:
        raise ValueError(f"Wert nicht lesbar: {s!r}")
    return float(m.group(1)) * _PREFIX[m.group(2)]


def build(mode):
    """Liefert die Bauteilliste.  mode = 'tx' oder 'rx' (Relaisstellung).

    RL1 (Vorverstaerker): RX = angezogen (Preamp im Pfad), TX = abgefallen (Bypass).
    RL2 (PA):             TX = angezogen (PA im Pfad),      RX = abgefallen (Bypass).
    Die Kontakte werden als Netzbruecken modelliert (gleicher Netzname).
    """
    tx = mode == "tx"
    comps = []

    def add(kind, name, nodes, **params):
        comps.append(dict(kind=kind, name=name, nodes=list(nodes), params=params))

    def diode(name, a, k, model):
        add("Diode", name, [a, k], **MODEL[model])

    def bjt(name, b, c, e, model):
        add("BJT", name, [b, c, e], **MODEL[model])

    # ---------------- Versorgung ----------------
    add("Vdc", "V1", ["vin", "gnd"], U=PARAM["Vbat"])
    diode("D11", "gnd", "vin", "1N5400")
    add("R", "Fuse1", ["vin", "vcc"], R=PARAM["Fuse_R"])
    add("C", "C31", ["vcc", "gnd"], C="470 nF")
    add("C", "C29", ["vcc", "gnd"], C="100 nF")
    add("C", "C30", ["vcc", "gnd"], C="100 uF")
    add("R", "R12", ["vcc", "led1"], R="1 kOhm")
    add("R", "R20", ["vcc", "led2"], R="1 kOhm")
    diode("LED1a", "led1", "gnd", "LED")
    diode("LED1b", "led2", "gnd", "LED")

    # ---------------- HF-Erkennung (VOX) und Relaissteuerung ----------------
    add("C", "C9", ["rtx", "c9"], C="8.2 pF")
    diode("D7", "gnd", "c9", "1N4148")
    diode("D6", "c9", "rect", "1N4148")
    add("C", "C11", ["rect", "gnd"], C="4.7 uF")
    add("C", "C12", ["rect", "gnd"], C="47 uF")
    add("C", "C13", ["rect", "gnd"], C="100 nF")
    add("R", "R8", ["rect", "b4"], R="4.7 kOhm")
    add("R", "R19", ["b4", "gnd"], R="2.2 kOhm")
    bjt("Tr4", "b4", "x", "gnd", "BC547")
    add("R", "R18", ["vcc", "x"], R="2.2 kOhm")
    add("R", "R17", ["x", "b1"], R="12 kOhm")
    bjt("Tr1", "b1", "c1", "gnd", "BC547")
    add("R", "RL1", ["vcc", "c1"], R=PARAM["Rcoil"])
    diode("D12", "c1", "vcc", "1N4007")
    diode("D14", "vcc", "d14k", "1N4007")
    add("R", "RL2", ["d14k", "x"], R=PARAM["Rcoil"])
    diode("D13", "x", "d14k", "1N4007")
    add("C", "C14", ["x", "gnd"], C="10 nF")

    # ---------------- RX-Vorverstaerker (BF199) ----------------
    add("R", "R16", ["vcc", "p"], R="100 Ohm")
    add("C", "C27", ["p", "gnd"], C="10 nF")
    add("R", "R15", ["p", "m"], R="12 kOhm")
    diode("D10", "m", "q", "1N4148")
    add("R", "R13", ["q", "gnd"], R="2.2 kOhm")
    bjt("Tr6", "q", "col6", "em6", "BF199")
    add("R", "R14", ["em6", "gnd"], R="100 Ohm")
    add("C", "C26", ["em6", "gnd"], C="470 pF")
    add("L", "L1", ["p", "col6"], L=PARAM["L1"])
    diode("D8", "p", "col6", "1N4148")
    diode("D9", "col6", "p", "1N4148")
    add("C", "C25", ["col6", "c25"], C="150 pF")
    add("C", "C28", ["m", "c28"], C="56 pF")

    # ---------------- Leistungsverstaerker ----------------
    add("R", "R9", ["pa_in", "n_in"], R=PARAM["R9"])
    add("C", "C15", ["n_in", "n_a"], C="100 pF")
    add("C", "C16", ["n_a", "gnd"], C="220 pF")
    add("C", "C17", ["n_a", "gnd"], C="270 pF")
    add("L", "L2", ["n_a", "n_b"], L=PARAM["L2"])
    add("R", "R11", ["n_b", "gnd"], R="10 Ohm")
    add("L", "L3", ["n_b", "gnd"], L=PARAM["L3"])
    if PARAM["Le5"] not in ("0", "0 nH"):
        bjt("Tr5", "n_b", "n_c", "n_e5", "MRF455")
        add("L", "Le5", ["n_e5", "gnd"], L=PARAM["Le5"])
    else:
        bjt("Tr5", "n_b", "n_c", "gnd", "MRF455")
    add("L", "L4", ["vcc", "n_c"], L=PARAM["L4"])
    add("C", "C18", ["n_c", "gnd"], C="120 pF")
    add("L", "L5", ["n_c", "n_o"], L=PARAM["L5"])
    add("C", "C19", ["n_o", "gnd"], C="220 pF")
    add("C", "C20", ["n_o", "gnd"], C="270 pF")
    add("C", "C21", ["n_o", "gnd"], C="120 pF")
    add("C", "C23", ["n_o", "pa_out"], C="1 nF")

    # ---------------- Relaiskontakte als Netzbruecken ----------------
    if tx:
        bridge = {"pa_in": "rtx", "pa_out": "ant"}     # Bypass-RL1 + RL2 angezogen
        floating = ["c25", "c28"]                       # Preamp-Kontakte offen
    else:
        bridge = {"c25": "rtx", "c28": "ant"}           # RL1 angezogen, RL2 Bypass
        floating = ["pa_in", "pa_out"]                  # PA-Kontakte offen
    for c in comps:
        c["nodes"] = [bridge.get(n, n) for n in c["nodes"]]
    # Wertvariationen fuer Analysen: PARAM["OV"] = {"R14": "68 Ohm"}, PARAM["SCALE"] = {"C16": 0.97}
    for c in comps:
        key = {"R": "R", "C": "C", "L": "L"}.get(c["kind"])
        if key is None:
            continue
        if c["name"] in PARAM["OV"]:
            c["params"][key] = PARAM["OV"][c["name"]]
        if c["name"] in PARAM["SCALE"]:
            c["params"][key] = f"{to_float(c['params'][key]) * PARAM['SCALE'][c['name']]:.6g}"
    for n in floating:
        add("R", "Rleak_" + n, [n, "gnd"], R="1 GOhm")  # nur fuer DC-Konvergenz
    return comps
