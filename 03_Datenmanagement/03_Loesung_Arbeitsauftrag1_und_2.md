# Lösungsentwurf: Arbeitsauftrag 1 und 2 (Datenmanagement)

Bezug: UE 1 (Wissensvermittlung), UE 2 (Arbeitsauftrag 1), UE 3 (Arbeitsauftrag 2)

---

# Teil 1 – Arbeitsauftrag 1: Predictive Maintenance einführen

**Szenario:** Ein Produktionsunternehmen will Predictive Maintenance einführen. Sensordaten aus Maschinen werden bereits erfasst, Wartungsprotokolle liegen teilweise unvollständig vor, und es gibt Excel-Listen aus verschiedenen Abteilungen mit unterschiedlichen Zeitstempeln. Wir sind das Datenmanagement-Team.

## 1. Relevante Datenquellen identifizieren

Predictive Maintenance sagt voraus, wann eine Maschine ausfällt, bevor es passiert. Dafür braucht man Zustandsdaten (was misst die Maschine?), Ereignisdaten (was ist passiert und was wurde repariert?) und Kontextdaten (welche Maschine, welche Belastung?). Nach UE 1 lassen sich die Quellen in ***intern***e und ***externe***   sowie in ***Stamm-*** und ***Bewegungsdaten*** einteilen.

| # | Datenquelle | Art (UE 1) | Inhalt / Nutzen für Predictive Maintenance | Status im Szenario |
|---|---|---|---|---|
| 1 | **Sensordaten der Maschinen** (Temperatur, Vibration, Druck, Strom, Drehzahl) | intern, Bewegungsdaten, strukturiert | Kernfeature für Zustandsüberwachung und Anomalieerkennung | erfasst |
| 2 | **Wartungsprotokolle** (Datum, Maßnahme, Ersatzteil, Dauer) | intern, Bewegungsdaten, teils unstrukturiert (Freitext) | Quelle für das Zielereignis: Wann wurde repariert? Ohne Labels kein Training | teils unvollständig |
| 3 | **Störungs-/Ausfallmeldungen** (Stillstandsprotokolle, Tickets, MES/Leitstand) | intern, Bewegungsdaten | Die tatsächlichen Ausfälle samt Ursache und Dauer, das eigentliche Prognoseziel | nicht genannt, vermutlich in Excel |
| 4 | **Maschinenstammdaten** (Typ, Baujahr, Hersteller, Standort, Komponenten) | intern, Stammdaten (ERP/Anlagenverwaltung) | Vergleichbarkeit von Maschinen, Gruppierung, Alterseffekte | nicht genannt |
| 5 | **Excel-Listen der Abteilungen** (Instandhaltung, Produktion, Qualität) | intern, uneinheitlich, halbstrukturiert | Schichtlisten, Ausfalllisten, Ersatzteilverbrauch. Wichtig, aber Silo-Daten | vorhanden, uneinheitlich |
| 6 | **Produktions-/Auftragsdaten** (ERP/MES: Auftrag, Stückzahl, Produkt, Laufzeit) | intern, Bewegungsdaten, transaktional | Belastungsprofil: Welche Last lag vor dem Ausfall an? | nicht genannt |
| 7 | **Ersatzteil- und Lagerdaten** (ERP) | intern, transaktional | Verfügbarkeit und Kosten, wichtig für die Umsetzung (Wartung rechtzeitig planen) | nicht genannt |
| 8 | **Externe Daten** (Herstellerangaben, Wetter/Hallenklima, Wartungsintervalle der Hersteller) | extern | Kontext, z. B. Temperatur und Luftfeuchte als Einflussfaktoren | optional |

**Zu Leitfrage 1 (fehlende Daten):** Für die Umsetzung fehlen vermutlich:
- ein sauber erfasster **Ausfall-Label** (exakter Zeitpunkt und Art jedes Ausfalls),
- ein durchgängiger **Maschinenschlüssel**, der Sensor, Wartung und Excel verbindet,
- **Betriebs- und Lastkontext** (welcher Auftrag lief, Umgebungsbedingungen),
- ausreichend **Ausfallhistorie**. Ausfälle sind selten, sodass sehr wenige Ereignisse für das Training vorliegen können.

