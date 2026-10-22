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
# # 05 · Notebook-Preisempfehlung
# Regression auf `05_Notebookpreise_Arbeitsauftrag.csv`
#
# ## So startest du das Ganze (im Terminal)
# ```bash
# cd "<Pfad zu deinem Kursordner>/05_Modellauswahl"
# source .venv/bin/activate          # Prompt zeigt danach (.venv)
#
# jupyter lab                        # Browser öffnet sich, dort 05_Notebookpreise_Modell.ipynb öffnen
# # oder ohne Browser, nur Konsole (Plots öffnen sich als Fenster):
# python 05_Notebookpreise_Modell.py
#
# deactivate                         # venv wieder verlassen
# ```
# Ohne Aktivieren geht auch: `.venv/bin/jupyter lab` bzw. `.venv/bin/python 05_Notebookpreise_Modell.py`.
#
# **Falls `.venv` fehlt oder Pakete fehlen (einmalig):**
# ```bash
# python3 -m venv .venv && source .venv/bin/activate
# pip install pandas scikit-learn matplotlib seaborn jupyterlab jupytext
# ```
#
# **Kernel in Jupyter:** `Python 3 (ipykernel)` wählen. Läuft `jupyter lab` aus der aktivierten venv, ist das automatisch die richtige.
#
# **Py und Notebook gleichzeitig:** `.py` (Vim) und `.ipynb` sind über jupytext gekoppelt. Nach dem Speichern in Vim im Terminal
# `jupytext --sync 05_Notebookpreise_Modell.py` ausführen, dann zieht das Notebook nach. Umgekehrt synchronisiert Jupyter Lab beim Speichern die `.py` automatisch.

# %%
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

sns.set_theme(style="whitegrid")

# __file__ gibt es im Notebook nicht: dort liegt die CSV im aktuellen Ordner
DATEI = (Path(__file__).parent if "__file__" in globals() else Path.cwd()) / "05_Notebookpreise_Arbeitsauftrag.csv"
MERKMALE = ["Display_Zoll", "Akku_Wh", "RAM_GB", "SSD_GB", "Gewicht_g"]
ZIEL = "Preis_EUR"

# %% [markdown]
# ## 1 · Laden und prüfen
# Auffälligkeiten der Datei: `Display_Zoll` mit führenden Nullen (`00000000014`),
# Preis mit Dezimalkomma in Anführungszeichen, am Ende eine leere Zeile `,,,,,,`.

# %%
roh = pd.read_csv(DATEI, dtype=str)
print("Zeilen roh:", len(roh))
df = roh.dropna(how="all").copy()
print("Zeilen nach Entfernen leerer Zeilen:", len(df))

for spalte in MERKMALE:
    df[spalte] = pd.to_numeric(df[spalte])          # "00000000014" -> 14
df[ZIEL] = pd.to_numeric(df[ZIEL].str.replace(",", ".", regex=False))

print("fehlende Werte:", int(df[MERKMALE + [ZIEL]].isna().sum().sum()))
print("doppelte Modelle:", int(df["Modell"].duplicated().sum()))
print("doppelte Zeilen (ohne Name):", int(df[MERKMALE + [ZIEL]].duplicated().sum()))
df[MERKMALE + [ZIEL]].describe().round(1).T

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Aus 501 Zeilen werden 500 (eine leere Excel-Zeile am Ende). Führende Nullen und das Dezimalkomma mussten repariert werden, sonst wären Zoll und Preis Text geblieben. Es fehlen keine Werte, es gibt keine Duplikate: Die Daten sind sauber genug zum Modellieren.</div>

# %% [markdown]
# ## 2 · Zusammenhänge erkunden

# %%
print("Korrelation mit dem Preis:")
print(df[MERKMALE + [ZIEL]].corr()[ZIEL].drop(ZIEL).round(2).sort_values(ascending=False).to_string())
print("\nKorrelation der Merkmale untereinander (Multikollinearität):")
print(df[MERKMALE].corr().round(2).to_string())
print("\nMittlerer Preis nach RAM:")
print(df.groupby("RAM_GB")[ZIEL].agg(["count", "mean"]).round(0).to_string())
print("\nMittlerer Preis nach SSD:")
print(df.groupby("SSD_GB")[ZIEL].agg(["count", "mean"]).round(0).to_string())

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> <b>RAM (0,77) und SSD (0,62)</b> hängen am stärksten am Preis, Gewicht, Display und Akku nur schwach (0,17 bis 0,27). Der Ø-Preis steigt von 988 € (8 GB RAM) auf 1.630 € (64 GB).</div>

