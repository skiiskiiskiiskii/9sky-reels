#!/usr/bin/env python3
"""made 2026-11-25, batch 1125a: 6 more reels BT09-BT14 on the "bad together." format (Kirill: 6 new reels, other lines).
Same base as 1124d: Louboutin hook to the 3.13 s cut with one short line, black / white pages on half beats, pair
finale, loop 12 beats on the 99 BPM grid (post with the "bad together" track).

New against 1124d:
- endings of the hook nobody has seen yet: SOLES 6.6-7.2 (two red soles big, after the logo), COUPLE 5.0-5.6 (red soles
  close), MARBLE played backwards (the heel comes down); couple_red / soles_red / NAILS heel only once each, reframed;
- a 5-shot hook (a cut on every beat) in BT11;
- pages: hers first (BT09), the pair images as pages (BT10), 8 pages WANTED (BT11), bigger garments (BT12),
  4 half-beat pages + a 1-beat his | hers page (BT13), black first (BT14); each tone used once;
- labels: HERS / HIS, SET OF TWO, WANTED, SUSPECT A / B."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
from vitrine2 import vpage2, vside, vstacked2, vgrid
from build_1119a import gr, sh, couple_red, soles_red, marble_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-25a/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
LBL = {  # label sets: key -> (black, white)
    "his": ("HIS  ·  BLACK", "HERS  ·  WHITE"),
    "set": ("SET OF TWO", "SET OF TWO"),
    "wanted": ("WANTED  ·  BLACK", "WANTED  ·  WHITE"),
    "suspect": ("SUSPECT A  ·  BLACK", "SUSPECT B  ·  WHITE"),
}
WHITE = {"WF", "WB", "XWF", "XWB"}


def o(name):
    return O + "bt1125_" + name + ".jpg"


def half_pages(tag, keys, tone, labels="his", scale=0.9, cy=0.47, spot=None, start=0):
    out = []
    for j, k in enumerate(keys):
        lab = LBL[labels][1 if k in WHITE else 0]
        out.append((0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[start + j], cat(start + j + 1, lab), tone,
                                    scale=scale, cy=cy, spot=spot), 1)))
    return out


def fin(path, beats):
    return (beats, img(path, 1))


R = []   # key, line, hook, after, idea

# BT09 she started it. - her hand -> his shoes -> walking -> two red soles big (SOLES after the logo); hers first, smoke
g = gr(b=-0.014, c=1.05, s=0.9); g.update(rh=0.015)
R.append(("BT09_she-started-it", "she started it.",
          [sh("SOLES", 0.55, 21, g, zoom=1.3, crop_x=0.35, crop_y=0.55), sh("NAILS", 1.6, 18, g, zoom=1.12),
           sh("COUPLE", 2.4, 37, g, zoom=1.08, crop_y=0.65, flip=True), sh("SOLES", 6.6, 18, g, zoom=1.12, crop_y=0.5)],
          half_pages("09", ["WF", "XWF", "WB", "XWB", "KF", "ZF"], "smoke") +
          [fin(vside(P["XWF"], P["ZF"], o("09f"), "N° VII", "FIRST LOOK", "smoke", title="EX MUSEO"), 3)],
          "SOLES her hand -> NAILS -> COUPLE walking mirrored -> SOLES two red soles big; hers first (white), smoke; her zip | his zip"))

# BT10 do not separate. - both pairs walking (wide) -> legs together -> red soles close (COUPLE 5.0); pair pages, slate
g = gr(b=-0.012, c=1.06, s=0.92, g=0.98)
R.append(("BT10_do-not-separate", "do not separate.",
          [sh("COUPLE", 1.3, 39, g, zoom=1.0, crop_y=0.5), sh("SOLES", 2.95, 37, g, zoom=1.05, crop_y=0.5),
           sh("COUPLE", 5.0, 18, g, zoom=1.15, crop_x=0.5, crop_y=0.7)],
          half_pages("10", ["PF", "ZPF", "PB", "ZPB", "PF", "ZPF"], "slate", labels="set", scale=0.95) +
          [fin(vgrid([P["KF"], P["WF"], P["KB"], P["WB"]], o("10f"), "N° VII", "FIRST LOOK", "slate"), 3)],
          "COUPLE both pairs wide -> SOLES legs -> COUPLE red soles close; the pair mockups as pages (SET OF TWO), slate; QZ 2 x 2"))

# BT11 wanted. both of them. - a cut on every beat: mist -> red nails close -> watch -> walking -> MARBLE backwards; ink
g = gr(b=-0.016, c=1.07, s=0.88); g.update(bs=0.015)
R.append(("BT11_wanted-both-of-them", "wanted.\nboth of them.",
          [sh("NAILS", 0.6, 21, g, zoom=1.1, crop_y=0.5), sh("COUPLE", 0.9, 18, g, zoom=1.35, crop_x=0.4, crop_y=0.5),
           sh("SOLES", 2.7, 19, g, zoom=1.25, crop_x=0.5), sh("COUPLE", 2.9, 18, g, zoom=1.0, crop_y=0.55),
           sh("MARBLE", 0.49, 18, g, zoom=1.15, crop_y=0.5, reverse=True)],
          half_pages("11", ["KF", "WF", "KB", "WB", "ZF", "XWF", "ZB", "XWB"], "ink", labels="wanted", scale=0.86,
                     spot=(0.5, 0.43, 0.6, 0.34)) +
          [fin(vstacked2(P["KF"], P["WF"], o("11f"), "N° IX", tone="ink"), 2)],
          "5 shots on the beats: NAILS mist -> COUPLE red nails close -> SOLES watch -> COUPLE walking -> MARBLE backwards; WANTED, 8 pages, ink; QZ black over white"))

# BT12 the red stays between us. - close-ups: hand -> red nails -> both red soles tight (COUPLE); big garments, oxblood
g = gr(b=-0.012, c=1.06, s=0.93); g.update(rm=0.02)
R.append(("BT12_the-red-stays-between-us", "the red stays\nbetween us.",
          [sh("COUPLE", 0.55, 39, g, zoom=1.4, crop_x=0.45, crop_y=0.45), sh("SOLES", 1.5, 37, g, zoom=1.45, crop_x=0.4),
           couple_red(g, zoom=1.4, crop_x=0.5, crop_y=0.8)],
          half_pages("12", ["KF", "XWF", "ZF", "WF", "KF", "XWF"], "oxblood", scale=1.0, cy=0.48,
                     spot=(0.5, 0.36, 0.55, 0.3)) +
          [fin(vside(P["ZF"], P["WF"], o("12f"), "N° VII", "FIRST LOOK", "oxblood", title="EX MUSEO"), 3)],
          "COUPLE hand tight -> SOLES red nails tight -> COUPLE both soles tight; garments bigger, glow on the collar, oxblood; his zip | her QZ"))

# BT13 two suspects. one color. - legs walking -> his loafers -> heels in the mist -> logo sole (wide); vitrine
g = gr(b=-0.018, c=1.06, s=0.85, g=0.97)
R.append(("BT13_two-suspects-one-color", "two suspects.\none color.",
          [sh("SOLES", 2.95, 39, g, zoom=1.05, crop_y=0.45), sh("COUPLE", 1.6, 18, g, zoom=1.2, crop_y=0.7, flip=True),
           sh("NAILS", 0.3, 19, g, zoom=1.0), soles_red(18, g, zoom=1.0, crop_y=0.5)],
          half_pages("13", ["KF", "WF", "ZF", "XWF"], "vitrine", labels="suspect", scale=0.88) +
          [fin(vside(P["KF"], P["WF"], o("13s"), "N° V", cat(5, "SUSPECT A  ·  SUSPECT B"), "vitrine"), 1),
           fin(vgrid([P["KF"], P["WF"], P["ZF"], P["XWF"]], o("13f"), "N° VI", "FIRST LOOK", "vitrine"), 3)],
          "SOLES legs -> COUPLE loafers mirrored -> NAILS mist -> SOLES logo sole wide; SUSPECT A / B, 4 half pages + 1-beat pair, vitrine; 2 x 2"))

# BT14 she ruined him. - her red nails -> his loafers -> her heel lifts, red (NAILS); his black first, then hers; bronze
g = gr(b=-0.014, c=1.05, s=0.9); g.update(rh=0.02)
R.append(("BT14_she-ruined-him", "she ruined him.",
          [sh("SOLES", 1.5, 39, g, zoom=1.2, crop_x=0.45), sh("COUPLE", 1.6, 37, g, zoom=1.15, crop_y=0.65, flip=True),
           sh("NAILS", 5.4, 18, g, zoom=1.05, crop_x=0.0, crop_y=0.5)],
          half_pages("14", ["ZF", "WF", "KF", "XWF", "ZB", "WB"], "bronze", scale=0.9) +
          [fin(vstacked2(P["ZPF"], P["PF"], o("14f"), "N° VII", tone="bronze"), 3)],
          "SOLES red nails -> COUPLE his loafers mirrored -> NAILS heel lift; his black first on every pair, bronze; zip pair over QZ pair"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1125a", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=48000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1125_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1125a.json"), "w"), indent=1)