## 2. Mindestens fünf potenzielle Datenprobleme (mit Kategorie)

Die Zuordnung folgt dem Raster der Aufgabe: **Qualität**, **Struktur**, **Organisation**.

| # | Datenproblem | Beschreibung im Szenario | Betroffene Qualitätsdimension (UE 1) | Kategorie |
|---|---|---|---|---|
| 1 | **Lückenhafte Wartungsprotokolle** | Maßnahmen oder Zeitpunkte fehlen. Dadurch sind Ausfälle nicht sicher bestimmbar und Trainingslabels unzuverlässig. | Vollständigkeit | **Qualität** |
| 2 | **Fehlende Werte und Ausreißer in Sensordaten** | Sensorausfall, Kabelbruch, Kalibrierdrift, Spikes. Das Modell lernt Messfehler statt Maschinenverhalten. | Vollständigkeit, Genauigkeit | **Qualität** |
| 3 | **Inkonsistente Angaben zwischen Quellen** | Dieselbe Störung ist in Excel der Instandhaltung anders datiert oder beschrieben als im Wartungsprotokoll. Maschinen heißen in jeder Liste anders. | Konsistenz | **Qualität** |
| 4 | **Unterschiedliche Zeitstempel** | Verschiedene Formate (`TT.MM.JJJJ` vs. ISO), Zeitzonen und Sommerzeit, unterschiedliche Auflösung (Sekundentakt bei Sensoren, Tageswerte bei Wartung). Ereignisse lassen sich nicht korrekt zeitlich zuordnen. | Konsistenz, Aktualität | **Struktur** |
| 5 | **Uneinheitliche Formate und Einheiten** | Excel-Freitext statt Katalogwerte, °C vs. °F, bar vs. kPa, Dezimalkomma vs. -punkt, Spaltennamen je Abteilung verschieden. | Konsistenz | **Struktur** |
| 6 | **Kein gemeinsamer Schlüssel / Stammdatenbezug** | Maschinen-ID im Sensorsystem ≠ Anlagennummer in Wartung ≠ Bezeichnung in Excel. Die Quellen lassen sich nur manuell oder gar nicht verknüpfen. | Konsistenz | **Struktur** |
| 7 | **Datensilos in den Abteilungen** | Jede Abteilung führt eigene Excel-Listen. Es gibt keinen Gesamtüberblick, und doppelte oder widersprüchliche Bestände entstehen. | Konsistenz | **Organisation** |
| 8 | **Fehlende Verantwortung (Data Ownership)** | Niemand ist für Pflege und Prüfung von Wartungs- und Sensordaten zuständig. Die Qualität verfällt, Lücken bleiben unbemerkt. | alle Dimensionen | **Organisation** |
| 9 | **Uneinheitliche Definitionen** | Was ist ein „Ausfall"? Ungeplanter Stillstand, Qualitätsabweichung oder auch geplante Wartung? Was ist „Wartung"? Produktion und Instandhaltung zählen unterschiedlich. | Konsistenz | **Organisation** |
| 10 | **Zugriffsrechte und Datenschutz** | Excel-Listen liegen auf lokalen Laufwerken oder Postfächern. Fremde Abteilungen haben keinen Zugriff. Teils sind personenbezogene Daten (Schichtführer, Techniker) enthalten (DSGVO, Datenminimierung). | – | **Organisation** |
| 11 | **Veraltete Daten / Latenz** | Wartungsprotokolle werden Tage später nachgetragen. Für Prognosen im laufenden Betrieb ist das zu spät. | Aktualität | **Qualität** |

Die Aufgabe verlangt mindestens fünf Probleme. Hier sind es elf, aus denen im Plenum eine Auswahl getroffen werden kann.

## 3. Kategorisierung (Überblick)

| Kategorie | Probleme (Nr.) | Kernaussage |
|---|---|---|
| **Qualität** (fehlende Werte, Ausreißer, Inkonsistenzen) | 1, 2, 3, 11 | Die Inhalte der Daten sind lückenhaft, fehlerhaft oder veraltet. |
| **Struktur** (Formate, Zeitstempel, Einheiten) | 4, 5, 6 | Die Daten sind technisch nicht zusammenführbar. |
| **Organisation** (Zuständigkeiten, Zugriffsrechte, Silos) | 7, 8, 9, 10 | Die Ursache ist, dass niemand Datenhoheit und Standards festgelegt hat. |

