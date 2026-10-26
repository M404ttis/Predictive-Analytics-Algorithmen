# Tag 7 · Use-Case-Design: Lösungen Arbeitsauftrag 1 und 2

> **Inhalt:** Teil I (Abschnitte 0 bis 5) löst **Arbeitsauftrag 1** (drei Geschäftsprobleme als Use Cases). Teil II (Abschnitte 6 bis 9) löst **Arbeitsauftrag 2** (Fehlermaße MAE, RMSE, MAPE).

**Aufgabe (Folie "UE 2 · Arbeitsauftrag 1"):** Drei Geschäftsprobleme in je einen Predictive-Analytics-Use-Case übersetzen:

1. Sinkende Kundenbindung
2. Hohe Lagerkosten
3. Unklare Marketingwirkung

Zu jedem Problem sollen wir (1) einen Use Case formulieren, (2) eine Zielgröße definieren und (3) einen Modelltyp zuordnen. Das Orientierungsraster der Folie fragt dazu: *Was ist die Frage hinter dem Problem? Welche Zielgröße folgt daraus? Ist sie eine Zahl, eine Kategorie oder eine Entwicklung über Zeit?*

> **Annahmen und Herkunft:** Das ist ein Entwurf auf Basis der Folien UE 1 und UE 2. Das Unternehmen **VitalPoint Fitness**, alle Zahlen und Kosten in Abschnitt 2 sind **erfunden und als Annahmen gedacht**, nicht aus den Folien. Sie sollen den Use Case durchrechenbar machen und lassen sich durch eigene Werte ersetzen.

---

## 0. Das Werkzeug: Use-Case-Bausteine

Aus UE 1 (Folien 9, 28, 29) nehmen wir das Raster, nach dem jeder Use Case aufgebaut wird:

| Baustein | Leitfrage |
| --- | --- |
| **Problem** | Ist das Geschäftsproblem klar? (Symptom von Ursache trennen, z. B. mit 5× Warum) |
| **Zielgröße** | Ist sie messbar und eindeutig? Welcher Modelltyp folgt daraus? |
| **Daten & Modell** | Sind die Daten vorhanden, und waren sie **zum Prognosezeitpunkt schon bekannt**? |
| **Entscheidung / Handlung** | Wer tut was, wenn der Score hoch ist? |
| **Bewertung** | Business Impact, Umsetzbarkeit, Risiko |

Ein **schlechter** Use Case sagt "Wir wollen KI nutzen" (kein Ziel, keine Handlung). Ein **guter** hat ein klares Problem und Ziel, vorhandene Daten und eine definierte Handlung samt Wirkung.

---

## 1. Kundenbindung: Was ist das, und wo zählt sie am meisten?

### 1.1 Definition

**Kundenbindung** heißt: Kunden bleiben einem Unternehmen über die Zeit treu. Sie kaufen wieder, verlängern ihren Vertrag oder nutzen das Angebot weiter, statt zu kündigen oder zur Konkurrenz zu gehen.

Zwei Ebenen, die man auseinanderhalten sollte (allgemeine Marketing-Fachbegriffe, nicht aus den Folien):

| Ebene | Frage | Beispiel |
| --- | --- | --- |
| **Verhalten** (messbar) | Was tun die Kunden? | Vertrag verlängert, wieder gekauft, Angebot genutzt |
| **Einstellung** (schwer messbar) | Was denken die Kunden? | zufrieden, vertrauen uns, würden uns weiterempfehlen |

Wichtig für Predictive Analytics: **Zufrieden ist nicht gleich gebunden.** Ein zufriedener Kunde kann trotzdem wechseln, ein unzufriedener bleibt vielleicht wegen einer langen Vertragslaufzeit. Wir können nur **Verhalten** als Zielgröße nutzen, weil nur das in den Daten steht.

**Wie man sie misst:**

| Kennzahl | Bedeutung |
| --- | --- |
| **Kündigungsrate (Churn)** | Anteil der Kunden, die in einem Zeitraum gehen |
| **Bindungsrate (Retention)** | 1 − Kündigungsrate |
| **Wiederkaufrate** | Anteil der Kunden mit einem zweiten Kauf |
| **Kundenwert (Customer Lifetime Value)** | Gesamter Erlös eines Kunden über seine Bindungsdauer |

Das "Problem" der Folie ("sinkende Kundenbindung") ist noch ein **Symptom**, also ein sichtbares Problem ohne Warum. Hier setzt der Use Case an (Folie 5).

### 1.2 Wo sie am meisten zählt

Kundenbindung ist dort besonders wichtig, wo **wiederkehrende Erlöse** das Geschäft tragen, **Neukunden teuer** sind und der **Wechsel leicht** ist:

| Branche | Warum Bindung dort zählt | Typisches Frühsignal |
| --- | --- | --- |
| **Abo- und Mitgliedschaftsmodelle** (Fitness, Streaming, Software) | Der Erlös entsteht monatlich, jede Kündigung kappt ihn | Nutzung lässt nach |
| **Telekommunikation, Energie** | Hohe Akquisekosten, Wechsel per Klick, Preisvergleich | Preisanfragen, Servicekontakte |
| **Versicherung** | Lange Verträge, aber jährlich kündbar | Beschwerden, Schadenfälle |
| **Handel mit Stammkundschaft** | Wiederkäufer bringen den Großteil des Umsatzes | Abstand zwischen Käufen wächst |
| **Gesundheit und Dienstleistung** (Praxen, wie PhysioNord) | Behandlung braucht Kontinuität | Termine werden seltener |

### 1.3 Unser Fall: VitalPoint Fitness (erfunden)

Wir wählen eine **Fitnessstudio-Kette**, weil dort alles zusammenkommt:

- Der Erlös ist ein **Monatsbeitrag**, jede Kündigung wirkt sofort.
- Es gibt ein **starkes, früh sichtbares Signal**: Wer nicht mehr hingeht, kündigt bald. Das System sieht jeden Besuch.
- Die **Handlung** ist klar und billig (Anruf, Trainerangebot, Nachricht).
- Er unterscheidet sich vom Telekom-Fall aus Tag 5 und 6, nutzt aber dieselbe Logik. Wer den Churn-Fall verstanden hat, kann ihn hier wiedererkennen.

