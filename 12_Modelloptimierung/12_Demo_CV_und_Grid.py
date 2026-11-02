"""Tag 12, Bohnenwerk: Kreuzvalidierung (Arbeitsauftrag 1) und Grid Search (Arbeitsauftrag 2).

Das mitgelieferte Skript 12_02_UE2_Arbeitsauftrag1_CV.py sucht die Datei "1202_UE2_..." mit
Semikolon und Dezimalkomma. Unsere CSV heißt anders und hat Kommas, deshalb hier eine eigene
Version mit pandas und sklearn. Gleiches Modell (lineare Regression), gleiche Merkmale.

Start (im Kursordner):
    .venv/bin/python 12_Modelloptimierung/12_Demo_CV_und_Grid.py
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score

DATEI = Path(__file__).parent / "12_02_UE2_Arbeitsauftrag1_Daten.csv"
MERKMALE = ["Woche", "Budget_Social_EUR", "Budget_Newsletter_EUR", "Budget_Print_EUR",
            "Rabattaktion", "Weihnachtsgeschaeft", "Temperatur_C"]
ZIEL = "Umsatz_EUR"
SEKUNDEN_PRO_LAUF = 20      # Annahme der Aufgabe: ein Training auf dem Firmenlaptop
BUDGET_SEKUNDEN = 3600      # die IT gibt höchstens eine Stunde frei


def lade():
    # utf-8-sig wegen BOM, dropna wegen der leeren letzten Zeile
    return pd.read_csv(DATEI, encoding="utf-8-sig").dropna(how="all").astype(float)


def folds_nach_wochen(d, grenzen):
    """grenzen = [(von, bis), ...] in Wochen; jeder Bereich ist einmal Test."""
    return [(np.where(~d["Woche"].between(a, b))[0], np.where(d["Woche"].between(a, b))[0])
            for a, b in grenzen]


def mse_je_fold(modell, d, folds):
    return -cross_val_score(modell, d[MERKMALE], d[ZIEL], cv=folds,
                            scoring="neg_mean_squared_error")


def zeige(titel, werte):
    print(f"{titel:34s} " + " ".join(f"{w:>10,.0f}" for w in werte)
          + f"   Mittel {werte.mean():>10,.0f}   RMSE {werte.mean() ** 0.5:>6,.0f} EUR")


def arbeitsauftrag1(d):
    print("=== Arbeitsauftrag 1: lineare Regression, MSE je Fold ===")
    lin = LinearRegression()
    zeige("k=2 (Wochen 1-78, 79-156)", mse_je_fold(lin, d, folds_nach_wochen(d, [(1, 78), (79, 156)])))
    zeige("k=3 (Jahre 2023, 2024, 2025)",
          mse_je_fold(lin, d, folds_nach_wochen(d, [(1, 52), (53, 104), (105, 156)])))
    zeige("k=4 (je 39 Wochen)", mse_je_fold(lin, d, folds_nach_wochen(d, [(i * 39 + 1, i * 39 + 39) for i in range(4)])))
    zeige("k=12 (je 13 Wochen, ein Quartal)",
          mse_je_fold(lin, d, folds_nach_wochen(d, [(i * 13 + 1, i * 13 + 13) for i in range(12)])))
    zeige("k=3 zufällig gemischt", -cross_val_score(
        lin, d[MERKMALE], d[ZIEL], cv=KFold(3, shuffle=True, random_state=42),
        scoring="neg_mean_squared_error"))
    zeige("k=3 Jahre ohne Spalte Woche", -cross_val_score(
        lin, d[MERKMALE[1:]], d[ZIEL], cv=folds_nach_wochen(d, [(1, 52), (53, 104), (105, 156)]),
        scoring="neg_mean_squared_error"))

    # Größte Fehler: wo liegen sie?
    res = pd.Series(index=d.index, dtype=float)
    for a, b in [(i * 13 + 1, i * 13 + 13) for i in range(12)]:
        te = d["Woche"].between(a, b)
        modell = LinearRegression().fit(d.loc[~te, MERKMALE], d.loc[~te, ZIEL])
        res[te] = d.loc[te, ZIEL] - modell.predict(d.loc[te, MERKMALE])
    print("\nWochen mit Fehler über 2.500 EUR (k=12):")
    print(d.assign(fehler=res.round())[res.abs() > 2500][["Woche", "Jahr", "KW", ZIEL, "fehler"]]
          .to_string(index=False))


def arbeitsauftrag2(d):
    print("\n=== Arbeitsauftrag 2: Random Forest und Gradient Boosting gegen linear (k=3, Jahre) ===")
    jahre = folds_nach_wochen(d, [(1, 52), (53, 104), (105, 156)])
    zeige("Linear", mse_je_fold(LinearRegression(), d, jahre))
    zeige("Random Forest (Standard)", mse_je_fold(RandomForestRegressor(random_state=42), d, jahre))
    zeige("Gradient Boosting (Standard)", mse_je_fold(GradientBoostingRegressor(random_state=42), d, jahre))

    raster = {"n_estimators": [100, 300, 500], "max_depth": [3, 5, 8, 12], "max_features": [2, 4, 7]}
    kombis = int(np.prod([len(v) for v in raster.values()]))
    laeufe = kombis * len(jahre)
    print(f"\nGrid Random Forest: {kombis} Kombinationen x {len(jahre)} Folds = {laeufe} Läufe")
    print(f"Rechenzeit laut Aufgabe: {laeufe * SEKUNDEN_PRO_LAUF / 60:.0f} Minuten "
          f"(+ 1 Endtraining = {(laeufe + 1) * SEKUNDEN_PRO_LAUF / 60:.1f} Minuten, Budget 60)")
    start = time.time()
    gs = GridSearchCV(RandomForestRegressor(random_state=42), raster, cv=jahre,
                      scoring="neg_mean_squared_error").fit(d[MERKMALE], d[ZIEL])
    print(f"Tatsächlich auf diesem Rechner: {time.time() - start:.0f} s")
    erg = pd.DataFrame(gs.cv_results_)
    erg["mse"] = -erg["mean_test_score"]
    spalten = ["param_n_estimators", "param_max_depth", "param_max_features", "mse"]
    print("\nBeste 5 Kombinationen:")
    print(erg.sort_values("mse")[spalten].head(5).round(0).to_string(index=False))
    print("\nBester MSE je Wert (über alle übrigen Einstellungen):")
    for p in ["param_max_depth", "param_n_estimators", "param_max_features"]:
        print(f"  {p[6:]:13s}", erg.groupby(p)["mse"].min().round(0).to_dict())

    kleines = {"n_estimators": [100, 300, 500], "learning_rate": [0.03, 0.1, 0.3], "max_depth": [2, 3, 5]}
    gb = GridSearchCV(GradientBoostingRegressor(random_state=42), kleines, cv=jahre,
                      scoring="neg_mean_squared_error").fit(d[MERKMALE], d[ZIEL])
    print(f"\nGradient Boosting (27 Kombinationen): bestes {gb.best_params_}, MSE {-gb.best_score_:,.0f}")


if __name__ == "__main__":
    daten = lade()
    arbeitsauftrag1(daten)
    arbeitsauftrag2(daten)
