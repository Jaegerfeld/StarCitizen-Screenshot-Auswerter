"""Baut SC_Screenshot_Auswerter.html: die App-Vorlage (auswerter_app.html) mit eingebetteter
Referenz (referenz.json: Waren, Shops, letzte Preise aus der data.json des Handels-Planers).

Start:  python auswerter_bauen.py            (nutzt referenz.json wie vorhanden)
        python auswerter_bauen.py --referenz (zieht vorher die Referenz frisch von GitHub Pages)
"""
import json
import pathlib
import sys

from version import VERSION

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATE = HERE / "auswerter_app.html"
REF = HERE / "referenz.json"
OUT = HERE / "SC_Screenshot_Auswerter.html"


def main(argv):
    if "--referenz" in argv:
        import referenz_aktualisieren
        referenz_aktualisieren.main([])
    ref = json.loads(REF.read_text(encoding="utf-8"))
    payload = json.dumps(ref, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__REF__*/{}", payload).replace("{{VERSION}}", VERSION)
    OUT.write_text(html, encoding="utf-8")
    print(f"Geschrieben: {OUT.name} ({OUT.stat().st_size // 1024} KB) – Referenz {ref.get('stand', '')}, "
          f"{len(ref['waren'])} Waren, {len(ref['shops'])} Shops")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