**Steckbrief (alle Zahlen angenommen):**

| Merkmal | Angaben |
| --- | --- |
| **Unternehmen** | Fitnessstudio-Kette, 12 Studios, regional |
| **Mitglieder** | 24.000 aktive Mitglieder |
| **Beitrag** | 39 € pro Monat, monatlich kündbar nach der Erstlaufzeit |
| **Symptom** | Etwa 30 % der Mitglieder gehen pro Jahr, das sind 7.200 Kündiger; der Umsatz je Studio stagniert trotz Werbung |
| **Daten** | Mitgliedsstammdaten, Check-in am Eingang, Kursbuchungen, Zahlungen, Servicekontakte |
| **Auftrag** | Geschäftsführung: "Wir verlieren zu viele Mitglieder, bevor wir es merken." |

---

## 2. Use Case 1: Sinkende Kundenbindung (ausführlich)

### 2.1 Vom Symptom zur Ursache (5× Warum, Folie 7 und 8)

| Frage | Antwort (Hypothese, an Daten zu prüfen) |
| --- | --- |
| **Symptom** | Mitgliederzahl und Umsatz je Studio stagnieren |
| **1. Warum?** | Es kündigen fast so viele Mitglieder, wie neu eintreten |
| **2. Warum?** | Etwa 30 % kündigen pro Jahr, viele in den ersten Monaten |
| **3. Warum?** | Sie gehen vor der Kündigung immer seltener hin ("Karteileichen") |
| **4. Warum?** | Niemand bemerkt das, solange der Beitrag weiterläuft |
| **5. Warum?** | Es gibt kein System, das nachlassende Nutzung sichtbar macht und eine Reaktion auslöst |
| **Ansatz** | **Kündigungsrisiko je Mitglied vorhersagen, bevor es kündigt** |

Wir stoppen bei einer Ursache, die sich beheben lässt: **zu spätes Erkennen**. Das ist etwas, das ein Modell leisten kann. Die Hypothesen (Nutzungsrückgang vor Kündigung) müssen wir als Erstes in den Daten prüfen.

### 2.2 Use-Case-Steckbrief

| Baustein | VitalPoint Fitness |
| --- | --- |
| **Problem** | Mitglieder kündigen unbemerkt, die Studios reagieren zu spät |
| **Fachfrage** | "Wer kündigt?" |
| **Zielgröße** | **Kündigung (oder Nichtverlängerung) innerhalb von 90 Tagen nach dem Stichtag (ja/nein)**, Prognose am Monatsanfang |
| **Art der Zielgröße** | **Kategorie** (ja/nein), keine Zahl, keine Zeitreihe |
| **Modelltyp** | **Klassifikation mit Score** (Wahrscheinlichkeit 0 bis 1) |
| **Daten** | Besuche pro Woche und deren **Trend**, Vertragsdauer, Tarif, Alter, Kursnutzung, Zahlungsrückstände, Servicekontakte |
| **Handlung** | Ab Schwelle: persönlicher Anruf mit Angebot. Darunter: nur automatische Nachricht |
| **Zuständig** | Studioleitung, Liste jeden Montag |
| **Bewertung** | Quick Win: hoher Nutzen, Daten vorhanden |

**Vage zu messbar** (nach Folie 10):

| Vage | Messbar und eindeutig |
| --- | --- |
| "Bessere Kundenbindung" | Kündigung innerhalb 90 Tage nach Stichtag (ja/nein) |
| "Weniger Kündigungen" | Kündigungsrate je Studio und Quartal in % |
| "Treuere Mitglieder" | Mitglied noch aktiv nach 12 Monaten (ja/nein) |

**Warum Klassifikation?** Die Frage heißt "Wer kündigt?", die Antwort ist ja oder nein. Das passt zur Übersetzungstabelle von Folie 11 ("Wer kündigt?" → Kündigung in 90 Tagen → Klassifikation). Als Startmodell eignet sich die logistische Regression (erklärbar, Koeffizienten lesbar), als Herausforderer Gradient Boosting (siehe Fallstudie TeleCom, Tag 5).

### 2.3 Datenbasis prüfen (nach Folie 12)

Entscheidend ist die Frage: **War die Information zum Prognosezeitpunkt schon bekannt?** Sonst entsteht **Data Leakage**.

| Datenquelle | Vorhanden? | Zum Stichtag bekannt? |
| --- | --- | --- |
| Besuche der letzten Wochen (Check-in) | ja | ja |
| Vertragsdauer, Tarif, Alter | ja | ja |
| Kursbuchungen | ja | ja |
| Zahlungsrückstände | ja | ja |
| **Kündigungsgrund** | ja | **nein, erst nach der Kündigung** |
| **Antrag auf Beitragspause / Kündigungseingang** | ja | **nein, ist schon die Kündigung** |

Die beiden letzten Zeilen dürfen **nicht** als Merkmal ins Modell. Sie wären nach der Kündigung bekannt und würden das Ergebnis sonst künstlich perfekt machen.

### 2.4 Vom Modell zur Wirkung (Folie 13 und 14)

| Mitglied | Score | Aktion |
| --- | ---: | --- |
| Mitglied A | 0,62 | Persönlicher Anruf der Studioleitung mit Angebot (z. B. kostenloses Trainer-Gespräch) |
| Mitglied B | 0,41 | Persönlicher Anruf, falls Kapazität; sonst automatische Nachricht |
| Mitglied C | 0,12 | Keine Aktion |
| **Zuständig** | | Studioleitung, Liste jeden Montag um 10 Uhr |

Die Kette lautet **Prognose → Empfehlung → Handlung → Wirkung**. Gemessen wird die Wirkung an der **Kündigungsrate der angerufenen Mitglieder** im Vergleich zu einer **Kontrollgruppe** ohne Anruf.

### 2.5 Welche Schwelle lohnt sich? (Folie 19 bis 21)

