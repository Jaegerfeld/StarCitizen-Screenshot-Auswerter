"""Baut SC_Screenshot_Auswerter.html: die App-Vorlage (auswerter_app.html) mit eingebetteter
Referenz (referenz.json: Waren, Shops, letzte Preise aus der data.json des Handels-Planers).

Start:  python auswerter_bauen.py            (nutzt referenz.json wie vorhanden)
        python auswerter_bauen.py --referenz (zieht vorher die Referenz frisch von GitHub Pages)
"""
import json
import pathlib
import sys

import kopfzeile as kz
import sc_design as sd
from version import VERSION

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "auswerter_app.html"
REF = HERE / "referenz.json"
OUT = HERE / "SC_Screenshot_Auswerter.html"



def fill_header(html):
    """Gemeinsame Kopfzeile, „Was ist neu?“-Dialog und Changelog einsetzen (kopfzeile.py)."""
    refresh = ('<button class="btn fh-btn" id="refBtn" type="button" title="Referenz (Waren, Shops, Preise) '
               'vom Handels-Planer auf GitHub Pages laden">'
               f'🔄 {kz.bi("Neuesten Stand laden (GitHub)", "Load latest reference (GitHub)")}</button>')
    head = kz.header_html(
        "auswerter",
        eyebrow=("Star Citizen · Handelskonsolen · OCR", "Star Citizen · Trade terminals · OCR"),
        title=("SC Screenshot-Auswerter", "SC Screenshot Reader"),
        lede=("Screenshots der Handelskonsole hineinziehen – die Seite liest Ort, Reiter, Waren, Preise und "
              "Bestände im Browser, du prüfst die Tabelle und lädst JSON oder CSV herunter. Nichts verlässt "
              "deinen Rechner.",
              "Drop screenshots of the trade terminal – the page reads place, tab, commodities, prices and "
              "stock in your browser; you check the table and download JSON or CSV. Nothing leaves your "
              "computer."),
        version=VERSION, refresh=refresh, data='<span id="refStat"></span>')
    html = html.replace("<!--FH_HEADER-->", head)
    html = html.replace("/*FH_CSS*/", kz.CSS + sd.CSS).replace("/*FH_JS*/", kz.JS + sd.JS)
    html = html.replace("<!--SD_FONTS-->", sd.FONTS)
    return html.replace("<!--FH_DIALOG-->", kz.dialog_html("auswerter", VERSION) + "\n"
                        + kz.changelog_script(HERE / "CHANGELOG.md"))


def main(argv):
    if "--referenz" in argv:
        import referenz_aktualisieren
        referenz_aktualisieren.main([])
    ref = json.loads(REF.read_text(encoding="utf-8"))
    payload = json.dumps(ref, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = fill_header(TEMPLATE.read_text(encoding="utf-8")).replace("/*__REF__*/{}", payload).replace("{{VERSION}}", VERSION)
    OUT.write_text(html, encoding="utf-8")
    print(f"Geschrieben: {OUT.name} ({OUT.stat().st_size // 1024} KB) – Referenz {ref.get('stand', '')}, "
          f"{len(ref['waren'])} Waren, {len(ref['shops'])} Shops")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
