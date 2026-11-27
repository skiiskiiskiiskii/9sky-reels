#!/usr/bin/env python3
"""made 2026-11-27 (morning), batch 1127b: 5 reels BT34-BT38. Kirill: 5 new reels, without the cheap effects of the last
reels, and the lines more logical and simpler.

So: back to the clean "bad together." look - one Cormorant line at the top, no text cards / bubbles / bands (1127a),
no camera flashes (BT22), no backwards clips, no strong push-ins; plain cuts at real speed. The line says what the reel
shows: her red is outside (soles), his red is inside (collar / hood). Pages: V01's black / white run with HIS / HERS.

BT34 hers outside. his inside.          COUPLE in one take, 1.1x
BT35 one red for two.                   COUPLE in one take, mirrored, 1.08x
BT36 look at her shoes. then his collar. heels in the mist -> his loafers -> both soles close; quarter zips only (collar)
BT37 black and white. red inside.       bright: his shoes in the flash -> marble -> legs -> red heel (plain cuts)
BT38 her heels. his hood.               her pumps -> heels in the mist -> walking -> her heel lifts; zip hoodies only (hood)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
import vitrine as V
from vitrine2 import vpage2, vstacked2, vgrid
from build_1119a import gr, sh, couple_red
import loopreel

V.TONES.setdefault("lamp", ((92, 86, 78), (5, 5, 5)))
OUT = "/mnt/user-data/outputs/ready-2026-11-27b/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
WHITE = {"WF", "WB", "XWF", "XWB"}


def o(name):
    return O + "bt1127b_" + name + ".jpg"


def pages(tag, keys, tone, scale=0.9, cy=0.47, spot=None):
    return [(0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j],
                             cat(j + 1, "HERS  ·  WHITE" if k in WHITE else "HIS  ·  BLACK"), tone, scale=scale, cy=cy,
                             spot=spot), 1)) for j, k in enumerate(keys)]


def fin(path, beats):
    return (beats, img(path, 1))


R = []

g = gr(b=-0.012, c=1.05, s=0.9); g.update(rh=0.01)
R.append(("BT34_hers-outside-his-inside", "hers outside.\nhis inside.",
          [couple_red(g, speed=1.1, zoom=1.08, crop_x=0.45, crop_y=0.68)],
          pages("34", ["KF", "WF", "ZF", "XWF", "KB", "WB"], "vitrine") +
          [fin(vstacked2(P["PF"], P["ZPF"], o("34f"), "N° VII", tone="vitrine"), 3)],
          "COUPLE one take 1.1x; V01 pages, vitrine; QZ pair over zip pair"))

g = gr(b=-0.014, c=1.06, s=0.9, g=0.98)
R.append(("BT35_one-red-for-two", "one red for two.",
          [couple_red(g, speed=1.08, zoom=1.2, crop_x=0.42, crop_y=0.7, flip=True)],
          pages("35", ["WF", "KF", "XWF", "ZF", "WB", "KB"], "slate") +
          [fin(vgrid([P["KF"], P["WF"], P["ZF"], P["XWF"]], o("35f"), "N° VII", "FIRST LOOK", "slate"), 3)],
          "COUPLE one take 1.08x, mirrored; white first, slate; 2 x 2"))

g = gr(b=-0.014, c=1.06, s=0.92); g.update(rm=0.015)
R.append(("BT36_look-at-her-shoes-then-his-collar", "look at her shoes.\nthen his collar.",
          [sh("NAILS", 0.55, 21, g, zoom=1.05, crop_y=0.55), sh("COUPLE", 1.7, 55, g, zoom=1.05, crop_y=0.62),
           sh("SOLES", 5.42, 18, g, zoom=1.12, crop_y=0.5)],
          pages("36", ["KF", "WF", "KB", "WB", "KF", "WF"], "oxblood", scale=0.92, spot=(0.5, 0.38, 0.56, 0.3)) +
          [fin(vstacked2(P["PF"], P["PB"], o("36f"), "N° VII", tone="oxblood"), 3)],
          "NAILS heels in the mist -> COUPLE his loafers -> SOLES both soles close; quarter zips only, glow on the collar, oxblood; QZ pair front / back"))

gb = gr(b=0.02, c=1.06, s=0.86, g=1.05)
R.append(("BT37_black-and-white-red-inside", "black and white.\nred inside.",
          [sh("COUPLE", 1.4, 39, gb, zoom=1.15, crop_x=0.5, crop_y=0.6), sh("MARBLE", 0.0, 19, gb, zoom=1.1, crop_y=0.5),
           sh("SOLES", 3.2, 18, gb, zoom=1.08, crop_y=0.5), sh("MARBLE", 0.49, 18, gb, zoom=1.1, crop_y=0.55)],
          pages("37", ["ZF", "XWF", "KF", "WF", "ZB", "XWB"], "lamp") +
          [fin(vgrid([P["ZF"], P["XWF"], P["KF"], P["WF"]], o("37f"), "N° VII", "FIRST LOOK", "lamp"), 3)],
          "bright, plain cuts: COUPLE shoes in the flash -> MARBLE -> SOLES legs -> MARBLE red heel; lamp; 2 x 2"))

g = gr(b=-0.012, c=1.05, s=0.9); g.update(rh=0.02)
R.append(("BT38_her-heels-his-hood", "her heels.\nhis hood.",
          [sh("SOLES", 0.55, 21, g, zoom=1.1, crop_y=0.55), sh("NAILS", 1.0, 18, g, zoom=1.08),
           sh("COUPLE", 2.3, 37, g, zoom=1.05, crop_y=0.6, flip=True),
           sh("NAILS", 5.4, 18, g, zoom=1.05, crop_x=0.0, crop_y=0.5)],
          pages("38", ["ZF", "XWF", "ZB", "XWB", "ZF", "XWF"], "bronze", scale=0.9, spot=(0.5, 0.38, 0.56, 0.3)) +
          [fin(vstacked2(P["ZPF"], P["ZPB"], o("38f"), "N° VII", tone="bronze"), 3)],
          "SOLES her pumps -> NAILS heels in the mist -> COUPLE walking mirrored -> NAILS heel lift; zip hoodies only, glow on the hood, bronze; zip pair"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1127b", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=55000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1127b_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1127b.json"), "w"), indent=1)
