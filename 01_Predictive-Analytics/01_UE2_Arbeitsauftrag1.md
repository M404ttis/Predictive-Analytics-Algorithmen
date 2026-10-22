# UE 2 · Arbeitsauftrag 1 – Prognose-Anwendungsfelder

**Szenario:** Online-Händler für Elektronikprodukte
**Problemfelder:** Unklare Nachfrageentwicklung · Hohe Lagerkosten · Viele Retouren · Steigende Kundenabwanderung
**Rolle:** Analytics-Team – Einsatzmöglichkeiten erkennen, ohne technisches Vorwissen
**Arbeitsform:** Individuell → Ergebnis festhalten → Kurzpräsentation & Diskussion im Plenum


---

## 1. Ergebnistabelle

| # | Anwendungsfeld (Was wird vorhergesagt?) | Geschäftsbereich | Datenbasis (Welche Daten brauchen wir?) | Nutzen |
|---|---|---|---|---|
| 1 | **Absatzprognose** je Produkt/Kategorie (Wie viele Einheiten werden in den nächsten Wochen verkauft?) | Vertrieb | Verkaufshistorie, Saison/Feiertage, Preise & Aktionen, Produktlaunches, Webseiten-Traffic | hoch |
| 2 | **Lagerbestand & Nachbestellmenge** (Welcher Bestand wird wann benötigt?) | Logistik | Absatzprognose, aktuelle Bestände, Lieferzeiten, Lagerkosten, Abverkaufsgeschwindigkeit | hoch |
| 3 | **Kundenabwanderung (Churn)** (Welche Kunden kaufen bald nicht mehr?) | Marketing / Service | Kaufhistorie, letzte Bestellung, Login-/Klickverhalten, Beschwerden, Newsletter-Reaktion | hoch |
| 4 | **Retourenwahrscheinlichkeit** (Welche Bestellung wird voraussichtlich zurückgeschickt?) | Service / Logistik | Retourenhistorie, Produktkategorie, Bewertungen, Kundenverhalten, Zahlungs-/Lieferart | mittel |
| 5 | **Zahlungsausfall / Betrugsrisiko** (Welche Bestellung wird nicht bezahlt?) | Finance | Zahlungshistorie, Bestellmuster, Zahlart, Bonitätsdaten | mittel |

<!-- Optionale Alternativen / Ergänzungen:
     - Customer Lifetime Value (Marketing)
     - Preis-/Rabattwirkung (Vertrieb)
     - Lieferzeit-Prognose (Logistik)
     - Produktdefekte / Garantiefälle (Service)
-->

---

## 2. Bewertung nach Use-Case-Kriterien

Kriterien aus UE 1: **Business Impact**, **Umsetzbarkeit**, **Datenverfügbarkeit** (jeweils hoch / mittel / niedrig).

| # | Anwendungsfeld | Business Impact | Umsetzbarkeit | Datenverfügbarkeit | Gesamtnutzen |
|---|---|:---:|:---:|:---:|:---:|
| 1 | Absatzprognose | hoch | hoch | hoch | **hoch** |
| 2 | Lagerbestand & Nachbestellung | hoch | mittel | hoch | **hoch** |
| 3 | Kundenabwanderung | hoch | mittel | mittel | **hoch** |
| 4 | Retourenwahrscheinlichkeit | mittel | mittel | mittel | **mittel** |
| 5 | Zahlungsausfall / Betrug | mittel | mittel | niedrig | **mittel** |

---

## 3. Einordnung im Analytics-Spektrum

| Stufe | Leitfrage | Beispiel aus unserem Szenario |
|---|---|---|
| Descriptive | Was war? | Absatz- und Retourenquote der letzten 12 Monate |
| **Predictive** | **Was wird sein?** | Prognose Absatz, Churn-Risiko, Retourenwahrscheinlichkeit |
| Prescriptive | Was tun? | Automatische Nachbestellung, gezielte Halte-Aktion für Churn-Kunden |

---

## 4. Zielvariable, Modelltyp und Metriken

Entscheidungslogik aus UE 1: 
*Zählt der Verlauf über die Zeit?* → Zeitreihe 
*Zielvariable eine Zahl?* → Regression 
*Zielvariable eine Kategorie?* → Klassifikation 
*Keine Zielvariable?* → Clustering.

| Anwendungsfeld | Zielvariable (Was wird vorhergesagt?) | Zieltyp | Modelltyp | Passende Metriken |
|---|---|---|---|---|
| 1 Absatzprognose | Verkaufte Einheiten pro Woche/Monat | stetig (continuous) | Zeitreihe (ggf. Regression mit Preis, Aktion, Saison als Merkmale) | MAE, RMSE, MAPE |
| 1 Absatzprognose (Variante) | Absatz je Produkt aus Preis/Werbebudget, ohne Zeitverlauf | stetig (continuous) | Regression | MAE, RMSE, R² |
| 2 Lagerbestand & Nachbestellung | Benötigte Menge bis zur nächsten Lieferung | stetig (continuous) | Zeitreihe / Regression | MAE, RMSE, MAPE |
| 2 Lagerbestand (Variante) | Lieferengpass ja/nein | binär | Klassifikation | Recall, Precision, F1, ROC-AUC |
| 3 Kundenabwanderung | Kunde kündigt / bleibt | binär | Klassifikation | Recall, Precision, F1, ROC-AUC |
| 4 Retouren | Bestellung wird zurückgeschickt ja/nein | binär | Klassifikation | Recall, Precision, F1, ROC-AUC |
| 4 Retouren (Variante) | Retourengrund (defekt / passt nicht / gefällt nicht) | mehrklassig (multi class) | Klassifikation | Accuracy, Macro-F1, Confusion Matrix |
| 5 Zahlungsausfall / Betrug | Bestellung wird nicht bezahlt / ist Betrug | binär | Klassifikation | Recall, Precision, F1, ROC-AUC |
| Zusatz: Kundensegmente | keine Zielvariable | – | Clustering | Silhouette-Koeffizient + fachliche Deutung |

