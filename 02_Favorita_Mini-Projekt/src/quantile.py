"""Phase I: Quantil-Prognosen (Median, 75 %, 90 %) für den Nachbestell-Bedarf. Bericht 3.10.
Ausführen: uv run python -u src/quantile.py   (dauert ca. 10 Minuten; Ausgabe: reports/quantile_output.txt, reports/results_quantile.csv, reports/forecast_next16.csv)
Vorher: src/clean.py muss gelaufen sein.
"""
# %%
import sys
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
sys.path.insert(0, str(ROOT / "src"))
from forecast_eval import HORIZON, WINDOWS, load_clean, window_frames  # noqa: E402
from gbm_model import CATEGORICAL, DEFAULT_DROP, PARAMS, N_TREES, Panel  # noqa: E402

pd.set_option("display.width", 170)
lines = []


def out(msg=""):
    print(msg, flush=True)
    lines.append(str(msg))


ALPHAS = (0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9)

# %% [markdown]
# ## 1. Was ist ein Quantil-Modell?
# Das Basismodell (Bericht 3.8) minimiert den quadrierten Fehler auf `log1p(Absatz)` und liefert einen **typischen** Wert.
# Hier ändert sich nur die Verlustfunktion: `objective="quantile"` mit `alpha`.
# Der Absatz liegt dann in `alpha` aller Fälle **höchstens** so hoch wie die Prognose.
# `alpha = 0.9` heißt: an 9 von 10 Tagen reicht der Bestand, an 1 von 10 Tagen nicht.
# Quantile bleiben bei monotonen Umrechnungen erhalten, daher ist `expm1` des Log-Quantils das Quantil des Absatzes.
# Je Quantil wird ein eigenes Modell trainiert. Danach werden die Werte je Zelle sortiert, damit sich Quantile nicht kreuzen.


# %%
def fit_predict_quantiles(panel, origin, alphas=ALPHAS, n_days=730, draws=2, n_trees=N_TREES, drop=DEFAULT_DROP, seed=0):
    """Je alpha ein LightGBM-Modell; Rückgabe: {alpha: Tabelle Zieldatum x Reihe} in Stück (nicht log)."""
    o = panel.dates.get_loc(origin)
    X, y = panel.training_set(o, n_days=n_days, draws=draws, seed=seed)
    X = X.drop(columns=list(drop))
    cats = [c for c in CATEGORICAL if c not in drop]
    Xf, j = panel.forecast_set(o)
    raw = {}
    for a in alphas:
        params = {**PARAMS, "objective": "quantile", "alpha": a, "seed": 42 + seed}
        model = lgb.train(params, lgb.Dataset(X, label=y, categorical_feature=cats, free_raw_data=False), num_boost_round=n_trees)
        raw[a] = model.predict(Xf[X.columns])
    stacked = np.sort(np.stack([raw[a] for a in alphas]), axis=0)  # Quantile nicht kreuzen lassen
    return {
        a: pd.DataFrame(np.clip(np.expm1(stacked[k]), 0, None).reshape(len(j), panel.S), index=panel.dates[j], columns=panel.cols)
        for k, a in enumerate(alphas)
    }


def pinball_log(truth, pred, a):
    """Mittlerer Pinball-Verlust auf log1p-Skala (das Trainingsziel eines Quantil-Modells)."""
    d = np.log1p(truth) - np.log1p(pred)
    return float(np.nanmean(np.maximum(a * d, (a - 1) * d).to_numpy(dtype=float)))


# %% [markdown]
# ## 2. Prüfung in den drei Fenstern
# **Abdeckung** = Anteil der Zellen, in denen der echte Absatz <= Prognose war. Soll ≈ alpha sein.
# **Aufschlag** = Mittel der Quantil-Prognose in Stück geteilt durch die des Medians (wie viel mehr Bestand das kostet).
# **Summe 16 Tage**: Die Tagesprognosen werden je Reihe aufsummiert und mit dem echten 16-Tage-Absatz verglichen.
# Dabei werden nur Reihen ohne Schließtage im Fenster gezählt.

# %%
df = load_clean()
panel = Panel(df)
rows, fam_cov = [], {}
for name, origin in WINDOWS.items():
    t0 = time.time()
    preds = fit_predict_quantiles(panel, origin)
    truth, excluded, _ = window_frames(df, origin)
    valid = truth.notna() & ~excluded
    t_eff = truth.where(valid)
    full_series = valid.all(axis=0)  # Reihen mit 16 gültigen Tagen
    total_truth = truth.loc[:, full_series].sum()
    for a, p in preds.items():
        hit = (t_eff <= p).where(valid)
        cov = float(np.nanmean(hit.to_numpy(dtype=float)))
        cov_total = float((total_truth <= p.loc[:, full_series].sum()).mean())
        rows.append({
            "Fenster": name, "alpha": a, "Abdeckung": cov, "Abdeckung Summe 16 Tage": cov_total,
            "Pinball (log)": pinball_log(t_eff, p, a),
            "Aufschlag vs. Median": float(p.where(valid).sum().sum() / preds[0.5].where(valid).sum().sum()),
        })
        if a == 0.9 and name.startswith("W1"):
            fam = pd.Series(hit.columns.get_level_values("family"), index=hit.columns)
            fam_cov = {f: float(np.nanmean(hit[list(c.index)].to_numpy(dtype=float))) for f, c in fam.groupby(fam)}
    out(f"{name}: fertig ({time.time() - t0:.0f} s)")

