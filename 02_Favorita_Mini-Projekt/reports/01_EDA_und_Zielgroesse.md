# Mini-Projekt Favorita: EDA, Datenbereinigung und Zielgröße

> Entwurf. Alle Zahlen stammen aus Skripten in `src/` (Reihenfolge und Ausführung: `README.md`). Rohausgaben liegen in `reports/*_output.txt`, Plots in `reports/figures/`.
> Zuordnung: 3.9 `counter_tests.py` · 3.8 `gbm.py` mit `gbm_model.py` und `leakage_check.py` · 3.7 `statistical.py` mit `stat_models.py` · 3.6 `baselines.py` mit `forecast_eval.py` · Abschnitte 1 bis 2.3 `eda_checks.py` · 2.4 und 2.8 (Promotion, Schließungen) `explore_promo_closures.py` · 2.5 und 2.8 (Ausreißer) `outliers.py` · 2.8 (Ergebnis) `clean.py`
> `TODO` = Entscheidung für uns beide · `?` = Vermutung, noch nicht belegt

## 1. Die Daten im Überblick

| Tabelle | Zeilen | Inhalt |
|---|---|---|
| `train.csv` | 3.000.888 | Absatz je Tag × Filiale × Produktfamilie, 2013-01-01 bis 2017-08-15 |
| `test.csv` | 28.512 | gleiche Struktur ohne `sales`, 2017-08-16 bis 2017-08-31 (16 Tage) |
| `stores.csv` | 54 | Stadt, Region, Typ, Cluster |
| `oil.csv` | 1.218 | Ölpreis (externe Quelle) |
| `holidays_events.csv` | 350 | Feiertage und Ereignisse |
| `transactions.csv` | 83.488 | Anzahl Bons je Filiale und Tag |

54 Filialen × 33 Produktfamilien = 1.782 Zeitreihen. Sie sind mit der Filiale × Produktgruppe aus der Aufgabe bei Gartenwelt Berger vergleichbar.

## 2. Bereinigung: Befund und Entscheidung

Leitidee aus UE 1: erst prüfen, dann bewusst entscheiden (löschen, schätzen, ersetzen, markieren), nie blind rechnen.

### 2.1 Duplikate

| Prüfung | Befund | Entscheidung |
|---|---|---|
| `train`: identische Zeilen | 0 | nichts zu tun |
| `train`: doppelter Schlüssel (Datum, Filiale, Familie) | 0 | nichts zu tun |
| `transactions`, `oil`: doppelte Schlüssel | 0 | nichts zu tun |
| `holidays`: gleiches Datum und Ort | 7 | prüfen, dann zusammenführen |
| `holidays`: mehrere Einträge am selben Tag | 38 | gewollt (z. B. Feiertag und Event), je Tag zu Flags verdichten |

Die Absatzdaten sind in dieser Hinsicht sauber. Das Doppelte steckt in den Feiertagen, und die Ursache ist dort inhaltlich: ein Tag kann mehrere Einträge haben.
Auch **verlegte Feiertage** brauchen eine Regel. 12 Zeilen sind `Holiday` mit `transferred = True`: an diesem Tag ist **kein** Feiertag. Der echte Feiertag steht in einer der 12 `Transfer`-Zeilen. Wer `type` nicht auswertet, kennzeichnet den falschen Tag.

### 2.2 Fehlende Werte

| Was fehlt | Befund | Entscheidung |
|---|---|---|
| `train`, `stores`, `holidays`, `transactions`: Nullwerte | keine | nichts zu tun |
| `oil`: Preis leer | 43 Einträge leer, dazu Tage ohne Zeile (Wochenenden, Feiertage) | auf Kalender erweitern, dann letzten bekannten Preis übernehmen (`ffill`), erste Lücke mit `bfill` |
| 25. Dezember | Tag fehlt komplett in 2013 bis 2016 (4 Tage) | Filialen sind geschlossen. Als „geschlossen“ markieren und nicht in Training und Bewertung nehmen |
| 1. Januar | Gesamtabsatz nur 2.512 bis 16.433 statt ca. 700.000 | fast alle Filialen zu. Ebenfalls als Sondertag markieren |
| `onpromotion` | Bis 2014-03-31 überall 0, danach in 28 % der Zeilen größer 0; Start je Filiale gestaffelt | Flag `promo_known` je Filiale, siehe 2.4 |

Der Ölpreis hat nur dann Sinn, wenn man weiß, wofür man ihn nutzt: Ecuador ist ölabhängig, er ist also ein grober Konjunkturindikator (`?` ob er der Prognose wirklich hilft, das testen wir später).

### 2.3 Nullen sind nicht gleich Nullen

31 % aller Zeilen haben `sales = 0`. Das sind drei verschiedene Dinge:

| Art der Null | Beispiel aus den Daten | Entscheidung |
|---|---|---|
| Filiale existiert noch nicht | 8 von 54 Filialen starten spät, z. B. Filiale 52 erst am 2017-04-20 (1.566 Nulltage davor) | führende Nullen **entfernen** |
| Produktfamilie wird noch nicht geführt | `BOOKS` erst ab 2016-10-08, `BABY CARE` ab 2014-03-01, mehrere weitere ab 2014-01 | führende Nullen je Filiale × Familie **entfernen** |
| Echte Null: niemand hat gekauft | langsame Familien wie `BOOKS`, `BABY CARE`, `SCHOOL AND OFFICE SUPPLIES` | **behalten**, das ist echte Information |

Eine Null kann auch ein **Ausverkauf** sein. Genau das war bei Gartenwelt Berger „Absatz ≠ Nachfrage“. Ohne Bestandsdaten können wir es hier nicht unterscheiden. Das halten wir als Einschränkung fest.

### 2.4 Promotion: unbekannt ist nicht „keine Aktion“

Quelle ist allein die Spalte `onpromotion` in `train.csv` und `test.csv`: die Anzahl der Artikel einer Familie, die in dieser Filiale an diesem Tag in Aktion waren. Es gibt keine eigene Aktionstabelle, und wir erfahren weder Rabatthöhe noch Art noch welche Artikel.

