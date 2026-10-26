#!/usr/bin/env python3
"""2026-10-27 batch after the market analysis: formats 1, 3 and 4 from the solutions doc.
Q  - release question ("should we?", "black or white?") on the pair page
P  - category-upgrade POV line on the hook ("pov: you're done with basic quarter zips.")
M  - art-history moodboard from Met Open Access (CC0) paintings, our mockup as the last item
All text in Cormorant italic; no zoom, no grain, no labels on the garment."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, HOOD, IX, SP, DROP

SRC = "/mnt/user-data/uploads/hooks ids/snaptik_"
S2, S5, S7 = (SRC + v + "_hd.mp4" for v in ("7382217770819177761", "7615821256385924366", "7656541418327903501"))
ART = "/mnt/user-data/uploads/9sky-reels/hooks/art-met/9sky_art_"


def tx(text, y, frm=0, to="drop", size=96):
    return {"text": text, "from": frm, "to": to, "y": y, "size": size, "scrim": 0.5, "font": "cg-italic"}


def art(name, **kw):
    d = dict(type="image", src=ART + name + ".jpg", fit="cover")
    d.update(kw)
    return d


def moodboard(pre, post):
    """3 paintings before the drop (~1 s each), then one painting every 2 beats"""
    step = DROP / len(pre)
    segs = [art(n, dur=step) for n in pre[:-1]] + [art(pre[-1], until="drop")]
    return segs + [art(n, beats=2) for n in post]


S = {}
# Q01 - release question, quarter zip
S["Q01_should-we"] = dict(seed=10101, segments=
    [clip("x", 14.20, src=S7, speed=0.55, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("PF", cat(2, "NOT MADE YET"))], None, "q01", 2) +
    [img(fin_path("PF", "PB", "q01", "N° III"), 4)],
    texts=[tx("we haven't made\nthis yet.", 0.60), tx("should we?", 0.215, "b:2", "b:4")])
# Q02 - black or white
S["Q02_black-or-white"] = dict(seed=10102, segments=
    [clip("38_marble-relief-b", 0.2, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("WF", cat(2, COLLAR)), ("PF", cat(3, "ONE OF THEM"))], None, "q02", 2) +
    [img(fin_path("PF", "PB", "q02", "N° IV"), 4)],
    texts=[tx("help us\npick one.", 0.60), tx("black or white?", 0.215, "b:4", "b:6")])
# P01 - category upgrade, quarter zip
S["P01_basic-quarter-zips"] = dict(seed=10103, segments=
    [clip("x", 5.40, src=S2, until="drop")] +
    pages([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], None, "p01", 2) +
    [img(fin_path("PF", "PB", "p01", "N° III"), 4)],
    texts=[tx("pov: you're done with\nbasic quarter zips.", 0.60)])
# P02 - category upgrade, zip hoodie
S["P02_basic-zip-hoodies"] = dict(seed=10104, segments=
    [clip("28_golden-dome-b", 0.2, until="drop")] +
    pages([("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], None, "p02", 2) +
    [img(fin_path("ZPF", "ZPB", "p02", "N° III"), 4)],
    texts=[tx("pov: you're done with\nbasic zip hoodies.", 0.60)])
# M01 - dark portraits and marble, black quarter zip last
S["M01_till-closing"] = dict(seed=10105, segments=
    moodboard(["m1_01", "m1_07", "m1_03"], ["m1_02", "m1_08", "m1_04", "m1_06", "m1_05", "m1_09"]) +
    pages([("KF", cat(1, COLLAR))], None, "m01", 3) +
    [img(fin_path("PF", "PB", "m01", "N° II"), 4)],
    texts=[tx("for the ones who stay\nin museums till closing.", 0.60, 0, "b:12")])
# M02 - red in old paintings, red collar last
S["M02_starter-pack"] = dict(seed=10106, segments=
    moodboard(["m2_07", "m2_01", "m2_03"], ["m2_02", "m2_08", "m2_04", "m2_06", "m2_09", "m2_05"]) +
    pages([("KF", cat(1, IX))], None, "m02", 3) +
    [img(fin_path("PF", "PB", "m02", "N° II"), 4)],
    texts=[tx("art history major\nstarter pack.", 0.60, 0, "b:12")])

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"q1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