**Die Schwelle folgt aus den Kosten, nicht aus der Accuracy.** Wir verwenden dieselbe Regel wie in Tag 6: *Kontakt lohnt sich, wenn p · q · W > K.*

| Größe | Bedeutung | Wert (Annahme) |
| --- | --- | ---: |
| **p** | **Kündigungsrisiko des Mitglieds**: die vom Modell berechnete Wahrscheinlichkeit (Score von 0 bis 1), dass genau dieses Mitglied in den nächsten 90 Tagen kündigt. Sie ist **je Mitglied verschieden** und die einzige Größe, die das Modell liefert. | z. B. 0,62 (62 %) |
| **K** | Kosten je Kontakt (Anrufzeit, Angebot) | 40 € |
| **q** | Anteil der angerufenen Kündiger, die wir halten | 25 % |
| **W** | Erlös je gehaltenem Mitglied (12 Monate · 39 €) | 468 € |

Der Nutzen je gehaltenem Mitglied ist q · W = 0,25 · 468 € = **117 €**. Die Schwelle ist

> p > K / (q · W) = 40 € / 117 € ≈ **34 %**

*Dabei ist p das Kündigungsrisiko des einzelnen Mitglieds laut Modell, die Schwelle (34 %) ist der Wert, ab dem wir anrufen. K, q und W sind für alle Mitglieder gleich, nur p unterscheidet sich.*

Ab einem Risiko von etwa 34 % lohnt sich der Anruf. Das ist **mehr als die Basisrate von 30 %**: Wer einfach alle anruft, verliert Geld.

**Die Formel: Wert = TP · (q · W − K) − FP · K**

Sie sagt: *Gesamtnutzen = Gewinn aus den richtigen Anrufen − Kosten der Fehlanrufe.* Sie entsteht, wenn man für jedes Feld der Confusion Matrix (siehe Tag 6) fragt, was der Anruf **kostet und bringt**:

| Feld | Was passiert | Kosten | Gewinn | Ergebnis je Mitglied |
| --- | --- | ---: | ---: | ---: |
| **TP** | Wir rufen an, das Mitglied wollte wirklich kündigen. Mit Wahrscheinlichkeit q halten wir es. | K = 40 € | q · W = 117 € (erwartet) | **q · W − K = +77 €** |
| **FP** | Wir rufen an, aber das Mitglied wäre geblieben. Der Anruf bringt nichts, denn der Beitrag wäre ohnehin gezahlt worden. | K = 40 € | 0 € | **−K = −40 €** |
| **FN** | Wir rufen nicht an, das Mitglied kündigt. | 0 € | 0 € | **0 €** (entgangene Chance, aber keine Ausgabe) |
| **TN** | Wir rufen nicht an, das Mitglied bleibt. | 0 € | 0 € | **0 €** |

Nur Anrufe verursachen Kosten, deshalb zählen nur **TP und FP**. FN und TN bringen 0 €. Die Formel ist also einfach **TP mal Gewinn je TP plus FP mal Verlust je FP**.

Die Bausteine einzeln:

- **q · W = 0,25 · 468 € = 117 €:** Wir halten nur 25 % der Angerufenen (q). Der Erlös je gehaltenem Mitglied ist 468 € (W). Im Durchschnitt bringt ein Anruf bei einem echten Kündiger also 117 €.
- **− K:** Den Anruf zahlen wir **immer**, auch bei den 75 %, die wir nicht halten. Deshalb steht K in der Klammer: 117 € − 40 € = **77 € im Mittel je TP**.
- **− FP · K:** Jeder Fehlanruf kostet 40 € und bringt nichts.

*Probe an 100 Treffern (TP):* 25 werden gehalten (25 · 468 € = 11.700 €), aber alle 100 Anrufe kosten 4.000 €. Ergebnis: 11.700 € − 4.000 € = 7.700 € = 100 · 77 €. ✓

**Zusammenhang mit der Schwelle von 34 %:** Ruft man ein Mitglied mit Risiko p an, ist es mit Wahrscheinlichkeit p ein TP (+77 €) und mit Wahrscheinlichkeit 1 − p ein FP (−40 €). Der erwartete Wert je Anruf ist

> p · (q · W − K) − (1 − p) · K = p · q · W − K

Er ist größer als 0 genau dann, wenn **p · q · W > K**, also p > K / (q · W) = 40 / 117 ≈ 34 % (p = Kündigungsrisiko des Mitglieds laut Modell). Die Schwelle ist damit **dieselbe Formel**, nur für ein einzelnes Mitglied gerechnet. Die Jahresrechnung unten summiert sie für alle Mitglieder.

**Jahresrechnung** (Wert = TP · (q · W − K) − FP · K), Annahmen: 24.000 Mitglieder, davon 7.200 Kündiger und 16.800 Bleiber im Jahr.

| Variante | Anrufe | Treffer (TP) | Fehlanrufe (FP) | Nutzen pro Jahr |
| --- | ---: | ---: | ---: | ---: |
| **Kein Modell** (keiner angerufen) | 0 | 0 | 0 | 0 € |
| **Alle anrufen** | 24.000 | 7.200 | 16.800 | 7.200 · 77 − 16.800 · 40 = **−117.600 €** |
| **Modell**, Zielwerte Recall 60 %, Precision 60 % | 7.200 | 4.320 | 2.880 | 4.320 · 77 − 2.880 · 40 = **+217.440 €** |

Dabei ist q · W − K = 117 € − 40 € = 77 € der Gewinn je angerufenem Kündiger.

Daraus folgt:

- Ohne Modell ist der Anruf **zu teuer**, mit Modell **lohnt er sich**. Das ist der Wert der Vorhersage.
- **Kapazität:** 7.200 Anrufe im Jahr sind 600 im Monat, also etwa **50 je Studio und Monat** (rund 12 pro Woche). Das ist machbar.
- Die Modellwerte (Recall 60 %, Precision 60 %) sind **Zielwerte für den Pilot**, kein Ergebnis. Sie sind erst nach dem Training auf einem Testdatensatz belegt.
- **Nicht eingerechnet** sind gesparte Werbekosten für Ersatzmitglieder. Der echte Nutzen ist eher höher.

