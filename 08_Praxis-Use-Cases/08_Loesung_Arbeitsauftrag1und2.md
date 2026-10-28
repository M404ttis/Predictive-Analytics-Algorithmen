# Tag 8 · Praxis-Use-Cases: Lösungen Arbeitsauftrag 1 und 2

**Arbeitsauftrag 1 (Fehlerkosten, Metrik & Schwelle):** Für die vier Felder Demand Forecasting, Predictive Maintenance, Marketing (Churn) und Finance (Fraud) entscheiden wir: Welcher Fehler ist teurer, welche Leitmetrik passt, ist die Schwelle eher hoch oder niedrig? Jede Wahl in einem Satz begründet.

**Arbeitsauftrag 2 (Anti-Muster):** Vier Use-Case-Vorschläge klingen real, haben aber einen versteckten Konstruktionsfehler. Wir stellen **Diagnose** und **Therapie**.

> **Annahmen:** Gegeben sind nur die Zahlen der Folien. Alle weiteren Zahlen (Prüfkosten 5 €, Modellgüte im Beispiel, Kosten pro Fehler im Demand-Feld) sind **Annahmen** und als solche gekennzeichnet. Sie lassen sich austauschen, die Logik bleibt gleich.

---

## Das Ergebnis in Kürze

| Feld | Teurerer Fehler | Leitmetrik | Schwelle |
| --- | --- | --- | --- |
| Demand Forecasting | beide, aber verschieden: Unterprognose (leere Regale) vs. Überprognose (Entsorgung) | **MAE** (plus Bias), RMSE bei teuren Ausreißern | keine Klassenschwelle, stattdessen **Quantil** der Prognose |
| Predictive Maintenance | **FN** (ungeplanter Ausfall) | **Recall**, Precision als Nebenbedingung | **niedrig** |
| Marketing (Churn) | **FN** (verlorener Kunde), aber nur, wenn die Aktion wirkt | **Wert in €**, Recall und Precision zur Kontrolle | **mittel**, rechnerisch p > K / (q · W) |
| Finance (Fraud) | **FN** (400 € je Betrug) | **Recall und Precision**, nie Accuracy | **niedrig**, rechnerisch p > K / 400 € |

| Fall | Konstruktionsfehler (Diagnose) | Rettung (Therapie) |
| --- | --- | --- |
| **A** Fitnessstudio | Trainingsdaten enthalten **keine Kündiger** (Löschung nach Vertragsende) | Historie aufbewahren, Zielgröße mit Stichtag definieren, Start verschieben |
| **B** Zahlungsdienstleister | **falsche Metrik**: 99 % Accuracy ist bei 1 % Betrug wertlos | Recall und Precision, kostenbasierte Schwelle, Mensch bleibt im Prozess |
| **C** Lebensmittelhandel | **Saison und Aktionen fehlen**, Pilot in der falschen Jahreszeit | Saison- und Aktionsmerkmale, Pilot über eine Saison, Vergleich mit der Baseline |
| **D** Chemiewerk | **kein Betrieb**: keine Überwachung, kein Verantwortlicher, kein Budget | Monitoring, Nachtraining auf neue Pumpen, Verantwortlichkeit, Betriebsbudget |

---

# Arbeitsauftrag 1: Fehlerkosten, Metrik und Schwelle

## 0. Handwerkszeug

**Zwei Fehlerarten** (Folie 2):

| | Fehlalarm (FP) | Übersehen (FN) |
| --- | --- | --- |
| Was passiert | Modell schlägt an, obwohl nichts ist | Modell übersieht den echten Fall |
| Kosten | Aufwand, Nerven, Vertrauen | der Schaden bleibt unentdeckt |

**Lesehilfe (aus Tag 6):** Das zweite Wort sagt, was das Modell behauptet hat ("Positive" = Alarm). Das erste Wort sagt, ob das Modell damit richtig lag. FP = falscher Alarm, FN = durchs Netz gerutscht.

**Metriken:**

```
Recall    = TP / (TP + FN)     "Wie viele der echten Fälle finden wir?"
Precision = TP / (TP + FP)     "Wie viele unserer Alarme sind echt?"
MAE       = (1/n) · Σ |yᵢ − ŷᵢ|    "Typischer Fehler in Einheiten"
RMSE      = √( (1/n) · Σ (yᵢ − ŷᵢ)² )    "wie MAE, aber große Fehler zählen stärker"
```

**Die Schwelle (Entscheidungsregel):** Ein Modell liefert einen Score p (Wahrscheinlichkeit für "Treffer"). Wir handeln, wenn p über der Schwelle liegt. Die Schwelle ist **keine Naturkonstante**, sie folgt aus den Kosten:

```
Handeln lohnt sich, wenn   p · Nutzen der Handlung  >  Kosten der Handlung K

Schwelle   p*  =  K / Nutzen
```

- **Niedrige Schwelle:** das Modell schlägt oft an. **Weniger FN, mehr FP.** Recall steigt, Precision sinkt.
- **Hohe Schwelle:** das Modell schlägt selten an. **Weniger FP, mehr FN.** Precision steigt, Recall sinkt.

Das beantwortet den Denkanstoß "Senkt eine niedrigere Schwelle eher FN oder FP?": Eine niedrigere Schwelle senkt **FN** und erhöht FP.

---

## 1. Demand Forecasting (Zahl: MAE oder RMSE?)

Beispiel Bäckerei Krume aus den Folien: Absatz je Artikel, Filiale und Tag.

