"""Bereinigung Favorita nach reports/01_EDA_und_Zielgroesse.md, Abschnitt 2.
Ausführen: uv run python src/clean.py   (Ausgabe: data/clean/*.parquet, reports/clean_log.txt)
"""
from pathlib import Path

import numpy as np
import pandas as pd

from masking import spike_flags

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "clean"
OUT.mkdir(parents=True, exist_ok=True)

SPIKE_FACTOR = 10  # Tageswert > 10 × Median der 4 Tage davor UND danach (Isolationsregel, siehe src/outliers.py)
SPIKE_MIN = 500    # und mindestens so viele Einheiten
log_lines = []


def log(msg=""):
    print(msg)
    log_lines.append(msg)


train = pd.read_csv(RAW / "train.csv", parse_dates=["date"]).drop(columns="id")
test = pd.read_csv(RAW / "test.csv", parse_dates=["date"]).drop(columns="id")
stores = pd.read_csv(RAW / "stores.csv")
oil = pd.read_csv(RAW / "oil.csv", parse_dates=["date"])
hol = pd.read_csv(RAW / "holidays_events.csv", parse_dates=["date"])

log(f"Rohdaten: train {len(train):,} Zeilen, test {len(test):,} Zeilen")

# --- 1. Duplikate ------------------------------------------------------------
key = ["date", "store_nbr", "family"]
n_dup = train.duplicated(key).sum()
train = train.drop_duplicates(key)
log(f"[Duplikate] doppelte Schlüssel in train entfernt: {n_dup}")

# --- 2. 25. Dezember: Tag fehlt, Filialen geschlossen -> Zeilen mit sales = NaN ergänzen ----
all_days = pd.date_range(train.date.min(), train.date.max())
missing_days = all_days.difference(train.date.unique())
combos = train[["store_nbr", "family"]].drop_duplicates()
fill = pd.DataFrame(
    [(d, s, f) for d in missing_days for s, f in combos.itertuples(index=False)],
    columns=key,
)
fill["sales"], fill["onpromotion"] = np.nan, 0
train = pd.concat([train, fill], ignore_index=True)
train["is_closed_day"] = train.date.isin(missing_days).astype("int8")
log(f"[Lücken] fehlende Kalendertage ergänzt (sales = NaN, is_closed_day = 1): "
    f"{[d.strftime('%Y-%m-%d') for d in missing_days]} -> {len(fill):,} Zeilen")

# --- 3. Strukturelle Nullen entfernen ------------------------------------------
daily_store = train.groupby(["store_nbr", "date"]).sales.sum()
store_open = daily_store[daily_store > 0].reset_index().groupby("store_nbr").date.min()
fam_start = train[train.sales > 0].groupby("family").date.min()
train = train.merge(store_open.rename("store_open"), on="store_nbr").merge(fam_start.rename("fam_start"), on="family")
before_open = train.date < train.store_open
before_fam = train.date < train.fam_start
log(f"[Strukturelle Nullen] Zeilen vor Filialeröffnung: {before_open.sum():,}; "
    f"vor Einführung der Familie: {before_fam.sum():,}; zusammen entfernt: {(before_open | before_fam).sum():,}")
train = train[~(before_open | before_fam)].drop(columns=["store_open", "fam_start"])

# Filiale zeitweise zu (Gesamtumsatz 0 nach Eröffnung): markieren, nicht löschen
tot = train.groupby(["store_nbr", "date"]).sales.transform("sum")
train["is_store_closed"] = ((tot == 0) & (train.is_closed_day == 0)).astype("int8")
log(f"[Filiale zu] Zeilen an Tagen mit Filial-Gesamtumsatz 0 nach Eröffnung (markiert): {train.is_store_closed.sum():,} "
    f"({train[train.is_store_closed == 1].groupby(['store_nbr', 'date']).ngroups} Filial-Tage)")

# --- 4. Promotion: promo_known je Filiale ------------------------------------------
first_promo = train[train.onpromotion > 0].groupby("store_nbr").date.min().rename("first_promo")
for df in (train, test):
    df["first_promo"] = df.store_nbr.map(first_promo)
    df["promo_known"] = (df.date >= df.first_promo).astype("int8")
    df.drop(columns="first_promo", inplace=True)
log(f"[Promotion] Zeilen mit promo_known = 0 in train: {(train.promo_known == 0).sum():,} "
    f"({(train.promo_known == 0).mean():.1%}); in test: {(test.promo_known == 0).sum()}")

# --- 5. Ölpreis auf Kalender, auffüllen -------------------------------------------
cal = pd.DataFrame({"date": pd.date_range(train.date.min(), test.date.max())})
oil = cal.merge(oil, on="date", how="left")
oil["oil_filled"] = oil.dcoilwtico.isna().astype("int8")
oil["dcoilwtico"] = oil.dcoilwtico.ffill().bfill()
log(f"[Ölpreis] Kalendertage aufgefüllt (ffill/bfill): {oil.oil_filled.sum()} von {len(oil)}")

