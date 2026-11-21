# SC Screenshot-Auswerter – Anleitung

## Kurzanleitung

Der Screenshot-Auswerter liest Screenshots der Handelskonsole in Star Citizen aus. Du bekommst eine Prüftabelle mit Ware, Preis je SCU, Bestand, Status, Ort und Zeitpunkt und lädst sie als JSON oder CSV herunter.

### Bereiche der Seite

- **Kopfzeile:** Sprache **DE | EN**, **Hell / Dunkel**, **Was ist neu?** (Änderungen je Version) und **🔄 Neuesten Stand laden (GitHub)**. Darunter **Weitere Tools** und die Datenzeile mit dem Stand der Referenz (Datum, Patch, Zahl der Waren und Shops).
- **Ablagefeld „Screenshots hierher ziehen“:** Bilder (PNG, JPG) oder einen Ordner hineinziehen. Alternativ **Bilder wählen** oder **Ordner wählen**. Auch die Datei `ocr_words.json` der Windows-OCR gehört hierher.
- **Fortschritt:** Balken und Dateiliste. Je Bild steht dort ✓ oder ✗, der erkannte Client (deutsch oder englisch) und ob das Bild schräg oder als Glas-Kiosk gelesen wurde.
- **Ecken-Auswahl:** Erscheint nur bei schräg aufgenommenen Konsolen, wenn die Seite das Panel nicht selbst findet. Du klickst vier Ecken an, dann **Entzerren und lesen**. Mit **Ecken löschen** fängst du neu an, mit **Bild überspringen** lässt du das Bild aus.
- **Serien:** Je Ort und Reiter ein Block. Die Plakette zeigt **KAUFEN · Shop verkauft** oder **LOKALER MARKTWERT · Shop kauft**. Rechts wählst du unter **Shop (star-head)** den passenden Shop.
- **Prüftabelle:** Spalten **Ware**, **Preis ¤/SCU**, **Bestand SCU** (nur beim Kaufen), **Status**, **Stand**, **Bild**, **Hinweise**. Gelbe Zeilen mit **PRÜFEN** sind unsicher. Ware, Preis und Bestand kannst du direkt in der Zelle ändern (Stift-Zeichen ✎).
- **Knöpfe je Zeile:** **✓** bestätigt die Zeile, **✕** entfernt sie aus dem Export.
- **Ergebnisleiste:** **⬇ JSON**, **⬇ CSV**, **Alles zurücksetzen** und der Zähler „noch zu prüfen“.

### Häufige Handgriffe

- Gelbe Zeile gegen das Bild prüfen: Klick auf den Dateinamen in der Spalte **Bild** öffnet den Screenshot in einem neuen Tab.
- Alles in einer Serie passt: **✓ Alle offenen in dieser Serie bestätigen**.
- Ort nicht erkannt: Shop im Feld **Shop (star-head)** von Hand wählen.
- Neu anfangen: **Alles zurücksetzen**.

### Daten und Speicherung

- Die Referenz (Warenliste, Shops, letzte star-head-Preise) steckt in der Seite. Sie stammt aus den täglichen Daten des Handels-Planers.
- **🔄 Neuesten Stand laden (GitHub)** holt die Referenz frisch von GitHub Pages. Die Seite merkt sie sich im Browser.
- Im Browser bleiben außerdem nur Sprache und Hell/Dunkel. Deine Korrekturen in der Tabelle werden nicht gespeichert. Lade die Datei herunter, bevor du die Seite schließt.
- Offline-Kopie: `SC_Screenshot_Auswerter.html` per Doppelklick öffnen. Für die Texterkennung im Browser lädt die Seite Tesseract.js und die Sprachdaten aus dem Internet.

### Datenschutz

- Deine Screenshots werden nicht hochgeladen. Die Texterkennung läuft auf deinem Rechner.
- Ins Internet gehen nur Abrufe: die Texterkennung (Tesseract.js) und auf Knopfdruck die Referenz von GitHub Pages.

## Tutorial: Preisliste aus Bildern

Ziel: Du machst im Spiel Screenshots einer Handelskonsole und erhältst eine geprüfte Preisliste als CSV oder JSON.