| Frage | Antwort |
| --- | --- |
| **Welcher Fehler ist teurer?** | Beide Fehler kosten, aber verschieden. **Unterprognose:** ausverkauft, Umsatz und Kundenvertrauen gehen verloren (bei Krume: Samstag ab 15 Uhr). **Überprognose:** Ware wird entsorgt (11 %). Bei Frischware ist die Überprognose pro Stück meist günstiger (Einkaufspreis), die Unterprognose kostet den **entgangenen Gewinn**. |
| **Leitmetrik** | **MAE**, begleitet vom **Bias (ME)**. |
| **Schwelle** | Es gibt keine Ja/Nein-Schwelle. Das Gegenstück ist das **Quantil**: Man bestellt nicht auf den Mittelwert, sondern auf das Quantil, das zum Kostenverhältnis passt. |

**Begründung in einem Satz:** Die Bestellung ist eine Zahl in Stück, deren **durchschnittlicher** Fehler in verständlichen Einheiten zählt, deshalb MAE; RMSE wäre nur dann besser, wenn einzelne große Ausreißer (etwa ein ausverkaufter Samstag vor einem Feiertag) überproportional teuer wären.

**Zur Frage "zählt der Schnitt oder der Ausreißer?":**

| Situation | Metrik | Warum |
| --- | --- | --- |
| Alltagsware, viele kleine Bestellungen, Fehler kosten linear | **MAE** | Jede Abweichung um ein Stück kostet gleich viel, der Schnitt zählt. |
| Ein großer Fehler ist viel schlimmer als mehrere kleine (Großaktion, leere Regale bei Spitzenbedarf) | **RMSE** | Quadrierte Fehler bestrafen Ausreißer. Der Tag-7-Vergleich: Modell B hatte MAE 3,80, aber RMSE 6,77, weil zwei große Fehler 98 % der Quadratsumme ausmachten. |
| Mehrere Artikel mit sehr verschiedener Größe vergleichen | **MAPE** oder **WAPE** | Relative Fehler sind größenunabhängig. Vorsicht bei MAPE und Werten nahe null. |

**MAE, MedAE oder RMSE: Welche Metrik wann?** RMSE ist nicht "immer besser". Jede Metrik unterstellt eine andere Kostenform und eine andere Haltung zu Ausreißern:

| Metrik | Unterstellte Kostenform | Reaktion auf Ausreißer | Antwortet auf die Frage |
| --- | --- | --- | --- |
| **MAE** | linear: 20 Stück daneben kostet doppelt so viel wie 10 | jeder Fehler zählt, proportional zur Größe | Was kostet der Fehler im Schnitt, schlechte Tage eingerechnet? |
| **MedAE** | (keine Kostenform, reine Lagemessung) | Ausreißer werden ignoriert | Wie weit liegt das Modell an einem **typischen** Tag daneben? |
| **RMSE** | überproportional: 20 Stück daneben kostet viermal so viel wie 10 | große Fehler dominieren | Wie schlimm sind die großen Fehlgriffe? |

Beispiel mit acht Tagesfehlern (in Stück), ein Tag ist ein Ausreißer:

```
|Fehler| = 2, 3, 2, 4, 3, 2, 3, 60

MAE   = 79 / 8                              ≈ 9,9
MedAE = sortiert 2, 2, 2, 3, 3, 3, 4, 60  → (3 + 3) / 2 = 3
```

An sieben von acht Tagen liegt das Modell nur 2 bis 4 Stück daneben. Der eine Ausreißer (60) zieht den MAE auf 9,9, der MedAE bleibt bei 3. Beide Werte stimmen, sie beantworten verschiedene Fragen.

- **MAE nehmen**, wenn die schlechten Tage echtes Geld kosten (jedes fehlende und jedes entsorgte Brötchen schlägt in die Bilanz durch) und die Kosten ungefähr linear wachsen. MAE × n ist dann die Gesamtabweichung. Das ist bei der Bäckerei der Fall.
- **MedAE nehmen**, wenn Ausreißer Rauschen sind, das kein Modell vorhersagen kann (Kassenfehler, Streik, Eingabefehler), oder wenn man die Qualität im Normalbetrieb beurteilen will. Wenige defekte Datensätze entscheiden dann nicht über die Rangfolge der Modelle.
- **RMSE nehmen**, wenn ein großer Fehler viel schlimmer ist als mehrere kleine (Großaktion, leere Regale bei Spitzenbedarf, nicht mehr verkaufbare Übermenge) oder wenn man seltene große Fehlgriffe aufspüren will.

**Am besten nebeneinander lesen:**

| Befund | Bedeutung |
| --- | --- |
| MAE ≈ MedAE und RMSE/MAE nahe 1 | Fehler sind gleichmäßig, keine Ausreißer |
| MAE deutlich größer als MedAE | Der typische Tag ist gut, einzelne Tage sind sehr schlecht. Diese Tage ansehen: Datenfehler (aussortieren) oder echte teure Ausreißer (Modell verbessern)? |
| RMSE viel größer als MAE | Wenige große Fehler dominieren (Tag-7-Beispiel Modell B: MAE 3,80, RMSE 6,77) |

**Vorsicht beim MedAE:** Er kann ein Modell gut aussehen lassen, das an wenigen wichtigen Tagen (Weihnachten, Hauptaktion) stark versagt. Dann ist der "Ausreißer" genau der Fall, den man treffen muss, und MAE oder RMSE sind die ehrlichere Metrik.

