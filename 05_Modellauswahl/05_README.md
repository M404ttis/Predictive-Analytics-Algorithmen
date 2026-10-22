# Notebook-Preise: Das Jupyter-Notebook im Browser starten

Schritt-für-Schritt-Anleitung für Einsteiger, für **Mac und Windows**.

**Was du am Ende hast:** Ein Notebook im Browser, das 500 Notebook-Preise einliest, Diagramme zeichnet, fünf Modelle vergleicht und einen Preis vorhersagt.

## Was du brauchst

| # | Was | Wofür |
| --- | --- | --- |
| 1 | **Python** | ein Programm, das den Code ausführt |
| 2 | `05_Notebookpreise_Modell.ipynb` | das Notebook |
| 3 | `05_Notebookpreise_Arbeitsauftrag.csv` | die 500 Notebooks (Daten) |

> **Hinweis:** Das Notebook ist die `.ipynb`-Datei. Die gleichnamige `.py`-Datei enthält denselben Inhalt als reinen Text. Du brauchst nur eine der beiden, hier nutzen wir die `.ipynb`.

**So funktionieren die Befehle:** Du tippst sie in ein **Terminal**, also ein Fenster, in das man Text-Befehle schreibt und mit der Eingabetaste (`Enter`) ausführt. Jeden Befehl in einem grauen Kasten kannst du mit dem Kopier-Symbol rechts oben im Kasten kopieren und im Terminal einfügen. Zeilen, die mit `#` beginnen, sind nur Erklärungen und müssen nicht mitkopiert werden.

---

## Teil A: Einmalige Einrichtung

### Schritt 1: Python installieren (falls noch nicht geschehen)

1. Öffne <https://www.python.org/downloads/> und lade die aktuelle Version herunter (Python 3.10 oder neuer ist in Ordnung).
2. Starte das Installationsprogramm.
   - **Windows:** Setze im ersten Fenster **unbedingt** den Haken bei **"Add python.exe to PATH"** (unten im Fenster), dann auf "Install Now" klicken.
   - **Mac:** Einfach den Anweisungen folgen.
3. Prüfen, ob es geklappt hat (das geht erst, wenn du ein Terminal offen hast, siehe Schritt 3):

   **Mac:**

   ```bash
   python3 --version
   ```

   **Windows:**

   ```powershell
   python --version
   ```

   Es sollte etwas wie `Python 3.12.4` erscheinen.

### Schritt 2: Ordner anlegen und die zwei Dateien hineinlegen

1. Lege irgendwo einen neuen Ordner an, zum Beispiel auf dem Schreibtisch, und nenne ihn `notebook-preise` (am besten ohne Leerzeichen und Umlaute im Namen).
2. Kopiere **beide** Dateien in **denselben** Ordner:
   - `05_Notebookpreise_Modell.ipynb`
   - `05_Notebookpreise_Arbeitsauftrag.csv`
3. **Wichtig:** Das Notebook sucht die CSV im selben Ordner. Liegen die Dateien an verschiedenen Orten, kommt der Fehler `FileNotFoundError`.

### Schritt 3: Das Terminal öffnen

- **Mac:** `Cmd` + `Leertaste` drücken, `Terminal` tippen, `Enter` drücken.
- **Windows:** Auf Start klicken, `PowerShell` tippen, `Enter` drücken.

### Schritt 4: Im Terminal in deinen Ordner wechseln

Das Terminal muss "in" dem Ordner sein, in dem deine Dateien liegen. Der Befehl dafür ist `cd` (change directory).

**Mac** (Ordner liegt auf dem Schreibtisch):

```bash
cd ~/Desktop/notebook-preise
```

> Tipp für den Mac: Tippe `cd` und ein Leerzeichen, ziehe dann den Ordner mit der Maus ins Terminal-Fenster und drücke `Enter`.

**Windows** (Ordner liegt auf dem Schreibtisch):

```powershell
cd $HOME\Desktop\notebook-preise
```

Liegt dein Schreibtisch in OneDrive:

