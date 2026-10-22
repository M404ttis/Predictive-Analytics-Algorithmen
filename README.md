# Predictive Analytics & Algorithmen

Arbeitsmaterial zur Fortbildung **„Predictive Analytics & Algorithmen – Prognosemodelle und datenbasierte Entscheidungen mit Big Data"**.
Gesammelt, damit Mitlernende von den Lösungsentwürfen, Notebooks und Spickzetteln profitieren können.

> **Hinweis:** Das sind persönliche Lernunterlagen, keine Musterlösungen. Die Entwürfe sind mit Unterstützung von KI (Claude) entstanden.
> Bewertungen, Punktwerte und Szenario-Annahmen sind begründete Einschätzungen und als **Annahme** gekennzeichnet. Bitte kritisch prüfen und anpassen.
> Die Kursfolien (PDF) sind **nicht** enthalten.

## Schnellstart: das Notebook mit den Notebook-Preisen

Siehe [`05_Modellauswahl/05_README.txt`](05_Modellauswahl/05_README.txt): Schritt für Schritt von „Python installieren" bis „Notebook im Browser".

## Aufbau

| Ordner | Thema | Wichtigste Dateien |
| --- | --- | --- |
| [`00_Kompendium`](00_Kompendium) | Nachschlagewerk über alle Tage | `00_Kompendium_Predictive_Analytics.md` (Konzepte, Formeln, Wenn-dann-Regeln), `00_Data_Science_Beginner_Cheatsheet.md` |
| [`01_Predictive-Analytics`](01_Predictive-Analytics) | Anwendungsfelder, Modelltypen, Metriken | `01_UE2_Arbeitsauftrag1.md` |
| [`02_Daten-und-Modelle`](02_Daten-und-Modelle) | Datenprobleme und Szenarien, Mini-Projekt Nachfrageprognose (Kaggle Favorita) | `02_UE2_Arbeitsauftrag1_Bearbeitung.md`, Unterordner [`02_Favorita_Mini-Projekt`](02_Daten-und-Modelle/02_Favorita_Mini-Projekt) mit eigener `README.md` und Berichten in `reports/` |
| [`03_Datenmanagement`](03_Datenmanagement) | DWH, Data Lake, Governance, Datenqualität | Lösungen, Fallstudie AutoParts, `03_MLPenguins` (EDA) |
| [`04_Datenaufbereitung`](04_Datenaufbereitung) | Cleaning, Features, Pipelines | Bestelldaten-Diagnose (`.py` und Bericht), Features, ETL-Pipeline, Transferprojekt |
| [`05_Modellauswahl`](05_Modellauswahl) | Modellwahl, Regression, Kreuzvalidierung | Lösungsentwurf, Notebook mit Plots, CSV mit 500 Notebooks |

Die Dateien tragen die Nummer des Tages als Präfix (`04_...` gehört zu Tag 4).

## Hinweise zur Nutzung

- **Diagramme** sind in Mermaid geschrieben und werden auf GitHub direkt angezeigt.
- **Notebooks** (`.ipynb`) sind über [jupytext](https://jupytext.readthedocs.io) mit gleichnamigen `.py`-Dateien gekoppelt (Zellen mit `# %%`). So lassen sich Änderungen in Git gut lesen.
- **Mini-Projekt Favorita:** Die Rohdaten stammen von Kaggle (*Store Sales – Time Series Forecasting*) und liegen nicht im Repository. Siehe dessen `README.md`.