# %% [markdown]
# ### Plot 1 · Verteilung des Preises

# %%
fig, ax = plt.subplots(figsize=(7, 4))
sns.histplot(df[ZIEL], bins=30, kde=True, ax=ax)
ax.set(title="Verteilung der Notebook-Preise", xlabel="Preis in EUR", ylabel="Anzahl")
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Die Preise reichen von 699 bis 2.048 €, Mittelwert 1.250 €. Zwei Gipfel (um 1.000 und um 1.450 €) deuten auf Preisklassen hin, die vermutlich von der Ausstattung kommen. Diese Spanne muss das Modell treffen.</div>

# %% [markdown]
# ### Plot 2 · Preis nach RAM und SSD
# RAM und SSD sind die beiden Hebel: Der Preis steigt mit jeder Stufe deutlich.

# %%
fig, achsen = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
sns.boxplot(data=df, x="RAM_GB", y=ZIEL, ax=achsen[0])
achsen[0].set(title="Preis nach RAM", xlabel="RAM in GB", ylabel="Preis in EUR")
sns.boxplot(data=df, x="SSD_GB", y=ZIEL, ax=achsen[1])
achsen[1].set(title="Preis nach SSD", xlabel="SSD in GB", ylabel="")
plt.tight_layout()
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Der Preis steigt mit <b>jeder</b> RAM- und SSD-Stufe deutlich. Zwei Hebel erklären den größten Teil des Preises.</div>

# %% [markdown]
# ### Plot 3 · Preis gegen RAM, eingefärbt nach SSD
# Bei gleichem RAM zeigen die Farbschichten den SSD-Aufschlag: nahezu parallele Stufen sprechen für einen linearen Zusammenhang.

# %%
fig, ax = plt.subplots(figsize=(7, 5))
sns.stripplot(data=df, x="RAM_GB", y=ZIEL, hue="SSD_GB", palette="viridis", dodge=True, alpha=0.7, ax=ax)
ax.set(title="Preis nach RAM und SSD", xlabel="RAM in GB", ylabel="Preis in EUR")
ax.legend(title="SSD in GB", fontsize=8)
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Bei jedem RAM-Wert liegen die SSD-Größen als saubere Schichten übereinander, und die Schichten wiederholen sich bei jeder RAM-Stufe in ähnlichem Abstand. RAM und SSD <b>addieren</b> sich also zum Preis, das passt zu einem <b>linearen</b> Modell.</div>

# %% [markdown]
# ### Plot 4 · Korrelations-Heatmap
# Display, Gewicht und Akku hängen zusammen (Multikollinearität), RAM und SSD sind unabhängig.