### Metriken im Überblick

| Metrik | Gilt für | Formel | Frage, die sie beantwortet | Hinweis |
|---|---|---|---|---|
| **Accuracy** | Klassifikation | $\frac{TP + TN}{TP + TN + FP + FN}$ | Wie viel Prozent aller Vorhersagen sind richtig? | Täuscht bei seltenen Klassen (z. B. 2 % Betrug → 98 % „Accuracy" ohne Modell) |
| **Precision** | Klassifikation | $\frac{TP}{TP + FP}$ | Wie viele der als „positiv" markierten Fälle sind wirklich positiv? | Wichtig, wenn Fehlalarme teuer sind (z. B. Kunden fälschlich blockieren) |
| **Recall** | Klassifikation | $\frac{TP}{TP + FN}$ | Wie viele der echten positiven Fälle finden wir? | Wichtig, wenn Übersehen teuer ist (Betrug, Churn) |
| **F1-Score** | Klassifikation | $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ | Ausgleich aus Precision und Recall | Ein einzelner Wert, wenn beides zählt |
| **ROC-AUC** | Klassifikation | $\int_0^1 \text{TPR}\, d(\text{FPR})$ mit $\text{TPR} = \frac{TP}{TP+FN}$, $\text{FPR} = \frac{FP}{FP+TN}$ | Wie gut trennt das Modell die Klassen über alle Schwellenwerte? | Fläche unter der ROC-Kurve; 0,5 = Zufall, 1 = perfekt. Bewertet die Wahrscheinlichkeiten, nicht eine feste Entscheidung |
| **MAE** | Regression / Zeitreihe | $\frac{1}{n} \sum_{i=1}^{n} \lvert y_i - \hat{y}_i \rvert$ | Wie weit liegen wir im Durchschnitt daneben (in Einheiten)? | Leicht verständlich, robust gegenüber Ausreißern |
| **RMSE** | Regression / Zeitreihe | $\sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$ | Wie weit liegen wir daneben, große Fehler stärker gewichtet? | Immer ≥ MAE; stärker von Ausreißern beeinflusst |
| **MAPE** | Regression / Zeitreihe | $\frac{100\,\%}{n} \sum_{i=1}^{n} \left\lvert \frac{y_i - \hat{y}_i}{y_i} \right\rvert$ | Wie viel Prozent liegen wir im Schnitt daneben? | Unbrauchbar bei Werten nahe 0 |
| **R²** | Regression | $1 - \frac{\sum_i (y_i - \hat{y}_i)^2}{\sum_i (y_i - \bar{y})^2}$ | Welcher Anteil der Schwankung wird vom Modell erklärt? | Für Zeitreihen nur eingeschränkt aussagekräftig |
| **Silhouette** | Clustering | $s = \frac{b - a}{\max(a,\, b)}$ | Wie klar sind die Gruppen voneinander getrennt? | Wert zwischen −1 und 1; ersetzt nicht die fachliche Deutung der Gruppen |

**Legende:**
$TP$ = richtig positiv, $TN$ = richtig negativ, $FP$ = falsch positiv (Fehlalarm), $FN$ = falsch negativ (übersehen) ·
$y_i$ = tatsächlicher Wert, $\hat{y}_i$ = vorhergesagter Wert, $\bar{y}$ = Mittelwert der tatsächlichen Werte, $n$ = Anzahl der Fälle ·
$a$ = mittlerer Abstand eines Punktes zu seiner eigenen Gruppe, $b$ = mittlerer Abstand zur nächsten fremden Gruppe


---

## 5. Begründung der Nutzen-Bewertung

1. **Absatzprognose – hoch:** Grundlage für fast alles andere (Lager, Einkauf, Marketing); löst direkt das Problem „unklare Nachfrage".
2. **Lagerbestand – hoch:** Adressiert hohe Lagerkosten und Lieferfähigkeit; baut auf #1 auf.
3. **Churn – hoch:** Neukunden sind teurer als Bestandskunden; früh erkannte Abwanderung lässt sich noch beeinflussen.
4. **Retouren – mittel:** Spürbare Kosten, aber nur teilweise beeinflussbar (z. B. Produktbeschreibung, Beratung).
5. **Zahlungsausfall – mittel:** Wichtig, aber meist kleinerer Anteil am Gesamtverlust; Daten oft bei Dritten.

---

## 6. Leitfragen (Ideenfindung)

- Wo entstehen gerade die größten Kosten oder Verluste? → *Lager, Retouren*
- Wo müssen heute Entscheidungen ohne gute Datenbasis getroffen werden? → *Einkaufsmengen, Aktionsplanung*
- Was würde sich ändern, wenn wir es einen Monat früher wüssten? → *Bestellungen anpassen, Kunden gezielt halten*