**Befund:** 2013 steht überall 0, 2014 bei 10 % der Zeilen eine Aktion, 2017 bei 45 %.

**Annahme (`?`):** Das ist eher ein Erfassungsproblem als ein echter Sprung. Vor dem ersten Eintrag ist unbekannt, ob es Aktionen gab. Das Dataset sagt das nicht, es ist unser Schluss aus dem Muster. Das ist die „fehlende Aktionsdaten“-Situation der Fallstudie.

**Der Start ist je Filiale verschieden:** Das erste `onpromotion > 0` liegt je nach Filiale zwischen 2014-04-01 und 2014-07-25 (gestaffelt). Sechs später eröffnete Filialen starten erst 2015-02-13 bis 2017-04-21, jeweils direkt nach ihrer Eröffnung. Ein einziges globales Datum wäre falsch.

**Entscheidung:** Flag `promo_known` je Filiale: 0 vor dem ersten Datum mit `onpromotion > 0` dieser Filiale, danach 1. Alle Daten bleiben erhalten. Das Modell kann so „echte Null“ (`promo_known = 1`) von „unbekannt“ (`promo_known = 0`) trennen.
Einschränkung: Das erste Datum ist der früheste Beleg, nicht der Beweis für den Erfassungsbeginn.
`TODO` Gegenprobe später: nur mit `promo_known = 1` trainieren und Validierungsfehler vergleichen.

### 2.5 Ausreißer und Sondertage

- Größter Tageswert: 124.717 Stück `GROCERY I` in Filiale 2 am 2016-05-02. Auffällig ist auch Filiale 39 `MEATS` mit 89.576 am 2016-10-07, das ist das 654-fache des Medians dieser Reihe (`?` Fehler oder echt, das müssen wir prüfen).
- Das **Erdbeben vom 2016-04-16** zeigt sich im Gesamtabsatz deutlich: Der Absatz springt von rund 0,87 Mio. am 16. auf 1,27 bis 1,35 Mio. am 17./18. April. Die Ursache (Hamsterkäufe) ist aus den Daten allein nicht belegt (`?`), sie passt aber zur Zeit des Ereignisses.
- 462.113 Zeilen haben Nachkommastellen, vermutlich Artikel nach Gewicht (z. B. kg). Das ist kein Fehler, also `float` behalten.

Entscheidung: Nichts löschen. Untersuchung und endgültige Regel stehen in 2.9.

### 2.6 `transactions` ist für die Prognose nicht nutzbar

In `test.csv` gibt es keine Transaktionen. Würden wir sie als Eingabe nutzen, hätten wir im Training eine Information, die es bei der echten Prognose nicht gibt (Datenleck). Dazu fehlen 118 Filial-Tage mit Umsatz im Transaktionsfile.
Entscheidung: nicht als Eingabe verwenden, nur für die Analyse. Dasselbe gilt für alle Größen, die wir für die Zukunft nicht kennen.

### 2.7 Struktur der Gesamtreihe

Der Gesamtabsatz (`reports/figures/01_gesamtabsatz.png`) steigt über die Jahre und hat Niveausprünge, etwa 2015 und Anfang 2014. Mindestens ein Teil davon dürfte von neuen Filialen und Familien kommen (`?`). Daher sollten wir **je Reihe** modellieren oder die Eröffnungen als Information mitgeben, statt nur die Gesamtreihe fortzuschreiben.
Saisonmuster (`02_saisonalitaet.png`): Wochenende deutlich höher als Wochenmitte, Dezember am stärksten.

### 2.8 Ergebnis der Bereinigung (`src/clean.py`)

Das Skript setzt Abschnitt 2 um und schreibt `data/clean/train_clean.parquet` und `test_clean.parquet`. Protokoll: `reports/clean_log.txt`.

| Schritt | Ergebnis |
|---|---|
| Duplikate | 0 entfernt |
| 25. Dezember (4 Tage) | 7.128 Zeilen ergänzt, `sales = NaN`, `is_closed_day = 1` |
| Strukturelle Nullen | 466.356 Zeilen entfernt (222.552 vor Filialeröffnung, 278.910 vor Einführung der Familie, mit Überschneidung) |
| Filiale zu | 18.998 Zeilen (601 Filial-Tage) markiert mit `is_store_closed = 1`, nicht gelöscht |
| Promotion | `promo_known = 0` in 23,5 % der Trainingszeilen, im Test nie |
| Ölpreis | 529 von 1.704 Kalendertagen aufgefüllt |
| Feiertage | 12 verlegte Feiertage entfernt, Rest je Filiale und Tag verdichtet (`is_holiday`, `is_workday`, `is_event`) |
| Ausreißer | 212 isolierte Spitzen markiert (`is_outlier`) und in `sales_train` maskiert, keine gelöscht (2.9) |

Vorher/nachher: 3.000.888 Zeilen werden zu 2.541.660. Der Anteil `sales = 0` sinkt von 31,3 % auf 18,6 %. Die einzigen fehlenden Werte in `sales` sind die ergänzten 25.-Dezember-Tage. `sales_train` hat zusätzlich die maskierten Zeilen (212 Spitzen, 6.015 geschlossene Tage, 18.998 Zeilen „Filiale zu“, insgesamt 25.225, ohne Überschneidung).
Es bleiben genau 1.782 Reihen (Filiale × Familie).

**Neuer Befund: Filialen waren zeitweise geschlossen.** Die 601 Filial-Tage bestehen aus
- 6 längeren Blöcken, z. B. Filiale 18 vom 2016-08-15 bis 2016-12-02 (110 Tage) und Filiale 24 vom 2014-04-14 bis 2014-07-23 (101 Tage), außerdem Filialen 25, 12, 14 und 30,
- 196 Tagen am 1. Januar und einzelnen weiteren Tagen.

Warum die Filialen zu waren, steht nicht in den Daten (`?` Umbau o. Ä.). Diese Nullen sind kein Nachfragesignal und dürfen nicht als „niemand wollte etwas“ gelernt werden. Beim Training und bei der Bewertung schließen wir `is_closed_day` und `is_store_closed` aus.