Einzelne Probleme gehören zu mehr als einer Kategorie (z. B. Nr. 3 hat auch eine organisatorische Ursache in uneinheitlichen Definitionen). Die Zuordnung nennt die **Hauptursache**.

## Leitfragen der Analyse

**Wo widersprechen sich die Datenquellen?**
- Ausfallzeitpunkt: Wartungsprotokoll vs. Excel der Instandhaltung vs. Sensorverlauf.
- Maschinenbezeichnung und -ID in jeder Quelle anders.
- Dauer eines Stillstands: Produktion (Auftragsunterbrechung) vs. Instandhaltung (Reparaturzeit).
- Zeitstempel verschieben sich durch Zeitzonen und Sommerzeit.

**Wer müsste für die Datenqualität verantwortlich sein?**

| Datenbereich | Vorschlag Data Owner | Aufgabe |
|---|---|---|
| Sensordaten | Betriebs-/Automatisierungstechnik (OT) | Kalibrierung, Ausfallüberwachung der Sensoren |
| Wartungsprotokolle, Störungen | Instandhaltungsleitung | Vollständigkeit, zeitnahe Erfassung, einheitlicher Katalog |
| Maschinenstammdaten | Anlagenverwaltung / IT-Stammdatenmanagement | eindeutige Maschinen-ID (Master Data Management) |
| Produktionsdaten | Produktionsleitung | Auftrags- und Laufzeitdaten |
| Übergreifend | Datenmanagement-Team (wir) + Data Governance | Standards, Definitionen, Qualitätschecks |

## Ergebnissicherung (Erkenntnisse)

- Datenprobleme sind meist eine **Mischung aus technischen und organisatorischen Ursachen**. Zeitstempel-Chaos ist technisch, aber es besteht nur, weil niemand einen Standard vorgegeben hat.
- Der erste Schritt ist, Probleme **sichtbar und benennbar** zu machen (Dateninventur, Qualitätskennzahlen wie Anteil fehlender Werte und Dublettenquote).
- Vorgehen nach UE 1: **Erfassen → Integrieren → Sichern → Bereitstellen**. Wichtigster Hebel: Single Source of Truth und Data Ownership.

---

# Teil 2 – Arbeitsauftrag 2: Datenqualität bewerten und priorisieren

**Gegeben:**

| Quelle | Beschreibung |
|---|---|
| **A) Kundendaten** | vollständig, aber teilweise veraltet (eine Abteilung) |
| **B) Sensordaten** | aktuell, aber unvollständig |
| **C) Verkaufsdaten** | vollständig, aber inkonsistent zwischen Abteilungen |

**Rahmenbedingungen:** Budget begrenzt, Zeitdruck (schnelle Ergebnisse erforderlich).

## 1. Bewertung nach Qualität und (potenziellem) Nutzen

**Qualität** nach den vier Dimensionen aus UE 1 (Skala 1 = schlecht bis 5 = gut):

| Quelle | Vollständigkeit | Aktualität | Konsistenz | Genauigkeit | Fazit Qualität |
|---|---|---|---|---|---|
| **A) Kundendaten** | 5 | 2 | 4 (eine Abteilung, ein Silo) | 3 (veraltet ⇒ falsche Werte möglich) | mittel, **Aktualität** ist das Defizit |
| **B) Sensordaten** | 2 | 5 | 4 (maschinell erzeugt, einheitlich) | 3–4 (Messfehler, Lücken) | mittel, **Vollständigkeit** ist das Defizit |
| **C) Verkaufsdaten** | 5 | 4 | 2 | 3 (Zahlen widersprechen sich) | mittel, **Konsistenz** ist das Defizit |

(Die Punktwerte sind eine begründete Schätzung auf Basis der Angaben, keine Messung. Als Folgeschritt wären echte Kennzahlen zu erheben: Anteil fehlender Werte, Dublettenquote, Alter der Datensätze.)

**Potenzieller Nutzen:** Der Nutzen hängt vom Verwendungszweck ab. Die Aufgabe nennt keinen konkreten Use Case, daher wird er hier bewusst transparent gemacht. Annahme: Es soll ein Prognosemodell aufgebaut werden (z. B. Nachfrage-/Absatzprognose oder Predictive Maintenance wie in Teil 1).

