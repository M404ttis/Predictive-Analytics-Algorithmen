# UE 2 · Arbeitsauftrag 1 – Datenprobleme bei der Gartenwelt Berger GmbH



## 1. Ausgangslage (Kurzfassung)

- Gartenwelt Berger GmbH: 14 Filialen + Onlineshop, Garten- und Freizeitartikel
- **Ziel:** Absatz je Produktgruppe für die nächsten **6 Monate** vorhersagen (→ Zeitreihen-Prognose, vgl. UE 1 Folie 16/21)
- **Heute:** Einkauf nach Erfahrung der Filialleitungen → Frühjahr: Bestseller ausverkauft, Herbst: Ware bleibt liegen
- **Unsere Rolle:** Datenanalyse-Team; Ziel ist, Datenprobleme zu *erkennen und zu strukturieren* (noch nicht zu lösen)

| Quelle | Inhalt | Details aus der Aufgabe |
|---|---|---|
| Kassensystem | Bons: Artikel, Menge, Preis, Datum | seit 2019, CSV je Filiale; 2 Filialen Systemwechsel März 2023 |
| Onlineshop | Bestellungen mit Kundenkonto | seit 2021, Excel; Datum `TT.MM.JJJJ` (Kasse: `JJJJ-MM-TT`) |
| Kundendaten | Kundenkarte (Filiale) / Kundenkonto (online) | Filialen zählen Karten, Onlineshop zählt Konten als „Kunden“ |
| Produktstamm | 8.000 Artikel in Produktgruppen | seit 2024 neue Einteilung: 12 statt 9 Gruppen |
| Wetterdaten | Temperatur, Niederschlag je Region | externer Anbieter, täglich aktualisiert |

---

## 2. Aufgabe 1 + 2: Datenprobleme identifizieren und kategorisieren

Kategorien laut Orientierungsraster: \
**Qualität** (fehlende Werte, Ausreißer, Duplikate) \
**Struktur** (Formate, Datentypen, Dateistruktur)\
**Inhalt** (unklare Definitionen, Inkonsistenzen, fehlender Kontext)