### 2.9 Ausreißer: Untersuchung und Entscheidung (`src/outliers.py`, Notebook `04_outliers`)

Auffällig große Werte sind nicht alle dasselbe. Wir haben drei Arten unterschieden:

| Art | Beispiel | Echt oder Fehler? | Als Ausreißer behandeln? |
|---|---|---|---|
| Isolierte Spitze | Filiale 39 `MEATS` am 2016-10-07: 89.576 bei Nachbartagen von 120 bis 224, andere Familien normal, keine Aktion | vermutlich Fehler oder einmalige Großbuchung (`?`) | ja |
| Saisonale Spitze | `LIQUOR,WINE,BEER` und `GROCERY II` im Dezember, sonst fast keine Verkäufe | echt, kehrt jedes Jahr wieder | nein |
| Niveausprung | Filiale 24 `PRODUCE` im Juli 2014: vorher etwa 5 pro Tag, danach 2.500 bis 6.300 | echt: Wiedereröffnung am 2014-07-23 nach Schließung seit April | nein |

**Warum die erste Regel nicht reichte.** Der Vergleich mit dem lokalen Median (29 Tage) markierte 850 Zeilen, davon 210 im Dezember und 8 im Juli 2014 für Filiale 24. Das sind Saison und Niveausprung, keine Fehler. Die erste Fassung in `clean.py` (10-Fache des 99. Perzentils) markierte nur 26 Zeilen und übersah z. B. 63.434 in Filiale 2 am 2016-04-26.

**Regel (gilt jetzt in `clean.py`).** Eine Zeile ist eine isolierte Spitze, wenn sie mehr als das 10-Fache des Medians der 4 Tage davor **und** der 4 Tage danach beträgt und mindestens 500 Einheiten hat. Ein Niveausprung oder eine Saisonwelle hält mehrere Tage an und fällt damit durch.
Ergebnis: **212 Zeilen**, das sind 0,008 % der Zeilen und 0,08 % des Gesamtabsatzes. Am häufigsten: `LIQUOR,WINE,BEER` (95), `HOME AND KITCHEN I` (30), `MEATS` (23).

**Maskieren statt kappen.** Der Rohwert bleibt in `sales`. Die neue Spalte `sales_train` ist dieselbe Zahl, aber mit `NaN` bei Spitzen, am 25. Dezember und bei geschlossenen Filialen. Ein Kappen auf das 10-Fache des 99. Perzentils hätte aus 89.576 immer noch eine absurde Zahl gemacht. Der eigentliche Schaden einer Spitze entsteht in den Lag- und Mittelwert-Merkmalen: Sie würde die nächsten Wochen verfälschen.

**Offene Punkte und Grenzen:**
- **Schwelle ist gewählt, nicht gemessen.** Je nach Faktor ändert sich die Trefferzahl stark: Faktor 5 gibt 708 Zeilen, 8 gibt 295, 10 gibt 212, 15 gibt 125, 20 gibt 92.
- **Große Reihen werden knapp verpasst.** Filiale 20 `GROCERY I` am 2016-04-21 (87.439, Faktor 8,6) und Filiale 45 am 2016-04-18 (76.090, Faktor 5,1) bleiben unmaskiert. Bei großen Reihen reicht der relative Faktor nicht.
- **Echt oder Fehler lässt sich nicht beweisen.** Filiale 35 `GROCERY I` hat eine Spitze jedes Jahr im Dezember (2014-12-08, 2015-12-14, 2016-12-12). Das spricht eher für eine wiederkehrende Großbestellung (`?`), nicht für einen Fehler. Mehrere Spitzen im April und Mai 2016 passen zeitlich zum Erdbeben, belegt ist es nicht.
- `TODO` Den Faktor nicht ausdiskutieren, sondern im Vergleich testen: Validierungsfehler ohne Maskierung, mit Faktor 10 und mit Faktor 5 (Phase G).

## 3. Zielgröße

### 3.1 Was wollen wir vorhersagen?

| Frage | Festlegung |
|---|---|
| Zielvariable | `sales`: Absatz je **Filiale × Produktfamilie × Tag** (Stück bzw. kg) |
| Modelltyp | **Zeitreihenprognose** (Szenario C aus Arbeitsauftrag 2). Promotion, Feiertage und Wochentag kommen als Zusatzinformation dazu |
| Einschränkung | Wir sagen Absatz voraus, nicht echte Nachfrage (2.3) |

Die Zielgröße bestimmt den Modelltyp und nicht die verfügbaren Daten (Kernbotschaft UE 3). Der Absatz ist eine Zahl über die Zeit. Klassifikation scheidet aus, und eine reine Regression ohne Zeitbezug würde Wochentag und Saison nicht sauber abbilden.

### 3.2 Horizont (entschieden)

**16 Tage.** Das passt zu `test.csv`, und die Promotionen sind für diesen Zeitraum bekannt (sie stehen im Test). Der Horizont ist nur die Frage, *wie weit* wir vorausschauen, er sagt nichts über die Methode oder die genutzte Historie.
Einordnung für die Fallstudie: Bei 6 Monaten (Gartenwelt, SmartRetail) wären künftige Aktionen und das Wetter unbekannt. Das Modell müsste dann überwiegend von Saison und Trend leben. Das zeigen wir am Ende als Ausblick, nicht als Hauptziel.

### 3.3 Validierung (UE 1: „mit ungesehenen Daten prüfen“)

Zeitlich trennen, nie zufällig. Wir prüfen auf **drei Fenstern** zu je 16 Tagen. Ein einziges Fenster im August sagt nichts über Weihnachten.

| Fenster | Training bis | Validierung | Zweck |
|---|---|---|---|
| W1 August 2017 | 2017-07-30 | 2017-07-31 bis 2017-08-15 | entspricht dem echten Test |
| W2 Dezember 2016 | 2016-12-08 | 2016-12-09 bis 2016-12-24 | Weihnachtsgeschäft, Härtetest |
| W3 Frühjahr 2017 | 2017-03-07 | 2017-03-08 bis 2017-03-23 | normale Phase |