| Quelle | Potenzieller Nutzen | Begründung |
|---|---|---|
| **A) Kundendaten** | mittel | Basis für Churn- und Marketing-Analysen (CRM, UE 1). Weniger kritisch, wenn das Ziel Absatz- oder Wartungsprognose ist. |
| **B) Sensordaten** | hoch | Direkt prognoserelevant. Echtzeitfähig, hohes Potenzial für Frühwarnung und Anomalieerkennung. |
| **C) Verkaufsdaten** | hoch | Zentrale Zielgröße vieler Prognosen (Absatz, Umsatz). Entscheidungsrelevant für Planung. |

**Zusammenfassung (Qualität × Nutzen):**

| Quelle | Qualität | Nutzen | Verbesserungsaufwand (Schätzung) | Wirkung der Verbesserung |
|---|---|---|---|---|
| A | mittel | mittel | gering bis mittel (eine Abteilung aktualisiert den Bestand) | mittel |
| B | mittel | hoch | **mittel bis hoch** (Hardware, Sensorwartung, Imputation) | hoch |
| C | mittel | hoch | **mittel** (Definitionen klären, Abteilungen abstimmen) | **sehr hoch** |

## 2. Priorisierung: Welche Daten zuerst verbessern?

**Empfohlene Reihenfolge: C → B → A**

| Rang | Quelle | Maßnahme | Begründung kurz |
|---|---|---|---|
| **1** | **C) Verkaufsdaten** | Einheitliche Definitionen (z. B. was zählt als Verkauf, Netto/Brutto, Stornos), Abgleich der Abteilungen, eine verbindliche Datenbasis (Single Source of Truth) | Hoher Nutzen, Mängel sind überwiegend **organisatorisch** und damit mit begrenztem Budget schnell behebbar. Die Daten sind vollständig und aktuell, das Problem ist die Abstimmung. |
| **2** | **B) Sensordaten** | Lücken analysieren (Ursache: Sensor, Übertragung, Speicherung), Plausibilitätsregeln, automatisierte Qualitätschecks, Imputationsverfahren für kleine Lücken | Hoher Nutzen, aber teils **technisch/investiv**. Zuerst die Ursachen der Lücken ermitteln, dann gezielt investieren. Kurzfristig mit statistischen Verfahren überbrückbar. |
| **3** | **A) Kundendaten** | Aktualisierungsprozess in der zuständigen Abteilung, Stichtag für Datenpflege, Data Owner benennen | Vollständig, nur lokal veraltet, geringster Aufwand. Kann **parallel/nebenbei** laufen (Quick Win), hat aber den geringsten Hebel für die Prognose. |

**Wichtiger Hinweis:** Die Rangfolge gilt unter der Annahme, dass Absatz-/Sensorprognosen im Vordergrund stehen. Steht ein kundenorientierter Use Case im Mittelpunkt (z. B. Churn), rückt **A** nach vorn. Datenqualität ist relativ und immer im Verhältnis zum Verwendungszweck zu bewerten (Kernbotschaft UE 3).

## 3. Begründung der Entscheidung

1. **Zielkonflikt Geschwindigkeit vs. Qualität (UE 1):** Wegen des Zeitdrucks ist die Verbesserung mit dem besten Verhältnis aus Nutzen zu Aufwand zuerst dran. Das sind die Verkaufsdaten, weil die Klärung von Definitionen kaum Technik kostet.
2. **Kosten vs. Nutzen (UE 1):** Das Budget ist begrenzt. Datenpflege kostet, Nutzen entsteht oft erst später. Eine Investition muss sich rechtfertigen lassen. Konsistenz bei hoher Relevanz bringt den größten Effekt pro Euro.
3. **Konsistenz ≠ Korrektheit (UE 1, SSOT):** Eine einheitliche Datenbasis ist Voraussetzung. Danach kann jede Korrektur überall wirken (Korrigierbarkeit). Ohne diese Basis würden sich Fehler in A und B in jede Auswertung fortpflanzen.
4. **Fehlerfortpflanzung:** Datenqualität → Prognosegüte → Entscheidung → Geschäftserfolg. Qualität ist günstiger als Korrektur im Nachhinein. Widersprüchliche Verkaufszahlen würden sofort die Entscheidungen verfälschen.
5. **Sensordaten an Platz 2:** Hoher Nutzen, aber erst nach Ursachenanalyse sinnvoll investieren. Es wäre riskant, Geld in Sensorik zu stecken, bevor klar ist, ob die Lücken technisch oder organisatorisch bedingt sind.
6. **Kundendaten an Platz 3:** Aktualisierung ist ein klar abgegrenzter Quick Win, rechtfertigt aber keinen Vorrang vor Quellen mit größerem Prognosehebel.