**Für die Bäckerei:** MAE als Leitmetrik, **Bias (ME)** als Richtungsanzeige, MedAE als Gegenprobe für die Qualität im Normalbetrieb, RMSE als Warnlampe für einzelne große Fehlgriffe. Keine dieser Metriken erfasst, dass zu wenig und zu viel bestellen unterschiedlich viel kostet. Das leistet erst das Quantil.

**Warum zusätzlich der Bias (ME)?** MAE, MedAE und RMSE nehmen den Betrag oder das Quadrat des Fehlers und verlieren dabei das **Vorzeichen**. Sie sagen, *wie weit* das Modell danebenliegt, aber nicht *in welche Richtung*. Bei der Bäckerei ist die Richtung aber der Kern des Problems: zu wenig bestellt heißt ausverkauft (entgangener Gewinn), zu viel bestellt heißt Entsorgung.

```
ME (Bias) = (1/n) · Σ (yᵢ − ŷᵢ)       mit yᵢ = Ist, ŷᵢ = Vorhersage

ME > 0   Vorhersage im Schnitt zu niedrig  →  Unterprognose, Regale leer
ME < 0   Vorhersage im Schnitt zu hoch     →  Überprognose, Entsorgung
ME ≈ 0   keine feste Schlagseite
```

Beispiel mit fünf Tagen, an denen jeweils 100 Brötchen verkauft werden (Ist = 100). **Zwei Prognosen mit gleichem MAE:**

| Tag | Ist | Prognose A | Fehler A | Prognose B | Fehler B |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 100 | 90 | +10 | 92 | +8 |
| 2 | 100 | 110 | −10 | 92 | +8 |
| 3 | 100 | 90 | +10 | 92 | +8 |
| 4 | 100 | 110 | −10 | 92 | +8 |
| 5 | 100 | 100 | 0 | 92 | +8 |
| | | **MAE** | **(10 + 10 + 10 + 10 + 0) / 5 = 40 / 5 = 8** | **MAE** | **(8 + 8 + 8 + 8 + 8) / 5 = 40 / 5 = 8** |
| | | **ME** | **(10 − 10 + 10 − 10 + 0) / 5 = 0 / 5 = 0** | **ME** | **(8 + 8 + 8 + 8 + 8) / 5 = 40 / 5 = +8** |

*Beim MAE zählen die Beträge der Fehler (Vorzeichen weg), beim ME die Fehler mit Vorzeichen. Deshalb heben sich bei A die +10 und −10 im ME auf (Summe 0), im MAE aber nicht (Summe 40).*

Beide Prognosen haben denselben MAE von 8, aber sie sind grundverschieden:

- **A** liegt mal zu hoch, mal zu niedrig. Im Schnitt gleicht sich das aus (ME = 0). Das ist ein "unruhiges" Modell ohne Schlagseite.
- **B** liegt **jeden Tag** um 8 zu niedrig (ME = +8). Die Filiale ist täglich ausverkauft, obwohl der MAE "nur 8" meldet. Der MAE zeigt das Problem nicht, der Bias schon.

Der Bias ist außerdem der **direkte Hinweis, wie man korrigiert**: ME = +8 bedeutet, dass man die Bestellung im Schnitt um 8 anheben muss. Ein Modell mit ME ≠ 0 ist systematisch verschoben und lässt sich oft mit einfachen Mitteln verbessern.

**Zwei Arten von Fehler:** Der Bias (ME) erfasst nur die erste Art. Die zweite Art, die Streuung, zeigt sich im MAE, nicht im ME.

| | Systematischer Fehler (Bias) | Streuung (Zufallsfehler, "unruhiges" Modell) |
| --- | --- | --- |
| Beispiel | Prognose B: jeden Tag 8 zu niedrig | Prognose A: mal +10, mal −10 |
| Erkennbar an | ME ≠ 0 | ME ≈ 0, aber MAE > 0 |
| Fehler hat ein Muster? | Ja, immer dieselbe Richtung | Nein, aus der Richtung nicht ablesbar |
| Korrektur | oft einfach: Konstante addieren (B + 8 = 100, alle Fehler 0) | schwierig: bessere Merkmale oder ein besseres Modell (Verschieben hilft nicht, A + 8 ergibt +18 und −2) |

Ein konstanter Zuschlag behandelt nur das Symptom. Stammt der Bias aus den Daten (zum Beispiel ausverkaufte Tage, an denen der Absatz den Bedarf unterschätzt) oder ändert er sich je nach Wochentag, genügt die einfache Korrektur nicht. Dann hilft ein ME je Wochentag oder Artikelgruppe, und die Ursache gehört behoben.

**Grenzen des Bias:** Er allein ist kein Gütemaß. Prognose A hat ME = 0, ist aber nicht fehlerfrei, denn positive und negative Fehler heben sich auf. Deshalb gilt immer das Paar: **MAE sagt, wie groß der Fehler ist, ME sagt, in welche Richtung er zeigt.**

**Die "Schwelle" beim Forecast, das Quantil.** Kostet ein fehlendes Stück `C_unter` und ein überschüssiges `C_über`, bestellt man auf das Quantil

```
τ = C_unter / (C_unter + C_über)
```

Beispiel mit **angenommenen** Kosten: entgangener Gewinn 1,20 € pro fehlendem Brötchen, Entsorgungsverlust 0,30 €. Dann ist τ = 1,20 / (1,20 + 0,30) = **0,8**. Man bestellt auf das 80-%-Quantil, also etwas **über** dem erwarteten Absatz. Das ist die "hohe Bestellung" als Gegenstück zur niedrigen Alarmschwelle.

