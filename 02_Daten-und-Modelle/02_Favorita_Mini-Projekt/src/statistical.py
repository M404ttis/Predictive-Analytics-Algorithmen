"""Stufe 2: Statistisches Modell je Reihe (exponentielle Glättung mit Wochenmuster), Bericht 3.5 und 3.7.
Ausführen: uv run python src/statistical.py   (Ausgabe: reports/statistical_output.txt, reports/results_statistical.csv)
Vorher: src/clean.py und src/baselines.py (für den Benchmark) müssen gelaufen sein.
"""
# %%
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
sys.path.insert(0, str(ROOT / "src"))
from forecast_eval import WINDOWS, load_clean, score, seasonal_baselines, to_wide, window_frames  # noqa: E402
from stat_models import ets_forecast  # noqa: E402

pd.set_option("display.width", 170)
lines = []


def out(msg=""):
    print(msg)
    lines.append(str(msg))


df = load_clean()
W_train = to_wide(df, "sales_train")

# %% [markdown]
# ## 1. Das Modell
# Für **jede** der 1.782 Reihen wird einzeln ein Holt-Winters-Modell angepasst (statsmodels `ExponentialSmoothing`):
# - Zielgröße `log1p(Absatz)`, danach Rücktransformation mit `expm1` und Begrenzung auf mindestens 0
# - **Level** (aktuelles Niveau, jüngere Tage zählen mehr) plus **additives Wochenmuster** (7 Tage), kein Trend
# - Historie: die letzten 365 Tage bis zum Prognose-Ursprung, maskierte Tage linear überbrückt
# - **Rückfall auf die Baseline** (Mittel 4 Wochen), wenn eine Reihe weniger als 28 verwertbare Tage hat oder ihr
#   letzter Wert mehr als 14 Tage vor dem Ursprung liegt
#
# Das Modell sieht keine Promotion, keine Feiertage, keine anderen Reihen. Es ist rein statistisch je Reihe.

# %%
rows, per_family, fallback_counts = [], {}, {}
for name, origin in WINDOWS.items():
    truth, excluded, outlier = window_frames(df, origin)
    b2 = seasonal_baselines(W_train.loc[:origin], origin)["B2 Mittel 4 Wochen"]
    pred, counts = ets_forecast(W_train, origin, fallback=b2)
    r = score(truth, pred, excluded, outlier)
    rows.append({"Fenster": name, "Modell": "ETS je Reihe", "RMSLE": r["rmsle"], "RMSLE ohne Spitzen": r["rmsle_ohne_spitzen"],
                 "bewertet": r["n_bewertet"], "ohne Prognose": r["n_ohne_prognose"]})
    per_family[name] = r["je_familie"]
    fallback_counts[name] = counts
res = pd.DataFrame(rows)
out(res.round(4).to_string(index=False))
out("\nReihen je Fenster: mit Modell / Rückfall zu wenig Daten / Rückfall zu alt / Fit-Fehler / gar keine Prognose")
for k, c in fallback_counts.items():
    out(f"{k}: {c['modell']} / {c['zu_wenig_daten']} / {c['zu_alt']} / {c['fit_fehler']} / {c['ohne_prognose']}")

# %% [markdown]
# ## 2. Vergleich mit dem Benchmark
# Benchmark = beste Baseline je Fenster (Mittel der letzten 4 gleichen Wochentage). Erfolgskriterium (Bericht 3.4):
# 10 % niedrigerer RMSLE im Mittel der drei Fenster und in mindestens zwei Fenstern einzeln.

# %%
base = pd.read_csv(ROOT / "reports" / "results_baselines.csv")
bench = base.pivot(index="Fenster", columns="Modell", values="RMSLE").min(axis=1).reindex(list(WINDOWS))
ets = res.set_index("Fenster").RMSLE
cmp_ = pd.DataFrame({"Benchmark": bench, "ETS je Reihe": ets})
cmp_["Änderung"] = (cmp_["ETS je Reihe"] / cmp_.Benchmark - 1).map("{:+.1%}".format)
cmp_["Ziel (-10 %)"] = (0.9 * cmp_.Benchmark).round(4)
cmp_["erreicht"] = cmp_["ETS je Reihe"] <= cmp_["Ziel (-10 %)"]
out("\n" + cmp_.round(4).to_string())
mean_b, mean_e = bench.mean(), ets.mean()
out(f"\nMittel: Benchmark {mean_b:.4f}, ETS {mean_e:.4f}, Änderung {mean_e / mean_b - 1:+.1%} (Ziel: {0.9 * mean_b:.4f})")
out(f"Erfolgskriterium: Mittel <= Ziel: {mean_e <= 0.9 * mean_b}; Fenster einzeln erreicht: {int(cmp_['erreicht'].sum())} von 3")

# %% [markdown]
# ## 3. Wo gewinnt, wo verliert das Modell? (Fehler je Familie, W1)

# %%
truth, excluded, outlier = window_frames(df, WINDOWS["W1 Aug 2017"])
b2_w1 = seasonal_baselines(W_train.loc[:WINDOWS["W1 Aug 2017"]], WINDOWS["W1 Aug 2017"])["B2 Mittel 4 Wochen"]
base_fam = score(truth, b2_w1, excluded, outlier)["je_familie"]
fam = pd.DataFrame({"B2 Baseline": base_fam, "ETS": per_family["W1 Aug 2017"]})
fam["Änderung"] = fam.ETS / fam["B2 Baseline"] - 1
out("\nFamilien in W1, größte Verbesserung zuerst:\n" + fam.sort_values("Änderung").assign(
    Änderung=lambda d: d.Änderung.map("{:+.1%}".format)).round(3).to_string())
out(f"\nFamilien mit besserem ETS: {(fam.ETS < fam['B2 Baseline']).sum()} von {len(fam)}")

# %% [markdown]
# ## 4. Empfindlichkeit: wie viel Historie?
# Die 365 Tage haben wir gewählt, nicht gemessen. Zum Vergleich 90 und 180 Tage.
# Achtung: Wir wählen hier anhand derselben Fenster, mit denen wir bewerten. Bei nur drei Varianten ist das tolerierbar,
# aber der Unterschied sollte größer als das Rauschen sein, bevor wir daraus etwas schließen.

# %%
sens = {}
for hd in (90, 180, 365):
    vals = []
    for name, origin in WINDOWS.items():
        truth, excluded, outlier = window_frames(df, origin)
        b2 = seasonal_baselines(W_train.loc[:origin], origin)["B2 Mittel 4 Wochen"]
        pred, _ = ets_forecast(W_train, origin, fallback=b2, history_days=hd)
        vals.append(score(truth, pred, excluded, outlier)["rmsle"])
    sens[f"{hd} Tage"] = vals
sens = pd.DataFrame(sens, index=list(WINDOWS))
sens.loc["Mittel"] = sens.mean()
out("\nRMSLE je Historienlänge:\n" + sens.round(4).to_string())

# %%
res.to_csv(ROOT / "reports" / "results_statistical.csv", index=False)
(ROOT / "reports" / "statistical_output.txt").write_text("\n".join(lines), encoding="utf-8")
