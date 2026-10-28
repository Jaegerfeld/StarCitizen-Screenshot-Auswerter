# StarCitizen Screenshot-Auswerter

Liest **Screenshots der Handelskonsolen** in Star Citizen (Reiter „Kaufen" und „Lokaler Marktwert") mit der eingebauten **Windows-OCR** aus und macht daraus eine **Prüftabelle** plus **JSON/CSV**: Ware, Preis je SCU, Bestand, Status, Ort, Zeitpunkt. Gedacht für zwei Dinge:

1. **star-head.de entlasten** – wer dort Preise pflegt, muss die Konsole nicht mehr abtippen, sondern prüft eine Tabelle und gibt die Datei weiter.
2. **Eigene Daten** – der Export lässt sich in den [Handels-Planer](https://github.com/Jaegerfeld/StarCitizen-Handels-Planer) laden und ergänzt dort die star-head-Daten um die eigenen, frischen Preise.

Alles läuft **lokal und offline**: Windows 10/11 mit OCR-Sprachpaket (Deutsch oder Englisch, in der Regel vorhanden) und Python 3 (nur Standardbibliothek). Keine Installation von Tesseract oder ähnlichem.

## So geht's

1. **Vor dem Screenshot im Spiel:** links unter „Deine Inventare" den **Standort auswählen**. Dann steht der Ort im Bild und der Auswerter kann ihn zuordnen. Ohne Auswahl zeigt das Feld nur „Standort wählen".
2. **Frontal auf die Konsole schauen** und per SC-Screenshot-Taste (Standard **F12**, Datei `ScreenShot-JJJJ-MM-TT_hh-mm-ss-xxx.jpg` im Ordner `StarCitizen\LIVE\screenshots`) oder einem beliebigen Tool aufnehmen. Lange Listen: einfach scrollen und mehrere Screenshots machen, die Auswertung führt sie zusammen.
3. **Auswerten:** Ordner (oder einzelne Bilder) auf `Auswerten.bat` ziehen, oder

   ```bash
   python auswerter.py "C:\Pfad\zu\den\Screenshots"
   ```

   Ergebnis im Unterordner `Auswertung\`: `auswertung.html` (Prüftabelle), `auswertung.json`, `auswertung.csv`, dazu `ocr_words.json` (Rohdaten).
4. **Prüfen:** Die HTML-Seite öffnen. Gelb markierte Zeilen bitte gegen den Screenshot prüfen und direkt in der Tabelle korrigieren (Ware, Preis, Bestand sind editierbar, Zeilen lassen sich entfernen). Bei mehrdeutigem Ort (z. B. Orison: TDD oder Municipal Services) den Shop im Kopf der Serie wählen.
5. **Herunterladen:** Knopf „JSON" oder „CSV" – die Datei enthält die geprüften Werte und kann an star-head gehen oder in den Handels-Planer geladen werden.

## Was erkannt wird

| Reiter in der Konsole | Bedeutung | Spalten |
|---|---|---|
| **Kaufen** (Shop verkauft) | Du kaufst dort ein | Ware, Preis ¤/SCU, **Bestand SCU**, Status (z. B. „Sehr niedrige Bestände") |
| **Lokaler Marktwert** (Shop kauft) | Du verkaufst dort | Ware, Preis ¤/SCU, Status (z. B. „Ausverkauft") |

Der aktive Reiter wird an der hell hinterlegten Reiter-Beschriftung erkannt; der Ort am Feld „Deine Inventare". Warennamen werden gegen die star-head-Warenliste abgeglichen (OCR-Fehler wie `ALUMINI.jn` → Aluminum), der Preis gegen den letzten bekannten star-head-Preis plausibilisiert. Jede Unsicherheit steht als Hinweis in der Zeile; nichts wird stillschweigend geraten.

## Grenzen (Stand 0.1.0)

- **Schräg aufgenommene Konsolen** (Blick von der Seite, perspektivisch verzerrt) liest die Windows-OCR schlecht. Frontal davorstellen hilft am meisten.
- Deutscher Spiel-Client. Englische Konsolentexte folgen, sobald Screenshots vorliegen.
- Die OCR verwechselt gelegentlich 0/O und 1/l und verliert bei Preisen die führende Ziffer; der Auswerter korrigiert, was eindeutig ist, und markiert den Rest.

## Dateiformat

`auswertung.json` / `auswertung.csv` (Semikolon, UTF-8): `system`, `ort`, `shop`, `standort_im_bild`, `art` (Kauf/Verkauf, aus Sicht des Spielers), `ware`, `preis_auec_scu`, `bestand_scu` (nur Kauf), `status`, `stand` (Zeitpunkt des Screenshots), `bild`, `konfidenz` (`ok`, `pruefen`, nach Korrektur `korrigiert`), `hinweise`. Schema-Kennung `sc-konsole-export/1`. Das Format ist ein Vorschlag und wird angepasst, sobald star-head ein Einreichformat festlegt.

## Referenzdaten

`referenz.json` (Warenliste, Shops mit Ort und System, letzte Preise) stammt aus der täglich gebauten `data.json` des Handels-Planers. Aktualisieren mit:

```bash
python referenz_aktualisieren.py
```

## Lizenz

BSD-3-Clause, siehe `LICENSE`. Inoffizielles Fan-Projekt, nicht mit Cloud Imperium Games verbunden. Star Citizen® ist eine Marke von CIG.