---

## 2. Predictive Maintenance (Ausfall ja/nein)

Beispiel Stadtwerke Elbtal: Pumpe fällt in den nächsten 14 Tagen aus, ja oder nein.

| Frage | Antwort |
| --- | --- |
| **Welcher Fehler ist teurer?** | **FN.** Eine übersehene Ausfallpumpe bedeutet **ungeplanten Stillstand**, Notreparatur und im Wasserwerk unter Umständen Versorgungsausfall. Ein Fehlalarm kostet dagegen nur ein vorgezogenes Ersatzteil und einen gebuchten Wartungstermin. |
| **Leitmetrik** | **Recall** (Trefferquote bei Ausfällen). **Precision** als Nebenbedingung, damit das Instandhaltungsteam nicht in Alarmen untergeht. |
| **Schwelle** | **Niedrig.** Lieber einmal zu viel prüfen als einmal zu wenig. |

**Begründung in einem Satz:** Ein verpasster Ausfall ist viel teurer als eine unnötige Prüfung, deshalb zählt der Recall und die Schwelle liegt niedrig, solange die Fehlalarmquote das Team nicht überlastet.

**Grenze:** Wird die Schwelle zu niedrig, kommt die "Alarmmüdigkeit" (viele Fehlalarme, das Team ignoriert Warnungen). Die Untergrenze ergibt sich aus der Prüfkapazität: Wie viele Alarme pro Woche kann die Instandhaltung abarbeiten?

---

## 3. Marketing / Churn (Kündigung ja/nein)

| Frage | Antwort |
| --- | --- |
| **Welcher Fehler ist teurer?** | Es kommt darauf an. Der **FN** (verlorener Kunde) kostet den Kundenwert W. Der **FP** (Halteangebot an einen Kunden, der ohnehin bleibt) kostet die Aktionskosten K und gegebenenfalls einen verschenkten Rabatt. Meist ist der FN teurer, aber **nur dann, wenn die Aktion überhaupt wirkt**. |
| **Leitmetrik** | **Wert in €** (Nettonutzen der Kampagne); **Recall und Precision** als Kontrolle. |
| **Schwelle** | **Mittel.** Rechnerisch: `p > K / (q · W)`. |

**Begründung in einem Satz:** Eine Aktion lohnt sich nur, wenn die erwartete gerettete Marge (p · q · W) die Kosten K übersteigt; deshalb ist der Euro-Wert die ehrliche Metrik und die Schwelle ergibt sich aus der Rechnung, nicht aus einem Bauchgefühl.

Mit den Zahlen aus Tag 7 (VitalPoint Fitness): K = 40 €, Erfolgsquote q = 25 %, Kundenwert W = 468 €:

```
p* = K / (q · W) = 40 € / (0,25 · 468 €) = 40 € / 117 € ≈ 34 %
```

Die Schwelle liegt also bei etwa 34 %. Das ist **nicht niedrig**: Wirkt die Aktion nur bei jedem vierten Kunden, ist jede Ansprache an einen Kunden mit einer Kündigungswahrscheinlichkeit unter 34 % ein Verlustgeschäft. Ist das Halteangebot dagegen fast gratis (K klein) oder sehr wirksam (q hoch), sinkt die Schwelle.

**Hinweis zum Fehlerbegriff:** Bei Churn ist "Positive" = "kündigt". Ein FP ist hier ein "falsch als Kündiger markierter Bleiber" (Details siehe Tag 6).

---

## 4. Finance / Fraud (seltener Treffer ja/nein)

Beispiel aus den Folien: 50 echte Betrugsfälle, 47 erkannt, 3 übersehen, dazu 12 Fehlalarme.

| Frage | Antwort |
| --- | --- |
| **Welcher Fehler ist teurer?** | **FN.** Ein unentdeckter Betrug kostet im Schnitt **400 €**. Ein Fehlalarm kostet eine kurze Prüfung (angenommen 5 €) und etwas Kundenärger. |
| **Leitmetrik** | **Recall** und **Precision**. **Nie die Accuracy**, weil Betrug selten ist. |
| **Schwelle** | **Niedrig.** Rechnerisch: `p > K / 400 €`. Mit K = 5 € ergibt sich 5 € / 400 € = **1,25 %**. |

**Begründung in einem Satz:** Ein übersehener Betrug kostet 400 €, ein Fehlalarm nur wenige Euro, deshalb wird die Schwelle niedrig gesetzt und der Recall überwacht, die Accuracy ist bei seltenen Treffern wertlos.

**Die Zahlen der Folie nachgerechnet:**

```
Recall    = 47 / (47 + 3)  = 47 / 50 = 94 %
Precision = 47 / (47 + 12) = 47 / 59 ≈ 79,7 %
```

Der Recall von 94 % klingt gut, aber nur die Precision zeigt, dass etwa jeder fünfte Alarm falsch ist. Ob das tragbar ist, entscheidet das Verhältnis der Kosten: 12 Fehlalarme × 5 € = 60 €, dagegen 3 übersehene Betrugsfälle × 400 € = 1.200 €. Die übersehenen Fälle sind zwanzigmal so teuer.

**Warum "niedrig" nicht "so niedrig wie möglich" bedeutet:** Bei sehr niedriger Schwelle werden viele harmlose Zahlungen blockiert, Kunden verlieren das Vertrauen und die Prüfkapazität ist erschöpft. Die Schwelle ist ein Kompromiss, in der Praxis oft **mehrstufig**: sehr hoher Score blockiert automatisch, mittlerer Score geht in die manuelle Prüfung, niedriger Score läuft durch.

