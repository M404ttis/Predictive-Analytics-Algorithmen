# Tag 12: Modelloptimierung – Lösung Arbeitsauftrag 1 und 2 (Bohnenwerk)

Alle Zahlen stammen aus `12_Demo_CV_und_Grid.py` (Start: `.venv/bin/python 12_Modelloptimierung/12_Demo_CV_und_Grid.py`).
Daten: 156 Wochen Onlineumsatz der Rösterei, Ziel `Umsatz_EUR`, 7 Merkmale (`Woche`, drei Budgets, `Rabattaktion`, `Weihnachtsgeschaeft`, `Temperatur_C`). Modell in Arbeitsauftrag 1: lineare Regression.

## Ergebnis in Kürze

<div style="background:#e6f4f1;border-left:4px solid #1a8a7a;padding:10px 14px;margin:10px 0">

**Arbeitsauftrag 1:** k = 3, jeder Fold ein Kalenderjahr. MSE je Fold 1,19 Mio / 2,17 Mio / 0,92 Mio, Mittel **1,43 Mio** (RMSE ≈ **1.196 €**, bei einem Durchschnittsumsatz von 17.668 € rund 6,8 %). Das Jahr 2024 ist am schlechtesten, vor allem wegen der **Kaffeemesse in KW 38** (Umsatz 25.618 €, Modellfehler 8.516 €).

**Arbeitsauftrag 2:** Gewählt wird **Random Forest** mit 3 × 4 × 3 = **36 Kombinationen**. Mit 3 Folds sind das **108 Läufe = 36 Minuten** (+ 20 Sekunden fürs Endtraining), also im Budget von 60 Minuten. Überraschung: Das beste Baummodell (MSE 3,33 Mio) ist **mehr als doppelt so schlecht** wie die lineare Regression (1,43 Mio). Die Antwort an die Marketingleitung lautet: **Nein, ein baumbasiertes Verfahren sagt den Umsatz hier nicht besser voraus.** Tuning ändert daran nichts.

</div>

---

## Arbeitsauftrag 1: Kreuzvalidierung

### 1.1 Wahl von k

**Gewählt: k = 3, ein Fold je Jahr (2023, 2024, 2025).**

| Durchlauf | Trainiert mit den Wochen | Getestet mit den Wochen | MSE | RMSE |
|---|---|---|---:|---:|
| 1 | 53 bis 156 (2024 und 2025) | 1 bis 52 (2023) | 1.192.934 | 1.092 € |
| 2 | 1 bis 52 und 105 bis 156 (2023 und 2025) | 53 bis 104 (2024) | 2.174.355 | 1.475 € |
| 3 | 1 bis 104 (2023 und 2024) | 105 bis 156 (2025) | 921.688 | 960 € |
| **Mittel** | | | **1.429.659** | **1.196 €** |

(Die Spalte RMSE je Fold ist die Wurzel des jeweiligen MSE. Der RMSE des Mittelwerts, 1.196 €, ist die Wurzel aus dem **mittleren** MSE und nicht der Mittelwert der drei RMSE.)

**Warum 3 und nicht 2, 5, 10 oder 12?**

- **Jahreszeiten:** Die Daten haben eine Jahressaison (Weihnachten KW 47 bis 51, Rabattaktionen). Ein Fold mit genau einem Jahr enthält jede Jahreszeit einmal. Würde ein Fold nur Januar bis Juni enthalten, wäre er nicht mit einem Fold „Juli bis Dezember" vergleichbar.
- **Genug Training:** Bei k = 3 trainiert jeder Durchlauf mit 104 Wochen (zwei Dritteln). Das reicht für 7 Merkmale locker.
- **Genug Test:** 52 Wochen je Fold sind stabil genug für einen MSE. Bei k = 12 hat ein Fold nur 13 Wochen und ein einzelner Ausreißer dominiert (siehe unten).
- **Erklärbar:** „Wir testen jedes Jahr einmal gegen die beiden anderen" versteht auch die Geschäftsführung.
- **Rechenzeit:** k Folds kosten k Trainings. Das spielt bei Arbeitsauftrag 2 eine Rolle.

Vergleich, was ein anderes k ergibt:

