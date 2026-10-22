# UE 3 · Arbeitsauftrag 2: Feature Engineering verstehen

*Arbeitsdatei, Basis: `04_01_UE1_Datenaufbereitung.pdf` (Folien 10–13, 25–27) und `04_03_UE3_Arbeitsauftrag2.pdf`*

## 0. Aufgabe auf einen Blick

| | |
| --- | --- |
| **Gegebene Rohdaten** | `Kaufdatum`, `Kaufbetrag`, `Produktkategorie` |
| **Aufgabe 1** | 5 neue sinnvolle Features entwickeln |
| **Aufgabe 2** | Begründen, warum sie für Prognosen hilfreich sind |
| **Aufgabe 3** | Features identifizieren, die problematisch sein könnten |
| **Kernbotschaft (Folie 10, 12)** | Gute Features übersetzen Rohdaten in Geschäftslogik. Gute Features steigern die Modellgüte oft mehr als das Modell. |

**Merksatz aus UE 1 (Folie 12):** Feature = Eingabemerkmal des Modells. Feature Engineering = Merkmale gezielt bauen und Fachwissen einbringen.

---

## 1. Erst die Denkweise: zwei Blickwinkel auf dieselben Rohdaten

Aus drei Spalten lassen sich Features auf zwei Ebenen bauen. Das erklärt, warum die Ideen aus der Folie ("Kaufhäufigkeit", "Zeit seit dem letzten Kauf") und eure Ideen ("Umsatz pro Wochentag") unterschiedlich aussehen.

| | **A: Kundenebene** | **B: Absatz-/Kalenderebene** |
| --- | --- | --- |
| Frage | Wie verhält sich dieser Kunde? | Wie viel wird an diesem Tag verkauft? |
| Eine Zeile im Modell = | ein Kunde (zu einem Stichtag) | ein Tag oder eine Woche |
| Typische Prognose | Kauft der Kunde wieder? Wird er abwandern? | Absatz morgen / nächste Woche |
| Quelle | Folie 3 (Orientierungsraster), Folie 11 | Folie 20 (tägliche Absatz-Pipeline), Folie 27 (zeitliche Merkmale) |

**Faustregel zum Finden von Features:** Für jede Rohspalte vier Fragen stellen.

| Frage | Beispiel mit `Kaufdatum` | Beispiel mit `Kaufbetrag` | Beispiel mit `Produktkategorie` |
| --- | --- | --- | --- |
| Zerlegen: Welche Bestandteile stecken drin? | Wochentag, Monat, Quartal | (Betrag ist schon eine Zahl) | Oberkategorie / Unterkategorie |
| Aggregieren: Zusammenfassen über Zeit oder Kunde? | Käufe pro Monat | Summe / Mittelwert pro Kunde | Anteil je Kategorie pro Kunde |
| Vergleichen: Gegenüber früher oder anderen? | gleicher Tag Vorjahr | Betrag vs. eigener Durchschnitt | Kategorie vs. Gesamtsortiment |
| Veränderung: Wie entwickelt es sich? | Abstand zwischen Käufen wird größer | Steigung über die Zeit | Wechsel der bevorzugten Kategorie |

---

## 2. Die Ideen im Detail

### 2.1 Eure Kalender-Ideen (Ebene B)

