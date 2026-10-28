# Tag 7 · Transferprojekt Bergmann Baumärkte: Analytics-Startplan für das erste Jahr

**Rolle (Folie 4):** Wir sind **CAO / CDO** bei Bergmann. Bergmann steht am **Beginn seiner Analytics-Reise**, die Geschäftsführung erwartet einen **konkreten Startplan**.

**Auftrag:** Eine **Strategie zur Auswahl und Umsetzung** der Use Cases entwickeln, die **strategischen Wert mit realistischer Umsetzbarkeit** verbindet. Sechs Ergebnisse (Folie 5 und 6):

1. Auswahl und Begründung
2. Bewertungsmatrix
3. Priorisierung
4. Umsetzungsstrategie
5. Risikoanalyse
6. Kernentscheidung

> **Annahmen und Herkunft:** Gegeben sind nur die Zahlen der Folien (Abschnitt 1). Alles, was wir **bewerten, gewichten oder verteilen** (Punkte, Gewichte, Budgetaufteilung, Rohertragsmarge, Quartalsplan), sind **Annahmen** und als solche gekennzeichnet. Sie lassen sich austauschen. Zwei Folienangaben prüfen wir kritisch (Abschnitt 2.3).

---

## Das Ergebnis in Kürze

| | Entscheidung |
| --- | --- |
| **Auswahl** | **Garten-Absatzprognose** (Abschriften), **Handwerker-Abwanderung** (Kernproblem 2), dazu als leichter dritter Schritt **Frequenzprognose für den Personaleinsatz** in den 12 Märkten mit Zähler |
| **Nicht im ersten Jahr** | **App-Personalisierung** und **Preisoptimierung Onlineshop** (hoher Aufwand, schwache Daten, unsicherer Nutzen) |
| **Reihenfolge** | **1. Garten**, **2. Handwerker** (Datenaufbau von Anfang an), **3. Personal** (nur wenn Kapazität da ist) |
| **Kernentscheidung** | **Quick Win zuerst.** Garten liefert nach 6 Monaten messbaren Erfolg. Das **Datenfundament** für die Handwerker (Kartenquote) wird **von Tag 1 parallel** gelegt, weil es die Engstelle ist. |
| **Budget** | 500.000 €: Garten 180 T€, Handwerker 140 T€, Personal 40 T€, gemeinsame Plattform 50 T€, Schulung 40 T€, Reserve 50 T€ |
| **Rechtfertigung Garten** | Schon **2 % weniger Abschriften** (180 T€ von 9 Mio €) zahlen den Garten-Anteil zurück |

---

## 1. Ausgangslage (Folie 2 und 3)

| Merkmal | Angaben |
| --- | --- |
| **Unternehmen** | Familiengeführte Bau- und Gartenmarktkette, **38 Märkte** in Bayern und Thüringen, **2.900 Mitarbeitende**, **640 Mio. €** Umsatz |
| **Kanäle** | Onlineshop mit Click & Collect seit 2022 (**7 % des Umsatzes**, das sind etwa 45 Mio. €). Kundenkarte mit **410.000 aktiven Mitgliedern** |
| **Probleme** | Gartensortiment **stark wetterabhängig**, **Abschriften 9 Mio. €/Jahr**. **Handwerker wandern zu Fachhändlern ab** |
| **Analytics heute** | Berichte aus der Warenwirtschaft, **keine Prognosen**. **BI-Team mit 3 Personen** |
| **Vorgabe** | **Höchstens 3 Use Cases** im ersten Jahr, **Budget 500.000 €** |

**Use-Case-Kandidaten (Folie 3):**

| # | Use Case | Nutzen pro Jahr | Datenlage | Aufwand |
| :-: | --- | --- | --- | --- |
| 1 | **Wetterbasierte Absatzprognose Garten** | 2 bis 3 Mio. € weniger Abschriften | Kassendaten 10 Jahre + Wetterdienst | mittel |
| 2 | **Abwanderung von Handwerkern erkennen** | ca. 1,5 Mio. € gesicherter Umsatz | nur 55 % der Handwerker mit Karte | mittel |
| 3 | **Personaleinsatz nach Kundenfrequenz** | 0,8 Mio. € Personalkosten | Frequenzzähler nur in 12 Märkten | gering |
| 4 | **Personalisierte Angebote in der App** | unsicher, Wettbewerber melden +4 % Umsatz | App-Daten erst seit 1 Jahr | hoch |
| 5 | **Preisoptimierung im Onlineshop** | 0,5 bis 1 Mio. € Marge | Wettbewerbspreise müssten gekauft werden | hoch |

**Zwei Kernprobleme** (Folie 5): **Abschriften** und **Abwanderung der Handwerker**. Daran messen wir die **Relevanz** jedes Kandidaten.

---

## 2. Ergebnis 1: Auswahl und Begründung

### 2.1 Die Auswahl