### 2.6 Bewertung (Folie 15 bis 18)

| Achse | Einschätzung |
| --- | --- |
| **Business Impact** | **hoch**: etwa 217 T€ pro Jahr nach Annahmen, direkter Bezug zum Umsatz |
| **Umsetzbarkeit** | **gut**: Check-in-Daten und Vertragsdaten sind vorhanden, Aktion ist einfach |
| **Einordnung** | **Quick Win** (hoher Impact, gut umsetzbar) |

### 2.7 Risiken und Stakeholder (Folie 21, 24 bis 27)

| Thema | Risiko | Maßnahme |
| --- | --- | --- |
| **Fehlalarme** | Anruf bei Mitgliedern, die gar nicht kündigen wollten, kostet 40 € und kann lästig sein | Schwelle aus Kosten ableiten, Anruf freundlich formulieren |
| **"Schlafende Hunde"** | Der Anruf erinnert jemanden an die Kündigung, der sonst weiter gezahlt hätte | **Kontrollgruppe** im Pilot, Wirkung messen statt annehmen |
| **Liste kommt zu spät** | wie beim Versicherer (Folie 30): Prognose nach der Kündigung nützt nichts | Prognose **vor** der Kündigungsfrist, Liste jeden Montag |
| **Datenschutz** | Check-in-Daten sind personenbezogen | Rechtsgrundlage prüfen, nur nötige Daten, **keine Gesundheitsdaten** nutzen |
| **Akzeptanz** | Studioleitungen vertrauen der Liste nicht | früh einbinden, Pilot in 2 bis 3 Studios, realistische Genauigkeit kommunizieren |
| **Verantwortung** | Wer verantwortet Modell und Wirkung? | Eine Person im Mitgliederservice, Fehlentscheidungen werden gemeldet |

**Stakeholder:** Geschäftsführung (entscheidet), Studioleitung (setzt um), Trainer (erleben die Gespräche), Mitglieder (Betroffene), Datenschutz.

### 2.8 Checkliste (Folie 28)

| Frage | Antwort |
| --- | --- |
| Ist das Geschäftsproblem klar? | ja: Kündigungen werden zu spät bemerkt |
| Ist die Zielgröße messbar? | ja: Kündigung in 90 Tagen (ja/nein) |
| Sind die Daten verfügbar? | ja, zum Stichtag bekannt (ohne Kündigungsgrund) |
| Ist die Handlung definiert? | ja: Anruf ab 34 %, Studioleitung, montags |

---

## 3. Use Case 2: Hohe Lagerkosten

> Für Problem 2 und 3 reicht dieselbe Struktur, aber knapper. Auch diese Fälle sind **Entwürfe mit Annahmen**.

| Baustein | Lösung |
| --- | --- |
| **Frage hinter dem Problem** | Warum liegt zu viel Ware im Lager? Weil niemand weiß, **wie viel wir wann verkaufen**, und deshalb vorsichtshalber zu viel bestellt wird. |
| **Use Case** | Absatz je Artikel und Woche vorhersagen und die Bestellmenge daran ausrichten |
| **Zielgröße** | **Absatzmenge je Artikel und Filiale pro Woche (Stück), vier Wochen im Voraus** |
| **Art der Zielgröße** | **Zahl**, mit **Entwicklung über Zeit** (Saison, Trend) |
| **Modelltyp** | **Regression bzw. Zeitreihenprognose** |
| **Daten** | Verkaufshistorie, Preise und Aktionen, Feiertage, Saison, Lagerbestand |
| **Handlung** | Bestellmenge = Prognose + Sicherheitsbestand − aktueller Bestand |
| **Metrik** | Fehler in Stück (z. B. MAE), dazu Fehlerkosten: Überbestand kostet Lagerkosten, Fehlbestand kostet Umsatz |
| **Besonderheit** | Die Fehler sind **asymmetrisch**: je nach Ware ist zu wenig oder zu viel teurer |
| **Bewertung** | Impact hoch, Umsetzbarkeit gut, wenn die Verkaufsdaten sauber sind |

Das ist derselbe Typ Aufgabe wie das Favorita-Projekt aus Tag 2 (Absatz je Filiale und Tag).

---

## 4. Use Case 3: Unklare Marketingwirkung

| Baustein | Lösung |
| --- | --- |
| **Frage hinter dem Problem** | Welche Kampagne bringt **zusätzlichen** Umsatz, und welche erreicht nur Kunden, die ohnehin gekauft hätten? |
| **Use Case** | Wirkung einer Kampagne je Kunde schätzen und nur Kunden ansprechen, bei denen sie etwas bewirkt |
| **Zielgröße** | **Kauf innerhalb von 14 Tagen nach Kampagne (ja/nein)**, getrennt für **angesprochene und nicht angesprochene** Kunden. Die Wirkung ist der Unterschied. |
| **Art der Zielgröße** | **Kategorie** (ja/nein), aber als **Unterschied zweier Gruppen** |
| **Modelltyp** | **Klassifikation mit Kontrollgruppe** (Uplift-Modell). Ist die Wirkung je Woche gesucht: **Regression über Zeit** (Marketing-Mix-Modell). |
| **Daten** | Kampagnenkontakt, Kaufhistorie, **zufällig gebildete Kontrollgruppe** |
| **Handlung** | Budget auf Kampagnen und Kunden verlagern, die nachweislich zusätzliche Käufe bringen |
| **Besonderheit** | Ohne Kontrollgruppe sieht man nur **Korrelation**: Wer die Aktion erhielt und kaufte, hätte vielleicht ohnehin gekauft |
| **Bewertung** | Impact mittel bis hoch, Umsetzbarkeit **mittel** (braucht saubere Tests) |

Ein reines "Wer kauft?"-Modell würde die Wirkung **überschätzen**, weil es auch die Kunden zählt, die ohne Kampagne gekauft hätten. Deshalb ist die Kontrollgruppe hier Pflicht.

---

## 5. Überblick: Drei Probleme, drei Use Cases