| Idee | Was ist das genau? | Brauchbar als Feature? | Fallstrick |
| --- | --- | --- | --- |
| **Umsatz pro Wochentag** | Zwei Varianten: (a) **`Wochentag`** als Merkmal des Datums (Mo = 1 … So = 7). (b) **Durchschnittsumsatz je Wochentag** aus der Historie. | Ja. Samstag verkauft anders als Dienstag. Die Wochentagsmuster sind in Handelsdaten fast immer stark. | `Wochentag` als Zahl 1–7 suggiert eine Reihenfolge, 7 und 1 liegen aber nebeneinander. Besser One-Hot (siehe Abschnitt 4). Variante (b) darf nur aus **Trainingsdaten** berechnet werden. |
| **Umsatz pro Woche** | Summe der Umsätze einer Kalenderwoche. | Nur als **Vorwoche**, nicht als aktuelle Woche. | **Data Leakage**: Wenn ich den Umsatz von Dienstag vorhersage und die Wochensumme (Mo–So) als Feature nutze, steckt Dienstag selbst und die Zukunft (Mi–So) darin. Richtig: `Umsatz_Vorwoche`. |
| **Umsatz pro Quartal** | Summe je Quartal. | Als Information "welches Quartal" (`Quartal` = 1–4) ja. Als Quartalssumme eher grob. | Nur 4 Ausprägungen pro Jahr, also wenig Auflösung. Hängt stark mit `Monat` und `Kalenderwoche` zusammen (Redundanz, siehe 5.4). |
| **Umsatz am selben Tag des Vorjahres** | Der Wert vom Tag exakt 1 Jahr zuvor, oder als Verhältnis heute / Vorjahr. | Sehr gut: fängt Saison (Weihnachten, Sommer) und Feiertage ein. | Braucht **mindestens 1 Jahr Historie**; für neue Produkte/Filialen leer. Besser **364 Tage** zurück statt 365: dann ist es derselbe **Wochentag**. Bewegliche Feiertage (Ostern) wandern. |

> **Zur Unterscheidung:** Ihr habt "Umsatz pro …" geschrieben. Als *Feature* ist meist nicht die Summe dieses Zeitraums gemeint, sondern eine **Kennzeichnung des Zeitraums** (`Wochentag`, `Quartal`) und/oder die **Kennzahl der Vergangenheit** (`Umsatz_Vorwoche`). Die Umsatzsumme des Zielzeitraums selbst ist das, was man **vorhersagen** will (Zielgröße), kein Feature.

### 2.2 Wie wird aus mehreren Tageswerten ein "Trend"? (Ihre Frage)

Ein Trend beantwortet: **Geht es hoch, runter oder bleibt es gleich?** Er entsteht immer aus *vergangenen* Werten, also nur aus Tagen **vor** dem Vorhersagezeitpunkt. Es gibt vier gängige Wege, vom einfachsten zum aufwändigsten:

| # | Methode | Formel / Idee | Beispiel | Aussage |
| --- | --- | --- | --- | --- |
| 1 | **Gleitender Durchschnitt** (Rolling Mean) | Mittelwert der letzten *n* Tage | Ø der letzten 7 Tage | Glättet Tagesrauschen (ein einzelner Ausreißer fällt kaum auf) |
| 2 | **Differenz oder Verhältnis zweier Zeitfenster** | kurzes Fenster minus (oder geteilt durch) langes Fenster | Ø letzte 7 Tage ÷ Ø letzte 28 Tage | > 1: Absatz steigt, < 1: sinkt. Der **einfachste verständliche Trend** |
| 3 | **Steigung** (lineare Regression über die letzten *n* Tage) | Anstieg der Geraden durch die letzten Punkte | Steigung über 14 Tage | Ein Zahlenwert: Stärke und Richtung des Trends |
| 4 | **Exponentiell gleitender Durchschnitt** (EMA) | neuere Tage zählen stärker | EMA mit Halbwertszeit 3 Tage | Reagiert schneller auf Wendepunkte |

Dazu die **Lag-Features** ("Werte von früher"): `Umsatz_gestern` (Lag 1), `Umsatz_vor_7_Tagen` (Lag 7, gleicher Wochentag), `Umsatz_vor_364_Tagen` (Vorjahr). Trend und Lags sind die Standardzutaten für Zeitreihenprognosen.

**Die wichtigste Regel: `shift(1)`.** Fenster dürfen den Tag, den man vorhersagt, **nicht** enthalten, sonst Data Leakage.