| Use Case | Verbindung zum Kernproblem | Rolle im Plan |
| --- | --- | --- |
| **1. Wetterbasierte Absatzprognose Garten** | **direkt:** weniger Fehlmengen bei Wetterumschwung, **weniger Abschriften** (9 Mio. €) | **Quick Win**, Start im Q1 |
| **2. Abwanderung von Handwerkern** | **direkt:** frühes Erkennen und Halten der Handwerker (**Kernproblem 2**) | **Strategisches Thema**, Datenaufbau ab Q1, Pilot im Q3 |
| **3. Personaleinsatz nach Kundenfrequenz** | **indirekt:** gleiche Methode und gleiche Wetterdaten wie Use Case 1 (Zeitreihe mit Wetter), senkt Kosten | **leichter dritter Schritt**, nur bei freier Kapazität, Start im Q3 |

**Warum diese drei passen zusammen:**

- **Gemeinsame Technik:** Garten und Personal sind beide **Zeitreihenprognosen mit Wetter**. Wetterdaten, Kalender und Erfahrung des Teams werden doppelt genutzt.
- **Gemeinsame Datenbasis:** Der Ausbau der **Kundenkarte** hilft den Handwerkern jetzt und später auch App und Angeboten.
- **Passend zur Größe:** 3 Personen im BI-Team schaffen nicht drei große Projekte gleichzeitig. Deshalb ist Nummer 3 bewusst **leicht und optional**.

### 2.2 Warum nicht App und Preisoptimierung?

| Use Case | Gründe gegen den Start im ersten Jahr |
| --- | --- |
| **Personalisierte Angebote in der App** | **Nutzen unsicher:** die "+4 % Umsatz" sind **Angaben von Wettbewerbern**, kein Beleg für Bergmann. **App-Daten erst seit 1 Jahr:** das ist **ein einziger Saisonzyklus**, Muster und Saison sind nicht lernbar. **Aufwand hoch.** |
| **Preisoptimierung Onlineshop** | Online sind nur **7 % des Umsatzes** (etwa 45 Mio. €). **Wettbewerbspreise müssten gekauft werden**, das kostet Budget bevor ein Nutzen da ist. **Aufwand hoch.** Der Nutzen von 0,5 bis 1 Mio. € wären 1 bis 2 % vom Onlineumsatz, nicht unrealistisch, aber teuer zu erreichen. |

Beide kommen **später** wieder auf die Liste (Entscheidung im vierten Quartal), sobald Daten und Team bereit sind.

### 2.3 Zwei Angaben, die wir kritisch lesen

Die Folie nennt **Nutzen pro Jahr**, die man nicht ungeprüft übernehmen sollte:

| Angabe | Problem | Konsequenz |
| --- | --- | --- |
| **Handwerker: 1,5 Mio. € "gesicherter Umsatz"** | Erstens **Umsatz, nicht Gewinn** (Garten: weniger Abschriften = Kosten, wirkt voll aufs Ergebnis). Zweitens haben **nur 55 % der Handwerker eine Karte**, das Modell sieht also nur etwas mehr als die Hälfte. | Bei 55 % Abdeckung: 0,55 · 1,5 = **0,825 Mio. € Umsatz**. Bei **30 % Rohertragsmarge** (Annahme): **0,25 Mio. €** Ergebniswirkung. |
| **Personal: 0,8 Mio. € Personalkosten** | Frequenzzähler gibt es nur in **12 von 38 Märkten** (32 %). Gilt der Wert für alle Märkte, erreichen wir nur einen Teil. | Bei gleich großen Märkten (Annahme): 0,8 · 12 / 38 ≈ **0,25 Mio. €** |

**Garten dagegen** (2 bis 3 Mio. €) steht auf **10 Jahren Kassendaten**, das Ziel entspricht **22 bis 33 %** der 9 Mio. € Abschriften. Das ist ehrgeizig. Wir planen deshalb mit der **unteren Grenze** (2 Mio. €), im Risikoplan mit der Hälfte.

---

## 3. Ergebnis 2: Bewertungsmatrix

### 3.1 Kriterien, Skala und Gewichte

Wir bewerten alle fünf Kandidaten nach den **vier Kriterien der Folie**, **Skala 1 bis 5**, **5 = am besten** (auch beim Aufwand: 5 = geringer Aufwand).

| Kriterium | Gewicht | 1 bedeutet | 5 bedeutet |
| --- | ---: | --- | --- |
| **Relevanz** (für die Kernprobleme Abschriften und Handwerker) | **25 %** | unabhängig von beiden Kernproblemen | wirkt **direkt** auf ein Kernproblem |
| **Wirkung** (Ergebnis pro Jahr, nach Abdeckung angepasst, Abschnitt 2.3) | **35 %** | unter 0,2 Mio. € oder nicht belastbar | ab 2,0 Mio. € (Stufen: 2 = 0,2 bis 0,5; 3 = 0,5 bis 1,0; 4 = 1,0 bis 2,0) |
| **Datenverfügbarkeit** | **25 %** | kaum Daten, Lücken | lange Historie, vollständig |
| **Aufwand** (umgekehrt: hoch = 1, mittel = 3, gering = 5) | **15 %** | Aufwand hoch | Aufwand gering |