# %%
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(df[MERKMALE + [ZIEL]].corr(), annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
ax.set_title("Korrelationen")
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Display, Gewicht und Akku hängen zusammen (0,5 bis 0,7, Multikollinearität). RAM und SSD sind voneinander unabhängig. Darum sind ihre Koeffizienten stabil, die von Gewicht und Akku nur vorsichtig zu deuten.</div>

# %% [markdown]
# ## 3 · Modelle vergleichen
# **Frage:** Welches Modell sagt Preise am besten voraus? Wir probieren **fünf Modelle** aus, alle mit denselben Daten
# und derselben Prüfmethode, damit der Vergleich fair ist:
#
# | # | Modell | Idee in einem Satz | Rolle |
# | --- | --- | --- | --- |
# | 1 | **Baseline** (`DummyRegressor`) | sagt immer den Durchschnittspreis voraus | Messlatte: wer das nicht schlägt, ist nutzlos |
# | 2 | **Lineare Regression** | legt eine gewichtete Summe durch die Daten (Preis = Grundpreis + x € je GB RAM + ...) | einfach und erklärbar |
# | 3 | **Entscheidungsbaum** (Tiefe 4) | stellt Ja/Nein-Fragen („RAM ≥ 32?") und landet in einer Preisgruppe | einfach, erklärbar |
# | 4 | **Random Forest** | 200 Bäume stimmen ab, jeder sieht andere Daten | komplexer, Black Box |
# | 5 | **Gradient Boosting** | Bäume lernen nacheinander, jeder korrigiert die Fehler des vorigen | komplexer, Black Box |
#
# ### Was heißt „5-fache Kreuzvalidierung"?
# **Problem:** Ein Modell darf nicht mit denselben Daten geprüft werden, mit denen es gelernt hat. Das wäre wie eine Klausur
# mit den Übungsaufgaben: Auswendiglernen (Overfitting) würde belohnt. Also hält man Daten zum **Testen** zurück.
# Mit nur **einer** Aufteilung hängt das Ergebnis aber vom Zufall ab: Vielleicht waren die Testzeilen zufällig leicht oder schwer.
#
# **Lösung:** Man teilt die 500 Zeilen zufällig in **5 gleich große Teile** („Folds") zu je 100 Zeilen und prüft **fünfmal**.
# Jedes Mal ist ein anderer Teil der Test-Teil, die anderen vier (400 Zeilen) sind der Lern-Teil:
#
# ```text
# Durchlauf 1:  [ TEST ][ lernen ][ lernen ][ lernen ][ lernen ]   -> Fehler 1
# Durchlauf 2:  [ lernen ][ TEST ][ lernen ][ lernen ][ lernen ]   -> Fehler 2
# Durchlauf 3:  [ lernen ][ lernen ][ TEST ][ lernen ][ lernen ]   -> Fehler 3
# Durchlauf 4:  [ lernen ][ lernen ][ lernen ][ TEST ][ lernen ]   -> Fehler 4
# Durchlauf 5:  [ lernen ][ lernen ][ lernen ][ lernen ][ TEST ]   -> Fehler 5
# ```
#
# Das Modell wird in jedem Durchlauf **neu und von null** trainiert und nur auf den 100 **ungesehenen** Zeilen geprüft.
# Am Ende gibt es fünf Fehlerwerte. Daraus werden zwei Zahlen:
# - **Mittelwert** der fünf Fehler → wie gut ist das Modell typischerweise? (Spalte `MAE (EUR)`, `R2`)
# - **Streuung** der fünf Fehler → wie stabil ist es? Eine kleine Streuung heißt: egal welche Daten, ähnlich gutes Ergebnis. (Spalte `Streuung MAE`)
#
# **Ja, jedes der fünf Modelle wird so getestet**, jeweils mit den **gleichen fünf Aufteilungen** (`random_state=42` legt den Zufall fest).
# Insgesamt entstehen 5 Modelle × 5 Durchläufe = **25 Trainings**. Das Modell, das wir später für die Preisempfehlung nutzen, ist ein
# **eigenes, danach trainiertes** (siehe Abschnitt 4), die Kreuzvalidierung dient nur dem **Vergleich**.
#
# ### Die Kennzahlen
# - **MAE** (mittlerer absoluter Fehler): Im Schnitt liegt die Prognose um so viele **Euro** daneben. Kleiner ist besser.
# - **R²**: Anteil der Preisschwankung, den das Modell erklärt. 1,0 = perfekt, 0 = nicht besser als der Durchschnitt, negativ = schlechter.

# %%
X, y = df[MERKMALE], df[ZIEL]

# Alle Kandidaten in einem Dictionary: Name -> Modellobjekt. Weitere Modelle ergänzt man einfach als neue Zeile.
modelle = {
    # Modell 1 · Baseline: sagt immer den Durchschnittspreis voraus. Ohne Lernen, nur die Messlatte.
    # Varianten zum Ausprobieren: strategy="median" (Mittelwert -> Median)
    "Baseline: Mittelwert": DummyRegressor(strategy="mean"),

    # Modell 2 · Lineare Regression: Preis = Grundpreis + x * Display + y * RAM + ...
    # StandardScaler bringt alle Merkmale auf gleiche Skala (Gramm vs. GB). Für die Genauigkeit egal, hilft bei der Deutung.
    # make_pipeline hängt beide Schritte zusammen: erst skalieren, dann rechnen. In der Kreuzvalidierung geschieht das je Durchlauf
    # nur mit den Lern-Daten, so schleicht sich nichts aus den Test-Daten ein (Data Leakage).
    # Varianten: Ridge() oder Lasso() (aus sklearn.linear_model), bestrafen sehr große Koeffizienten
    "Lineare Regression": make_pipeline(StandardScaler(), LinearRegression()),

    # Modell 3 · Entscheidungsbaum: Ja/Nein-Fragen wie "RAM >= 32 GB?". max_depth=4 heißt höchstens 4 Fragen hintereinander.
    # Zu tief = lernt Zufälle auswendig (Overfitting), zu flach = zu grob (Underfitting).
    # Varianten: max_depth=2 (sehr einfach), max_depth=10 (sehr detailliert)
    "Entscheidungsbaum (Tiefe 4)": DecisionTreeRegressor(max_depth=4, random_state=42),

    # Modell 4 · Random Forest: 200 Bäume, jeder sieht eine zufällige Stichprobe, das Ergebnis ist der Durchschnitt.
    # Viele schwache Meinungen mitteln sich zu einer stabilen. Standardeinstellungen, nicht abgestimmt.
    # Varianten: n_estimators=500 (mehr Bäume), max_depth=6 (flachere Bäume)
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),

    # Modell 5 · Gradient Boosting: Bäume lernen nacheinander, jeder korrigiert die Restfehler der vorigen.
    # Oft sehr genau, aber empfindlicher bei den Einstellungen. Hier Standardwerte, nicht abgestimmt.
    # Varianten: learning_rate=0.05, n_estimators=500 (langsamer lernen, mehr Runden)
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
}

