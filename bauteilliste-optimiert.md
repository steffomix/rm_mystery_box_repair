# Bauteilliste: Vorher / Nachher (optimiert)

Zugehörig: [analyse-bericht.md](./analyse-bericht.md) (Begründung, Zahlen, Grenzen)
Quellen für „Vorher": [bauteilliste.md](./bauteilliste.md) (Original RM Italy Rel. 5.04) und die IST-Spalte im [README.md](./README.md).

> **Hinweis:** Die Änderungen sind **Simulationsergebnisse mit geschätzten Spulen- und Transistorwerten**. Sie sind Vorschläge zum schrittweisen Prüfen am Gerät (Abschnitt „Umbaureihenfolge"), kein Freigabenachweis.
> Zeichen: ✅ geändert · ➖ unverändert (untersucht oder unkritisch) · ❔ nicht untersucht, unverändert.

---

## 1. Erwarteter Effekt im Modell (Kurzfassung)

| Größe | Vorher | Nachher |
|---|---|---|
| Ausgangsleistung bei 5 W Ansteuerung (Mittel, ± Toleranzen) | 21,6 W (16–25 W) | **44,2 W (33–48 W)** |
| Gain bei 5 W | 5,8 dB (Kompression) | **9,6 dB** |
| Eingangs-VSWR bei 5 W (Mittel, Bereich) | 16 (8–29) | **3,1 (2,6–4,4)** |
| Kollektor-Spitzenspannung bei 5 W | 76 V (58–85 V) | **38 V (31–44 V)** |
| H2 / H3 bei 5 W | −21 / −34 dBc | **−31 / −47 dBc** |
| Leistung 26 → 29,7 MHz (2 W Ansteuerung) | 27,1 → 7,6 W | **18,6 → 16,1 W** |
| RX-Vorverstärker: |S22| am Antennenanschluss | **+1,1 dB** (> 0 dB, bedingt stabil) | **−0,2 dB** (< 0 dB im ganzen Band) |
| RX-Vorverstärker: Rauschzahl bei 27 MHz | 4,6 dB | **3,5 dB** |
| RX-Vorverstärker: Gain, 26–30 MHz | 15,7 dB (15,4–16,3) | **16,1 dB (flach)** |
| RX-Vorverstärker: Ruhestrom | 10 mA | 4 mA |

Toleranzstreuung (Monte-Carlo, 10 Läufe): Spulen ± 10 %, Kondensatoren ± 5 % (Vorher) bzw. ± 2 % (Nachher).

---

## 2. Gegenüberstellung

### 2.1 Endstufe (TX) und Ausgangsnetzwerk

| ID | Original (RM-Liste) | IST (README) | **Nachher** | | Begründung |
|---|---|---|---|---|---|
| **R9** | 15 Ω 2 W | **fehlt**, Drahtbrücke | **15 Ω / 2 W, induktionsarm (Metalloxid oder Metallfilm)** | ✅ | VSWR 9,4 → 7,5 (2 W) bzw. 21,6 → 13,9 (5 W) bei gleicher Leistung (±1 %). R9 verbraucht 0,4–0,8 W. Drahtwiderstand nicht simuliert, wegen Eigeninduktivität bei 27 MHz nicht empfohlen. |
| **L2** | ANRA 289 | ANRA 289 | **Abgleich auf ≈ 70 nH** | ✅ | Eingangsresonanz mit C16∥C17. Optimum 60–70 nH (Modell). L2 +30 % senkt Pout um 64 %. **Ist-Wert unbekannt: erst messen**, dann auf 70 nH einstellen. Annahme „Vorher" war 85 nH. |
| **L5** | ANRA 289/3 | ANRA 289/3 | **Abgleich auf ≈ 60 nH** | ✅ | Ausgangskreis. Bei ≥ 70 nH kippt der Betrieb in hohe Kollektorspannung (56–87 V). 60 nH liegt auf einem breiten Plateau. **Ist-Wert unbekannt: erst messen.** Annahme „Vorher" war 80 nH. |
| **C15** | 100 pF 50 V NP0 | Kerko 101J (5 %) | 100 pF, **± 2 %** (C0G oder Glimmer), 50 V | ✅ | Teil des selektiven Eingangskreises. Spannung 19 V Spitze bei 5 W. Der Wert bleibt gleich, nur die Toleranz wird enger. |
| **C16** | 220 pF 50 V N750 | Kerko NP0 221J | **220 pF Silberglimmer ± 2 %**, ≥ 100 V | ✅ | Eingangskreis: Toleranz und Temperaturdrift. 17–25 V Spitze bei 5 W (bei 10 W ≈ 34 V). Der Spannungsspielraum zu 50 V ist begrenzt, deshalb ≥ 100 V. |
| **C17** | 270 pF 50 V N750 | Kerko SL 271J | **270 pF Silberglimmer ± 2 %**, ≥ 100 V | ✅ | wie C16 |
| **C18** | 120 pF 500 V NP0 | Kerko NP0 121J | **470 pF Silberglimmer ± 2 %, 500 V** | ✅ | Größtes Einzelhebel für Oberwellen: H2 −23 → −29 dBc, H3 −34 → −45 dBc, Kollektor-Spitze 38 → 31 V, Wirkungsgrad 31 → 40 % (bei 2 W; 680 pF noch besser, 470 pF als Kompromiss). Strom ≈ 0,9 A eff. |
| **C19** | 220 pF 500 V N750 | Kerko NP0 221J | **220 pF Silberglimmer ± 2 %, 500 V** | ✅ | Strom bis 1,8 A eff. Verlust 174 mW (Keramik) gegen 44 mW (Glimmer), jeweils Modellannahme tanδ 2·10⁻³ bzw. 5·10⁻⁴. Entspricht der README-Empfehlung. |
| **C20** | 270 pF 500 V N750 | Kerko SL 271J | **270 pF Silberglimmer ± 2 %, 500 V** | ✅ | Höchste Belastung: **2,2 A eff.**, 214 mW (Keramik) gegen 53 mW (Glimmer). |
| **C21** | 120 pF 500 V NP0 | Kerko NP0 121J | **120 pF Silberglimmer ± 2 %, 500 V** | ✅ | 1,0 A eff., 95 mW gegen 24 mW. |
| **C23** | 1,0 nF 500 V | Kerko B 102K | 1,0 nF 500 V (Typ wie bisher) | ➖ | 8 V Spitze, 11 mW Verlust. Keine Änderung nötig. |
| **L3** | VK200 | VK200 | VK200 | ➖ | Parametersweep 1–10 µH: < 1 % Einfluss. |
| **L4** | ANRA 455 | ANRA 455 | ANRA 455 | ➖ | Sweep 0,2–1,5 µH: < 3 % Einfluss. |
| **R11** | 10 Ω 0,5 W | OK | 10 Ω 0,5 W | ❔ | nicht einzeln variiert |
| **TR5** | MRF455 | MRF455 (oder SD1446) | unverändert | ➖ | Modell **nicht** exakt. Bei Umbau Emitterzuleitung nicht verändern (Modell schwingt ohne Zuleitungsinduktivität). |

### 2.2 Empfangszweig (RX-Vorverstärker)

| ID | Original (RM-Liste) | IST (README) | **Nachher** | | Begründung |
|---|---|---|---|---|---|
| **R14** | 100 Ω 0,25 W | OK | **330 Ω 0,25 W** (1 %) | ✅ | Emitter-Gegenkopplung. Mit C26 = 2,2 nF: |S22| < 0 dB im ganzen Band, Gain 16,1 dB flach, Rauschzahl 3,5 dB. 270–390 Ω unkritisch (Gain 15,4–16,9 dB). |
| **C26** | 470 pF 50 V N750 | Kerko SL 471J | **2,2 nF**, C0G oder X7R, 50 V | ✅ | Emitter-Bypass. Toleranz unkritisch: 1,8–2,7 nF bleiben im Gain ± 0,1 dB. **Achtung:** zu klein (100 pF) bricht der Gain auf 4,5 dB ein. |
| **C25** | 150 pF 50 V NP0 | Kerko NP0 151J | unverändert | ➖ | 47–330 pF: ± 1 dB Gain. |
| **C28** | 56 pF 50 V NP0 | Kerko NP0 56J | unverändert | ➖ | 33–100 pF: Gain 14,2–16,7 dB. Kein Stabilitätsgewinn. |
| **R13** | 2,2 kΩ 0,25 W | OK | unverändert | ➖ | 4,7 kΩ ändert den Gain um 0,5 dB, S22 wird schlechter. |
| **R15** | 12 kΩ 0,25 W | OK | unverändert | ➖ | 22 kΩ senkt Gain (13,7 dB) und S22 nur wenig. |
| **R16** | 100 Ω 0,25 W | OK | unverändert | ➖ | 220 Ω: kaum Wirkung. |
| **C27** | 10 nF 50 V | Kerko 103Z | unverändert | ❔ | |
| **L1** | 10 µH | OK | unverändert | ❔ | |
| **D8, D9, D10** | 1N4148 | OK | unverändert | ❔ | |
| **TR6** | BF199 | OK | unverändert | ➖ | Arbeitspunkt Ic 10 → 4 mA durch R14, Vce 12,1 V. Großsignalverhalten nicht untersucht. |

### 2.3 Relais-Steuerung (VOX), Versorgung und Sonstiges

Dieser Teil wurde **nicht** optimiert und bleibt unverändert.

| ID | Original (RM-Liste) | IST (README) | Nachher | | Anmerkung |
|---|---|---|---|---|---|
| C9 | 8,2 pF 50 V NP0 | OK | unverändert | ❔ | VOX-Empfindlichkeit nicht untersucht |
| C11 | 4,7 µF 16 V | OK | unverändert | ❔ | |
| C12 | 47 µF 16 V | OK | unverändert | ❔ | |
| C13 + C29 | 100 nF 50 V | Kerko 104Z | unverändert | ❔ | |
| C14 | 10 nF 50 V | Kerko 103Z | unverändert | ❔ | |
| C30 | 100 µF 25 V | OK | unverändert | ❔ | |
| C31 | 470 nF 100 V | OK | unverändert | ❔ | |
| R8 | 4,7 kΩ | OK | unverändert | ❔ | |
| R12, R20 | 1,0 kΩ | OK | unverändert | ❔ | LED-Vorwiderstände |
| R17 | 12 kΩ | OK | unverändert | ❔ | |
| R18 | 10 kΩ | OK | unverändert | ❔ | |
| R19 | 2,2 kΩ | OK | unverändert | ❔ | |
| R10 | nicht vorhanden | – | – | – | |
| D6, D7 | 1N4148 | OK | unverändert | ❔ | |
| D11 | 1N5400 | OK | unverändert | ❔ | |
| D12, D13 | 1N4007 | OK | unverändert | ❔ | |
| **D14** | 1N4007 | OK (ohne Kühlung) | unverändert | ❔ | **Im Schaltplan Teil der Relaisversorgung**, keine Bias-Diode für Tr5. Die README-Empfehlung „thermisch an Tr5 koppeln" ist durch den Schaltplan nicht gestützt. **Am Gerät prüfen.** |
| TR1, TR4 | BC547 | OK | unverändert | ❔ | |
| D1 | LED bicolor | – | unverändert | ❔ | |
| RL1, RL2 | Relais 12 V 3022.7.012 | – | unverändert | ❔ | Zeitverhalten nicht untersucht |
| Fuse | 12 A | – | unverändert | ❔ | |

---

## 3. Einkaufs- und Abgleichliste (nur Änderungen)

| Menge | Teil | Wert / Typ | Für |
|---|---|---|---|
| 1 | Silberglimmer 500 V, ± 2 % | **470 pF** | C18 |
| 1 | Silberglimmer 500 V, ± 2 % | **220 pF** | C19 |
| 1 | Silberglimmer 500 V, ± 2 % | **270 pF** | C20 |
| 1 | Silberglimmer 500 V, ± 2 % | **120 pF** | C21 |
| 1 | Silberglimmer ≥ 100 V, ± 2 % | 220 pF | C16 |
| 1 | Silberglimmer ≥ 100 V, ± 2 % | 270 pF | C17 |
| 1 | C0G oder Glimmer, ± 2 %, 50 V | 100 pF | C15 |
| 1 | C0G oder X7R, 50 V | **2,2 nF** | C26 |
| 1 | Widerstand 15 Ω / 2 W, induktionsarm | **15 Ω** | R9 |
| 1 | Widerstand 330 Ω, 0,25 W, 1 % | **330 Ω** | R14 |
| – | Spulenabgleich (Windungsabstand) | **L2 ≈ 70 nH, L5 ≈ 60 nH** | LCR-Meter nötig |

Die Silberglimmer müssen für **≥ 2 A HF-Strom bei 27 MHz** ausgelegt sein (C19–C21). Alternativ mehrere kleinere Kondensatoren parallel.

---

## 4. Umbaureihenfolge (empfohlen)

1. **Messen, nichts ändern:** L2 und L5 (Induktivität), Leistung bei 1 / 2 / 5 W an 50-Ω-Last, Eingangs-VSWR, Ruhestrom, Temperatur von C19–C21.
2. **R9 = 15 Ω** einsetzen → VSWR und Leistung erneut messen (erwartet: bessere Anpassung, gleiche Leistung).
3. **Kondensatoren C16–C21 gegen Glimmer tauschen** (Werte unverändert) → Temperatur im Ausgangsnetzwerk vergleichen.
4. **C18 auf 470 pF** erhöhen → Oberwellen, Kollektortemperatur und Leistung prüfen. Notfalls schrittweise (180 → 270 → 390 → 470 pF).
5. **L2 und L5** auf die Zielwerte abgleichen (70 / 60 nH). Jeweils mit Leistungsmesser und Last, nie mit Antenne.
6. **RX:** R14 → 330 Ω und C26 → 2,2 nF. Verstärkung und Rauschen messen, mit **offener** und **kurzgeschlossener** Antennenbuchse auf Schwingen prüfen.

Nach jedem Schritt auf **Schwingen** achten (Spektrum bei 20–30 MHz). Bei Auffälligkeiten den letzten Schritt rückgängig machen.

---

## 5. Zuordnung zu den Simulationsdateien

| Zustand | uSimmics-Plan (RX) | uSimmics-Plan (TX) |
|---|---|---|
| **Vorher** (IST: R9 Brücke, L2 85 nH, L5 80 nH, C18 120 pF) | [`kl200_rx.sch`](./simulation/kl200_rx.sch) | [`kl200_tx.sch`](./simulation/kl200_tx.sch) |
| **Nachher** (Tabellen oben) | [`kl200_rx_opt.sch`](./simulation/kl200_rx_opt.sch) | [`kl200_tx_opt.sch`](./simulation/kl200_tx_opt.sch) |

Die Werte der „Nachher"-Pläne stehen in `OPTIMIERT` in [`simulation/kl200_circuit.py`](./simulation/kl200_circuit.py). Die Kondensatoren C15–C21 sind dort mit Nennwerten abgebildet (die Glimmer-Eigenschaften erscheinen nur in der Verlustrechnung im Bericht).
