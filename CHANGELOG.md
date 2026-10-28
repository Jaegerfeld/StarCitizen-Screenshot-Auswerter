# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.0.0/), Versionierung nach [SemVer](https://semver.org/lang/de/).

## [0.1.0] – 2026-10-28

### Hinzugefügt
- Erster Prototyp: Handelskonsolen-Screenshots (deutscher Client) per Windows-OCR lesen – Ort, aktiver Reiter (Kaufen / Lokaler Marktwert), Ware, Preis ¤/SCU, Bestand, Status, Zeitpunkt aus dem SC-Dateinamen.
- Namensabgleich gegen die star-head-Warenliste, Shop-Zuordnung über den Ort (bei Mehrdeutigkeit Vorschlag nach Waren-Überschneidung), Preis-Plausibilität gegen den letzten star-head-Wert.
- Zusammenführen mehrerer Scroll-Screenshots derselben Serie; zwei OCR-Lesungen je Bild, Widersprüche werden markiert.
- Prüftabelle `auswertung.html` (editierbar, Zweifel markiert, Shop-Auswahl, JSON/CSV-Download, DE/EN, Hell/Dunkel) sowie `auswertung.json` und `auswertung.csv` (Schema `sc-konsole-export/1`).
- `referenz_aktualisieren.py` zieht die Referenzdaten aus der `data.json` des Handels-Planers.
