"""Stufe 3: Globales Gradient-Boosting (LightGBM), Bericht 3.8.
Ausführen: uv run python src/gbm.py   (Ausgabe: reports/gbm_output.txt, reports/results_gbm.csv, reports/gbm_importance.csv)
Vorher: src/clean.py, src/baselines.py und src/statistical.py müssen gelaufen sein.
"""
# %%
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
sys.path.insert(0, str(ROOT / "src"))
from forecast_eval import WINDOWS, load_clean, score, seasonal_baselines, to_wide, window_frames  # noqa: E402
from gbm_model import Panel, fit_predict  # noqa: E402
from stat_models import ets_forecast  # noqa: E402

pd.set_option("display.width", 170)
lines = []


def out(msg=""):
    print(msg)
    lines.append(str(msg))


df = load_clean()
W_train = to_wide(df, "sales_train")
panel = Panel(df)
out(f"Reihen: {panel.S}, Tage: {panel.T}")

# %% [markdown]
# ## 1. Das Modell
# **Ein** Modell für alle 1.782 Reihen (LightGBM, 500 Bäume). Eine Trainingszeile beschreibt eine Reihe, einen Zieltag und den
# Abstand `h` (1 bis 16 Tage) zum Prognose-Ursprung. Zielgröße `log1p(Absatz)`.
#
# **Eingaben aus der Vergangenheit** (nur Tage bis zum Ursprung):
# Mittel der letzten 7, 28, 91 und 364 Tage, letzter bekannter Wert, Tage seit diesem Wert, Alter der Reihe, die 4 letzten
# Werte des gleichen Wochentags wie der Zieltag und ihr Mittel.
#
# **Eingaben, die auch in der Zukunft bekannt sind:** Wochentag, Tag im Monat, Monat, Feiertag, Ereignis, Arbeitstag-Ausgleich,
# Aktion (`onpromotion`), `promo_known`, Filiale, Familie, Filialtyp, Stadt, Region, Cluster.
#
# **Training:** je Fenster die 730 Tage vor dem Ursprung, je (Reihe, Zieltag) zwei zufällige Abstände. Das Label eines
# Trainingstags liegt immer vor dem Ursprung. Maskierte Tage (`sales_train` = NaN) sind weder Label noch Eingabe.
# Ohne Ölpreis (Bericht 3.4, Entscheidung 8).

# %%
rows, per_family_w1, importances, models = [], {}, [], {}
for name, origin in WINDOWS.items():
    t0 = time.time()
    pred, model, n_rows = fit_predict(panel, origin)
    truth, excluded, outlier = window_frames(df, origin)
    r = score(truth, pred, excluded, outlier)
    rows.append({"Fenster": name, "Modell": "LightGBM", "RMSLE": r["rmsle"], "RMSLE ohne Spitzen": r["rmsle_ohne_spitzen"],
                 "bewertet": r["n_bewertet"], "ohne Prognose": r["n_ohne_prognose"]})
    if name.startswith("W1"):
        per_family_w1 = r["je_familie"]
    importances.append(pd.Series(model.feature_importance("gain"), index=model.feature_name(), name=name))
    out(f"{name}: RMSLE {r['rmsle']:.4f} (Trainingszeilen {n_rows:,}, {time.time() - t0:.0f} s)")
res = pd.DataFrame(rows)

# %% [markdown]
# ## 2. Vergleich mit Benchmark und statistischem Modell
# Erfolgskriterium (Bericht 3.4): RMSLE mindestens 10 % unter der besten Baseline, im Mittel der drei Fenster
# und in mindestens zwei Fenstern einzeln.

# %%
base = pd.read_csv(ROOT / "reports" / "results_baselines.csv")
bench = base.pivot(index="Fenster", columns="Modell", values="RMSLE").min(axis=1).reindex(list(WINDOWS))
ets = pd.read_csv(ROOT / "reports" / "results_statistical.csv").set_index("Fenster").RMSLE.reindex(list(WINDOWS))
gbm = res.set_index("Fenster").RMSLE
cmp_ = pd.DataFrame({"Benchmark": bench, "ETS": ets, "LightGBM": gbm})
cmp_["LightGBM vs. Benchmark"] = (cmp_.LightGBM / cmp_.Benchmark - 1).map("{:+.1%}".format)
cmp_["LightGBM vs. ETS"] = (cmp_.LightGBM / cmp_.ETS - 1).map("{:+.1%}".format)
cmp_["Ziel (-10 %)"] = (0.9 * cmp_.Benchmark)
cmp_["erreicht"] = cmp_.LightGBM <= cmp_["Ziel (-10 %)"]
out("\n" + cmp_.round(4).to_string())
out(f"\nMittel: Benchmark {bench.mean():.4f}, ETS {ets.mean():.4f}, LightGBM {gbm.mean():.4f} "
    f"({gbm.mean() / bench.mean() - 1:+.1%} gegen Benchmark; Ziel {0.9 * bench.mean():.4f})")
out(f"Erfolgskriterium: Mittel erreicht: {gbm.mean() <= 0.9 * bench.mean()}; Fenster einzeln erreicht: {int(cmp_['erreicht'].sum())} von 3")

# %% [markdown]
# ## 3. Wo gewinnt LightGBM gegenüber ETS? Fehler je Familie, Fenster W1

# %%
o1 = WINDOWS["W1 Aug 2017"]
truth, excluded, outlier = window_frames(df, o1)
b2 = seasonal_baselines(W_train.loc[:o1], o1)["B2 Mittel 4 Wochen"]
ets_w1, _ = ets_forecast(W_train, o1, fallback=b2)
ets_fam = score(truth, ets_w1, excluded, outlier)["je_familie"]
fam = pd.DataFrame({"ETS": ets_fam, "LightGBM": per_family_w1})
fam["Änderung"] = fam.LightGBM / fam.ETS - 1
out("\nFamilien in W1, größte Verbesserung gegenüber ETS zuerst:\n" + fam.sort_values("Änderung").assign(
    Änderung=lambda d: d.Änderung.map("{:+.1%}".format)).round(3).to_string())
out(f"\nFamilien mit besserem LightGBM: {(fam.LightGBM < fam.ETS).sum()} von {len(fam)}")

# %% [markdown]
# ## 4. Was nutzt das Modell? Wichtigkeit der Merkmale
# Die Wichtigkeit (Gain) sagt, wie viel Fehler ein Merkmal beim Trainieren insgesamt abgebaut hat. Sie zeigt
# **Nutzung**, nicht Ursache: Ein wichtiges Merkmal ist nicht automatisch der Grund für den Absatz.

# %%
imp = pd.concat(importances, axis=1)
imp["Anteil"] = (imp.mean(axis=1) / imp.mean(axis=1).sum())
imp = imp.sort_values("Anteil", ascending=False)
out("\nMerkmalswichtigkeit (Anteil am Gesamt-Gain, Mittel der drei Fenster):\n" + imp[["Anteil"]].assign(
    Anteil=lambda d: (d.Anteil * 100).round(1).astype(str) + " %").to_string())

# %%
res.to_csv(ROOT / "reports" / "results_gbm.csv", index=False)
imp.to_csv(ROOT / "reports" / "gbm_importance.csv")
(ROOT / "reports" / "gbm_output.txt").write_text("\n".join(lines), encoding="utf-8")
