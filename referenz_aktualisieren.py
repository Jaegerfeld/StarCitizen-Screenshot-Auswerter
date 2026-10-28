"""Referenzdaten für den Auswerter aus der data.json des SC Handels-Planers ziehen.

Die Handels-Planer-Seite wird täglich aus star-head.de gebaut; ihre data.json enthält alle Waren,
Shops (mit Ort und System) und die letzten bekannten Preise. Daraus entsteht referenz.json:
  waren   – Warennamen (für den Namensabgleich der OCR)
  shops   – Shop, Ort, System (für die Standort-Zuordnung)
  angebot – je Shop und Art (Kauf/Verkauf) die bekannten Waren mit Preis (Plausibilität, Shop-Wahl)

Start:  python referenz_aktualisieren.py            (lädt von GitHub Pages)
        python referenz_aktualisieren.py pfad/data.json   (lokale Datei)
"""
import json
import pathlib
import sys
import urllib.request

URL = "https://jaegerfeld.github.io/StarCitizen-Handels-Planer/data.json"
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "referenz.json"
ART = {0: "Kauf", 1: "Verkauf"}


def build(d):
    wares = [w["w"] for w in d["wares"]]
    shops, angebot = {}, {}
    for row in d["rows"]:
        idx, art, preis, shop, ort, system, _inv, _cont, stand = row[:9]   # ab Handels-Planer 1.3 folgt ein 10. Feld (Quelle)
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