| | **Kundenbindung** | **Lagerkosten** | **Marketingwirkung** |
| --- | --- | --- | --- |
| **Frage** | Wer kündigt? | Wie viel Absatz kommt? | Was bewirkt die Kampagne? |
| **Zielgröße** | Kündigung in 90 Tagen (ja/nein) | Absatz je Artikel und Woche (Stück) | Kauf in 14 Tagen (ja/nein), mit und ohne Kampagne |
| **Art** | Kategorie | Zahl über Zeit | Kategorie, Unterschied zweier Gruppen |
| **Modelltyp** | Klassifikation | Regression / Zeitreihe | Klassifikation mit Kontrollgruppe (Uplift) |
| **Handlung** | Anruf ab Schwelle | Bestellmenge anpassen | Budget umverteilen |
| **Haupt-Risiko** | Fehlalarme, "schlafende Hunde" | Fehlbestand und Überbestand | Korrelation statt Wirkung |

---

## Kernaussagen Arbeitsauftrag 1

1. **Das Problem ist nur das Symptom.** Mit 5× Warum kommt man zur Ursache, an der der Use Case ansetzt.
2. **Die Zielgröße muss messbar und eindeutig sein**, inklusive Zeitfenster ("Kündigung in 90 Tagen"), nicht "bessere Kundenbindung".
3. **Die Zielgröße bestimmt den Modelltyp:** ja/nein → Klassifikation, Zahl → Regression, Verlauf → Zeitreihe.
4. **Ein Use Case endet nicht beim Modell**, sondern bei einer Handlung mit Zuständigem und Zeitpunkt.
5. **Die Schwelle kommt aus den Kosten:** p > K / (q · W). Ohne Modell lohnt sich der Anruf nicht, mit Modell schon.
6. **Nur Daten nutzen, die zum Prognosezeitpunkt bekannt sind** (Data Leakage vermeiden).

---

## Wo könnten Antworten bei Arbeitsauftrag 1 abweichen?

- Andere Branchen sind genauso passend (Telekom, Versicherung, Online-Shop). Entscheidend ist, dass Zielgröße, Daten und Handlung zusammenpassen.
- Andere Zeitfenster (60 oder 180 Tage) sind möglich. Das Fenster muss zur **Reaktionszeit** passen: Bis zur Kündigungsfrist muss genug Zeit für die Aktion bleiben.
- Bei Problem 3 kann man auch einfacher sagen "Umsatz je Kunde (Regression)". Das ist zulässig, misst aber nicht die **zusätzliche** Wirkung.
- Die Kosten und Quoten (K = 40 €, q = 25 %, 30 % Kündigung) sind **Annahmen**. Mit anderen Werten verschiebt sich die Schwelle, das Vorgehen bleibt gleich.

---

# Arbeitsauftrag 2: Fehlermaße der Regression (MAE, RMSE, MAPE)

**Aufgabe (Folie "UE 3 · Arbeitsauftrag 2"):**

- **Teil 1, Berechnen:** Für zwei Modelle (A und B) je Zeile |Fehler| und Fehler² eintragen und daraus **MAE** und **RMSE** berechnen.
- **Teil 2, Analysieren:** MAE und RMSE vergleichen. Wo liegen sie nah beieinander, wo weit auseinander, und **warum**?

Beide Tabellen enthalten 10 Vorhersagen. Modell A hat laut Folie "gleichmäßige Fehler", Modell B "einen großen Ausreißer". Wir ergänzen zusätzlich **MAPE** und weitere Regressionsmaße (Abschnitt 8).

## 6. Notation und Formeln

### 6.1 Legende der Zeichen

| Zeichen | Lesart | Bedeutung |
| --- | --- | --- |
| **n** | "n" | Anzahl der Beobachtungen, hier **n = 10** |
| **i** | "i" | Laufnummer der Zeile, **i = 1 bis n** |
| **yᵢ** | "y i" | **Ist-Wert** (tatsächlicher Wert) der Zeile i. Die Einzelwerte heißen **y₁, y₂, …, yₙ** |
| **ŷᵢ** | "y-Dach i" (englisch *y hat*) | **Vorhersage** des Modells für Zeile i. Das **Dach** (^) bedeutet immer **"geschätzt/vorhergesagt"**, ohne Dach steht der echte Wert. Die Einzelwerte heißen **ŷ₁, ŷ₂, …, ŷₙ** |
| **eᵢ** | "e i" | **Fehler** (englisch *error*, auch *Residuum*) der Zeile i: **eᵢ = yᵢ − ŷᵢ** |
| **\|eᵢ\|** | "Betrag von e i" | **Absoluter Fehler**: das Vorzeichen wird weggelassen, nur die Größe zählt |
| **eᵢ²** | "e i Quadrat" | **Quadrierter Fehler** |
| **Σ** | "Summe" | Alles von i = 1 bis n aufaddieren |
| **ȳ** | "y-quer" | **Mittelwert** der Ist-Werte: ȳ = (1/n) · Σ yᵢ |

**Vorzeichen:** Hier ist eᵢ = Ist − Vorhersage. **eᵢ > 0** heißt, das Modell hat **zu niedrig** geschätzt, **eᵢ < 0** heißt **zu hoch**. Manche Bücher rechnen Vorhersage − Ist, dann dreht sich das Vorzeichen um. Für MAE, RMSE und MAPE ist das egal, weil dort Betrag oder Quadrat steht.

**Beispiel Zeile 1 in Modell A:** y₁ = 100, ŷ₁ = 98, also e₁ = 100 − 98 = 2, \|e₁\| = 2, e₁² = 4.

### 6.2 Die Formeln

```
MAE  = (1/n) · Σ |y − ŷ|
MSE  = (1/n) · Σ (y − ŷ)²
RMSE = √[(1/n) · Σ (y − ŷ)²]
MAPE = (100/n) · Σ |(y − ŷ) / y|
```

(`Σ` = Summe über alle Zeilen, `|…|` = Betrag, `ŷ` = "y-Dach" = Vorhersage. Wie in der Legende steht in jeder Summe `y` für yᵢ, `ŷ` für ŷᵢ und i läuft von 1 bis n.)

