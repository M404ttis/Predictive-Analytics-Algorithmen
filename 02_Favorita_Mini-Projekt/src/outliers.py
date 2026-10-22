"""Ausreißer-Untersuchung Schritt für Schritt (Bericht 2.5 und 2.8).
Ausführen: uv run python src/outliers.py   (Ausgabe auch in reports/outliers_output.txt)
Vorher: src/clean.py muss gelaufen sein (liest data/clean/train_clean.parquet).

Die Schritte bauen aufeinander auf:
  1. Was markiert die bisherige Regel (10 x p99)?
  2. Einzelfälle ansehen: Nachbartage, andere Familien, andere Filialen
  3. Naive Regel (Verhältnis zum lokalen Median): zu viele Treffer, warum?
  4. Isolationsregel: nur echte Einzeltags-Spitzen
"""
# %%
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
pd.set_option("display.width", 170)
lines = []


def out(msg=""):
    print(msg)
    lines.append(str(msg))


# %%
t = pd.read_parquet(ROOT / "data/clean/train_clean.parquet")

# %% [markdown]
# ## 1. Bisherige Regel
# In einer früheren Fassung von `clean.py` hatten wir einen Tageswert als Ausreißer markiert, wenn er größer war als das 10-Fache des 99. Perzentils der eigenen Reihe.
# Frage: Was findet diese Regel, und was übersieht sie?

# %%
out("=== 1. Bisherige Regel (frühere Fassung von clean.py): Tageswert > 10 x 99. Perzentil der eigenen Reihe ===")
p99 = t[t.sales > 0].groupby(["store_nbr", "family"], observed=True).sales.quantile(0.99).rename("p99")
old = t.merge(p99, on=["store_nbr", "family"], how="left")
old = old[old.sales > 10 * old.p99].sort_values("sales", ascending=False)
out(f"markierte Zeilen: {len(old)}")
out(old.groupby(["store_nbr", "family"], observed=True).agg(n=("sales", "size"), max=("sales", "max"))
    .sort_values("max", ascending=False).head(10).to_string())

# %% [markdown]
# ## 2. Einzelfälle ansehen
# Bevor wir eine Regel festlegen, schauen wir uns die Fälle an.
# Leitfrage: Würde eine echte Nachfragewelle nur **eine** Reihe an **einem** Tag treffen? Wir prüfen Nachbartage, andere Familien derselben Filiale und dieselbe Familie in anderen Filialen.

# %%
out("\n=== 2. Einzelfälle: Umfeld ansehen ===")
out("Leitfrage: Würde eine echte Nachfragewelle nur diese eine Reihe an einem Tag treffen?")
cases = [(2, "GROCERY I", "2016-05-02"), (39, "MEATS", "2016-10-07"), (35, "GROCERY I", "2014-12-08"),
         (35, "GROCERY I", "2015-12-14"), (43, "POULTRY", "2015-10-03"), (12, "MEATS", "2016-10-13"),
         (2, "GROCERY I", "2016-04-26")]  # letzter Fall: von der alten Regel NICHT markiert
for store, fam, day in cases:
    d = pd.Timestamp(day)
    s = t[(t.store_nbr == store) & (t.family == fam)].set_index("date")
    w = s.loc[d - pd.Timedelta(days=4): d + pd.Timedelta(days=4), ["sales", "onpromotion", "is_holiday", "is_event"]]
    out(f"\n--- Filiale {store} · {fam} · {day} ---")
    out(w.to_string())
    before = s.sales[(s.index >= d - pd.Timedelta(days=60)) & (s.index < d)]
    out(f"Median / Max der 60 Tage davor: {before.median():.0f} / {before.max():.0f}")
    day_all = t[t.date == d]
    same_fam = day_all[day_all.family == fam].sales
    out(f"Gleiche Familie, andere Filialen am Tag: Median {same_fam.median():.0f}; "
        f"Rang dieser Filiale {int((same_fam > s.loc[d, 'sales']).sum()) + 1} von {len(same_fam)}")
    top = day_all[day_all.store_nbr == store].sort_values("sales", ascending=False).head(3)
    out("Top-3-Familien dieser Filiale am Tag: " + str(dict(zip(top.family.astype(str), top.sales.round(0)))))

# %% [markdown]
# ## 3. Naive Regel: Verhältnis zum lokalen Median
# Wir vergleichen jeden Tag mit dem Median der umliegenden 29 Tage. Ergebnis: zu viele Treffer. Warum? Weil **Saison** (Dezember) und **Niveausprünge** (Wiedereröffnung) wie Ausreißer aussehen, aber echt sind.