Für jedes Fenster wird mit den Daten bis zum Trainingsende gelernt (Prognose-Ursprung = letzter bekannter Tag). Alles, was für die Zukunft nicht bekannt wäre, ist tabu.

### 3.4 Entscheidungen

| # | Thema | Entscheidung |
|---|---|---|
| 1 | Validierungsfenster | drei Fenster W1 bis W3 (3.3) |
| 2 | Maß | **RMSLE** als Hauptmaß, zusätzlich Fehler je Produktfamilie |
| 3 | Aus der Bewertung ausgeschlossen | `is_closed_day` und `is_store_closed`. Isolierte Spitzen mit und ohne ausweisen |
| 4 | Ausreißer im Training | isolierte Spitzen (Regel in 2.9) **maskieren**: Spalte `sales_train`, Rohwert bleibt in `sales`. Schwellenfaktor später im Vergleich prüfen |
| 5 | Zielgröße im Modell | `log1p(sales)`, Rücktransformation mit `expm1`, danach auf mindestens 0 begrenzen |
| 6 | Trainingshistorie | alle Daten mit Flag `promo_known`. Gegenprobe: nur Zeilen mit `promo_known = 1` |
| 7 | ML-Strategie | **direkt**: ein Modell für alle 16 Tage. Eingaben aus Verkäufen nur bis zum Prognose-Ursprung, dazu der Prognoseschritt (1 bis 16) und die Kalendermerkmale des Zieltags |
| 8 | Merkmale | Wochentag, Monat, Feiertage und Events, Aktion (`onpromotion`, `promo_known`), Filialattribute, Familie, jüngste Verkäufe (Mittelwerte). **Ohne** Ölpreis, der kommt später als Test dazu |
| 9 | Modelle | Baseline, statistisches Modell, globales Gradient-Boosting (LightGBM) |
| 10 | Erfolgskriterium | RMSLE mindestens **10 % unter der Baseline** im Mittel der drei Fenster und in mindestens zwei von drei einzeln |
| 11 | Test-Datei | nur eigene Validierung. Ein Kaggle-Upload ist optional und später möglich |
| 12 | Fallstudie, drei Aufbereitungsmaßnahmen | strukturelle Nullen entfernen, `promo_known` je Filiale, geschlossene Tage ausschließen |

### 3.5 Modellstufen

| Stufe | Ansatz | Genutzte Historie | Frage, die sie beantwortet |
|---|---|---|---|
| 1 | Baseline: gleicher Wochentag der Vorwoche, und Mittel der letzten 4 gleichen Wochentage | 1 bis 4 Wochen | Was ist das Minimum, das ein Modell schlagen muss? |
| 2 | Statistisch je Reihe (z. B. exponentielle Glättung oder Regression mit Wochentag und Feiertag) | ganze Reihe | Reicht Statistik, und ist sie gut erklärbar? |
| 3 | Globales Gradient-Boosting über alle 1.782 Reihen | ein Jahr und mehr | Bringt Training mit Aktionen, Feiertagen und Struktur spürbar mehr? |

Als Vergleichswert gilt die bessere der beiden Baselines. Hypothese (`?`): Stufe 3 gewinnt, vor allem bei den vielen Reihen mit häufigen Nullen. Das entscheiden die Zahlen.

### 3.6 Ergebnis Stufe 1: Baselines (`src/baselines.py`, Auswertungscode in `src/forecast_eval.py`, Notebook `05_baselines`)

Die Baselines sehen nur Daten bis zum Prognose-Ursprung und sagen die folgenden 16 Tage voraus. Bewertet wird mit RMSLE, ohne geschlossene Tage und Filialen.

| Fenster | B1 Vorwoche | B2 Mittel 4 Wochen | Benchmark (beste) | Zielwert (10 % besser) |
|---|---|---|---|---|
| W1 Aug 2017 | 0,6166 | **0,5306** | 0,5306 | 0,4775 |
| W2 Dez 2016 | 0,6469 | **0,5938** | 0,5938 | 0,5345 |
| W3 Mär 2017 | 0,5395 | **0,4523** | 0,4523 | 0,4071 |
| **Mittel** | | | **0,5256** | **0,4730** |

**Was wir daraus lernen:**
- B2 (Mittel der letzten 4 gleichen Wochentage) schlägt B1 in allen drei Fenstern und in allen 33 Familien. Mitteln glättet das Tagesrauschen, ein einzelner Vorwochenwert ist zu zufällig.
- Das Weihnachtsfenster (W2) ist am schwersten, die Frühjahrsphase (W3) am leichtesten.
- Die isolierten Spitzen verändern das Ergebnis kaum (W2: 0,6469 gegen 0,6454 ohne Spitzen). In den Fenstern kommen fast keine vor.
- Ein Modell muss im Mittel unter **0,4730** kommen und in mindestens zwei Fenstern einzeln unter dem jeweiligen Zielwert.

**Wo die Baselines schwach sind** (Fehler je Familie, W1):
- `SCHOOL AND OFFICE SUPPLIES` hat mit 1,80 den größten Fehler, mehr als das Dreifache der übrigen. Der Monatsabsatz zeigt, warum: Jedes Jahr gibt es Spitzen im August und September (2016: 17.214 und 23.556 gegen rund 2.500 in ruhigen Monaten), 2017 im August sogar 50.169. 2016 und 2017 kommt zusätzlich eine Spitze im April und Mai. Ein Durchschnitt der letzten 4 Wochen kann einen solchen Saisonanstieg nicht kommen sehen. Zwei Schuljahresanfänge im Jahr wären eine Erklärung (`?`, belegt ist nur das Muster). Hier kann ein Modell mit Monat als Merkmal am meisten gewinnen.
- `BOOKS` hat mit 0,10 den kleinsten Fehler, aber nur weil die Reihe fast immer 0 ist. Das ist keine Leistung des Modells.
- Stabile Großfamilien (`PRODUCE`, `DAIRY`, `BREAD/BAKERY`) liegen bei 0,16 bis 0,19, schwer vorherzusagen sind seltene oder saisonale Waren.

