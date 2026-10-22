"""Gemeinsamer Auswertungscode: Validierungsfenster, RMSLE, Baselines (Bericht 3.3 bis 3.5).
Wird von den Modell-Skripten importiert, nicht direkt ausgeführt.
"""
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
HORIZON = 16

# Prognose-Ursprung = letzter bekannter Tag. Alles danach ist für das Modell unbekannt.
WINDOWS = {
    "W1 Aug 2017": pd.Timestamp("2017-07-30"),
    "W2 Dez 2016": pd.Timestamp("2016-12-08"),
    "W3 Mär 2017": pd.Timestamp("2017-03-07"),
}


def targets_of(origin):
    """Die 16 Tage nach dem Ursprung."""
    return pd.date_range(origin + pd.Timedelta(days=1), periods=HORIZON)


def load_clean():
    df = pd.read_parquet(ROOT / "data/clean/train_clean.parquet")
    df["family"] = df.family.astype(str)
    return df


def to_wide(df, col, fill=None):
    """Tabelle (Datum x Reihe) mit einer Spalte je Filiale x Familie."""
    w = df.pivot(index="date", columns=["store_nbr", "family"], values=col)
    w = w.reindex(pd.date_range(w.index.min(), w.index.max()))
    return w if fill is None else w.fillna(fill)


def seasonal_baselines(W, origin, n_weeks=4):
    """Zwei einfache Baselines je Reihe, nur aus Daten bis zum Ursprung.

    B1 'Vorwoche':      gleicher Wochentag, jüngster verfügbarer Wert der letzten n_weeks Wochen
    B2 'Mittel 4 Wo.':  Mittelwert der letzten n_weeks gleichen Wochentage
    W ist die maskierte Tabelle (sales_train): Spitzen und geschlossene Tage sind NaN und zählen nicht mit.
    """
    targets = targets_of(origin)
    b1 = pd.DataFrame(np.nan, index=targets, columns=W.columns)
    b2 = b1.copy()
    for d in targets:
        m = int(np.ceil((d - origin).days / 7))  # so viele Wochen zurück, bis der Tag <= Ursprung liegt
        dates = [d - pd.Timedelta(days=7 * (m + j)) for j in range(n_weeks)]
        vals = W.reindex(dates).to_numpy()
        assert max(dates) <= origin
        latest = np.full(vals.shape[1], np.nan)
        for row in vals:                                  # jüngster Wert zuerst
            latest = np.where(np.isnan(latest), row, latest)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)  # Reihen ohne jeden Wert
            mean = np.nanmean(vals, axis=0)
        b1.loc[d], b2.loc[d] = latest, mean
    return {"B1 Vorwoche": b1, "B2 Mittel 4 Wochen": b2}


def rmsle_matrix(truth, pred):
    """Quadrierte Log-Fehler je Zelle: (log1p(pred) - log1p(truth))^2."""
    return (np.log1p(np.clip(pred, 0, None)) - np.log1p(truth)) ** 2


def score(truth, pred, excluded, outlier):
    """RMSLE für ein Fenster.

    truth, pred, excluded, outlier: Tabellen (Datum x Reihe) mit gleichem Index/Spalten.
    Bewertet wird nur, wo es einen echten Wert gibt (truth), der Tag nicht ausgeschlossen ist
    (geschlossene Tage/Filialen) und eine Prognose vorliegt.
    Rückgabe: Gesamtwerte und Fehler je Familie.
    """
    err = rmsle_matrix(truth, pred)
    have_truth = truth.notna() & ~excluded
    valid = have_truth & pred.notna()
    valid_wo = valid & ~outlier

    def rmsle_of(mask, cols=None):
        e = err.where(mask)
        if cols is not None:
            e = e[cols]
        vals = e.to_numpy(dtype=float)
        return float(np.sqrt(np.nanmean(vals))) if np.isfinite(vals).any() else np.nan

    fam = pd.Series(err.columns.get_level_values("family"), index=err.columns)
    return {
        "rmsle": rmsle_of(valid),
        "rmsle_ohne_spitzen": rmsle_of(valid_wo),
        "n_bewertet": int(valid.to_numpy().sum()),
        "n_ohne_prognose": int((have_truth & pred.isna()).to_numpy().sum()),
        "n_ausgeschlossen": int((truth.notna() & excluded).to_numpy().sum()),
        "je_familie": {f: rmsle_of(valid, list(cols.index)) for f, cols in fam.groupby(fam)},
    }


def window_frames(df, origin):
    """Wahrheit und Ausschluss-Flags für das 16-Tage-Fenster nach dem Ursprung."""
    targets = targets_of(origin)
    truth = to_wide(df, "sales").reindex(targets)
    excluded = ((to_wide(df, "is_closed_day", 0) + to_wide(df, "is_store_closed", 0)) > 0).reindex(targets).fillna(False)
    outlier = (to_wide(df, "is_outlier", 0) > 0).reindex(targets).fillna(False)
    return truth, excluded, outlier