| Maß | In Worten |
| --- | --- |
| **MAE** (Mean Absolute Error) | **Mittelwert** der Beträge der Fehler |
| **MSE** (Mean Squared Error) | Mittelwert der **quadrierten** Fehler |
| **RMSE** (Root Mean Squared Error) | **Wurzel** aus dem MSE, damit wieder in der **Einheit** der Daten |
| **MAPE** (Mean Absolute Percentage Error) | mittlerer **prozentualer** Fehler, bezogen auf den Ist-Wert |

**Warum die Wurzel beim RMSE?** Quadrierte Fehler haben die Einheit "Euro²" bzw. "Stück²". Die Wurzel bringt sie zurück auf "Euro" bzw. "Stück", sodass man sie mit dem MAE vergleichen kann.

---

## 7. Teil 1: Berechnen

### 7.1 Modell A ("gleichmäßige Fehler")

| i | Ist-Wert yᵢ | Vorhersage ŷᵢ | Fehler eᵢ = yᵢ − ŷᵢ | \|eᵢ\| | eᵢ² | \|eᵢ\| / yᵢ |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | 100 | 98 | 100 − 98 = 2 | 2 | 2² = 4 | 2 / 100 = 2,00 % |
| 2 | 120 | 122 | 120 − 122 = −2 | 2 | 2² = 4 | 2 / 120 = 1,67 % |
| 3 | 95 | 92 | 95 − 92 = 3 | 3 | 3² = 9 | 3 / 95 = 3,16 % |
| 4 | 110 | 113 | 110 − 113 = −3 | 3 | 3² = 9 | 3 / 110 = 2,73 % |
| 5 | 130 | 128 | 130 − 128 = 2 | 2 | 2² = 4 | 2 / 130 = 1,54 % |
| 6 | 105 | 107 | 105 − 107 = −2 | 2 | 2² = 4 | 2 / 105 = 1,90 % |
| 7 | 88 | 85 | 88 − 85 = 3 | 3 | 3² = 9 | 3 / 88 = 3,41 % |
| 8 | 115 | 118 | 115 − 118 = −3 | 3 | 3² = 9 | 3 / 115 = 2,61 % |
| 9 | 122 | 120 | 122 − 120 = 2 | 2 | 2² = 4 | 2 / 122 = 1,64 % |
| 10 | 99 | 101 | 99 − 101 = −2 | 2 | 2² = 4 | 2 / 99 = 2,02 % |
| **Σ** | | | **Σ eᵢ = 0** | **Σ \|eᵢ\| = 24** | **Σ eᵢ² = 60** | **Σ = 22,67 %** |
| **Ergebnis** | | | **ME = 0 / 10 = 0,0** | **MAE = 24 / 10 = 2,40** | **MSE = 60 / 10 = 6,0**, **RMSE = √6,0 = 2,45** | **MAPE = 22,67 % / 10 = 2,27 %** |

**Ergebnis Modell A: MAE = 2,40 und RMSE ≈ 2,45.**

### 7.2 Modell B ("ein großer Ausreißer")

| i | Ist-Wert yᵢ | Vorhersage ŷᵢ | Fehler eᵢ = yᵢ − ŷᵢ | \|eᵢ\| | eᵢ² | \|eᵢ\| / yᵢ |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | 50 | 51 | 50 − 51 = −1 | 1 | 1² = 1 | 1 / 50 = 2,00 % |
| 2 | 62 | 61 | 62 − 61 = 1 | 1 | 1² = 1 | 1 / 62 = 1,61 % |
| 3 | 48 | 49 | 48 − 49 = −1 | 1 | 1² = 1 | 1 / 48 = 2,08 % |
| 4 | 55 | 54 | 55 − 54 = 1 | 1 | 1² = 1 | 1 / 55 = 1,82 % |
| 5 | 70 | 71 | 70 − 71 = −1 | 1 | 1² = 1 | 1 / 70 = 1,43 % |
| 6 | 44 | 43 | 44 − 43 = 1 | 1 | 1² = 1 | 1 / 44 = 2,27 % |
| 7 | 58 | 59 | 58 − 59 = −1 | 1 | 1² = 1 | 1 / 58 = 1,72 % |
| 8 | 66 | 65 | 66 − 65 = 1 | 1 | 1² = 1 | 1 / 66 = 1,52 % |
| 9 | 52 | 67 | 52 − 67 = −15 | 15 | 15² = 225 | 15 / 52 = 28,85 % |
| 10 | 60 | 45 | 60 − 45 = 15 | 15 | 15² = 225 | 15 / 60 = 25,00 % |
| **Σ** | | | **Σ eᵢ = 0** | **Σ \|eᵢ\| = 38** | **Σ eᵢ² = 458** | **Σ = 68,30 %** |
| **Ergebnis** | | | **ME = 0 / 10 = 0,0** | **MAE = 38 / 10 = 3,80** | **MSE = 458 / 10 = 45,8**, **RMSE = √45,8 = 6,77** | **MAPE = 68,30 % / 10 = 6,83 %** |

**Ergebnis Modell B: MAE = 3,80 und RMSE ≈ 6,77.**

**Hinweis zu Modell B:** Auf der Folie heißt es "ein großer Ausreißer". In den Daten sind es genau genommen **zwei Zeilen** mit einem Fehler von 15 (Zeile 9: zu hoch geschätzt, Zeile 10: zu niedrig geschätzt). Alle anderen acht Fehler sind nur 1. Gemeint ist ein "großer Fehlertyp", der in zwei Zeilen auftritt.

**Rechenweg im Überblick:**

| | Modell A | Modell B |
| --- | ---: | ---: |
| Σ \|eᵢ\| | 24 | 38 |
| MAE = Σ \|eᵢ\| / 10 | **2,40** | **3,80** |
| Σ eᵢ² | 60 | 458 |
| MSE = Σ eᵢ² / 10 | 6,0 | 45,8 |
| RMSE = √MSE | **2,45** | **6,77** |

---

## 8. Weitere Regressionsmaße: Was lohnt sich?