---

## 5. Gesamtübersicht Arbeitsauftrag 1

| Feld | Zielgröße | Teurerer Fehler | Leitmetrik | Schwelle | Ein-Satz-Begründung |
| --- | --- | --- | --- | --- | --- |
| **Demand** | Absatz in Stück | Unter- vs. Überprognose, je nach Ware | MAE (+ Bias), RMSE bei Ausreißern | Quantil τ = C_unter / (C_unter + C_über) | Der durchschnittliche Fehler in Stück zählt, die Asymmetrie steckt im Quantil. |
| **Maintenance** | Ausfall in 14 Tagen | FN | Recall (+ Precision) | niedrig | Ein verpasster Ausfall ist teurer als eine unnötige Prüfung. |
| **Churn** | Kündigung in 90 Tagen | FN, wenn die Aktion wirkt | Wert in € | mittel, p > K / (q · W) | Nur wenn die erwartete gerettete Marge die Kosten übersteigt, lohnt die Aktion. |
| **Fraud** | Betrug ja/nein | FN | Recall + Precision, nie Accuracy | niedrig, p > K / 400 € | 400 € je Betrug schlagen wenige Euro je Prüfung. |

**Das gemeinsame Prinzip:** Man wählt Metrik und Schwelle nicht nach Gewohnheit, sondern **aus den Kosten der Fehler**. Zuerst die Frage "Was kostet FP, was kostet FN?", dann die Metrik, dann die Schwelle.

---

# Arbeitsauftrag 2: Anti-Muster (Diagnose und Therapie)

**Diagnose-Werkzeugkasten (Folie 8)**, den wir bei jedem Fall abprüfen:

| # | Frage |
| --- | --- |
| 1 | Sind alle Merkmale zum Zeitpunkt der Vorhersage schon bekannt? |
| 2 | Bleibt das Modell gültig, wenn sich die Welt ändert? |
| 3 | Passt die Metrik zum Problem und zu den Kosten von Fehlern? |
| 4 | Folgt aus der Vorhersage eine konkrete Handlung? |
| 5 | Bilden die Daten alle wichtigen Einflüsse ab? |
| 6 | Gibt es eine messbare Zielgröße mit Historie (Labels)? |

Die Folie sagt es selbst: **Der Fehler liegt in der Idee, nicht in der Technik.**

---

## Fall A · Fitnessstudio-Kette

**Die Idee:** Ein Modell sagt je Mitglied die Kündigungswahrscheinlichkeit voraus, trainiert auf dem **aktuellen CRM-Bestand**. Nach Vertragsende wird ein Mitglied aus dem CRM gelöscht. Start in vier Wochen.

### Diagnose

**Der Trainingsdatensatz enthält fast keine Kündiger.** Wer gekündigt hat, ist aus dem CRM gelöscht. Im Bestand stehen nur die Mitglieder, die geblieben sind. Das Modell lernt also nie, wie ein späterer Kündiger aussieht. Das ist ein **Auswahlfehler (Survivorship Bias)** und zugleich ein Fehler bei der Zielgröße: **Es gibt keine Labels** für die Klasse, die man vorhersagen will.

| Werkzeug-Frage | Ergebnis |
| --- | --- |
| 6. Zielgröße mit Historie (Labels)? | **Nein.** Kündigungen sind nicht gespeichert. Das ist der Kernfehler. |
| 5. Alle wichtigen Einflüsse in den Daten? | Nur Merkmale der Bleiber. Kündigerverhalten (nachlassende Check-ins) fehlt. |
| 4. Folgt eine Handlung? | Ja, das Halteangebot. Das ist der Teil, der stimmt. |

Zur Größenordnung: 15 % von 120.000 Mitgliedern sind **etwa 18.000 Kündigungen pro Jahr**. Genau diese 18.000 Fälle pro Jahr wären der Lernstoff, sie werden aber gelöscht.

### Therapie

1. **Historie aufbewahren:** Gekündigte Mitglieder nicht löschen, sondern mit Kündigungsdatum markieren (oder aus Archiv und Buchhaltung rekonstruieren). Zahlungen und Verträge liegen meist in der Buchhaltung.
2. **Zielgröße mit Stichtag definieren:** "Kündigt innerhalb von 90 Tagen nach dem Stichtag", dazu gehört ein **Stichtagsdatensatz**: Zustand der Mitglieder zu einem Tag in der Vergangenheit, Kündigung im Anschluss als Label.
3. **Merkmale nur aus der Zeit vor dem Stichtag** (Check-ins, Kursbuchungen, Zahlungen). Merkmale wie "Kündigungsgrund" gehören nicht hinein, sie sind erst nach der Kündigung bekannt (Leakage).
4. **Zeitplan anpassen:** Vier Wochen reichen für die Datenrekonstruktion nicht. Realistisch ist erst eine **Datenphase**, dann ein **Pilot an wenigen Studios** mit Kontrollgruppe.
5. **Messen:** Hochrisiko-Gruppe zufällig teilen (z. B. 90 % Halteangebot, 10 % Kontrollgruppe ohne Angebot), danach die Kündigungsquoten beider Teile vergleichen. Nur der Zufall stellt sicher, dass beide Teile das gleiche Ausgangsrisiko haben; ein Vergleich mit Mitgliedern mit niedrigem Risiko oder mit "zufällig nicht angerufenen" Mitgliedern wäre verzerrt.

