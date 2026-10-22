# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# for using the code in a shell without jupyter
# python3 -m venv .venv
# source .venv/bin/activate
# once: pip install pandas seaborn matplotlib scikit-learn
# jupyter lab

# %%
import pandas as pd
import seaborn as sns

# %%
# Datensatz laden
df = sns.load_dataset("penguins")


# %%
# Datensatz kennenlernen

# erste Zeilen ansehen
print(df.head(10))

# %%
# allgemeine Informationen 
print(df.info())

# %%
# graphische EDA

import matplotlib.pyplot as plt

# %%
# mögliche Eingaben für Vorhersage
features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

plt.figure(figsize=(12, 8))

for i, feat in enumerate(features, 1):
    plt.subplot(2, 2, i)
    sns.violinplot(data=df, x="species", y=feat, 
                   color="orange", inner="quartile")
    plt.title(feat)

plt.tight_layout()
plt.show()

# %%
sns.pairplot(df.dropna(), hue="species")
plt.show()

# %%
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
plt.show()

# %%
# Suche nach Ausreißern

num_cols = df.select_dtypes(include="number").columns

df[num_cols].plot(
    kind="box",
    subplots=True,
    layout=(2, 2),
    figsize=(10, 7)
)
plt.tight_layout()
plt.show()

# %%
sns.scatterplot(
    data=df,
    x="bill_length_mm",
    y="bill_depth_mm",
    hue="species"
)
plt.show()


# %%
# Datenbereinigung
# Einziges erkanntes Problem: leere Zellen, "NaN"

# alle Zeilen mit nan raus
df_clean = df.dropna()

# %%

# # Künstliche Ausreißer
df_outliers = df.copy()

# # drei Zeilen
rows = df_outliers.dropna(
    subset=["bill_length_mm", "body_mass_g"]
).index[:3]

# # Werte ändern
df_outliers.loc[rows[0], "bill_length_mm"] = 100
df_outliers.loc[rows[1], "body_mass_g"] = 10000
df_outliers.loc[rows[2], "bill_length_mm"] = 110


# %%
# selbe Graphiken wie oben

num_cols = df_outliers.select_dtypes(include="number").columns

df_outliers[num_cols].plot(
    kind="box",
    subplots=True,
    layout=(2, 2),
    figsize=(10, 7)
)
plt.tight_layout()
plt.show()

# %%
sns.scatterplot(
    data=df_outliers,
    x="bill_length_mm",
    y="bill_depth_mm",
    hue="species"
)
plt.show()