**Warum diese Gewichte?**

- **Wirkung 35 %** ist das größte Gewicht: Ohne messbaren Nutzen rechtfertigt das Budget nichts.
- **Relevanz 25 %**: Der Plan soll die **Kernprobleme** treffen, nicht irgendeinen Hebel.
- **Datenverfügbarkeit 25 %**: Fehlen Daten, gibt es **kein Modell**. Das ist ein **Ausschlusskriterium**, deshalb ebenso hoch wie die Relevanz.
- **Aufwand 15 %**: Der Aufwand ist teilweise durch Budget und Vorgabe (3 Use Cases) bereits begrenzt und wiegt deshalb am wenigsten.
- **Strategie (Relevanz + Wirkung) 60 %, Umsetzbarkeit (Daten + Aufwand) 40 %.** Das entspricht dem Auftrag, **strategischen Wert mit realistischer Umsetzbarkeit zu verbinden**, mit leichtem Übergewicht beim Wert.

```
Score = 0,25 · Relevanz + 0,35 · Wirkung + 0,25 · Daten + 0,15 · Aufwand
```

### 3.2 Bewertung

| Use Case | Relevanz | Wirkung | Daten | Aufwand | **Gesamt** |
| --- | :-: | :-: | :-: | :-: | :-: |
| **1. Garten-Absatzprognose** | 5 | 5 | 4 | 3 | **4,45** |
| **2. Handwerker-Abwanderung** | 5 | 2 | 2 | 3 | **2,90** |
| **3. Personaleinsatz** | 2 | 2 | 2 | 5 | **2,45** |
| **4. App-Angebote** | 3 | 1 | 1 | 1 | **1,50** |
| **5. Preisoptimierung Online** | 2 | 3 | 2 | 1 | **2,20** |

Rechenweg (Garten und Handwerker, die anderen analog):

```
Garten     = 0,25 · 5 + 0,35 · 5 + 0,25 · 4 + 0,15 · 3 = 1,25 + 1,75 + 1,00 + 0,45 = 4,45
Handwerker = 0,25 · 5 + 0,35 · 2 + 0,25 · 2 + 0,15 · 3 = 1,25 + 0,70 + 0,50 + 0,45 = 2,90
```

**Begründung der Punkte:**

| Use Case | Begründung |
| --- | --- |
| **Garten** | **Relevanz 5:** trifft Abschriften direkt. **Wirkung 5:** 2 bis 3 Mio. €. **Daten 4:** 10 Jahre Kassendaten sind sehr gut. Abzug, weil für das Training **archivierte Wettervorhersagen** nötig sind, nicht nur das tatsächliche Wetter. **Aufwand 3:** mittel (Folie). |
| **Handwerker** | **Relevanz 5:** Kernproblem 2. **Wirkung 2:** nach Abdeckung und Marge nur etwa 0,25 Mio. € (Abschnitt 2.3). **Daten 2:** nur 55 % mit Karte. **Aufwand 3:** mittel (Folie). |
| **Personal** | **Relevanz 2:** kein Kernproblem. **Wirkung 2:** etwa 0,25 Mio. € bei 12 von 38 Märkten. **Daten 2:** Zähler nur in 12 Märkten. **Aufwand 5:** gering (Folie). |
| **App** | **Relevanz 3:** stützt Bindung allgemein, nicht gezielt die Handwerker. **Wirkung 1:** nicht belastbar, Wettbewerberzahl nicht übertragbar. **Daten 1:** nur ein Jahr. **Aufwand 1:** hoch (Folie). |
| **Preis Online** | **Relevanz 2:** weder Abschriften noch Handwerker, Online nur 7 %. **Wirkung 3:** 0,5 bis 1 Mio. €. **Daten 2:** Wettbewerbspreise müssen gekauft werden. **Aufwand 1:** hoch (Folie). |

### 3.3 Robustheit der Gewichtung

Wir prüfen, ob eine **andere Gewichtung** die Reihenfolge ändert:

| Gewichtung (Relevanz / Wirkung / Daten / Aufwand) | Garten | Handwerker | Personal | Preis | App |
| --- | :-: | :-: | :-: | :-: | :-: |
| **Basis** (25 / 35 / 25 / 15) | **4,45** | 2,90 | 2,45 | 2,20 | 1,50 |
| **Gleich** (je 25 %) | **4,25** | 3,00 | 2,75 | 2,00 | 1,50 |
| **Strategie** (40 / 40 / 10 / 10) | **4,70** | 3,30 | 2,30 | 2,30 | 1,80 |
| **Umsetzung** (10 / 20 / 40 / 30) | **4,00** | 2,60 | **2,90** | 1,90 | 1,20 |

