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

# %% [markdown]
# # Pinguine mit seaborn: Art vorhersagen
#
# Ablauf: Datensatz laden, bereinigen, Features wählen, trainieren, bewerten.

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# %% [markdown]
# ## Welche Datensätze gibt es?
#
# seaborn bringt Beispieldatensätze mit. Die Funktion liefert alle Namen, die
# `sns.load_dataset(name)` kennt. Sie fragt dafür das seaborn-data-Repository
# auf GitHub ab, deshalb braucht sie eine Internetverbindung.

# %%
def verfuegbare_datensaetze():
    """Gibt die Namen aller seaborn-Beispieldatensätze als Liste zurück."""
    return print(sns.get_dataset_names())


print(verfuegbare_datensaetze())

# %%
dow = sns.load_dataset("dowjones")
print(dow.head(10))


# %%
test = sns.load_dataset("healthexp")
print(test.head(5))

# %% [markdown]
# ## Datensatz laden

# %%
df = sns.load_dataset("penguins")

# erste Zeilen ansehen
# print(df.head(10))

# print(df.info())

# %% [markdown]
# ## Daten bereinigen und Features wählen

# %%
# mögliche Eingaben für Vorhersage
features = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]

# alle Zeilen mit nan raus
df_clean = df.dropna()

# Zielspalte alleine, Rest alleine
X = df_clean.drop("species", axis=1)
y = df_clean["species"]

# Alle features verwenden
# Kategorische Variablen umwandeln
X = pd.get_dummies(X, drop_first=True)

# Featurepaar auswählen

# features = ["body_mass_g", "bill_depth_mm"]
features = ["flipper_length_mm", "bill_length_mm"]

X = df_clean[features]
y = df_clean["species"]

# %% [markdown]
# ## Training- und Testdatensatz

# %%
from sklearn.model_selection import train_test_split

# notwendig für nearest neighbors
# X = X.dropna()
# y = y[X.index]  # entsprechende Zeilen aus y raus

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# %% [markdown]
# ## Modell wählen und trainieren
#
# Hier: Random Forest (funktioniert gut ohne viel Tuning).

# %%
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(max_depth=None, n_estimators=100,
                               min_samples_split=2, random_state=42)
model.fit(X_train, y_train)

# import joblib

# joblib.dump(model, "pinguin_modell.joblib")

# %%
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# %% [markdown]
# ## Bewerten

# %%
from sklearn.metrics import classification_report, accuracy_score

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))

# %%
# # Neue Werte als 2D-Array (Shape: (1, 2))
# neue_werte = pd.DataFrame([[0.5, 1.2]], columns=model.feature_names_in_)

# # Vorhersage machen
# vorhersage = model.predict(neue_werte, )
# print("Vorhersage:", vorhersage[0])  # z. B. Klasse 0 oder 1
