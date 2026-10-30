"""Tag 11, Zusatz A11-1: Wie stark beschönigen die vier verdächtigen Stellen die Güte?

Künstliche Kundendaten (Kündigung), 1.000 Kunden mit je 6 Monatszeilen. Die echten Merkmale
sagen die Kündigung nur schwach voraus. Dann bauen wir die vier Fehler der Folie einzeln ein.

Start (im Kursordner):
    .venv/bin/python 11_Modelltraining/11_Demo_Data_Leakage.py
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
N_KUNDEN, N_MONATE = 1000, 6


# =============================================================================
# Daten: pro Kunde feste Eigenschaften (stabil über die Monate) plus monatliches Rauschen
# =============================================================================
def erzeuge_daten():
    kunde = np.repeat(np.arange(N_KUNDEN), N_MONATE)
    kuendigt = (rng.random(N_KUNDEN) < 0.20).astype(int)           # 20 % kündigen
    alter = rng.normal(45, 12, N_KUNDEN)                           # feste Kundeneigenschaften
    laufzeit = rng.normal(30, 15, N_KUNDEN) - 9 * kuendigt         # schwacher echter Zusammenhang
    grundpreis = rng.normal(40, 8, N_KUNDEN) + 3 * kuendigt      # schwacher echter Zusammenhang
    df = pd.DataFrame({
        "kunde": kunde,
        "alter": alter[kunde] + rng.normal(0, 0.3, len(kunde)),
        "laufzeit_monate": laufzeit[kunde] + rng.normal(0, 0.3, len(kunde)),
        "grundpreis": grundpreis[kunde] + rng.normal(0, 0.3, len(kunde)),
        "beschwerden": rng.poisson(0.4 + 0.9 * kuendigt[kunde]),   # monatlich neu gezogen
        "kuendigung": kuendigt[kunde],
    })
    # a) Merkmal "Vertrag bereits gekündigt": entsteht erst NACH der Kündigung (nicht ganz lückenlos gepflegt)
    gepflegt = rng.random(N_KUNDEN) < 0.95
    df["vertrag_gekuendigt"] = (df["kuendigung"] * gepflegt[kunde]).astype(int)
    # d) Merkmal "Umsatz der Folgemonate": Kündiger zahlen danach wenig oder nichts
    anteil = np.where(df["kuendigung"] == 1, rng.uniform(0.0, 0.7, len(df)), rng.uniform(0.6, 1.1, len(df)))
    df["umsatz_folgemonate"] = df["grundpreis"] * anteil
    return df


def bewerte(X_train, X_test, y_train, y_test, modell=None):
    modell = modell or RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
    modell.fit(X_train, y_train)
    pred = modell.predict(X_test)
    return accuracy_score(y_test, pred), recall_score(y_test, pred)


def split_nach_kunde(df):
    """Alle Zeilen eines Kunden landen entweder in Training oder in Test."""
    teiler = GroupShuffleSplit(n_splits=1, test_size=0.3, random_state=42)
    train, test = next(teiler.split(df, groups=df["kunde"]))
    return df.iloc[train], df.iloc[test]


def split_zufaellig(df):
    """Zeilen zufällig mischen: derselbe Kunde kann in beiden Teilen sein."""
    return train_test_split(df, test_size=0.3, random_state=42)


ECHT = ["alter", "laufzeit_monate", "grundpreis", "beschwerden"]


def lauf(name, df, merkmale, split, skaliere_vorher=False, modell=None):
    df = df.copy()
    df[merkmale] = df[merkmale].astype(float)
    if skaliere_vorher:                      # b) Skalierung über ALLE Daten, vor dem Split
        df[merkmale] = StandardScaler().fit_transform(df[merkmale])
    train, test = split(df)
    X_train, X_test = train[merkmale], test[merkmale]
    if not skaliere_vorher:                  # sauber: Skalierung nur mit den Trainingsdaten
        skalierer = StandardScaler().fit(X_train)
        X_train, X_test = skalierer.transform(X_train), skalierer.transform(X_test)
    acc, rec = bewerte(X_train, X_test, train["kuendigung"], test["kuendigung"], modell)
    print(f"{name:58s} Genauigkeit {acc:6.1%}   Recall (Kündiger) {rec:6.1%}")


# =============================================================================
# Ablauf
# =============================================================================
def main():
    df = erzeuge_daten()
    print(f"Anteil Kündiger: {df['kuendigung'].mean():.0%}  "
          f"(wer immer 'bleibt' sagt, hat {1 - df['kuendigung'].mean():.0%} Genauigkeit)\n")
    lauf("Sauber (Split nach Kunde, Skalierung nur auf Training)", df, ECHT, split_nach_kunde)
    lauf("b) Skalierung über alle Daten vor dem Split", df, ECHT, split_nach_kunde, skaliere_vorher=True)
    print("   (Random Forest braucht keine Skalierung, daher kein Unterschied. Mit einem abstandsbasierten Modell:)")
    lauf("   KNN, sauber skaliert", df, ECHT, split_nach_kunde, modell=KNeighborsClassifier())
    lauf("   KNN, b) vor dem Split skaliert", df, ECHT, split_nach_kunde, True, KNeighborsClassifier())
    lauf("c) Gleicher Kunde in Training und Test (Zufallssplit)", df, ECHT, split_zufaellig)
    lauf("a) + Merkmal 'Vertrag bereits gekündigt'", df, ECHT + ["vertrag_gekuendigt"], split_nach_kunde)
    lauf("d) + Merkmal 'Umsatz der Folgemonate'", df, ECHT + ["umsatz_folgemonate"], split_nach_kunde)
    lauf("alle vier Fehler zusammen", df, ECHT + ["vertrag_gekuendigt", "umsatz_folgemonate"],
         split_zufaellig, skaliere_vorher=True)


if __name__ == "__main__":
    main()