```python
import pandas as pd

# tag: ein DataFrame mit einer Zeile pro Tag, Spalte "umsatz", Index = Datum (sortiert!)
tag["wochentag"] = tag.index.dayofweek          # 0 = Montag
tag["quartal"] = tag.index.quarter

# nur Vergangenheit: erst um 1 Tag verschieben, DANN das Fenster bilden
vergangen = tag["umsatz"].shift(1)
tag["mittel_7"] = vergangen.rolling(7).mean()
tag["mittel_28"] = vergangen.rolling(28).mean()
tag["trend_7_28"] = tag["mittel_7"] / tag["mittel_28"]    # > 1 = steigt

tag["lag_7"] = tag["umsatz"].shift(7)           # gleicher Wochentag letzte Woche
tag["lag_364"] = tag["umsatz"].shift(364)       # gleicher Wochentag Vorjahr
tag["yoy"] = tag["umsatz"].shift(1).rolling(7).sum() / tag["umsatz"].shift(365).rolling(7).sum()
```

*Hinweis:* Die ersten Zeilen sind leer (`NaN`), weil noch keine Historie da ist. Das ist normal. Sie werden gelöscht oder bewusst behandelt (Folie 4, 23: fehlende Werte).

---

## 3. Vorschlag für die 5 Features zur Abgabe

Zur Aufgabe passt ein Mix aus Verhalten (Ebene A, Orientierungsraster Folie 3) und Zeitbezug (Ebene B). Alle fünf lassen sich aus den **drei Rohspalten** ableiten.

| # | Feature | Berechnung | Rohspalte(n) | Warum hilft es der Prognose? (Aufgabe 2) |
| --- | --- | --- | --- | --- |
| 1 | **Kaufhäufigkeit** (Käufe der letzten 90 Tage) | Anzahl Käufe je Kunde im Fenster vor dem Stichtag | Kaufdatum | Viele Käufe zeigen Bindung. Wer oft kauft, kauft wahrscheinlich wieder. Aus vielen Zeilen pro Kunde (schwer modellierbar) wird **ein** aussagekräftiger Wert (Folie 11). |
| 2 | **Tage seit dem letzten Kauf** (Recency) | Stichtag minus letztes Kaufdatum | Kaufdatum | Je länger der letzte Kauf her ist, desto höher das Risiko, dass der Kunde weg ist. Klassischer Frühindikator für Abwanderung. |
| 3 | **Durchschnittlicher Kaufbetrag** | Mittelwert der Beträge je Kunde (Median bei Ausreißern) | Kaufbetrag | Trennt Schnäppchen- von Premiumkunden. Das Betragsniveau ist ein stabiles Kundenmerkmal. |
| 4 | **Bevorzugte Produktkategorie** (bzw. Anteil je Kategorie) | Kategorie mit höchstem Umsatzanteil je Kunde; danach **One-Hot** | Produktkategorie | Gibt dem Modell Information über Interessen. Verschiedene Kategorien haben verschiedene Kaufzyklen (Verbrauchsgüter vs. Elektronik). |
| 5 | **Trend des Kaufbetrags** (Ø letzte 30 Tage ÷ Ø vorherige 30 Tage) | Verhältnis zweier Zeitfenster | Kaufbetrag, Kaufdatum | Sinkende Beträge können Abwanderung ankündigen, steigende Kaufkraft oder Interesse. Zeigt die **Richtung**, nicht nur den Stand. |

**Bonus aus eurer Liste (Ebene B, falls die Prognose "Absatz pro Tag" gemeint ist):** `Wochentag` (One-Hot), `Quartal`, `Umsatz_Vorwoche`, `Umsatz_Vorjahr (364 Tage)`, `Trend 7/28`. Wenn der Fokus der Abgabe auf Absatzprognose liegt, ersetzt diese Gruppe die Features 1–5.

---

## 4. One-Hot-Encoding: wann, warum, was bringt es im Training?

*Bezug: Folie 25 (One-Hot-Encoding) und 26 (Kategoriale Daten kodieren).*

### 4.1 Das Problem

Modelle rechnen mit Zahlen, nicht mit Text (Folie 26). Eine Kategorie wie `Elektronik` muss also in Zahlen übersetzt werden. Zwei Wege:

**Weg 1: Durchnummerieren (Label-/Integer-Encoding)**

