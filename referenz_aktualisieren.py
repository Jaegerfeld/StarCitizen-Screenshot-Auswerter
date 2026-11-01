# =============================================================================
# Autor:          Robert Seebauer
# Repository:     https://github.com/Jaegerfeld/StarCitizen-Screenshot-Auswerter
# KI-Unterstützung: Erstellt mit Unterstützung von Claude (Anthropic)
# Erstellt:       28.10.2026
# Geändert:       28.10.2026
# Lizenz:         BSD-3-Clause (siehe LICENSE)
#
# Fachliche Funktion:
#   Zieht die Referenzdaten des Auswerters aus der data.json des SC
#   Handels-Planers (GitHub Pages, täglich aus star-head.de gebaut) oder aus
#   einer lokalen Datei und schreibt sie kompakt als referenz.json:
#     waren   – Warennamen für den unscharfen Namensabgleich der OCR,
#     shops   – Shop, Ort und System für die Standort- und Shop-Zuordnung,
#     angebot – je Shop und Art (Kauf/Verkauf) die bekannten Waren mit letztem
#               Preis und Stand; dient der Plausibilitätsprüfung der gelesenen
#               Preise (Vorziffer-Falle, /UNITS-Preise) und der Shop-Wahl.
#   Die Seite selbst baut dieselbe Struktur beim Nachladen im Browser
#   (buildRef in auswerter_app.html); beide müssen gleich bleiben.
# =============================================================================
"""Pull the reference data for the reader from the SC Handels-Planer's data.json.

The Handels-Planer page is built daily from star-head.de; its data.json holds all commodities,
shops (with place and system) and the last known prices. This produces referenz.json:
  waren   – commodity names (for matching OCR names)
  shops   – shop, place, system (for assigning the location)
  angebot – per shop and kind (Kauf/Verkauf) the known commodities with price (plausibility,
            shop choice)

Start:  python referenz_aktualisieren.py                  (loads from GitHub Pages)
        python referenz_aktualisieren.py path/data.json   (local file)
"""
import json
import pathlib
import sys
import urllib.request

#: Published data.json of the Handels-Planer (GitHub Pages).
URL = "https://jaegerfeld.github.io/StarCitizen-Handels-Planer/data.json"
#: Folder of this script; referenz.json is written next to it.
HERE = pathlib.Path(__file__).resolve().parent
#: Output file that auswerter_bauen.py embeds into the page.
OUT = HERE / "referenz.json"
#: Maps the data.json trade kind (0 = shop sells, 1 = shop buys) to the reader's labels.
ART = {0: "Kauf", 1: "Verkauf"}


def build(d):
    """Turn a Handels-Planer data.json object into the reader's reference structure.

    Args:
        d: Parsed data.json with ``wares`` (list of ``{"w": name}``) and ``rows``
            (``[ware index, kind, price, shop, place, system, inventory, container, as of, …]``).

    Returns:
        Reference dict with schema ``sc-auswerter-referenz/1`` and the keys ``quelle``,
        ``stand``, ``patch``, ``waren``, ``shops`` (sorted) and ``angebot``
        (``{"shop|place": {kind: {ware: [price, as of]}}}``).

    Raises:
        KeyError: If ``wares``/``rows`` are missing or a row has an unknown kind.
    """
    wares = [w["w"] for w in d["wares"]]
    shops, angebot = {}, {}
    for row in d["rows"]:
        idx, art, preis, shop, ort, system, _inv, _cont, stand = row[:9]   # from Handels-Planer 1.3 on a 10th field (source) follows
        shops[(shop, ort)] = system
        angebot.setdefault(f"{shop}|{ort}", {}).setdefault(ART[art], {})[wares[idx]] = [preis, stand]
    return {
        "schema": "sc-auswerter-referenz/1",
        "quelle": d.get("source", "star-head.de"),
        "stand": d.get("generated", ""),
        "patch": d.get("patch", ""),
        "waren": wares,
        "shops": [{"shop": s, "ort": o, "system": sy} for (s, o), sy in sorted(shops.items())],
        "angebot": angebot,
    }


def main(argv=None):
    """Load data.json (local path or GitHub Pages) and write referenz.json.

    Args:
        argv: Arguments without the program name; an optional first entry is the path of a
            local data.json. ``None`` reads ``sys.argv``.

    Raises:
        urllib.error.URLError: If GitHub Pages cannot be reached.
        OSError: If the local file cannot be read or referenz.json not written.
        json.JSONDecodeError: If the data is not valid JSON.
        KeyError: If the data lacks the expected fields (see ``build``).
    """
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        raw = pathlib.Path(argv[0]).read_text(encoding="utf-8")
    else:
        req = urllib.request.Request(URL, headers={"User-Agent": "SC-Screenshot-Auswerter"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
    ref = build(json.loads(raw))
    OUT.write_text(json.dumps(ref, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"referenz.json: {len(ref['waren'])} Waren, {len(ref['shops'])} Shops, Stand {ref['stand']}")


if __name__ == "__main__":
    main()