Nur MAE und RMSE zu betrachten ist wie ein Auto nur nach dem Verbrauch zu beurteilen. Je nach Frage sind andere Maße besser. Hier die wichtigsten, mit den Werten aus unseren zwei Tabellen:

| Maß | Formel | Modell A | Modell B | Wann nützlich? |
| --- | --- | ---: | ---: | --- |
| **MAE** | (1/n) · Σ \|eᵢ\| | 2,40 | 3,80 | Typischer Fehler in der **Einheit** der Daten, robust gegen Ausreißer |
| **RMSE** | √[(1/n) · Σ eᵢ²] | 2,45 | 6,77 | Wenn **große Fehler besonders teuer** sind |
| **MAPE** | (100/n) · Σ \|eᵢ\| / \|yᵢ\| | 2,27 % | 6,83 % | Fehler **in Prozent**, vergleichbar zwischen **Datensätzen mit verschiedener Größenordnung** |
| **WAPE** (gewichteter MAPE) | Σ \|eᵢ\| / Σ \|yᵢ\| | 2,21 % | 6,73 % | Wie MAPE, aber **stabil bei kleinen oder null Ist-Werten** (gebräuchlich in der Absatzplanung) |
| **sMAPE** (symmetrischer MAPE) | (100/n) · Σ 2·\|eᵢ\| / (\|yᵢ\| + \|ŷᵢ\|) | 2,27 % | 6,82 % | Wenn zu hohe und zu niedrige Schätzungen **gleich behandelt** werden sollen |
| **ME** (Mean Error, **Bias**) | (1/n) · Σ eᵢ | 0,0 | 0,0 | Ist das Modell **systematisch** zu hoch oder zu niedrig? |
| **MedAE** (Median des absoluten Fehlers) | Median von \|eᵢ\| | 2 | 1 | **Typischer** Fehler, unempfindlich gegen Ausreißer |
| **Max. Fehler** | max \|eᵢ\| | 3 | 15 | **Schlimmster Einzelfall** |
| **R²** (Bestimmtheitsmaß) | 1 − SS_res / SS_tot | 0,96 | 0,25 | Welchen **Anteil der Schwankung** der Ist-Werte erklärt das Modell? (1 = alles, 0 = nicht besser als der Mittelwert) |

**Zu den Rechnungen:**

- **WAPE:** Modell A: Σ\|yᵢ\| = 1.084, also 24 / 1.084 = 2,21 %. Modell B: Σ\|yᵢ\| = 565, also 38 / 565 = 6,73 %.
- **R²:** SS_res = Σ eᵢ² (Summe der quadrierten Fehler) und SS_tot = Σ (yᵢ − ȳ)² (Summe der quadrierten Abweichungen vom Mittelwert). Modell A: ȳ = 108,4, Σ(yᵢ − ȳ)² = 1.598,4, also R² = 1 − 60 / 1.598,4 = 0,96. Modell B: ȳ = 56,5, Σ(yᵢ − ȳ)² = 610,5, also R² = 1 − 458 / 610,5 = 0,25.
- **ME = 0** in beiden Fällen: Die Fehler sind je zur Hälfte positiv und negativ und heben sich auf. Deshalb nimmt man für die Fehlergröße **nie** den einfachen Mittelwert der Fehler, sondern Betrag oder Quadrat. Der ME ist trotzdem sinnvoll, um **systematische Verzerrung** zu erkennen.

### 8.1 MAPE: Stärken und Fallen

**Stärke:** Der Fehler steht in Prozent. Modell A (Werte um 108) und Modell B (Werte um 57) haben verschiedene Größenordnungen, MAE 2,40 und 3,80 sind deshalb **nicht direkt vergleichbar**. Nach MAPE ist Modell A mit 2,27 % deutlich besser als Modell B mit 6,83 %.

**Fallen:**

| Falle | Erklärung |
| --- | --- |
| **Ist-Wert 0** | Division durch 0, MAPE ist nicht definiert. Bei Absatz mit Tagen ohne Verkauf ein echtes Problem. |
| **Kleine Ist-Werte** | Ein kleiner Fehler bei einem kleinen Wert wird zu einem riesigen Prozentwert und dominiert den Durchschnitt. |
| **Asymmetrie** | Zu niedrige Schätzungen sind auf höchstens 100 % begrenzt, zu hohe können beliebig groß werden. MAPE bestraft daher "zu hoch" stärker. |
| **Kein Bezug zu Kosten** | 10 % Fehler bei einem 1-€-Artikel und bei einem 1.000-€-Artikel zählen gleich. |

**Gegenmittel:** WAPE (Summen statt Einzelquotienten) oder sMAPE.

### 8.2 Welche Maße sind sinnvoll? Empfehlung

| Frage | Maß |
| --- | --- |
| Wie groß ist der **typische** Fehler in der Einheit? | **MAE** (dazu MedAE) |
| Sind **große Ausreißer** besonders teuer? | **RMSE** |
| **Verschiedene Datensätze** oder Größenordnungen vergleichen? | **MAPE oder WAPE**, bei Nullen **WAPE** |
| **Systematisch** zu hoch oder zu niedrig? | **ME (Bias)** |
| Wie viel der Schwankung wird erklärt? | **R²** (Faustregel zum Gesamtbild) |

Praktisch zeigt man **mehrere Maße zusammen**, mindestens **MAE, RMSE und MAPE**. **Zusätzlich:** Bei Prognosen mit unterschiedlichen Kosten für "zu viel" und "zu wenig" (z. B. Lager, Abschnitt 3) nutzt man **asymmetrische Verlustfunktionen**, etwa den Quantil- bzw. *Pinball*-Verlust. Das ist der Hintergrund des Notebooks `09_quantile` im Favorita-Projekt.

---

## 9. Teil 2: Analysieren

### 9.1 MAE und RMSE im Vergleich

| | MAE | RMSE | RMSE / MAE |
| --- | ---: | ---: | ---: |
| **Modell A** | 2,40 | 2,45 | **1,02** |
| **Modell B** | 3,80 | 6,77 | **1,78** |

