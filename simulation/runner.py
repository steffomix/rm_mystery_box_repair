"""Hilfsfunktionen: Simulationen mit qucsator_rf (aus analyse/inst) starten und auswerten.

Nutzung (Beispiel):
    from runner import run_tr, run_sp
    r = run_tr(tag="basis", pin="33", stop="40 us")
    r = run_tr(tag="mit_R9", param={"R9": "15 Ohm"}, model={"Rb": "0.2"})
"""

import contextlib
import os
import re
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

import kl200_circuit as kc
from netlist import netlist

ROOT = Path(__file__).resolve().parent.parent
QUCSATOR = ROOT / "analyse" / "inst" / "bin" / "qucsator_rf"
ENV = {**os.environ, "LD_LIBRARY_PATH": str(ROOT / "analyse" / "inst" / "lib")}
WORK = ROOT / "analyse" / "run"
WORK.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()


@contextlib.contextmanager
def overrides(param=None, model=None):
    old_p, old_m = dict(kc.PARAM), {k: dict(v) for k, v in kc.MODEL.items()}
    kc.PARAM.update(param or {})
    kc.MODEL["MRF455"].update(model or {})
    try:
        yield
    finally:
        kc.PARAM.clear(); kc.PARAM.update(old_p)
        for k, v in old_m.items():
            kc.MODEL[k].clear(); kc.MODEL[k].update(v)


def load_dat(fn):
    text = Path(fn).read_text()
    out = {}
    for m in re.finditer(r"<(indep|dep) (\S+)[^>]*>\n(.*?)</\1>", text, re.S):
        vals = []
        for x in m.group(3).split():
            mm = re.match(r"^([+-][0-9.eE+-]+?)([+-])j([0-9.eE+-]+)$", x)
            if mm:
                vals.append(complex(float(mm.group(1)), float(mm.group(3)) * (1 if mm.group(2) == "+" else -1)))
            else:
                vals.append(float(x))
        out[m.group(2)] = vals
    return out


def _prepare(mode, analysis, param, model, **kw):
    with _lock, overrides(param, model):
        return netlist(mode, analysis, **kw)


def _simulate(tag, net):
    nf = WORK / f"{tag}.net"
    nf.write_text(net)
    r = subprocess.run([str(QUCSATOR), "-i", str(nf), "-o", str(nf.with_suffix(".dat"))],
                       capture_output=True, text=True, env=ENV)
    errs = [l for l in (r.stderr + r.stdout).splitlines() if "ERROR" in l]
    return nf.with_suffix(".dat"), errs


def analyse_tr(d, f0, pin_dbm, tail=8e-6, vsupply=13.8):
    """Kennwerte aus den letzten `tail` Sekunden der Transientenanalyse."""
    t = np.array(d["time"])
    T = 1 / f0
    t0 = t[-1] - tail
    n = int(round(tail / T))
    tg = np.arange(t[-1] - n * T, t[-1], T / 64)

    def fourier(key, harmonics=6):
        v = np.interp(tg, t, d[key])
        return [abs(np.mean(v * np.exp(-2j * np.pi * h * f0 * tg))) * (1 if h == 0 else 2) for h in range(harmonics)]

    va = fourier("ant.Vt")
    iin = -np.mean(np.interp(tg, t, d["V1.It"]))
    pout = va[1] ** 2 / 100
    pin_w = 1e-3 * 10 ** (pin_dbm / 10)
    # Spektrum: staerkste Linie, die nicht auf Harmonischen der Treiberfrequenz liegt
    ts = np.arange(t0, t[-1], 0.5e-9)
    v = np.interp(ts, t, d["ant.Vt"])
    spec = np.abs(np.fft.rfft((v - v.mean()) * np.hanning(len(v))))
    fr = np.fft.rfftfreq(len(v), 0.5e-9)
    carrier = spec[np.argmin(abs(fr - f0))] if pout > 1e-3 else spec.max()
    mask = (fr > 1e6) & (fr < 120e6)
    for k in range(1, 5):
        mask &= abs(fr - k * f0) > 0.35e6
    i = np.argmax(np.where(mask, spec, 0))
    spur_dbc = 20 * np.log10(spec[i] / carrier + 1e-12)
    # Huellkurvenschwankung der Grundwelle
    n16 = 16
    tg2 = np.arange(t0, t[-1] - T, T / n16)
    vv = np.interp(tg2, t, d["ant.Vt"])
    npr = len(vv) // n16
    env = np.abs(vv[: npr * n16].reshape(npr, n16) @ np.exp(-2j * np.pi * np.arange(n16) / n16)) * 2 / n16
    ripple = (env.max() - env.min()) / max(env.mean(), 1e-9)
    def phasor(key):
        v = np.interp(tg, t, d[key])
        return 2 * np.mean(v * np.exp(-2j * np.pi * f0 * tg))

    ph = {k: phasor(k + ".Vt") for k in ("vsrc", "rtx", "n_in", "n_a", "n_b", "n_c", "n_o", "ant")}
    i_src = (ph["vsrc"] - ph["rtx"]) / 50
    zin = ph["rtx"] / i_src
    gamma = abs((zin - 50) / (zin + 50))
    vswr = (1 + gamma) / max(1 - gamma, 1e-9)
    return dict(ph=ph, zin=zin, vswr=vswr, pout=pout, gain=10 * np.log10(max(pout, 1e-12) / pin_w), eff=pout / max(iin * vsupply, 1e-9),
                iin=iin, h2=20 * np.log10(va[2] / max(va[1], 1e-12) + 1e-12),
                h3=20 * np.log10(va[3] / max(va[1], 1e-12) + 1e-12),
                spur_dbc=spur_dbc, spur_mhz=fr[i] / 1e6, ripple=ripple,
                vant_pk=va[1], vcmax=float(np.max(np.interp(tg, t, d["n_c.Vt"]))))


def run_tr(tag, pin="33", f="27.185 MHz", stop="40 us", param=None, model=None, tail=8e-6):
    ppm = 400
    pts = int(float(stop.split()[0]) * ppm) + 1
    net = _prepare("tx", "tr", param, model, pin=pin, f=f, stop=stop, points=pts)
    dat, errs = _simulate(tag, net)
    res = dict(tag=tag, err=errs)
    if dat.exists():
        d = load_dat(dat)
        f0 = float(f.split()[0]) * 1e6
        res.update(analyse_tr(d, f0, float(pin), tail))
    return res


def run_sp(tag, mode="rx", param=None, model=None, start="1 MHz", stop="100 MHz", points=100, noise=False):
    net = _prepare(mode, "sp", param, model, sweep=(start, stop, points), noise=noise)
    dat, errs = _simulate(tag, net)
    return load_dat(dat), errs


def run_many(jobs, workers=10):
    """jobs: Liste von dicts mit den Argumenten von run_tr."""
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(lambda j: run_tr(**j), jobs))


def show(results, keys=("pout", "gain", "eff", "iin", "h2", "h3", "spur_dbc", "spur_mhz", "ripple", "vcmax")):
    for r in results:
        vals = " ".join(f"{k}={r[k]:.3g}" for k in keys if k in r)
        print(f"{r['tag']:<22} {'ERR ' + r['err'][0] if r['err'] else ''} {vals}")
