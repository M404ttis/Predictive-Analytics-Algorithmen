"""Zwei Untersuchungen aus dem Bericht (Abschnitte 2.4 und 2.8), nachvollziehbar als Skript.
Ausführen: uv run python src/explore_promo_closures.py   (Ausgabe auch in reports/explore_promo_closures_output.txt)
Vorher: src/clean.py muss gelaufen sein (liest data/clean/train_clean.parquet).
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


raw = pd.read_csv(ROOT / "data/raw/train.csv", parse_dates=["date"])

# %% [markdown]
# ## A. Wann beginnt die Promotion?
# Gibt es ein einheitliches Startdatum, oder startet jede Filiale anders? Das entscheidet, wie wir `promo_known` definieren (Bericht 2.4).

# %%
out("=== A. Wann beginnt die Promotion? (Bericht 2.4) ===")
out("Frage: gibt es ein einheitliches Startdatum, oder startet jede Filiale anders?")
promo = raw[raw.onpromotion > 0]
first_store = promo.groupby("store_nbr").date.min()
first_fam = promo.groupby("family").date.min()
out("\nErste Aktion je Filiale (Datum: Anzahl Filialen):")
out(first_store.value_counts().sort_index().to_string())
out(f"Filialen ohne je eine Aktion: {raw.store_nbr.nunique() - len(first_store)}")
out("\nErste Aktion je Familie (Datum: Anzahl Familien):")
out(first_fam.value_counts().sort_index().to_string())
out(f"Familien ohne je eine Aktion: {sorted(set(raw.family) - set(first_fam.index))}")
out("\nSpäte Starter (erste Aktion nach 2014-12-31) im Vergleich zur Filialeröffnung:")
daily = raw.groupby(["store_nbr", "date"]).sales.sum()
opening = daily[daily > 0].reset_index().groupby("store_nbr").date.min()
late = first_store[first_store > "2014-12-31"]
out(pd.DataFrame({"erste_Aktion": late, "Eröffnung": opening[late.index]}).to_string())

# %% [markdown]
# ## B. Filialen zeitweise geschlossen
# Tage mit Gesamtumsatz 0 **nach** der Eröffnung: Einzeltage oder längere Blöcke? Diese Nullen sind kein Nachfragesignal (Bericht 2.8).

# %%
out("\n=== B. Filialen zeitweise geschlossen (Bericht 2.8) ===")
out("Frage: Tage mit Gesamtumsatz 0 NACH der Eröffnung. Einzeltage oder längere Blöcke?")
t = pd.read_parquet(ROOT / "data/clean/train_clean.parquet")
c = (t[t.is_store_closed == 1].groupby(["store_nbr", "date"]).size().reset_index()[["store_nbr", "date"]]
     .sort_values(["store_nbr", "date"]))
out(f"Filial-Tage insgesamt: {len(c)}")
out(f"davon am 1. Januar: {(c.date.dt.strftime('%m-%d') == '01-01').sum()}")
out("\nFilial-Tage je Filiale (Top 8):")
out(c.store_nbr.value_counts().head(8).to_string())
c["block"] = (c.groupby("store_nbr").date.diff().dt.days != 1).cumsum()
blocks = c.groupby(["store_nbr", "block"]).date.agg(["min", "max", "count"]).sort_values("count", ascending=False)
out("\nLängste zusammenhängende Schließungen:")
out(blocks.head(8).to_string())
out(f"Blöcke mit mindestens 7 Tagen: {(blocks['count'] >= 7).sum()}   Einzeltage: {(blocks['count'] == 1).sum()}")

# %% [markdown]
# ## C. Feiertagstypen
# Welche Typen gibt es, und warum braucht die Tabelle eine Regel (verlegte Feiertage, mehrere Einträge je Tag)? (Bericht 2.1)

# %%
out("\n=== C. Feiertagstypen (Bericht 2.1) ===")
hol = pd.read_csv(ROOT / "data/raw/holidays_events.csv", parse_dates=["date"])
out(hol.groupby(["type", "locale"]).size().unstack(fill_value=0).to_string())
out("\nBeispiel: mehrere Einträge am selben Tag und Ort")
out(hol[hol.duplicated(["date", "locale_name"], keep=False)].sort_values("date").head(6).to_string())

(ROOT / "reports" / "explore_promo_closures_output.txt").write_text("\n".join(lines), encoding="utf-8")