- **Garten ist in jeder Variante Platz 1**, mit deutlichem Abstand.
- **App ist in jeder Variante Letzter.** **Preis** liegt immer hinter den Handwerkern (bei Strategie gleichauf mit Personal).
- **Platz 2 und 3** hängen von der Gewichtung ab: Nur bei der Gewichtung **"Umsetzung"** überholt **Personal** die Handwerker. Wer vor allem auf Machbarkeit schaut, zieht Personal vor. Wer die Kernprobleme betont, wählt Handwerker. Das ist die eigentliche Entscheidung in Ergebnis 6.

---

## 4. Ergebnis 3: Priorisierung

### 4.1 Reihenfolge

| Platz | Use Case | Start | Begründung |
| --- | --- | --- | --- |
| **1** | **Garten-Absatzprognose** | **Q1** | Höchster Score, **messbar nach 6 Monaten**, schafft Vertrauen und Budget |
| **2** | **Handwerker-Abwanderung** | **Datenaufbau Q1, Pilot Q3** | Kernproblem 2, aber **Datenbasis** (Kartenquote) braucht Zeit, deshalb früh starten |
| **3** | **Personaleinsatz** | **Q3**, nur bei Kapazität | Gleiche Methode wie Garten, geringer Aufwand, aber kleiner Nutzen |
| **später** | App, Preisoptimierung | Neubewertung Q4 | Daten und Aufwand passen noch nicht |

### 4.2 Einordnung (Impact × Umsetzbarkeit)

|  | Gut umsetzbar | Schwer umsetzbar |
| --- | --- | --- |
| **Hoher Impact** | **Quick Win: Garten** | **Vorbereiten: Handwerker** (Daten aufbauen, dann Pilot) |
| **Geringer Impact** | **Nebenbei: Personal** (leicht, bei Kapazität) | **Meiden (vorerst): App, Preisoptimierung** |

### 4.3 Warum Garten, damit die Geschäftsführung nach 6 Monaten einen Erfolg sieht?

- **Beste Daten:** 10 Jahre Kassendaten, fertig vorhanden.
- **Passender Zeitpunkt:** Bei Start im **Q1** (Annahme) liegt der **Pilot im Q2** zum Beginn der **Gartensaison**. Nach etwa 6 Monaten (Juni) gibt es **Vergleichszahlen**: Abschriften in Pilotmärkten gegen Kontrollmärkte.
- **Messbar in Euro:** Abschriften sind eine Zahl, die die Geschäftsführung kennt.
- **Hohe Rendite:** Schon **2 % weniger Abschriften** zahlen den Garten-Anteil zurück (Abschnitt 6).

> **Wichtig:** Das gilt nur, wenn das Projekt **vor der Saison** startet. Beginnt es im Herbst, ist ein Erfolg erst nach der **nächsten Saison** sichtbar. Bis dahin lässt sich nur im Rückblick (Backtest) zeigen, dass das Modell funktioniert. Das gehört in die Planung.

---

## 5. Ergebnis 4: Umsetzungsstrategie

### 5.1 Wer arbeitet mit?

| Beteiligte | Rolle |
| --- | --- |
| **BI-Team (3 Personen)** | Kern: Dateningenieur (Daten und Pipeline), Analyst/Modellierer (Prognose), BI-Entwickler (Berichte, Pilot-Messung). Ein Teammitglied übernimmt die **Produktverantwortung** je Use Case |
| **Einkauf / Category Management Garten** | **Fachlicher Eigentümer** von Use Case 1: nutzt Bestellempfehlungen, bewertet sie |
| **Marktleitungen (Pilotmärkte)** | Setzen Empfehlungen um (Nachbestellung, Umlagerung, Aktionen), geben Rückmeldung |
| **Marketing / Kundenkarte (CRM)** | Eigentümer von Use Case 2: Kartenaktion, Halteaktion, Kontrollgruppe |
| **Personalplanung / Betriebsrat** | Use Case 3: Einbindung **früh**, weil Personaleinsatz und Zähler mitbestimmungsrelevant sein können |
| **Datenschutz** | Kundenkarte, Profiling, Frequenzzähler |
| **Externe Partner (befristet)** | Data Scientist für Garten-Modell (Beratung), **Wetterdatenanbieter** (inklusive archivierter Vorhersagen), ggf. Agentur für die Kartenaktion |
| **Geschäftsführung** | Sponsor, entscheidet an den **Gates** (Ende Q2 und Q4) |

### 5.2 Quartalsplan

Annahme: **Start Anfang Q1**, Gartensaison ab April.