| # | Datenproblem | Quelle | Kategorie | Warum ist das ein Problem? | Konzept aus UE 1 |
|---|---|---|---|---|---|
| 1 | **Produktgruppen ändern sich 2024** (9 → 12 Gruppen) | Produktstamm | Inhalt | Zeitreihe je Produktgruppe bricht 2024 ab; alte und neue Gruppen sind nicht vergleichbar, solange kein Mapping existiert. Prognose soll genau *je Produktgruppe* erfolgen. | Inkonsistenzen, Aufbereitung: vereinheitlichen |
| 2 | **Absatz ≠ Nachfrage** (im Frühjahr ausverkauft, im Herbst Überbestand) | Kasse / Online | Inhalt | Wenn Ware ausverkauft ist, sieht man nur den Absatz, nicht die eigentliche Nachfrage → Frühjahrsspitzen werden unterschätzt. Abverkäufe im Herbst evtl. nur durch Rabatte erzielt. Fehlender Kontext: Bestandsdaten. | fehlender Kontext, Verzerrung der Prognose |
| 3 | **Systemwechsel in 2 Filialen (März 2023)** | Kasse | Struktur + Qualität | Evtl. andere Spalten/Artikelnummern/Formate vor und nach dem Wechsel; mögliche Lücken oder Doppelbuchungen rund um den Wechsel; Strukturbruch in der Zeitreihe dieser Filialen. | fehlende Werte, Dubletten, vereinheitlichen |
| 4 | **Unterschiedliche Datumsformate** (`TT.MM.JJJJ` vs. `JJJJ-MM-TT`) | Online vs. Kasse | Struktur | Zusammenführen ohne Vereinheitlichung führt zu Fehlinterpretation (z. B. 03.04. vs. 2023-04-03) oder fehlerhaften Zeitreihen. Gut lösbar. | vereinheitlichen |
| 5 | **„Kunde“ ist nicht gleich definiert** (Karte vs. Konto) | Kundendaten | Inhalt | Eine Person kann Karte *und* Konto haben → Doppelzählung; Personen ohne Karte/Konto fehlen komplett. Kundenzahlen sind nicht vergleichbar. | Dubletten, unklare Definitionen |
| 6 | **Verteilte Quellen & Formate** (14 CSV-Dateien + Excel + Produktstamm + Wetter) | alle | Struktur | Aufwändiges manuelles Zusammenführen, Fehlerrisiko, keine einheitliche Datengrundlage (Datensilos). | Aufbereitung: bereinigen, vereinheitlichen |
| 7 | **Unterschiedlich lange Historien** (Kasse ab 2019, Online ab 2021) | Kasse / Online | Inhalt | Online hat weniger Saisonzyklen → Saisonalität schwerer zu lernen. Außerdem: Online-Anteil wächst vermutlich (Trend) – Kanäle verhalten sich ggf. anders. | Repräsentative Daten, Zeitreihen: Trend/Saison |
| 8 | **Wetterdaten nur je Region** (nicht je Filiale) und nur Vergangenheit/kurzfristig | Wetter | Inhalt + Struktur | Zuordnung Filiale → Region nötig (fehlt evtl.). Vor allem: für eine 6-Monats-Prognose gibt es kein verlässliches Wetter – nutzbar nur als historischer Erklärungsfaktor oder mit Klimadurchschnitt. | Korrelation ≠ Kausalität, Anreichern |
| 9 | **Mögliche Ausreißer durch Sondereffekte** ? (z. B. Corona-Jahre 2020/21 mit Garten-Boom, Aktionen, Großbestellungen online) | Kasse / Online | Qualität | Verzerren Mittelwerte und lernen „Ausnahme“ als Normalfall. Fehler oder echte Besonderheit? → erst prüfen. | Ausreißer, Mittelwert vs. Median |
| 10 | **Fehlende Einflussdaten** ? (Preisaktionen, Werbung, Bestand, Retouren/Stornos, Filialeröffnungen/-schließungen) | – | Inhalt | Ohne diese Information sind Absatzschwankungen nicht erklärbar. Preis steht auf dem Bon, aber keine Aktionskennzeichnung. | fehlender Kontext, anreichern |
| 11 | **Artikel-Stammdaten über die Zeit** ? (neue/ausgelistete Artikel, evtl. unterschiedliche Artikelnummern in Kasse/Online) | Produktstamm | Inhalt + Qualität | Artikel müssen eindeutig zwischen Kasse, Online und Produktstamm verknüpfbar sein; sonst gehen Umsätze verloren oder werden doppelt gezählt. | Inkonsistenzen, Dubletten |

> Punkte mit `?` sind plausible Annahmen, die **nicht** direkt in der Aufgabenstellung stehen – ggf. kennzeichnen oder streichen.

### Verteilung nach Kategorie