**Kurzfassung:** Ohne Kündiger im Datensatz kann kein Modell Kündiger erkennen. Erst die Daten reparieren, dann modellieren.

---

## Fall B · Zahlungsdienstleister

**Die Idee:** Etwa 2 Mio. Kartenzahlungen pro Monat, jede hundertste ist Betrug, ein unentdeckter Betrug kostet 400 €. Das Team sagt: "Das Modell liegt auf den Testdaten in 99 % der Fälle richtig, es ist produktionsreif." Das Modell ersetzt die manuelle Prüfung.

### Diagnose

**Falsche Metrik: Die Accuracy ist bei seltenen Ereignissen eine Scheingröße.**

```
Betrugsfälle pro Monat   = 2.000.000 · 1 %      = 20.000
Schaden ohne Erkennung   = 20.000 · 400 €       = 8.000.000 € pro Monat
```

Ein "Modell", das **jede** Zahlung als harmlos einstuft, hat 99 % Accuracy (99 % der Zahlungen sind harmlos), erkennt aber **null** Betrugsfälle. Der Wert "99 %" beweist also nichts: Er ist genau das, was man ohne jede Intelligenz erreicht.

| Werkzeug-Frage | Ergebnis |
| --- | --- |
| 3. Metrik passt zu Problem und Fehlerkosten? | **Nein.** Accuracy ignoriert, dass FN (400 €) viel teurer ist als FP. |
| 4. Folgt eine konkrete Handlung? | Teilweise: unklar, was bei Alarm geschieht, wenn kein Mensch mehr prüft. |
| 2. Gültig, wenn sich die Welt ändert? | Betrüger passen sich an. Ohne manuelle Stichprobe fehlen künftig neue Labels. |

Der zweite Fehler steckt im **Plan**: Wird die manuelle Prüfung ersetzt, versiegt der Strom neuer, verlässlich geprüfter Fälle. Das Modell kann dann nicht mehr nachlernen und nicht mehr kontrolliert werden.

### Therapie

1. **Richtige Metriken:** Recall (Wie viele der 20.000 Fälle finden wir?) und Precision (Wie viele Alarme sind echt?), dazu die Euro-Bilanz.
2. **Schwelle aus den Kosten:** Bei angenommenen 5 € je Prüfung ist `p* = 5 € / 400 € = 1,25 %`.
3. **Beispielrechnung (angenommene Güte: Recall 80 %, Precision 50 %):**

```
Gefunden (TP)           = 20.000 · 80 %          = 16.000
Übersehen (FN)          = 20.000 − 16.000        =  4.000
Fehlalarme (FP)         = 16.000 · (1 − 0,5)/0,5 = 16.000
Prüfaufwand             = (16.000 + 16.000) · 5 €=    160.000 €
Vermiedener Schaden     = 16.000 · 400 €         =  6.400.000 €
Restschaden (FN)        =  4.000 · 400 €         =  1.600.000 €
Nettonutzen             = 6.400.000 € − 160.000 € = 6.240.000 € pro Monat
```

Das Modell lohnt sich, aber nach diesen Maßen, nicht nach "99 %".
4. **Mensch bleibt im Prozess:** Das Modell **priorisiert** die Prüfung (hoher Score zuerst), das Prüfteam entscheidet. Eine **Zufallsstichprobe** bleibt als Qualitätskontrolle und als Quelle für neue Labels.
5. **Pilot statt Ersatz:** Parallellauf (Modell und Stichprobe) und Vergleich, bevor etwas abgeschaltet wird.

**Kurzfassung:** Nicht "Wie oft liegt das Modell richtig?", sondern "Wie viele der 20.000 Betrugsfälle finden wir, und zu welchem Preis an Fehlalarmen?".

---

## Fall C · Lebensmittelhandel

**Die Idee:** 60 Filialen, rund 8.000 Artikel, wöchentliche Bestellung je Filiale und Artikel. Bestellmenge = **Mittelwert der letzten acht Wochen**, für alle Artikel gleich. Pilot im Februar/März mit nur 5 % Abweichung, Rollout auf alle Filialen ab Oktober. Im Sortiment u. a. Lebkuchen, Spargel, Grillkohle, Speiseeis, jede Woche ein Prospekt mit Angeboten.

### Diagnose

**Die Daten bilden die wichtigsten Einflüsse nicht ab (Saison, Aktionen), und der Pilot beweist nichts.**

1. **Saisonartikel:** Ein Mittelwert der letzten acht Wochen hinkt der Realität immer hinterher. Beispiele:
   - **Lebkuchen:** Im Oktober fängt der Verkauf an. Der Mittelwert der letzten acht Wochen (August und September) ist fast null, die Regale sind leer, wenn die Nachfrage steigt. Im Januar ist es umgekehrt: Der Mittelwert ist hoch, die Nachfrage bricht ein, es bleibt Ware übrig.
   - **Grillkohle und Speiseeis:** gleiches Muster mit Sommerbeginn und Wetter.
   - **Spargel:** kurze Saison im Frühjahr, der Mittelwert ist zu Saisonbeginn zu klein, am Ende zu groß.