| Produktkategorie | Code |
| --- | --- |
| Bücher | 1 |
| Elektronik | 2 |
| Kleidung | 3 |

**Weg 2: One-Hot (jede Kategorie bekommt eine eigene 0/1-Spalte)**

| Produktkategorie | ist_Bücher | ist_Elektronik | ist_Kleidung |
| --- | --- | --- | --- |
| Bücher | 1 | 0 | 0 |
| Elektronik | 0 | 1 | 0 |
| Kleidung | 0 | 0 | 1 |

### 4.2 Warum ist One-Hot besser als Namen oder Nummern?

| Aspekt | Namen (Text) | Durchnummerieren (1, 2, 3) | One-Hot |
| --- | --- | --- | --- |
| Für das Modell lesbar? | Nein, Fehler beim Training | Ja | Ja |
| Erfindet es eine Reihenfolge? | – | **Ja**: Kleidung (3) > Elektronik (2) > Bücher (1); Elektronik wäre "genau in der Mitte" | **Nein**: alle Kategorien sind gleichberechtigt |
| Erfindet es Abstände? | – | Ja: Abstand Bücher–Kleidung (2) = doppelt so groß wie Bücher–Elektronik (1) | Nein: jede Kategorie ist gleich weit entfernt |
| Gewicht je Kategorie | – | **Ein** Gewicht für alles, das "mehr Kategorie-Nummer = mehr Umsatz" ausdrückt | **Ein eigenes Gewicht je Kategorie**: Elektronik kann positiv wirken, Bücher negativ |

**Der Vorteil beim Training:** Ein Modell wie eine lineare Regression lernt pro Spalte ein Gewicht. Mit der Nummer 1/2/3 kann es nur eine einzige Geradenneigung über alle Kategorien lernen. Das Modell würde annehmen, Kleidung wirke "dreimal so stark" wie Bücher. Mit One-Hot lernt es getrennt: "Elektronik erhöht den Kaufbetrag um 40 €, Bücher senken ihn um 5 €". Ohne künstliche Ordnung erkennt es also echte Unterschiede, was die Vorhersage genauer und die Interpretation ehrlicher macht.

### 4.3 Wann One-Hot, wann etwas anderes?

| Situation | Empfehlung | Begründung |
| --- | --- | --- |
| Kategorien **ohne Reihenfolge**, wenige Ausprägungen (bis ca. 10–20) | **One-Hot** | Standardfall. `Produktkategorie` gehört dazu. |
| Kategorien **mit echter Reihenfolge** (S < M < L, Note 1–6, Gold > Silber > Bronze) | **Ordinal kodieren** (1, 2, 3) | Die Reihenfolge ist Information. One-Hot würde sie verwerfen (Folie 26). |
| **Sehr viele** Ausprägungen (Artikelnummer, PLZ, Kunden-ID) | **Nicht** One-Hot. Stattdessen gruppieren, seltene zu "Sonstige", Target- oder Frequency-Encoding | Hunderte Spalten, fast nur Nullen, Überanpassungsgefahr |
| `Wochentag`, `Monat` | One-Hot **oder** zyklisch (sin/cos) | Zyklisch, 7 liegt neben 1. One-Hot ist einfacher und reicht meist. |
| Baumbasierte Modelle (Random Forest, XGBoost) | One-Hot oft nicht zwingend, aber unschädlich | Bäume können auch mit Nummern gut Schwellen setzen. Lineare Modelle, kNN, neuronale Netze und SVM brauchen es dringend. |

**Praxis-Hinweise:**

- **Dummy-Trap:** Bei linearen Modellen eine Spalte weglassen (`drop_first=True`), da die letzte Kategorie aus den anderen folgt (Mehrfachkollinearität).
- **Neue Kategorien im Betrieb:** Taucht in neuen Daten eine unbekannte Kategorie auf, darf die Pipeline nicht abstürzen (`handle_unknown="ignore"`).
- **Nur auf Trainingsdaten anpassen** (`fit`), dann auf Testdaten anwenden (`transform`), sonst Data Leakage und andere Spalten bei Training und Betrieb. Das ist auch ein Reproduzierbarkeitsthema (Folie 16, Pipelines).

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Variante pandas (schnell, zum Ausprobieren)
df = pd.get_dummies(df, columns=["produktkategorie"], dtype=int)

