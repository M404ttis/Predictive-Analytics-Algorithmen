"""Phase G: Gegenproben zum LightGBM-Modell, Bericht 3.9.
Ausführen: uv run python -u src/counter_tests.py   (dauert ca. 15 Minuten; Ausgabe: reports/counter_tests_output.txt, reports/results_counter_tests.csv)
Vorher: src/clean.py muss gelaufen sein.
"""
# %%
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().resolve().parent  # Skript oder Notebook
sys.path.insert(0, str(ROOT / "src"))
from forecast_eval import WINDOWS, load_clean, score, window_frames  # noqa: E402
from gbm_model import DEFAULT_DROP, Panel, fit_predict  # noqa: E402
from masking import spike_flags  # noqa: E402

pd.set_option("display.width", 170)
lines = []


def out(msg=""):
    print(msg, flush=True)
    lines.append(str(msg))


df = load_clean()

# %% [markdown]
# ## 1. Was wird getestet?
# Jede Gegenprobe ändert **eine** Sache gegenüber dem Basismodell (Bericht 3.8) und rechnet alle drei Fenster neu.
# Bewertet wird immer auf denselben Zeilen mit demselben Rohwert `sales`, nur das Training ändert sich.
#
# | Gruppe | Frage |
# |---|---|
# | Rauschen | Wie stark schwankt das Ergebnis, wenn nur die Zufallszahlen anders sind? Das ist die Messlatte für alles andere. |
# | Merkmale weglassen | Welche Merkmalsgruppe zieht wirklich Gewicht? |
# | Ölpreis | Hilft der Ölpreis (am Ursprung bekannt)? |
# | `promo_known` | Hilft es, nur mit verlässlichen Aktionsangaben zu trainieren? |
# | Maskierung | Spielt es eine Rolle, ob und wie streng Spitzen maskiert werden? |

# %%
GROUPS = {
    "aktion": ("aktion", "aktion_bekannt"),
    "kalender_feiertag": ("feiertag", "ereignis", "arbeitstag_ausgleich"),
    "monat": ("monat", "tag_im_monat"),
    "filiale_familie": ("family", "store", "type", "city", "state", "cluster"),
}
ALL_GROUPS = tuple(c for g in GROUPS.values() for c in g)
VARIANTS = [
    ("Basis", {}),
    ("Basis, andere Zufallszahlen", {"seed": 1}),
    ("ohne Aktion", {"drop": DEFAULT_DROP + GROUPS["aktion"]}),
    ("ohne Feiertage und Ereignisse", {"drop": DEFAULT_DROP + GROUPS["kalender_feiertag"]}),
    ("ohne Monat und Tag im Monat", {"drop": DEFAULT_DROP + GROUPS["monat"]}),
    ("ohne Filial- und Familienmerkmale", {"drop": DEFAULT_DROP + GROUPS["filiale_familie"]}),
    ("nur Verkaufshistorie und Wochentag", {"drop": DEFAULT_DROP + ALL_GROUPS}),
    ("mit Ölpreis", {"drop": ()}),
    ("Training nur mit promo_known = 1", {"only_promo_known": True}),
]
MASKING = [("keine Maskierung der Spitzen", None), ("Maskierung Faktor 5", 5)]

truths = {name: window_frames(df, origin) for name, origin in WINDOWS.items()}
panel = Panel(df)
rows, fam_w1 = [], {}


def run(label, pnl, **kw):
    t0 = time.time()
    vals, fam = {}, None
    for name, origin in WINDOWS.items():
        pred, _, _ = fit_predict(pnl, origin, **kw)
        truth, excluded, outlier = truths[name]
        r = score(truth, pred, excluded, outlier)
        vals[name] = r["rmsle"]
        if name.startswith("W1"):
            fam = r["je_familie"]
    fam_w1[label] = fam
    rows.append({"Variante": label, **vals})
    out(f"{label}: " + ", ".join(f"{k.split()[0]} {v:.4f}" for k, v in vals.items()) + f"  ({time.time() - t0:.0f} s)")


for label, kw in VARIANTS:
    run(label, panel, **kw)

# %% [markdown]
# ## 2. Maskierung der Spitzen
# Hier ändert sich das Training: Die Spalte `sales_train` wird mit einer anderen Regel maskiert (Bericht 2.9).
# Geschlossene Tage und Filialen bleiben in allen Varianten maskiert. Bewertet wird weiter auf dem Rohwert.

# %%
closed = (df.is_closed_day == 1) | (df.is_store_closed == 1)
for label, factor in MASKING:
    d2 = df.copy()
    spike = spike_flags(df, factor) if factor else pd.Series(False, index=df.index)
    d2["sales_train"] = df.sales.where(~(closed | spike))
    out(f"[{label}] maskierte Spitzen: {int(spike.sum())}")
    run(label, Panel(d2))

# %% [markdown]
# ## 3. Ergebnis
# `Änderung` = Mittel der drei Fenster gegenüber dem Basismodell. Positiv = schlechter. Das Rauschen steht in der Zeile
# „Basis, andere Zufallszahlen“: Änderungen in dieser Größe sind nicht von Zufall zu unterscheiden.

# %%
res = pd.DataFrame(rows).set_index("Variante")
res["Mittel"] = res[list(WINDOWS)].mean(axis=1)
res["Änderung"] = (res.Mittel / res.loc["Basis", "Mittel"] - 1).map("{:+.1%}".format)
for w in WINDOWS:
    res[f"Δ {w.split()[0]}"] = (res[w] / res.loc["Basis", w] - 1).map("{:+.1%}".format)
out("\n" + res.round(4).to_string())
noise = abs(res.loc["Basis, andere Zufallszahlen", "Mittel"] / res.loc["Basis", "Mittel"] - 1)
out(f"\nRauschen (Mittel der drei Fenster, anderer Zufall): {noise:.2%}")

# %% [markdown]
# ## 4. Welche Familien leiden, wenn eine Merkmalsgruppe fehlt? (Fenster W1)

# %%
base = pd.Series(fam_w1["Basis"])
for label in ["ohne Aktion", "ohne Feiertage und Ereignisse", "ohne Monat und Tag im Monat", "ohne Filial- und Familienmerkmale"]:
    d = (pd.Series(fam_w1[label]) / base - 1).sort_values(ascending=False)
    out(f"\n{label}: am stärksten verschlechtert (W1)")
    out(d.head(5).map("{:+.1%}".format).to_string())
    out(f"Familien verschlechtert um mehr als 2 %: {int((d > 0.02).sum())} von {len(d)}")

# %%
res.to_csv(ROOT / "reports" / "results_counter_tests.csv")
(ROOT / "reports" / "counter_tests_output.txt").write_text("\n".join(lines), encoding="utf-8")
