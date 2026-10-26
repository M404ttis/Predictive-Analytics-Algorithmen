# Tag 7 · Fallstudie OmniRetail Group: Use Cases zuordnen, Modelltypen benennen, priorisieren

**Aufgabe (Folien "UE 5–6 · Fallstudie"):** Ein Omnichannel-Händler hat mehrere Probleme gleichzeitig, aber begrenzte Ressourcen. Wir sollen

1. die Probleme **Use-Case-Typen zuordnen**,
2. die passenden **Modelltypen benennen**,
3. die Use Cases **priorisieren und die Reihenfolge begründen**.

Leitfragen der Folie: *Welcher Modelltyp passt je Problem? Wo ist die Datenlage am besten? Welcher Use Case bringt schnell Wert?*

> **Annahmen und Herkunft:** Gegeben sind nur die Zahlen der Folie (Abschnitt 1). Alles andere, vor allem der **erreichbare Anteil** der Kosten (10 bis 20 %), die **Punktebewertung** in Abschnitt 5 und die Zahlenbeispiele, sind **Annahmen** und mit Annahme gekennzeichnet. Sie lassen sich austauschen. Die Folie nennt das dritte Problem ("Weitere Herausforderung im Tagesgeschäft") nicht beim Namen, aus der Tabelle auf Folie 3 lesen wir daraus **Retouren**.

---

## Das Ergebnis in Kürze

| Frage der Folie | Antwort |
| --- | --- |
| **Welcher Modelltyp passt je Problem?** | Lager: **Regression / Zeitreihe** (Absatz in Stück). Churn: **Klassifikation** (wandert ab ja/nein). Retouren: **Klassifikation** (Retoure ja/nein), davor **Textanalyse** der Gründe. |
| **Wo ist die Datenlage am besten?** | **Lager** (ERP, gut). Danach Churn (CRM, mittel). Am schwächsten: Retouren (Freitext). |
| **Welcher Use Case bringt schnell Wert?** | **Lager**: größtes Problem (1,2 Mio €) **und** beste Daten. |
| **Reihenfolge** | **1. Lager, 2. Churn, 3. Retouren** (Retouren zunächst nur Datenbasis verbessern, noch kein Modell). |

Lager liegt bei **jedem** der vier Kriterien mindestens so gut wie Churn. Deshalb steht die Reihenfolge **unabhängig von der Gewichtung** fest (Abschnitt 5.3).

---

## 1. Ausgangslage

| Merkmal | Angaben (Folie 2 und 3) |
| --- | --- |
| **Unternehmen** | OmniRetail Group, Omnichannel-Händler: **40 Filialen + Online** |
| **Kunden** | etwa **120.000** |
| **Team** | **ein kleines Data-Team** |
| **Rahmenbedingungen** | begrenzte Ressourcen, verschiedene Datenlagen je Bereich, **schnelle erste Erfolge** erwünscht, mehrere Problemfelder gleichzeitig |

| Problemfeld | Kosten pro Jahr | Datenlage |
| --- | ---: | --- |
| **Überbestand / Lager** | 1,2 Mio € | gut (ERP) |
| **Kundenabwanderung** | 800 T€ | mittel (CRM) |
| **Retouren** | 450 T€ | schwach (Freitext) |
| **Summe** | **2,45 Mio €** | |

**Wichtig:** Die Kosten sind die **Größe des Problems**, nicht das, was wir einsparen können. Ein Modell beseitigt nie 100 % davon. In Abschnitt 5 rechnen wir deshalb mit einem **erreichbaren Anteil**.

---

## 2. Aufgabe 1: Probleme Use-Case-Typen zuordnen

Wir übersetzen jedes Symptom wie in Tag 7 in eine **Vorhersagefrage mit Handlung** (Folien UE 1: Symptom → Ursache → Use Case).