**Grenze der Baselines:** In W2 gibt es 99 Zellen ohne Prognose. Alle gehören zu Filiale 18, die am 2016-12-03 nach 110 Tagen Schließung wieder öffnete. In den vier Wochen vor dem Ursprung gibt es dort kaum verwertbare Werte. Ein Modell mit längerer Historie oder Filialmerkmalen kann das besser lösen. Diese Zellen sind nicht mit bewertet.

### 3.7 Ergebnis Stufe 2: Statistisches Modell je Reihe (`src/statistical.py`, `src/stat_models.py`, Notebook `06_statistical`)

**Modell:** Für jede der 1.782 Reihen wird einzeln eine exponentielle Glättung nach Holt-Winters angepasst: Niveau plus additives Wochenmuster, kein Trend, auf `log1p(Absatz)`, mit den letzten 365 Tagen als Historie. Reihen mit weniger als 28 verwertbaren Tagen fallen auf die Baseline zurück. Das Modell sieht weder Promotion noch Feiertage noch andere Reihen.

| Fenster | Benchmark (B2) | ETS je Reihe | Änderung | Ziel (-10 %) |
|---|---|---|---|---|
| W1 Aug 2017 | 0,5306 | 0,4845 | -8,7 % | 0,4775 |
| W2 Dez 2016 | 0,5938 | 0,5512 | -7,2 % | 0,5345 |
| W3 Mär 2017 | 0,4523 | 0,4108 | -9,2 % | 0,4071 |
| **Mittel** | **0,5256** | **0,4822** | **-8,3 %** | **0,4730** |

**Erfolgskriterium (-10 %) nicht erreicht**, aber nah dran: 0 von 3 Fenstern erreichen das Ziel, im Mittel fehlen 1,7 Prozentpunkte. Das Modell ist in allen drei Fenstern besser als die Baseline.

**Wo es gewinnt und verliert (Fenster W1):**
- Besser in **27 von 33 Familien**. Am meisten bei `HOME APPLIANCES` (-22 %), `BOOKS` (-20 %), `BABY CARE` (-16 %), `SCHOOL AND OFFICE SUPPLIES` (-15 %).
- Schlechter bei `CLEANING` (+13 %), `HOME CARE`, `GROCERY II`, `DAIRY`, `FROZEN FOODS`. Warum, wissen wir nicht (`?` mögliche Rolle von Aktionen, die das Modell nicht sieht).
- `SCHOOL AND OFFICE SUPPLIES` bleibt mit 1,54 mit Abstand die schwächste Familie. Ein Modell ohne Saison- oder Kalendermerkmale kann den Schulbeginn nicht vorhersagen.

**Mehr Historie hilft:** 90 Tage geben 0,4963, 180 Tage 0,4891, 365 Tage 0,4822 (Mittel der Fenster). Die Verbesserung ist in jedem Fenster gleichläufig, also kein Zufall in einem einzelnen. Die Historienlänge haben wir mit denselben Fenstern verglichen, mit denen wir bewerten, bei drei Varianten ist das tolerierbar.

**Rückfälle:** In W2 und W3 fallen je 33 bis 34 Reihen auf die Baseline zurück. In W2 sind das die 33 Reihen von Filiale 18 (wiedereröffnet am 2016-12-03, zu wenig verwertbare Tage), in W3 Filiale 52 (noch nicht eröffnet, dort gibt es auch keine Wahrheit zum Bewerten). Nur 3 Zellen in W2 bleiben ohne Prognose, gegenüber 99 bei den Baselines.

**Einordnung:** Ein reines Zeitreihenmodell je Reihe holt 8 % heraus. Das Erfolgskriterium verlangt 10 %. Der nächste Schritt (Stufe 3) gibt dem Modell Dinge, die dieses nicht kennt: Aktionen, Feiertage, Monat, Filial- und Familienmerkmale und das Lernen über alle Reihen hinweg.

### 3.8 Ergebnis Stufe 3: LightGBM (`src/gbm.py`, `src/gbm_model.py`, Notebook `07_gbm`)

**Modell:** Ein einziges LightGBM-Modell (500 Bäume) für alle 1.782 Reihen, direkte Strategie. Eine Trainingszeile steht für eine Reihe, einen Zieltag und einen Abstand `h` von 1 bis 16 Tagen zum Prognose-Ursprung. Zielgröße `log1p(Absatz)`, damit passt das Trainingsziel zu RMSLE.
- **Eingaben aus der Vergangenheit** (nur Tage bis zum Ursprung): Mittel der letzten 7, 28, 91 und 364 Tage, letzter bekannter Wert, Tage seit diesem Wert, Alter der Reihe, die 4 letzten Werte des gleichen Wochentags und ihr Mittel.
- **Eingaben, die auch in der Zukunft bekannt sind:** Wochentag, Tag im Monat, Monat, Feiertag, Ereignis, Arbeitstag-Ausgleich, Aktion (`onpromotion`), `promo_known`, Filiale, Familie, Filialtyp, Stadt, Region, Cluster. Ohne Ölpreis.
- **Training:** je Fenster die 730 Tage vor dem Ursprung, je (Reihe, Zieltag) zwei zufällige Abstände, rund 2,4 Mio. Zeilen. Maskierte Tage sind weder Label noch Eingabe.
- **Parameter:** Standardwerte (Lernrate 0,05, 63 Blätter), nicht an den Fenstern abgestimmt.

| Fenster | Benchmark | ETS | LightGBM | gegen Benchmark | gegen ETS | Ziel (-10 %) |
|---|---|---|---|---|---|---|
| W1 Aug 2017 | 0,5306 | 0,4845 | **0,3939** | -25,8 % | -18,7 % | 0,4775 |
| W2 Dez 2016 | 0,5938 | 0,5512 | **0,4358** | -26,6 % | -20,9 % | 0,5345 |
| W3 Mär 2017 | 0,4523 | 0,4108 | **0,3987** | -11,8 % | -2,9 % | 0,4071 |
| **Mittel** | **0,5256** | **0,4822** | **0,4095** | **-22,1 %** | **-15,1 %** | **0,4730** |

