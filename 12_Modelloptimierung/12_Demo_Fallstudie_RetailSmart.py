"""Tag 12, Fallstudie RetailSmart: Random Forest bei ca. 5 % seltenen Ereignissen verbessern.

Die Fallstudie liefert keine Daten. Dies ist eine SIMULATION mit künstlichen Daten (ca. 6 % Ereignisse),
nur um den Ablauf zu zeigen: Aufteilen, Tuning mit stratifizierter CV auf der passenden Metrik,
Schwelle wählen, einmal auf dem Test prüfen. Die Zahlen sind NICHT die von RetailSmart.

Start (im Kursordner):
    .venv/bin/python 12_Modelloptimierung/12_Demo_Fallstudie_RetailSmart.py
"""
import time

import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score
from sklearn.model_selection import (RandomizedSearchCV, StratifiedKFold, cross_val_predict,
                                     train_test_split)

SEED = 42

# --- Daten: 20.000 Zeilen, ca. 6 % Ereignisse, bewusst schwer trennbar -----------------------
X, y = make_classification(n_samples=20_000, n_features=20, n_informative=6, n_redundant=4,
                           weights=[0.95], flip_y=0.03, class_sep=0.8, random_state=SEED)
print(f"Ereignisanteil: {y.mean():.1%}")


def kennzahlen(y_wahr, vorhersage):
    return (f"F1 {f1_score(y_wahr, vorhersage):.2f}  Recall {recall_score(y_wahr, vorhersage):.2f}  "
            f"Precision {precision_score(y_wahr, vorhersage):.2f}")


# --- 1. Aufteilen: Test einmal beiseite, stratifiziert -----------------------------------
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
print(f"Training {len(y_tr)} ({y_tr.mean():.1%} Ereignisse), Test {len(y_te)} ({y_te.mean():.1%})")

# --- 2. Ausgangslage: Standardmodell, Schwelle 0,5 ---------------------------------------
cv = StratifiedKFold(5, shuffle=True, random_state=SEED)
basis = RandomForestClassifier(random_state=SEED, n_jobs=-1)
p_cv = cross_val_predict(basis, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
print("\nStandard-Random-Forest, Schwelle 0,5 (CV auf Training):", kennzahlen(y_tr, p_cv >= 0.5))

# --- 3. Tuning: Zufallssuche mit F1/PR-AUC statt Accuracy, class_weight als Stellschraube ---
raster = {"n_estimators": [200, 400, 600], "max_depth": [6, 10, 15, None],
          "min_samples_leaf": [1, 3, 5, 10], "max_features": ["sqrt", 0.3, 0.5],
          "class_weight": [None, "balanced", "balanced_subsample"]}
suche = RandomizedSearchCV(RandomForestClassifier(random_state=SEED, n_jobs=-1), raster,
                           n_iter=20, cv=cv, scoring="average_precision", random_state=SEED)
start = time.time()
suche.fit(X_tr, y_tr)
print(f"\nZufallssuche: 20 Kombinationen x 5 Folds = 100 Läufe in {time.time() - start:.0f} s")
print("Bestes Setup:", suche.best_params_, f"PR-AUC (CV) {suche.best_score_:.3f}")

# --- 4. Schwelle wählen: auf Validierungsvorhersagen (CV), NICHT auf dem Test -------------
bestes = suche.best_estimator_
p_cv = cross_val_predict(bestes, X_tr, y_tr, cv=cv, method="predict_proba")[:, 1]
schwellen = np.linspace(0.05, 0.9, 86)
f1s = [f1_score(y_tr, p_cv >= s) for s in schwellen]
schwelle = float(schwellen[int(np.argmax(f1s))])
print(f"Beste Schwelle laut CV: {schwelle:.2f} -> {kennzahlen(y_tr, p_cv >= schwelle)}")

# --- 5. Einmal auf dem Test prüfen ---------------------------------------------------------
bestes.fit(X_tr, y_tr)
p_te = bestes.predict_proba(X_te)[:, 1]
basis.fit(X_tr, y_tr)
print("\nTest (einmal):")
print("  Standard, Schwelle 0,5 :", kennzahlen(y_te, basis.predict_proba(X_te)[:, 1] >= 0.5))
print(f"  Getunt, Schwelle {schwelle:.2f}  :", kennzahlen(y_te, p_te >= schwelle))
print(f"  PR-AUC Test: Standard {average_precision_score(y_te, basis.predict_proba(X_te)[:, 1]):.3f}, "
      f"getunt {average_precision_score(y_te, p_te):.3f}")

# --- 6. Zusatz: Zielwerte der Fallstudie zusammen erreichbar? -----------------------------
p, r = 0.70, 0.80
print(f"\nF1 bei Precision {p} und Recall {r} (beide genau am Ziel): {2 * p * r / (p + r):.3f}")