| Problem (Symptom) | Ursache, an der der Use Case ansetzt (Hypothese) | Use-Case-Typ | Fachfrage |
| --- | --- | --- | --- |
| **Überbestand / Lager** (und Unterbestand) | Bestellmengen folgen Bauchgefühl oder Vorjahreswert, nicht einer Prognose der Nachfrage je Artikel und Filiale | **Nachfrageprognose** (Demand Forecasting) zur Bestellsteuerung | "Wie viel verkaufen wir wovon wo?" |
| **Kundenabwanderung** | Kunden werden **inaktiv, bevor** jemand reagiert. Es gibt keine Warnung und keine Halteaktion | **Abwanderungsprognose** (Churn Prediction) mit Halteaktion | "Wer wandert ab?" |
| **Retouren** | Unklar, **warum** zurückgeschickt wird. Die Gründe stehen als Freitext, kaum auswertbar | **Retourenrisiko je Bestellung**, davor **Analyse der Gründe** (Textanalyse) | "Welche Bestellung kommt zurück, und warum?" |

**Eine Besonderheit beim Lager:** Das Problem heißt **Über- und Unterbestand**. Beide Fehler kosten Geld: Überbestand bindet Kapital und führt zu Abschriften, Unterbestand heißt entgangener Umsatz. Der Use Case muss also **beide Richtungen** behandeln, nicht nur "weniger Bestand".

**Eine Besonderheit bei Churn im Handel:** Es gibt oft **keine Kündigung**, wie bei Fitness oder Telekom. Ein Kunde kauft einfach nicht mehr. Die Zielgröße braucht deshalb eine **Definition von Inaktivität** (siehe 3.3).

---

## 3. Aufgabe 2: Modelltypen und Zielgrößen

### 3.1 Überblick

| | **Lager** | **Churn** | **Retouren** |
| --- | --- | --- | --- |
| **Zielgröße** | Absatz in Stück je **Artikel, Filiale und Woche**, 4 Wochen im Voraus | Kein Kauf in den **nächsten 180 Tagen** bei bisher aktivem Kunden (ja/nein) | Retoure der Bestellposition (ja/nein) |
| **Art der Zielgröße** | **Zahl**, mit **Entwicklung über Zeit** | **Kategorie** (ja/nein) | **Kategorie** (ja/nein) |
| **Modelltyp** | **Regression / Zeitreihe** | **Klassifikation** mit Score | **Klassifikation** mit Score. Vorstufe: **Textklassifikation** der Retourengründe |
| **Start-Modell (Baseline)** | Absatz derselben Woche im Vorjahr, gleitender Mittelwert | logistische Regression | logistische Regression |
| **Stärkeres Modell** | Gradient Boosting mit Kalender- und Aktionsmerkmalen | Gradient Boosting | Gradient Boosting |
| **Metrik** | WAPE und MAE (Tag 7), dazu Kosten von zu viel und zu wenig | Recall, Precision, **Wert in Euro** (Tag 6) | Precision bei den Top-Risiken, Wert in Euro |
| **Daten** | Verkäufe, Preise, Aktionen, Kalender, Bestand (ERP) | Kaufhistorie, Kontakte, Kanäle (CRM) | Bestellpositionen, Artikel, Größe, Retourengrund (Freitext) |

Die Zuordnung folgt der Übersetzungstabelle von UE 1: ja/nein → Klassifikation, Zahl → Regression, Verlauf über Zeit → Zeitreihe.

### 3.2 Lager: Steckbrief

| Baustein | Inhalt |
| --- | --- |
| **Problem** | 1,2 Mio € Kosten durch Über- und Unterbestand |
| **Zielgröße** | Absatz in Stück je Artikel, Filiale und Woche, 4 Wochen voraus (Zeitreihe) |
| **Daten** | ERP: Verkäufe, Bestand, Preise, Aktionen; dazu Kalender (Feiertage, Saison). **Zum Prognosezeitpunkt bekannt:** vergangene Verkäufe, geplante Aktionen, Kalender |
| **Modell** | Baseline (Vorjahreswoche), dann Gradient Boosting. Das ist derselbe Aufbau wie im Favorita-Projekt (Tag 2) |
| **Handlung** | Vorschlag für Bestellmenge je Artikel und Filiale für die **Disposition**, Disponent bestätigt oder ändert |
| **Zuständig** | Einkauf und Disposition |
| **Wirkung messen** | Bestandsreichweite, Abschriften, Lieferfähigkeit vor und nach dem Pilot, Vergleich mit Kontrollfilialen |

**Die Menge folgt aus den Kosten, nicht aus dem Mittelwert.** Zu viel und zu wenig kosten unterschiedlich. Es gilt die Regel des kritischen Verhältnisses (Zeitungsverkäufer-Regel), das Gegenstück zur Schwelle aus Tag 6:

