# Tag 12, Zusatz A12-2: Bias und Varianz – vier Modelle, ein Problem

Aufgabe: Vier Modellvarianten für dieselbe Aufgabe, je mit Güte auf Training und Test. Jedes Modell einordnen (Underfit, gut, Overfit), eine Maßnahme nennen und ein Modell für den Betrieb wählen.

Die Folie nennt kein Gütemaß. Ich gehe davon aus, dass **größer = besser** ist (Werte zwischen 0 und 1, etwa R² oder Trefferquote). Bei einem Fehlermaß wie MSE würde sich die Lesart umkehren, die Aussagen bleiben gleich.

> [!NOTE]
> **Ergebnis in Kürze**
>
> - **Modell 1:** leichtes **Underfit** (Training 0,71, Test 0,69). Maßnahme: mehr Komplexität.
> - **Modell 2:** **gut** (0,88 / 0,86). Maßnahme: beibehalten, nur fein abstimmen und per Cross-Validation absichern.
> - **Modell 3:** **Overfit** (0,99 / 0,72). Maßnahme: regularisieren oder vereinfachen.
> - **Modell 4:** deutliches **Underfit** (0,64 / 0,63). Maßnahme: Komplexität stark erhöhen oder bessere Merkmale.
> - **Betrieb:** **Modell 2.** Es hat die beste Testgüte (0,86) und einen kleinen Abstand (0,02).

---

## 1. Die Messwerte und was der Abstand verrät

| Modell | Train-Güte | Test-Güte | Abstand (Train − Test) |
|---:|---:|---:|---:|
| 1 | 0,71 | 0,69 | 0,02 |
| 2 | 0,88 | 0,86 | 0,02 |
| 3 | 0,99 | 0,72 | **0,27** |
| 4 | 0,64 | 0,63 | 0,01 |

Zwei Fragen genügen für die Diagnose:

| Frage | Antwort deutet auf |
|---|---|
| **Wie groß ist der Abstand Training ↔ Test?** | Großer Abstand: das Modell hat **Rauschen auswendig gelernt** (hohe Varianz, Overfit). |
| **Wie hoch sind die Werte selbst?** | Beide niedrig: das Modell ist **zu einfach** für das Muster (hoher Bias, Underfit). |

> [!NOTE]
> **Der Abstand allein reicht nicht.** Modell 1, 2 und 4 haben fast denselben Abstand (0,01 bis 0,02), und trotzdem ist nur Modell 2 gut. Erst das **Niveau** zeigt, ob ein kleiner Abstand Stärke bedeutet (Modell 2) oder nur „gleichmäßig schlecht" (Modell 4). Man braucht immer beide Informationen.

### Was bedeutet „beide niedrig"?

Das Modell erreicht schon **auf den Daten, die es kennt**, keine gute Güte. Es kann das Muster gar nicht abbilden (zum Beispiel eine Gerade durch eine Kurve). Das ist **Underfitting**, der Fehler ist **systematisch** (hoher Bias). Mehr Daten helfen dann kaum, denn das Modell ist nicht zu unruhig, sondern zu grob.

---

## 2. Einordnung und Maßnahme je Modell

| Modell | Einordnung | Begründung | Konkrete Maßnahme |
|---:|---|---|---|
| **1** | **leichtes Underfit** | Beide Werte um 0,70, kaum Abstand. Dass Modell 2 auf denselben Daten 0,86 schafft, zeigt, dass **etwa 0,17 Güte ungenutzt** bleiben. | Mehr Komplexität: Wechselwirkungen oder nichtlineare Merkmale ergänzen (z. B. Rabatt × Weihnachten), tiefere Bäume, schwächere Regularisierung, Merkmale hinzufügen. |
| **2** | **gut** | Hohe Güte, Abstand nur 0,02. Training und Test stimmen überein: das Modell hat das **Muster** gelernt, nicht das Rauschen. | Beibehalten. Feinabstimmung der Hyperparameter mit Cross-Validation (Grid Search, siehe Arbeitsauftrag 2), Stabilität über Folds prüfen. |
| **3** | **Overfit** | Training 0,99, Test nur 0,72. Das Modell kennt die Trainingsdaten fast **auswendig**. Auf neuen Daten fällt es um 0,27 ab. | **Regularisieren oder vereinfachen:** `max_depth` begrenzen oder `min_samples_leaf` erhöhen, L1/L2-Strafe (`alpha`, `C`), weniger Merkmale, Early Stopping, mehr Trainingsdaten, Random Forest statt Einzelbaum (Mittelung senkt die Varianz). |
| **4** | **deutliches Underfit** | Training 0,64, Test 0,63: **schlechteste Werte** beider Spalten, der Abstand ist hier sogar am kleinsten. Das Modell ist zu grob. | Komplexität **deutlich** erhöhen: anderes Verfahren (z. B. Boosting statt Gerade), neue aussagekräftige Merkmale (Saison, Trend). Vorher prüfen, ob die Daten das Muster überhaupt enthalten (Merkmale vorhanden? Zielwerte plausibel?). |

