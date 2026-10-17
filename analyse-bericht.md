# Analysebericht: RM Italy KL 200/P (Rel. 5.04), Simulation und Optimierung

Stand: 16.10.2026 · Simulation mit `qucsator_rf` 1.0.7, Gegenprobe mit uSimmics 5.9 (Wine)
Zugehörig: [bauteilliste-optimiert.md](./bauteilliste-optimiert.md) (Vorher/Nachher-Gegenüberstellung)

> **Wichtigster Vorbehalt:** Die Zahlen stammen aus einem **Modell mit geschätzten Werten** (Spulen L2–L5, Transistor, Relaisspulen).
> Aussagen über *absolute* Leistung sind nicht belastbar. Belastbar sind die **Tendenzen, Empfindlichkeiten und Vergleiche** zwischen „Vorher" und „Nachher", weil beide mit demselben Modell gerechnet wurden.
> Die Empfehlungen sind Vorschläge zur Überprüfung am Gerät, kein Freigabenachweis. Siehe [Grenzen](#7-grenzen-und-unsicherheiten).

---

## 1. Zusammenfassung

| # | Befund | Konfidenz |
|---|---|---|
| 1 | **Tr5 arbeitet im C-Betrieb.** Die Basis hat keine Vorspannung (nur L2/R11/L3 nach Masse). D14 sitzt in der Relais-Versorgung und ist **keine** Bias-Diode für Tr5. Das widerspricht dem README-Abschnitt „KI-Schaltungsanalyse" Punkt 1. | hoch (Schaltplan), am Gerät prüfen |
| 2 | **Der Eingangskreis (C15–C17, L2) ist hoch selektiv.** L2 +30 % (85 → 110 nH) senkt die Ausgangsleistung um 64 %. Die Endstufe reagiert dadurch stark auf Spulen- und Kondensatortoleranzen. | mittel-hoch |
| 3 | **Mit der geschätzten Abstimmung (L2 ≈ 85 nH, L5 ≈ 80 nH, R9 = Brücke) ist der Verstärker im Modell schlecht angepasst:** Eingangs-VSWR 9–30, Kollektorspitzen 63–85 V, Kompression ab ≈ 2 W Ansteuerung, Leistungsabfall zu 29,7 MHz. | mittel (abhängig von der Spulenannahme) |
| 4 | **Eine Abstimmung mit R9 = 15 Ω, L2 ≈ 70 nH, L5 ≈ 60 nH, C18 = 470 pF** verbessert im Modell alle untersuchten Größen deutlich und **ist gegen Toleranzen robust** (Abschnitt 5). | mittel |
| 5 | **Der RX-Vorverstärker (BF199) ist nur bedingt stabil:** |S22| > 0 dB am Antennenanschluss (+1,1 dB bei 27 MHz). Mit R14 = 330 Ω und C26 = 2,2 nF ist |S22| < 0 dB im ganzen Band 1–100 MHz, bei gleicher Verstärkung und 1 dB besserer Rauschzahl. | hoch (zwei Simulatoren übereinstimmend) |
| 6 | **Ausgangsnetzwerk C19–C21 führt bis ≈ 2,2 A effektiv.** Keramik verliert dort ≈ 4× mehr als Silberglimmer. Die README-Empfehlung Glimmer wird bestätigt. | mittel (Verlustfaktor angenommen) |
| 7 | Das Modell der Endstufe **schwingt** bei Großsignal um ≈ 25 MHz, wenn der Emitter ideal an Masse liegt. Ein realistischer Emitter-/Bonddraht-Anteil (Le5 ≥ 3 nH) beseitigt das. Ob das reale Gerät in dieser Hinsicht Reserve hat, ist offen. | niedrig-mittel |

---

## 2. Vorgehen

1. Schaltplan [`images/schaltung_v5.04.png`](./images/schaltung_v5.04.png) wurde abgelesen, Werte aus [`bauteilliste.md`](./bauteilliste.md) und README übernommen.
2. Die Schaltung steht einmalig in [`simulation/kl200_circuit.py`](./simulation/kl200_circuit.py). Daraus entstehen
   - die Netzliste für `qucsator_rf` ([`netlist.py`](./simulation/netlist.py)) und
   - die uSimmics-Schaltpläne ([`schematic.py`](./simulation/schematic.py), [`build.py`](./simulation/build.py)).
3. **Relaiskontakte** sind als Netzbrücken modelliert, daher je ein Plan für **RX** (RL1 an, RL2 ab) und **TX** (RL1 ab, RL2 an).
4. **Gegenprobe:** `kl200_rx.sch`, `kl200_tx.sch`, `kl200_rx_opt.sch` und `kl200_tx_opt.sch` wurden in uSimmics 5.9 geöffnet und simuliert. Die RX-Kurven stimmen mit `qucsator_rf` überein, die TX-Läufe zeigen dasselbe Verhalten (Schwingung im alten Modell, sauberer Träger im optimierten).
5. **Analysen**
   - DC-Arbeitspunkt, S-Parameter (RX, K/μ, Rauschzahl).
   - **Transientenanalyse** für TX (Gear, 27,185 MHz, 30–40 µs, Auswertung der letzten 8 µs). Harmonic Balance stürzt in `qucsator_rf` ab und wurde nicht verwendet.
   - Toleranzstreuung (Monte-Carlo), Temperaturdrift, Frequenzgang.

---

## 3. Modell und Annahmen

| Größe | Wert | Herkunft |
|---|---|---|
| Versorgung | 13,8 V | Annahme |
| L1 | 10 µH | Bauteilliste |
| **L2 (ANRA 289)** | **85 nH** (Vorher) | **Schätzung** (Wheeler, 3 Wdg. Ø 8 mm aus dem älteren Handbuch) |
| **L5 (ANRA 289/3)** | **80 nH** (Vorher) | **Schätzung** (3 Wdg. Ø 8 mm, Draht 1,2 mm) |
| L4 (ANRA 455) | 0,35 µH | Schätzung (12 Wdg. Ø 6 mm) |
| L3 (VK200) | 3 µH | Schätzung |
| Relaisspulen | 360 Ω | Schätzung |
| **Tr5** | Gummel-Poon-Näherung eines 60–90-W-HF-Transistors, Cob ≈ 250 pF | Schätzung, an SD1446-Datenblattgrößen orientiert |
| **Le5** (Emitter-Zuleitung Tr5) | 3 nH | Annahme, nötig für Stabilität |
| R9 | 1 mΩ (Drahtbrücke, **IST laut README**) | README |
| Dioden, BC547, BF199 | typische Modellparameter | Schätzung |
| Kondensatorverluste | tanδ 2·10⁻³ (Keramik), 5·10⁻⁴ (Glimmer) | Annahme, nur in der Verlustrechnung |

Die Transistoren des Gerätes (MRF455 oder SD1446) sind nicht modelliert, sondern durch Ersatzparameter angenähert. Die Abweichung zum realen Bauteil kann groß sein.

---

## 4. Ergebnisse Empfangszweig (RX)

### 4.1 Arbeitspunkt (Vorstufe)

Ic ≈ 10 mA, Vce ≈ 11,7 V, Vbe ≈ 0,75 V. Der DC-Arbeitspunkt beider Relaisstellungen konvergiert, Tr4 sperrt ohne HF, Tr1 zieht RL1 an.

### 4.2 Verstärkung und Stabilität (Vorher)

| Größe | Wert |
|---|---|
| Verstärkung S12 (ANT→RTX) | 15,7 dB bei 27 MHz, 15,4–16,3 dB über 26–30 MHz |
| Rückwärtsisolation S21 | ≈ −49 dB bei 25 MHz |
| **S22 (Antennenanschluss)** | **+1,1 dB bei 27 MHz, Maximum +1,9 dB bei 47 MHz** |
| Stabilitätsfaktor K / μ | negativ (K<0, μ<0) wegen |S22| > 1 |
| Rauschzahl bei 27 MHz | 4,6 dB |

**Deutung:** Der Eingang wirkt für einen echten 50-Ω-Abschluss stabil (|Γs| = 0). Bei fast totaler Reflexion am Antennenanschluss (offene oder kurzgeschlossene Leitung, VSWR > 16) ist die Schleifenverstärkung > 1. Dann ist eine Schwingung möglich. Das kann bei fehlender Antenne auftreten.

### 4.3 Variationen und Optimum

Ergebnis der Einzelvariationen (`experiments/exp7.py`, `exp7b.py`, `exp16.py`):

| Änderung | G(27 MHz) | S22 (27 MHz) | S22max |
|---|---|---|---|
| Vorher (R14 100 Ω, C26 470 pF) | 15,7 dB | +1,1 dB | +1,9 dB |
| nur C26 = 100 pF | 4,5 dB | 0,0 dB | +3,7 dB |
| nur C26 = 1 nF | 18,7 dB | +0,9 dB | +0,9 dB |
| nur R14 = 220 Ω | 14,9 dB | +0,9 dB | +1,3 dB |
| nur R15 = 22 kΩ | 13,7 dB | +0,6 dB | +0,9 dB |
| C26 = 1 nF, R14 = 330 Ω | 15,8 dB | +0,3 dB | +0,3 dB |
| **C26 = 2,2 nF, R14 = 330 Ω** | **16,1 dB** | **−0,2 dB** | **0,0 dB** (bei 4 MHz) |

- **Nachher:** Gain 16,1 dB, **flach (± 0,0 dB über 26–30 MHz)**, |S22| < 0 dB über das ganze Band.
- Toleranz: C26 1,8–2,7 nF und R14 270–390 Ω ändern das Ergebnis kaum (Gain 15,4–16,9 dB, |S22| bleibt ≤ +0,01 dB).
- **Rauschzahl bei 27 MHz:** 4,6 → **3,5 dB** (qucsator-Rauschanalyse).
- **Arbeitspunkt:** Ic 10 → 4 mA, Vce 11,7 → 12,1 V. Der Stromverbrauch sinkt etwas.
- **uSimmics-Gegenprobe** (`kl200_rx_opt.sch`): S12 ≈ 16 dB flach, |S22| < 0 dB bis auf einen kleinen Ausschlag (≈ +0,05 dB) bei ≈ 4 MHz.

**Nicht untersucht:** Großsignalverhalten (Übersteuerung, Intermodulation) mit 4 mA statt 10 mA Ruhestrom.

---

## 5. Ergebnisse Sendezweig (TX)

### 5.1 Stabilität des Modells

| Modell | Verhalten bei 2 W Ansteuerung (33 dBm) |
|---|---|
| Emitter ideal an Masse | **Schwingung bei ≈ 25 MHz**, Träger moduliert (Hüllkurve 35–70 V) |
| Le5 = 1–2 nH | teilweise Schwingung |
| **Le5 ≥ 3 nH** (Rb 0,1 Ω) bzw. ≥ 2 nH (Rb 0,5 Ω) | **sauber** (Nebenlinien < −40 dBc) |

- Ohne Ansteuerung schwingt das Modell nie. Die Schwingung ist ein Großsignaleffekt und wandert **nicht** mit der Treiberfrequenz.
- Eine Resonanz aus L2 und C16∥C17 liegt bei ≈ 24,7 MHz, in der Nähe der beobachteten Schwingung.
- Die Parameter wurden danach so gewählt (Le5 = 3 nH), dass das Modell stabil ist. **Ob die reale Endstufe solche Reserve hat, ist damit nicht belegt.**

### 5.2 Vorher gegen Nachher (27,185 MHz, 50-Ω-Quelle und -Last)

**Vorher** = IST: R9 Drahtbrücke, L2 85 nH, L5 80 nH, C18 120 pF.
**Nachher** = R9 15 Ω, L2 70 nH, L5 60 nH, C18 470 pF.

| Treiber | | Pout | Gain | Wirkungsgrad | Kollektor-Spitze | Eingangs-VSWR | H2 | H3 |
|---|---|---|---|---|---|---|---|---|
| 1 W (30 dBm) | Vorher | 12,4 W | 10,9 dB | 30 % | 46 V | 4,7 | −24 dBc | −40 dBc |
| | **Nachher** | 8,8 W | 9,4 dB | 28 % | 27 V | 2,6 | −26 dBc | −45 dBc |
| 2 W (33 dBm) | Vorher | 17,6 W | 9,5 dB | 44 % | 63 V | 9,4 | −21 dBc | −36 dBc |
| | **Nachher** | 18,8 W | 9,7 dB | 40 % | 31 V | 2,8 | −29 dBc | −45 dBc |
| 5 W (37 dBm) | Vorher | 19,2 W | **5,8 dB** | 57 % | 75 V | 21,6 | −21 dBc | −33 dBc |
| | **Nachher** | **45,7 W** | **9,6 dB** | 60 % | 39 V | 3,1 | −31 dBc | −48 dBc |
| 10 W (40 dBm) | Vorher | 20,0 W | 3,0 dB | 69 % | 82 V | 29,5 | −21 dBc | −32 dBc |
| | **Nachher** | 69,3 W | 8,4 dB | 78 % | 51 V | 2,6 | −27 dBc | −44 dBc |

Lesehilfe: Der „Vorher"-Verstärker läuft ab ≈ 2 W in die Kompression (Gain fällt von 10,9 auf 3 dB). Der „Nachher"-Verstärker behält ≈ 8–10 dB über den ganzen Bereich.

### 5.3 Frequenzgang (2 W Ansteuerung)

| f / MHz | Vorher Pout | Vorher VSWR | Nachher Pout | Nachher VSWR |
|---|---|---|---|---|
| 26,0 | 27,1 W | 4,0 | 18,6 W | 2,6 |
| 26,965 (CB Kanal 1) | – | – | 18,8 W | 2,8 |
| 27,185 | 17,6 W | 9,4 | 18,8 W | 2,8 |
| 27,405 (CB Kanal 40) | – | – | 18,6 W | 2,9 |
| 28,0 | 13,3 W | 15,7 | 18,2 W | 3,1 |
| 29,0 | – | – | 17,0 W | 3,6 |
| 29,7 | 7,6 W | 41,6 | 16,1 W | 4,1 |

„Nachher" ist über 26–29,7 MHz auf ± 0,6 dB flach. „Vorher" fällt über das Band um ≈ 5,5 dB.

### 5.4 Robustheit gegen Toleranzen (Monte-Carlo, 10 Läufe, 5 W)

Streuung: L2 und L5 ± 10 % (von Hand gewickelt), Kondensatoren C15–C21, C23: ± 5 % (Vorher, Keramik J) bzw. ± 2 % (Nachher, Glimmer).

| Größe | Vorher (min / Mittel / max) | Nachher (min / Mittel / max) |
|---|---|---|
| Pout | 16,3 / 21,6 / 25,0 W | **33,3 / 44,2 / 48,1 W** |
| Eingangs-VSWR | 8,0 / 16,0 / 29,2 | **2,6 / 3,1 / 4,4** |
| Kollektor-Spitze | 58 / 76 / 85 V | **31 / 38 / 44 V** |
| Wirkungsgrad | 44 / 62 / 75 % | 48 / 59 / 66 % |
| H2 | −20,4 / −21,0 / −22,9 dBc | −28,2 / −30,6 / −31,7 dBc |
| H3 | −32,0 / −33,5 / −38,3 dBc | −43,5 / −46,9 / −48,6 dBc |

Bei 2 W (33 dBm, C18 = 120 pF) lag die Streuung ähnlich: Pout 12,5–27,7 W (Vorher) gegen 14,6–17,1 W (Nachher-Zwischenstand).

### 5.5 Empfindlichkeit einzelner Teile

| Teil | Variation | Wirkung (2 W, Modell) |
|---|---|---|
| **L2** | 40 / 60 / 85 / 110 / 140 nH | 6,3 / 19,2 / 17,6 / 6,4 / 1,3 W: **scharfe Resonanz** |
| **L5** | 40 / 60 / 80 / 100 / 120 nH (2 W, Vorher-Zustand) | 8,1 / 13,1 / 17,6 / 7,2 / 3,7 W; bei 5 W kippt der Betrieb ab ≈ 70 nH in hohe Kollektorspannung (56–87 V) |
| **C18** | 120 → 180 / 270 / 390 / 470 / 680 pF (mit L2 70 nH, L5 60 nH, R9 15 Ω) | H2 −23 → −24 / −25 / −27 / −29 / −32 dBc; H3 −34 → −36 / −39 / −43 / −45 / −49 dBc; Kollektor-Spitze 38 → 37 / 35 / 32 / 31 / 29 V; Wirkungsgrad 31 → 33 / 36 / 38 / 40 / 42 % |
| **R9** | Brücke gegen 15 Ω | Pout ±1 %, aber VSWR 9,4 → 7,5 (2 W) und 21,6 → 13,9 (5 W); R9 verbraucht 0,4–0,8 W |
| **L3** | 1 / 3 / 10 µH | < 1 % |
| **L4** | 0,2 / 0,35 / 0,6 / 1,5 µH | < 3 % |
| **N750-Drift** | +40 K (−3 % bei C16, C17, C19, C20) | ≈ +0,2 bis +0,5 dB (gering) |

### 5.6 Kondensatorbelastung (Nachher, 5 W, Pout 45,7 W)

Verlust = ½·V²·ωC·tanδ (nur Grundwelle).

| Teil | Wert | Spannung (Spitze) | Strom eff. | Verlust Keramik | Verlust Glimmer |
|---|---|---|---|---|---|
| C15 | 100 pF | 19,4 V | 0,23 A | 6 mW | 2 mW |
| C16 | 220 pF | 16,8 V | 0,45 A | 11 mW | 3 mW |
| C17 | 270 pF | 16,8 V | 0,55 A | 13 mW | 3 mW |
| C18 | 470 pF | 15,1 V | 0,86 A | 18 mW | 5 mW |
| C19 | 220 pF | 68,1 V | 1,81 A | 174 mW | 44 mW |
| C20 | 270 pF | 68,1 V | 2,22 A | 214 mW | 53 mW |
| C21 | 120 pF | 68,1 V | 0,99 A | 95 mW | 24 mW |
| C23 | 1 nF | 7,9 V | 0,96 A | 11 mW | 3 mW |
| **Summe** | | | | **542 mW** | **136 mW** |

- Im „Vorher"-Zustand bei 5 W: 275 mW (Keramik) gegen 69 mW (Glimmer), bezogen auf die Ausgangsleistung ebenfalls ≈ 4:1.
- Spannungen: alle weit unter 50 V bzw. 500 V. Der Strom in C19–C21 (bis 2,2 A eff.) ist das eigentliche Problem, nicht die Spannung.
- C16/C17 (50 V): ≈ 17–25 V Spitze. Das reicht bei 5 W, enger wird es bei 10 W (ca. 34 V). Fundamental-Rechnung, Oberwellen kommen hinzu.

---

## 6. Empfehlungen (Kurzfassung)

Die vollständige Gegenüberstellung steht in [bauteilliste-optimiert.md](./bauteilliste-optimiert.md).

1. **R9 = 15 Ω / 2 W einsetzen** (statt Drahtbrücke). Wirkung: bessere Eingangsanpassung, kein Leistungsverlust. Vorsicht: Das ist die Spar-Maßnahme der MRF455-Version und könnte absichtlich sein.
2. **L2 auf ≈ 70 nH und L5 auf ≈ 60 nH einstellen.** Die Ist-Werte sind unbekannt, deshalb zuerst messen (LCR-Meter / Dip-Meter) und dann auf diese **absoluten Zielwerte** abgleichen (Windungsabstand).
3. **C18: 120 → 470 pF** (Glimmer, 500 V). Senkt Oberwellen und Kollektor-Spitze.
4. **C16, C17, C19, C20, C21: Silberglimmer, ± 2 %.** Weniger Verlust und Toleranz im selektiven Eingangskreis.
5. **RX: R14 100 → 330 Ω und C26 470 pF → 2,2 nF.** |S22| < 0 dB, Gain flach, Rauschzahl ≈ 1 dB besser.
6. **Nicht ändern:** L1, L3, L4, C9, C11–C14, C23, C25, C27–C31, alle Widerstände außer R9/R14, Dioden, BC547, BF199, Relais, Sicherung (nicht oder kaum untersucht, bzw. unempfindlich).

### Vorgeschlagene Verifikation am Gerät

1. **Vor der Änderung messen:** L2, L5 (LCR-Meter bei 1–30 MHz), Ruhestrom, Leistung bei 1 W / 2 W / 5 W, Eingangs-VSWR.
2. **Eine Änderung nach der anderen:** erst R9, dann L2/L5, dann C18. Jeweils Leistung, VSWR und Kollektor-Temperatur messen.
3. **Mit Lastwiderstand und Oszilloskop** arbeiten (50-Ω-Last, ausreichend Kühlung), nicht mit Antenne.
4. **RX-Vorstufe:** Verstärkung, Rauschen und Stabilität mit offener sowie kurzgeschlossener Antennenbuchse prüfen.

---

## 7. Grenzen und Unsicherheiten

- **Transistor:** Ersatzmodell. Cob, Ikf, hFE und Sättigung des realen MRF455/SD1446 weichen ab. C18 und die Kollektorabstimmung hängen direkt davon ab. Vor allem die Verbesserung durch größeres C18 ist modellabhängig.
- **Spulen:** L2–L5 sind aus Wickeldaten geschätzt. Die Zuordnung alter zu neuen Spulennummern ist eine Vermutung. Die **absoluten Zielwerte** (70/60 nH) gelten nur im Modell.
- **Kollektor-Spitzen:** Das Modell liefert für „Vorher" 63–85 V, mehr als die Vcbo des SD1446 (36 V). Entweder ist das Modell zu „weich", oder die Spulenannahmen stimmen nicht. In beiden Fällen ist die Aussage „Vorher ist riskant" **nicht** gesichert.
- **Leistungswerte** (19–46 W) liegen unter den Herstellerangaben des KL 200/P. Das Modell schöpft den Transistor nicht aus.
- **Oberwellen:** −27 bis −31 dBc (H2) erfüllen keine praktische Anforderung an ein Endgerät (üblich −50 dBc oder besser). Dafür wäre ein zusätzlicher Tiefpass nötig.
- **Harmonic Balance** war nicht verfügbar. Transientenläufe über 30–40 µs sind eingeschwungen, aber kurz.
- **Nicht untersucht:** VOX-Schwelle (C9, R8, R19, Tr4), Relaiszeiten, Netzteil und Elkos, Wärmehaushalt, Intermodulation, Rauschen der Vorstufe bei Großsignal, mechanische Kopplung der Spulen.
- **D14:** Der README bezeichnet D14 als thermisch gekoppelte Bias-Diode. Im Schaltplan ist sie in der Relaisspannung (Anode an Vcc, Kathode an RL2/D13). Das sollte am Gerät geprüft werden, bevor jemand D14 thermisch an den Transistor koppelt.

---

## 8. Reproduzierbarkeit

Voraussetzung: `analyse/inst/bin/qucsator_rf` (aus [`ra3xdh/qucsator_rf`](https://github.com/ra3xdh/qucsator_rf) gebaut) und Python 3 mit `numpy`.

```bash
cd simulation
python3 build.py                              # erzeugt kl200_{rx,tx}.sch und kl200_{rx,tx}_opt.sch
PYTHONPATH=. python3 experiments/exp13.py     # Monte-Carlo und Treibersweep (Nachher gegen Vorher, 37 dBm)
PYTHONPATH=. python3 experiments/exp7b.py     # RX-Vorverstärker, Kombinationen
```

| Datei | Inhalt |
|---|---|
| [`simulation/kl200_circuit.py`](./simulation/kl200_circuit.py) | Schaltung, Annahmen (`PARAM`), optimierte Werte (`OPTIMIERT`) |
| [`simulation/runner.py`](./simulation/runner.py) | Simulationsläufe und Auswertung |
| [`simulation/kl200_rx.sch`](./simulation/kl200_rx.sch), [`kl200_tx.sch`](./simulation/kl200_tx.sch) | uSimmics-Pläne **Vorher** |
| [`simulation/kl200_rx_opt.sch`](./simulation/kl200_rx_opt.sch), [`kl200_tx_opt.sch`](./simulation/kl200_tx_opt.sch) | uSimmics-Pläne **Nachher** |
| [`simulation/experiments/`](./simulation/experiments) | alle Einzelexperimente (`exp1` … `exp16`), Ergebnisse in `results/` |

`exp1` und `exp2` variieren `Le5` (Abschnitt 5.1). Ab `exp3` gilt `Le5 = 3 nH`. Die RX-Experimente (`exp7`–`exp7d`, `exp16`) sind davon unabhängig.