```
τ = C_unter / (C_unter + C_über)
```

- `C_unter`: Kosten **je fehlendem Stück** (entgangener Deckungsbeitrag).
- `C_über`: Kosten **je überschüssigem Stück** (Kapitalbindung, Abschrift).
- `τ` (griechisch "tau"): das **Quantil** der Nachfrage, auf das bestellt wird.

*Beispiel (Annahme):* `C_unter` = 8 €, `C_über` = 2 € → τ = 8 / (8 + 2) = **0,8**. Man bestellt auf das **80-%-Quantil** der Prognose, also etwas **über** dem erwarteten Absatz, weil ein fehlendes Stück viermal so teuer ist wie ein überschüssiges. Das ist der Hintergrund des Quantil-Notebooks im Favorita-Projekt.

### 3.3 Churn: Steckbrief

| Baustein | Inhalt |
| --- | --- |
| **Problem** | 800 T€ Kosten durch Abwanderung. Kunden werden still inaktiv |
| **Zielgröße** | **Kein Kauf in den nächsten 180 Tagen** (ja/nein) bei Kunden, die in den letzten 12 Monaten gekauft haben. Das Fenster (hier 180 Tage) muss zum **üblichen Kaufrhythmus** passen und wird mit den Daten geprüft |
| **Daten** | CRM: Käufe (Zeitpunkt, Wert, Kanal), Abstand seit dem letzten Kauf, Newsletter- und Kontaktverhalten, Retouren, Servicekontakte |
| **Leakage** | Nicht verwenden, was erst nach dem Stichtag bekannt ist: z. B. **Abmeldung vom Newsletter** nach dem Stichtag oder "Kundenkonto gelöscht" |
| **Modell** | logistische Regression als Start (erklärbar), Gradient Boosting als Herausforderer |
| **Handlung** | Ab einer **Schwelle**: persönliche Halteaktion (Gutschein, Mailing) durch das CRM-Team. Darunter nichts |
| **Zuständig** | CRM und Marketing |
| **Wirkung messen** | **Kontrollgruppe** ohne Aktion. Ohne sie weiß man nicht, ob der Kunde wegen der Aktion geblieben ist |

**Schwelle aus den Kosten** (Regel aus Tag 6 und Tag 7):

```
p > K / (q · W)
```

- `p`: vom Modell berechnetes **Abwanderungsrisiko** des Kunden (0 bis 1).
- `K`: Kosten je Halteaktion.
- `q`: Anteil der angesprochenen Abwanderer, die wir halten.
- `W`: Wert eines gehaltenen Kunden.

Die Aktion muss also **billig im Verhältnis zu q · W** sein. Im Handel ist W je Kunde oft klein, deshalb bevorzugt man automatisierte, günstige Aktionen (E-Mail, Gutschein erst bei Einlösung) statt Anrufe.

**Obere Grenze des Nutzens (Annahme):** Halten wir q = 20 % der Abwanderer und erkennt das Modell Recall = 60 % davon, sind das 0,2 · 0,6 = **12 %** der 800 T€, also etwa **96 T€** brutto vor den Aktionskosten. Das passt in die Spanne von 10 bis 20 % aus Abschnitt 5.

### 3.4 Retouren: Steckbrief

| Baustein | Inhalt |
| --- | --- |
| **Problem** | 450 T€ Kosten durch Retouren. Die Gründe stehen nur als **Freitext** |
| **Zielgröße** | Wird die Bestellposition **zurückgeschickt** (ja/nein) |
| **Daten** | Bestellpositionen, Artikel, Größe, Kanal; **Retourengrund (Freitext)** |
| **Leakage** | Der **Retourengrund** ist **erst nach der Retoure** bekannt. Er darf **nicht** als Merkmal in ein Vorhersagemodell, nur in die **Ursachenanalyse** |
| **Zwei Wege** | **(a)** Gründe auswerten (Textanalyse: Themen wie "passt nicht", "Qualität", "gefällt nicht" gruppieren). **(b)** Retourenrisiko je Bestellung vorhersagen |
| **Handlung** | (a) Produktbeschreibung und Größentabelle verbessern, Lieferanten ansprechen. (b) Hinweis bei Risikobestellung, z. B. Größenberatung |
| **Zuständig** | Kundenservice, Produktmanagement, Online-Team |
| **Besonderheit** | **Keine automatischen Sanktionen** gegen Kunden mit hohem Score (Fairness, Kundenbeziehung) |

