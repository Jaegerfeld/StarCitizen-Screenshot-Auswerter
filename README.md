# StarCitizen Screenshot Evaluator

*Deutsche Fassung: [README.de.md](README.de.md)*

Reads **screenshots of Star Citizen trade terminals** (tabs "Buy" and "Local market value") with the built-in **Windows OCR** and turns them into a **review table** plus **JSON/CSV**: commodity, price per SCU, stock, status, location, timestamp. Two purposes:

1. **Support star-head.de** – contributors who maintain prices there no longer type the terminal off by hand; they check a table and hand over the file.
2. **Own data** – the export can be loaded into the [Trade Planner](https://github.com/Jaegerfeld/StarCitizen-Handels-Planer), where it enriches the star-head data with your own fresh prices.

Everything runs **locally and offline**: Windows 10/11 with an OCR language pack (German or English, usually present) and Python 3 (standard library only). No Tesseract or other installs.

## How to

1. **Before the screenshot:** in the left panel "Your inventories" **select the location**. The place is then visible in the image and can be matched. Without it the field only says "Select location".
2. **Face the terminal squarely** and capture with the SC screenshot key (default **F12**, file `ScreenShot-YYYY-MM-DD_hh-mm-ss-xxx.jpg` in `StarCitizen\LIVE\screenshots`) or any tool. Long lists: scroll and take several screenshots, they are merged.
3. **Evaluate:** drag the folder (or single images) onto `Auswerten.bat`, or

   ```bash
   python auswerter.py "C:\path\to\screenshots"
   ```

   Output in the sub-folder `Auswertung\`: `auswertung.html` (review table), `auswertung.json`, `auswertung.csv`, plus `ocr_words.json` (raw OCR).
4. **Review:** open the HTML page. Check highlighted rows against the screenshot and correct them in place (commodity, price, stock are editable, rows can be removed). If the place is ambiguous (e.g. Orison: TDD or Municipal Services) pick the shop in the series header.
5. **Download:** "JSON" or "CSV" – the file carries the reviewed values and can go to star-head or into the Trade Planner.

## What is recognised

| Terminal tab | Meaning | Columns |
|---|---|---|
| **Buy** (shop sells) | you buy here | commodity, price ¤/SCU, **stock SCU**, status |
| **Local market value** (shop buys) | you sell here | commodity, price ¤/SCU, status |

The active tab is detected from the highlighted tab label; the place from the "Your inventories" field. Commodity names are matched against the star-head list (OCR slips like `ALUMINI.jn` → Aluminum); prices are sanity-checked against the last known star-head price. Every doubt is written into the row; nothing is guessed silently.

## Limits (0.1.0)

- **Terminals captured at an angle** read poorly with Windows OCR. Standing square in front helps most.
- German game client only for now; English terminal texts follow once screenshots are available.
- OCR sometimes confuses 0/O and 1/l and drops a leading digit in prices; the evaluator fixes what is unambiguous and flags the rest.

## File format

`auswertung.json` / `auswertung.csv` (semicolon, UTF-8): `system`, `ort`, `shop`, `standort_im_bild`, `art` (Kauf/Verkauf from the player's view), `ware`, `preis_auec_scu`, `bestand_scu` (buy only), `status`, `stand` (screenshot time), `bild`, `konfidenz` (`ok`, `pruefen`, after editing `korrigiert`), `hinweise`. Schema id `sc-konsole-export/1`. The format is a proposal and will follow whatever star-head defines for submissions.

## Reference data

`referenz.json` (commodities, shops with place and system, last prices) comes from the Trade Planner's daily `data.json`. Refresh with `python referenz_aktualisieren.py`.

## License

BSD-3-Clause, see `LICENSE`. Unofficial fan project, not affiliated with Cloud Imperium Games. Star Citizen® is a trademark of CIG.
