# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [0.7.1] – 2026-11-01

### Geändert
- **Kommentare und Docstrings** nach dem Standard von [situation-report](https://github.com/Jaegerfeld/situation-report): Kopfblock mit Autor, Lizenz und fachlicher Funktion in jeder Quelldatei, englische Docstrings im Google-Stil mit `Args`/`Returns`/`Raises`, `#:`-Kommentare an Konstanten, ein Satz über jeder JavaScript-Funktion der Seite. Am Verhalten ändert sich nichts.
- Neue Datei `CONTRIBUTING.md` mit den gemeinsamen Regeln aller vier SC-Tools (Prüfungen, Kommentare, Versionen, gemeinsame Dateien).

## [0.7.0] – 2026-11-01

### Hinzugefügt
- **Gemeinsames Design** aller vier SC-Tools in `sc_design.py` (in allen vier Repos identisch, wie `kopfzeile.py`): Farben für Hell und Dunkel, Schriften (Rajdhani für Überschriften, Exo 2 für Text), Knöpfe, Eingabefelder, Fokusrahmen, Lösch-Knopf-Stil.
- **Handy und Tablet:** Auf schmalen Bildschirmen (unter 920 px) zeigen Tools mit mehreren Bereichen oben Reiter statt nebeneinanderliegender Spalten; der Hauptinhalt kommt zuerst. Auf Touch-Geräten sind Knöpfe, Felder und Häkchen mindestens 44 px groß. Kein seitliches Scrollen mehr bei 390 px Breite; breite Tabellen scrollen nur in ihrem Rahmen.
- Kopfzeile am Handy kompakter: Einzeiler auf zwei Zeilen gekürzt, „Weitere Tools“ klappt auf.

### Geändert
- Auswahlfelder werden auf dem Handy nicht breiter als der Bildschirm.

## [0.6.0] – 2026-11-01

### Hinzugefügt
- **„Was ist neu?“** in der Kopfzeile: zeigt dieses Changelog in einem Dialog, mit der aktuellen Version im Titel und einem Link auf die Datei auf GitHub. Der Text wird beim Bauen aus `CHANGELOG.md` übernommen und funktioniert auch in der Offline-Kopie. Schließen per Esc, Klick daneben oder ✕.

### Geändert
- **Einheitliche Kopfzeile** in allen vier SC-Tools (Bauplan-, Wikelo-, Handels-Planer, Screenshot-Auswerter): Kicker, Titel mit Version, Einzeiler, Aktionszeile (Sprache DE | EN mit sichtbarer aktiver Sprache, Hell/Dunkel, „Was ist neu?“, Tool-Aktionen, „Neuesten Stand laden“), eigene Zeile „Weitere Tools“ mit denselben Zielen in derselben Reihenfolge, Datenzeile. Quelle ist `kopfzeile.py`, in allen vier Repos identisch.
- Der GitHub-Link steht jetzt im „Was ist neu?“-Dialog statt in der Kopfzeile (wie in allen Tools).

## [0.5.0] – 2026-10-29

### Hinzugefügt
- **Englischer Spiel-Client:** Reiter BUY / LOCAL MARKET VALUE, Abschnitte IN STOCK / OUT OF STOCK / SELLABLE CARGO / IN DEMAND / NO DEMAND / CANNOT SELL, Statuszeilen (VERY LOW … MAX INVENTORY, … DEMAND), SHOP QUANTITY, YOUR INVENTORIES / SELECT LOCATION. Deutsch und Englisch laufen durch dieselbe Logik; die Dateiliste zeigt je Bild den erkannten Client, der Export trägt ihn im Feld `client`.
- **Preis je Container** (`¤ …/UNITS`, wenn im Spiel eine Containergröße angewählt ist): Umrechnung auf je SCU über den star-head-Referenzpreis (Teiler 2–32 wird vermerkt), sonst Markierung „zu prüfen“.

### Geändert
- Hinweistext und README: Screenshots im Spiel mit **Druck** (englisch **Print**), nicht F12.

## [0.4.0] – 2026-10-28

### Hinzugefügt
- **Schräge Aufnahmen** (bis etwa 30° Verkantung): Findet die grobe Lesung keine Reiter, wird das rechte Panel entzerrt (Homographie aus vier Ecken) und der helle Text per Schwellwert freigestellt, bevor Tesseract liest. Die Ecken sucht die Seite zuerst automatisch (größte helle Glasfläche); klappt das nicht, bittet sie um vier Klicks auf die Panel-Ecken. Gesetzte Ecken gelten für die folgenden Bilder gleicher Größe weiter, solange sie passen. Schräg gelesene Bilder sind in der Dateiliste markiert.

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