- **Nah beieinander: Modell A.** MAE 2,40 und RMSE 2,45 unterscheiden sich kaum, das Verhältnis ist 1,02.
- **Weit auseinander: Modell B.** MAE 3,80, aber RMSE 6,77. Der RMSE ist fast **doppelt** so groß wie der MAE (Verhältnis 1,78).

### 9.2 Warum entsteht dieser Unterschied?

**1. Der RMSE quadriert, bevor er mittelt.** Dadurch zählen große Fehler **überproportional**. Der MAE gewichtet jeden Fehler **linear**.

| Fehlergröße | Beitrag zum MAE (\|e\|) | Beitrag zum RMSE (e²) |
| ---: | ---: | ---: |
| 1 | 1 | 1 |
| 3 | 3 | 9 |
| 15 | 15 | **225** |

Ein Fehler von 15 ist **15-mal** so groß wie einer von 1, geht aber **225-mal** (also 15²) in die Summe ein.

**2. Modell A:** Alle Fehler sind **2 oder 3**. Sie liegen eng beieinander, es gibt keinen Ausreißer. Dann ändert das Quadrieren fast nichts am Mittelwert: **MAE ≈ RMSE**.

**3. Modell B:** Acht Fehler sind **1**, zwei Fehler sind **15**. Die zwei großen Fehler tragen

- zum MAE: 30 von 38, also **79 %** der Summe,
- zum RMSE: 450 von 458, also **98 %** der Summe.

Im quadratischen Maß **dominieren** die zwei Ausreißer fast vollständig. Der RMSE macht sie sichtbar, der MAE glättet sie weg.

**Probe:** Ohne die Zeilen 9 und 10 hätte Modell B MAE = 1,00 **und** RMSE = 1,00. Der gesamte Abstand zwischen den beiden Maßen kommt von diesen zwei Zeilen.

**4. Mathematische Regel:** Es gilt immer **RMSE ≥ MAE**. Beide sind genau dann **gleich**, wenn **alle** absoluten Fehler gleich groß sind. Je ungleicher die Fehler, desto größer das Verhältnis RMSE / MAE. Es kann höchstens √n erreichen (hier √10 ≈ 3,16), das wäre der Fall, wenn der **ganze** Fehler in einer einzigen Zeile steckt.

> **Faustregel:** RMSE ≈ MAE → Fehler **gleichmäßig**. RMSE deutlich größer als MAE → **einzelne große Ausreißer**.

### 9.3 Was heißt das für die Bewertung?

| Beobachtung | Aussage |
| --- | --- |
| **Typischer Fehler** | Modell B ist mit einem Median-Fehler von **1** (Modell A: 2) in den meisten Fällen **genauer** |
| **Schlimmster Fehler** | Modell B hat zwei Aussetzer mit **15**, Modell A höchstens 3 |
| **MAPE zeigt es auch** | Die Zeilen 9 und 10 haben je 28,85 % und 25,00 %, alle anderen unter 2,3 % |
| **R²** | Modell A erklärt 96 % der Schwankung, Modell B nur 25 %. Die zwei Aussetzer verderben das Bild |

**Welches Modell ist "besser"?** Das hängt von den **Fehlerkosten** ab (siehe Tag 6 und Abschnitt 2.5):

- Sind **seltene große Fehler teuer** (z. B. Lagerbestand, Brandmelder, Liquiditätsplanung), ist **RMSE** das passende Maß, und **Modell A** ist vorzuziehen.
- Zählt vor allem der **typische Fall** und sind Ausreißer verkraftbar, passt der **MAE** besser. Modell B hat zwar den kleineren Median-Fehler, liegt aber im MAE mit 3,80 gegen 2,40 trotzdem hinter Modell A.
- **Vergleichbarkeit:** A und B haben **verschiedene Wertebereiche** (um 108 gegen um 57). Für den fairen Vergleich über beide Tabellen nimmt man **MAPE oder WAPE**: A 2,27 % gegen B 6,83 %.

**Nächster Schritt bei Modell B:** Die Ausreißer **untersuchen**. Gibt es eine Besonderheit (Aktion, Feiertag, Messfehler, fehlendes Merkmal)? Liegt eine Ursache vor, kann das Modell oft verbessert werden, und dann wird der RMSE sofort viel kleiner.

---

## Kernaussagen Arbeitsauftrag 2

1. **Notation:** yᵢ = Ist-Wert, ŷᵢ = Vorhersage (das Dach bedeutet "geschätzt"), eᵢ = yᵢ − ŷᵢ = Fehler.
2. **MAE** mittelt die **Beträge**, **RMSE** mittelt die **Quadrate** und zieht dann die Wurzel, **MAPE** setzt den Fehler **in Prozent** zum Ist-Wert.
3. **RMSE ≥ MAE** gilt immer. Ein **großes Verhältnis RMSE / MAE** verrät **Ausreißer**.
4. **Modell A:** MAE 2,40 und RMSE 2,45, gleichmäßige Fehler. **Modell B:** MAE 3,80 und RMSE 6,77, zwei große Fehler dominieren den RMSE (98 % der Quadratsumme).
5. **Das Maß folgt den Kosten:** Sind große Fehler teuer, nimmt man RMSE, sonst MAE. Für Vergleiche über Größenordnungen MAPE oder WAPE.
6. Mehrere Maße **zusammen** zeigen: **MAE, RMSE, MAPE** und bei Bedarf **ME, MedAE, Max. Fehler, R²**.

---

*Hinweis zu Arbeitsauftrag 2: Alle Rechnungen wurden mit Python nachgerechnet (Summen, MAE, MSE, RMSE, MAPE, WAPE, sMAPE, ME, Median, R²). Die Darstellung der Formeln als Text ist so gewählt, dass sie in jedem Markdown-Viewer lesbar bleibt.*

---

*Hinweis zur Entstehung (Arbeitsauftrag 1): Entwurf auf Basis der Folien UE 1 und UE 2 zu Use-Case-Design. VitalPoint Fitness und alle Zahlen sind frei erfunden. Die Definition der Kundenbindung stützt sich auf allgemeine Marketing-Begriffe, nicht auf die Folien.*