| Quartal | Garten | Handwerker | Personal | Querschnitt |
| --- | --- | --- | --- | --- |
| **Q1** | Daten aufbereiten, **Wetterdaten** (archivierte Vorhersagen) beschaffen, **Baseline** (Vorjahr) und erstes Modell | **Handwerker definieren**, Churn-Definition festlegen, **Kartenaktion starten** (Ziel: Kartenquote erhöhen), Datenlage prüfen | | Datenplattform, **Schulung**, Kommunikation an Marktleitungen |
| **Q2** | **Pilot** in 8 bis 10 Märkten und ausgewählten Warengruppen, **Kontrollmärkte**. Wöchentliche Auswertung | Kartenaktion läuft, **regelbasierte Sofortmaßnahme** (z. B. kein Kauf seit 60 Tagen: Kontakt) | | **Gate 1 (Ende Q2):** Garten-Erfolg zeigen, über Rollout entscheiden |
| **Q3** | **Rollout** auf alle 38 Märkte | **Pilot** Halteaktion mit Modell v1 und **Kontrollgruppe** | Start Frequenzprognose in **12 Märkten**, wenn Kapazität da ist | Monitoring |
| **Q4** | Betrieb, **Auswertung der Saison** | Auswertung Pilot, Entscheidung über Rollout | Pilotauswertung | **Gate 2 (Q4):** Jahresbilanz, Neubewertung **App und Preisoptimierung**, Plan Jahr 2 |

### 5.3 Verteilung der 500.000 € (Annahme)

| Posten | Q1 | Q2 | Q3 | Q4 | **Summe** |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Garten** (Wetterdaten, externer Data Scientist, Pilot) | 70 | 70 | 30 | 10 | **180** |
| **Handwerker** (Kartenaktion, Pilot, Aktionskosten, Kontrollgruppe) | 30 | 30 | 50 | 30 | **140** |
| **Personal** (Frequenzprognose 12 Märkte) | 0 | 0 | 10 | 30 | **40** |
| **Gemeinsame Plattform** (Datenpipeline, Betrieb) | 30 | 10 | 5 | 5 | **50** |
| **Schulung und Change** (Marktleitungen, Einkauf) | 10 | 10 | 10 | 10 | **40** |
| **Zwischensumme** | **140** | **120** | **105** | **85** | **450** |
| **Reserve** (zurückgehalten) | | | | | **50** |
| **Gesamt** | | | | | **500** |

(Beträge in T€. Die **Reserve von 10 %** wird erst nach Gate 1 freigegeben.)

**Annahme zum Budget:** Die **Personalkosten des BI-Teams** (3 Personen) sind darin **nicht** enthalten, die 500 T€ decken Externe, Daten, Aktionen und Schulung. Wären die Gehälter im Budget, bliebe deutlich weniger übrig. Das ist **bei der Geschäftsführung zu klären**.

**Warum diese Verteilung?** Garten bekommt am meisten (größter Nutzen, externe Hilfe nötig). Die **Handwerker** bekommen **früh Geld für die Datenbasis**, damit das Pilot im Q3 überhaupt trägt.

### 5.4 Messgrößen

| Use Case | Erfolgsmaß (Wirkung) | Modellqualität |
| --- | --- | --- |
| **Garten** | **Abschriften in €** und Regalverfügbarkeit, Pilot gegen Kontrollmärkte | **WAPE** und MAE der Absatzprognose (Tag 7), Fehler getrennt für zu viel und zu wenig |
| **Handwerker** | **Aktivquote** und Umsatz der Handwerker, Aktionsgruppe gegen Kontrollgruppe, **Kartenquote** | Recall und Precision, Wert in Euro (Tag 6), Schwelle `p > K / (q · W)` |
| **Personal** | Personalstunden je Besucher, Über- und Unterdeckung | MAE der Frequenzprognose |

### 5.5 Kurzsteckbrief je Use Case

| Baustein | **Garten** | **Handwerker** |
| --- | --- | --- |
| **Zielgröße** | Absatz in Stück je Warengruppe, Markt und Woche | **Umsatzrückgang**: Umsatz im nächsten Quartal unter 50 % des eigenen Durchschnitts der letzten vier Quartale (ja/nein) |
| **Art / Modelltyp** | Zahl über Zeit: **Regression / Zeitreihe** | Kategorie: **Klassifikation** mit Score |
| **Start-Modell** | Vorjahreswert, dann Gradient Boosting mit Wetter und Kalender | logistische Regression, dann Gradient Boosting |
| **Daten** | Kassendaten 10 Jahre, **archivierte Wettervorhersagen**, Kalender, Aktionen | Kundenkarte: Käufe, Warenkorb, Abstand seit letztem Kauf |
| **Handlung** | Bestell-, Umlagerungs- und Aktionsempfehlung für Einkauf und Marktleitung | persönliche Halteaktion (Konditionen, Ansprache) durch Marktleitung oder CRM |
| **Besonderheit** | Fehler **asymmetrisch**: auf ein **Quantil** bestellen (Tag 7, Fallstudie OmniRetail) | **Teilabwanderung**: Handwerker kaufen oft **weniger**, nicht gar nichts mehr. Deshalb Umsatzrückgang statt "kein Kauf" |

---

## 6. Ergebnis 5: ROI und Risikoanalyse