# Variante scikit-learn (für Pipelines, merkt sich die Kategorien aus dem Training)
enc = OneHotEncoder(handle_unknown="ignore")
X_train_kat = enc.fit_transform(X_train[["produktkategorie"]])
X_test_kat = enc.transform(X_test[["produktkategorie"]])
```

**Antwort auf "Ist One-Hot auf Produktkategorien sinnvoll?"** Ja, wenn es überschaubar viele, ungeordnete Kategorien sind. Ein Modell kann dann pro Kategorie ein eigenes Muster lernen. Bei ein paar Hundert Unterkategorien lieber auf Oberkategorien verdichten oder die Anteile je Kunde als Zahlen (0–100 %) verwenden.

---

## 5. Kritische Prüfung: Welche Features können problematisch sein? (Aufgabe 3)

Die zwei Prüffragen der Folie 3: **(1)** Steckt Information aus der Zukunft drin (**Data Leakage**)? **(2)** Ist das Feature für **alle Kunden** gleich berechenbar?

### 5.1 Prüfmatrix

| Feature | Leakage-Gefahr | Für alle berechenbar? | Weitere Probleme | Gegenmaßnahme |
| --- | --- | --- | --- | --- |
| Kaufhäufigkeit (90 Tage) | **Hoch**, wenn das Fenster über den Stichtag hinausreicht oder den Kauf enthält, den man vorhersagt | Neukunden: 0 oder 1 Kauf, wenig Aussage | Dubletten zählen doppelt (siehe AA 1: B-1006, B-1012) | Fenster endet **vor** dem Stichtag. Vorher Dubletten entfernen. |
| Tage seit letztem Kauf | Mittel: nur korrekt, wenn "letzter Kauf" vor dem Stichtag liegt | **Neukunden: leer** (kein letzter Kauf) | Fehlwert hat Bedeutung ("noch nie gekauft") | Eigenes Kennzeichen `ist_neukunde`, Fehlwert nicht blind mit 0 füllen |
| Ø Kaufbetrag | Hoch, wenn der aktuelle Kauf im Mittelwert steckt | Neukunden: nur ein Wert | **Ausreißer und Retouren** (negative Beträge) verzerren den Mittelwert | Median statt Mittelwert, Retouren vorher markieren/herausnehmen |
| Bevorzugte Kategorie | Gering | Neukunden: "Mehrheit" aus einem Kauf, wackelig | **Label-Encoding** würde falsche Ordnung erfinden. Viele Kategorien = viele Spalten | One-Hot, Mindestanzahl Käufe verlangen |
| Trend des Kaufbetrags | **Hoch** bei zentrierten Fenstern oder Fenstern ohne `shift(1)` | **Nur bei ≥ 2 Fenstern Historie** (60+ Tage), sonst leer | Bei wenigen Käufen pro Fenster sehr rauschig | Nur Vergangenheit, Mindestmenge an Käufen, sonst bewusst `NaN` |
| `Umsatz_Woche` (aktuelle Woche) | **Sehr hoch**: enthält den Zieltag und die Zukunft | Ja | – | Nur `Umsatz_Vorwoche` verwenden |
| `Umsatz_Vorjahr` | Gering (Vergangenheit) | **Nein**: braucht ≥ 1 Jahr Historie, neue Produkte/Kunden leer | Feiertage verschieben sich | 364 statt 365 Tage, Fehlwerte bewusst behandeln |
| `Wochentag` als Zahl 1–7 | Keins | Ja | Falsche Reihenfolge, 7 und 1 liegen nebeneinander | One-Hot oder sin/cos |

### 5.2 Data Leakage: das größte Risiko

Das Modell sieht beim Training etwas, was es im echten Einsatz nicht wissen kann. Es erreicht dann im Test fantastische Werte und im Betrieb enttäuscht es. **Test:** Frage bei jedem Feature: *"Hätte ich diesen Wert zum Zeitpunkt der Vorhersage schon gekannt?"* Wenn nein, ist es Leakage.

### 5.3 Nicht für alle gleich berechenbar

Neukunden, neue Produkte oder neue Filialen haben keine Historie. Features wie Trend, Recency oder Vorjahr sind dort leer. Das Modell muss damit umgehen können (Fehlwerte behandeln, siehe Folie 23: Löschen / Mittelwert-Median / modellbasiert, jeweils mit Vor- und Nachteil).

### 5.4 Weitere Fallstricke

- **Redundanz:** `Woche`, `Monat` und `Quartal` tragen fast dieselbe Information. Mehr Features sind nicht automatisch besser. Irrelevante erhöhen die Komplexität (Folie 13: "weniger, aber bessere Features sind oft stärker").
- **Skalierung:** Kaufbetrag (Euro) und Kaufhäufigkeit (Anzahl) haben ganz verschiedene Wertebereiche. Bei vielen Modellen skalieren (Normalisierung 0–1 oder Standardisierung, Folie 7, 9, 24). One-Hot-Spalten sind schon 0/1 und brauchen das nicht.
- **Datenqualität vorher:** Features sind nur so gut wie die Bereinigung. Dubletten verfälschen Häufigkeiten, negative Beträge (Retouren) die Mittelwerte, falsche Datumsformate die Zeitabstände (siehe Arbeitsauftrag 1, `04_Bestelldaten_Probleme_Bericht.md`).
- **Zielkonflikt (Folie 4, 18, 19):** Mehr und komplexere Features steigern evtl. die Genauigkeit, machen aber die Pipeline langsamer und schwerer wartbar. Bewusst abwägen.

---

## 6. Einbettung in den Aufbereitungs-Workflow (Folie 22)

```
Cleaning ──► Transform ──► Features ──► Bereitstellen
Dubletten,   Datumsformat   Recency,       modellbereiter
Lücken,      einheitlich,   Häufigkeit,    Datensatz
Ausreißer    skalieren      Trend, One-Hot
```

Features kommen **nach** dem Cleaning und der Transformation. Sonst werden Fehler in Features "eingebacken". Die Feature-Berechnung gehört in die **Pipeline** (Folie 14–17, 20), damit sie bei jedem neuen Datenstand identisch und reproduzierbar läuft.

---

## 7. Checkliste (Folie 29, auf Features angewendet)

- [ ] Sind Lücken, Ausreißer, Dubletten **vor** dem Feature-Bau behandelt?
- [ ] Sind numerische Merkmale skaliert und Kategorien kodiert (One-Hot bei ungeordneten)?
- [ ] Ist **Data Leakage** ausgeschlossen (nur Daten vor dem Vorhersagezeitpunkt, `shift(1)`)?
- [ ] Ist jedes Feature für **alle** Kunden berechenbar, oder gibt es ein Kennzeichen für Fehlwerte?
- [ ] Ist die Berechnung in einer **reproduzierbaren Pipeline** abgebildet?

---

## 8. Kurzantwort für die Diskussion (Folie 5)

- **Häufigste Features:** Kaufhäufigkeit, Ø Kaufbetrag, Recency, bevorzugte Kategorie, Trend (Orientierungsraster); dazu Kalendermerkmale (Wochentag, Quartal, Vorjahr).
- **Potenziell problematisch:** alle, die die Zukunft enthalten (Leakage, z. B. aktuelle Wochensumme) oder für Neukunden nicht berechenbar sind (Trend, Recency, Vorjahr). Dazu Label-Encoding von Kategorien.
- **Wie verändert ein gutes Feature die Aussagekraft?** Es verdichtet viele Rohzeilen zu einem verständlichen Wert mit Geschäftsbezug ("kauft seltener", "gibt weniger aus"). Das Modell muss das Muster nicht mehr mühsam selbst finden.
