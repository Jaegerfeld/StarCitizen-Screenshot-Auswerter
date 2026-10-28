# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [0.3.0] – 2026-10-28

### Hinzugefügt
- **Bestätigen:** ✓ je Zeile (Werte geprüft, passen) und „Alle offenen in dieser Serie bestätigen“. Bestätigte Zeilen verlieren die Markierung und gehen mit `konfidenz = bestaetigt` in den Export; der Zähler „noch zu prüfen“ zählt je Serie und gesamt herunter. Beim Export fragt die Seite nach, wenn noch gelbe Zeilen offen sind.

## [0.2.1] – 2026-10-28

### Behoben
- `auswerter_bauen.py --referenz` reichte die Kommandozeile an `referenz_aktualisieren` durch; der Pages-Build brach mit „No such file: --referenz“ ab. Außerdem verträgt die Referenz jetzt das zehnte Feld (Quelle) in der `data.json` des Handels-Planers ab 1.3.0.

## [0.2.0] – 2026-10-28

### Hinzugefügt
- **Browser-App** `SC_Screenshot_Auswerter.html` (wie die SC-Planer: eine Datei, online auf GitHub Pages): Bilder per Drag-and-drop oder Ordnerwahl, Texterkennung im Browser mit Tesseract.js (deu+eng), Fortschritt je Bild, Prüftabelle mit editierbaren Zellen, Shop-Auswahl, JSON/CSV-Download, DE/EN, Hell/Dunkel, Knopf „Neuesten Stand laden" für die Referenz.
- ¤-Erkennung an der Glyphenform (quadratisch, niedriger als Ziffern), Standort-Feinlesung als Textblock in zwei Vergrößerungen, Panel-Eingrenzung über die Reiter-Beschriftung.
- `auswerter_bauen.py` bettet `referenz.json` in die App ein; Workflow baut täglich (05:30 UTC) und veröffentlicht auf Pages.
- `Windows_OCR_lesen.bat`: optional die Windows-OCR nutzen (`ocr_words.json` in die Seite ziehen).

### Geändert
- Die Auswertungslogik lebt nur noch in JavaScript (eine Logik für Tesseract- und Windows-OCR-Wörter); `auswerter.py` und `pruefseite.html` entfallen.

## [0.1.0] – 2026-10-28

### Hinzugefügt
- Erster Prototyp: Handelskonsolen-Screenshots (deutscher Client) per Windows-OCR lesen – Ort, aktiver Reiter (Kaufen / Lokaler Marktwert), Ware, Preis ¤/SCU, Bestand, Status, Zeitpunkt aus dem SC-Dateinamen.
- Namensabgleich gegen die star-head-Warenliste, Shop-Zuordnung über den Ort (bei Mehrdeutigkeit Vorschlag nach Waren-Überschneidung), Preis-Plausibilität gegen den letzten star-head-Wert.
- Zusammenführen mehrerer Scroll-Screenshots derselben Serie; zwei OCR-Lesungen je Bild, Widersprüche werden markiert.
- Prüftabelle `auswertung.html` (editierbar, Zweifel markiert, Shop-Auswahl, JSON/CSV-Download, DE/EN, Hell/Dunkel) sowie `auswertung.json` und `auswertung.csv` (Schema `sc-konsole-export/1`).
- `referenz_aktualisieren.py` zieht die Referenzdaten aus der `data.json` des Handels-Planers.