### 6.1 ROI der gewählten Use Cases

```
ROI = (Nutzen − Kosten) / Kosten
```

**Garten** (Annahme: Kosten 180 T€ Aufbau im Jahr 1 + 60 T€ Betrieb im Jahr 2 = 240 T€; Nutzen nur aus dem **Volljahr 2**, Einsparungen im Jahr 1 sind nicht eingerechnet):

| Szenario | Nutzen Jahr 2 | ROI |
| --- | ---: | ---: |
| **Vorsichtig** (halbe untere Grenze) | 1,0 Mio. € | (1.000 − 240) / 240 = **3,2** (317 %) |
| **Planwert** (untere Grenze der Folie) | 2,0 Mio. € | (2.000 − 240) / 240 = **7,3** (733 %) |
| **Obere Grenze** | 3,0 Mio. € | (3.000 − 240) / 240 = **11,5** (1.150 %) |

**Break-even beim Garten:** Der Aufbau allein (180 T€) ist bei **2,0 %** weniger Abschriften eingespielt (180 / 9.000), die Kosten über zwei Jahre (240 T€) bei **2,7 %**. Schon etwa **3 % weniger Abschriften** decken also alles. Auch das **ganze Budget von 500 T€** wäre bei **5,6 %** weniger Abschriften (500 / 9.000) wieder eingespielt.

**Handwerker** (Kosten 140 T€ + 40 T€ Betrieb = 180 T€; Nutzen = Rohertrag auf den erreichbaren Umsatz):

| Sicht | Nutzen | ROI |
| --- | ---: | ---: |
| **Heute** (55 % Karte, 30 % Marge): 0,55 · 1,5 Mio. € · 0,3 | etwa 0,25 Mio. € | (247 − 180) / 180 ≈ **0,4** (etwa 40 %) |
| **Mit Kartenquote 100 %** (30 % Marge): 1,5 Mio. € · 0,3 | 0,45 Mio. € | (450 − 180) / 180 = **1,5** (150 %) |

Der **kurzfristige ROI** der Handwerker ist also **deutlich schwächer** als beim Garten. Der Nutzen hängt stark an der **Kartenquote**, die wir ausbauen. Das ist ein Argument für den **frühen Datenaufbau** (Ergebnis 6).

### 6.2 Risikoanalyse (Frühwarnzeichen und Gegenmaßnahme)

**Garten**

| Risiko | Frühwarnzeichen | Gegenmaßnahme |
| --- | --- | --- |
| **Marktleitungen und Einkauf ignorieren die Prognose** | **Übernahmequote** der Empfehlungen unter 50 % nach 6 Wochen | Gründe erfragen, Empfehlung **erklären** (Treiber wie Temperatur, Vorjahr), einfach nutzbar machen, Abschriften als Ziel der Marktleitung verankern |
| **Leakage im Test:** Training mit dem **tatsächlichen** Wetter statt der **damaligen Vorhersage** | Modell im Backtest **viel besser** als im Pilot | Nur **archivierte Vorhersagen** nutzen, Pilot gegen Kontrollmärkte |
| **Wetterprognose trägt nur wenige Tage**, Saisonware wird aber **Wochen vorher** bestellt | Modell hilft bei Vorordern kaum | Wetter für **Nachsteuerung, Umlagerung und Aktionen** nutzen, für Vorordern Saisonmuster und Klimatologie, **Quantile** für Szenarien |
| **Datenqualität:** Fehlbestände werden als "Absatz 0" gewertet | Prognose zu niedrig in Wochen mit Lücken | Fehlbestandswochen als **fehlend** behandeln, nicht als Null |
| **Nutzenversprechen zu hoch** (2 bis 3 Mio. €) | Abschriftenrückgang im Pilot unter 10 % relativ | Auf **abschriftenstarke Warengruppen** konzentrieren, mit der **unteren Grenze** planen |

**Handwerker**

| Risiko | Frühwarnzeichen | Gegenmaßnahme |
| --- | --- | --- |
| **Datenlücke:** nur 55 % mit Karte | **Kartenquote** steigt bis Ende Q2 nicht | Anreize (Handwerkerkonditionen **nur mit Karte**), Abfrage an der Kasse, Aktion nachschärfen |
| **Aktion wirkt nicht** oder weckt **schlafende Hunde** | Abwanderung in der **Aktionsgruppe** nicht niedriger als in der **Kontrollgruppe** | **Kontrollgruppe** von Beginn an, Aktion ändern oder stoppen |
| **Abwanderung ist unscharf** (Teilabwanderung) | Modell trifft kaum, Zielgröße schwankt | Definition über **Umsatzrückgang** statt "kein Kauf", mit Fachbereich festlegen |
| **Datenschutz:** Profiling mit Kundenkarte | Datenschutz oder Kunden beanstanden | Rechtsgrundlage und Einwilligung früh klären, nur nötige Daten |
| **Handwerker wandern in der Zwischenzeit ab** | Aktivquote sinkt weiter | **Regelbasierte Sofortmaßnahme** (z. B. kein Kauf seit 60 Tagen: Anruf), kein Warten auf das Modell |

