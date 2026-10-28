"""SC Screenshot-Auswerter – liest Handelskonsolen-Screenshots (Star Citizen, deutscher Client)
per Windows-OCR und erzeugt eine Prüftabelle (HTML) sowie JSON/CSV zum Weitergeben.

Ablauf:
  1. ocr_engine.ps1 liest jedes Bild in drei Ausschnitten (links: Standort; rechts: Waren, zweimal)
     und misst die Helligkeit hinter den Reiter-Beschriftungen (der aktive Reiter ist hell).
  2. Zeilen rekonstruieren, Reiter bestimmen (KAUFEN = Shop verkauft, mit Bestand; LOKALER MARKTWERT =
     Shop kauft), Waren mit Preis/Bestand/Status herausziehen.
  3. Namen gegen die star-head-Warenliste abgleichen, Standort gegen die Shop-Liste, Preise gegen den
     letzten bekannten Preis plausibilisieren. Zweifel werden markiert, nicht verschwiegen.
  4. Gleiche Serie (Standort + Reiter) über mehrere Scroll-Screenshots zusammenführen.
  5. auswertung.html (Prüftabelle, editierbar, Download-Knöpfe), auswertung.json, auswertung.csv.

Start:  python auswerter.py <Ordner oder Bilder...> [--out ORDNER] [--words vorhandene_words.json]
"""
import argparse
import csv
import datetime as dt
import difflib
import json
import pathlib
import re
import subprocess
import sys

from version import VERSION

HERE = pathlib.Path(__file__).resolve().parent
ENGINE = HERE / "ocr_engine.ps1"
REF = HERE / "referenz.json"
TEMPLATE_FILE = HERE / "pruefseite.html"
SCHEMA = "sc-konsole-export/1"

# ---- Texte der Konsole (deutscher Client) ----
HEADERS = {
    "AUF LAGER": "lager", "NICHT VORRÄTIG": "nicht_vorraetig",
    "VERKAUFBARE FRACHT": "eigene_fracht", "NACHGEFRAGT": "nachgefragt", "KEINE NACHFRAGE": "keine_nachfrage",
    "KANN NICHT VERKAUFT WERDEN": "unverkaeuflich",
}
IGNORE = ["HANDELSWAREN", "INVENTAR", "KAUFEN", "LOKALER MARKTWERT", "KAUFEN LOKALER MARKTWERT",
          "VERFÜGBARE CONTAINERGRÖSSE (SCU)", "VERFÜGBARE CONTAINERGRÖSSE", "AKTUELLER KONTOSTAND:", "AUEC",
          "DEINE INVENTARE", "DER SHOP KAUFT GEGENSTÄNDE DIESER GRÖSSE ODER KLEINER:",
          "BITTE EIN GÜLTIGES INVENTAR AUSWÄHLEN,", "UM DIE TRANSAKTION DURCHZUFÜHREN."]
STATUS = ["AUSVERKAUFT", "SEHR NIEDRIGE BESTÄNDE", "NIEDRIGE BESTÄNDE", "MITTLERE BESTÄNDE", "HOHE BESTÄNDE",
          "SEHR HOHE BESTÄNDE", "MAXIMALE BESTÄNDE", "KEINE NACHFRAGE", "NIEDRIGE NACHFRAGE", "MITTLERE NACHFRAGE",
          "HOHE NACHFRAGE", "SEHR HOHE NACHFRAGE"]
NO_LOCATION = ["STANDORT WÄHLEN", "WÄHLE EINE UNTERKATEGORIE"]
KAUF_SECTIONS = {"lager", "nicht_vorraetig"}
DIGITS = "0-9OoIlS"
PRICE_RE = re.compile(rf"[¤n]?\s*([{DIGITS}][{DIGITS} .,]*)\s*/\s*[S5]?[CcGg]?[UuJj]?")
SCU_TAIL_RE = re.compile(rf"([{DIGITS}][{DIGITS} .,]*)\s*[S5][CG][UJ]\s*$", re.I)
PREFIX_RE = re.compile(rf"^[¤n]?\s*[{DIGITS}]{{1,3}}\s*[,.]?\s*$")       # einsames "¤ 10," vor "232/SCU"
TAIL_PREFIX_RE = re.compile(rf"[¤n]\s*[{DIGITS}]{{1,3}}\s*[,.]?\s*$")
DIGIT_FIX = str.maketrans({"O": "0", "o": "0", "I": "1", "l": "1", "S": "5"})


