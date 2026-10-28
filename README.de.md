# StarCitizen Screenshot-Auswerter

Liest **Screenshots der Handelskonsolen** in Star Citizen (Reiter „Kaufen" und „Lokaler Marktwert") direkt **im Browser** aus und macht daraus eine **Prüftabelle** plus **JSON/CSV**: Ware, Preis je SCU, Bestand, Status, Ort, Zeitpunkt. Nichts wird hochgeladen, die Texterkennung läuft auf deinem Rechner.

**🌐 Online-Version:** https://jaegerfeld.github.io/StarCitizen-Screenshot-Auswerter/

Gedacht für zwei Dinge:

1. **star-head.de entlasten** – wer dort Preise pflegt, muss die Konsole nicht mehr abtippen, sondern prüft eine Tabelle und gibt die Datei weiter.
2. **Eigene Daten** – der Export lässt sich in den [Handels-Planer](https://github.com/Jaegerfeld/StarCitizen-Handels-Planer) laden (Ordner `eigene_daten/`) und ergänzt dort die star-head-Daten um die eigenen, frischen Preise.

## So geht's

1. **Vor dem Screenshot im Spiel:** links unter „Deine Inventare" den **Standort auswählen**. Dann steht der Ort im Bild und wird zugeordnet. Ohne Auswahl zeigt das Feld nur „Standort wählen".
2. **Frontal auf die Konsole schauen** und per SC-Screenshot-Taste (Standard **F12**, Datei `ScreenShot-JJJJ-MM-TT_hh-mm-ss-xxx.jpg` im Ordner `StarCitizen\LIVE\screenshots`) oder einem beliebigen Tool aufnehmen. Lange Listen: scrollen und mehrere Screenshots machen, die Auswertung führt sie zusammen.
3. **Seite öffnen** (online oder `SC_Screenshot_Auswerter.html` per Doppelklick) und die Bilder hineinziehen – einzeln oder ein ganzer Ordner. Je Bild dauert die Erkennung etwa 15 Sekunden; die Serien erscheinen, sobald sie gelesen sind.
4. **Prüfen:** Gelb markierte Zeilen gegen den Screenshot prüfen (Link in der Spalte „Bild") und direkt in der Tabelle korrigieren. Ware, Preis und Bestand sind editierbar, Zeilen lassen sich entfernen. Bei mehrdeutigem Ort (z. B. Orison: TDD oder Municipal Services) den Shop im Kopf der Serie wählen.
5. **Herunterladen:** „JSON" oder „CSV" – die Datei enthält die geprüften Werte.

## Was erkannt wird

| Reiter in der Konsole | Bedeutung | Spalten |
|---|---|---|
| **Kaufen** (Shop verkauft) | Du kaufst dort ein | Ware, Preis ¤/SCU, **Bestand SCU**, Status (z. B. „Sehr niedrige Bestände") |
| **Lokaler Marktwert** (Shop kauft) | Du verkaufst dort | Ware, Preis ¤/SCU, Status (z. B. „Ausverkauft") |

- Der aktive Reiter wird an der hell hinterlegten Reiter-Beschriftung erkannt, der Ort am Feld „Deine Inventare", der Zeitpunkt am SC-Dateinamen.
- Jedes Bild wird zweimal gelesen (zwei Kontraste); das Währungszeichen ¤ wird an seiner Glyphenform erkannt, damit aus „¤10.000" nicht „110.000" wird.
- Warennamen werden gegen die star-head-Warenliste abgeglichen, Preise gegen den letzten bekannten star-head-Preis plausibilisiert. Jede Unsicherheit steht als Hinweis in der Zeile; nichts wird stillschweigend geraten.
- Die Referenz (Waren, Shops, letzte Preise) steckt in der Seite und kommt aus der täglichen `data.json` des Handels-Planers; der Knopf „Neuesten Stand laden" holt sie frisch von GitHub Pages.

## Windows-OCR als Alternative

Die eingebaute Windows-OCR liest etwas genauer als die Browser-Erkennung, braucht aber Windows. Ordner oder Bilder auf `Windows_OCR_lesen.bat` ziehen: `ocr_engine.ps1` schreibt `ocr_words.json` neben die Screenshots; diese Datei dann in die Seite ziehen. Auswertung, Prüftabelle und Export sind dieselben.

## Grenzen (Stand 0.2.0)

- **Schräg aufgenommene Konsolen** (Blick von der Seite) liest die Texterkennung schlecht. Frontal davorstellen hilft am meisten.
- Deutscher Spiel-Client. Englische Konsolentexte folgen, sobald Screenshots vorliegen.
- Einzelne Preise bleiben unlesbar (z. B. wenn ein Icon in die Zahl ragt); sie sind markiert, nicht geraten.

## Dateiformat

`auswertung.json` / `auswertung.csv` (Semikolon, UTF-8): `system`, `ort`, `shop`, `standort_im_bild`, `art` (Kauf/Verkauf, aus Sicht des Spielers), `ware`, `preis_auec_scu`, `bestand_scu` (nur Kauf), `status`, `stand` (Zeitpunkt des Screenshots), `bild`, `konfidenz` (`ok`, `pruefen`, nach Korrektur `korrigiert`), `hinweise`. Schema-Kennung `sc-konsole-export/1`. Das Format ist ein Vorschlag und wird angepasst, sobald star-head ein Einreichformat festlegt.

## Selbst bauen

```bash
python auswerter_bauen.py             # bettet referenz.json in die App ein -> SC_Screenshot_Auswerter.html
python auswerter_bauen.py --referenz  # zieht vorher die Referenz frisch von GitHub Pages
```

Nur Python-Standardbibliothek. Die Online-Version wird täglich (05:30 UTC, nach dem Handels-Planer) per GitHub Actions neu gebaut.

## Lizenz

BSD-3-Clause, siehe `LICENSE`. Inoffizielles Fan-Projekt, nicht mit Cloud Imperium Games verbunden. Star Citizen® ist eine Marke von CIG. Texterkennung: [Tesseract.js](https://github.com/naptha/tesseract.js) (Apache-2.0).
