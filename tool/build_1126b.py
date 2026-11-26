#!/usr/bin/env python3
"""made 2026-11-26, batch 1126b: 2 reels on the "bad together." format with the black hoodie. Kirill: one only with the
black hoodie, one with the hoodie and the zip. Read as: the Roman Night hoodie (black pullover, red IX on the front,
red print on the back; mockups `~/Downloads/мокапы/Roman night hoodie/9sky_hd_01_front.png`, `..._02_back.png`) -
alone, and next to the IX zip hoodie.
BT23 the ninth legion never came back.  theme: the legend of the lost Legio IX (the hoodie's IX); hook = marching, a cut on
                                        every beat, COUPLE walking, NAILS into the mist -> red on both; hoodie front / back only, oxblood
BT24 one shows the red. one hides it.   theme: show / hide - the hoodie wears its red outside, the zip hoodie inside the
                                        hood; bright hook (his shoes in the flash -> walking -> marble red heel)
Same base: one line, pages on half beats, a pair finale, loop 12 beats on the 99 BPM grid."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
from vitrine2 import vpage2, vside
from build_1119a import gr, sh, couple_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-26b/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
RN = "/mnt/user-data/uploads/мокапы/Roman night hoodie/"
M = dict(P, HF=RN + "9sky_hd_01_front.png", HB=RN + "9sky_hd_02_back.png")


def o(name):
    return O + "bt1126b_" + name + ".jpg"


def pages(tag, items, tone, cy=0.47, spot=None):
    """items: (mockup key, catalogue label, scale) -> one page per half beat"""
    return [(0.5, img(vpage2(M[k], o(f"{tag}{j}"), "N° " + NUMS[j], cat(j + 1, lab), tone, scale=sc, cy=cy,
                             spot=spot), 1)) for j, (k, lab, sc) in enumerate(items)]


def fin(path, beats):
    return (beats, img(path, 1))


R = []
F, B = "IX  ·  FRONT", "IX  ·  BACK"

# BT23 the ninth legion never came back. - marching: walking cut on every beat -> red on both; the hoodie only
g = gr(b=-0.012, c=1.06, s=0.9); g.update(rm=0.015)
R.append(("BT23_the-ninth-legion", "the ninth legion\nnever came back.",
          [sh("COUPLE", 1.3, 21, g, zoom=1.25, crop_y=0.62), sh("COUPLE", 2.3, 18, g, zoom=1.0, crop_y=0.55),
           sh("NAILS", 0.3, 19, g, zoom=1.05, crop_y=0.5), sh("COUPLE", 3.3, 18, g, zoom=1.15, crop_y=0.65, flip=True),
           couple_red(g, zoom=1.25, crop_x=0.45, crop_y=0.76)],
          pages("23", [("HF", F, 0.9), ("HB", B, 0.9), ("HF", F, 1.04), ("HB", B, 1.04), ("HF", F, 0.8),
                       ("HB", B, 0.8)], "oxblood", spot=(0.5, 0.45, 0.62, 0.38)) +
          [fin(vside(M["HF"], M["HB"], o("23f"), "N° VII", "FIRST LOOK", "oxblood", title="EX MUSEO"), 3)],
          "marching: COUPLE shoes -> walk wide -> NAILS into the mist -> COUPLE walk mirrored -> red on both, a cut on every beat; Roman Night hoodie front / back only, scale pulsing, oxblood"))

# BT24 one shows the red. one hides it. - bright hook; the hoodie (red outside) against the zip hoodies (red inside)
gb = gr(b=0.02, c=1.06, s=0.86, g=1.05)
S_, H_ = "SHOWS THE RED", "HIDES THE RED"
R.append(("BT24_one-shows-the-red", "one shows the red.\none hides it.",
          [sh("COUPLE", 1.55, 39, gb, zoom=1.3, crop_x=0.5, crop_y=0.62), sh("COUPLE", 2.3, 37, gb, zoom=1.0, crop_y=0.55),
           sh("MARBLE", 0.49, 18, gb, zoom=1.2, crop_x=0.5, crop_y=0.55)],
          pages("24", [("HF", S_, 0.9), ("XWF", H_, 0.9), ("HB", S_, 0.9), ("ZF", H_, 0.9), ("HF", S_, 0.9),
                       ("XWB", H_, 0.9)], "vitrine", spot=(0.5, 0.42, 0.6, 0.35)) +
          [fin(vside(M["HF"], M["ZF"], o("24f"), "N° VII", "FIRST LOOK", "vitrine", title="EX MUSEO"), 3)],
          "bright: COUPLE his shoes in the flash -> walk wide -> MARBLE red heel; Roman Night hoodie (SHOWS THE RED) against the zip hoodies (HIDES THE RED), vitrine"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1126b", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=51000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1126b_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1126b.json"), "w"), indent=1)