1. Geh im Spiel an eine Handelskonsole. Wähle links unter **Deine Inventare** deinen Standort aus. Ohne Auswahl steht dort nur „Standort wählen“, und der Ort fehlt später.
2. Wähle den Reiter **Kaufen** (der Shop verkauft) oder **Lokaler Marktwert** (der Shop kauft).
3. Stell dich frontal vor die Konsole und drück **Druck**. Das Spiel legt das Bild im Ordner `StarCitizen\LIVE\screenshots` ab.
4. Ist die Liste lang, scroll weiter und mach noch einen Screenshot. Die Seite führt mehrere Bilder derselben Konsole zu einer Serie zusammen.
5. Öffne den Screenshot-Auswerter. Zieh die Bilder auf **Screenshots hierher ziehen** oder klick **Bilder wählen** bzw. **Ordner wählen**.
6. Warte, bis der Balken durchgelaufen ist. Beim ersten Bild steht dort kurz „Texterkennung wird geladen …“. Danach dauert ein Bild etwa 15 Sekunden.
7. Prüf den Kopf jeder Serie: Stimmen Ort und Reiter? Steht dort ein Warnhinweis zum Standort, wähle den Shop unter **Shop (star-head)**.
8. Geh die gelben Zeilen durch. Die Spalte **Hinweise** sagt, was unsicher ist, zum Beispiel „Preis nicht lesbar“ oder „Name unsicher“. Öffne bei Bedarf das Bild über die Spalte **Bild**.
9. Stimmt ein Wert nicht, klick in die Zelle und korrigier ihn. Die Zeile zeigt dann „✓ geändert“.
10. Stimmen die Werte, klick **✓** in der Zeile oder **✓ Alle offenen in dieser Serie bestätigen**. Ist eine Zeile gar keine Ware, entferne sie mit **✕**.
11. Wenn „noch zu prüfen“ auf 0 steht, klick **⬇ CSV** oder **⬇ JSON**. Sind noch gelbe Zeilen offen, fragt die Seite vorher nach.
12. Die Datei heißt `auswertung.csv` bzw. `auswertung.json`. Die CSV ist für Excel eingerichtet (Semikolon, UTF-8). Den Export kannst du in den Handels-Planer laden (Ordner `eigene_daten/`).

### Tipps

- Schau frontal auf die Konsole. Schräge Bilder liest die Seite schlechter, den Ort oft gar nicht.
- Deutscher und englischer Spiel-Client werden erkannt, andere Sprachen nicht.
- Ein Bild mit ✗ und „kein Konsolentext gefunden“ zeigt meist keine Handelskonsole mit den Reitern Kaufen / Lokaler Marktwert.
- Fehlt eine ganz neue Ware, kennt die Referenz sie noch nicht. Probier **🔄 Neuesten Stand laden (GitHub)**.
- Zeigt die Konsole Preise je Container (`/UNITS`), rechnet die Seite auf je SCU um und vermerkt den Teiler in **Hinweise**.

## Tutorial: Windows-OCR

Ziel: Du liest die Screenshots mit der eingebauten Texterkennung von Windows. Sie liest etwas genauer als die Erkennung im Browser und läuft ohne Internet.

1. Lade dir das Repository herunter, sodass `Windows_OCR_lesen.bat`, `ocr_engine.ps1` und `SC_Screenshot_Auswerter.html` im selben Ordner liegen.
2. Sammle deine Screenshots in einem Ordner, zum Beispiel eine Kopie von `StarCitizen\LIVE\screenshots`.
3. Zieh den Ordner (oder einzelne Bilder) im Explorer auf `Windows_OCR_lesen.bat`.
4. Ein Konsolenfenster öffnet sich und liest die Bilder. Warte auf die Meldung „Fertig“.
5. Neben den Screenshots liegt jetzt die Datei `ocr_words.json`. Der Auswerter öffnet sich automatisch.
6. Zieh `ocr_words.json` auf **Screenshots hierher ziehen**. Die Dateiliste zeigt ✓ und die Zahl der Bilder.
7. Prüf, korrigier und bestätige die Zeilen wie im Tutorial „Preisliste aus Bildern“ (Schritte 7 bis 10).
8. Lade das Ergebnis mit **⬇ CSV** oder **⬇ JSON** herunter.

### Tipps

- Die Windows-OCR liest bevorzugt Deutsch, sonst die Sprache deines Windows-Profils, sonst Englisch.
- Bei dieser Variante ist der Dateiname in der Spalte **Bild** kein Link. Öffne den Screenshot zum Vergleich selbst im Explorer.
- Meldet das Fenster einen Fehler, steht die Ursache direkt darüber.

## Fragen

### Wird etwas hochgeladen?

Nein. Die Screenshots bleiben auf deinem Rechner. Die Seite lädt nur die Texterkennung aus dem Internet und auf Knopfdruck die Referenz von GitHub Pages.

### Warum ist eine Zeile gelb?

Die Seite ist sich bei Name, Preis oder Bestand nicht sicher, oder der Preis weicht stark vom letzten star-head-Wert ab. Der Grund steht in **Hinweise**. Die Seite rät nicht stillschweigend, sie markiert.

### Was bedeutet „neu für diesen Shop“?

Die Ware stand bisher nicht in den star-head-Daten dieses Shops. Das ist ein Hinweis, kein Fehler.

### Warum fehlt die Spalte „Bestand SCU“?

Beim Reiter **Lokaler Marktwert** kauft der Shop. Dort zeigt die Konsole keinen Bestand.

### Was steht in der Export-Datei?

Je Zeile System, Ort, Shop, Standort im Bild, Art (Kauf oder Verkauf aus deiner Sicht), Ware, Preis, Bestand, Status, Zeitpunkt, Bild, Konfidenz und Hinweise. Die Konfidenz ist `ok`, `bestaetigt`, `korrigiert` oder `pruefen`.

### Die Seite fragt nach vier Ecken. Was tun?

Das Bild ist schräg. Klick die Ecken des rechten Panels mit den Reitern an: oben links, oben rechts, unten rechts, unten links. Dann **Entzerren und lesen**. Die Ecken gelten auch für die folgenden Bilder gleicher Größe, solange sie passen.
