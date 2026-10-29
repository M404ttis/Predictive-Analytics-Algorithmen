"""Tag 10, Arbeitsauftrag 1: Pipeline für die automatische Nachfrageprognose.

Daten: Fluggäste je Monat 1949 bis 1960 (144 Werte mit Trend und Saison).
Ein Aufruf führt alle Schritte nacheinander aus, jeder Schritt ist eine Funktion.
In einem echten Betrieb wäre jede Funktion ein Task in Airflow (siehe Lösungsdatei).

Start (im Ordner des Kurses):
    .venv/bin/python 10_MLOPS/10_Pipeline_Nachfrageprognose.py
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit

# =============================================================================
# SCHRITT 0: Konfiguration (alle Stellschrauben an einem Ort)
# =============================================================================
ORDNER = Path(__file__).parent
DATEI = ORDNER / "10_02_UE2_Arbeitsauftrag1_Daten.csv"
ARTEFAKTE = ORDNER / "artefakte"        # Modell, Prognose, Protokoll (nicht ins Git)
TESTMONATE = 24                          # die letzten 24 Monate nur zum Prüfen
HORIZONT = 12                            # Prognose: die nächsten 12 Monate
MAX_MAPE = 0.10                          # Freigabe nur bei höchstens 10 % Fehler
MONATE = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# =============================================================================
# SCHRITT 1: Daten laden
# =============================================================================
def lade_daten(pfad):
    # utf-8-sig: die CSV beginnt mit einem BOM, sonst heißt die erste Spalte "﻿year"
    return pd.read_csv(pfad, encoding="utf-8-sig")


# =============================================================================
# SCHRITT 2: Daten prüfen (Datentest, bricht die Pipeline bei Fehlern ab)
# =============================================================================
def pruefe_daten(df):
    df = df.dropna(how="all")  # die Datei endet mit einer leeren Zeile (",,")
    fehler = []
    if df[["year", "month", "passengers"]].isna().any().any():
        fehler.append("fehlende Werte")
    if not df["month"].isin(MONATE).all():
        fehler.append("unbekannte Monatsnamen")
    if df.duplicated(["year", "month"]).any():
        fehler.append("doppelte Monate")
    if (df["passengers"] <= 0).any():
        fehler.append("Fluggäste <= 0")
    if (df.groupby("year").size() != 12).any():
        fehler.append("ein Jahr hat nicht 12 Monate")
    if fehler:
        raise ValueError("Datentest fehlgeschlagen: " + ", ".join(fehler))
    return df


# =============================================================================
# SCHRITT 3: Bereinigen und in eine Zeitreihe bringen
# =============================================================================
def bereinige(df):
    df = df.copy()
    df["monat_nr"] = df["month"].map({m: i + 1 for i, m in enumerate(MONATE)})
    df["datum"] = pd.to_datetime(
        dict(year=df["year"].astype(int), month=df["monat_nr"], day=1))
    # sortieren, denn bei Zeitreihen zählt die Reihenfolge
    return df.sort_values("datum").set_index("datum")[["monat_nr", "passengers"]]


# =============================================================================
# SCHRITT 4: Features berechnen (nur Information aus der Vergangenheit)
# =============================================================================
def baue_features(zr):
    f = pd.DataFrame(index=zr.index)
    f["vorjahr"] = zr["passengers"].shift(12)   # gleicher Monat im Vorjahr (Saison)
    f["vormonat"] = zr["passengers"].shift(1)   # letzter Wert (Niveau und Trend)
    monate = pd.get_dummies(zr["monat_nr"], prefix="m", dtype=float)
    f = pd.concat([f, monate.reindex(columns=[f"m_{i}" for i in range(1, 13)],
                                     fill_value=0.0)], axis=1)
    f["t"] = np.arange(len(zr))                 # laufende Nummer als einfacher Trend
    f["ziel"] = zr["passengers"]
    return f.dropna()                           # die ersten 12 Monate haben kein Vorjahr


# Kandidaten: (Name, Modell, benutzte Spalten)
MONATSSPALTEN = [f"m_{i}" for i in range(1, 13)]
KANDIDATEN = {
    "Trend + Monat":           (LinearRegression(), ["t"] + MONATSSPALTEN),
    "Vorjahr + Vormonat":      (LinearRegression(), ["vorjahr", "vormonat"]),
    "Vorjahr + Vormonat + Monat": (LinearRegression(),
                                   ["vorjahr", "vormonat"] + MONATSSPALTEN),
    "Boosting (Bäume)":        (GradientBoostingRegressor(random_state=42),
                                ["vorjahr", "vormonat"] + MONATSSPALTEN),
}


# =============================================================================
# SCHRITT 5: Zeitlich aufteilen (nie zufällig mischen, sonst Leakage)
# =============================================================================
def teile_auf(f):
    return f.iloc[:-TESTMONATE], f.iloc[-TESTMONATE:]


# =============================================================================
# SCHRITT 6: Training und Modellauswahl (Kreuzvalidierung nur auf Trainingsdaten)
# =============================================================================
def waehle_modell(train):
    ergebnisse = {}
    cv = TimeSeriesSplit(n_splits=4, test_size=12)  # jeweils die Zukunft vorhersagen
    for name, (modell, spalten) in KANDIDATEN.items():
        fehler = []
        for a, b in cv.split(train):
            modell.fit(train.iloc[a][spalten], train.iloc[a]["ziel"])
            vorhersage = modell.predict(train.iloc[b][spalten])
            fehler.append(mean_absolute_error(train.iloc[b]["ziel"], vorhersage))
        ergebnisse[name] = float(np.mean(fehler))
    bester = min(ergebnisse, key=lambda k: ergebnisse[k])
    modell, spalten = KANDIDATEN[bester]
    modell.fit(train[spalten], train["ziel"])
    return bester, modell, spalten, ergebnisse


# =============================================================================
# SCHRITT 7: Validierung auf den Testdaten (das Tor vor dem Ausrollen)
# =============================================================================
def validiere(modell, spalten, test):
    vorhersage = modell.predict(test[spalten])
    mae = mean_absolute_error(test["ziel"], vorhersage)
    mape = float(np.mean(np.abs(test["ziel"] - vorhersage) / test["ziel"]))
    # Vergleichswert: "so viel wie im Vorjahr" (ein Modell muss das schlagen)
    mae_naiv = mean_absolute_error(test["ziel"], test["vorjahr"])
    bestanden = bool(mape <= MAX_MAPE and mae < mae_naiv)
    return {"mae": float(mae), "mape": mape, "mae_naiv": float(mae_naiv),
            "bestanden": bestanden}


# =============================================================================
# SCHRITT 8: Deployment (nur bei bestandener Validierung)
# =============================================================================
def deploy(name, spalten, f, zr, kennzahlen):
    modell, _ = KANDIDATEN[name]
    # Endgültiges Modell auf ALLEN Daten, damit der jüngste Verlauf eingeht
    modell.fit(f[spalten], f["ziel"])
    ARTEFAKTE.mkdir(exist_ok=True)
    version = datetime.now().strftime("%Y%m%d-%H%M%S")
    joblib.dump(modell, ARTEFAKTE / f"modell_{version}.joblib")
    # Lineage: welche Daten, welches Modell, welche Kennzahlen
    meta = {
        "version": version,
        "modell": name,
        "spalten": spalten,
        "daten_hash": hashlib.sha256(DATEI.read_bytes()).hexdigest()[:12],
        "daten_bis": str(zr.index.max().date()),
        **kennzahlen,
    }
    (ARTEFAKTE / f"modell_{version}.json").write_text(json.dumps(meta, indent=2))
    return modell, version


# =============================================================================
# SCHRITT 9: Prognose erzeugen (Batch, Monat für Monat in die Zukunft)
# =============================================================================
def prognostiziere(modell, spalten, zr, version):
    werte = zr["passengers"].astype(float).tolist()
    start = zr.index.max()
    zeilen = []
    for h in range(1, HORIZONT + 1):
        datum = start + pd.DateOffset(months=h)
        zeile = {"vorjahr": werte[-12], "vormonat": werte[-1],
                 "t": len(werte)}
        zeile.update({f"m_{i}": float(i == datum.month) for i in range(1, 13)})
        wert = float(modell.predict(pd.DataFrame([zeile])[spalten])[0])
        werte.append(wert)  # die eigene Prognose dient als nächster "Vormonat"
        zeilen.append({"datum": datum.date(), "prognose": round(wert, 1)})
    ausgabe = pd.DataFrame(zeilen)
    ausgabe.to_csv(ARTEFAKTE / f"prognose_{version}.csv", index=False)
    return ausgabe


# =============================================================================
# SCHRITT 10: Protokollieren und überwachen (Experiment-Tracking in klein)
# =============================================================================
def protokolliere(meta_zeile):
    pfad = ARTEFAKTE / "laeufe.csv"
    ARTEFAKTE.mkdir(exist_ok=True)
    neu = pd.DataFrame([meta_zeile])
    if pfad.exists():
        neu = pd.concat([pd.read_csv(pfad), neu], ignore_index=True)
    neu.to_csv(pfad, index=False)


def ueberwache(modell, spalten, neu, fenster=6, schwelle=0.15):
    """Im Betrieb: vergleicht die Prognose mit den neu eingetroffenen Ist-Werten.
    Hier zur Demonstration mit den letzten Testmonaten (Modell vor dem Neutraining)."""
    letzte = neu.iloc[-fenster:]
    fehler = np.mean(np.abs(letzte["ziel"] - modell.predict(letzte[spalten]))
                     / letzte["ziel"])
    return {"mape_letzte_monate": float(fehler), "retraining_noetig": bool(fehler > schwelle)}


# =============================================================================
# Ablauf: die Schritte in fester Reihenfolge (bei Airflow wäre das der DAG)
# =============================================================================
def main():
    roh = lade_daten(DATEI)                                    # Schritt 1
    sauber = pruefe_daten(roh)                                 # Schritt 2
    zr = bereinige(sauber)                                     # Schritt 3
    f = baue_features(zr)                                      # Schritt 4
    train, test = teile_auf(f)                                 # Schritt 5
    name, modell, spalten, cv_mae = waehle_modell(train)       # Schritt 6
    kennzahlen = validiere(modell, spalten, test)              # Schritt 7

    print("Kreuzvalidierung (MAE, kleiner ist besser):")
    for k, v in sorted(cv_mae.items(), key=lambda x: x[1]):
        print(f"  {k:28s} {v:6.1f}")
    print(f"\nGewählt: {name}")
    print(f"Test: MAE {kennzahlen['mae']:.1f}, MAPE {kennzahlen['mape']:.1%}, "
          f"Vorjahres-Vergleich MAE {kennzahlen['mae_naiv']:.1f}")

    if not kennzahlen["bestanden"]:                            # Tor vor Schritt 8
        print("\nValidierung NICHT bestanden: kein Deployment, altes Modell bleibt.")
        protokolliere({"zeit": datetime.now().isoformat(timespec="seconds"),
                       "modell": name, "status": "abgelehnt", **kennzahlen})
        return

    ueberwachung = ueberwache(modell, spalten, test)           # Schritt 10 (Teil 2)
    modell, version = deploy(name, spalten, f, zr, kennzahlen)  # Schritt 8
    prognose = prognostiziere(modell, spalten, zr, version)    # Schritt 9
    protokolliere({"zeit": datetime.now().isoformat(timespec="seconds"),
                   "version": version, "modell": name, "status": "in Betrieb",
                   **kennzahlen})                              # Schritt 10

    print(f"\nDeployment: Version {version} in {ARTEFAKTE.name}/")
    print(f"Überwachung: {ueberwachung}")
    print("\nPrognose (die nächsten 12 Monate):")
    print(prognose.to_string(index=False))


if __name__ == "__main__":
    main()
