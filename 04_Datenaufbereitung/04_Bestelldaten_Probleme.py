# Arbeitsauftrag 1 (UE 2): Bestelldaten eines Online-Shops
# Das Skript bereinigt NICHTS, sondern benennt Annahmen, was schiefgelaufen sein
# könnte, und belegt sie mit Kennzahlen aus der CSV-Datei.
# Ausgabe: Konsole UND ein formatierter Markdown-Bericht (04_Bestelldaten_Probleme_Bericht.md)
#
# Ausführen:  python3 04_Bestelldaten_Probleme.py

# %%
import re
from datetime import date
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent if "__file__" in globals() else Path.cwd()
CSV = BASE / "04_Bestelldaten_Arbeitsauftrag1.csv"
BERICHT = BASE / "04_Bestelldaten_Probleme_Bericht.md"

SPALTEN = ["BestellID", "Datum", "KundenID", "Name", "E-Mail", "Produkt", "Menge", "Umsatz (EUR)"]
MONATE = {"januar": 1, "februar": 2, "märz": 3, "april": 4, "mai": 5, "juni": 6, "juli": 7,
          "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12}
AMPEL = {"hoch": "🔴 hoch", "mittel": "🟠 mittel", "gering": "🟡 gering"}


# %%
# Berichts-Helfer: jede Ausgabe geht in die Konsole und in den Markdown-Bericht
class Bericht:
    def __init__(self):
        self.md = []
        self.titel = []

    @staticmethod
    def _zelle(wert):
        if pd.isna(wert) if not isinstance(wert, (list, tuple)) else False:
            return "–"
        if isinstance(wert, float):
            return f"{wert:.2f}"
        return str(wert)

    def abschnitt(self, titel):
        print(f"\n{'=' * 72}\n{titel}\n{'=' * 72}")
        self.titel.append(titel)
        self.md += [f"## {titel}", ""]

    def text(self, konsole="", md=None):
        print(konsole)
        self.md += [konsole if md is None else md, ""]

    def liste(self, punkte):
        for p in punkte:
            print(f"  - {p}")
        self.md += [f"- {p}" for p in punkte] + [""]

    def annahmen(self, punkte):
        for p in punkte:
            print(f"  Annahme: {p}")
        self.md += ["**Annahmen**", ""] + [f"- {p}" for p in punkte] + [""]

    def tabelle(self, df, index=False):
        if index:
            df = df.reset_index()
        kopf = [str(c) for c in df.columns]
        zeilen = [[self._zelle(w) for w in z] for z in df.itertuples(index=False)]
        # Konsole: linksbündig, Spalten nach breitestem Eintrag
        breiten = [max(len(k), *(len(z[i]) for z in zeilen)) for i, k in enumerate(kopf)]
        print("  " + "  ".join(k.ljust(b) for k, b in zip(kopf, breiten)))
        print("  " + "  ".join("-" * b for b in breiten))
        for z in zeilen:
            print("  " + "  ".join(c.ljust(b) for c, b in zip(z, breiten)))
        print()
        # Markdown: Ampel-Spalte mit Emojis
        md_zeilen = []
        for z in zeilen:
            z = [AMPEL.get(c, c) if k == "Schwere" else c for k, c in zip(kopf, z)]
            md_zeilen.append("| " + " | ".join(c.replace("|", "\\|") for c in z) + " |")
        self.md += ["| " + " | ".join(kopf) + " |", "|" + "|".join(" --- " for _ in kopf) + "|",
                    *md_zeilen, ""]

    @staticmethod
    def _anker(titel):
        return re.sub(r"[^\w\- ]", "", titel.lower()).replace(" ", "-")

    def speichern(self, pfad, kopf_md):
        inhalt = [f"# Bestelldaten: Datenprobleme und Annahmen", "",
                  f"*Quelle: `{CSV.name}` · erzeugt von `{Path(__file__).name if '__file__' in globals() else 'Notebook'}` · "
                  f"{date.today():%d.%m.%Y}*", "", *kopf_md,
                  "## Inhalt", "",
                  *[f"- [{t}](#{self._anker(t)})" for t in self.titel], "",
                  "---", "", *self.md]
        pfad.write_text("\n".join(inhalt), encoding="utf-8")


b = Bericht()


# %%
# 1. Rohdatei: Ist schon die Dateistruktur kaputt?
b.abschnitt("1. Rohdatei: Struktur")

roh_bytes = CSV.read_bytes()
hat_bom = roh_bytes.startswith(b"\xef\xbb\xbf")
zeilen = roh_bytes.decode("utf-8-sig").splitlines()

try:
    naiv = pd.read_csv(CSV, sep=";", encoding="utf-8-sig")
    naiv_text = f"{naiv.shape[0]} Zeilen x {naiv.shape[1]} Spalte(n)"
except Exception as fehler:
    naiv_text = f"Fehler ({type(fehler).__name__}: {fehler})"

# Zeilenmuster: ganze Zeile steckt in EINEM Anführungszeichen-Paar: "Feld;Feld;...;Umsatz"
MUSTER = re.compile(r'^"(.*)"$')
eingepackt = [i for i, z in enumerate(zeilen, start=1) if MUSTER.match(z)]
leer = [i for i, z in enumerate(zeilen, start=1) if not z.strip()]
nur_trenner = [i for i, z in enumerate(zeilen, start=1) if z.strip() and not re.search(r"\w", z)]

b.tabelle(pd.DataFrame([
    ("Zeilen in der Datei", len(zeilen)),
    ("Byte Order Mark (BOM) am Dateianfang", "ja" if hat_bom else "nein"),
    ("Naives `pd.read_csv(sep=';')`", naiv_text),
    ("Zeilen komplett in ein Anführungszeichen-Paar gepackt", f"{len(eingepackt)} von {len(zeilen)}"),
    ("Leere Zeilen", f"{len(leer)}"),
    ("Zeilen nur aus Trennzeichen", f"{len(nur_trenner)} (Zeile {', '.join(map(str, nur_trenner))})"),
], columns=["Prüfung", "Ergebnis"]))
b.annahmen([
    "Excel hat jede Zeile als ein einziges Textfeld exportiert (Anführungszeichen um die ganze Zeile). "
    "Ein normaler CSV-Reader sieht daher nur eine Spalte.",
    "Die Zeile mit nur `;` ist ein Excel-Artefakt (leere Zeile mit Spaltentrenner) und kein Datensatz.",
    "Das BOM stammt vom Excel-Export; ohne `utf-8-sig` würde es im ersten Spaltennamen landen.",
])

# %%
# 2. Parsen: Zeilen manuell zerlegen
b.abschnitt("2. Parsen und Typen")

zeilen_daten = []
nicht_lesbar = []
for nr, zeile in enumerate(zeilen[1:], start=2):
    m = MUSTER.match(zeile)
    if not m:
        if zeile.strip() and re.search(r"\w", zeile):
            nicht_lesbar.append(nr)
        continue
    felder = m.group(1).split(";")
    if len(felder) != len(SPALTEN):
        nicht_lesbar.append(nr)
        continue
    zeilen_daten.append(felder)

df = pd.DataFrame(zeilen_daten, columns=SPALTEN).replace("", pd.NA)
kurze_cents = [x for x in df["Umsatz (EUR)"] if "," in x and len(x.split(",")[1]) < 2]

df["Menge"] = pd.to_numeric(df["Menge"])
df["Umsatz"] = pd.to_numeric(df["Umsatz (EUR)"].str.replace(",", ".", regex=False))

b.tabelle(pd.DataFrame([
    ("Gelesene Datenzeilen", len(df)),
    ("Nicht lesbare Zeilen", f"{len(nicht_lesbar)}" + (f" (Zeile {', '.join(map(str, nicht_lesbar))})" if nicht_lesbar else "")),
    ("Umsatz mit nur 1 Nachkommastelle", ", ".join(f"'{c}'" for c in kurze_cents) or "keine"),
    ("Typ `Menge`", str(df["Menge"].dtype)),
    ("Typ `Umsatz` (nach Komma-Ersetzung)", str(df["Umsatz"].dtype)),
], columns=["Prüfung", "Ergebnis"]))
b.annahmen([
    "Der Umsatz ist als Text mit Dezimalkomma gespeichert und muss in eine Zahl umgewandelt werden.",
    "`199,0` hat nur eine Nachkommastelle: vermutlich `199,00` (Excel schneidet abschließende Nullen ab). Unkritisch, da die Null eindeutig ist.",
])

# %%
# 3. Fehlende Werte (Vollständigkeit)
b.abschnitt("3. Fehlende Werte")

fehlt = df.isna().sum()
fehlt = fehlt[fehlt > 0]
b.tabelle(pd.DataFrame([
    (spalte, anzahl, f"{anzahl / len(df):.0%}", ", ".join(df.loc[df[spalte].isna(), "BestellID"]))
    for spalte, anzahl in fehlt.items()
], columns=["Spalte", "Fehlend", "Anteil", "BestellIDs"]))

zeilen_mit_luecke = int(df.isna().any(axis=1).sum())
b.text(f"Zeilen mit mindestens einer Lücke: {zeilen_mit_luecke} von {len(df)} "
       f"({zeilen_mit_luecke / len(df):.0%})",
       f"**Zeilen mit mindestens einer Lücke:** {zeilen_mit_luecke} von {len(df)} "
       f"({zeilen_mit_luecke / len(df):.0%})")

# Lassen sich Lücken aus anderen Zeilen rekonstruieren?
rekonstruktion = []
for _, z in df[df.isna().any(axis=1)].iterrows():
    for c in [c for c in ["KundenID", "Name", "E-Mail"] if pd.isna(z[c])]:
        if c != "KundenID" and pd.notna(z["KundenID"]):
            quelle = df[(df["KundenID"] == z["KundenID"]) & df[c].notna()][c]
        elif c == "KundenID" and pd.notna(z["Name"]):
            quelle = df[(df["Name"] == z["Name"]) & df[c].notna()][c]
        else:
            quelle = pd.Series(dtype=str)
        rekonstruktion.append((z["BestellID"], c, f"ja ({quelle.iloc[0]})" if len(quelle) else "nein"))
b.text("Rekonstruierbar aus anderen Bestellungen desselben Kunden?",
       "**Rekonstruierbar aus anderen Bestellungen desselben Kunden?**")
b.tabelle(pd.DataFrame(rekonstruktion, columns=["BestellID", "Fehlendes Feld", "Rekonstruierbar"]))
b.annahmen([
    "Pflichtfelder fehlten im Erfassungsformular bzw. wurden nicht erzwungen.",
    "Eine fehlende KundenID ist kritischer als eine fehlende E-Mail (Kunde nicht zuordenbar).",
])

# %%
# 4. Dubletten
b.abschnitt("4. Dubletten")

# nur die Originalspalten vergleichen (spätere Hilfsspalten enthalten Listen)
n_dubletten = int(df.duplicated(subset=SPALTEN).sum())
exakt = df[df.duplicated(subset=SPALTEN, keep=False)]
doppelte_id = df[df.duplicated("BestellID", keep=False)]
umsatz_roh = df["Umsatz"].sum()
umsatz_ohne = df.drop_duplicates(subset=SPALTEN)["Umsatz"].sum()

b.tabelle(pd.DataFrame([
    ("Exakte Dubletten (alle Spalten gleich)", f"{n_dubletten} überzählige Zeile(n)"),
    ("Betroffene BestellIDs", ", ".join(sorted(exakt["BestellID"].unique()))),
    ("Gleiche BestellID, andere Inhalte", f"{len(doppelte_id) - len(exakt)} (0 = alle ID-Dubletten sind exakte Kopien)"),
    ("Zeilen roh → ohne Dubletten", f"{len(df)} → {len(df.drop_duplicates(subset=SPALTEN))}"),
    ("Umsatz roh", f"{umsatz_roh:.2f} EUR"),
    ("Umsatz ohne Dubletten", f"{umsatz_ohne:.2f} EUR"),
    ("Verzerrung durch Dubletten", f"+{umsatz_roh - umsatz_ohne:.2f} EUR ({(umsatz_roh - umsatz_ohne) / umsatz_ohne:.1%})"),
], columns=["Prüfung", "Ergebnis"]))
b.annahmen([
    "Doppelter Export oder Doppelklick beim Absenden: gleiche BestellID = gleiche Bestellung.",
    "Löschen ist nur unkritisch, weil eine BestellID nur einmal vorkommen darf.",
])

# %%
# 5. Datumsformate (Konsistenz)
b.abschnitt("5. Datumsformate")


def datum_kandidaten(text):
    """Liefert (Formatname, [mögliche Daten]); mehrere Daten = mehrdeutig."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return "ISO (JJJJ-MM-TT)", [date.fromisoformat(text)]
    if m := re.fullmatch(r"(\d{2})\.(\d{2})\.(\d{4})", text):
        t, mo, j = map(int, m.groups())
        return "deutsch (TT.MM.JJJJ)", [date(j, mo, t)]
    if m := re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", text):
        a, c, j = map(int, m.groups())
        kandidaten = [date(j, a, c)]                    # US: MM/TT/JJJJ
        if a != c and a <= 12 and c <= 12:
            kandidaten.append(date(j, c, a))            # EU: TT/MM/JJJJ
        return "Schrägstrich (MM/TT oder TT/MM)", kandidaten
    if m := re.fullmatch(r"(\d{1,2})\.\s*(\w+)\s+(\d{4})", text):
        t, monat, j = int(m.group(1)), m.group(2).lower(), int(m.group(3))
        return "Text (5. März 2024)", [date(j, MONATE[monat], t)]
    return "unbekannt", []


ergebnis = [datum_kandidaten(d) for d in df["Datum"]]
df["Datumsformat"] = [e[0] for e in ergebnis]
df["Datum_kandidaten"] = [e[1] for e in ergebnis]

formate = df["Datumsformat"].value_counts().rename_axis("Format").reset_index(name="Anzahl")
b.tabelle(formate)
b.text(f"Anzahl verschiedener Formate: {df['Datumsformat'].nunique()}",
       f"**Anzahl verschiedener Formate:** {df['Datumsformat'].nunique()}")

mehrdeutig = []
for i, kand in df["Datum_kandidaten"].items():
    if len(kand) > 1:
        vorher = df["Datum_kandidaten"].iloc[i - 1][0] if i > 0 else None
        nachher = df["Datum_kandidaten"].iloc[i + 1][0] if i + 1 < len(df) else None
        passt = [str(k) for k in kand if vorher and nachher and vorher <= k <= nachher]
        mehrdeutig.append((df.at[i, "BestellID"], df.at[i, "Datum"], " oder ".join(str(k) for k in kand),
                           f"{vorher} … {nachher}", ", ".join(passt) if passt else "keine Variante"))
b.text("Mehrdeutige Daten:", "**Mehrdeutige Daten**")
b.tabelle(pd.DataFrame(mehrdeutig, columns=["BestellID", "Rohwert", "Mögliche Daten",
                                            "Nachbarn (nach BestellID)", "Passt zur Reihenfolge"]))
b.annahmen([
    "Bei `03/05/2024` wird MM/TT (US) angenommen, weil die Datei sonst deutsch formatiert ist.",
    "Eigentlich nicht entscheidbar: Rückfrage bei der Quelle nötig.",
])

df["Datum_parsed"] = [k[0] if k else pd.NaT for k in df["Datum_kandidaten"]]

ruecksprung = []
for i in range(1, len(df)):
    if df.at[i, "Datum_parsed"] < df.at[i - 1, "Datum_parsed"]:
        ruecksprung.append((df.at[i, "BestellID"], str(df.at[i, "Datum_parsed"]),
                            df.at[i - 1, "BestellID"], str(df.at[i - 1, "Datum_parsed"])))
b.text("Reihenfolge der Daten (BestellIDs werden als chronologisch angenommen):",
       "**Reihenfolge der Daten** (BestellIDs werden als chronologisch angenommen)")
if ruecksprung:
    b.tabelle(pd.DataFrame(ruecksprung, columns=["Zeile", "Datum", "steht nach", "Datum davor"]))
else:
    b.text("  keine Rücksprünge")
b.annahmen(["Der erste Rücksprung (B-1005) entsteht nur durch die MM/TT-Annahme bei B-1004; "
            "mit anderer Lesart (03. Mai) wäre die Lücke noch größer."])
b.text(f"Zeitraum: {df['Datum_parsed'].min()} bis {df['Datum_parsed'].max()}",
       f"**Zeitraum:** {df['Datum_parsed'].min()} bis {df['Datum_parsed'].max()}")

# %%
# 6. Negative Werte (Genauigkeit)
b.abschnitt("6. Negative Mengen und Umsätze")

neg = df[(df["Menge"] < 0) | (df["Umsatz"] < 0)]
retouren = []
for i, z in neg.iterrows():
    vorher = df.loc[:i - 1]
    vorkauf = vorher[(vorher["KundenID"] == z["KundenID"]) & (vorher["Produkt"] == z["Produkt"])
                     & (vorher["Menge"] > 0)]
    retouren.append((z["BestellID"], z["Produkt"], z["Menge"], z["Umsatz"], "ja" if len(vorkauf) else "nein"))
b.tabelle(pd.DataFrame(retouren, columns=["BestellID", "Produkt", "Menge", "Umsatz (EUR)",
                                          "Originalkauf vorhanden"]))

vorzeichen_ungleich = df[(df["Menge"] < 0) != (df["Umsatz"] < 0)]
b.liste([
    f"Zeilen mit negativer Menge oder negativem Umsatz: {len(neg)}",
    f"Zeilen mit unterschiedlichem Vorzeichen (Menge vs. Umsatz): {len(vorzeichen_ungleich)}",
    f"Umsatz der negativen Zeilen: {neg['Umsatz'].sum():.2f} EUR",
])
b.annahmen([
    "Negative Zeilen sind Retouren/Stornos, keine Tippfehler, denn Menge UND Umsatz sind negativ.",
    "Aber: Kein passender Originalkauf im Datensatz → Retoure aus früherem Zeitraum oder Fehlbuchung.",
    "Für 'Absatz pro Produkt' würden Retouren die Menge verfälschen; für den Umsatz sind sie echt.",
])

# %%
# 7. Plausibilität: Stückpreise und Ausreißer
b.abschnitt("7. Plausibilität: Stückpreis und Ausreißer")

df["Stückpreis"] = (df["Umsatz"] / df["Menge"]).round(2)
preise = df.groupby("Produkt")["Stückpreis"].agg(["count", "min", "max", "nunique"]).reset_index()
preise.columns = ["Produkt", "Zeilen", "Stückpreis min", "Stückpreis max", "Verschiedene Preise"]
b.text("Stückpreis (Umsatz / Menge) je Produkt:", "**Stückpreis (Umsatz / Menge) je Produkt**")
b.tabelle(preise)
b.annahmen(["Umsatz = Menge × Stückpreis, der Preis ist je Produkt konstant → der Umsatz ist intern konsistent."])

q1, q3 = df["Umsatz"].quantile([0.25, 0.75])
iqr = q3 - q1
unten, oben = q1 - 1.5 * iqr, q3 + 1.5 * iqr
ausreisser = df[(df["Umsatz"] < unten) | (df["Umsatz"] > oben)]
b.text(f"Umsatz: Q1 {q1:.2f}, Q3 {q3:.2f}, IQR-Grenzen [{unten:.2f}, {oben:.2f}]",
       f"**Umsatz:** Q1 {q1:.2f}, Q3 {q3:.2f}, IQR-Grenzen [{unten:.2f}, {oben:.2f}]")
b.tabelle(ausreisser[["BestellID", "Produkt", "Menge", "Umsatz"]])
b.annahmen([
    "Die Ausreißer sind erklärbar (teures Produkt, Menge 2, Retouren sind negativ), "
    "also echte Extreme statt Tippfehler → nicht blind entfernen (prüfen, dann entscheiden).",
])

# %%
# 8. Kunden: Konsistenz von ID, Name und E-Mail
b.abschnitt("8. Kundenstammdaten")

pro_id = df.groupby("KundenID").agg(namen=("Name", "nunique"), mails=("E-Mail", "nunique"))
pro_mail = df.dropna(subset=["E-Mail"]).groupby("E-Mail")["KundenID"].nunique()
mail_ok = df["E-Mail"].dropna().str.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+")
b.tabelle(pd.DataFrame([
    ("Verschiedene KundenIDs", len(pro_id)),
    ("KundenIDs mit mehr als einem Namen/einer E-Mail", int(((pro_id["namen"] > 1) | (pro_id["mails"] > 1)).sum())),
    ("E-Mails, die zu mehreren KundenIDs gehören", int((pro_mail > 1).sum())),
    ("Ungültig aufgebaute E-Mails", int((~mail_ok).sum())),
], columns=["Prüfung", "Ergebnis"]))
b.annahmen([
    "Mögliche Dubletten wie 'Marie Müller' / 'M. Müller' (Folie) sind hier nicht erkennbar.",
    f"Bei nur {len(pro_id)} Kunden ist ein Abgleich per Name/E-Mail möglich; "
    "in großen Beständen wäre Fuzzy-Matching nötig.",
])

# %%
# 9. Befunde pro Zeile
b.abschnitt("9. Befunde pro Zeile")

ISO = "ISO (JJJJ-MM-TT)"
befunde = {i: [] for i in df.index}
for i in exakt.index:
    befunde[i].append("Dublette")
for i, z in df.iterrows():
    fehlende = [c for c in ["KundenID", "Name", "E-Mail"] if pd.isna(z[c])]
    if fehlende:
        befunde[i].append("fehlt: " + ", ".join(fehlende))
    if z["Datumsformat"] != ISO:
        befunde[i].append("Datum: " + z["Datumsformat"].split(" ")[0])
    if len(z["Datum_kandidaten"]) > 1:
        befunde[i].append("Datum mehrdeutig")
for i in neg.index:
    befunde[i].append("negativ (Retoure?)")
for i in ausreisser.index:
    befunde[i].append("Umsatz-Ausreißer")
for bestell_id, *_ in ruecksprung:
    for i in df.index[df["BestellID"] == bestell_id]:
        befunde[i].append("Datum springt zurück")

zeilen_tabelle = df[["BestellID", "Datum", "KundenID", "Produkt", "Menge", "Umsatz"]].copy()
zeilen_tabelle["Befunde"] = ["; ".join(befunde[i]) or "–" for i in df.index]
b.tabelle(zeilen_tabelle)
zeilen_mit_befund = sum(1 for v in befunde.values() if v)

# %%
# 10. Zusammenfassung
b.abschnitt("10. Zusammenfassung: Problem, Umfang, Vorschlag")

n = len(df)
kern = df.drop_duplicates(subset=SPALTEN)
ohne_retouren = kern.loc[kern["Umsatz"] > 0, "Umsatz"].sum()
tabelle = pd.DataFrame([
    ("Dateistruktur (Zeile als ein Textfeld, BOM)", "hoch", f"alle {len(eingepackt)} Zeilen",
     "korrekt einlesen: Anführungszeichen entfernen, dann splitten (zuerst!)"),
    ("Exakte Dubletten", "hoch", f"{n_dubletten} Zeile(n), +{umsatz_roh - umsatz_ohne:.2f} EUR Umsatz",
     "löschen (BestellID eindeutig)"),
    ("Datumsformate gemischt", "mittel", f"{(df['Datumsformat'] != ISO).sum()} von {n} Zeilen",
     "vereinheitlichen: ein Format, Annahme für 03/05 dokumentieren"),
    ("Negative Menge / Umsatz", "mittel", f"{len(neg)} Zeile(n), {neg['Umsatz'].sum():.2f} EUR",
     "prüfen; als Retoure kennzeichnen statt löschen"),
    ("Fehlende KundenID", "mittel", f"{df['KundenID'].isna().sum()} Zeile(n)",
     "nicht schätzen; markieren/ausschließen oder Quelle fragen"),
    ("Fehlender Name / E-Mail", "gering", f"{df['Name'].isna().sum()} / {df['E-Mail'].isna().sum()} Zeile(n)",
     "so lassen, falls nicht modellrelevant"),
    ("Leere / Trennzeichen-Zeile", "gering", f"{len(leer) + len(nur_trenner)} Zeile(n)", "löschen"),
], columns=["Problem", "Schwere", "Umfang", "Methode"])
b.tabelle(tabelle)

b.text("Vorgeschlagene Reihenfolge (Abhängigkeiten):", "**Vorgeschlagene Reihenfolge (Abhängigkeiten)**")
reihenfolge = [
    "Datei korrekt einlesen: ohne das sind alle weiteren Schritte falsch",
    "Typen und Formate angleichen (Datum, Umsatz als Zahl)",
    "Dubletten entfernen: vor jeder Aggregation, sonst wird doppelt gezählt",
    "Negative Werte klären (Retoure markieren)",
    "Fehlende Werte behandeln: zuletzt, erst wenn klar ist, was wirklich fehlt",
]
for i, schritt in enumerate(reihenfolge, 1):
    print(f"  {i}. {schritt}")
b.md += [f"{i}. {s}" for i, s in enumerate(reihenfolge, 1)] + [""]

b.text("Wirkung auf den Gesamtumsatz:", "**Wirkung auf den Gesamtumsatz**")
b.tabelle(pd.DataFrame([
    ("roh", n, f"{umsatz_roh:.2f}"),
    ("ohne Dubletten", len(kern), f"{umsatz_ohne:.2f}"),
    ("ohne Dubletten, nur positive Zeilen (ohne Retouren)", int((kern["Umsatz"] > 0).sum()), f"{ohne_retouren:.2f}"),
], columns=["Stand", "Zeilen", "Umsatz (EUR)"]))

# %%
# Bericht schreiben (Kopf mit Kennzahlen wird erst jetzt gebaut, wenn alle Werte feststehen)
kopf = [
    "## Auf einen Blick", "",
    "| Kennzahl | Wert |", "| --- | --- |",
    f"| Datenzeilen gelesen | {n} |",
    f"| Zeilen nach Dublettenentfernung | {len(kern)} |",
    f"| Zeilen mit mindestens einem Befund | {zeilen_mit_befund} von {n} |",
    f"| Umsatz roh → ohne Dubletten | {umsatz_roh:.2f} → {umsatz_ohne:.2f} EUR |",
    f"| Verschiedene Datumsformate | {df['Datumsformat'].nunique()} |",
    f"| Negative Zeilen (Retouren?) | {len(neg)} |", "",
    "> Das Skript bereinigt nichts. Es benennt Annahmen und belegt sie mit Kennzahlen.", "",
]
b.speichern(BERICHT, kopf)
print(f"\nBericht geschrieben: {BERICHT}")
