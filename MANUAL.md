# SC Screenshot Reader – Manual

## Quick guide

The Screenshot Reader reads screenshots of the trade terminal in Star Citizen. You get a review table with commodity, price per SCU, stock, status, place and time, and you download it as JSON or CSV.

### Areas of the page

- **Header:** language **DE | EN**, **Light / Dark**, **What’s new?** (changes per version) and **🔄 Load latest reference (GitHub)**. Below it **More tools** and the data line with the state of the reference (date, patch, number of commodities and shops).
- **Drop area "Drop screenshots here":** drop images (PNG, JPG) or a folder. Or use **Choose images** or **Choose folder**. The `ocr_words.json` file from the Windows OCR goes here too.
- **Progress:** bar and file list. For each image it shows ✓ or ✗, the detected client (German or English) and whether the image was read as angled or as a glass kiosk.
- **Corner picker:** appears only for terminals captured at an angle, when the page cannot find the panel itself. You click four corners, then **Straighten and read**. **Clear corners** starts over, **Skip image** leaves the image out.
- **Series:** one block per place and tab. The badge shows **BUY · shop sells** or **LOCAL MARKET VALUE · shop buys**. On the right you pick the matching shop under **Shop (star-head)**.
- **Review table:** columns **Commodity**, **Price ¤/SCU**, **Stock SCU** (buy tab only), **Status**, **As of**, **Image**, **Notes**. Yellow rows marked **CHECK** are uncertain. You can edit commodity, price and stock directly in the cell (pencil mark ✎).
- **Buttons per row:** **✓** confirms the row, **✕** removes it from the export.
- **Result bar:** **⬇ JSON**, **⬇ CSV**, **Reset all** and the counter "still to check".

### Frequent actions

- Check a yellow row against the image: click the file name in the **Image** column to open the screenshot in a new tab.
- Everything in a series is right: **✓ Confirm all open rows in this series**.
- Place not recognised: pick the shop by hand under **Shop (star-head)**.
- Start over: **Reset all**.

### Data and storage

- The reference (commodity list, shops, last star-head prices) is built into the page. It comes from the daily data of the Trade Planner.
- **🔄 Load latest reference (GitHub)** fetches a fresh reference from GitHub Pages. The page keeps it in your browser.
- Apart from that, the browser only keeps language and light/dark. Your corrections in the table are not saved. Download the file before you close the page.
- Offline copy: open `SC_Screenshot_Auswerter.html` with a double click. For the OCR in the browser the page loads Tesseract.js and its language data from the internet.

### Privacy

- Your screenshots are not uploaded. The text recognition runs on your computer.
- The only internet requests are downloads: the OCR engine (Tesseract.js) and, when you press the button, the reference from GitHub Pages.

## Tutorial: Price list from images

Goal: you take screenshots of a trade terminal in the game and get a checked price list as CSV or JSON.

1. Go to a trade terminal in the game. On the left, under **Your inventories**, select your location. Without it the field only says "Select location", and the place will be missing later.
2. Pick the tab **Buy** (the shop sells) or **Local market value** (the shop buys).
3. Stand squarely in front of the terminal and press **Print**. The game saves the image in the folder `StarCitizen\LIVE\screenshots`.
4. If the list is long, scroll down and take another screenshot. The page merges several images of the same terminal into one series.
5. Open the Screenshot Reader. Drop the images on **Drop screenshots here** or click **Choose images** or **Choose folder**.
6. Wait until the bar has finished. For the first image it briefly shows "Loading OCR …". After that, one image takes about 15 seconds.
7. Check the head of each series: are place and tab right? If there is a warning about the location, pick the shop under **Shop (star-head)**.
8. Go through the yellow rows. The **Notes** column says what is uncertain, for example "price unreadable" or "name uncertain". Open the image from the **Image** column if needed.
9. If a value is wrong, click into the cell and correct it. The row then shows "✓ edited".
10. If the values are right, click **✓** in the row or **✓ Confirm all open rows in this series**. If a row is not a commodity at all, remove it with **✕**.
11. When "still to check" shows 0, click **⬇ CSV** or **⬇ JSON**. If yellow rows are still open, the page asks first.
12. The file is called `auswertung.csv` or `auswertung.json`. The CSV is set up for Excel (semicolons, UTF-8). You can load the export into the Trade Planner (folder `eigene_daten/`).

### Tips

- Look at the terminal squarely. The page reads angled images less well, and often not the place at all.
- German and English game clients are recognised, other languages are not.
- An image with ✗ and "no terminal text found" usually does not show a trade terminal with the tabs Buy / Local market value.
- If a brand-new commodity is missing, the reference does not know it yet. Try **🔄 Load latest reference (GitHub)**.
- If the terminal shows prices per container (`/UNITS`), the page converts them to per SCU and notes the divisor in **Notes**.

## Tutorial: Windows OCR

Goal: you read the screenshots with the text recognition built into Windows. It reads a little more accurately than the recognition in the browser and works without internet.

1. Download the repository so that `Windows_OCR_lesen.bat`, `ocr_engine.ps1` and `SC_Screenshot_Auswerter.html` are in the same folder.
2. Collect your screenshots in one folder, for example a copy of `StarCitizen\LIVE\screenshots`.
3. In Explorer, drag the folder (or single images) onto `Windows_OCR_lesen.bat`.
4. A console window opens and reads the images. Wait for the message "Fertig" (done).
5. The file `ocr_words.json` now sits next to the screenshots. The Screenshot Reader opens by itself.
6. Drop `ocr_words.json` on **Drop screenshots here**. The file list shows ✓ and the number of images.
7. Check, correct and confirm the rows as in the tutorial "Price list from images" (steps 7 to 10).
8. Download the result with **⬇ CSV** or **⬇ JSON**.

### Tips

- The Windows OCR prefers German, otherwise the language of your Windows profile, otherwise English.
- In this variant the file name in the **Image** column is not a link. Open the screenshot yourself in Explorer to compare.
- If the window reports an error, the cause is shown right above it.

## FAQ

### Is anything uploaded?

No. The screenshots stay on your computer. The page only loads the OCR engine from the internet and, when you press the button, the reference from GitHub Pages.

### Why is a row yellow?

The page is not sure about name, price or stock, or the price is far from the last star-head value. The reason is in **Notes**. The page does not silently guess, it marks.

### What does "new for this shop" mean?

The commodity was not yet in the star-head data of this shop. It is a note, not an error.

### Why is the "Stock SCU" column missing?

On the **Local market value** tab the shop buys. There the terminal shows no stock.

### What is in the export file?

Per row: system, place, shop, location in the image, type (buy or sell from your point of view), commodity, price, stock, status, time, image, confidence and notes. Confidence is `ok`, `bestaetigt` (confirmed), `korrigiert` (corrected) or `pruefen` (to check).

### The page asks for four corners. What now?

The image is angled. Click the corners of the right panel with the tabs: top-left, top-right, bottom-right, bottom-left. Then **Straighten and read**. The corners are reused for the following images of the same size as long as they fit.
