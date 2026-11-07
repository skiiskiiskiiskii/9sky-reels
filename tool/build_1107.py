#!/usr/bin/env python3
"""2026-11-07: 5 reels with a refreshed look (Kirill 11-07: some reels were refused by Instagram as duplicates).
- Mockup pages: same black catalogue, now lit like a vitrine (vitrine.py) - warm charcoal or oxblood glow behind
  the garment, so black pieces read; lighter halo. No grain, no zoom on mockups.
- On-screen lines: new content. Each one sets up a small story that only the cut to the collar finishes.
- Hooks: new framings so the frames differ from earlier reels - tighter crops on the shoes, and a smooth slow-down
  (motion-interpolated) right as the red sole appears. Still no strobe / flashes / punch-ins.
3 of 5 on mr popular."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, IX, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked

G = "/mnt/user-data/uploads/flowers hooks/"
GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU, DROP = 60 / 99.0, 60 / 123.05, 3.13
C2, C4 = DROP - 2 * BMP, DROP - 4 * BMP
MP, AU = "mrpopular", "aura"
NUMS = ["I", "II", "III", "IV"]


def lb(key, start=None, dur=None, speed=1.0, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.035, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def ramp(key, onset, flip=False, slow=0.55, rate=0.5, pre=1.0, **kw):
    """normal speed, then a smooth slow-down for the last `slow` s; the red appears inside the slow part"""
    s_end = onset + 0.13                                   # source time at the drop
    s_slow = s_end - slow * rate
    first = DROP - slow
    return [lb(key, start=s_slow - first * pre, dur=first, speed=pre, flip=flip, **kw),
            lb(key, start=s_slow, speed=rate, flip=flip, smooth=True, **kw)]


def soles(speed=0.95, tail=DROP, dur=None, **kw):
    return lb("SOLES", start=4.3 - (tail - 0.42) * speed, speed=speed, dur=dur, **kw)


def rose(name, dur, start=0.0, speed=1.15, flip=False):
    return dict(type="clip", src=G + name + ".mp4", start=start, dur=dur, align_red=False, speed=speed,
                zoom=1.0, crop_x=0.5, flip=flip, grade={})


def t(text, y=0.40, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


def vpages(items, tone, tag, beats):
    return [img(vpage(P[k], O + f"{tag}{i}.jpg", "N° " + NUMS[i], sub, tone), beats) for i, (k, sub) in enumerate(items)]


def vfin(front, back, tag, no, tone):
    return img(vstacked(P[front], P[back], O + f"{tag}c.jpg", no, tone=tone), 4)


KNIT = "BLACK KNIT"
QBW = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QKN = [("SWF", cat(1, KNIT)), ("KF", cat(2, COLLAR)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]
QW = [("PF", cat(1, COLLAR)), ("WF", cat(2, IX))]

R = [  # key, track, tone, hook, texts, pages, finale(front, back)
    ("E01_shoes-first", AU, "oxblood", ramp("COUPLE", 4.7, crop_x=0.55),
     t("they look at the shoes first.\nthen up."), QBW, ("PF", "PB")),
    ("E02_what-goes-with-red-soles", MP, "vitrine", [soles(speed=1.12, zoom=1.25, crop_y=0.62)],
     t("what goes with\nred soles?"), QKN, ("SPF", "SPB")),
    ("E03_second-most-famous-red", MP, "oxblood", [lb("COUPLE", speed=1.12, flip=True, zoom=1.22, crop_y=0.78)],
     t("the second most\nfamous red."), QBK, ("KF", "KB")),
    ("E04_in-that-order", MP, "vitrine",
     [rose("g3", C4), lb("STREET", start=1.4, dur=C2 - C4, speed=1.1, flip=True), lb("COUPLE", speed=1.1)],
     t("rose. sole. collar.\nin that order.", 0.56, 0.45), QW, ("PF", "PB")),
    ("E05_matched-her-shoes", AU, "oxblood",
     [rose("g1", DROP - 3 * BAU, start=0.3, speed=1.0), soles(speed=0.9, tail=3 * BAU)],
     t("she matched her shoes\nto his collar.", 0.56, 0.45), QKN, ("SPF", "SPB")),
]
for i, (k, track, tone, hook, texts, pg, fin) in enumerate(R):
    tag = f"e{i + 1:02d}"
    pb = 1 if track == MP else 2
    segs = hook + vpages(pg, tone, tag, pb) + [vfin(fin[0], fin[1], tag, "N° " + NUMS[len(pg)], tone)]
    spec = dict(seed=22000 + i, track=track, segments=segs, texts=texts)
    json.dump(spec, open(os.path.join(SP, f"e1107_{k}.json"), "w"), indent=1)
    print(f"e1107_{k}")