# %%
out("\n=== 3. Naive Regel: Tageswert > 8 x lokaler Median (29 Tage zentriert) und > 300 Einheiten ===")
ok = t[(t.is_closed_day == 0) & (t.is_store_closed == 0)].sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)
g = ok.groupby(["store_nbr", "family"], observed=True).sales
ok["med29"] = g.transform(lambda s: s.rolling(29, center=True, min_periods=15).median())
naive = ok[(ok.sales / ok.med29.clip(lower=1) > 8) & (ok.sales > 300)]
out(f"Treffer: {len(naive)}")
out("Treffer nach Monat (Top 5): " + str(naive.groupby(naive.date.dt.to_period('M')).size().sort_values(ascending=False).head(5).to_dict()))
out(f"Davon im Dezember: {(naive.date.dt.month == 12).sum()}  -> saisonale Spitzen, keine Fehler")
s24 = naive[(naive.store_nbr == 24) & (naive.family == "PRODUCE")]
out(f"Filiale 24 PRODUCE im Juli 2014: {len(s24)} Treffer -> Neustart nach Wiedereröffnung (Niveausprung), kein Fehler")

# %% [markdown]
# ## 4. Isolationsregel
# Ein Fehlerverdacht ist nur ein Tag, der **vorher und nachher** normal umgeben ist. Ein Niveausprung oder eine Saisonwelle hält mehrere Tage an. Diese Regel trennt die drei Fälle (Fehler, Saison, Niveausprung).

# %%
out("\n=== 4. Isolationsregel: > 10 x Median der 4 Tage davor UND der 4 Tage danach, und > 500 Einheiten ===")
before = g.transform(lambda s: s.shift(1).rolling(4, min_periods=3).median())
after = g.transform(lambda s: s[::-1].shift(1).rolling(4, min_periods=3).median()[::-1])
ok["ref"] = pd.concat([before, after], axis=1).max(axis=1)  # strengerer der beiden Bezugswerte
ok["ratio"] = ok.sales / ok.ref.clip(lower=1)
spikes = ok[(ok.ratio > 10) & (ok.sales > 500)]
out(f"isolierte Spitzen: {len(spikes)}  ({len(spikes) / len(ok):.4%} der Zeilen, "
    f"{spikes.sales.sum() / ok.sales.sum():.2%} des Gesamtabsatzes)")
out("nach Familie (Top 6): " + str(spikes.groupby("family", observed=True).size().sort_values(ascending=False).head(6).to_dict()))
out("nach Monat (Top 5):   " + str(spikes.groupby(spikes.date.dt.to_period('M')).size().sort_values(ascending=False).head(5).to_dict()))
show = spikes.sort_values("sales", ascending=False)[["date", "store_nbr", "family", "sales", "ref", "ratio"]].head(15)
out("\nGrößte isolierte Spitzen:")
out(show.assign(date=show.date.dt.date, sales=show.sales.round(0), ref=show.ref.round(0), ratio=show.ratio.round(0)).to_string(index=False))
out(f"\nKontrolle gegen clean.py: is_outlier = 1 in train_clean.parquet: {int(t.is_outlier.sum())} "
    f"(hier gefunden: {len(spikes)}) -> {'gleich' if int(t.is_outlier.sum()) == len(spikes) else 'ABWEICHUNG'}")
s35 = spikes[(spikes.store_nbr == 35) & (spikes.family == "GROCERY I")]
out(f"\nFiliale 35 GROCERY I, Spitzen: {[str(d.date()) for d in s35.date]}  (jedes Jahr im Dezember: wiederkehrend?)")

# %% [markdown]
# ## 5. Wie empfindlich ist die Schwelle?
# Die Zahl 10 haben wir gewählt, nicht gemessen. Wir sehen nach, wie sich die Trefferzahl mit dem Faktor ändert und welche
# großen Werte knapp unter der Schwelle bleiben.

# %%
out("\n=== 5. Empfindlichkeit der Schwelle (Mindestmenge 500 Einheiten) ===")
for factor in (5, 8, 10, 15, 20):
    out(f"Faktor {factor:>2}: {int(((ok.ratio > factor) & (ok.sales > 500)).sum()):>4} Treffer")
near = ok[(ok.ratio > 5) & (ok.ratio <= 10) & (ok.sales > 20000)].sort_values("sales", ascending=False)
out("\nGroße Werte (> 20.000) mit Faktor zwischen 5 und 10, von der Regel NICHT markiert:")
out(near[["date", "store_nbr", "family", "sales", "ref", "ratio"]].assign(
    date=near.date.dt.date, sales=near.sales.round(0), ref=near.ref.round(0), ratio=near.ratio.round(1)).to_string(index=False))

# %%
(ROOT / "reports" / "outliers_output.txt").write_text("\n".join(lines), encoding="utf-8")