**Erfolgskriterium erreicht:** Mittel 0,4095 gegen Ziel 0,4730, und alle drei Fenster einzeln unter ihrem Ziel. W3 ist mit 11,8 % am knappsten.

**Wo LightGBM gewinnt (Fenster W1, gegenüber ETS):**
- Besser in **30 von 33 Familien**.
- `SCHOOL AND OFFICE SUPPLIES` von 1,54 auf 0,68 (-56 %). Das war die größte Schwäche der einfachen Modelle: Der Schulbeginn ist über Monat und Familie lernbar.
- Auch `CLEANING` (-30 %), `PERSONAL CARE` (-30 %), `GROCERY I` (-24 %), `DAIRY` (-18 %).
- Etwas schlechter bei `HOME APPLIANCES` (+3,5 %), `LADIESWEAR` (+5,6 %) und `BOOKS` (+7,8 %): fast immer 0 oder sehr dünn, hier hilft das gemeinsame Lernen nicht.

**Was das Modell nutzt (Anteil am Gain, Mittel der drei Fenster):**
- Gleicher Wochentag, Mittel der letzten 4 Wochen: 58 %. Das ist praktisch unsere Baseline B2 als Eingabe.
- Mittel der letzten 7 Tage: 27 %. Letzter gleicher Wochentag: 9 %.
- Alle übrigen zusammen weniger als 7 %. `aktion` 0,2 %, `feiertag` 0,0 %, `monat` 0,2 %.
- Die Wichtigkeit zeigt, wo das Modell Fehler abgebaut hat, nicht Ursache und Wirkung. Dass Aktion und Feiertag dort kaum zählen, hat sich nicht bestätigt: Der Weglasstest in 3.9 zeigt für die Aktion +7,7 %.

**Leckage-Test (`src/leakage_check.py`):** Bei so großer Verbesserung prüfen wir, dass das Modell nicht schummelt. Wir ersetzen alle 28.510 Verkäufe nach dem Ursprung von W1 durch Zufallszahlen und rechnen neu. Die Prognosen bleiben identisch (größter Unterschied 0). Damit hängen die Verkaufs-Eingaben nur von der Vergangenheit ab. Zwei Einschränkungen:
- Die Maskierung der Spitzen nutzt Nachbartage bis 4 Tage nach einem Tag. Für Tage kurz vor dem Ursprung fließt so minimal Wissen über die Zeit danach ein. Das entfernt nur Werte, bringt keine Zielinformation, ist aber streng genommen nicht leckagefrei.
- Aktion, Feiertag und Kalender des Zieltags nutzen wir bewusst. Sie sind auch in `test.csv` bekannt.

**Einordnung:** Der Gewinn kommt vor allem davon, dass ein Modell über alle Reihen hinweg lernen kann, wie die jüngste Historie in eine Prognose übersetzt wird und wie Familien saisonal unterschiedlich laufen. Wir haben die Parameter nicht abgestimmt, und auch kein einzelnes Merkmal geprüft. Alle drei Fenster sind Ausschnitte von 16 Tagen, die Aussage hängt also nicht an einem einzigen Zeitraum, aber es bleibt die Frage, wie sich das Modell in anderen Monaten verhält.

### 3.9 Gegenproben (`src/counter_tests.py`, Notebook `08_counter_tests`)

Jede Gegenprobe ändert **eine** Sache gegenüber dem Basismodell (3.8) und rechnet alle drei Fenster neu. Bewertet wird immer auf denselben Zeilen mit dem Rohwert `sales`, nur das Training ändert sich. Positive Änderung = schlechter als die Basis.

| Variante | Mittel RMSLE | Änderung | je Fenster (W1 / W2 / W3) |
|---|---|---|---|
| **Basis** | 0,4095 | - | - |
| Basis, andere Zufallszahlen | 0,4119 | +0,6 % | +0,4 % / +0,8 % / +0,6 % |
| ohne Aktion | 0,4412 | +7,7 % | +16,3 % / +0,8 % / +6,9 % |
| ohne Feiertage und Ereignisse | 0,4102 | +0,2 % | +0,9 % / -0,5 % / +0,1 % |
| ohne Monat und Tag im Monat | 0,4357 | +6,4 % | +1,9 % / +16,4 % / -0,2 % |
| ohne Filial- und Familienmerkmale | 0,4495 | +9,8 % | +5,2 % / +17,8 % / +5,4 % |
| nur Verkaufshistorie und Wochentag | 0,4853 | +18,5 % | +24,1 % / +27,2 % / +3,5 % |
| mit Ölpreis | 0,4130 | +0,9 % | +0,7 % / +0,9 % / +1,0 % |
| Training nur mit promo_known = 1 | 0,4098 | +0,1 % | +0,2 % / +0,0 % / +0,0 % |
| keine Maskierung der Spitzen | 0,4099 | +0,1 % | +0,7 % / -0,6 % / +0,2 % |
| Maskierung Faktor 5 | 0,4108 | +0,3 % | +0,4 % / +0,3 % / +0,3 % |

**Messlatte Rauschen:** Mit anderen Zufallszahlen (Auswahl der Abstände und Boosting) ändert sich das Mittel um 0,6 %, in einzelnen Fenstern bis 0,8 %. Änderungen unter etwa 1 % sind deshalb nicht vom Zufall zu unterscheiden.

**Was zählt (Weglassen verschlechtert deutlich):**
- **Aktion** (`aktion`, `aktion_bekannt`): ohne sie +7,7 %, in W1 +16,3 %, in W3 +6,9 %, in W2 nur im Rauschen. In W1 kommt fast alles von `SCHOOL AND OFFICE SUPPLIES` (+110 %). Vermutung (`?`): Die Zahl der Artikel in Aktion steigt zum Schulbeginn und dient als Vorab-Signal der Saison. Das wäre ein Hinweis auf die Saison, nicht auf eine Wirkung der Aktion selbst.
- **Filial- und Familienmerkmale:** ohne sie +9,8 %, in allen drei Fenstern schlechter (+5 bis +18 %). In W1 verschlechtern sich 27 von 33 Familien um mehr als 2 %, `BOOKS` um 36 %.
- **Monat und Tag im Monat:** ohne sie +6,4 %, aber fast nur im Dezemberfenster W2 (+16,4 %). W1 +1,9 %, W3 −0,2 %. Der Monat trägt vor allem das Weihnachtsgeschäft, in W1 einzelne Familien wie `PERSONAL CARE` (+34 %) und `GROCERY I` (+30 %).