2. **Prospektaktionen:** Der Prospekt erscheint jede Woche und treibt den Absatz einzelner Artikel stark. Der Mittelwert enthält weder die Aktion der kommenden Woche noch ihre Wirkung.
3. **Pilot in der falschen Jahreszeit:** Februar/März ist für diese Artikel **eine ruhige Zeit**, in der die Nachfrage nahezu flach ist. Hier schlägt jeder einfache Mittelwert gut ab. Die **5 % Abweichung** gelten nur für diese Phase und sagen nichts über den Oktober, wenn Lebkuchen anlaufen, oder über den Sommer.
4. **Ein Rezept für 8.000 Artikel:** "einfach und für alle Artikel gleich" ignoriert, dass Artikel völlig verschieden reagieren (Dauerläufer, Saisonware, Aktionsware).
5. **Zensierte Nachfrage:** Wenn ein Artikel ausverkauft ist, zeigen die Verkaufsdaten nur den Absatz, nicht den Bedarf. Der Mittelwert lernt, zu wenig zu bestellen.

| Werkzeug-Frage | Ergebnis |
| --- | --- |
| 2. Gültig, wenn sich die Welt ändert? | **Nein.** Saison und Aktionen ändern die Welt jede Woche. |
| 5. Alle wichtigen Einflüsse abgebildet? | **Nein.** Saison, Prospekt und Wetter fehlen. |
| 3. Metrik passt? | Unklar: "5 % Abweichung" ohne Definition (MAPE? WAPE? je Artikel oder gesamt?). |

### Therapie

1. **Merkmale ergänzen:** Kalenderwoche, Feiertage, Ferien, **Prospektaktion** (ja/nein, Rabatt), Wetter (als **archivierte Wettervorhersage**, nicht als Ist-Wetter, sonst Leakage), Vorjahreswerte.
2. **Baseline und Modell vergleichen:** Der Achtwochen-Mittelwert wird zur Vergleichsbasis. Das Modell muss ihn auf demselben Zeitraum schlagen.
3. **Artikelgruppen bilden:** Dauerläufer, Saisonartikel, Aktionsartikel. Ein Modell für alle mit **Artikel und Filiale als Merkmal** (siehe Folie "Ein Modell für alle") ist einfacher als 480.000 Einzelmodelle. Das ergibt sich aus 60 Filialen × 8.000 Artikel.
4. **Pilot über eine volle Saison** oder zumindest gezielt in **Anlaufphasen** (Oktober für Lebkuchen, Frühjahr für Spargel). Alternativ ein **Rückwärtstest** auf den Vorjahresdaten, bei dem die Prognose zu jedem Zeitpunkt nur Daten bis dahin sieht.
5. **Metrik definieren:** WAPE oder MAE je Artikelgruppe, zusätzlich **Out-of-Stock-Quote** und **Abschriften** als Geschäftsmaß. Bestellt wird auf ein Quantil, das zum Kostenverhältnis passt (siehe Arbeitsauftrag 1).
6. **Pilot vor dem Rollout:** Wenige Filialen mit Vergleichsgruppe, dann ausrollen.

**Kurzfassung:** Ein einfaches Modell ist in Ordnung, aber es muss die Saison und die Aktionen kennen, und der Test muss in der Jahreszeit stattfinden, in der es schwierig wird.

---

## Fall D · Chemiewerk

**Die Idee:** Seit 2022 sagt ein Modell Pumpenausfälle aus Sensordaten voraus. 2024: neue Pumpentypen eingebaut, Umstellung auf Dreischichtbetrieb. Der Entwickler hat das Werk verlassen. Warnungen gehen automatisch an die Instandhaltung. Zuletzt **drei Ausfälle ohne Vorwarnung**. Die Werkleitung sagt: "Das Modell läuft stabil, es gibt keine Fehlermeldungen." Für 2027 ist kein Budget vorgesehen.

### Diagnose

**Es fehlt der Betrieb: Das Modell ist nicht überwacht, nicht gepflegt und niemand ist zuständig.**

1. **Konzeptdrift (Datendrift):** Das Modell wurde mit Daten aus 2022 trainiert. Neue Pumpentypen haben andere Vibrations- und Temperaturmuster, und der Dreischichtbetrieb verändert die Lastprofile. Die Welt hat sich geändert, das Modell nicht.
2. **Falsches Gütekriterium der Werkleitung:** "Keine Fehlermeldungen" heißt nur, dass die **Software** läuft. Es sagt nichts darüber, ob die **Vorhersagen** stimmen. Die drei Ausfälle ohne Vorwarnung sind drei **FN**, also genau der teure Fehler. Ein stilles Modell, das nichts meldet, ist hier ein schlechtes Zeichen.
3. **Keine Verantwortung:** Der Entwickler ist weg, Wissen und Dokumentation fehlen. Niemand kann Nachtraining, Fehlersuche oder Schwellen ändern.
4. **Kein Monitoring:** Es gibt keine Kennzahl, die zeigt, wie viele echte Ausfälle das Modell vorher gemeldet hat.
5. **Kein Budget:** Für 2027 ist nichts geplant. Das Modell würde damit stillschweigend veralten oder abgeschaltet.

| Werkzeug-Frage | Ergebnis |
| --- | --- |
| 2. Gültig, wenn sich die Welt ändert? | **Nein.** Neue Pumpen und Schichtbetrieb verändern die Daten. Das ist der Kernfehler. |
| 3. Metrik passt? | Es wird gar keine gemessen. Passend wäre der **Recall über echte Ausfälle**. |
| 5. Alle Einflüsse abgebildet? | Pumpentyp und Schichtmodell fehlen als Merkmale. |
| 6. Labels mit Historie? | Ja (Ausfälle sind bekannt), werden aber nicht genutzt. |

### Therapie