| Einteilung | MSE je Fold | Mittel | RMSE |
|---|---|---:|---:|
| k = 2 (Wochen 1–78, 79–156) | 1,05 Mio / 1,82 Mio | 1,44 Mio | 1.198 € |
| **k = 3 (Jahre)** | 1,19 Mio / 2,17 Mio / 0,92 Mio | **1,43 Mio** | **1.196 €** |
| k = 4 (je 39 Wochen) | 0,96 / 1,00 / 2,64 / 1,06 Mio | 1,41 Mio | 1.189 € |
| k = 12 (je 13 Wochen) | 0,44 Mio bis **6,43 Mio** | 1,41 Mio | 1.187 € |
| k = 3, zufällig gemischt | 1,03 / 1,20 / 2,05 Mio | 1,43 Mio | 1.195 € |

Der **Mittelwert** ist fast unabhängig von k (1,41 bis 1,44 Mio). Das ist die gute Nachricht: Die Größenordnung des Fehlers ist verlässlich. Was sich ändert, ist die **Streuung** der Folds.

### 1.2 Zuordnung der 156 Wochen

Jede Woche steht in genau einem Fold, die Folds überlappen nicht:

```python
FOLDS = {
    1: "1-52",      # 2023
    2: "53-104",    # 2024
    3: "105-156",   # 2025
}
```

### 1.3 Warum unterscheiden sich die Folds?

Der Fold 2024 (MSE 2,17 Mio) ist fast doppelt so schlecht wie 2023 (1,19 Mio) und mehr als doppelt so schlecht wie 2025 (0,92 Mio). Dafür gibt es einen klar erkennbaren Grund:

**Die Kaffeemesse (KW 38 / Woche 90) im September 2024.** Das Modell kennt kein Merkmal „Messe". Die Woche hatte 25.618 € Umsatz, die größte der 156 Wochen, das Modell erwartete rund 17.100 €. Fehler 8.516 €, quadriert 72,5 Mio.

Das lässt sich nachrechnen (k = 12, die Messewoche liegt im Fold mit den Wochen 79–91): Dieser Fold hat 6,43 Mio MSE, und der Messefehler allein trägt 72,5 Mio / 13 = 5,6 Mio davon bei, **rund 87 %**. Ohne die Messewoche läge dieser Fold bei etwa 0,9 Mio, wie alle anderen auch.

Andere große Fehler: KW 17/2023 (Woche 17, Fehler +3.899 €) und KW 35/2024 (Woche 87, Fehler −2.931 €). Für diese beiden gibt die Aufgabe keine Erklärung, sie sind nach den Angaben „Zufall" oder ein nicht erfasster Einfluss.

**Warum fällt das beim MSE so stark auf?** Der MSE quadriert die Fehler. Ein Fehler von 8.500 € zählt 64-mal so viel wie ein Fehler von 1.000 €. Eine einzige Woche kann einen ganzen Fold dominieren. Das ist auch der Grund, warum bei k = 12 die Spanne so groß ist (0,44 bis 6,43 Mio).

Weitere Hinweise aus der Aufgabe, die Folds unterscheiden könnten:

| Ereignis | Betrifft | Wirkung auf die Folds |
|---|---|---|
| Kaffeemesse KW 38/2024 | nur 2024 | Fold 2024 schlechter (belegt, s. o.) |
| Werkstudentin Social Media seit Januar 2024 | ab 2024 | Der Zusammenhang Social-Budget ↔ Umsatz kann sich geändert haben. Nicht belegt, nur Vermutung. |
| Bio-Siegel ab 2024, neues Logo ab März 2025 | 2024 / 2025 | Mehr oder weniger Grundumsatz, im Modell nur über den Trend (`Woche`) abgebildet |
| Umzug Mai 2023 | 2023 | Laut Aufgabe lief der Shop durchgehend: vermutlich kein Einfluss |

### 1.4 Warum zeigt CV mehr als ein Split?