**Bewusste Entscheidung statt Bauchgefühl:** Die Reihenfolge ergibt sich aus Kriterien (Nutzen, Aufwand, Art der Ursache, Zeitdruck) und nicht aus Intuition. Sie lässt sich bei geänderten Annahmen transparent neu bewerten.

## 4. Risiken bei schlechter Datenqualität

| Quelle | Konkretes Risiko |
|---|---|
| **A) Kundendaten (veraltet)** | Falsche Ansprache und Kampagnen, falsche Segmentierung, Churn-Modelle erkennen Abwanderung zu spät oder falsch. Kosten durch Streuverluste und Reputationsschaden. Außerdem Verstoß gegen die DSGVO-Richtigkeit bei falschen personenbezogenen Daten. |
| **B) Sensordaten (unvollständig)** | Ausfälle werden nicht erkannt (False Negatives), also ungeplante Stillstände und Folgekosten. Oder falsche Alarme (False Positives), also unnötige Wartung. Verzerrte Modelle, weil Lücken nicht zufällig sind (z. B. fällt der Sensor gerade vor einem Defekt aus). |
| **C) Verkaufsdaten (inkonsistent)** | Widersprüchliche Kennzahlen, Misstrauen in Reports, Streit über „die richtige Zahl". Fehlplanung bei Produktion, Lager und Budget, also **Fehlentscheidungen**. Verlorene Zeit durch manuellen Abgleich. |

**Übergreifende Risiken:**
- **Fehlentscheidungen** auf Basis falscher Prognosen (Garbage in, Garbage out).
- **Vertrauensverlust** in Daten und Datenprojekte, mit der Folge, dass die Akzeptanz im Unternehmen sinkt und Investitionen als verlorenes Geld gelten.
- **Verlorene Zeit und Kosten** durch Nacharbeit, manuelle Korrekturen und Doppelarbeit.
- **Scheinsicherheit:** Ein Modell mit guter Kennzahl auf schlechten Daten wirkt belastbar, ist es aber nicht. Konsistente, aber falsche oder veraltete Daten bleiben es auch in einer Single Source of Truth.
- **Compliance-Risiko** bei personenbezogenen Daten (DSGVO).

**Gegenmaßnahmen (Kurzfassung):** Qualitätskennzahlen definieren und regelmäßig messen, automatisierte Qualitätschecks, Data Ownership klar zuweisen, einheitliche Definitionen (Data Governance), Governance als Führungsaufgabe mit Budget und Rollen.

## Diskussionspunkte / Kernbotschaft

- **Welche Datenquelle wurde priorisiert, und warum?** Verkaufsdaten, weil der Nutzen hoch und die Behebung günstig ist.
- **Wo könnten Meinungen auseinandergehen?** Bei der Gewichtung von Sensordaten (hoher Nutzen vs. höhere Kosten) und bei der Frage, ob schnelle Teilergebnisse oder gründliche Datenbereinigung Vorrang haben.
- **Kernbotschaft:** Datenqualität ist relativ und immer im Verhältnis zum Verwendungszweck zu bewerten. Priorisierung erfordert eine bewusste Entscheidung, kein Bauchgefühl.

---

## Hinweis zur Entstehung

Dieser Lösungsentwurf basiert ausschließlich auf den Folien UE 1 bis UE 3. Die Bewertungen (Punktwerte, Aufwandsschätzungen) und der angenommene Use Case sind **Annahmen**, weil die Aufgabenstellung keine Messwerte oder konkreten Ziele nennt. Sie sollten vor einer Abgabe an das eigene Szenario angepasst werden.