def norm(s):
    s = s.upper().replace("ß", "SS").replace("ẞ", "SS")
    s = re.sub(r"[^A-Z0-9ÄÖÜ&'\- ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def ratio(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def best(text, candidates, cutoff):
    """Bester Kandidat (Original-Schreibweise) und Ähnlichkeit; None unter cutoff."""
    n = norm(text)
    if not n:
        return None, 0.0
    top, score = None, 0.0
    for c in candidates:
        r = difflib.SequenceMatcher(None, n, norm(c)).ratio()
        if r > score:
            top, score = c, r
    return (top, score) if score >= cutoff else (None, score)


def to_int(s):
    digits = re.sub(r"[^0-9]", "", s.translate(DIGIT_FIX))
    return int(digits) if digits else None


# ---- Zeilen aus Wortboxen ----
def lines_of(words):
    lines = []
    for w in sorted(words, key=lambda w: (w["y"], w["x"])):
        for ln in lines:
            if abs(ln["y"] - w["y"]) < max(w["h"], 8) * 0.6:
                ln["w"].append(w)
                break
        else:
            lines.append({"y": w["y"], "h": w["h"], "w": [w]})
    out = []
    for ln in sorted(lines, key=lambda ln: ln["y"]):
        ws = sorted(ln["w"], key=lambda w: w["x"])
        out.append({"y": ln["y"], "h": ln["h"], "text": " ".join(w["text"] for w in ws), "x": ws[0]["x"]})
    # Zerrissene Preise wieder zusammensetzen: "¤ 10," (eigene Zeile) + "232/SCU"
    merged = []
    for ln in out:
        prev = merged[-1] if merged else None
        if prev and "/" in ln["text"] and ln["y"] - prev["y"] < prev["h"] * 1.6 and \
                (PREFIX_RE.match(prev["text"]) or TAIL_PREFIX_RE.search(prev["text"])):
            prev["text"] = prev["text"].rstrip() + " " + ln["text"].lstrip()
            continue
        merged.append(ln)
    return merged


# ---- Standort (linkes Panel) ----
def parse_location(words):
    texts = [ln["text"] for ln in lines_of(words)]
    start = next((i for i, t in enumerate(texts) if ratio(t, "DEINE INVENTARE") >= 0.75), None)
    if start is None:
        return None, "Panel „Deine Inventare“ nicht gefunden"
    for t in texts[start + 1:start + 4]:
        if any(ratio(t, h) >= 0.75 for h in ("NACHGEFRAGT", "KEINE NACHFRAGE", "KANN NICHT VERKAUFT WERDEN")):
            break
        if any(ratio(t, n) >= 0.7 for n in NO_LOCATION):
            return None, "Standort nicht gewählt (Feld „Standort wählen“ leer)"
        if len(norm(t)) >= 3:
            return t, ""
    return None, "Standort nicht lesbar"


# ---- Waren (rechtes Panel) ----
def classify(text):
    h, _ = best(text, list(HEADERS), 0.78)
    if h:
        return "header", HEADERS[h]
    n = norm(text)
    if ratio(text, "BESTAND") >= 0.8:
        return "bestand", None
    if any(ratio(text, i) >= 0.8 for i in IGNORE) or "CONTAINER" in n or "GEGENST" in n:
        return "ignore", None
    st, _ = best(text, STATUS, 0.72)
    if st:
        return "status", st
    m = SCU_TAIL_RE.search(text)
    if m and len(norm(text[:m.start()])) < 3:
        return "scu", to_int(m.group(1))
    m = PRICE_RE.search(text)
    if m and "/" in text:
        return "price", to_int(m.group(1))
    return "text", text


def looks_like_garbage(roh):
    n = norm(roh)
    letters = re.sub(r"[^A-Z]", "", n)
    return len(letters) < 5 or re.search(r"\bS?CU\b|^\W", n) is not None


def parse_items(words, wares):
    """Waren-Einträge einer OCR-Lesung des rechten Panels; dazu, ob die Kauf-Beschriftung BESTAND vorkam."""
    items, section, cur, bestand_seen = [], None, None, False
    for ln in lines_of(words):
        text = ln["text"]
        kind, val = classify(text)
        if kind == "header":
            section, cur = val, None
        elif kind == "bestand":
            bestand_seen = True
        elif kind == "ignore":
            pass
        elif kind == "status" and cur:
            cur["status"] = val
        elif kind == "price" and cur and val is not None:
            cur["preis"] = val
        elif kind == "scu" and cur:
            cur["scu"] = val
        elif kind == "text":
            t = re.sub(r"\bBESTAND\b", " ", text, flags=re.I)
            if re.search(r"\bBESTAND\b", text, re.I):
                bestand_seen = True
            m = SCU_TAIL_RE.search(t)
            scu = to_int(m.group(1)) if m else None
            name_part = (t[:m.start()] if m else t).strip()
            name, score = best(name_part, wares, 0.6)
            if not name and " " in name_part:                       # Icon-Müll vorne abschneiden
                name, score = best(name_part.split(" ", 1)[1], wares, 0.6)
            if not name and len(norm(name_part)) >= 4:
                name, score = best(norm(name_part)[1:], wares, 0.6)
            if not name and looks_like_garbage(name_part):
                continue
            cur = {"ware": name, "roh": name_part, "score": round(score, 2), "section": section,
                   "preis": None, "scu": scu, "status": ""}
            items.append(cur)
    return [i for i in items if i["ware"] or i["preis"]], bestand_seen


def pick_number(a, b, notes, label):
    """Zwei Lesungen einer Zahl vereinen: Null oder abgeschnittene Ziffern verlieren, echter Widerspruch wird notiert."""
    if a is None or b is None or a == b:
        return a if a is not None else b
    if a == 0 or b == 0:
        return a or b
    sa, sb = str(a), str(b)
    if sa.endswith(sb) or sb.endswith(sa):
        return max(a, b)
    notes.append(f"{label}: zwei Lesungen ({a:,} / {b:,}) – bitte prüfen".replace(",", "."))
    return a


def merge_items(dest, items, art, label_a="", label_b=""):
    """Einträge (einer zweiten Lesung oder eines weiteren Bildes) in dest einarbeiten."""
    for it in items:
        key = it["ware"] or it["roh"]
        if key not in dest:
            dest[key] = dict(it, hinweise=list(it.get("hinweise", [])))
            continue
        o = dest[key]
        o["preis"] = pick_number(o["preis"], it["preis"], o["hinweise"], "Preis")
        if art == "Kauf":
            o["scu"] = pick_number(o["scu"], it["scu"], o["hinweise"], "Bestand")
        o["status"] = o["status"] or it["status"]
        o["section"] = o["section"] or it["section"]
        if it["score"] > o["score"]:
            o["roh"], o["score"] = it["roh"], it["score"]
        o["hinweise"] = sorted(set(o["hinweise"] + it.get("hinweise", [])))
    return dest


def decide_art(page, items, bestand_seen, prev_art):
    tabs = page.get("tabs") or {}
    k, m = tabs.get("kaufen"), tabs.get("markt")
    if k is not None and m is not None and abs(k - m) > max(k, m) * 0.15:
        return "Kauf" if k > m else "Verkauf", "Reiter"
    secs = {i["section"] for i in items if i["section"]}
    if secs & KAUF_SECTIONS:
        return "Kauf", "Abschnitt"
    if secs:
        return "Verkauf", "Abschnitt"
    if bestand_seen:
        return "Kauf", "Bestand"
    if prev_art:
        return prev_art, "Vorbild"
    return "?", ""


# ---- Shop-Zuordnung ----
def match_ort(ref, location):
    if not location:
        return None, 0.0
    orte = sorted({s["ort"] for s in ref["shops"]} | {s["shop"] for s in ref["shops"]})
    return best(location, orte, 0.7)


def match_shop(ref, ort, art, wares_seen):
    """Kandidaten-Shops am Ort; Vorschlag = größte Überschneidung mit den erkannten Waren."""
    if not ort:
        return None, []
    cands = [s for s in ref["shops"] if s["ort"] == ort or s["shop"] == ort]
    ranked = []
    for s in cands:
        known = ref["angebot"].get(f"{s['shop']}|{s['ort']}", {}).get(art, {})
        ranked.append((len(set(known) & set(wares_seen)), len(known) > 0, s))
    ranked.sort(key=lambda r: (-r[0], -int(r[1]), r[2]["shop"]))
    return (ranked[0][2] if ranked else None), [r[2] for r in ranked]


# ---- Zeitstempel ----
STAMP_RE = re.compile(r"ScreenShot-(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})-(\d{2})", re.I)


def stamp_of(page):
    m = STAMP_RE.search(page["file"])
    if m:
        return f"{m.group(1)}T{m.group(2)}:{m.group(3)}:{m.group(4)}"
    return page.get("mtime", "")[:19]


# ---- Auswertung ----
def evaluate(ocr, ref):
    wares = ref["waren"]
    series, prev = {}, {}
    for page in sorted(ocr["pages"], key=lambda p: p["file"]):
        v = {x["tag"]: x["words"] for x in page["variants"]}
        location, loc_note = parse_location(v.get("L", []))
        ort, _ = match_ort(ref, location)
        items_a, b1 = parse_items(v.get("R", []), wares)
        items_b, b2 = parse_items(v.get("RB", []), wares)
        art, art_quelle = decide_art(page, items_a + items_b, b1 or b2, prev.get(ort or location))
        merged = merge_items(merge_items({}, items_a, art), items_b, art)
        key = (ort or location or "?", art)
        s = series.setdefault(key, {"standort": location, "ort": ort, "standort_hinweis": loc_note, "art": art,
                                    "art_quelle": art_quelle, "bilder": [], "items": {}})
        if location and (not s["standort"] or (ort and ratio(location, ort) > ratio(s["standort"], ort))):
            s["standort"] = location
        if s["standort_hinweis"] and not loc_note:
            s["standort_hinweis"] = ""
        s["bilder"].append({"datei": page["file"], "pfad": page["path"], "stand": stamp_of(page), "n": len(merged)})
        for it in merged.values():
            it["bild"], it["stand"] = page["file"], stamp_of(page)
        merge_items(s["items"], merged.values(), art)
        if ort or location:
            prev[ort or location] = art if art != "?" else prev.get(ort or location)
    out = []
    for (_loc, art), s in series.items():
        seen = [k for k, i in s["items"].items() if i["ware"]]
        shop, cands = match_shop(ref, s["ort"], art, seen)
        known = ref["angebot"].get(f"{shop['shop']}|{shop['ort']}", {}).get(art, {}) if shop else {}
        rows = []
        for it in s["items"].values():
            notes, info = list(it["hinweise"]), []
            if not it["ware"]:
                notes.append(f"Ware nicht erkannt (gelesen: „{it['roh']}“)")
            elif it["score"] < 0.85:
                notes.append(f"Name unsicher (gelesen: „{it['roh']}“)")
            if it["preis"] is None:
                notes.append("Preis nicht lesbar")
            elif it["ware"] in known:
                refp = known[it["ware"]][0]
                if refp and not (0.5 <= it["preis"] / refp <= 2.0):
                    notes.append(f"Preis weicht stark vom letzten star-head-Wert ab ({refp:,.0f})".replace(",", "."))
            elif shop and it["ware"]:
                info.append("neu für diesen Shop")
            if art == "Kauf" and it["scu"] is None:
                notes.append("Bestand nicht lesbar")
            rows.append({"ware": it["ware"] or "", "roh": it["roh"], "art": art, "preis": it["preis"],
                         "bestand_scu": it["scu"] if art == "Kauf" else None, "status": it["status"].title(),
                         "abschnitt": it["section"] or "", "bild": it["bild"], "stand": it["stand"],
                         "konfidenz": "pruefen" if notes else "ok", "hinweise": notes + info})
        rows.sort(key=lambda r: (r["konfidenz"] != "pruefen", r["ware"] or r["roh"]))
        out.append({"standort": s["standort"], "ort": s["ort"], "standort_hinweis": s["standort_hinweis"],
                    "art": art, "art_quelle": s["art_quelle"], "shop": shop, "shop_kandidaten": cands,
                    "bilder": s["bilder"], "zeilen": rows})
    out.sort(key=lambda s: (s["ort"] or s["standort"] or "~", s["art"]))
    return out


# ---- Ausgabe ----
def export_rows(series):
    rows = []
    for s in series:
        shop = s["shop"] or {}
        for r in s["zeilen"]:
            rows.append({"system": shop.get("system", ""), "ort": shop.get("ort", s["ort"] or s["standort"] or ""),
                         "shop": shop.get("shop", ""), "standort_im_bild": s["standort"] or "", "art": r["art"],
                         "ware": r["ware"], "preis_auec_scu": r["preis"], "bestand_scu": r["bestand_scu"],
                         "status": r["status"], "stand": r["stand"], "bild": r["bild"], "konfidenz": r["konfidenz"],
                         "hinweise": "; ".join(r["hinweise"])})
    return rows


def write_outputs(series, out_dir, ref, ocr):
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = export_rows(series)
    meta = {"schema": SCHEMA, "generator": f"SC Screenshot-Auswerter {VERSION}",
            "generated": dt.datetime.now().isoformat(timespec="seconds"), "client": "de",
            "ocr": ocr.get("ocrLanguage", ""), "referenz_stand": ref.get("stand", ""), "patch": ref.get("patch", "")}
    (out_dir / "auswertung.json").write_text(json.dumps(dict(meta, eintraege=rows), ensure_ascii=False, indent=1),
                                             encoding="utf-8")
    with (out_dir / "auswertung.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["ware"], delimiter=";")
        w.writeheader()
        w.writerows(rows)
    data = json.dumps({"meta": meta, "serien": series, "waren": ref["waren"], "shops": ref["shops"]}, ensure_ascii=False).replace("</", "<\\/")
    page = TEMPLATE_FILE.read_text(encoding="utf-8").replace("/*DATA*/", data).replace("{{VERSION}}", VERSION)
    (out_dir / "auswertung.html").write_text(page, encoding="utf-8")
    return rows


# ---- Hauptprogramm ----
def run_ocr(images, words_out):
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ENGINE),
           "-Images", ",".join(str(p) for p in images), "-Out", str(words_out)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(f"OCR fehlgeschlagen (Code {r.returncode})")


def collect_images(args):
    imgs = []
    for a in args:
        p = pathlib.Path(a)
        if p.is_dir():
            imgs += sorted(x for x in p.iterdir() if x.suffix.lower() in (".png", ".jpg", ".jpeg", ".bmp"))
        elif p.is_file():
            imgs.append(p)
    return imgs


def main(argv=None):
    ap = argparse.ArgumentParser(description="SC Screenshot-Auswerter")
    ap.add_argument("eingabe", nargs="+", help="Ordner oder Bilddateien")
    ap.add_argument("--out", help="Ausgabeordner (Standard: <Ordner>/Auswertung)")
    ap.add_argument("--words", help="vorhandene OCR-Wortdatei statt neuer OCR")
    a = ap.parse_args(argv)
    images = collect_images(a.eingabe)
    if not images and not a.words:
        raise SystemExit("Keine Bilder gefunden.")
    base = images[0].parent if images else pathlib.Path(a.words).parent
    out_dir = pathlib.Path(a.out) if a.out else base / "Auswertung"
    out_dir.mkdir(parents=True, exist_ok=True)
    words = pathlib.Path(a.words) if a.words else out_dir / "ocr_words.json"
    if not a.words:
        print(f"{len(images)} Bilder -> OCR ...")
        run_ocr(images, words)
    ocr = json.loads(words.read_text(encoding="utf-8-sig"))
    ref = json.loads(REF.read_text(encoding="utf-8"))
    series = evaluate(ocr, ref)
    rows = write_outputs(series, out_dir, ref, ocr)
    n_chk = sum(1 for r in rows if r["konfidenz"] == "pruefen")
    for s in series:
        shop = f"{s['shop']['shop']} ({s['shop']['ort']})" if s["shop"] else "?"
        print(f"  {s['ort'] or s['standort'] or '?'} · {s['art']} [{s['art_quelle']}]: {len(s['zeilen'])} Waren aus "
              f"{len(s['bilder'])} Bild(ern) -> Shop {shop}")
    print(f"Fertig: {len(rows)} Zeilen, {n_chk} zu prüfen -> {out_dir / 'auswertung.html'}")


if __name__ == "__main__":
    main()