1. **Sofort messen:** Rückblickend prüfen, wie viele der Ausfälle seit 2024 das Modell vorher gemeldet hat (Recall) und wie viele Alarme falsch waren (Precision). Die drei Ausfälle ohne Vorwarnung sind die ersten Fälle.
2. **Verantwortlichen benennen:** Ein Modell-Owner (Rolle, nicht Person), dazu Dokumentation, Übergabe und eine Vertretung.
3. **Nachtrainieren:** Mit Daten ab 2024, **Pumpentyp und Schichtmodell als Merkmale**. Wenn für die neuen Pumpen noch wenig Ausfälle vorliegen, vorerst zusätzlich regelbasierte Grenzwerte.
4. **Monitoring einführen:**
   - Verteilung der Sensorwerte gegen die Trainingsdaten (Drift-Alarm),
   - monatlich Recall und Precision auf den tatsächlichen Ausfällen,
   - Zahl der Alarme pro Woche (zu wenige und zu viele sind beides Warnzeichen).
5. **Fallback:** Bis das Modell neu geprüft ist, gilt die zeit- oder zustandsbasierte Wartung als Absicherung.
6. **Betriebsbudget einplanen:** Ein Modell ist kein Projekt mit Enddatum, sondern ein laufender Betrieb (Pflege, Überwachung, Nachtraining). Die Kosten stehen im Verhältnis zu den Ausfallkosten. Ein einziger ungeplanter Stillstand kann ein Vielfaches der jährlichen Pflege kosten.

**Kurzfassung:** Ein Modell ohne Verantwortlichen, ohne Monitoring und ohne Budget stirbt leise. "Keine Fehlermeldungen" ist keine Gütekennzahl.

---

## Gesamtübersicht Arbeitsauftrag 2

| Fall | Hauptfehler | Welche Werkzeug-Frage greift | Was fehlt (Daten, Metrik, Betrieb) | Rettung |
| --- | --- | --- | --- | --- |
| **A** Fitnessstudio | Trainingsdaten ohne Kündiger | 6 (Labels), 5 (Einflüsse) | **Daten** | Historie, Stichtagsdatensatz, Pilot |
| **B** Zahlungsdienstleister | Accuracy bei seltenem Ereignis | 3 (Metrik) | **Metrik** | Recall/Precision, Kostenschwelle, Mensch im Prozess |
| **C** Lebensmittelhandel | Saison und Aktionen fehlen, Pilot zur falschen Zeit | 2 (Welt ändert sich), 5 (Einflüsse) | **Daten** (Merkmale) und **Test** | Saison-/Aktionsmerkmale, Pilot über Saison |
| **D** Chemiewerk | Kein Betrieb, Drift | 2 (Welt ändert sich), 3 (Metrik) | **Betrieb** | Monitoring, Nachtraining, Owner, Budget |

**Zusammenhang mit den Folien:** Die Fälle passen zur Kernbotschaft von Folie 9: Die meisten ML-Projekte scheitern nicht an der Technik, sondern an **Zielgröße** (Fall A), **Daten** (Fälle A und C) und **Betrieb** (Fall D). Fall B liegt dazwischen: die **Bewertung** (Metrik) ist falsch. Auch Zillow (Tag 8, Einstieg) passt dazu: Prognose als Kaufpreis ohne Puffer, schnelle Skalierung ohne Pilot, keine frühe Wirkungsmessung.

---

## Kernaussagen

1. **Fehler haben Preise.** Erst FP und FN in Euro fassen, dann Metrik und Schwelle wählen. Die Schwelle folgt aus `p* = K / Nutzen`.
2. **Bei seltenen Ereignissen ist Accuracy wertlos.** Ein Modell, das nie anschlägt, hat bei 1 % Betrug 99 % Accuracy.
3. **Ohne Labels kein Lernen.** Die Zielgröße muss mit Historie vorhanden sein, auch für die Fälle, die man vorhersagen will (Kündiger, Ausfälle, Betrug).
4. **Die Welt ändert sich.** Saison, Aktionen, neue Maschinen, neue Betrugsmuster: Ein Modell braucht Merkmale für das, was sich ändert, und Monitoring für das, was man nicht vorhergesehen hat.
5. **Ein Pilot muss die schwierige Zeit abdecken.** Ein guter Wert in ruhiger Zeit beweist nichts über die Spitzen.
6. **Betrieb gehört zum Use Case.** Verantwortlicher, Überwachung und Budget sind Teil des Modells, nicht ein Anhang.

---

## Wo könnten Antworten abweichen?

- **Demand:** Je nach Ware kann die Überprognose teurer sein (Frischware mit kurzer Haltbarkeit) oder die Unterprognose (Dauerware mit hoher Marge). Die Richtung des Quantils folgt daraus.
- **Churn:** Wird die Aktion als nahezu kostenlos angesehen (E-Mail), liegt die Schwelle niedrig und der FN ist klar teurer. Bei teuren Aktionen (Rabatt, Anruf) liegt sie höher.
- **Fraud:** Die Prüfkosten (hier 5 €) sind eine Annahme. Je höher die Kosten, desto höher die Schwelle.
- **Fall A:** Es gibt auch die Lesart "Leakage", wenn das CRM Kündigungsmerkmale enthält. Der Kernfehler bleibt aber das Fehlen der Kündiger.
- **Fall C:** Man kann argumentieren, dass die Prospektaktion der wichtigste fehlende Faktor ist, andere sehen die Saison vorn. Beides gehört in die Diagnose.