# Die 5-fache Kreuzvalidierung: 5 Teile, vorher zufällig gemischt (shuffle), fester Zufall (random_state) für Wiederholbarkeit.
cv = KFold(n_splits=5, shuffle=True, random_state=42)

zeilen = []
for name, modell in modelle.items():
    # cross_validate trainiert das Modell 5x neu (je 400 Zeilen) und prüft 5x auf den restlichen 100 Zeilen.
    # Ergebnis: je Kennzahl eine Liste mit 5 Werten, einer pro Durchlauf.
    s = cross_validate(modell, X, y, cv=cv, scoring=("neg_mean_absolute_error", "r2"))
    zeilen.append({
        "Modell": name,
        # sklearn liefert den Fehler negativ (größer = besser), daher das Minus davor
        "MAE (EUR)": -s["test_neg_mean_absolute_error"].mean(),     # Mittelwert der 5 Fehler
        "Streuung MAE": s["test_neg_mean_absolute_error"].std(),    # Streuung der 5 Fehler = Stabilität
        "R2": s["test_r2"].mean(),
    })
vergleich = pd.DataFrame(zeilen)
print(vergleich.round(2).to_string(index=False))

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> <b>Die einfache lineare Regression gewinnt:</b> Fehler 33 € gegen 37 € (Boosting), 40 € (Random Forest), 58 € (Baum) und 267 € (Baseline). Komplexer heißt hier nicht besser.</div>

# %% [markdown]
# ### Plot 5 · Fehler der Modelle im Vergleich

# %%
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=vergleich, y="Modell", x="MAE (EUR)", color="steelblue", ax=ax)
ax.errorbar(vergleich["MAE (EUR)"], range(len(vergleich)), xerr=vergleich["Streuung MAE"],
            fmt="none", ecolor="black", capsize=3)
for i, wert in enumerate(vergleich["MAE (EUR)"]):
    ax.text(wert + 4, i, f"{wert:.0f} €", va="center")
ax.set(title="Mittlerer Fehler (MAE), kleiner ist besser", xlabel="MAE in EUR", ylabel="")
plt.tight_layout()
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Die lineare Regression hat den kleinsten Balken und mit 1 € auch die kleinste Streuung zwischen den fünf Durchläufen. Sie ist das genaueste <b>und</b> das stabilste Modell.</div>

# %% [markdown]
# ## 4 · Lineare Regression deuten (Hold-out 80/20)

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
linear = LinearRegression().fit(X_train, y_train)
vorhersage = linear.predict(X_test)
print(f"Achsenabschnitt: {linear.intercept_:,.1f} EUR")
for name, koef in zip(MERKMALE, linear.coef_):
    print(f"  {name:13s} {koef:+9.3f} EUR je Einheit")
print(f"Test: MAE {mean_absolute_error(y_test, vorhersage):.1f} EUR · "
      f"RMSE {root_mean_squared_error(y_test, vorhersage):.1f} EUR · "
      f"R2 {r2_score(y_test, vorhersage):.3f}")

skaliert = make_pipeline(StandardScaler(), LinearRegression()).fit(X_train, y_train)
wichtig = permutation_importance(skaliert, X_test, y_test, n_repeats=30, random_state=42,
                                 scoring="neg_mean_absolute_error")
rang = pd.Series(wichtig.importances_mean, index=MERKMALE).sort_values(ascending=False)
print("\nPermutationswichtigkeit (Anstieg des MAE in EUR, wenn Merkmal durchmischt wird):")
print(rang.round(1).to_string())

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Pro GB RAM +10,9 € (16 GB ≈ +174 €), pro TB SSD ≈ +293 €. Display, Akku und Gewicht tragen kaum etwas bei. Test-Fehler im Schnitt <b>33,6 €</b>, R² 0,98: Das Modell ist gut <b>und</b> in Euro erklärbar.</div>

# %% [markdown]
# ### Plot 6 · Welche Merkmale zählen?