- **Ein Split liefert eine Zahl, die vom Zufall der Aufteilung abhängt.** Hätten wir 2024 als Test gewählt, hätten wir 2,17 Mio gesehen („das Modell ist schlecht"), bei 2025 wären es 0,92 Mio gewesen („sehr gut"). Beides ist richtig und keines die ganze Wahrheit.
- **CV liefert Mittel und Streuung.** Mittel 1,43 Mio sagt, wie gut das Modell **typischerweise** ist. Die Spanne 0,92 bis 2,17 Mio sagt, wie **verlässlich** das ist und dass es **Ausreißerwochen** gibt.
- **Jede Woche wird genau einmal getestet** und geht k − 1-mal ins Training ein. Keine Daten werden verschenkt, wie bei einem festen 20-%-Test.
- **Die Streuung ist ein Befund an sich:** Sie zeigt, dass die Planung für ein Messejahr mit einem Fehler von rund 1.500 € je Woche rechnen sollte, in einem ruhigen Jahr mit etwa 1.000 €.

### 1.5 Training mit 2025, Test mit 2023: sinnvoll?

**Für diese Daten: nein, wenn man ein Modell für die Zukunft bewerten will.** Das Modell soll das **Budget 2026** planen, also in die Zukunft vorhersagen. Wer mit 2025 trainiert und 2023 testet, lässt das Modell die **Vergangenheit „vorhersagen"** und nutzt Wissen aus der Zukunft. In der Praxis hat man nie Daten aus der Zukunft.

Das ist zwar kein klassisches Leck über die Zielspalte, aber es ist eine **falsche Prüfsituation**: Der Test beantwortet „Wie gut kann das Modell 2023 aus 2024/2025 rekonstruieren?", nicht „Wie gut sagt es 2026 vorher?".

Zur Einordnung: Das mitgelieferte Skript hat dafür `NUR_VERGANGENHEIT = True`. Dann trainiert jeder Durchlauf nur mit Wochen **vor** seinem Testfold. Ergebnis bei k = 3: Fold 2023 hat **kein Training** und entfällt, Fold 2024 (Training 2023) hat MSE 2,32 Mio, Fold 2025 (Training 2023 und 2024) hat 0,92 Mio. Mittel über zwei Folds: 1,62 Mio (RMSE 1.274 €) statt 1,43 Mio. Das ist die ehrlichere Zahl für den Einsatz „2026 vorhersagen", aber auf nur zwei Folds gestützt.

Dass die Reihenfolge hier trotzdem wenig ändert (zufällig gemischt: 1,43 Mio, gleich wie Jahre-Folds), liegt daran, dass der Zusammenhang einfach ist (ein linearer Trend plus Wirkung der Budgets). Das darf man aber nicht voraussetzen, es ist bei anderen Daten oft anders (siehe Tag 10: Zeitreihen, `TimeSeriesSplit`).

---

## Arbeitsauftrag 2: Tuning und Grid Search

### 2.1 Verfahren wählen und begründen

**Gewählt: Random Forest.**

| Kriterium | Random Forest | Gradient Boosting |
|---|---|---|
| Empfindlichkeit gegen die Einstellungen | Gering. Meist auch mit Standardwerten brauchbar, wenige Stellschrauben mit großer Wirkung | Höher. Lernrate, Anzahl Bäume und Tiefe hängen zusammen (kleine Lernrate braucht mehr Bäume) |
| Überanpassung | Mehr Bäume machen es **nicht** schlechter, nur langsamer | Zu viele Bäume oder zu hohe Lernrate überanpassen |
| Parallelisierbar | Ja, Bäume sind unabhängig | Nein, jeder Baum baut auf dem vorigen auf |
| Verrauschte Daten (Messe-Ausreißer) | Mittelung glättet | Folgebäume versuchen, den Ausreißer zu „korrigieren" |
| Genauigkeit auf Tabellen | gut | oft etwas besser |

Das Marketing will nur wissen, **ob** Bäume besser sind. Dafür reicht das robuste Verfahren mit wenig Aufwand. Gradient Boosting wäre eine Alternative (27 Kombinationen, siehe 2.5).

### 2.2 Übliche Werte und Quellen

| Hyperparameter | Standard in sklearn | Zu klein | Zu groß |
|---|---|---|---|
| `n_estimators` (Anzahl Bäume) | 100 | Ergebnis schwankt stark zwischen Läufen, Mittelung greift kaum | Mehr Rechenzeit, **kaum noch Gewinn** (Kurve flacht ab) |
| `max_depth` (Tiefe) | keine Grenze | **Unteranpassung**: Baum zu grob, Training und Validierung schlecht | **Überanpassung**: Training sehr gut, Validierung schlechter |
| `max_features` (Merkmale je Teilung) | alle (1,0) | Jeder Baum sieht zu wenig, Bäume schwächer | Bäume werden einander ähnlich, Mittelung bringt weniger |