```powershell
cd $HOME\OneDrive\Desktop\notebook-preise
```

**Prüfen**, ob du richtig bist (du solltest deine zwei Dateien sehen):

Mac:

```bash
ls
```

Windows:

```powershell
dir
```

### Schritt 5: Eine "virtuelle Umgebung" (`.venv`) anlegen

Eine virtuelle Umgebung ist ein eigener, sauberer Werkzeugkasten nur für dieses Projekt. So kommen die Pakete nicht mit anderen Programmen in Konflikt. Das machst du nur **einmal**.

**Mac:**

```bash
python3 -m venv .venv
```

**Windows:**

```powershell
python -m venv .venv
```

Danach liegt im Ordner ein neuer Unterordner namens `.venv`. Auf dem Mac ist er unsichtbar, weil er mit einem Punkt beginnt. Das ist normal.

### Schritt 6: Die Umgebung einschalten (aktivieren)

**Mac:**

```bash
source .venv/bin/activate
```

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

Du erkennst es daran, dass ganz links im Terminal jetzt `(.venv)` steht. Dann ist alles richtig.

**Windows, falls eine rote Fehlermeldung** zu "Ausführungsrichtlinie" bzw. "running scripts is disabled" kommt, führe einmal aus:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Bestätige mit `J` oder `Y` und wiederhole dann den Aktivierungsbefehl von oben.

### Schritt 7: Die Pakete installieren (einmalig, dauert einige Minuten)

```bash
pip install pandas scikit-learn matplotlib seaborn jupyterlab
```

Das lädt die Programmbausteine aus dem Internet:

| Paket | Wofür |
| --- | --- |
| `pandas` | Tabellen einlesen und bearbeiten |
| `scikit-learn` | die Vorhersage-Modelle |
| `matplotlib`, `seaborn` | Diagramme |
| `jupyterlab` | die Oberfläche im Browser |

Es erscheint viel Text. Warte, bis du wieder eine Eingabezeile siehst. Fertig ist es, wenn zuletzt `Successfully installed ...` steht.

---

## Teil B: Das Notebook starten

### Schritt 8: Jupyter Lab starten

Stelle sicher, dass du im richtigen Ordner bist (Schritt 4) und `(.venv)` links im Terminal steht (Schritt 6). Dann:

```bash
jupyter lab
```

Nach einigen Sekunden öffnet sich dein Browser mit der Jupyter-Oberfläche. Öffnet er sich nicht, kopiere die Adresse aus dem Terminal, die mit `http://localhost:8888/...` beginnt, in die Adresszeile des Browsers.

> **Wichtig:** Das Terminal-Fenster muss offen bleiben, solange du arbeitest. Schließt du es, funktioniert das Notebook nicht mehr.

### Schritt 9: Das Notebook öffnen und ausführen

1. Links im Browser siehst du eine Dateiliste. Doppelklick auf `05_Notebookpreise_Modell.ipynb`.
2. Fragt Jupyter nach einem "Kernel": wähle **Python 3 (ipykernel)**.
3. Das Notebook besteht aus "Zellen" (Kästen mit Text oder Code). Führe alles auf einmal aus über das Menü **Run → Run All Cells**. Oder einzeln: Zelle anklicken und `Umschalt` + `Enter` drücken (führt die Zelle aus und springt zur nächsten).
4. Warte, bis links neben den Zellen kein `[*]` mehr steht, sondern Zahlen wie `[1]`, `[2]` ... Dann siehst du Tabellen, Diagramme und die Auswertung. Die **türkisen Kästen** sind die wichtigsten Erkenntnisse.
5. Du kannst im Code etwas ändern und die Zelle neu ausführen. Kaputt gehen kann nichts, die Originaldatei hast du ja noch.

### Schritt 10: Beenden

1. Speichern im Browser: `Cmd` + `S` (Mac) bzw. `Strg` + `S` (Windows).
2. Browser-Tab schließen.
3. Im Terminal-Fenster `Ctrl` + `C` drücken (auch auf dem Mac `Ctrl`, nicht `Cmd`), bei der Rückfrage `y` eingeben und `Enter` drücken.
4. Umgebung verlassen:

   ```bash
   deactivate
   ```

