# StarCitizen Screenshot Evaluator

*Deutsche Fassung: [README.de.md](README.de.md)*

Reads **screenshots of Star Citizen trade terminals** (tabs "Buy" and "Local market value") **in the browser** and turns them into a **review table** plus **JSON/CSV**: commodity, price per SCU, stock, status, location, timestamp. Nothing is uploaded; OCR runs on your machine.

**🌐 Online version:** https://jaegerfeld.github.io/StarCitizen-Screenshot-Auswerter/

Two purposes:

1. **Support star-head.de** – contributors who maintain prices there no longer type the terminal off by hand; they check a table and hand over the file.
2. **Own data** – the export can be loaded into the [Trade Planner](https://github.com/Jaegerfeld/StarCitizen-Handels-Planer) (folder `eigene_daten/`), where it enriches the star-head data with your own fresh prices.

## How to

1. **Before the screenshot:** in the left panel "Your inventories" **select the location**. The place is then visible in the image and can be matched.
2. **Face the terminal squarely** and capture with the SC screenshot key (**Print**, file `ScreenShot-YYYY-MM-DD_hh-mm-ss-xxx.jpg` in `StarCitizen\LIVE\screenshots`) or any tool. Long lists: scroll and take several screenshots, they are merged.
3. **Open the page** (online or `SC_Screenshot_Auswerter.html` by double-click) and drop the images – single files or a whole folder. About 15 seconds per image; series appear as soon as they are read.
4. **Review:** check highlighted rows against the screenshot (link in the "Image" column). Values right: click **✓** (or "Confirm all open rows in this series"). Values wrong: edit commodity, price or stock in place. Not a commodity at all (icon noise): **✕** removes the row from the export. The counter "still to check" shows when you are done; the export asks before leaving yellow rows in. If the place is ambiguous (e.g. Orison: TDD or Municipal Services) pick the shop in the series header.
5. **Download:** "JSON" or "CSV" – with the reviewed values.

## What is recognised

| Terminal tab | Meaning | Columns |
|---|---|---|
| **Buy** (shop sells) | you buy here | commodity, price ¤/SCU, **stock SCU**, status |
| **Local market value** (shop buys) | you sell here | commodity, price ¤/SCU, status |

- Active tab from the highlighted tab label, place from the "Your inventories" field, timestamp from the SC file name.
- Each image is read twice (two contrasts); the currency glyph ¤ is detected by its shape so that "¤10,000" does not become "110,000".
- Commodity names are matched against the star-head list; prices are sanity-checked against the last known star-head price. Every doubt is written into the row; nothing is guessed silently.
- The reference (commodities, shops, last prices) is embedded and comes from the Trade Planner's daily `data.json`; "Load latest reference" fetches it fresh from GitHub Pages.

## Windows OCR as an alternative

The built-in Windows OCR reads slightly better than the browser engine but needs Windows. Drop a folder or images onto `Windows_OCR_lesen.bat`: `ocr_engine.ps1` writes `ocr_words.json` next to the screenshots; drop that file into the page. Evaluation, review table and export are the same.

## Limits (0.5.0)

- **Terminals captured at an angle** (up to about 30°): the page straightens the right panel from four corners (found automatically or clicked by you) and isolates the text by threshold. Still noticeably worse than a square shot; the place is often not recognised then, so pick the shop by hand. Standing square in front remains best.
- German and English game clients are recognised (tabs, sections, status, location field); the file list shows the detected client per image. No other languages.
- If the terminal shows the price per container (`/UNITS`, when a container size is selected in game), the page converts to per SCU via the star-head reference price and notes the divisor; without a reference the row stays flagged.
- Single prices may stay unreadable (e.g. an icon touching the number); they are flagged, not guessed.

## File format

`auswertung.json` / `auswertung.csv` (semicolon, UTF-8): `system`, `ort`, `shop`, `standort_im_bild`, `art` (Kauf/Verkauf from the player's view), `ware`, `preis_auec_scu`, `bestand_scu` (buy only), `status`, `stand`, `bild`, `konfidenz` (`ok` = recognised without doubt, `bestaetigt` = confirmed by a person, `korrigiert` = edited by a person, `pruefen` = still unchecked), `hinweise`. Schema id `sc-konsole-export/1`; a proposal until star-head defines a submission format.

## Build it yourself

```bash
python auswerter_bauen.py             # embeds referenz.json -> SC_Screenshot_Auswerter.html
python auswerter_bauen.py --referenz  # refreshes the reference from GitHub Pages first
```

Standard library only. The online version is rebuilt daily (05:30 UTC, after the Trade Planner) by GitHub Actions.

## License

BSD-3-Clause, see `LICENSE`. Unofficial fan project, not affiliated with Cloud Imperium Games. Star Citizen® is a trademark of CIG. OCR: [Tesseract.js](https://github.com/naptha/tesseract.js) (Apache-2.0).
