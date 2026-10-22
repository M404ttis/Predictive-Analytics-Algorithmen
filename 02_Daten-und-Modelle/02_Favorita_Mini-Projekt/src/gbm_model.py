"""Globales Gradient-Boosting (LightGBM) über alle Reihen, direkte Strategie. Bericht 3.4 (Entscheidungen 5 bis 9) und 3.8.

Eine Trainingszeile = (Reihe, Zieltag j, Abstand h zum Prognose-Ursprung i = j - h), h = 1..16.
Alle Eingaben aus Verkäufen stammen aus Tagen <= i. Kalender, Feiertage und Aktionen des Zieltags j
sind auch in der Zukunft bekannt (wie in test.csv).
Wird von src/gbm.py importiert.
"""
import warnings

import lightgbm as lgb
import numpy as np
import pandas as pd

from forecast_eval import HORIZON, to_wide

PARAMS = dict(
    objective="regression",       # L2 auf log1p(Absatz) = RMSLE
    learning_rate=0.05, num_leaves=63, min_data_in_leaf=100, feature_fraction=0.8,
    bagging_fraction=0.8, bagging_freq=1, lambda_l2=1.0, seed=42, deterministic=True,
    force_row_wise=True, verbose=-1, num_threads=0,
)
N_TREES = 500
CATEGORICAL = ["family", "store", "type", "city", "state"]
# Standardmäßig ohne Ölpreis (Bericht 3.4, Entscheidung 8); die Gegenprobe schaltet ihn ein.
DEFAULT_DROP = ("oel_ursprung",)


