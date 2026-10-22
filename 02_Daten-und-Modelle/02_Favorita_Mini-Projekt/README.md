# Favorita Mini-Projekt – Nachfrageprognose

Lernprojekt zur Fortbildung „Predictive Analytics & Algorithmen“. Daten: Kaggle *Store Sales – Time Series Forecasting*
(54 Filialen × 33 Produktfamilien, tägliche Verkäufe 2013 bis 2017).

**Ziel:** den Absatz je Filiale und Produktfamilie für die nächsten **16 Tage** vorhersagen und nachvollziehen, welche Datenprobleme
und Modellentscheidungen dabei wichtig sind. Der ausführliche Bericht mit allen Entscheidungen steht in `reports/01_EDA_und_Zielgroesse.md`.

## Inhalt

1. [Ergebnisse auf einen Blick](#ergebnisse-auf-einen-blick)
2. [Wo finde ich was?](#wo-finde-ich-was)
3. [Alles nachvollziehen](#alles-nachvollziehen)
4. [Fragen und Antworten](#fragen-und-antworten)
5. [Regeln für dieses Projekt](#regeln-für-dieses-projekt)

## Ergebnisse auf einen Blick

Fehlermaß RMSLE (kleiner ist besser), Mittel über drei Validierungsfenster zu je 16 Tagen:

| Stufe | Modell | RMSLE | gegen Benchmark |
|---|---|---|---|
| 1 | Baseline: Mittel der letzten 4 gleichen Wochentage (Benchmark) | 0,5256 | - |
| 2 | Statistisch: exponentielle Glättung je Reihe | 0,4822 | -8,3 % |
| 3 | LightGBM über alle Reihen | **0,4095** | **-22,1 %** |

Erfolgskriterium (mindestens 10 % besser als der Benchmark, im Mittel und in mindestens zwei von drei Fenstern) ist mit LightGBM erreicht.
Der Gewinn kommt aus den Kontextmerkmalen (Filiale und Familie, Monat, Aktion), nicht vom Algorithmus allein (Details: Bericht 3.9).

## Wo finde ich was?

```
02_Favorita_Mini-Projekt/
├── README.md              diese Datei: Überblick, Struktur, Fragen und Antworten
├── pyproject.toml         Projektumgebung (uv); uv.lock fixiert die genauen Versionen
├── data/
│   ├── raw/               Kaggle-Rohdaten (train, test, stores, oil, holidays, transactions)
│   └── clean/             Ausgabe von clean.py: train_clean.parquet, test_clean.parquet
├── src/                   der Code, die Quelle für alles andere (Tabelle unten)
├── notebooks/             01 bis 09: derselbe Code als Notebook, mit Erklärtext und gespeicherten Ausgaben
└── reports/
    ├── 01_EDA_und_Zielgroesse.md   der Bericht: Befunde, Entscheidungen, Ergebnisse
    ├── *_output.txt                gedruckte Ausgabe je Skript (Quelle der Zahlen im Bericht)
    ├── results_*.csv               Ergebniszahlen, die spätere Stufen einlesen (z. B. der Benchmark)
    ├── forecast_next16.csv         Quantil-Prognose 16. bis 31.08.2017 je Filiale, Familie und Tag
    ├── gbm_importance.csv          Merkmalswichtigkeit von LightGBM
    └── figures/                    Plots
```

`data/` ist nicht für die Versionsverwaltung gedacht (`.gitignore`). `.venv/`, `src/__pycache__/` und `notebooks/.ipynb_checkpoints/`
entstehen automatisch und gehören nicht zum Projekt.

### Welche Datei gehört zu welcher Phase?

Die Phasen A bis I sind der Plan im Bericht (Abschnitt 4).

| Phase | Frage | Code in `src/` | Notebook | Ergebnis |
|---|---|---|---|---|
| **A. Daten** | Was ist an den Daten falsch, und wie bereinigen wir? | `eda_checks.py`, `eda_plots.py`, `explore_promo_closures.py`, `clean.py` | 01, 02, 03 | `data/clean/`, Bericht 2.1 bis 2.8 |
| **B. Ausreißer** | Welche Extremwerte sind Fehler? | `outliers.py`, `masking.py` | 04 | 212 isolierte Spitzen, Spalte `sales_train`, Bericht 2.9 |
| **C. Validierung** | Wie bewerten wir jedes Modell fair? | `forecast_eval.py` (Modul) | | drei Fenster W1 bis W3, RMSLE |
| **D. Stufe 1** | Was ist das Minimum, das ein Modell schlagen muss? | `baselines.py` | 05 | `results_baselines.csv`, Bericht 3.6 |
| **E. Stufe 2** | Hilft ein statistisches Modell je Reihe? | `stat_models.py` (Modul), `statistical.py` | 06 | `results_statistical.csv`, Bericht 3.7 |
| **F. Stufe 3** | Hilft ein gemeinsames gelerntes Modell über alle Reihen? | `gbm_model.py` (Modul), `gbm.py`, `leakage_check.py` | 07 | `results_gbm.csv`, Bericht 3.8 |
| **G. Gegenproben** | Was zieht wirklich Gewicht? | `counter_tests.py` | 08 | `results_counter_tests.csv`, Bericht 3.9 |
| **H. Fallstudie** | Alles für die Fallstudie aufschreiben | | | offen |
| **I. Nachbestellung** | Wie viel Ware reicht mit 75 % oder 90 % Wahrscheinlichkeit? | `quantile.py` | 09 | `results_quantile.csv`, `forecast_next16.csv`, Bericht 3.10 |

### Wie hängen die Dateien zusammen?

```
data/raw ──► clean.py ──► data/clean ──┬──► eda_* / outliers / explore_*  (anschauen und verstehen)
              ▲                        │
              └── masking.py           └──► forecast_eval.py  (Fenster, RMSLE, Baselines)
                                                │
              ┌─────────────────────────────┼──────────────────────┐
         baselines.py ──► statistical.py ──► gbm.py            counter_tests.py
        (Benchmark als     (+ stat_models)   (+ gbm_model)     (+ gbm_model, masking)
         results_*.csv)
```

Pfeile zwischen `baselines`, `statistical` und `gbm` bedeuten: Das spätere Skript liest die Ergebnisdatei des früheren für den Vergleich.
`counter_tests.py`, `leakage_check.py` und `quantile.py` rechnen ihre LightGBM-Modelle selbst und brauchen nur `data/clean/`.

- **Module** (`forecast_eval`, `stat_models`, `gbm_model`, `masking`) enthalten wiederverwendbare Funktionen und werden nie direkt gestartet.
  Alle anderen Dateien laufen und drucken ihre Ergebnisse.
- **`clean.py` ist das Tor:** Alles Spätere liest `data/clean/`, nie die Rohdaten. So gilt jede Bereinigungsentscheidung überall.
- **Die Vergleichsstufen lesen frühere Ergebnisse:** `statistical.py` liest den Benchmark aus `results_baselines.csv`, `gbm.py` zusätzlich `results_statistical.csv`. Deshalb ist die Reihenfolge unten wichtig.

## Alles nachvollziehen

Alle Befehle aus dem Projektordner `02_Favorita_Mini-Projekt/`.

```bash
uv sync                                                          # Umgebung installieren
uv run kaggle competitions download -c store-sales-time-series-forecasting -p data
unzip data/store-sales-time-series-forecasting.zip -d data/raw   # Kaggle-Login nötig, Regeln einmal akzeptieren
uv run python src/eda_checks.py                           # 1. Datenqualität: Duplikate, Lücken, Nullen
uv run python src/eda_plots.py                            # 2. Plots in reports/figures/
uv run python src/clean.py                                # 3. Bereinigung -> data/clean/
uv run python src/explore_promo_closures.py               # 4. Promotion-Start, Schließungen, Feiertage
uv run python src/outliers.py                             # 5. Ausreißer Schritt für Schritt
uv run python src/baselines.py                            # 6. Baselines und Benchmark
uv run python src/statistical.py                          # 7. Statistisches Modell je Reihe
uv run python src/gbm.py                                  # 8. LightGBM über alle Reihen
uv run python src/leakage_check.py                        # 9. Leckage-Test für LightGBM
uv run python -u src/counter_tests.py                     # 10. Gegenproben (dauert ca. 15 Minuten)
uv run python -u src/quantile.py                          # 11. Quantil-Prognose für Nachbestellungen (ca. 12 Minuten)
```

Jedes Skript druckt seine Befunde und schreibt sie zusätzlich nach `reports/*_output.txt`.
Skripte 4 bis 11 brauchen die Ausgabe von Skript 3. Skript 7 braucht zusätzlich die Ergebnisse von Skript 6, Skript 8 die von 6 und 7.
Alle Läufe sind reproduzierbar (feste Zufallszahlen): Ein erneuter Lauf liefert dieselben Zahlen, nur die Laufzeiten unterscheiden sich.

### Einmalige Einrichtung

- LightGBM braucht auf macOS `brew install libomp`.
- Jupyter-Kernel anlegen: `uv run python -m ipykernel install --user --name favorita --display-name "Favorita (uv)"`.
- **Ordner umbenannt oder verschoben?** Dann zeigen die Programme in `.venv/bin` auf den alten Pfad. Abhilfe: `uv sync --reinstall`
  und den Kernel mit dem Befehl oben neu anlegen.

### Notebooks

Die Analyse-Skripte `eda_checks`, `eda_plots`, `explore_promo_closures`, `outliers`, `baselines`, `statistical`, `gbm`, `counter_tests` und `quantile`
sind im Jupytext-Format geschrieben (`# %%` trennt Zellen, `# %% [markdown]` sind Erklärtexte). Sie laufen als Skript **und** als Notebook.
Die Quelle ist immer `src/*.py`.

```bash
uv run jupyter lab notebooks/                   # Notebooks im Browser öffnen
# Notebook nach Änderung am Skript neu erzeugen und ausführen:
uv run jupytext --to ipynb --set-kernel favorita --output notebooks/04_outliers.ipynb src/outliers.py
uv run jupyter nbconvert --to notebook --execute --inplace notebooks/04_outliers.ipynb
```

Änderungen nicht von Hand in die `.ipynb` schreiben, sondern in `src/*.py` und das Notebook neu erzeugen, sonst laufen beide auseinander.
In Neovim lassen sich die `.py`-Dateien mit `# %%`-Zellen direkt bearbeiten (z. B. mit `jupytext.nvim` oder `molten.nvim` zellweise ausführen).

## Fragen und Antworten

Hier stehen Fragen, die beim Arbeiten aufgekommen sind, mit kurzen Antworten. Der Bericht geht tiefer.

### Begriffe

**Was ist eine „Reihe“ (series)?**
Der Absatz **einer Filiale mit einer Produktfamilie über die Zeit**, also ein (Filiale, Familie)-Paar mit einer Zahl je Tag, z. B. Filiale 5 × `BEVERAGES`.
Es gibt 54 × 33 = **1.782 Reihen**, und sie sind die Einheit, die wir vorhersagen. Eine 16-Tage-Prognose besteht aus 1.782 × 16 = 28.512 Zahlen.
Reihen sind sehr unterschiedlich groß (`PRODUCE` tausende pro Tag, `BOOKS` fast nichts) und können spät beginnen (neue Filiale, neu eingeführte Familie).
Ergebnisse „je Familie“ mitteln die Fehler der 54 Reihen dieser Familie.

**Was heißt „16 Tage Horizont“, und ist das schon die statistische Methode?**
Nein. Der Horizont ist nur, **wie weit** wir vorausschauen. Er sagt nichts über Methode oder genutzte Historie. In allen Stufen werden dieselben 16 Tage vorhergesagt,
die Stufen unterscheiden sich in der Historie und im Verfahren: Baseline 1 bis 4 Wochen, statistisches Modell 365 Tage je Reihe, LightGBM 730 Tage Training über alle Reihen.
„Die letzten zwei Wochen als Grundlage“ entspricht eher der Baseline.

**Was ist ein „Prognose-Ursprung“?**
Der letzte Tag, den das Modell kennen darf. Alles danach ist für das Modell Zukunft. Eingaben dürfen nur aus Tagen bis zum Ursprung stammen (oder aus Dingen, die
auch in der Zukunft bekannt sind, wie Kalender und geplante Aktionen).

**Was ist „Leckage“ (Leakage), und wie prüfen wir sie?**
Wenn das Modell im Training etwas kennt, was es bei der echten Prognose nicht kennen kann. Beispiel: `transactions` gibt es in `test.csv` nicht, deshalb nutzen wir sie nicht.
`src/leakage_check.py` ersetzt alle Verkäufe nach dem Ursprung durch Zufallszahlen. Bleibt die Prognose gleich, hängt sie nicht von der Zukunft ab (Ergebnis: identisch).

### Fehlermaß und Ziel

**Wie ist RMSLE definiert?**
Für jede Prognose (Reihe, Tag): `Fehler = ln(1 + Prognose) − ln(1 + wahrer Wert)`. Alle Fehler quadrieren, mitteln, Wurzel ziehen.
Das misst **relative** Abweichungen, nicht Stückzahlen: 100 wahr und 150 prognostiziert ergibt etwa 0,40, 10 wahr und 15 prognostiziert ergibt etwa 0,38.
Eine Prognose von 3 bei wahrem Wert 0 ergibt 1,39, ein Treffer 0.

**Wie lese ich einen RMSLE-Wert, z. B. 0,16 oder 1,5?**
Mit `e^RMSLE` bekommt man den typischen Abweichungsfaktor. 0,16 bedeutet etwa Faktor 1,17 (rund 17 % daneben, `PRODUCE`).
1,5 bedeutet etwa Faktor 4,5 (`SCHOOL AND OFFICE SUPPLIES` ohne Aktion). Das ist nur eine grobe Faustregel: RMSLE ist ein quadratisches Mittel,
große Fehler zählen mehr. Bei sehr kleinen Mengen dämpft die „+1“ im Logarithmus.

**Was bedeutet das „10 %-Ziel“?**
Nicht „auf 10 % genau“. Es ist eine **relative Verbesserung des Fehlers gegenüber dem Benchmark**: RMSLE des Modells ≤ 0,9 × RMSLE der besten Baseline.
Beispiel Mittel: 0,9 × 0,5256 = 0,4730. LightGBM hat 0,4095.

**Was bedeuten die Prozentwerte in den Gegenproben (z. B. „+7,7 %“)?**
Die relative Änderung des RMSLE gegenüber dem Basismodell: ohne Aktion 0,4412 / 0,4095 = 1,077, also +7,7 %. Im Mittel über 1.782 Reihen wirkt das klein (typischer Faktor 1,51 gegen 1,55).
Eindrücklicher ist der Anteil am Gesamtgewinn: Gegenüber dem Benchmark haben wir 0,116 gewonnen, ohne Aktion gehen davon 0,032 verloren (etwa 27 %),
ohne Filial- und Familienmerkmale etwa 34 %, ohne Monat etwa 23 %. Und in einer einzelnen Familie kann der Effekt groß sein: `SCHOOL AND OFFICE SUPPLIES` fällt ohne Aktion von Faktor 2,0 auf 4,2.

**Wie viel schwankt ein Ergebnis allein durch den Zufall?**
Etwa 0,6 % im Mittel, in einzelnen Fenstern bis 0,8 % (Test „Basis, andere Zufallszahlen“). Änderungen unter etwa 1 % sind deshalb nicht belastbar.

### Transformation und Pandas

**Was ist `log1p(sales)`, und was ist der natürliche Logarithmus?**
`ln(x)` ist die Potenz, mit der man die Eulersche Zahl e (≈ 2,718) potenzieren muss, um x zu bekommen: `ln(x) = y` heißt `e^y = x`.
`log1p(x)` ist `ln(1 + x)`, das „+1“ erlaubt Nullen (`ln(0)` gibt es nicht). Wir trainieren auf `log1p(sales)`, weil das zu RMSLE passt, große Werte beruhigt und relative Fehler gleich behandelt.
Zurückrechnen mit `expm1`, danach auf mindestens 0 begrenzen.

**Was macht `isna()`?**
Eine pandas-Funktion, die für jeden Wert `True` liefert, wenn er fehlt (`NaN`/`None`). Mit `isna().sum()` zählt man die fehlenden Werte, `isna().mean()` gibt den Anteil.
Eine `0` ist **nicht** fehlend, deshalb findet `isna()` weder unsere strukturellen Nullen noch die Aktions-Nullen vor 2014.
Verwandt: `notna()` (Gegenteil), `dropna()`, `fillna()`, `ffill()` und `bfill()` (vom vorigen bzw. nächsten Wert auffüllen).

### Daten und Bereinigung

**Was ist „Maskieren“, und warum nicht löschen oder kappen?**
Der Wert wird in der Spalte `sales_train` auf fehlend (`NaN`) gesetzt, die Zeile bleibt und `sales` behält den Rohwert. Löschen reißt Lücken in die Zeitachse und stört Mittelwerte über Tage.
Kappen (z. B. auf das 10-Fache des 99. Perzentils) lässt bei 89.576 immer noch eine absurde Zahl übrig. Der eigentliche Schaden einer Spitze entsteht in den Merkmalen (Mittel der letzten Wochen).
Maskiert werden 212 isolierte Spitzen, die 6.015 Zeilen vom 25. Dezember und die 18.998 Zeilen mit geschlossener Filiale.

**Was ist `promo_known`, und woher wissen wir überhaupt etwas über Aktionen?**
Quelle ist allein die Spalte `onpromotion` in `train.csv` und `test.csv`: Anzahl der Artikel einer Familie, die in der Filiale an diesem Tag in Aktion waren. Es gibt keine Angabe zu Rabatt, Art oder Artikel.
Bis 2014 steht überall 0. Das ist vermutlich eine fehlende Erfassung, nicht „keine Aktion“ (Annahme, das Dataset sagt es nicht). Der Start ist je Filiale verschieden (April bis Juli 2014, neue Filialen später).
`promo_known` ist 0 vor dem ersten Eintrag einer Filiale und danach 1, damit das Modell „echte Null“ von „unbekannt“ unterscheiden kann.
Die Gegenprobe zeigt: Bei 730 Trainingstagen ist das irrelevant, weil das Training erst nach dem Start der Erfassung beginnt.

**Warum gibt es drei Arten von Nullen?**
Eine Null kann heißen: die Filiale oder Familie gab es noch nicht (strukturell, wird entfernt), niemand hat gekauft (echt, bleibt) oder die Ware war ausverkauft (nicht erkennbar, es gibt keine Bestandsdaten).

**Sind die großen Werte alle Fehler?**
Nein. Es gibt isolierte Spitzen (vermutlich Fehler oder Großbuchung), saisonale Spitzen (z. B. Dezember, echt) und Niveausprünge (z. B. Wiedereröffnung einer Filiale, echt).
Nur die isolierten Spitzen werden maskiert (Bericht 2.9).

### Modell

**Was heißt „ein Modell trainieren“?**
Dem Modell werden Millionen vergangene Beispiele gezeigt, bei denen die richtige Antwort bekannt ist, und es stellt seine Parameter so ein, dass seine Vorhersagen den wahren Werten möglichst nahekommen.
LightGBM besteht aus 500 kleinen Entscheidungsbäumen, die nacheinander die Fehler der vorigen ausgleichen. Ein Trainingsbeispiel ist: Reihe, Zieltag, Abstand zum Ursprung (1 bis 16 Tage), Eingaben, richtige Antwort `log1p(sales)`.
Validierung heißt, das trainierte Modell auf 16 Tagen zu prüfen, die es nie gesehen hat.

**Warum genau diese Merkmale?**
Eine Eingabe muss zum Prognosezeitpunkt bekannt sein und es muss einen Grund geben, dass sie den Absatz beeinflusst.

| Merkmal | Grund |
|---|---|
| Mittel der letzten 7/28/91/364 Tage, gleicher Wochentag früherer Wochen | aktuelles Niveau und Wochenrhythmus |
| Wochentag, Monat, Tag im Monat, Feiertag, Ereignis | Kalendereffekte (Dezember, Schulbeginn, Zahltage) |
| Aktion (`onpromotion`, `promo_known`) | die Fallstudie nennt fehlende Aktionsdaten als Kernproblem, und Aktionen sind vorab bekannt |
| Filiale, Familie, Filialtyp, Stadt, Region, Cluster | Reihen unterscheiden sich, ähnliche können Muster teilen |
| Alter der Reihe, Tage seit letztem Wert, Abstand h | neue oder wiedereröffnete Reihen, frische Daten zählen mehr |

Absichtlich weggelassen: `transactions` (Leckage) und der Ölpreis (Gegenprobe zeigt keinen Nutzen). Ob jede Gruppe wirklich nützt, zeigt der Weglasstest (Bericht 3.9).

**Warum bringt „Merkmalswichtigkeit“ weniger Aufschluss als der Weglasstest?**
Die Wichtigkeit (Gain) zeigt, wo das Modell beim Trainieren Fehler abgebaut hat, und unterschätzt Merkmale, die nur in wenigen Reihen viel ausmachen. `aktion` hatte 0,2 %, das Weglassen kostet +7,7 %.

**Warum Skript *und* Notebook, schließt sich das aus?**
Nein. Die Quelle ist eine normale `.py`-Datei mit Zellenmarkierungen (Jupytext). Sie läuft als Skript und wird daraus als Notebook erzeugt. So gibt es nur eine Quelle, die Notebooks sind Ansicht mit Erklärtext und Ausgaben.

### Anwendung

**Was bedeutet das Ergebnis im echten Leben, z. B. für Nachbestellungen?**
Das Modell prognostiziert **Absatz**, nicht Nachfrage: War Ware ausverkauft, sieht man nur, was verfügbar war, und das Modell wiederholt den Mangel.
Außerdem ist die Prognose ein typischer Wert (nahe am Median), Bestellmengen brauchen einen höheren Wert (z. B. die Menge, die an 9 von 10 Tagen reicht).
Eine Bestellmenge ergibt sich etwa aus: Prognose über Lieferzeit plus Bestellintervall, plus Sicherheitsbestand, minus Bestand und offene Bestellungen. Dafür fehlen hier Bestand, Lieferzeiten, Packungsgrößen, Haltbarkeit und Kosten.
Der Horizont von 16 Tagen deckt nur Lieferzeiten bis dahin ab.
Betrieb heißt: regelmäßig laufen lassen, Prognose und Ist vergleichen (Monitoring), neu trainieren, und Schwachstellen (saisonale, sehr dünne Reihen) von Menschen prüfen lassen.

**Was macht eine Quantil-Prognose (z. B. 90 %)?**
Statt „was verkauft sich typischerweise“ beantwortet sie „wie viel verkauft sich höchstens, an 9 von 10 Tagen“. Das Modell wird dafür mit `objective="quantile"` und `alpha=0.9` trainiert, sonst ändert sich nichts. Das 90-%-Quantil ist im Mittel 25 % höher als der Median, bei stabilen Reihen weniger, bei schwankenden mehr (Bericht 3.10, `src/quantile.py`).
Die Prognose aus 3.8 ist dagegen ein typischer Wert, wer genau diese Menge bestellt, hat an etwa jedem zweiten Tag zu wenig.

**Wie gut stimmt „90 %“ wirklich?**
Das prüft die **Abdeckung**: Anteil der Tage, an denen der echte Absatz höchstens so hoch war wie die Prognose. In unseren drei Fenstern liegt sie für das 90-%-Quantil bei 91,9 % / 90,2 % / 89,2 %. Je Familie schwankt sie stark: `SCHOOL AND OFFICE SUPPLIES` nur 78,8 %, `BOOKS` 99,2 %.
Der Median zeigt 56 % statt 50 %, weil Tage mit Absatz 0 als abgedeckt zählen.

**Warum kann ich die 16 Tagesquantile nicht einfach addieren?**
Gute und schlechte Tage gleichen sich in der Summe teilweise aus. Die Summe der Tages-90-%-Werte deckt den 16-Tage-Absatz zu 96,9 % ab statt zu 90 %, du bestellst also zu viel. Die Summe der Mediane deckt nur 43 % ab. Für die Summe passt in unseren Fenstern das 80-%-Quantil am besten (91,1 % Abdeckung, +15,5 % Ware gegenüber dem Median statt +25 %). Gewählt auf denselben drei Fenstern, an denen es geprüft wird: eine Faustregel, kein verlässlicher Wert.

**Was ist die „Pinball“-Verlustfunktion?**
Das Fehlermaß, das ein Quantil-Modell beim Training minimiert. Zu niedrig liegen kostet `alpha` je Einheit Fehler, zu hoch liegen `1 - alpha`. Bei `alpha = 0.9` ist Unterbestand also neunmal so teuer wie Überbestand, deshalb liegt die Prognose höher. RMSLE passt hier nicht, weil das Quantil absichtlich verzerrt ist.

## Regeln für dieses Projekt

- **Jede Zahl im Bericht muss auf ein Skript zurückführbar sein.** Einmal-Befehle im Terminal gehören nicht in den Bericht. Untersuchungen kommen zuerst in `src/`, dann die Zahl in den Bericht.
- **`src/` ist die Quelle.** Notebooks und `reports/` werden daraus erzeugt, nicht von Hand geändert.
- **Fragen, die beim Arbeiten aufkommen, gehören in „Fragen und Antworten“.** Wer etwas nachfragen muss, hilft damit dem Nächsten: kurze Antwort, mit Zahlen aus unseren Daten, Verweis auf den Bericht.