| Kategorie | Probleme (#) |
|---|---|
| Qualität | 3, 9, 11 (teilweise) |
| Struktur | 3, 4, 6, 8 (teilweise) |
| Inhalt | 1, 2, 5, 7, 8, 10, 11 |

> Beobachtung für die Diskussion: Viele Probleme passen in **mehrere** Kategorien (z. B. #3, #8, #11) – das entspricht dem Hinweis im Auftrag, dass „Struktur, Qualität und Inhalt ineinandergreifen“. `TODO` Entscheiden, welche Hauptkategorie wir je Problem festlegen.

---

## 3. Aufgabe 3: Kritikalität für die Prognose bewerten

Leitfragen aus dem Auftrag:
1. Verzerrt das Problem die Prognose **direkt**?
2. Lässt es sich mit **vertretbarem Aufwand** beheben?
3. Welche Daten brauchen wir **zwingend**, welche sind „nice to have“?

Skala: 🔴 kritisch · 🟠 wichtig · 🟢 unkritisch/gut lösbar

| # | Problem | Verzerrt direkt? | Aufwand | Zwingend? | Bewertung | Begründung / Empfehlung |
|---|---|---|---|---|---|---|
| 1 | Produktgruppen 9 → 12 | Ja, stark | mittel (Mapping Alt→Neu auf Artikelebene) | Ja | 🔴 | Zielgröße der Prognose ist Absatz je Produktgruppe. Lösung: alle Artikel rückwirkend der neuen Gruppierung zuordnen (Artikelebene ist vorhanden). |
| 2 | Absatz ≠ Nachfrage (Ausverkauf) | Ja, systematisch | hoch (Bestandsdaten nötig, Schätzung der verpassten Nachfrage) | Ja (Bestand) | 🔴 | Genau das beobachtete Geschäftsproblem; Modell würde die Unterversorgung „lernen“ und fortschreiben. Mindestens bekannt machen, ggf. Bestandsdaten ergänzen. |
| 3 | Systemwechsel 2 Filialen | Teilweise (2 von 14 Filialen) | mittel | Ja | 🟠 | Lücken/Brüche prüfen, Spaltenmapping. Betrifft Datenqualität der Filialen, nicht das Gesamtbild. |
| 4 | Datumsformate | Ja, wenn unbehandelt | gering | Ja | 🟢 | Schnell und eindeutig behebbar (einheitliches ISO-Format). Aber: Fehler hier wäre fatal, daher früh erledigen. |
| 5 | „Kunde“ uneinheitlich | Gering für Absatzprognose | mittel–hoch (Personenabgleich) | Nein (nice to have) | 🟢/🟠 | Für Absatz je Produktgruppe nicht nötig; relevant erst für Kundenanalysen/Segmentierung. Aber Kennzahlen „Kunden“ nicht verwenden, bis definiert. |
| 6 | Verteilte Quellen/Formate | Indirekt | mittel | Ja | 🟠 | Grundvoraussetzung für alles andere; einmal automatisierte Zusammenführung bauen statt manuell. |
| 7 | Unterschiedliche Historien | Ja (Saisonalität online) | nicht behebbar, nur handhabbar | Ja | 🟠 | Mehr Daten gibt es nicht; Online ggf. gemeinsam mit Filialen modellieren, Kanal als Merkmal. |
| 8 | Wetterdaten | Gering–mittel | mittel | Nein (nice to have) | 🟢 | Für 6-Monats-Horizont kaum prognosefähig; erst Basismodell ohne Wetter, später als Zusatz testen. |
| 9 | Ausreißer / Sondereffekte | Ja, mittel | gering–mittel | Ja (Prüfung) | 🟠 | Erst klären: Fehler oder echte Seltenheit? Dann bewusst behandeln (Median, markieren, ausschließen). |
| 10 | Fehlende Einflussdaten (Aktionen, Werbung…) | Ja, indirekt | mittel–hoch | teils | 🟠 | Aktionskennzeichnung hätte hohen Nutzen; Rest nice to have. |
| 11 | Artikelzuordnung Kasse/Online/Stamm | Ja bei Fehlern | mittel | Ja | 🟠 | Voraussetzung für Lösung von #1. |

### Fazit (Entwurf)

- **Kritisch (zwingend vor dem Start klären):** #1 Produktgruppen-Umstellung, #2 Absatz ≠ Nachfrage
- **Wichtig (zeitnah beheben):** #3, #6, #7, #9, #10, #11
- **Gut lösbar / später:** #4 (schnell erledigt, aber früh!), #5, #8
- Leitgedanke aus dem Auftrag: **Nicht jedes Problem muss vor dem Start gelöst sein – aber jedes muss bekannt sein.**



---

# UE 3 · Arbeitsauftrag 2 – Auswahl eines Modellansatzes

**Aufgabe:**
1. Jedem Szenario einen Modelltyp zuordnen
2. Einfach und nachvollziehbar begründen
3. Risiken bei falscher Modellwahl benennen

**Rahmenbedingungen:**
- Daten teilweise unvollständig
- Zeitdruck, schnelle Lösung nötig

**Konzepte aus UE 1:**
- Modell-Lifecycle: Daten → Training → Validierung → Deployment & Monitoring
- Algorithmen: Regression, Klassifikation, Zeitreihe

## 4. Aufgabe 1: Zuordnung Szenario → Modelltyp

| Szenario | Zielgröße | Modelltyp |
|---|---|---|
| A) Verkaufszahlen vorhersagen (kontinuierlich) | eine Zahl | **Regression** |
| B) Kunde kündigt (ja/nein) | Kategorie | **Klassifikation** |
| C) Monatliche Trends über Zeit | zeitlicher Verlauf | **Zeitreihe** |

## 5. Aufgabe 2: Begründung

