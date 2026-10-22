"""Leckage-Test für das LightGBM-Modell (Bericht 3.8).
Idee: Eine Prognose mit Ursprung o darf nicht von Verkäufen NACH o abhängen. Wir ersetzen alle Verkäufe nach o durch
Zufallszahlen, rechnen das Modell neu und vergleichen. Ein sauberes Modell liefert identische Prognosen.
Ausführen: uv run python src/leakage_check.py   (Ausgabe: reports/leakage_check_output.txt)
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from forecast_eval import WINDOWS, load_clean  # noqa: E402
from gbm_model import Panel, fit_predict  # noqa: E402

lines = []


def out(msg=""):
    print(msg)
    lines.append(str(msg))


df = load_clean()
name = "W1 Aug 2017"
origin = WINDOWS[name]
pred_real, _, _ = fit_predict(Panel(df), origin)

df2 = df.copy()
future = (df2.date > origin) & df2.sales_train.notna()
rng = np.random.default_rng(1)
df2.loc[future, "sales_train"] = rng.integers(0, 5000, size=int(future.sum())).astype(float)
out(f"{name}: {int(future.sum()):,} Verkaufswerte nach {origin.date()} durch Zufallszahlen (0 bis 5000) ersetzt")
pred_fake, _, _ = fit_predict(Panel(df2), origin)

diff = float((pred_real - pred_fake).abs().to_numpy().max())
out(f"Größter Unterschied der Prognosen (Einheiten): {diff:.6g}")
out("ERGEBNIS: " + ("keine Abhängigkeit von Verkäufen nach dem Ursprung" if diff < 1e-6 else "ACHTUNG: Prognose hängt von der Zukunft ab"))
(ROOT / "reports" / "leakage_check_output.txt").write_text("\n".join(lines), encoding="utf-8")