**Reihenfolge innerhalb des Falls:** Erst **Daten verbessern** (Retourengrund als **Pflichtauswahl** statt Freitext, dazu optional Freitext), dann ein Modell. Ein Modell auf schwachen Daten liefert schwache Ergebnisse.

---

## 4. Wo ist die Datenlage am besten?

| Problem | Datenlage (Folie) | Einschätzung für den Use Case |
| --- | --- | --- |
| **Lager** | **gut (ERP)** | Verkäufe und Bestände liegen strukturiert vor, lange Historie. **Beste Basis.** |
| **Churn** | **mittel (CRM)** | Käufe vorhanden, aber Lücken bei Kanälen (Filiale ohne Kundenkarte, Online mit Konto) und bei der Definition "abgewandert". Brauchbar nach Aufbereitung. |
| **Retouren** | **schwach (Freitext)** | Grund nicht strukturiert, Qualität unklar. **Erst verbessern**, dann modellieren. |

---

## 5. Aufgabe 3: Priorisieren und begründen

### 5.1 Kriterien (und Skala)

Wir bewerten nach den Bewertungsachsen aus UE 1 (Business Impact × Umsetzbarkeit), ergänzt um die Rahmenbedingungen der Fallstudie ("schnelle erste Erfolge", "begrenzte Ressourcen"). **Skala 1 bis 5** (5 = am besten). Die Skala wird **vorab festgelegt**, sonst sind die Punkte beliebig:

| Kriterium | Gewicht | 1 bedeutet | 5 bedeutet |
| --- | ---: | --- | --- |
| **Business Impact** | 35 % | erreichbarer Nutzen unter 25 T€ pro Jahr | ab 150 T€ pro Jahr (Stufen dazwischen: 2 = 25 bis 60 T€, 3 = 60 bis 100 T€, 4 = 100 bis 150 T€; bewertet wird die **Mitte** der Spanne aus 5.2) |
| **Datenlage** | 25 % | Freitext, unstrukturiert | strukturiert, lange Historie |
| **Aufwand / Machbarkeit** | 20 % | viel Neuaufbau, viele Beteiligte | Standardverfahren, wenige Beteiligte |
| **Zeit bis zum Wert** | 20 % | Wirkung erst nach über 12 Monaten | erste Wirkung in unter 3 Monaten |

### 5.2 Erreichbarer Nutzen (Annahme)

Ein Modell löst nur einen **Teil** des Problems. Wir nehmen für jedes Feld einen erreichbaren Anteil an:

| Problem | Kosten pro Jahr | erreichbarer Anteil (Annahme) | erreichbarer Nutzen pro Jahr |
| --- | ---: | ---: | ---: |
| Lager | 1.200 T€ | 10 bis 20 % | **120 bis 240 T€** |
| Churn | 800 T€ | 10 bis 20 % | **80 bis 160 T€** |
| Retouren | 450 T€ | 5 bis 15 % (Daten schwächer) | **22 bis 68 T€** |

### 5.3 Bewertung

| Use Case | Impact | Datenlage | Aufwand | Zeit bis Wert | **Gesamt** |
| --- | :-: | :-: | :-: | :-: | :-: |
| **Lager** | 5 | 5 | 3 | 4 | **4,40** |
| **Churn** | 4 | 3 | 3 | 3 | **3,35** |
| **Retouren** | 2 | 1 | 2 | 2 | **1,75** |

Rechenweg (nur Lager, die anderen analog):

```
Score = 0,35 · Impact + 0,25 · Daten + 0,20 · Aufwand + 0,20 · Zeit
Lager = 0,35 · 5 + 0,25 · 5 + 0,20 · 3 + 0,20 · 4 = 1,75 + 1,25 + 0,60 + 0,80 = 4,40
```

**Begründung der Punkte:**

