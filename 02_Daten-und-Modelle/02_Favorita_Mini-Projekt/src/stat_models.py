"""Statistisches Modell je Reihe: exponentielle Glättung mit Wochenmuster (Holt-Winters), Bericht 3.5 Stufe 2.
Wird von src/statistical.py importiert.
"""
import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from forecast_eval import targets_of

MIN_POINTS = 28   # weniger verwertbare Tage -> Rückfall auf Baseline
MAX_STALE = 14    # letzter verwertbarer Wert älter als so viele Tage vor dem Ursprung -> Rückfall


def ets_forecast(W, origin, fallback, history_days=365):
    """Je Reihe: Level + additives Wochenmuster auf log1p(Absatz), 16 Tage voraus.

    W        Tabelle (Datum x Reihe) mit sales_train (NaN = maskiert/unbekannt)
    fallback Tabelle (Ziel-Datum x Reihe) mit der Baseline, wird genutzt, wenn die Reihe zu dünn oder zu alt ist
    Rückgabe: Prognose-Tabelle und Zähler, wie oft zurückgefallen wurde.
    """
    targets = targets_of(origin)
    hist = np.log1p(W.loc[:origin].iloc[-history_days:])
    pred = fallback.copy()
    counts = {"modell": 0, "zu_wenig_daten": 0, "zu_alt": 0, "fit_fehler": 0, "ohne_prognose": 0}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for col in hist.columns:
            y = hist[col]
            valid = y.dropna()
            if len(valid) < MIN_POINTS:
                counts["zu_wenig_daten"] += 1
                continue
            if (origin - valid.index[-1]).days > MAX_STALE:
                counts["zu_alt"] += 1
                continue
            y = y.loc[valid.index[0]:].interpolate(limit_direction="both")  # Lücken (maskiert) linear überbrücken
            try:
                fit = ExponentialSmoothing(y.to_numpy(), trend=None, seasonal="add", seasonal_periods=7,
                                           initialization_method="estimated").fit()
                f = np.clip(np.expm1(fit.forecast(len(targets))), 0, None)
            except Exception:
                counts["fit_fehler"] += 1
                continue
            pred[col] = f
            counts["modell"] += 1
    counts["ohne_prognose"] = int(pred.isna().all().sum())
    return pred, counts