Quellen: scikit-learn-Dokumentation (Referenz zu `RandomForestRegressor` und `GradientBoostingRegressor`, Kapitel „Ensemble methods" im User Guide). Die Standardwerte in der Tabelle habe ich direkt in der installierten sklearn-Version (1.9.1) per `get_params()` ausgelesen. Die Tipps zu „zu klein / zu groß" sind Erfahrungswerte aus der Dokumentation und stützen sich hier auf die Ergebnisse in 2.4; Recherche im Netz habe ich nicht gemacht.

**Woran erkennt man zu kleine oder zu große Werte?** Am Vergleich von Trainings- und Validierungsfehler (`return_train_score=True` in `GridSearchCV`):
- Beide Fehler hoch → zu einfach (Tiefe zu klein).
- Training niedrig, Validierung deutlich höher → zu komplex (Tiefe zu groß).
- Fehler ändert sich beim Verdoppeln der Bäume kaum → die Zahl reicht.

### 2.3 Das Grid

| Hyperparameter | Gewählte Werte | Anzahl | Quelle / Begründung |
|---|---|---:|---|
| `n_estimators` | 100, 300, 500 | 3 | 100 ist der sklearn-Standard, darüber prüfen, ob mehr nützt |
| `max_depth` | 3, 5, 8, 12 | 4 | Standard ist „unbegrenzt". Bei nur 104 Trainingswochen sind Tiefen über 12 sinnlos (ein Blatt je Woche) |
| `max_features` | 2, 4, 7 | 3 | 7 Merkmale insgesamt: 7 = alle (Standard), 4 ≈ die Hälfte, 2 ≈ ein Drittel |
| **Kombinationen** | 3 × 4 × 3 | **36** | |
| **Läufe** | 36 × 3 Folds | **108** | Jede Kombination wird k = 3-mal trainiert |

### 2.4 Zu trainierende Modelle und Rechenzeit

```
Kombinationen         = 3 · 4 · 3                = 36
Läufe mit CV (k = 3)  = 36 · 3                   = 108
Rechenzeit            = 108 · 20 s = 2.160 s     = 36 Minuten
+ Endtraining         = 1 · 20 s                 = 20 Sekunden
Gesamt                                           ≈ 36,3 Minuten  (Budget: 60 Minuten)
```

**Es passt in die Stunde** mit gut 23 Minuten Reserve (Fehlversuch, Neustart, Auswertung).

(Die 20 Sekunden je Lauf sind die Annahme der Aufgabe. Auf diesem Rechner dauern alle 108 Läufe zusammen 13 Sekunden, weil der Datensatz klein ist. Die Rechnung ist für den Firmenlaptop gedacht.)

**Wie viele Läufe kostet eine Kombination?** k Läufe, also 3. Das ist der Faktor, den man leicht vergisst: 36 Kombinationen sind **nicht** 36 Läufe.

### 2.5 Wenn es nicht passen würde

| Maßnahme | Wirkung |
|---|---|
| Weniger Werte je Hyperparameter | Aufwand sinkt multiplikativ |
| **Erst grob, dann fein:** grobes Grid, danach ein feines Grid um den besten Bereich | Spart meist am meisten |
| Weniger Folds (k = 2) | Spart ein Drittel, aber die Aussage wird unsicherer |
| `RandomizedSearchCV`: zufällig 20 von 36 Kombinationen | Findet meist eine fast so gute Einstellung |
| Parallel rechnen (`n_jobs=-1`) | Auf einem Laptop mit 8 Kernen weniger Wartezeit, die Rechenzeit der IT wird aber nicht kleiner |
| Verfahren mit weniger Stellschrauben | Boosting: 3 × 3 × 3 = 27 Kombinationen × 3 = 81 Läufe = 27 Minuten |

### 2.6 Der Rat des Kollegen: „einfach alle Werte von 1 bis 100 ausprobieren"

**Rechnung für alle drei Hyperparameter:** 100 × 100 × 100 = 1.000.000 Kombinationen × 3 Folds × 20 s = 60.000.000 s ≈ **694 Tage**. Das Budget beträgt 1 Stunde.

Selbst für **einen** Hyperparameter wären es 100 × 3 × 20 s = 6.000 s = 100 Minuten, über der Stunde.

Außerdem sinnlos: Bei `n_estimators` bringt von 100 auf 101 nichts, Werte wachsen sinnvoll **in Schritten** (100, 300, 500). Bei `max_features` gibt es bei 7 Merkmalen nur die Werte 1 bis 7, alles über 7 ist dasselbe wie 7.

### 2.7 Das Ergebnis der Suche

Die Suche habe ich tatsächlich laufen lassen (3 Jahre-Folds, MSE):

| Rang | `n_estimators` | `max_depth` | `max_features` | MSE |
|---:|---:|---:|---:|---:|
| 1 | 100 | 8 | 4 | **3.328.099** |
| 2 | 300 | 8 | 4 | 3.357.449 |
| 3 | 500 | 8 | 4 | 3.407.179 |
| 4 | 500 | 12 | 4 | 3.448.574 |
| 5 | 300 | 12 | 4 | 3.477.893 |
| schlechtester | 300 | 3 | 2 | 4.609.603 |

Was man ablesen kann:
- **Tiefe:** 3 (4,22 Mio) → 5 (3,60 Mio) → **8 (3,33 Mio)** → 12 (3,45 Mio). Zu flach unteranpasst, zu tief beginnt zu überanpassen. Der beste Wert liegt im Inneren des Grids, gut so: Wäre er am Rand, müsste man das Grid erweitern.
- **Bäume:** 100 reichen, 300 und 500 sind **nicht** besser (leichtes Rauschen).
- **Merkmale je Teilung:** 4 ist besser als 2 oder 7.

### 2.8 Die wichtigste Erkenntnis: lineare Regression ist besser

| Modell (MSE, k = 3 Jahre) | Fold 2023 | Fold 2024 | Fold 2025 | Mittel | RMSE |
|---|---:|---:|---:|---:|---:|
| **Lineare Regression** | 1,19 Mio | 2,17 Mio | 0,92 Mio | **1,43 Mio** | **1.196 €** |
| Random Forest (Standard) | 3,45 Mio | 3,78 Mio | 3,94 Mio | 3,72 Mio | 1.929 € |
| Random Forest (getunt) | | | | 3,33 Mio | 1.824 € |
| Gradient Boosting (getunt, 27 Kombinationen) | | | | 3,33 Mio | 1.824 € |

Tuning bringt rund 10 % (3,72 → 3,33 Mio), der Abstand zur linearen Regression ist **mehr als das Doppelte**. Das Ergebnis gilt auch bei zufällig gemischten Folds (Linear 1,43 Mio, Random Forest 3,03 Mio), liegt also nicht an der Art der Aufteilung.

**Warum verliert der Wald?**

1. **Trend:** Der Umsatz wächst mit der Zeit (Spalte `Woche`, ca. +25 € je Woche). Bäume geben nur Werte aus, die sie im Training gesehen haben, und können einen Trend **nicht fortsetzen**. Testet man 2025 und hat gerade Wochen 105 bis 156 aus dem Training herausgenommen, kennt der Baum keine so hohen Wochen.
2. **Einfacher, nahezu linearer Zusammenhang:** Die Budgets wirken fast proportional (Social ca. 2 € je 1 € Budget, Newsletter ca. 3 €, Rabattaktion ca. +2.400 €). Das liegt der Geraden, nicht den Stufen eines Baums.
3. **Wenig Daten:** 104 Trainingswochen sind für 7 Merkmale und Baumstufen knapp.

Der Beleg für den Trend: Lässt man die Spalte `Woche` aus der linearen Regression weg, steigt deren MSE von 1,43 auf **4,16 Mio**. Ohne den Trend ist die Gerade ähnlich schlecht wie der Wald (3,3 bis 3,7 Mio).

**Antwort an die Marketingleitung:** Der Baumansatz ist hier **nicht besser**, auch nach 36 getesteten Einstellungen nicht. Wer das Budget 2026 planen will, bleibt bei der **linearen Regression**. Ein Vorteil: Sie ist erklärbar („1 € mehr Newsletter bringt rund 3 € Umsatz"), der Wald nicht.

*Vorbehalt:* Dass die lineare Regression gewinnt, gilt für **diese** Daten. Hätte der Umsatz Schwelleneffekte („ab 2.000 € Social-Budget flacht die Wirkung ab"), könnte ein Baum aufholen.

---

## Was in den Zusatzinformationen steckt (Arbeitsauftrag 2)

| Angabe | Bedeutung für das Ergebnis |
|---|---|
| Termin: Quartalsrunde im Januar | Es gibt eine feste Frist. Das Rechenbudget (1 Stunde) ist Teil der Aufgabe, kein Zusatz. |
| **Newsletter ab 2026 zweimal pro Woche** | Das Modell hat **nie** gesehen, was zwei Newsletter pro Woche bewirken. Ob 2 × 1.000 € doppelt so viel Umsatz bringen oder nur 1,3-mal, ist aus den Daten nicht ablesbar. **Extrapolation außerhalb der Trainingsdaten.** Hier ist die lineare Regression gefährlicher (sie setzt die Gerade endlos fort), der Baum hält sich an gesehene Werte. Prognose daher als **Spanne** angeben und nach Start des neuen Rhythmus nachtrainieren. |
| **Zweiter Röststandort in Hamburg 2026** | Ein neuer Standort ändert Kunden, Kapazität und Versand. Die Daten kommen nur aus Lüneburg. Das Modell ist für **Hamburg nicht gültig**. Auch hier **Verteilungsverschiebung** (Drift): Im Betrieb überwachen, wie in Tag 10 beschrieben. |
| „Alle Werte von 1 bis 100" | Siehe 2.6. |

## Kernaussagen

- **k wählt man nach den Daten:** hier k = 3, ein Fold je Jahr, damit jeder Fold alle Jahreszeiten enthält.
- **Der Mittelwert der Folds ist robust, die Streuung ist der Befund.** Ein Ausreißerereignis (Messe) verdirbt einen ganzen Fold, weil der MSE quadriert.
- **Grid-Größe = Produkt der Werte je Hyperparameter, Läufe = Kombinationen × k.** Immer vor dem Start nachrechnen, besonders bei „alle Werte von 1 bis 100".
- **Der beste Wert sollte im Inneren des Grids liegen**, nicht am Rand.
- **Tuning rettet kein falsches Verfahren:** Der Wald wird durch Tuning rund 10 % besser, die Gerade ist aber mehr als doppelt so gut. Erst Baseline schlagen, dann tunen.
- **Neue Entwicklungen (Newsletter, Hamburg) liegen außerhalb der Daten.** Kein Tuning und kein Modell kann sie vorhersagen. Das gehört offen in die Empfehlung.

## Abweichungen und Annahmen

- Das mitgelieferte Skript `12_02_UE2_Arbeitsauftrag1_CV.py` läuft mit unserer CSV **nicht** (es sucht `1202_UE2_…`, erwartet Semikolon und Dezimalkomma; unsere Datei heißt `12_02_…` und nutzt Kommas). Ich habe die Folds mit sklearn nachgebaut: gleiches Modell (lineare Regression mit den 7 Spalten), gleiche Fold-Einteilung. Die Zahlen für k = 2, `NUR_VERGANGENHEIT` und k = 3 habe ich außerdem mit eigenem Code gegengerechnet, das Original-Skript selbst nicht gestartet.
- Die 20 Sekunden je Lauf sind die Annahme der Aufgabe; gemessen dauern alle 108 Läufe auf diesem Rechner 13 Sekunden.
- Die Folds in Arbeitsauftrag 2 sind dieselben Jahres-Folds wie in Arbeitsauftrag 1 (Aufgabe: „Ihr k aus Arbeitsauftrag 1"). Bei anderem k ändern sich die Läufe (k = 5 → 180 Läufe = 60 Minuten, knapp am Limit).
- Die Aussage zu Social-Media-Werkstudentin und Bio-Siegel als Ursache der Fold-Unterschiede ist nur Vermutung. Belegt ist der Messeeffekt.
- Gradient Boosting wurde nur als Vergleich gerechnet (3 × 3 × 3, beste Einstellung: 300 Bäume, Lernrate 0,03, Tiefe 2, MSE 3,33 Mio).
- Die Fehler der Wochen 17 und 35 habe ich nicht erklärt, die Aufgabe nennt keine Ursache.
- Gerendert habe ich die Tabellen und das Farbfeld nicht.