> [!TIP]
> **Merkregel für die Maßnahme:** Overfit (Abstand groß) → **Komplexität senken**. Underfit (beide niedrig) → **Komplexität erhöhen**. Immer nur **eine** Änderung auf einmal und danach neu messen.

### Warum nicht „mehr Daten" für alle?

| Problem | Hilft mehr Daten? |
|---|---|
| Overfit (Modell 3) | **Ja**, weil das Rauschen weniger ins Gewicht fällt, wenn das Modell mehr Beispiele sieht. |
| Underfit (Modell 1, 4) | **Kaum.** Das Modell ist zu einfach, mehr Beispiele ändern daran nichts. |

---

## 3. Wo liegt das Minimum des Testfehlers?

Ordnet man die vier Modelle nach Komplexität, ergibt sich die bekannte Kurve. Die Folie nennt die Komplexität nicht. **Annahme:** Die Reihenfolge ergibt sich aus dem Muster der Werte, also 4 (am einfachsten) → 1 → 2 → 3 (am komplexesten).

```
Güte
1,00 |                               T(0,99)
0,90 |                    T(0,88)
0,86 |                    t(0,86)  ← Optimum auf Test
0,80 |
0,72 |                               t(0,72)
0,70 |          T(0,71)
0,69 |          t(0,69)
0,64 | T(0,64)
0,63 | t(0,63)
     +-------------------------------------------→ Komplexität
        Modell 4  Modell 1  Modell 2   Modell 3
        (Underfit)(Underfit) (gut)     (Overfit)

T = Training, t = Test
```

- **Trainingsgüte steigt immer** mit der Komplexität (0,64 → 0,71 → 0,88 → 0,99). Sie sagt allein nichts über die Qualität.
- **Testgüte steigt, erreicht ihr Maximum und fällt wieder** (0,63 → 0,69 → **0,86** → 0,72).
- **Das Minimum des Testfehlers (= Maximum der Testgüte) liegt bei Modell 2.** Links davon ist das Modell zu einfach (Bias), rechts davon zu komplex (Varianz).

> [!IMPORTANT]
> **Nie nach der Trainingsgüte wählen.** Modell 3 hat mit 0,99 die beste Trainingsgüte und ist trotzdem eine schlechte Wahl. Die Trainingsgüte misst nur, wie gut ein Modell die Daten kennt, die es schon gesehen hat.

### Bias und Varianz in einem Satz

| | Bias | Varianz |
|---|---|---|
| Bedeutung | Systematischer Fehler durch ein zu einfaches Modell | Empfindlichkeit gegenüber den Trainingsdaten |
| Zeichen | Training **und** Test niedrig | Training hoch, Test deutlich niedriger |
| Modelle hier | 1 und 4 | 3 |

---

## 4. Auswahl für den Betrieb

> [!NOTE]
> **Wahl: Modell 2.**

| Kriterium | Modell 1 | **Modell 2** | Modell 3 | Modell 4 |
|---|---|---|---|---|
| Testgüte (zählt für neue Daten) | 0,69 | **0,86** | 0,72 | 0,63 |
| Abstand Train−Test (Verlässlichkeit) | 0,02 | **0,02** | 0,27 | 0,01 |
| Risiko im Betrieb | verschenktes Potenzial | **gering** | Güte fällt auf neuen Daten stark | verschenktes Potenzial |

**Begründung:**
1. **Beste Testgüte** (0,86) mit deutlichem Vorsprung: 0,14 vor dem Zweitplatzierten (Modell 3 mit 0,72).
2. **Kleiner Abstand** von 0,02: Die Güte, die wir im Test sehen, ist wahrscheinlich auch auf neuen Daten zu erwarten. Bei Modell 3 wäre die 0,99 aus dem Training eine Täuschung.
3. **Kein Modell mit hoher Varianz.** Modell 3 reagiert empfindlich auf neue Daten und würde im Betrieb schwanken.

