"""Stufe 1: Baselines und Validierungsaufbau (Bericht 3.3 bis 3.5).
Ausführen: uv run python src/baselines.py   (Ausgabe: reports/baselines_output.txt, reports/results_baselines.csv)
Vorher: src/clean.py muss gelaufen sein.
"""
# %%
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
sys.path.insert(0, str(ROOT / "src"))
from forecast_eval import WINDOWS, load_clean, score, seasonal_baselines, targets_of, to_wide, window_frames  # noqa: E402

pd.set_option("display.width", 170)
lines = []


def out(msg=""):
    print(msg)
    lines.append(str(msg))


df = load_clean()
W_train = to_wide(df, "sales_train")  # maskiert: Spitzen, 25. Dezember, geschlossene Filialen = NaN
out(f"Reihen: {W_train.shape[1]}, Tage: {W_train.shape[0]}")

# %% [markdown]
# ## 1. Die drei Fenster
# Pro Fenster ist der **Ursprung** der letzte bekannte Tag. Die Baselines sehen nur Daten bis dahin.
# Danach folgen die 16 Tage, die wir vorhersagen und mit der Wahrheit vergleichen.

# %%
for name, origin in WINDOWS.items():
    t = targets_of(origin)
    out(f"{name}: Ursprung {origin.date()}, Prognose {t[0].date()} bis {t[-1].date()}")

# %% [markdown]
# ## 2. Baselines rechnen und bewerten
# - **B1 Vorwoche:** gleicher Wochentag, jüngster bekannter Wert (mit Verfall bis 4 Wochen zurück)
# - **B2 Mittel 4 Wochen:** Mittelwert der letzten 4 gleichen Wochentage
#
# Bewertet wird nur, wo es einen echten Wert gibt, der Tag nicht ausgeschlossen ist (geschlossene Tage und Filialen)
# und eine Prognose vorliegt. Zusätzlich zeigen wir den Fehler ohne die isolierten Spitzen.

# %%
rows, per_family = [], {}
for name, origin in WINDOWS.items():
    truth, excluded, outlier = window_frames(df, origin)
    preds = seasonal_baselines(W_train.loc[:origin], origin)
    for model, pred in preds.items():
        r = score(truth, pred, excluded, outlier)
        rows.append({"Fenster": name, "Modell": model, "RMSLE": r["rmsle"], "RMSLE ohne Spitzen": r["rmsle_ohne_spitzen"],
                     "bewertet": r["n_bewertet"], "ohne Prognose": r["n_ohne_prognose"], "ausgeschlossen": r["n_ausgeschlossen"]})
        per_family[(name, model)] = r["je_familie"]
res = pd.DataFrame(rows)
out("\n" + res.round(4).to_string(index=False))

# %% [markdown]
# ## 3. Benchmark
# Als Vergleichswert für die späteren Modelle gilt je Fenster die **bessere** der beiden Baselines.
# Das Erfolgskriterium (Bericht 3.4): mindestens 10 % niedrigerer RMSLE, im Mittel der drei Fenster
# und in mindestens zwei von drei einzeln.

# %%
pivot = res.pivot(index="Fenster", columns="Modell", values="RMSLE").reindex(list(WINDOWS))
pivot["Benchmark (beste Baseline)"] = pivot.min(axis=1)
out("\nRMSLE je Fenster:\n" + pivot.round(4).to_string())
bench = pivot["Benchmark (beste Baseline)"]
out(f"\nMittel über die drei Fenster: {bench.mean():.4f}")
out(f"Zielwert für ein Modell (10 % besser): Mittel <= {0.9 * bench.mean():.4f}, "
    f"je Fenster <= {', '.join(f'{k.split()[0]}: {0.9 * v:.4f}' for k, v in bench.items())}")

# %% [markdown]
# ## 4. Wo sind die Baselines schwach? Fehler je Produktfamilie (Fenster W1)
# Ein Gesamtwert versteckt, dass einige Familien viel schlechter laufen. Das zeigt, wo ein Modell am meisten gewinnen kann.

# %%
fam = pd.DataFrame({m: per_family[("W1 Aug 2017", m)] for m in ["B1 Vorwoche", "B2 Mittel 4 Wochen"]})
fam["beste"] = fam.min(axis=1)
out("\nFehler je Familie, W1 (sortiert, schlechteste zuerst):\n" + fam.sort_values("beste", ascending=False).round(3).to_string())

# %% [markdown]
# ## 5. Zwei Auffälligkeiten nachprüfen
# a) In W2 gibt es 99 Zellen ohne Prognose: welche Reihen sind das?
# b) `SCHOOL AND OFFICE SUPPLIES` hat im August einen Fehler von etwa 1,8, mehr als das Dreifache der anderen.
#    Hypothese: Schulbeginn. Wir sehen uns den Monatsabsatz an.

# %%
origin = WINDOWS["W2 Dez 2016"]
truth, excluded, outlier = window_frames(df, origin)
pred = seasonal_baselines(W_train.loc[:origin], origin)["B2 Mittel 4 Wochen"]
missing = (truth.notna() & ~excluded & pred.isna()).sum()
missing = missing[missing > 0]
out("\nW2: Reihen mit Wahrheit, aber ohne Prognose (Filiale, Familie: Tage):")
out(missing.to_string())
first = df[df.sales_train.notna()].groupby(["store_nbr", "family"]).date.min()
out("Erster verwertbarer Wert dieser Reihen:\n" + first.reindex(missing.index).dt.date.to_string())

# %%
school = df[df.family == "SCHOOL AND OFFICE SUPPLIES"].set_index("date").sales_train
monthly = school.groupby([school.index.year, school.index.month]).sum().unstack(0)
out("\nSCHOOL AND OFFICE SUPPLIES, Monatsabsatz (Zeilen = Monat, Spalten = Jahr):\n" + monthly.round(0).astype("Int64").to_string())

# %%
res.to_csv(ROOT / "reports" / "results_baselines.csv", index=False)
(ROOT / "reports" / "baselines_output.txt").write_text("\n".join(lines), encoding="utf-8")