---

## Beim nächsten Mal (nur noch 4 Schritte)

Die Schritte 1, 2, 5 und 7 entfallen.

1. Terminal öffnen (Schritt 3).
2. In den Ordner wechseln, zum Beispiel:

   ```bash
   cd ~/Desktop/notebook-preise
   ```

   Windows:

   ```powershell
   cd $HOME\Desktop\notebook-preise
   ```

3. Umgebung einschalten:

   Mac:

   ```bash
   source .venv/bin/activate
   ```

   Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Jupyter Lab starten:

   ```bash
   jupyter lab
   ```

---

## Häufige Probleme

**`python: command not found` oder "python wird nicht erkannt"**
- Mac: `python3` statt `python` benutzen.
- Windows: Python neu installieren und den Haken bei "Add python.exe to PATH" setzen. Terminal danach neu öffnen.

**Links steht kein `(.venv)`**
- Schritt 6 (Aktivieren) wiederholen. Ohne aktive Umgebung findet das Terminal die installierten Pakete nicht.

**`jupyter: command not found` oder "jupyter wird nicht erkannt"**
- Die Umgebung ist nicht aktiv (Schritt 6) oder Schritt 7 wurde nicht bis zum Ende ausgeführt. Beides wiederholen.

**`ModuleNotFoundError: No module named 'pandas'` (oder `sklearn`, `seaborn` ...)**
- Das Notebook läuft mit dem falschen Kernel. Starte `jupyter lab` aus dem Terminal mit `(.venv)` (Schritt 8). Dann oben rechts im Notebook auf den Kernel-Namen klicken und "Python 3 (ipykernel)" wählen.
- Alternativ die Pakete nochmal installieren:

  ```bash
  pip install pandas scikit-learn matplotlib seaborn
  ```

**`FileNotFoundError: ... 05_Notebookpreise_Arbeitsauftrag.csv`**
- CSV und Notebook liegen nicht im selben Ordner, oder `jupyter lab` wurde in einem anderen Ordner gestartet. Beide Dateien in einen Ordner legen, in diesen Ordner wechseln (Schritt 4), `jupyter lab` neu starten.

**Die Zellen laufen nicht oder bleiben bei `[*]` hängen**
- Menü **Kernel → Restart Kernel and Run All Cells**.

**Der Browser öffnet sich nicht**
- Die Adresse `http://localhost:8888/lab?token=...` aus dem Terminal kopieren und in den Browser einfügen.

**Diagramme fehlen oder sehen seltsam aus**
- Menü **Run → Run All Cells**. Erst nach dem Ausführen erscheinen die Diagramme.

---

## Kleines Glossar

| Begriff | Bedeutung |
| --- | --- |
| **Terminal** | Fenster zum Eintippen von Befehlen |
| **Ordner / `cd`** | Verzeichnis. `cd` wechselt in einen Ordner |
| **`.venv`** | eigener Werkzeugkasten für ein Projekt (virtuelle Umgebung) |
| **`pip`** | Programm, das Python-Pakete installiert |
| **Paket** | fertiger Programmbaustein (z. B. `pandas`) |
| **Jupyter Lab** | Oberfläche im Browser, in der man Code Stück für Stück ausführt und die Ergebnisse darunter sieht |
| **Notebook** | eine `.ipynb`-Datei: Text, Code und Diagramme in einem |
| **Zelle** | ein Kasten im Notebook (Text oder Code) |
| **Kernel** | das "Rechenwerk" im Hintergrund, das den Code ausführt |

---

*Hinweis: Das Notebook selbst wurde unter macOS in einer bestehenden Umgebung getestet. Die Einrichtung von null (Schritte 1 bis 7) und die Windows-Schritte folgen den Standard-Befehlen von Python und PowerShell, wurden aber nicht auf einem frischen Rechner ausprobiert.*
