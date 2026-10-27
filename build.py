#!/usr/bin/env python3
"""Liest Aktuell, Programme und Shop von consciousunion.ch und erzeugt index.html aus template.html."""
import html, json, re, sys, urllib.request
from datetime import date
from pathlib import Path

BASE = "https://www.consciousunion.ch"
MONATE = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
HIER = Path(__file__).parent


def laden(pfad):
    req = urllib.request.Request(BASE + pfad, headers={"User-Agent": "Mozilla/5.0 (ConsciousUnionApp)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def zu_markdown(h):
    import html2text
    c = html2text.HTML2Text()
    c.body_width = 0
    c.ignore_images = True
    return re.sub(r'\\([\\`*_{}\[\]()#+\-.!])', r'\1', c.handle(h))


def bereich(md, titel):
    m = re.search(r'^##\s+' + re.escape(titel) + r'\s*$', md, re.M)
    if not m:
        return []
    rest = md[m.end():]
    e = re.search(r'^#\s+\S', rest, re.M)
    if e:
        rest = rest[:e.start()]
    return [b.strip() for b in re.split(r'^\s*\* \* \*\s*$', rest, flags=re.M) if b.strip()]


def sauber(t):
    return re.sub(r'!\[[^\]]*\]\([^)]*\)', '', t)


def link(b):
    m = re.findall(r'(?<!!)\[([^\]]+)\]\((https?://[^)\s]+)\)', b)
    return m[-1] if m else None


def ohne_link(b):
    return re.sub(r'(?<!!)\[[^\]]+\]\(https?://[^)]+\)', '', b)


def zeilen(t):
    return [re.sub(r'\s+', ' ', z.replace('**', '')).strip() for z in t.splitlines()]


def esc(s):
    return html.escape(s, quote=False)


def aktuell(md):
    out = []
    for b in bereich(md, "Aktuell"):
        b = sauber(b)
        l = link(b)
        m = re.search(r'^\*\*(.+?)\*\*\s*$', b, re.M)
        if not m or not l:
            continue
        teile = re.split(r'\s+-\s+', m.group(1).strip())
        titel, tag, mon, preis = teile[0], "", "", ""
        for t in teile[1:]:
            d = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{4})', t)
            if d:
                tag = d.group(1).zfill(2)
                mon = f"{MONATE[int(d.group(2)) - 1]} {d.group(3)}"
            else:
                preis = re.sub(r'EUR:?\s*', 'EUR ', t.strip())
        if preis.upper() == "KOSTENLOS":
            preis = "Kostenlos"
        ne = [z for z in zeilen(ohne_link(b[m.end():])) if z]
        tags = []
        while ne and len(ne[-1]) < 45 and not ne[-1].endswith(('.', '?', '!', ':')):
            tags.insert(0, ne.pop())
        out.append([tag or "•", mon, esc(titel), esc(preis), esc(" ".join(ne)), [esc(t) for t in tags], html.escape(l[1])])
    return out


def programme(md):
    out = []
    for b in bereich(md, "Unsere Programme"):
        b = sauber(b)
        l = link(b)
        m = re.search(r'\*\*(.+?)\*\*', b)
        if not m or not l:
            continue
        zl = [z for z in zeilen(ohne_link(b[m.end():])) if z]
        meta = []
        while zl and re.match(r'(Start|Für )', zl[0]) and len(zl[0]) < 70:
            meta.append(zl.pop(0).rstrip('.'))
        out.append([esc(m.group(1).strip()), esc(" · ".join(meta)), esc(" ".join(zl)), html.escape(l[1]), esc(l[0])])
    return out


def shop(md):
    out = []
    for b in bereich(md, "Shop"):
        b = sauber(b)
        l = link(b)
        m = re.search(r'\*\*(.+?)\*\*', b)
        if not m or not l:
            continue
        titel = re.sub(r'^Kostenlos:\s*', '', m.group(1).strip())
        rest = ohne_link(b[m.end():])
        gratis = m.group(1).startswith("Kostenlos") or bool(re.search(r'\*\*Kostenlos\*\*', rest))
        preise = [int(p.rstrip(".'").replace('.', '').replace("'", '')) for p in re.findall(r"EUR\s*:?\s*(\d[\d.']*)", rest)]
        monat = bool(re.search(r'EUR\s*\d+[^*\n]*monatlich', rest))
        if preise:
            preis = ("ab " if len(set(preise)) > 1 else "") + f"EUR {min(preise)}" + (" / Monat" if monat else "")
        else:
            preis = "Kostenlos" if gratis else ""
        rest = re.sub(r'\*\*[^*]*(EUR|Kostenlos)[^*]*\*\*', '', rest)
        text = " ".join(z for z in zeilen(rest) if z)
        if len(text) > 260:
            text = text[:260].rsplit(' ', 1)[0] + "…"
        out.append([esc(titel), esc(preis), esc(text), html.escape(l[1]), esc(l[0])])
    return out


def js(x):
    return json.dumps(x, ensure_ascii=False).replace("</", "<\\/")


def rendern(E, P, S, stand):
    t = (HIER / "template.html").read_text(encoding="utf-8")
    return t.replace("__E__", js(E)).replace("__P__", js(P)).replace("__S__", js(S)).replace("{{STAND}}", stand)


def schreiben(E, P, S):
    ziel = HIER / "index.html"
    alt = ziel.read_text(encoding="utf-8") if ziel.exists() else ""
    m = re.search(r'Stand: (\d\d\.\d\d\.\d{4})', alt)
    neu = rendern(E, P, S, m.group(1) if m else "")
    if neu != alt:
        neu = rendern(E, P, S, date.today().strftime("%d.%m.%Y"))
        ziel.write_text(neu, encoding="utf-8")
        print("index.html aktualisiert")
    else:
        print("Keine Änderungen auf der Homepage")


def main():
    E = aktuell(zu_markdown(laden("/aktuell/")))
    P = programme(zu_markdown(laden("/programme/")))
    S = shop(zu_markdown(laden("/shop/")))
    if len(E) < 1 or len(P) < 4 or len(S) < 8:
        sys.exit(f"Abbruch: zu wenige Einträge gefunden (Aktuell {len(E)}, Programme {len(P)}, Shop {len(S)}). index.html bleibt unverändert.")
    schreiben(E, P, S)


if __name__ == "__main__":
    main()