**Personal**

| Risiko | Frühwarnzeichen | Gegenmaßnahme |
| --- | --- | --- |
| **Betriebsrat und Beschäftigte lehnen ab** | Widerstand im Gespräch, Verzögerung | **Früh einbinden**, Empfehlung statt Automatik, transparente Ziele |
| **Zu wenig Personal** (teurer Fehler: Wartezeit, Verkauf geht verloren) | Wartezeiten und Beschwerden steigen | Im Zweifel **eher auf der sicheren Seite** planen (Quantil), Pilot in wenigen Märkten |
| **Nur 12 Märkte** liefern Daten | Übertragbarkeit auf andere Märkte unklar | Pilot begrenzen, Zähler schrittweise nachrüsten, wenn Nutzen belegt |

**Über alle Use Cases**

| Risiko | Frühwarnzeichen | Gegenmaßnahme |
| --- | --- | --- |
| **Überlastung des 3-Personen-Teams** | Meilensteine verschieben sich um mehr als 4 Wochen | Use Case 3 **zurückstellen** (Gate), externe Hilfe, Aufgaben priorisieren |
| **Abhängigkeit von Schlüsselpersonen** | Wissen steckt in einer Person | Dokumentation, Vertretung, Code und Daten gemeinsam ablegen |
| **Erwartungen zu hoch** | Geschäftsführung erwartet Wunder nach 3 Monaten | Realistische Genauigkeit kommunizieren, **Pilot vor Rollout** |

---

## 7. Ergebnis 6: Die Kernentscheidung

**Frage der Folie:** Starten wir mit dem **schnell messbaren Quick Win** (Garten) oder mit dem **strategisch wichtigeren** Thema Handwerker?

### 7.1 Die Abwägung (Folie 7)

| | **Kurzfristiger ROI (Garten)** | **Strategischer Nutzen (Handwerker)** |
| --- | --- | --- |
| **Pro** | Spart schon in der **nächsten Saison** Abschriften. Der sichtbare Erfolg schafft **Vertrauen und Budget**. | Bindung der Handwerker **sichert das Wachstumssegment**. |
| **Contra** | Die **Handwerker wandern in der Zwischenzeit weiter ab**. | **Datenbasis** (Kundenkarte) muss erst ausgebaut werden. Erfolg erst nach **12 bis 18 Monaten** sichtbar. |

### 7.2 Entscheidung: Quick Win zuerst, Handwerker-Datenaufbau parallel

> **Wir starten mit dem Garten (Quick Win) und legen das Fundament für die Handwerker von Tag 1 an.** Das ist **keine Entweder-oder-Entscheidung**, sondern eine Reihenfolge mit Überlappung.

**Begründung gegenüber der Geschäftsführung:**

1. **Der Engpass bei den Handwerkern ist die Datenbasis, nicht das Modell.** Ein Modell auf 55 % der Handwerker wäre **blind** für fast die Hälfte. Der Ausbau der Kartenquote dauert Monate, also fangen wir **sofort** damit an. Das kostet im Q1 wenig (30 T€), und nichts wartet auf das Garten-Modell.
2. **Der Garten finanziert das Vertrauen.** Nach 6 Monaten gibt es einen **messbaren Erfolg in Euro**. Damit steht die Freigabe der Reserve und des Handwerker-Piloten auf festem Boden.
3. **Der Garten ist finanziell deutlich stärker:** 2 bis 3 Mio. € gegen etwa 0,25 Mio. € Ergebniswirkung (Abschnitt 2.3). Der strategische Wert der Handwerker liegt im **Wachstumssegment und im Datenfundament**, nicht in der Einjahres-Zahl.
4. **Dem Risiko "Handwerker wandern weiter ab" begegnen wir ohne Modell:** mit einer **regelbasierten Sofortmaßnahme** (z. B. Kontakt, wenn seit 60 Tagen nichts gekauft wurde). So verlieren wir in der Wartezeit nicht ungeschützt Kunden.
5. **Das Kartenfundament nützt später auch App und Angebote.** Es ist eine Investition in einen **gemeinsamen Datenschatz**.

**Was wir offen sagen:** Der **kurzfristige ROI** der Handwerker ist schwächer als der des Gartens (Abschnitt 6.1). Wir rechtfertigen ihn mit dem Wachstumssegment, und dazu fehlt in den Folien eine Zahl. Die **Geschäftsführung** muss entscheiden, wie viel das Segment strategisch wert ist.

**Wann würden wir anders entscheiden?**

- **Handwerker zuerst**, wenn das Segment stark wächst oder besonders profitabel ist (**Zahlen nachfordern**), oder wenn die Kartenquote schon über etwa 80 % läge.
- **Garten nicht zuerst**, wenn der Start nach der Saison liegt und ein Erfolg erst in einem Jahr sichtbar wäre. Dann könnte Personal als schneller Beleg dienen.

