"""Datenqualitäts-Checks für Favorita (Store Sales). Ausführen: uv run python src/eda_checks.py"""
# %%
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
RAW = ROOT / "data" / "raw"
pd.set_option("display.width", 160)


def h(title):
    print(f"\n{'=' * 8} {title} {'=' * 8}")


train = pd.read_csv(RAW / "train.csv", parse_dates=["date"])
test = pd.read_csv(RAW / "test.csv", parse_dates=["date"])
stores = pd.read_csv(RAW / "stores.csv")
oil = pd.read_csv(RAW / "oil.csv", parse_dates=["date"])
hol = pd.read_csv(RAW / "holidays_events.csv", parse_dates=["date"])
trx = pd.read_csv(RAW / "transactions.csv", parse_dates=["date"])

# %% [markdown]
# ## 1. Überblick

# %%
h("1. Überblick")
for name, df in [("train", train), ("test", test), ("stores", stores), ("oil", oil), ("holidays", hol), ("transactions", trx)]:
    print(f"{name:13s} {df.shape[0]:>9,} Zeilen  {df.shape[1]} Spalten")
print("train Zeitraum:", train.date.min().date(), "→", train.date.max().date())
print("test  Zeitraum:", test.date.min().date(), "→", test.date.max().date())
print("Filialen:", train.store_nbr.nunique(), " Produktfamilien:", train.family.nunique())

# %% [markdown]
# ## 2. Fehlende Werte je Tabelle

# %%
h("2. Fehlende Werte je Tabelle")
for name, df in [("train", train), ("stores", stores), ("oil", oil), ("holidays", hol), ("transactions", trx)]:
    # TODO: add a oneliner what the .isna() fct is 
    na = df.isna().sum()
    print(name, "→", dict(na[na > 0]) or "keine")

# %% [markdown]
# ## 3. Duplikate

# %%
h("3. Duplikate")
print("train: komplett identische Zeilen:", train.drop(columns="id").duplicated().sum())
print("train: doppelte Schlüssel (date, store, family):", train.duplicated(["date", "store_nbr", "family"]).sum())
print("transactions: doppelte (date, store):", trx.duplicated(["date", "store_nbr"]).sum())
print("oil: doppelte Daten:", oil.date.duplicated().sum())
print("holidays: doppelte (date, locale_name):", hol.duplicated(["date", "locale_name"]).sum(),
      "| mehrere Einträge am selben Tag:", hol.date.duplicated().sum())

# %% [markdown]
# ## 4. Lückenlose Zeitachse?

# %%
h("4. Lückenlose Zeitachse?")
full = pd.date_range(train.date.min(), train.date.max())
missing = full.difference(train.date.unique())
print("fehlende Kalendertage im train:", list(missing.strftime("%Y-%m-%d")))
per_day = train.groupby("date").size()
print("Zeilen pro Tag (erwartet 54*33=1782):", per_day.value_counts().to_dict())
print("oil: Kalendertage ohne Eintrag:", len(full.difference(oil.date)), "| Einträge mit NaN:", oil.dcoilwtico.isna().sum())

# %% [markdown]
# ## 5. Wertebereiche in sales / onpromotion

# %%
h("5. Wertebereiche in sales / onpromotion")
print(train[["sales", "onpromotion"]].describe().round(2).to_string())
print("negative sales:", (train.sales < 0).sum())
print("Anteil sales == 0:", round((train.sales == 0).mean(), 3))
print("Nicht ganzzahlige sales (Gewicht/kg-Artikel):", (train.sales % 1 != 0).sum())

# %% [markdown]
# ## 6. Filialen: Start der Verkäufe (Null-Phasen am Anfang)

# %%
h("6. Filialen: Start der Verkäufe (Null-Phasen am Anfang)")
daily = train.groupby(["store_nbr", "date"]).sales.sum().reset_index()
first_sale = daily[daily.sales > 0].groupby("store_nbr").date.min()
late = first_sale[first_sale > train.date.min() + pd.Timedelta(days=30)]
print(f"{len(late)} von 54 Filialen starten erst nach Tag 30 (neu eröffnet):")
print(late.dt.date.to_string())
zero_days = daily[daily.sales == 0].groupby("store_nbr").size()
print("Tage mit Gesamtumsatz 0 je Filiale (Top 8):", zero_days.sort_values(ascending=False).head(8).to_dict())

# %% [markdown]
# ## 7. Produktfamilien: Null-Reihen

# %%
h("7. Produktfamilien: Null-Reihen")
fam = train.groupby("family").sales.agg(total="sum", zero_share=lambda s: (s == 0).mean()).round(3)
print(fam.sort_values("zero_share", ascending=False).head(8).to_string())

# %% [markdown]
# ## 8. Promotion: wann ist onpromotion > 0?

# %%
h("8. Promotion: wann ist onpromotion > 0?")
promo_first = train[train.onpromotion > 0].date.min()
print("erster Tag mit onpromotion > 0:", promo_first.date())
print("Anteil Zeilen mit Promo vor/nach diesem Datum:",
      round((train[train.date >= promo_first].onpromotion > 0).mean(), 3))
print("Promo je Jahr (Anteil Zeilen > 0):")
print(train.assign(y=train.date.dt.year).groupby("y").onpromotion.apply(lambda s: round((s > 0).mean(), 3)).to_string())

# %% [markdown]
# ## 9. Feiertage

# %%
h("9. Feiertage")
print(hol.groupby(["type", "transferred"]).size().to_string())
print("Locale:", hol.locale.value_counts().to_dict())

# %% [markdown]
# ## 10. Transactions vs. train

# %%
h("10. Transactions vs. train")
tr_pairs = set(zip(trx.date, trx.store_nbr))
tn_pairs = set(map(tuple, daily[daily.sales > 0][["date", "store_nbr"]].itertuples(index=False, name=None)))
print("Filial-Tage mit Umsatz, aber ohne Transaktionseintrag:", len(tn_pairs - tr_pairs))
print("Transaktionseinträge ohne Umsatz:", len(tr_pairs - tn_pairs))

# %% [markdown]
# ## 11. Ausreißer: größte Tageswerte je (Filiale, Familie) vs. Median

# %%
h("11. Ausreißer: größte Tageswerte je (Filiale, Familie) vs. Median")
s = train[train.sales > 0].groupby(["store_nbr", "family"]).sales
ratio = (s.max() / s.median()).sort_values(ascending=False)
print(ratio.head(6).round(1).to_string())
top = train.nlargest(5, "sales")[["date", "store_nbr", "family", "sales"]]
print(top.to_string(index=False))

# %% [markdown]
# ## 12. Erdbeben 16.04.2016 & Jahresende

# %%
h("12. Erdbeben 16.04.2016 & Jahresende")
tot = train.groupby("date").sales.sum()
print(tot["2016-04-10":"2016-04-24"].round(0).to_string())
