#!/usr/bin/env python3
"""made 2026-11-26 (night), batch 1126d: 4 new reels BT27-BT30 on the "bad together." format (Kirill: 4 new reels).

From the numbers of 11-24..11-26 (Metricool, 11-26 23:00): V01 "bad together." 3.2K (15 saves, 23 shares) and BT14
"she ruined him." 2.1K lead; the lines that work are the provocative couple ones ("bad" / ruined / secret). The Latin pun
(BT17, 0.3K, 52 %) and the all-black pages (BT25 dark mode, 54 % past 3 s) did worst. So: 4 lines in the "bad together"
register, V01-like pages (black next to white, HIS / HERS), 2 couple hooks, 1 BT14-like mix, 1 bright hook.

BT27 toxic, but matching.                COUPLE in one take, 1.1x, as V01 but reframed; vitrine; zip pair over QZ pair
BT28 he never wore red before her.       her red nails -> his loafers -> red on both (his red sole too); oxblood, zip pair finale
BT29 she's a bad idea.                   bright, a cut on every beat: walk wide -> terrazzo -> marble -> shoes -> heel; lamp
BT30 don't date someone who matches you. her hand -> the whole walk, mirrored; slate; V01's finale (QZ pair front / back)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
import vitrine as V
from vitrine2 import vpage2, vside, vstacked2, vgrid
from build_1119a import gr, sh, couple_red
import loopreel

V.TONES.setdefault("lamp", ((92, 86, 78), (5, 5, 5)))
OUT = "/mnt/user-data/outputs/ready-2026-11-26d/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
WHITE = {"WF", "WB", "XWF", "XWB"}


def o(name):
    return O + "bt1126d_" + name + ".jpg"


def pages(tag, keys, tone, scale=0.9, cy=0.47, spot=None):
    """V01's run: one garment per half beat, HIS · BLACK / HERS · WHITE"""
    return [(0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j],
                             cat(j + 1, "HERS  ·  WHITE" if k in WHITE else "HIS  ·  BLACK"), tone, scale=scale, cy=cy,
                             spot=spot), 1)) for j, k in enumerate(keys)]


def fin(path, beats):
    return (beats, img(path, 1))


R = []

# BT27 toxic, but matching. - COUPLE in one take at 1.1x (V01's speed), not mirrored, a touch tighter than V01
g = gr(b=-0.012, c=1.06, s=0.9)
R.append(("BT27_toxic-but-matching", "toxic, but matching.",
          [couple_red(g, speed=1.1, zoom=1.06, crop_x=0.5, crop_y=0.64)],
          pages("27", ["KF", "WF", "ZF", "XWF", "KB", "WB"], "vitrine") +
          [fin(vstacked2(P["ZPF"], P["PF"], o("27f"), "N° VII", tone="vitrine"), 3)],
          "COUPLE one take 1.1x, not mirrored, zoom 1.06; V01 pages (black / white, HIS / HERS), vitrine; zip pair over QZ pair"))

# BT28 he never wore red before her. - her red nails -> his loafers walking -> red soles on both (his red sole too)
g = gr(b=-0.014, c=1.06, s=0.92); g.update(rm=0.02)
R.append(("BT28_he-never-wore-red-before-her", "he never wore red\nbefore her.",
          [sh("SOLES", 1.45, 39, g, zoom=1.3, crop_x=0.4), sh("COUPLE", 2.0, 37, g, zoom=1.25, crop_y=0.7),
           couple_red(g, zoom=1.2, crop_x=0.5, crop_y=0.72)],
          pages("28", ["KF", "WF", "ZF", "XWF", "ZB", "XWB"], "oxblood", scale=0.9, spot=(0.5, 0.4, 0.6, 0.34)) +
          [fin(vstacked2(P["ZPF"], P["ZPB"], o("28f"), "N° VII", tone="oxblood"), 3)],
          "SOLES red nails -> COUPLE his loafers -> COUPLE red on both; HIS first, oxblood; zip pair front over back"))

# BT29 she's a bad idea. - bright, a cut on every beat: walk wide -> terrazzo -> marble -> shoes close -> red heel
gb = gr(b=0.02, c=1.06, s=0.86, g=1.05)
R.append(("BT29_shes-a-bad-idea", "she's a bad idea.",
          [sh("COUPLE", 1.6, 21, gb, zoom=1.0, crop_y=0.55), sh("SOLES", 3.2, 18, gb, zoom=1.1, crop_y=0.5),
           sh("MARBLE", 0.0, 19, gb, zoom=1.25, crop_x=0.6, crop_y=0.5), sh("COUPLE", 1.9, 18, gb, zoom=1.3, crop_y=0.62),
           sh("MARBLE", 0.49, 18, gb, zoom=1.0, crop_y=0.5, flip=True)],
          pages("29", ["WF", "KF", "XWF", "ZF", "WB", "KB"], "lamp") +
          [fin(vgrid([P["WF"], P["KF"], P["XWF"], P["ZF"]], o("29f"), "N° VII", "FIRST LOOK", "lamp"), 3)],
          "bright, 5 shots on the beats: COUPLE walk wide -> SOLES terrazzo -> MARBLE -> COUPLE shoes close -> MARBLE heel mirrored; white first, lamp; 2 x 2"))

# BT30 don't date someone who matches you. - her hand -> the whole walk, mirrored -> red on both; V01's finale
g = gr(b=-0.012, c=1.05, s=0.9, g=0.98)
R.append(("BT30_dont-date-someone-who-matches-you", "don't date someone\nwho matches you.",
          [sh("COUPLE", 0.55, 21, g, zoom=1.2, crop_x=0.4, crop_y=0.6, flip=True),
           couple_red(g, zoom=1.1, crop_x=0.5, crop_y=0.6, flip=True)],
          pages("30", ["ZF", "XWF", "KF", "WF", "ZB", "XWB"], "slate", scale=0.9) +
          [fin(vstacked2(P["PF"], P["PB"], o("30f"), "N° VII", tone="slate"), 3)],
          "COUPLE mirrored: her hand -> the whole walk -> red on both; zips first, slate; QZ pair front over back (V01's finale)"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1126d", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=53000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1126d_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1126d.json"), "w"), indent=1)