# --- 6. Feiertage je Filiale ---------------------------------------------------------
n_transferred = ((hol.type == "Holiday") & hol.transferred).sum()
hol = hol[~((hol.type == "Holiday") & hol.transferred)]  # an diesem Tag war KEIN Feiertag
hol = hol.assign(
    is_holiday=hol.type.isin(["Holiday", "Transfer", "Additional", "Bridge"]),
    is_workday=hol.type.eq("Work Day"),
    is_event=hol.type.eq("Event"),
)
parts = []
for loc, col in [("National", None), ("Regional", "state"), ("Local", "city")]:
    h = hol[hol.locale == loc]
    if col is None:
        m = h.merge(stores[["store_nbr"]], how="cross")
    else:
        m = h.merge(stores[["store_nbr", col]], left_on="locale_name", right_on=col)
    parts.append(m[["date", "store_nbr", "is_holiday", "is_workday", "is_event"]])
hol_store = pd.concat(parts).groupby(["date", "store_nbr"], as_index=False).max()
log(f"[Feiertage] verlegte Feiertage ohne Wirkung am Tag entfernt: {n_transferred}; "
    f"Filial-Tage mit Eintrag nach Verdichtung: {len(hol_store):,}")


def enrich(df):
    df = df.merge(stores, on="store_nbr", how="left").merge(oil, on="date", how="left")
    df = df.merge(hol_store, on=["date", "store_nbr"], how="left")
    for c in ["is_holiday", "is_workday", "is_event"]:
        df[c] = df[c].fillna(False).astype("int8")
    df["dayofweek"] = df.date.dt.dayofweek.astype("int8")
    df["is_new_year"] = ((df.date.dt.month == 1) & (df.date.dt.day == 1)).astype("int8")
    df["family"] = df.family.astype("category")
    return df


train, test = enrich(train), enrich(test)
test["is_closed_day"] = 0
test["is_store_closed"] = 0

# --- 7. Isolierte Spitzen markieren und maskieren (nicht löschen) ------------------------------
# Eine Spitze ist verdächtig, wenn der Tag vorher UND nachher normal umgeben ist. Saison und
# Niveausprünge (mehrere Tage) fallen so nicht auf. Auf Zeilen ohne geschlossene Tage gerechnet.
train = train.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)
train["is_outlier"] = spike_flags(train, SPIKE_FACTOR, SPIKE_MIN).astype("int8")
log(f"[Ausreißer] isolierte Spitzen markiert (> {SPIKE_FACTOR} × Nachbar-Median, > {SPIKE_MIN}): {train.is_outlier.sum()} Zeilen")
log(train[train.is_outlier == 1].nlargest(8, "sales")[["date", "store_nbr", "family", "sales"]].to_string(index=False))

# sales      = unverändert (Rohwert, für Bewertung mit und ohne Ausreißer)
# sales_train = sales mit NaN an allen unzuverlässigen Beobachtungen: Spitzen, 25. Dezember, Filiale zu
unreliable = (train.is_outlier == 1) | (train.is_closed_day == 1) | (train.is_store_closed == 1)
train["sales_train"] = train.sales.where(~unreliable)
log(f"[Maskierung] sales_train = NaN an {int(unreliable.sum()):,} Zeilen "
    f"(Spitzen {int((train.is_outlier == 1).sum())}, geschlossene Tage {int(train.is_closed_day.sum()):,}, "
    f"Filiale zu {int(train.is_store_closed.sum()):,}; Überschneidung: {int(train.is_outlier.add(train.is_closed_day).add(train.is_store_closed).gt(1).sum())})")

# --- 8. Speichern und Kontrolle -------------------------------------------------------------
train = train.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)
test = test.sort_values(["store_nbr", "family", "date"]).reset_index(drop=True)
train.to_parquet(OUT / "train_clean.parquet", index=False)
test.to_parquet(OUT / "test_clean.parquet", index=False)

log("\n[Ergebnis]")
log(f"train_clean: {len(train):,} Zeilen (von 3.000.888 + {len(fill):,} ergänzt), {train.date.min().date()} bis {train.date.max().date()}")
log(f"test_clean:  {len(test):,} Zeilen")
log(f"Reihen (Filiale × Familie): {train.groupby(['store_nbr', 'family'], observed=True).ngroups}")
log(f"Anteil sales == 0 jetzt: {(train.sales == 0).mean():.1%} (vorher 31,3 %)")
log("Fehlende Werte train (sales: nur 25. Dezember; sales_train: zusätzlich maskierte Zeilen):")
na = train.isna().sum()
log(str(dict(na[na > 0])))
(ROOT / "reports" / "clean_log.txt").write_text("\n".join(log_lines), encoding="utf-8")
