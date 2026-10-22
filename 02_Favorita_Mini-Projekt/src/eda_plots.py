"""Plots für die EDA. Ausführen: uv run python src/eda_plots.py"""
# %%
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
OUT = ROOT / "reports" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
train = pd.read_csv(ROOT / "data/raw/train.csv", parse_dates=["date"])

# %% [markdown]
# ## 1. Zielgröße: Gesamtabsatz pro Tag

# %%
tot = train.groupby("date").sales.sum()
fig, ax = plt.subplots(figsize=(11, 4))
tot.plot(ax=ax, lw=0.5, alpha=0.6, label="täglich")
tot.rolling(28, center=True).mean().plot(ax=ax, lw=1.8, label="28-Tage-Mittel")
ax.set(title="Gesamtabsatz aller Filialen und Familien pro Tag", xlabel="", ylabel="Absatz")
ax.legend(); fig.tight_layout(); fig.savefig(OUT / "01_gesamtabsatz.png", dpi=110); plt.close(fig)

# %% [markdown]
# ## 2. Saisonalität: Wochentag und Monat

# %%
d = tot["2014":].to_frame("sales")
fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
d.groupby(d.index.dayofweek).sales.mean().plot.bar(ax=axs[0], title="Ø Absatz je Wochentag (0=Mo)")
d.groupby(d.index.month).sales.mean().plot.bar(ax=axs[1], title="Ø Absatz je Monat")
fig.tight_layout(); fig.savefig(OUT / "02_saisonalitaet.png", dpi=110); plt.close(fig)

# %% [markdown]
# ## 3. Neue Filialen: Nullphase vor Eröffnung

# %%
daily = train.groupby(["store_nbr", "date"]).sales.sum().unstack(0)
fig, ax = plt.subplots(figsize=(11, 3.6))
for s in (20, 22, 52, 36):
    daily[s].rolling(7).mean().plot(ax=ax, label=f"Filiale {s}")
ax.set(title="Neue Filialen: Nullphase vor Eröffnung (7-Tage-Mittel)", xlabel="", ylabel="Absatz")
ax.legend(); fig.tight_layout(); fig.savefig(OUT / "03_neue_filialen.png", dpi=110); plt.close(fig)

# %% [markdown]
# ## 4. Produktfamilien: Anteile

# %%
fam = train.groupby("family").sales.sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 7))
fam.plot.barh(ax=ax, title="Gesamtabsatz je Produktfamilie"); fig.tight_layout()
fig.savefig(OUT / "04_familien.png", dpi=110); plt.close(fig)

# %% [markdown]
# ## Zusatz-Zahlen für den Bericht

# %%
print("1. Januar, Gesamtabsatz je Jahr:", tot[tot.index.strftime('%m-%d') == '01-01'].round(0).to_dict())
fam_start = train[train.sales > 0].groupby("family").date.min().sort_values().tail(5)
print("Familien mit spätem erstem Verkauf:\n", fam_start.dt.date.to_string())
zero_all = train.groupby(["family", "date"]).sales.sum()
print("Tage mit Absatz 0 über ALLE Filialen je Familie (Top 5):",
      (zero_all == 0).groupby("family").sum().sort_values(ascending=False).head(5).to_dict())
print("Anteil Absatz auf Top-3-Familien:", round(fam.tail(3).sum() / fam.sum(), 3), list(fam.tail(3).index))
