"""Qucs-Netzliste (qucsator_rf) aus der Schaltungsbeschreibung erzeugen."""

from kl200_circuit import PARAM, build


from kl200_circuit import BJT_DEFAULTS, DIODE_DEFAULTS


def _prop(params):
    return " ".join(f'{k}="{v}"' for k, v in params.items())


def circuit_lines(comps):
    out = []
    for c in comps:
        nodes = list(c["nodes"])
        params = dict(c["params"])
        if c["kind"] == "BJT":
            nodes.append("gnd")  # Substratknoten
            params = {**BJT_DEFAULTS, **params}
        elif c["kind"] == "Diode":
            nodes.reverse()  # qucsator erwartet Kathode zuerst, die Beschreibung Anode zuerst
            params = {**DIODE_DEFAULTS, **params}
        out.append(f'{c["kind"]}:{c["name"]} {" ".join(nodes)} {_prop(params)}')
    return out


def netlist(mode, analysis, **kw):
    comps = build(mode)
    L = ["# KL200/P Rel. 5.04 - Modus " + mode, ""]
    L += circuit_lines(comps)
    L.append("")
    f = kw.get("f", PARAM["f"])
    if analysis == "tr":
        # Quelle: Vac mit 50 Ohm Innenwiderstand -> Pin = (Vpk/2)^2 / (2*50)
        L.append(f'Eqn:Eqn1 Pin_dBm="{kw.get("pin", PARAM["Pin_dBm"])}" Pin_W="1e-3*10^(Pin_dBm/10)" Vpk="2*sqrt(2*50*Pin_W)" Export="yes"')
        L.append('Vac:V2 vsrc gnd U="Vpk" f="%s" Phase="0" Theta="0"' % f)
        L.append('R:Rsrc vsrc rtx R="50 Ohm"')
        L.append('R:Rload ant gnd R="50 Ohm"')
        stop = kw.get("stop", "12 us")
        pts = kw.get("points", 6001)
        L.append('.TR:TR1 Type="lin" Start="0" Stop="%s" Points="%d" IntegrationMethod="Gear" Order="2" '
                 'InitialStep="1 ns" MinStep="1e-16" MaxIter="150" reltol="0.001" abstol="1 pA" vntol="1 uV" '
                 'Temp="26.85" LTEreltol="1e-3" LTEabstol="1e-6" LTEfactor="1" Solver="CroutLU" relaxTSR="no" '
                 'initialDC="yes" MaxStep="1 ns"' % (stop, pts))
    elif analysis == "sp":
        L.append('Pac:P1 rtx gnd Num="1" Z="50 Ohm" P="0 W" f="%s"' % f)
        L.append('Pac:P2 ant gnd Num="2" Z="50 Ohm" P="0 W" f="%s"' % f)
        L.append('.DC:DC1 Temp="26.85" reltol="0.001" abstol="1 pA" vntol="1 uV" saveOPs="no" MaxIter="150"')
        a, b, n = kw.get("sweep", ("1 MHz", "100 MHz", 100))
        L.append('.SP:SP1 Type="lin" Start="%s" Stop="%s" Points="%d"' % (a, b, n))
    elif analysis == "dc":
        L.append('Pac:P1 rtx gnd Num="1" Z="50 Ohm" P="0 W" f="%s"' % f)
        L.append('Pac:P2 ant gnd Num="2" Z="50 Ohm" P="0 W" f="%s"' % f)
        L.append('.DC:DC1 Temp="26.85" reltol="0.001" abstol="1 pA" vntol="1 uV" saveOPs="yes" MaxIter="150"')
    return "\n".join(L) + "\n"