| | Begründung |
| --- | --- |
| **Lager** | Impact 5: größtes Feld (120 bis 240 T€). Daten 5: ERP gut. Aufwand 3: viele Artikel × Filialen, aber Standardverfahren, Disposition muss eingebunden werden. Zeit 4: Pilot in wenigen Warengruppen und Filialen in etwa 3 Monaten möglich, die Wirkung auf Bestände braucht danach einige Umschlagszyklen. |
| **Churn** | Impact 4: zweitgrößtes Feld, aber nur ein Teil der Abwanderer ist haltbar. Daten 3: CRM mittel, Definition "abgewandert" muss geklärt werden. Aufwand 3: Modell **plus** Halteaktion **plus** Kontrollgruppe. Zeit 3: erst nach Aktion und Messfenster (mindestens 90 bis 180 Tage) belegt. |
| **Retouren** | Impact 2: kleinstes Feld. Daten 1: Freitext. Aufwand 2: Textanalyse plus Prozessänderung. Zeit 2: erst Daten sammeln, dann Modell. |

**Die Reihenfolge ist robust:** Lager ist bei **allen vier Kriterien** mindestens so gut wie Churn (5 ≥ 4, 5 ≥ 3, 3 ≥ 3, 4 ≥ 3). Churn ist wiederum bei allen vier besser als Retouren. Dann ergibt **jede beliebige Gewichtung** dieselbe Reihenfolge. Mit gleichen Gewichten (je 25 %) erhält man 4,25 / 3,25 / 1,75, also **dieselbe Reihenfolge**. Nur die **Punkte** selbst sind Einschätzung, nicht die Gewichte.

### 5.4 Einordnung (Impact × Umsetzbarkeit, Folie 17 aus UE 1)

|  | Gut umsetzbar | Schwer umsetzbar |
| --- | --- | --- |
| **Hoher Impact** | **Quick Win: Lager** | **Vorbereiten: Churn** (Definition, Daten, Aktion) |
| **Geringer Impact** | | **Meiden (vorerst): Retouren als Modell.** Daten zuerst verbessern |

---

## 6. Empfohlene Reihenfolge

| Platz | Use Case | Begründung |
| --- | --- | --- |
| **1** | **Lager (Nachfrageprognose)** | Größtes Problem (1,2 Mio €), beste Daten, schneller sichtbarer Nutzen. Erfüllt den Wunsch nach einem **schnellen ersten Erfolg**. |
| **2** | **Churn (Abwanderungsprognose)** | Zweitgrößtes Problem, brauchbare Daten. Baut auf den Erfahrungen und der Infrastruktur von Platz 1 auf. Braucht Vorarbeit in der Definition und Aktion. |
| **3** | **Retouren** | Schwächste Daten, kleinster Nutzen. Zuerst **Datenerfassung verbessern**, noch kein Modell. |

### 6.1 Vorgehen in Phasen (Annahme)

Das Data-Team ist klein und schafft **einen Use Case nach dem anderen**. Die Vorarbeit für spätere Use Cases läuft aber **leichtgewichtig nebenher**:

| Phase | Zeitraum | Lager | Churn | Retouren |
| --- | --- | --- | --- | --- |
| **1** | Monat 0 bis 3 | **Pilot** in 2 bis 3 Warengruppen und einigen Filialen, Baseline gegen Modell | **Definition** von "abgewandert", CRM-Daten prüfen | **Retourengrund als Pflichtauswahl** einführen, keine KI |
| **2** | Monat 3 bis 9 | **Rollout** auf alle Filialen, Wirkung messen | **Pilot** mit Kontrollgruppe | Gründe sammeln, einfache Auswertung (Häufigkeiten) |
| **3** | ab Monat 9 | Betrieb und Monitoring | Rollout, wenn die Kontrollgruppe Wirkung zeigt | **Modell** (Textanalyse, Retourenrisiko), wenn genug saubere Daten vorliegen |

---

## 7. Risiken und Stakeholder

