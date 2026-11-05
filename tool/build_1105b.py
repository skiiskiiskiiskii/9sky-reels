#!/usr/bin/env python3
"""2026-11-05 (evening): 5 experimental rose x Louboutin reels (Kirill: something new, new lines, slightly
changed video tracks). New moves, still no strobe / flashes / punch-ins:
N1, N2 - keep_red: the whole hook in grey, only the red (rose, sole) keeps its colour
N3     - reversed order: shoes + a short red-sole flash first, the rose closes the hook
N4     - three shots on the mr popular beats: rose -> hand with nails -> red sole
N5     - slow and dreamy (0.85x), the line comes in at 1.0 s instead of at the start"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP, P

G = "/mnt/user-data/uploads/flowers hooks/"
GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU, DROP = 60 / 99.0, 60 / 123.05, 3.13


def rose(name, dur=None, start=0.0, speed=1.0, flip=False, **kw):
    d = dict(type="clip", src=G + name + ".mp4", start=start, align_red=False, speed=speed, zoom=1.0,
             crop_x=0.5, flip=flip, grade={})
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def lb(key, start=None, dur=None, speed=1.0, flip=False, crop_x=0.5, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=1.035, crop_x=crop_x, flip=flip, grade=GR)
    if start is None:
        d.update(align_red=True, lead=lead)
    else:
        d.update(start=start, align_red=False)
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def t(text, y=0.56, frm=0):
    return [{"text": text, "from": frm, "to": "drop", "y": y, "size": 96, "scrim": 0.45, "font": "cg-italic"}]


KNIT = "BLACK KNIT"
QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
ZHB = [("XWF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME)), ("ZPF", cat(3, "BLACK  ·  WHITE"))]
SW = [("SWF", cat(1, KNIT)), ("KF", cat(2, COLLAR)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]
QF, QKF, ZFIN, SFIN = ("PF", "PB"), ("KF", "KB"), ("ZPF", "ZPB"), ("SPF", "SPB")
MP, AU = "mrpopular", "aura"

c2, c3a = DROP - 2 * BMP, DROP - 3 * BAU          # cut points on the beat
c4 = DROP - 4 * BMP

R = [  # key, track, hook segments, texts, pages, page beats, finale
    ("N01_only-red-stays", MP,
     [rose("g3", c2, speed=1.1, keep_red=True), lb("COUPLE", speed=1.05, keep_red=True)],
     t("only red stays."), QW1, 1, QF),
    ("N02_everything-else-grey", AU,
     [rose("g1", c3a, start=0.3, keep_red=True), lb("NAILS", start=5.98 - (DROP - c3a) * 1.35, speed=1.35, keep_red=True)],
     t("everything else is grey."), QK, 2, QKF),
    ("N03_rose-for-her", MP,                       # shoes, the sole flashes ~0.3 s before the cut, then the rose
     [lb("COUPLE", start=4.7 + 0.3 * 1.1 - c2 * 1.1, dur=c2, speed=1.1), rose("g2", start=0.4, speed=1.1)],
     t("rose for her.\ncollar for him."), ZHB, 1, ZFIN),
    ("N04_red-first", MP,
     [rose("g2", c4, start=0.2, speed=1.15), lb("NAILS", start=2.0, dur=c2 - c4, speed=1.1, flip=True),
      lb("COUPLE", speed=1.1, flip=True)],
     t("you'll notice the red first."), QW2, 1, QF),
    ("N05_worth-the-wait", AU,
     [rose("g1", c3a, start=0.2, speed=0.85, flip=True), lb("SOLES", start=4.3 - (DROP - c3a - 0.42) * 0.85, speed=0.85)],
     t("worth the wait.", frm=1.0), SW, 2, SFIN),
]
for i, (k, track, hook, texts, pg, pb, fin) in enumerate(R):
    tag = f"w{i + 1:02d}"
    spec = dict(seed=20000 + i, track=track, segments=hook + pages(pg, None, tag, pb) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=texts)
    json.dump(spec, open(os.path.join(SP, f"w1105_{k}.json"), "w"), indent=1)
    print(f"w1105_{k}")