res = pd.DataFrame(rows)
out("\n" + res.round(4).to_string(index=False))
avg = res.groupby("alpha")[["Abdeckung", "Abdeckung Summe 16 Tage", "Pinball (log)", "Aufschlag vs. Median"]].mean()
out("\nMittel der drei Fenster:\n" + avg.round(4).to_string())

# %% [markdown]
# ## 2b. Welches Quantil passt für die 16-Tage-Summe?
# Wer für 16 Tage auf einmal bestellt, braucht nicht das 90-%-Quantil jedes Tages, sondern ein Quantil, dessen **Summe** in 90 % der Fälle reicht.
# Gesucht: das alpha, bei dem „Abdeckung Summe 16 Tage“ nahe 0,9 liegt. Es wurde auf denselben drei Fenstern gesucht, an denen es geprüft wird;
# daher zählt vor allem, ob die Fenster einzeln nahe beieinander liegen.

# %%
tot = res.pivot(index="alpha", columns="Fenster", values="Abdeckung Summe 16 Tage")
tot["Mittel"] = tot.mean(axis=1)
tot["Aufschlag vs. Median"] = res.groupby("alpha")["Aufschlag vs. Median"].mean()
out("\nAbdeckung der 16-Tage-Summe je alpha:\n" + tot.round(3).to_string())
best = (tot.Mittel - 0.9).abs().idxmin()
out(f"\nalpha mit Summen-Abdeckung am nächsten an 90 %: {best}")

# %% [markdown]
# ## 3. Wo ist das 90-%-Quantil zu knapp? (Fenster W1)
# Familien mit der niedrigsten Abdeckung. Dort reicht der Bestand häufiger nicht, als das Ziel von 90 % verspricht.

# %%
fc = pd.Series(fam_cov).sort_values()
out("\nAbdeckung des 90-%-Quantils je Familie (W1), niedrigste 5:\n" + fc.head(5).map("{:.1%}".format).to_string())
out("\nhöchste 5:\n" + fc.tail(5).map("{:.1%}".format).to_string())

# %% [markdown]
# ## 4. Prognose für die nächsten 16 Tage (16.–31.08.2017)
# Ursprung = letzter Trainingstag 2017-08-15. Kalender, Feiertage und Aktionen der Tage danach stehen in `test.csv`.
# Echte Werte gibt es nicht, die Prognose ist eine Demonstration. Vertrauen kommt aus den Abdeckungen oben.

# %%
test = pd.read_parquet(ROOT / "data/clean/test_clean.parquet")
test["family"] = test.family.astype(str)
test["is_outlier"] = 0
ext = pd.concat([df, test], ignore_index=True)
origin = df.date.max()
preds = fit_predict_quantiles(Panel(ext), origin)
long = []
for a, p in preds.items():
    s = p.stack(["store_nbr", "family"]).rename(f"q{round(a * 100)}")
    long.append(s)
fc_out = pd.concat(long, axis=1).round(2).reset_index().rename(columns={"level_0": "date"})
fc_out = fc_out.rename(columns={fc_out.columns[0]: "date"})
closed = test.set_index(["date", "store_nbr", "family"])[["is_closed_day", "is_store_closed"]].max(axis=1).rename("geschlossen")
fc_out = fc_out.merge(closed.reset_index(), on=["date", "store_nbr", "family"], how="left")
fc_out.to_csv(ROOT / "reports" / "forecast_next16.csv", index=False)
out(f"\nPrognose geschrieben: {len(fc_out)} Zeilen ({fc_out.date.min().date()} bis {fc_out.date.max().date()})")
tot = fc_out[fc_out.geschlossen == 0].groupby("family")[["q50", "q75", "q90"]].sum().sort_values("q50", ascending=False)
out("\nSumme 16 Tage je Familie (Stück), größte 5, nur offene Tage, Summe der Tageswerte:\n" + tot.head(5).round(0).to_string())

# %%
res.to_csv(ROOT / "reports" / "results_quantile.csv", index=False)
(ROOT / "reports" / "quantile_output.txt").write_text("\n".join(lines), encoding="utf-8")