| Use Case | Risiko | Maßnahme |
| --- | --- | --- |
| **Lager** | Aktionen und neue Artikel sind schwer zu prognostizieren. Fehlende Akzeptanz der Disponenten. Fehlbestände werden nicht als "Absatz 0" falsch gewertet | Modell gibt **Empfehlungen**, der Mensch entscheidet mit. Neue Artikel über ähnliche Artikel schätzen. Fehlbestände als **fehlende** Werte behandeln, nicht als Null |
| **Churn** | Aktion erinnert Kunden ans Wechseln ("schlafende Hunde"). Falsche Definition von Abwanderung. Datenschutz bei Marketing | **Kontrollgruppe**, Fenster an Kaufrhythmus anpassen, Einwilligung und Rechtsgrundlage prüfen |
| **Retouren** | Schlechte Datenqualität. Sanktionen gegen Kunden wirken unfair und schaden der Bindung | Daten verbessern vor dem Modell, **keine automatischen Sanktionen** |
| **Alle** | Zu viele Projekte gleichzeitig überfordern das kleine Team | **Ein Use Case zur Zeit**, Pilot vor Rollout, realistische Erwartungen kommunizieren |

**Stakeholder:** Geschäftsführung (priorisiert), Einkauf und Disposition (Lager), Filialleitungen, CRM und Marketing (Churn), Kundenservice und Produktmanagement (Retouren), Datenschutz, Data-Team (setzt um).

---

## 8. Checkliste pro Use Case (Folie 28 aus UE 1)

| Frage | Lager | Churn | Retouren |
| --- | :-: | :-: | :-: |
| Ist das Geschäftsproblem klar? | ja | ja | **teilweise** (Gründe unklar) |
| Ist die Zielgröße messbar? | ja (Stück je Woche) | ja, nach Definition | ja (Retoure ja/nein) |
| Sind die Daten verfügbar? | **ja** | **ja, mit Aufbereitung** | **nein, erst verbessern** |
| Ist die Handlung definiert? | ja (Bestellvorschlag) | ja (Halteaktion) | **teilweise** |

Nur **Lager** erfüllt alle vier Punkte vollständig. Das ist ein weiterer Grund für Platz 1.

---

## Kernaussagen

1. **Das Problem ist ein Symptom.** Aus jedem Problemfeld wird eine **Vorhersagefrage mit Handlung**.
2. **Zielgröße bestimmt Modelltyp:** Lager = Zahl über Zeit (Regression / Zeitreihe), Churn und Retouren = ja/nein (Klassifikation).
3. **Gute Daten und großer Hebel** zusammen machen den Quick Win: Lager.
4. **Die Kosten des Problems sind nicht der Nutzen.** Ein Modell erreicht nur einen Teil, wir rechnen mit 10 bis 20 %.
5. **Die Menge und die Schwelle folgen aus den Kosten:** `τ = C_unter / (C_unter + C_über)` beim Lager, `p > K / (q · W)` bei Churn.
6. **Die Reihenfolge ist robust:** Lager schlägt Churn in allen Kriterien, deshalb hängt Platz 1 nicht von der Gewichtung ab.
7. **Schwache Daten sind kein Grund für ein Modell, sondern für eine bessere Datenerfassung.** Bei Retouren zuerst Pflichtfeld einführen.
8. **Ein kleines Team macht einen Use Case nach dem anderen**, mit Pilot und Kontrollgruppe.

---

## Wo könnten Antworten abweichen?

- **Churn zuerst:** Wenn die Geschäftsführung Kundenbindung **strategisch** höher wertet oder die Lagerdaten schlechter sind als angegeben. Mit den Zahlen der Folie bleibt Lager vorn.
- **Retouren als erster Schritt:** Wenn ein einfacher Hebel ohne Modell (Größentabelle, bessere Produktbeschreibung) schnell wirkt. Das ist ein **Quick Win ohne KI**, aber kein Predictive-Analytics-Use-Case.
- **Andere Zielgrößen:** Beim Churn sind 90 oder 365 Tage statt 180 möglich. Das Fenster muss zum Kaufrhythmus des Händlers passen.
- **Andere Punkte:** Die Bewertung in 5.3 ist eine **Einschätzung**. Eine andere Gruppe darf zu anderen Punkten kommen, solange sie die Skala vorher festlegt und begründet.
- **Zahlen:** Der erreichbare Anteil (10 bis 20 %) und die Beispielkosten (8 € und 2 € beim Lager) sind **Annahmen**.

---

*Hinweis zur Entstehung: Entwurf auf Basis der Folien "Fallstudie OmniRetail" (UE 5–6) und UE 1 bis UE 3 zu Use-Case-Design. Gegeben sind nur Eckdaten und Kosten der Folie. Alle Punkte, Anteile, Beispielkosten und der Phasenplan sind Annahmen.*
