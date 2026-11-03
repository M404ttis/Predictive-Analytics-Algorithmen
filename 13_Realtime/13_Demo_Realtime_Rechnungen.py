"""Tag 13, Realtime: Rechnungen zu Arbeitsauftrag 1, Fallstudie QuickRetail und Zusatz A13-4.

Reine Rechenbeispiele ohne Bibliotheken. Alle Werte mit "ANNAHME" stehen NICHT in den Aufgaben,
sondern sind Platzhalter für eine realistische Rechnung und lassen sich oben im Skript ändern.

Start (im Kursordner):
    .venv/bin/python 13_Realtime/13_Demo_Realtime_Rechnungen.py
"""

# --- Seilschaft Outdoor: wie groß ist der Datenstrom wirklich? ------------------------------
bestellungen_tag = 1500            # aus der Aufgabe (inkl. Marktplatz, ANNAHME: die 400 sind enthalten)
zahlungsmeldungen_je_bestellung = 2  # aus der Aufgabe: 1-3, ANNAHME Mittelwert
kasse_tag, lager_tag = 120, 2000   # aus der Aufgabe
events_tag = (bestellungen_tag * (1 + zahlungsmeldungen_je_bestellung) + kasse_tag + lager_tag)
print("== Seilschaft ==")
print(f"Ereignisse pro Tag      : {events_tag:,}  = {events_tag / 86_400:.2f} pro Sekunde (Mittel)")
spitze_h = 300 * (1 + zahlungsmeldungen_je_bestellung)
print(f"Samstagsspitze          : 300 Bestellungen/h -> {spitze_h} Ereignisse/h = {spitze_h / 3600:.2f} pro Sekunde")
print(f"Stornos 'nicht lieferbar': 290 von {400 * 365:,} Marktplatz-Bestellungen = {290 / (400 * 365):.2%}"
      f" (von allen {bestellungen_tag * 365:,}: {290 / (bestellungen_tag * 365):.3%}); Aufgabe nennt 1,8 %")

# --- QuickRetail, Situation 1: der virale Artikel ---------------------------------------------
print("\n== Situation 1: virale Trinkflasche ==")
rate_hype = 600 / 15               # Bestellungen pro Minute
rate_normal = 40 / 15              # ANNAHME: "~40" bedeutet ~40 je 15 Minuten
bestand, schwelle, lieferzeit_tage, mindestmenge = 500, 100, 5, 1000
print(f"Nachfrage Hype {rate_hype:.0f}/min = {rate_hype / rate_normal:.0f}x Normalbetrieb ({rate_normal:.1f}/min)")
print(f"Bestand {bestand} reicht {bestand / rate_hype:.1f} min (normal: {bestand / rate_normal / 60:.1f} h);"
      f" Schwelle {schwelle} erreicht nach {(bestand - schwelle) / rate_hype:.0f} min")
minuten = lieferzeit_tage * 24 * 60
for anteil in (1.0, 0.1):
    print(f"Bedarf in {lieferzeit_tage} Tagen bei {anteil:.0%} der Hype-Rate: {rate_hype * anteil * minuten:,.0f} Stück")
print(f"Bedarf in {lieferzeit_tage} Tagen bei Normalnachfrage: {rate_normal * minuten:,.0f} Stück"
      f" -> Mindestmenge {mindestmenge} deckt {mindestmenge / rate_normal / 60:.1f} h Normalnachfrage")

# --- Situation 2: Schwellen aus Fehlerkosten --------------------------------------------------
print("\n== Situation 2: Schwellen aus Fehlerkosten (ANNAHMEN: Marge 25 %, Kundenwert 30 EUR, Prüfung 5 EUR) ==")
marge, kundenwert, pruefkosten, gebuehr = 0.25, 30, 5, 15


def kosten(warenwert):
    fn = warenwert + gebuehr                 # Betrug durchgelassen: Ware weg + Rückbuchungsgebühr
    fp = warenwert * marge + kundenwert      # echten Kunden blockiert: Marge weg + Kunde verärgert
    return fn, fp


for wert in (80, 6400):
    fn, fp = kosten(wert)
    p_block = fp / (fp + fn)                 # ab hier ist Blocken billiger als Durchlassen
    p_frei = pruefkosten / fn                # darunter ist Durchlassen billiger als Prüfen
    p_hart = 1 - pruefkosten / fp            # darüber ist Blocken billiger als Prüfen
    print(f"Warenwert {wert:>5} EUR: FN {fn:>6.0f} EUR, FP {fp:>5.0f} EUR | Blocken statt Durchlassen ab p={p_block:.2f}"
          f" | Durchlassen unter p={p_frei:.4f} | Auto-Block erst ab p={max(p_hart, 0):.3f}")
fn, fp = kosten(6400)
p = 0.78
print(f"Fall 03:12 Uhr (p={p}): Durchlassen kostet im Mittel {p * fn:,.0f} EUR, Blocken {(1 - p) * fp:,.0f} EUR,"
      f" Prüfen {pruefkosten} EUR")

print("\nBetrugsquote 0,5 %, Spitze 5.000 Bestellungen/h:")
betrug_h = 5000 * 0.005
for fpr, recall in ((0.01, 0.9), (0.001, 0.9)):
    tp, fp_n = recall * betrug_h, fpr * (5000 - betrug_h)
    gepr = tp + fp_n
    print(f"  FPR {fpr:.1%}, Recall {recall:.0%}: {gepr:.0f} Fälle/h markiert, Precision {tp / gepr:.0%},"
          f" bei 5 Min/Fall (ANNAHME) {gepr * 5 / 60:.1f} Personen Dauerlast")

# --- Situation 3 und 4: Last und Ausfall ------------------------------------------------------
print("\n== Situation 3/4: Last und Ausfall ==")
print(f"Last x{12_000 / 2_000:.0f}, p99-Latenz x{340 / 70:.1f}; Budget 100 ms um {340 / 100:.1f}x überschritten")
for rate in (2_000, 12_000):
    rueckstand = 90 * rate
    print(f"Lag 90 s bei {rate:,}/s = {rueckstand:,} Ereignisse im Rückstand")
for kapazitaet in (3_000, 4_000, 6_000):
    print(f"  Aufholzeit bei {kapazitaet:,}/s Kapazität und 2.000/s Zufluss: {90 * 2_000 / (kapazitaet - 2_000):.0f} s")

# --- Zusatz A13-4: Prüfaufwand und Make-or-Buy ------------------------------------------------
print("\n== A13-4 Nordlicht Reisen (ANNAHME: 2 Min je Hoteltext, 8 Tage Bauaufwand) ==")
print(f"Hoteltexte alle prüfen: {2000 * 2 / 60:.0f} h; 5 % Stichprobe: {2000 * 0.05 * 2 / 60:.1f} h;"
      f" 10 %: {2000 * 0.10 * 2 / 60:.1f} h")
print(f"Wochenreport: 1 Tag/Woche Handarbeit = {46} Tage/Jahr; Bau 8 Tage lohnt nach {8} Wochen")
print(f"Newsletter: 1 % Fehlerquote bei 300.000 Empfängern = {300_000 * 0.01:,.0f} betroffene Empfänger")