class Panel:
    """Alle Reihen als Zahlen-Tabellen (Zeit x Reihe), damit Merkmale vektorisiert entstehen."""

    def __init__(self, df):
        sales = to_wide(df, "sales_train")
        self.dates, self.cols = sales.index, sales.columns
        self.T, self.S = sales.shape
        self.y = np.log1p(sales.to_numpy(dtype=np.float32))  # NaN = maskiert/unbekannt
        ylog = pd.DataFrame(self.y, index=self.dates, columns=self.cols)
        self.rm = {w: ylog.rolling(w, min_periods=max(3, w // 4)).mean().to_numpy(np.float32) for w in (7, 28, 91, 364)}
        self.ffill = ylog.ffill().to_numpy(np.float32)
        valid = ~np.isnan(self.y)
        self.lastpos = np.maximum.accumulate(np.where(valid, np.arange(self.T)[:, None], -1), axis=0)
        self.firstpos = np.where(valid.any(0), valid.argmax(0), 10**6)

        def wide0(col):
            return to_wide(df, col, 0).reindex(self.dates, columns=self.cols).fillna(0).to_numpy(np.float32)

        oil = df.groupby("date").dcoilwtico.first().reindex(self.dates).ffill()
        self.oil = oil.to_numpy(np.float32)
        self.promo = np.log1p(wide0("onpromotion"))
        self.promo_known = wide0("promo_known")
        self.holiday, self.event, self.workday = wide0("is_holiday"), wide0("is_event"), wide0("is_workday")

        store = self.cols.get_level_values("store_nbr")
        info = df.drop_duplicates("store_nbr").set_index("store_nbr")[["cluster", "type", "city", "state"]].reindex(store)
        codes = lambda s: pd.Categorical(s).codes.astype(np.int16)
        self.static = {
            "family": codes(self.cols.get_level_values("family")), "store": codes(store),
            "type": codes(info.type.to_numpy()), "city": codes(info.city.to_numpy()),
            "state": codes(info.state.to_numpy()), "cluster": info.cluster.to_numpy(np.int16),
        }

    def features(self, j, s, h):
        """Merkmale für Zeilen (Zieltag-Index j, Reihen-Index s, Abstand h)."""
        i = j - h
        f = {"h": h}
        for w, arr in self.rm.items():
            f[f"mittel_{w}d"] = arr[i, s]
        f["letzter_wert"] = self.ffill[i, s]
        lp = self.lastpos[i, s]
        f["tage_seit_letztem_wert"] = np.where(lp >= 0, i - lp, np.nan)
        age = i - self.firstpos[s]
        f["alter_reihe"] = np.where(age >= 0, age, np.nan)
        m = np.ceil(h / 7).astype(int)  # gleicher Wochentag wie der Zieltag, aber nicht jünger als der Ursprung
        sw = []
        for k in range(4):
            idx = j - 7 * (m + k)
            v = np.where(idx >= 0, self.y[np.clip(idx, 0, None), s], np.nan)
            f[f"gleicher_wochentag_{k + 1}"] = v
            sw.append(v)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            f["gleicher_wochentag_mittel"] = np.nanmean(np.vstack(sw), axis=0)
        d = self.dates[j]
        f["wochentag"], f["tag_im_monat"], f["monat"] = d.dayofweek.to_numpy(), d.day.to_numpy(), d.month.to_numpy()
        f["oel_ursprung"] = self.oil[i]  # Ölpreis am Ursprung (der künftige Preis ist unbekannt)
        f["aktion"], f["aktion_bekannt"] = self.promo[j, s], self.promo_known[j, s]
        f["feiertag"], f["ereignis"], f["arbeitstag_ausgleich"] = self.holiday[j, s], self.event[j, s], self.workday[j, s]
        for name, arr in self.static.items():
            f[name] = arr[s]
        X = pd.DataFrame(f)
        for c in CATEGORICAL:
            X[c] = pd.Categorical(X[c], categories=np.unique(self.static[c]))
        return X

    def training_set(self, origin_idx, n_days=730, draws=2, seed=0, only_promo_known=False):
        """Zeilen mit bekanntem Label (Zieltag <= Ursprung). Je (Reihe, Zieltag) werden `draws` zufällige h gezogen."""
        rng = np.random.default_rng(seed)
        js = np.arange(max(origin_idx - n_days + 1, 40), origin_idx + 1)
        J, S = np.repeat(js, self.S), np.tile(np.arange(self.S), len(js))
        keep = ~np.isnan(self.y[J, S])
        if only_promo_known:  # nur Zieltage, an denen die Aktionsangabe der Filiale als verlässlich gilt
            keep &= self.promo_known[J, S] == 1
        J, S = J[keep], S[keep]
        parts_X, parts_y = [], []
        for _ in range(draws):
            h = rng.integers(1, HORIZON + 1, size=len(J))
            parts_X.append(self.features(J, S, h))
            parts_y.append(self.y[J, S])
        return pd.concat(parts_X, ignore_index=True), np.concatenate(parts_y)

    def forecast_set(self, origin_idx):
        j = origin_idx + np.arange(1, HORIZON + 1)
        J, S = np.repeat(j, self.S), np.tile(np.arange(self.S), HORIZON)
        return self.features(J, S, J - origin_idx), j


def fit_predict(panel, origin, n_days=730, draws=2, n_trees=N_TREES, drop=DEFAULT_DROP, seed=0, only_promo_known=False):
    """Trainiert mit Daten bis zum Ursprung und liefert die 16-Tage-Prognose (Tabelle Ziel-Datum x Reihe).

    drop              Merkmale, die weggelassen werden (für Gegenproben)
    seed              steuert die zufällige Auswahl der Abstände h und das Boosting (für Rauschtest)
    only_promo_known  nur Trainingszeilen mit verlässlicher Aktionsangabe
    """
    o = panel.dates.get_loc(origin)
    X, y = panel.training_set(o, n_days=n_days, draws=draws, seed=seed, only_promo_known=only_promo_known)
    X = X.drop(columns=list(drop))
    cats = [c for c in CATEGORICAL if c not in drop]
    params = {**PARAMS, "seed": 42 + seed}
    model = lgb.train(params, lgb.Dataset(X, label=y, categorical_feature=cats, free_raw_data=False), num_boost_round=n_trees)
    Xf, j = panel.forecast_set(o)
    p = np.clip(np.expm1(model.predict(Xf[X.columns])), 0, None).reshape(len(j), panel.S)
    return pd.DataFrame(p, index=panel.dates[j], columns=panel.cols), model, len(y)