Leitregel aus UE 1 (Folie 16): Die **Zielgröße** entscheidet – *nicht* die verfügbaren Daten.

| Szenario | Begründung (einfach) | Beispiel-Verfahren | Bezug zu Arbeitsauftrag 1 |
|---|---|---|---|
| A) Regression | Gesucht ist eine konkrete Zahl, die sich aus Eingaben wie Preis, Saison, Werbung ergibt. | lineare Regression | Preis steht auf dem Bon; Aktionen/Werbung fehlen (#10) |
| B) Klassifikation | Gesucht ist ein Ja/Nein. Das Modell liefert eine Wahrscheinlichkeit, eine Schwelle entscheidet über die Zuordnung. | Entscheidungsbaum | Braucht saubere Kundendefinition (#5) |
| C) Zeitreihe | Die Reihenfolge in der Zeit zählt. Das Modell erkennt Trend und Saisonalität und schreibt sie fort. | saisonale Fortschreibung | Passt zum Ziel „Absatz je Produktgruppe, nächste 6 Monate“ |

> **Zusammenhang mit Arbeitsauftrag 1:** Die Gartenwelt-Prognose ist im Kern ein **Zeitreihen-Problem (C)** (Saison: Frühjahr/Herbst). Regression (A) kann ergänzend Einflussfaktoren wie Preis oder Wetter berücksichtigen. Klassifikation (B) passt nicht zur Zielgröße.

### Umgang mit den Rahmenbedingungen

| Rahmenbedingung | Konsequenz für die Modellwahl |
|---|---|
| Daten teilweise unvollständig | Lücken zuerst prüfen und behandeln (löschen, schätzen, ersetzen). Bei Zeitreihen besonders wichtig: Lücken zerstören den zeitlichen Verlauf. Einfache, robuste Modelle bevorzugen. |
| Zeitdruck | Mit einfachem Basismodell starten, validieren, in Betrieb nehmen und iterativ verbessern (Lifecycle ist iterativ). Erklärbare Verfahren sind schneller vermittelbar. |

> `TODO` Prüfen: Sind die Beispiel-Verfahren Teil der Folien (dort nur: lineare Regression, Entscheidungsbäume)? „Saisonale Fortschreibung“ ist meine Ergänzung – ggf. streichen.

## 6. Aufgabe 3: Risiken bei falscher Modellwahl

| Falsche Wahl | Folge |
|---|---|
| A oder C statt B (Zahl statt Ja/Nein) | Keine klare Entscheidung ableitbar („Kunde kündigt mit 0,37“ ohne Schwelle). |
| B statt A (Kategorien statt Zahl) | Informationsverlust: nur „viel/wenig“ statt konkreter Menge; Einkauf nicht planbar. |
| A statt C (Regression statt Zeitreihe) | Trend und Saisonalität werden übersehen → Frühjahrsspitzen unterschätzt, Herbst überschätzt (genau das heutige Problem). |
| Zu komplexes Modell bei wenig/lückenhaften Daten | Overfitting: glänzt im Training, versagt in der Praxis. |
| Ohne Validierung / Monitoring | Fehler fallen erst im Betrieb auf; Model Drift bleibt unbemerkt. |

*Legende:* \
**A** = Verkaufszahlen vorhersagen (Zahl → Regression) \
**B** = Kündigung vorhersagen (Ja/Nein → Klassifikation) \
**C** = Monatliche Trends über Zeit (Verlauf → Zeitreihe)

**Allgemeine Folgen:** Zeitverlust (Neustart des Projekts), Vertrauensverlust bei Fachbereich und Filialleitungen, verschwendetes Budget.

## 7. Kernbotschaft und Diskussionsvorbereitung

- **Kernbotschaft:** Die Zielgröße bestimmt den Modelltyp – nicht die verfügbaren Daten. Falsche Modellwahl kostet Zeit, Vertrauen und Budget.
- **Wo könnten Zuordnungen abweichen?** Szenario A vs. C: „Verkaufszahlen“ über mehrere Monate kann man auch als Zeitreihe sehen. Entscheidend ist, ob die Zeit selbst (Trend, Saison) oder Einflussgrößen im Vordergrund stehen. `TODO` gemeinsam festlegen