**Was nichts bringt (Änderung im Rauschen oder schlechter):**
- **Feiertage und Ereignisse:** +0,2 %, kein messbarer Nutzen. Einschränkung (`?`): In 16 Tagen liegen nur wenige Feiertage, das erklärt den fehlenden Effekt vermutlich. Widerlegt ist der Nutzen damit nicht, nur in diesen Fenstern nicht gezeigt.
- **Ölpreis (am Ursprung):** +0,9 %, in allen Fenstern leicht schlechter. Bleibt draußen.
- **Nur mit `promo_known = 1` trainieren:** +0,1 %. In W2 und W3 sind die Ergebnisse auf vier Stellen identisch mit der Basis, der Filter hat dort also nichts entfernt: Die 730 Trainingstage beginnen nach dem Start der Aktionserfassung. Das Problem „Aktionsdaten fehlen vor 2014“ ist echt (23,5 % der Zeilen), spielt bei zwei Jahren Training aber keine Rolle. Es würde erst wirken, wenn wir die ganze Historie nutzen. `TODO` optional testen: 1.500 Tage Training mit und ohne den Filter.
- **Maskierung der Spitzen:** ohne Maskierung +0,1 %, mit Faktor 5 +0,3 %, beides im Rauschen. Die Regel aus 2.9 ist begründet und schadet nicht, bringt in diesen Fenstern aber keinen messbaren Gewinn. Wir stimmen den Faktor nicht weiter ab.

**Die wichtigste Erkenntnis:** „Nur Verkaufshistorie und Wochentag“ liegt bei 0,4853 und damit gleichauf mit dem statistischen Modell je Reihe (0,4822). Der Algorithmus allein bringt also nichts: Der Gewinn von LightGBM gegenüber ETS kommt aus den **Kontextmerkmalen** (Filiale und Familie, Monat, Aktion), die ein Modell über alle Reihen hinweg nutzen kann. Das passt zum Gedanken aus UE 1: Daten und Modell gehören zusammen.

**Eine Korrektur zu 3.8:** Die Merkmalswichtigkeit gab `aktion` nur 0,2 %, der Weglasstest zeigt +7,7 %. Die Wichtigkeit (Gain) unterschätzt Merkmale, die nur in wenigen Reihen sehr viel ausmachen. Für die Frage „bringt das Merkmal etwas?“ ist der Weglasstest die verlässlichere Antwort.

**Grenzen:** Drei Fenster mit je 16 Tagen. Die Wirkungen unterscheiden sich stark zwischen den Fenstern (Monat: nur W2, Aktion: nur W1 und W3), die Aussagen gelten also für diese Zeiträume. Wir ändern immer nur eine Sache, Wechselwirkungen testen wir nicht. Alle Tests nutzen dieselben Fenster wie die Bewertung, wir haben aber nichts abgestimmt, sondern nur weggelassen.

### 3.10 Quantil-Prognose für Nachbestellungen (`src/quantile.py`, Notebook `09_quantile`)

**Warum:** Die Prognose aus 3.8 ist ein typischer Wert. Der echte Absatz liegt an etwa jedem zweiten Tag darüber, wer genau diese Menge bestellt, hat an jedem zweiten Tag zu wenig. Für Nachbestellungen braucht man eine Menge, die mit vorgegebener Wahrscheinlichkeit (alpha) reicht.

**Wie:** Gleiche Merkmale, gleiche Trainingsfenster wie 3.8, nur die Verlustfunktion ändert sich (`objective="quantile"`, `alpha`). Je alpha ein Modell auf `log1p(sales)`; `expm1` des Log-Quantils ist das Quantil des Absatzes. Danach werden die sieben Quantile je Zelle sortiert, damit sie sich nicht kreuzen. Geprüft in denselben drei Fenstern.

**Abdeckung je Tag** (Anteil der Zellen mit echtem Absatz <= Prognose; Soll = alpha), Mittel der drei Fenster:

| alpha | Abdeckung je Tag | Bestand gegenüber Median |
|---|---|---|
| 0,50 | 56,3 % | - |
| 0,75 | 77,3 % | +12,2 % |
| 0,90 | 90,5 % | +25,0 % |

- **Das 90-%-Quantil trifft:** 91,9 % / 90,2 % / 89,2 % in W1 / W2 / W3. An etwa einem von zehn Tagen reicht der Bestand nicht.
- **Der Median zeigt 56 %, nicht 50 %:** Tage mit Absatz 0 zählen als abgedeckt, und viele Reihen haben Nullen. Das ist kein Fehler.
- **Der Preis:** Das 90-%-Quantil bedeutet im Mittel 25 % mehr Ware als der Median. Wie viel, hängt von der Reihe ab (W2 Dezember: +34 %, W1/W3: +20 %).

**Schwachstellen des 90-%-Quantils (W1, Abdeckung je Familie):**
- **Zu knapp:** `SCHOOL AND OFFICE SUPPLIES` 78,8 %, `BEAUTY` 86,0 %, `MAGAZINES` 86,7 %, `LINGERIE` 87,5 %, `HOME AND KITCHEN II` 88,8 %.
- **Zu großzügig:** `BOOKS` 99,2 %, `HOME CARE` 96,5 %, `DAIRY` 96,3 %, `PRODUCE` 96,1 %, `LADIESWEAR` 95,9 %.
- Ein globales Modell mit nur drei Prüffenstern kann familienweise nicht auf 90 % eingestellt werden. Die Ursache haben wir nicht weiter untersucht (`?`).

