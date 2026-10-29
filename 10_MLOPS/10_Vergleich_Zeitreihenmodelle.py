"""Tag 10, Zusatz: klassische Zeitreihenmodelle (statsmodels) gegen das lineare Modell der Pipeline.

Fairer Vergleich: Alle Modelle sagen von einem Stichtag aus die nächsten 12 Monate vorher,
ohne die Ist-Werte dieser 12 Monate zu kennen (so läuft die Prognose im Betrieb).
Stichtage: Ende 1955 bis Ende 1959 (Tests 1956 bis 1960), jeweils mit Neutraining.
Mehrere Stichtage, weil das Ergebnis bei nur 12 oder 24 Testmonaten zu stark vom Zufall abhängt.

Start (im Kursordner):
    .venv/bin/python 10_MLOPS/10_Vergleich_Zeitreihenmodelle.py
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

DATEI = Path(__file__).parent / "10_02_UE2_Arbeitsauftrag1_Daten.csv"
MONATE = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
HORIZONT = 12
STICHTAGE = [f"{jahr}-12-01" for jahr in range(1955, 1960)]


# =============================================================================
# Daten laden (wie in der Pipeline)
# =============================================================================
def lade_reihe():
    df = pd.read_csv(DATEI, encoding="utf-8-sig").dropna(how="all")
    df["datum"] = pd.to_datetime(dict(
        year=df["year"].astype(int),
        month=df["month"].map({m: i + 1 for i, m in enumerate(MONATE)}), day=1))
    reihe = df.set_index("datum")["passengers"].astype(float)
    reihe.index.freq = "MS"
    return reihe


# =============================================================================
# Modelle: jede Funktion bekommt die Vergangenheit und liefert 12 Prognosewerte
# =============================================================================
def lineares_modell(train):
    """Das Modell der Pipeline: Vorjahr + Vormonat + Monat, rekursiv prognostiziert."""
    f = pd.DataFrame({"vorjahr": train.shift(12), "vormonat": train.shift(1)})
    monate = pd.get_dummies(train.index.month, dtype=float)
    monate = monate.reindex(columns=range(1, 13), fill_value=0.0)
    monate.index = train.index
    f = pd.concat([f, monate.add_prefix("m_")], axis=1)
    f["ziel"] = train
    f = f.dropna()
    spalten = [c for c in f.columns if c != "ziel"]
    modell = LinearRegression().fit(f[spalten], f["ziel"])

    werte = train.tolist()
    ausgabe = []
    for h in range(1, HORIZONT + 1):
        datum = train.index[-1] + pd.DateOffset(months=h)
        zeile = {"vorjahr": werte[-12], "vormonat": werte[-1]}
        zeile.update({f"m_{i}": float(i == datum.month) for i in range(1, 13)})
        wert = float(modell.predict(pd.DataFrame([zeile])[spalten])[0])
        werte.append(wert)
        ausgabe.append(wert)
    return np.array(ausgabe)


def holt_winters_additiv(train):
    m = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12)
    return m.fit().forecast(HORIZONT).to_numpy()


def holt_winters_multiplikativ(train):
    # Die Saison-Ausschläge wachsen mit dem Niveau: multiplikative Saison passt besser
    m = ExponentialSmoothing(train, trend="add", seasonal="mul", seasonal_periods=12)
    return m.fit().forecast(HORIZONT).to_numpy()


def sarima_airline(train):
    # "Airline-Modell" (Box und Jenkins) auf dem Logarithmus: wurde für genau diese Daten entwickelt
    m = SARIMAX(np.log(train), order=(0, 1, 1), seasonal_order=(0, 1, 1, 12))
    return np.exp(m.fit(disp=False).forecast(HORIZONT).to_numpy())


def vorjahresregel(train):
    return train.iloc[-12:].to_numpy()


MODELLE = {
    "Vorjahresregel (Vergleich)": vorjahresregel,
    "Linear (Pipeline)": lineares_modell,
    "Holt-Winters additiv": holt_winters_additiv,
    "Holt-Winters multiplikativ": holt_winters_multiplikativ,
    "SARIMA (0,1,1)(0,1,1,12) auf log": sarima_airline,
}


# =============================================================================
# Vergleich
# =============================================================================
def main():
    warnings.filterwarnings("ignore")  # statsmodels warnt bei Konvergenz und Frequenz
    reihe = lade_reihe()
    zeilen = []
    for name, modell in MODELLE.items():
        fehler, prozent = [], []
        for stichtag in STICHTAGE:
            train = reihe[:stichtag]
            echt = reihe[train.index[-1] + pd.DateOffset(months=1):][:HORIZONT]
            prognose = modell(train)
            fehler.append(np.abs(echt.to_numpy() - prognose))
            prozent.append(np.abs(echt.to_numpy() - prognose) / echt.to_numpy())
        zeilen.append({
            "Modell": name,
            "MAE bestes Jahr": min(f.mean() for f in fehler),
            "MAE schlechtestes Jahr": max(f.mean() for f in fehler),
            "MAE gesamt": np.concatenate(fehler).mean(),
            "MAPE gesamt": np.concatenate(prozent).mean(),
            "Fehler Monat 1": np.mean([f[0] for f in fehler]),
            "Fehler Monat 12": np.mean([f[-1] for f in fehler]),
        })
    tabelle = pd.DataFrame(zeilen).set_index("Modell")
    pd.options.display.float_format = "{:.3f}".format
    print(tabelle.sort_values("MAE gesamt").to_string())


if __name__ == "__main__":
    main()
