# Bestelldaten: Datenprobleme und Annahmen

*Quelle: `04_Bestelldaten_Arbeitsauftrag1.csv` · erzeugt von `04_Bestelldaten_Probleme.py` · 21.10.2026*

## Auf einen Blick

| Kennzahl | Wert |
| --- | --- |
| Datenzeilen gelesen | 14 |
| Zeilen nach Dublettenentfernung | 12 |
| Zeilen mit mindestens einem Befund | 12 von 14 |
| Umsatz roh → ohne Dubletten | 522.00 → 477.60 EUR |
| Verschiedene Datumsformate | 4 |
| Negative Zeilen (Retouren?) | 2 |

> Das Skript bereinigt nichts. Es benennt Annahmen und belegt sie mit Kennzahlen.

## Inhalt

- [1. Rohdatei: Struktur](#1-rohdatei-struktur)
- [2. Parsen und Typen](#2-parsen-und-typen)
- [3. Fehlende Werte](#3-fehlende-werte)
- [4. Dubletten](#4-dubletten)
- [5. Datumsformate](#5-datumsformate)
- [6. Negative Mengen und Umsätze](#6-negative-mengen-und-umsätze)
- [7. Plausibilität: Stückpreis und Ausreißer](#7-plausibilität-stückpreis-und-ausreißer)
- [8. Kundenstammdaten](#8-kundenstammdaten)
- [9. Befunde pro Zeile](#9-befunde-pro-zeile)
- [10. Zusammenfassung: Problem, Umfang, Vorschlag](#10-zusammenfassung-problem-umfang-vorschlag)

---

## 1. Rohdatei: Struktur

| Prüfung | Ergebnis |
| --- | --- |
| Zeilen in der Datei | 16 |
| Byte Order Mark (BOM) am Dateianfang | ja |
| Naives `pd.read_csv(sep=';')` | Fehler (ParserError: Error tokenizing data. C error: Expected 1 fields in line 16, saw 2
) |
| Zeilen komplett in ein Anführungszeichen-Paar gepackt | 15 von 16 |
| Leere Zeilen | 0 |
| Zeilen nur aus Trennzeichen | 1 (Zeile 16) |

**Annahmen**

- Excel hat jede Zeile als ein einziges Textfeld exportiert (Anführungszeichen um die ganze Zeile). Ein normaler CSV-Reader sieht daher nur eine Spalte.
- Die Zeile mit nur `;` ist ein Excel-Artefakt (leere Zeile mit Spaltentrenner) und kein Datensatz.
- Das BOM stammt vom Excel-Export; ohne `utf-8-sig` würde es im ersten Spaltennamen landen.

## 2. Parsen und Typen

| Prüfung | Ergebnis |
| --- | --- |
| Gelesene Datenzeilen | 14 |
| Nicht lesbare Zeilen | 0 |
| Umsatz mit nur 1 Nachkommastelle | '199,0' |
| Typ `Menge` | int64 |
| Typ `Umsatz` (nach Komma-Ersetzung) | float64 |

**Annahmen**

- Der Umsatz ist als Text mit Dezimalkomma gespeichert und muss in eine Zahl umgewandelt werden.
- `199,0` hat nur eine Nachkommastelle: vermutlich `199,00` (Excel schneidet abschließende Nullen ab). Unkritisch, da die Null eindeutig ist.

## 3. Fehlende Werte

| Spalte | Fehlend | Anteil | BestellIDs |
| --- | --- | --- | --- |
| KundenID | 1 | 7% | B-1008 |
| Name | 1 | 7% | B-1003 |
| E-Mail | 2 | 14% | B-1003, B-1007 |

**Zeilen mit mindestens einer Lücke:** 3 von 14 (21%)

**Rekonstruierbar aus anderen Bestellungen desselben Kunden?**

| BestellID | Fehlendes Feld | Rekonstruierbar |
| --- | --- | --- |
| B-1003 | Name | nein |
| B-1003 | E-Mail | nein |
| B-1007 | E-Mail | nein |
| B-1008 | KundenID | nein |

**Annahmen**

- Pflichtfelder fehlten im Erfassungsformular bzw. wurden nicht erzwungen.
- Eine fehlende KundenID ist kritischer als eine fehlende E-Mail (Kunde nicht zuordenbar).

## 4. Dubletten

| Prüfung | Ergebnis |
| --- | --- |
| Exakte Dubletten (alle Spalten gleich) | 2 überzählige Zeile(n) |
| Betroffene BestellIDs | B-1006, B-1012 |
| Gleiche BestellID, andere Inhalte | 0 (0 = alle ID-Dubletten sind exakte Kopien) |
| Zeilen roh → ohne Dubletten | 14 → 12 |
| Umsatz roh | 522.00 EUR |
| Umsatz ohne Dubletten | 477.60 EUR |
| Verzerrung durch Dubletten | +44.40 EUR (9.3%) |

**Annahmen**

- Doppelter Export oder Doppelklick beim Absenden: gleiche BestellID = gleiche Bestellung.
- Löschen ist nur unkritisch, weil eine BestellID nur einmal vorkommen darf.

## 5. Datumsformate

| Format | Anzahl |
| --- | --- |
| ISO (JJJJ-MM-TT) | 10 |
| deutsch (TT.MM.JJJJ) | 2 |
| Schrägstrich (MM/TT oder TT/MM) | 1 |
| Text (5. März 2024) | 1 |

**Anzahl verschiedener Formate:** 4

**Mehrdeutige Daten**

| BestellID | Rohwert | Mögliche Daten | Nachbarn (nach BestellID) | Passt zur Reihenfolge |
| --- | --- | --- | --- | --- |
| B-1004 | 03/05/2024 | 2024-03-05 oder 2024-05-03 | 2024-03-02 … 2024-03-03 | keine Variante |

**Annahmen**

- Bei `03/05/2024` wird MM/TT (US) angenommen, weil die Datei sonst deutsch formatiert ist.
- Eigentlich nicht entscheidbar: Rückfrage bei der Quelle nötig.

**Reihenfolge der Daten** (BestellIDs werden als chronologisch angenommen)

| Zeile | Datum | steht nach | Datum davor |
| --- | --- | --- | --- |
| B-1005 | 2024-03-03 | B-1004 | 2024-03-05 |
| B-1008 | 2024-03-04 | B-1007 | 2024-03-05 |
| B-1011 | 2024-03-04 | B-1010 | 2024-03-05 |

**Annahmen**

- Der erste Rücksprung (B-1005) entsteht nur durch die MM/TT-Annahme bei B-1004; mit anderer Lesart (03. Mai) wäre die Lücke noch größer.

**Zeitraum:** 2024-03-01 bis 2024-03-05

## 6. Negative Mengen und Umsätze

| BestellID | Produkt | Menge | Umsatz (EUR) | Originalkauf vorhanden |
| --- | --- | --- | --- | --- |
| B-1005 | Webcam | -1 | -39.90 | nein |
| B-1011 | Maus | -2 | -39.80 | nein |

- Zeilen mit negativer Menge oder negativem Umsatz: 2
- Zeilen mit unterschiedlichem Vorzeichen (Menge vs. Umsatz): 0
- Umsatz der negativen Zeilen: -79.70 EUR

**Annahmen**

- Negative Zeilen sind Retouren/Stornos, keine Tippfehler, denn Menge UND Umsatz sind negativ.
- Aber: Kein passender Originalkauf im Datensatz → Retoure aus früherem Zeitraum oder Fehlbuchung.
- Für 'Absatz pro Produkt' würden Retouren die Menge verfälschen; für den Umsatz sind sie echt.

## 7. Plausibilität: Stückpreis und Ausreißer

**Stückpreis (Umsatz / Menge) je Produkt**

| Produkt | Zeilen | Stückpreis min | Stückpreis max | Verschiedene Preise |
| --- | --- | --- | --- | --- |
| Kopfhörer | 2 | 49.90 | 49.90 | 1 |
| Maus | 4 | 19.90 | 19.90 | 1 |
| Monitor | 1 | 199.00 | 199.00 | 1 |
| Tastatur | 2 | 29.90 | 29.90 | 1 |
| USB-Kabel | 3 | 4.90 | 4.90 | 1 |
| Webcam | 2 | 39.90 | 39.90 | 1 |

**Annahmen**

- Umsatz = Menge × Stückpreis, der Preis ist je Produkt konstant → der Umsatz ist intern konsistent.

**Umsatz:** Q1 19.90, Q3 47.40, IQR-Grenzen [-21.35, 88.65]

| BestellID | Produkt | Menge | Umsatz |
| --- | --- | --- | --- |
| B-1005 | Webcam | -1 | -39.90 |
| B-1007 | Monitor | 1 | 199.00 |
| B-1009 | Kopfhörer | 2 | 99.80 |
| B-1011 | Maus | -2 | -39.80 |

**Annahmen**

- Die Ausreißer sind erklärbar (teures Produkt, Menge 2, Retouren sind negativ), also echte Extreme statt Tippfehler → nicht blind entfernen (prüfen, dann entscheiden).

## 8. Kundenstammdaten

| Prüfung | Ergebnis |
| --- | --- |
| Verschiedene KundenIDs | 9 |
| KundenIDs mit mehr als einem Namen/einer E-Mail | 0 |
| E-Mails, die zu mehreren KundenIDs gehören | 0 |
| Ungültig aufgebaute E-Mails | 0 |

**Annahmen**

- Mögliche Dubletten wie 'Marie Müller' / 'M. Müller' (Folie) sind hier nicht erkennbar.
- Bei nur 9 Kunden ist ein Abgleich per Name/E-Mail möglich; in großen Beständen wäre Fuzzy-Matching nötig.

## 9. Befunde pro Zeile

| BestellID | Datum | KundenID | Produkt | Menge | Umsatz | Befunde |
| --- | --- | --- | --- | --- | --- | --- |
| B-1001 | 2024-03-01 | K-101 | Kopfhörer | 1 | 49.90 | – |
| B-1002 | 02.03.2024 | K-102 | Tastatur | 2 | 59.80 | Datum: deutsch |
| B-1003 | 2024-03-02 | K-103 | Maus | 1 | 19.90 | fehlt: Name, E-Mail |
| B-1004 | 03/05/2024 | K-104 | USB-Kabel | 3 | 14.70 | Datum: Schrägstrich; Datum mehrdeutig |
| B-1005 | 2024-03-03 | K-105 | Webcam | -1 | -39.90 | negativ (Retoure?); Umsatz-Ausreißer; Datum springt zurück |
| B-1006 | 2024-03-03 | K-101 | Maus | 1 | 19.90 | Dublette |
| B-1006 | 2024-03-03 | K-101 | Maus | 1 | 19.90 | Dublette |
| B-1007 | 5. März 2024 | K-106 | Monitor | 1 | 199.00 | fehlt: E-Mail; Datum: Text; Umsatz-Ausreißer |
| B-1008 | 2024-03-04 | – | Tastatur | 1 | 29.90 | fehlt: KundenID; Datum springt zurück |
| B-1009 | 2024-03-04 | K-107 | Kopfhörer | 2 | 99.80 | Umsatz-Ausreißer |
| B-1010 | 2024-03-05 | K-108 | Webcam | 1 | 39.90 | – |
| B-1011 | 04.03.2024 | K-107 | Maus | -2 | -39.80 | Datum: deutsch; negativ (Retoure?); Umsatz-Ausreißer; Datum springt zurück |
| B-1012 | 2024-03-05 | K-109 | USB-Kabel | 5 | 24.50 | Dublette |
| B-1012 | 2024-03-05 | K-109 | USB-Kabel | 5 | 24.50 | Dublette |

## 10. Zusammenfassung: Problem, Umfang, Vorschlag

| Problem | Schwere | Umfang | Methode |
| --- | --- | --- | --- |
| Dateistruktur (Zeile als ein Textfeld, BOM) | 🔴 hoch | alle 15 Zeilen | korrekt einlesen: Anführungszeichen entfernen, dann splitten (zuerst!) |
| Exakte Dubletten | 🔴 hoch | 2 Zeile(n), +44.40 EUR Umsatz | löschen (BestellID eindeutig) |
| Datumsformate gemischt | 🟠 mittel | 4 von 14 Zeilen | vereinheitlichen: ein Format, Annahme für 03/05 dokumentieren |
| Negative Menge / Umsatz | 🟠 mittel | 2 Zeile(n), -79.70 EUR | prüfen; als Retoure kennzeichnen statt löschen |
| Fehlende KundenID | 🟠 mittel | 1 Zeile(n) | nicht schätzen; markieren/ausschließen oder Quelle fragen |
| Fehlender Name / E-Mail | 🟡 gering | 1 / 2 Zeile(n) | so lassen, falls nicht modellrelevant |
| Leere / Trennzeichen-Zeile | 🟡 gering | 1 Zeile(n) | löschen |

**Vorgeschlagene Reihenfolge (Abhängigkeiten)**

1. Datei korrekt einlesen: ohne das sind alle weiteren Schritte falsch
2. Typen und Formate angleichen (Datum, Umsatz als Zahl)
3. Dubletten entfernen: vor jeder Aggregation, sonst wird doppelt gezählt
4. Negative Werte klären (Retoure markieren)
5. Fehlende Werte behandeln: zuletzt, erst wenn klar ist, was wirklich fehlt

**Wirkung auf den Gesamtumsatz**

| Stand | Zeilen | Umsatz (EUR) |
| --- | --- | --- |
| roh | 14 | 522.00 |
| ohne Dubletten | 12 | 477.60 |
| ohne Dubletten, nur positive Zeilen (ohne Retouren) | 10 | 557.30 |