# %%
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(x=rang.values, y=rang.index, color="seagreen", ax=ax)
ax.set(title="Wichtigkeit der Merkmale (Permutation)", xlabel="Anstieg des MAE in EUR beim Durchmischen", ylabel="")
plt.tight_layout()
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> <b>RAM</b> (225) und <b>SSD</b> (167) tragen das Modell. Display (21), Akku (3) und Gewicht (0,6) kann man fast weglassen. Ein einfacheres Modell wäre einen Test wert.</div>

# %% [markdown]
# ## 5 · Fehleranalyse am Test-Set

# %%
fehler = pd.DataFrame({"Ist": y_test, "Prognose": vorhersage.round(0)})
fehler["Abweichung"] = fehler["Prognose"] - fehler["Ist"]
print("mittlere Abweichung (Bias):", round(fehler["Abweichung"].mean(), 1), "EUR")
print("größte Unterschätzung:", round(fehler["Abweichung"].min(), 0), "EUR")
print("größte Überschätzung: ", round(fehler["Abweichung"].max(), 0), "EUR")
print("Anteil Prognosen innerhalb ±100 EUR:",
      f"{(fehler['Abweichung'].abs() <= 100).mean():.0%}")

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> <b>97 %</b> der Prognosen liegen innerhalb von ±100 €. Die mittlere Verzerrung ist mit −4 € klein, die größten Ausreißer liegen bei −129 € und +114 €. Eine Preisspanne von ±100 € ist als Orientierung brauchbar.</div>

# %% [markdown]
# ### Plot 7 · Prognose gegen Ist
# Punkte auf der Diagonalen sind perfekte Treffer. Das Band zeigt ±100 EUR.

# %%
fig, ax = plt.subplots(figsize=(6, 6))
grenze = [fehler["Ist"].min() - 50, fehler["Ist"].max() + 50]
ax.plot(grenze, grenze, color="black", lw=1)
ax.fill_between(grenze, [g - 100 for g in grenze], [g + 100 for g in grenze], color="grey", alpha=0.15, label="±100 EUR")
ax.scatter(fehler["Ist"], fehler["Prognose"], alpha=0.7)
ax.set(title="Prognose gegen Ist (Test-Set)", xlabel="Ist-Preis in EUR", ylabel="Prognose in EUR")
ax.legend()
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Die Punkte liegen eng an der Diagonalen, fast alle im ±100-€-Band: Das Modell trifft über die gesamte Preisspanne ähnlich gut, auch bei sehr günstigen und sehr teuren Geräten.</div>

# %% [markdown]
# ### Plot 8 · Residuen
# Prognose minus Ist. Ein Muster (Bogen, Trichter) würde zeigen, dass das lineare Modell etwas übersieht.

# %%
fig, achsen = plt.subplots(1, 2, figsize=(12, 4))
achsen[0].scatter(fehler["Prognose"], fehler["Abweichung"], alpha=0.7)
achsen[0].axhline(0, color="black", lw=1)
achsen[0].set(title="Residuen gegen Prognose", xlabel="Prognose in EUR", ylabel="Abweichung in EUR")
sns.histplot(fehler["Abweichung"], bins=20, kde=True, ax=achsen[1])
achsen[1].set(title="Verteilung der Abweichungen", xlabel="Abweichung in EUR", ylabel="Anzahl")
plt.tight_layout()
plt.show()

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Die Abweichungen streuen ohne erkennbares Muster um 0 und sind etwa glockenförmig. Das lineare Modell übersieht also <b>keine</b> systematische Struktur, mehr Komplexität bringt hier nichts.</div>

# %% [markdown]
# ## 6 · Beispiel: Preisempfehlung für ein neues Gerät

# %%
neu = pd.DataFrame([{"Display_Zoll": 15, "Akku_Wh": 65, "RAM_GB": 512, "SSD_GB": 512, "Gewicht_g": 1400}])
print(neu.to_string(index=False))
print(f"empfohlener Preis: {linear.predict(neu)[0]:,.0f} EUR")

# %% [markdown]
# <div style="background:#e0f2f1;border-left:6px solid #009688;color:#004d40;padding:10px 14px;border-radius:4px"><b>Takeaway:</b> Empfehlung <b>969 €</b> vom linearen Modell (trainiert auf 400 Zeilen). Das ist ein <b>Vorschlag</b>: Der Vertrieb entscheidet, und das Gerät muss im bekannten Wertebereich liegen (RAM 8 bis 64 GB, SSD 256 bis 2048 GB).</div>