**Vorbehalte, die ich nicht prüfen kann:**
- Wenn die vier Modelle **anhand der Testdaten verglichen und ausgewählt** wurden, ist der Testwert 0,86 leicht optimistisch (siehe Nested CV im Cheatsheet). Sauber wäre eine Auswahl mit Cross-Validation und ein einmaliger Test für das gewählte Modell.
- Die Folie nennt **keine Kosten** (Rechenzeit, Erklärbarkeit). Bei gleicher Güte würde man das einfachere Modell vorziehen.
- Ein einzelner Testwert hat eine **Streuung** (siehe Arbeitsauftrag 1). Ob 0,86 gegenüber 0,72 sicher besser ist, würde man per CV bestätigen. Der Abstand von 0,14 ist allerdings groß.

---

## 5. Beispiel mit echten Daten (Bohnenwerk)

Zur Veranschaulichung habe ich einen Entscheidungsbaum mit steigender Tiefe auf die Bohnenwerk-Daten gesetzt (R², zufällige Aufteilung 70/30 mit `random_state=42`, 109 Trainings- und 47 Testwochen):

| `max_depth` | Training | Test |
|---:|---:|---:|
| 1 | 0,23 | 0,32 |
| 2 | 0,50 | 0,60 |
| 3 | 0,69 | 0,50 |
| 4 | 0,84 | 0,55 |
| 5 | 0,92 | 0,61 |
| 6 | 0,96 | 0,53 |
| 8 | 0,99 | 0,53 |
| 12 | 1,00 | 0,47 |
| unbegrenzt | 1,00 | 0,46 |

- **Training** steigt bis 1,00 (der Baum lernt die 109 Wochen auswendig).
- **Test** bleibt bei etwa 0,5 bis 0,6 und fällt am Ende auf 0,46: Der Abstand (Training − Test) wächst von leicht negativ bei Tiefe 1 und 2 auf **über 0,5** bei Tiefe 12. Das ist das Bild von Modell 3.
- Tiefe 1 ist deutlich zu einfach (0,23 / 0,32), das Bild von Modell 4.
- Die Testkurve ist **nicht glatt** (Tiefe 3: 0,50, Tiefe 5: 0,61). Mit nur 47 Testwochen schwankt der Testwert stark, ein einzelner Split zeigt das Optimum nur ungefähr. Das ist auch ein Grund, es per Cross-Validation zu bestimmen.

> [!WARNING]
> **Die Schwankung der Testkurve ist selbst eine Lehre:** Wer das Optimum an einem kleinen Testset abliest, wählt zum Teil den Zufall. Dafür gibt es `validation_curve` mit Cross-Validation (siehe `05_Notebookpreise_Modell`).

---

## Kernaussagen

> [!TIP]
> - **Abstand und Niveau gemeinsam lesen.** Großer Abstand = Overfit (Varianz). Beide niedrig = Underfit (Bias). Kleiner Abstand bei hohem Niveau = gut.
> - **Die Trainingsgüte steigt immer mit der Komplexität, die Testgüte hat ein Maximum.** Gewählt wird das Maximum der Testgüte, nicht der Trainingsgüte.
> - **Die Maßnahme folgt der Diagnose:** Overfit → regularisieren, vereinfachen, mehr Daten. Underfit → mehr Komplexität, bessere Merkmale.
> - **Ein Testwert ist ein Schätzwert.** Zur Absicherung Cross-Validation, den Test nur einmal am Ende.

## Abweichungen und Annahmen

- Die Folie nennt **kein Gütemaß**. Angenommen: Werte zwischen 0 und 1, höher ist besser.
- Die **Reihenfolge nach Komplexität** (4, 1, 2, 3) ist aus dem Muster der Werte erschlossen, die Folie nennt die Modelle nicht.
- Die Einordnung von Modell 1 als „leichtes Underfit" ist eine Einschätzung im Vergleich zu Modell 2. Allein aus 0,71 / 0,69 ließe sich das nicht sagen, denn bei einer schwierigen Aufgabe könnten 0,70 gut sein. Dass 0,86 mit einem anderen Modell erreichbar ist, macht den Unterschied.
- Das Bohnenwerk-Beispiel (Abschnitt 5) ist nicht Teil der Aufgabe, nur eine Veranschaulichung. Die Zahlen stammen aus einem einmaligen Lauf mit `random_state=42`.
- Gerendert habe ich die Hinweisboxen (`> [!NOTE]` usw.) nicht. GitHub zeigt sie in Markdown-Dateien an. In anderen Programmen erscheinen sie als einfache Zitate.
