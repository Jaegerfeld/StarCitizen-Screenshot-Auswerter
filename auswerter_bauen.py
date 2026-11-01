# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       28.10.2026
# Geändert:       01.11.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Baut die auslieferbare Einzeldatei SC_Screenshot_Auswerter.html. Grundlage
#   ist die Vorlage auswerter_app.html (OCR-Pipeline und Parser im Browser); in
#   sie werden die gemeinsame Kopfzeile, der „Was ist neu?“-Dialog und der
#   Changelog (kopfzeile.py), das gemeinsame Design (sc_design.py), die
#   Versionsnummer (version.py) und die Referenzdaten (referenz.json: Waren,
#   Shops, letzte Preise aus der data.json des Handels-Planers) eingesetzt.
#
#   Die Referenz ist fest eingebettet, damit die Seite ohne Server und offline
#   arbeitet; die Seite kann sie bei Bedarf selbst von GitHub Pages
#   nachladen. Mit --referenz wird referenz.json vor dem Bau frisch gezogen
#   (referenz_aktualisieren.py). Bewusst nur Standardbibliothek.
# =============================================================================
"""Build SC_Screenshot_Auswerter.html: the app template (auswerter_app.html) with the reference
data (referenz.json: commodities, shops, last prices from the Handels-Planer's data.json) embedded.

Start:  python auswerter_bauen.py            (uses referenz.json as it is)
        python auswerter_bauen.py --referenz (first pulls a fresh reference from GitHub Pages)
"""
import json
import pathlib
import sys

import kopfzeile as kz
import sc_design as sd
from version import VERSION

#: Folder of this script; all inputs and the output live next to it.
HERE = pathlib.Path(__file__).resolve().parent
#: Page template with the OCR pipeline, parser and build placeholders.
TEMPLATE = HERE / "auswerter_app.html"
#: Reference data embedded into the page (see referenz_aktualisieren.py).
REF = HERE / "referenz.json"
#: Built single-file page that users open in the browser.
OUT = HERE / "SC_Screenshot_Auswerter.html"



def fill_header(html):
    """Insert the shared header, the "What's new?" dialog and the changelog.

    Replaces the header, CSS, JS, font and dialog placeholders of the template with the
    shared building blocks from kopfzeile.py and sc_design.py. The header gets an extra
    button that reloads the reference from the Handels-Planer on GitHub Pages.

    Args:
        html: Template text of auswerter_app.html.

    Returns:
        The template text with all shared header/design placeholders filled in.
    """
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
    """Build the page and write SC_Screenshot_Auswerter.html.

    Args:
        argv: Command-line arguments without the program name; ``--referenz`` refreshes
            referenz.json from GitHub Pages before building.

    Returns:
        Process exit code (0 on success).

    Raises:
        OSError: If the template or referenz.json cannot be read or the output not written.
        json.JSONDecodeError: If referenz.json is not valid JSON.
        KeyError: If referenz.json lacks the ``waren`` or ``shops`` list.
    """
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
