# -*- coding: utf-8 -*-
"""
k-Fold Cross-Validation für die Kaffeerösterei Bohnenwerk
=========================================================

Sie müssen nur den Abschnitt "IHRE EINGABE" anpassen:
  FOLDS   – welche Wochen (1 bis 156) bilden welchen Fold?
            Jeder Fold ist einmal Testmenge, alle übrigen Folds sind dann
            die Trainingsmenge.

Danach starten:   python 1202_UE2_Arbeitsauftrag1_CV.py
(Die Datei 1202_UE2_Arbeitsauftrag1_Daten.csv muss im selben Ordner liegen.
 Es wird nur Standard-Python benötigt, keine weiteren Pakete.)

Das Modell ist eine lineare Regression: Umsatz_EUR aus den Spalten in MERKMALE.
"""

# ============================ IHRE EINGABE ==================================

# Wochen als Bereiche "von-bis", mehrere Bereiche mit Komma trennen.
# Woche 1 = 2023 KW 1, Woche 53 = 2024 KW 1, Woche 105 = 2025 KW 1.
# BEISPIEL mit 2 Folds – ersetzen Sie es durch Ihre eigene Aufteilung:
FOLDS = {
    1: "1-78",
    2: "79-156",
}

# Optional: Merkmale, aus denen das Modell den Umsatz vorhersagt.
# Sie können Spalten entfernen; sonst nichts ändern nötig.
MERKMALE = ["Woche", "Budget_Social_EUR", "Budget_Newsletter_EUR", "Budget_Print_EUR",
            "Rabattaktion", "Weihnachtsgeschaeft", "Temperatur_C"]

# Optional: True = jeder Durchlauf trainiert nur mit Wochen VOR seinem Testfold.
NUR_VERGANGENHEIT = False

# ========================= AB HIER NICHTS ÄNDERN ============================

import csv, os, sys

DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "1202_UE2_Arbeitsauftrag1_Daten.csv")


def lade_daten():
    with open(DATEI, encoding="utf-8") as f:
        zeilen = list(csv.DictReader(f, delimiter=";"))
    return [{k: float(v.replace(",", ".")) for k, v in z.items()} for z in zeilen]


def wochen_aus_text(text):
    wochen = set()
    for teil in str(text).replace(";", ",").split(","):
        teil = teil.strip()
        if not teil:
            continue
        if "-" in teil:
            a, b = (int(x) for x in teil.split("-", 1))
            wochen.update(range(min(a, b), max(a, b) + 1))
        else:
            wochen.add(int(teil))
    return wochen


def pruefe_folds(folds, n):
    zuordnung = {}
    for name, text in folds.items():
        for w in wochen_aus_text(text):
            if not 1 <= w <= n:
                sys.exit(f"Fehler: Woche {w} in Fold {name} gibt es nicht (nur 1 bis {n}).")
            if w in zuordnung:
                sys.exit(f"Fehler: Woche {w} steht in Fold {zuordnung[w]} und in Fold {name}.")
            zuordnung[w] = name
    fehlend = [w for w in range(1, n + 1) if w not in zuordnung]
    if fehlend:
        sys.exit(f"Fehler: {len(fehlend)} Wochen sind keinem Fold zugeordnet, "
                 f"z. B. {', '.join(map(str, fehlend[:10]))}.")
    if len(folds) < 2:
        sys.exit("Fehler: Es braucht mindestens 2 Folds.")


def trainiere(zeilen, merkmale):
    """Lineare Regression (kleinste Quadrate) über die Normalgleichungen.
    Merkmale, die in den Trainingswochen konstant sind, bekommen das Gewicht 0."""
    aktiv = [m for m in merkmale if len({z[m] for z in zeilen}) > 1]
    w_aktiv = _kleinste_quadrate(zeilen, aktiv)
    gewichte = dict(zip(aktiv, w_aktiv[1:]))
    return [w_aktiv[0]] + [gewichte.get(m, 0.0) for m in merkmale]


def _kleinste_quadrate(zeilen, merkmale):
    X = [[1.0] + [z[m] for m in merkmale] for z in zeilen]
    y = [z["Umsatz_EUR"] for z in zeilen]
    p = len(X[0])
    A = [[sum(r[i] * r[j] for r in X) for j in range(p)] for i in range(p)]
    b = [sum(r[i] * yi for r, yi in zip(X, y)) for i in range(p)]
    for i in range(p):                                 # Gauß-Elimination
        piv = max(range(i, p), key=lambda k: abs(A[k][i]))
        A[i], A[piv], b[i], b[piv] = A[piv], A[i], b[piv], b[i]
        if abs(A[i][i]) < 1e-9:
            sys.exit("Fehler: Zu wenige Trainingswochen für so viele Merkmale.")
        for k in range(i + 1, p):
            f = A[k][i] / A[i][i]
            A[k] = [a - f * c for a, c in zip(A[k], A[i])]
            b[k] -= f * b[i]
    w = [0.0] * p
    for i in reversed(range(p)):
        w[i] = (b[i] - sum(A[i][j] * w[j] for j in range(i + 1, p))) / A[i][i]
    return w


def vorhersage(w, z, merkmale):
    return w[0] + sum(wi * z[m] for wi, m in zip(w[1:], merkmale))


def zahl(x, nachkomma=0):
    return f"{x:,.{nachkomma}f}".replace(",", " ").replace(".", ",").replace(" ", ".")


def main():
    daten = lade_daten()
    n = len(daten)
    pruefe_folds(FOLDS, n)
    for m in MERKMALE:
        if m not in daten[0]:
            sys.exit(f"Fehler: Spalte {m} gibt es nicht.")

    print(f"Daten: {n} Wochen   Folds: {len(FOLDS)}   Merkmale: {len(MERKMALE)}"
          + ("   nur Vergangenheit" if NUR_VERGANGENHEIT else ""))
    print()
    print(f"{'Fold':<6}{'Testwochen':<22}{'Training':>9}{'Test':>6}{'MSE':>16}{'RMSE (EUR)':>12}")
    ergebnisse = []
    for name, text in FOLDS.items():
        test_w = wochen_aus_text(text)
        text = text if len(text) <= 20 else text[:19] + "…"
        test = [z for z in daten if z["Woche"] in test_w]
        train = [z for z in daten if z["Woche"] not in test_w]
        if NUR_VERGANGENHEIT:
            train = [z for z in train if z["Woche"] < min(test_w)]
        if len(train) <= len(MERKMALE) + 1:
            print(f"{str(name):<6}{text:<22}{len(train):>9}{len(test):>6}"
                  f"{'– zu wenig Training –':>28}")
            continue
        w = trainiere(train, MERKMALE)
        mse = sum((z["Umsatz_EUR"] - vorhersage(w, z, MERKMALE)) ** 2 for z in test) / len(test)
        ergebnisse.append(mse)
        print(f"{str(name):<6}{text:<22}{len(train):>9}{len(test):>6}"
              f"{zahl(mse):>16}{zahl(mse ** 0.5):>12}")

    if ergebnisse:
        mittel = sum(ergebnisse) / len(ergebnisse)
        print()
        print(f"Mittlerer MSE über {len(ergebnisse)} Folds: {zahl(mittel)}"
              f"   (RMSE: {zahl(mittel ** 0.5)} EUR)")
        print(f"Kleinster / größter MSE: {zahl(min(ergebnisse))} / {zahl(max(ergebnisse))}")


if __name__ == "__main__":
    main()