---

## 8. Kurzvortrag: Gliederung (5 Minuten)

| Folie | Inhalt | Kernbotschaft |
| :-: | --- | --- |
| 1 | Ausgangslage | Zwei Kernprobleme: **9 Mio. € Abschriften**, Handwerker wandern ab. 3 Use Cases, 500 T€ |
| 2 | Auswahl | **Garten**, **Handwerker**, **Personal (optional)**. App und Preis später |
| 3 | Bewertungsmatrix | Vier Kriterien, Gewichte begründet. **Garten ist in jeder Gewichtung Platz 1** |
| 4 | Kernentscheidung | **Quick Win zuerst**, **Handwerker-Daten parallel** |
| 5 | Plan und Budget | Quartalsplan, 500 T€ verteilt, **Gate** nach Q2 und Q4 |
| 6 | Risiken und ROI | Frühwarnzeichen, Break-even **2,7 %** weniger Abschriften |

---

## 9. Abgleich mit den Bewertungskriterien (Folie 8)

| Kriterium der Folie | Wo erfüllt |
| --- | --- |
| **Priorisierungskriterien klar und nachvollziehbar gewichtet** | Abschnitt 3.1 (Gewichte mit Begründung), 3.3 (Robustheit) |
| **ROI vs. strategischer Nutzen explizit entschieden** | Abschnitt 6.1 (ROI), 7 (Entscheidung: Quick Win zuerst, Handwerker parallel) |
| **Umsetzungsplan nennt Verantwortliche, Quartale und Budget** | Abschnitt 5.1 (Wer), 5.2 (Quartale), 5.3 (Budget) |
| **Risiken benannt, mit Frühwarnzeichen und Gegenmaßnahme** | Abschnitt 6.2 |

---

## Kernaussagen

1. **Kernprobleme zuerst:** Wir messen jeden Kandidaten an **Abschriften** und **Handwerker-Abwanderung** (Relevanz).
2. **Folienzahlen kritisch lesen:** Umsatz ist nicht Gewinn, Datenabdeckung begrenzt den Nutzen (55 % Karte, 12 von 38 Zählern), Wettbewerberzahlen sind kein eigener Nutzen.
3. **Garten gewinnt in jeder Gewichtung.** Platz 2 und 3 (Handwerker gegen Personal) hängen von der Gewichtung ab.
4. **Quick Win zuerst, Strategie parallel vorbereiten:** Der Engpass bei den Handwerkern ist die Datenbasis, nicht das Modell.
5. **Break-even beim Garten:** schon 2,7 % weniger Abschriften decken die Kosten.
6. **Kleines Team, wenig Budget:** höchstens 3 Use Cases, einer davon bewusst leicht und optional, **Gates** nach Q2 und Q4.
7. **Kein Wetter-Leakage:** Training mit **archivierten Vorhersagen**, nicht mit dem tatsächlichen Wetter.
8. **Frühwarnzeichen definieren**, bevor etwas schiefgeht, zum Beispiel die Übernahmequote der Empfehlungen.

---

## Wo könnten Antworten abweichen?

- **Andere Gewichte oder Punkte:** Die Bewertung ist eine **Einschätzung**. Entscheidend ist, dass Skala und Gewichte **vorab festgelegt und begründet** sind (Abschnitt 3.3 zeigt, dass Platz 1 stabil bleibt).
- **Personal weglassen:** Bei knapper Kapazität sind **zwei** Use Cases ausreichend ("höchstens 3"). Dann bleibt das Budget für die Reserve.
- **Handwerker zuerst:** Möglich, wenn die Geschäftsführung das Segment höher bewertet. Dann muss der Plan den **Datenaufbau** und eine **regelbasierte Zwischenlösung** deutlich stärker betonen, und der erste messbare Erfolg kommt später.
- **Andere Marge, andere Abdeckung:** Die **30 % Rohertragsmarge** ist eine Annahme, ebenso die gleichmäßige Verteilung auf die Märkte. Mit anderen Werten ändern sich Wirkung und ROI der Handwerker und des Personaleinsatzes.
- **Budget:** Ob die **Gehälter des BI-Teams** im Budget enthalten sind, ist offen und ändert die Verteilung stark.
- **Startzeitpunkt:** Die Saisonplanung (Pilot im Q2) gilt für einen **Start im Q1**.

---

*Hinweis zur Entstehung: Entwurf auf Basis der Folien "Transferprojekt" (UE 8) und der Folien UE 1 bis UE 3 zu Use-Case-Design. Gegeben sind die Eckdaten, die Kandidaten und die Vorgaben der Folie. Alle Punkte, Gewichte, die 30 % Rohertragsmarge, die Budgetverteilung, der Quartalsplan und die Kosten für Betrieb sind Annahmen und Vorschläge, keine Folienangaben.*