**Summe über 16 Tage:** Wer für 16 Tage auf einmal bestellt, darf nicht einfach die 16 Tagesquantile addieren. Gute und schlechte Tage gleichen sich in der Summe teilweise aus, die Summe der 90-%-Werte liegt zu hoch. Gemessen wird, wie oft die Summe der Tagesquantile den echten 16-Tage-Absatz je Reihe abdeckt (nur Reihen ohne Schließtage im Fenster):

| alpha | W1 | W2 | W3 | Mittel | Bestand gegenüber Median |
|---|---|---|---|---|---|
| 0,50 | 53,2 % | 41,6 % | 34,7 % | 43,2 % | - |
| 0,70 | 85,1 % | 74,0 % | 74,9 % | 78,0 % | +8,7 % |
| 0,75 | 90,6 % | 81,3 % | 85,3 % | 85,7 % | +12,2 % |
| **0,80** | **94,9 %** | **87,5 %** | **90,9 %** | **91,1 %** | **+15,5 %** |
| 0,85 | 97,3 % | 91,4 % | 94,5 % | 94,4 % | +19,5 % |
| 0,90 | 98,5 % | 95,0 % | 97,1 % | 96,9 % | +25,0 % |

- **Die Summe der Mediane reicht nur in 43 % der Fälle.** Das ist schlechter als jeder einzelne Tag.
- **Die Summe der 90-%-Werte deckt 96,9 % ab** und kostet 25 % Mehrbestand. Das 80-%-Quantil erreicht im Mittel 91,1 % bei 15,5 % Mehrbestand, also rund 10 Prozentpunkte weniger Bestand für dieselbe Sicherheit.
- **Einschränkung:** alpha = 0,8 wurde auf denselben drei Fenstern gewählt, an denen es geprüft wird. Die Fenster streuen von 87,5 % bis 94,9 %. Als Faustregel brauchbar, als verlässlicher Wert nicht. Ein Test auf weiteren Zeiträumen steht aus. Außerdem gilt das nur für diese Aufsummierung ohne Annahmen über Zusammenhänge der Tage.

**Prognose 16.–31.08.2017:** `reports/forecast_next16.csv` (q50 bis q90 je Filiale, Familie und Tag, plus Kennzeichen für Schließtage). Es gibt keine echten Werte zum Vergleich, die Datei ist eine Demonstration. Vertrauen kommt aus den Abdeckungen in den drei Fenstern.

**Grenzen:** Das Modell prognostiziert weiter Absatz, nicht Nachfrage (ausverkaufte Tage drücken die Werte). Bestand, Lieferzeit, Packungsgrößen und Kosten fehlen, die Quantile sind also eine Eingabe für die Bestellformel, keine Bestellmenge. Ein erster Lauf mit nur drei Quantilen (0,5 / 0,75 / 0,9) wich um bis zu 0,5 Prozentpunkte in der Abdeckung ab (z. B. Median W1 61,4 % statt 61,0 %), weil das Sortieren der Quantile je Zelle mit mehr Modellen häufiger eingreift.

## 4. Plan und Stand

| Phase | Inhalt | Status |
|---|---|---|
| A. Daten | EDA, Bereinigung (`clean.py`), Promotion-Flag | erledigt |
| B. Ausreißer | Fälle untersucht, Regel „isolierte Spitze“, Maskierung in `clean.py` | erledigt |
| C. Validierung | Fenster W1 bis W3, RMSLE, Auswertung je Familie (`src/forecast_eval.py`) | erledigt |
| D. Stufe 1 | Baselines, Benchmark RMSLE 0,5256 | erledigt (3.6) |
| E. Stufe 2 | statistisches Modell, RMSLE 0,4822 (-8,3 %), Ziel knapp verfehlt | erledigt (3.7) |
| F. Stufe 3 | LightGBM, RMSLE 0,4095 (-22,1 %), Erfolgskriterium erreicht, Leckage-Test bestanden | erledigt (3.8) |
| G. Vergleich | Gegenproben: Merkmalsgruppen, Ölpreis, `promo_known`, Maskierung, Rauschtest | erledigt (3.9) |
| H. Fallstudie | Probleme, drei Maßnahmen, Modellansatz, Lifecycle aufschreiben, Ausblick 6 Monate | offen |
| I. Nachbestellung | Quantil-Prognose (Median, 75 %, 90 %), Abdeckung, Summe über 16 Tage | erledigt (3.10) |

Detail-Checkliste:

- [x] Promotion: Flag `promo_known` je Filiale (2.4)
- [x] `src/clean.py`: Bereinigung nach Abschnitt 2 als Skript, Ausgabe in `data/clean/`
- [x] Horizont, Validierungsfenster, Maß und Erfolgskriterium festgelegt (3.2 bis 3.4)
- [x] Ausreißer untersucht, Maskierung umgesetzt (2.9)
- [x] `src/forecast_eval.py`: Fenster, RMSLE, Ausschlüsse
- [x] Baselines rechnen und Benchmark festhalten (RMSLE 0,5256, Ziel 0,4730)
- [x] Statistisches Modell (3.7)
- [x] LightGBM (3.8)
- [x] Gegenproben (3.9)
- [x] Quantil-Prognose und Kalibrierung für die 16-Tage-Summe (3.10)
- [ ] optional: alpha = 0,8 für die Summe auf weiteren Zeiträumen prüfen
- [ ] Ergebnisse vergleichen und in die Fallstudie übertragen

## 5. Projektstruktur

```
02_Favorita_Mini-Projekt/
├── data/raw/        Kaggle-Rohdaten (nicht versioniert)
├── data/clean/      bereinigte Daten (parquet, nicht versioniert)
├── src/             eda_checks.py, eda_plots.py, clean.py, explore_promo_closures.py, outliers.py, forecast_eval.py, baselines.py, stat_models.py, statistical.py, gbm_model.py, gbm.py, leakage_check.py, masking.py, counter_tests.py, quantile.py
├── reports/         dieser Bericht, Rohausgaben, figures/
└── pyproject.toml   Umgebung (uv)
```

Ausführen: `uv run python src/eda_checks.py`
