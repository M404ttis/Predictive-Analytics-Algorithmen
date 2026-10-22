"""Regel für isolierte Spitzen (Bericht 2.9), gemeinsam genutzt von clean.py und den Gegenproben."""
import pandas as pd


def spike_flags(df, factor=10, min_units=500):
    """Boolesche Reihe (Index wie df): True bei isolierten Spitzen.

    Eine Zeile ist eine Spitze, wenn sie mehr als `factor` mal so groß ist wie der Median der 4 Tage davor UND der 4 Tage
    danach (der strengere Bezugswert zählt) und mindestens `min_units` hat. Geschlossene Tage/Filialen zählen nicht mit.
    df muss nach (store_nbr, family, date) sortiert sein und die Spalten sales, is_closed_day, is_store_closed haben.
    """
    open_rows = (df.is_closed_day == 0) & (df.is_store_closed == 0)
    ok = df.loc[open_rows, ["store_nbr", "family", "sales"]]
    g = ok.groupby(["store_nbr", "family"], observed=True).sales
    before = g.transform(lambda x: x.shift(1).rolling(4, min_periods=3).median())
    after = g.transform(lambda x: x[::-1].shift(1).rolling(4, min_periods=3).median()[::-1])
    ref = pd.concat([before, after], axis=1).max(axis=1).clip(lower=1)
    spike = (ok.sales > factor * ref) & (ok.sales > min_units)
    out = pd.Series(False, index=df.index)
    out.loc[spike[spike].index] = True
    return out
