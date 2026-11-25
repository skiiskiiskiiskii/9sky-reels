#!/usr/bin/env python3
"""made 2026-11-25 (night), batch 1125b: 3 more reels BT15-BT17 on the "bad together." format, with other THEMES for the
line (Kirill: find slightly different themes). 1124d / 1125a lines were couple bait + crime (red flags, red-handed,
wanted, suspects, last seen). New themes here:
BT15 pov: she picked your outfit.   - the POV format (the viewer is him), dating humour
BT16 red means stop. we didn't.     - wordplay on red as a signal
BT17 veni. vidi. matched.           - a Latin / Roman pun (the brand is inspired by ancient Rome; the backs carry the
                                      Ara Pacis ornament) - not "from Rome", not classy
Same base: Louboutin hook to the 3.13 s cut, one line, black / white pages on half beats, pair finale, loop 12 beats
on the 99 BPM grid (post with the "bad together" track)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP, ARA, ROME
from vitrine2 import vpage2, vside, vstacked2
from build_1119a import gr, sh, soles_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-25b/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
WHITE = {"WF", "WB", "XWF", "XWB"}


def o(name):
    return O + "bt1125b_" + name + ".jpg"


def pages(tag, items, tone, scale=0.9, cy=0.47, spot=None, beats=0.5):
    """items: (mockup key, catalogue label, place) -> one page each, half a beat by default"""
    return [(beats, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j], cat(j + 1, lab, place), tone, scale=scale,
                                cy=cy, spot=spot), 1)) for j, (k, lab, place) in enumerate(items)]


def fin(path, beats):
    return (beats, img(path, 1))


PRG = "PRAGUE, MMXXVI"
R = []   # key, line, hook, after, idea

# BT15 pov: she picked your outfit. - looking down at his shoes while her hand decides -> walking -> her red heel on
# marble, tight; HER PICK labels, 4 half pages + a 1-beat pair, slate
g = gr(b=-0.012, c=1.05, s=0.92, g=0.98)
R.append(("BT15_pov-she-picked-your-outfit", "pov: she picked\nyour outfit.",
          [sh("COUPLE", 0.55, 58, g, zoom=1.2, crop_x=0.5, crop_y=0.5), sh("SOLES", 3.0, 18, g, zoom=1.15, crop_y=0.5),
           sh("MARBLE", 0.49, 18, g, zoom=1.3, crop_x=0.55, crop_y=0.55, flip=True)],
          pages("15", [("XWF", "HER PICK  ·  WHITE", PRG), ("ZF", "HER PICK  ·  BLACK", PRG),
                       ("WF", "HER PICK  ·  WHITE", PRG), ("KF", "HER PICK  ·  BLACK", PRG)], "slate", scale=0.9) +
          [fin(vside(P["WF"], P["KF"], o("15s"), "N° V", cat(5, "HERS  ·  HIS"), "slate"), 1),
           fin(vstacked2(P["ZPF"], P["ZPB"], o("15f"), "N° VI", tone="slate"), 3)],
          "COUPLE one long look at his shoes, her hand -> SOLES walking -> MARBLE tight mirrored; HER PICK, 4 half pages + 1-beat pair, slate; zip pair"))

# BT16 red means stop. we didn't. - they keep walking (mist, wide, legs) -> stop on the red: logo sole + her red heels
# close (SOLES 5.6); ink; finale: the two QZ backs side by side
g = gr(b=-0.016, c=1.07, s=0.9); g.update(rm=0.02)
R.append(("BT16_red-means-stop", "red means stop.\nwe didn't.",
          [sh("NAILS", 0.55, 21, g, zoom=1.1, crop_y=0.5), sh("COUPLE", 1.5, 37, g, zoom=1.0, crop_y=0.55),
           sh("SOLES", 3.2, 18, g, zoom=1.1, crop_y=0.5), sh("SOLES", 5.6, 18, g, zoom=1.3, crop_x=0.4, crop_y=0.55)],
          pages("16", [("KF", "HIS  ·  BLACK", PRG), ("WF", "HERS  ·  WHITE", PRG), ("ZB", "HIS  ·  BLACK", PRG),
                       ("XWB", "HERS  ·  WHITE", PRG), ("ZF", "HIS  ·  BLACK", PRG), ("XWF", "HERS  ·  WHITE", PRG)],
                "ink", scale=0.88, spot=(0.5, 0.42, 0.6, 0.34)) +
          [fin(vside(P["KB"], P["WB"], o("16f"), "N° VII", "FIRST LOOK", "ink", title="EX MUSEO"), 3)],
          "NAILS heels in the mist -> COUPLE walking wide -> SOLES legs -> SOLES logo sole + red heels tight; ink; QZ backs side by side"))

# BT17 veni. vidi. matched. - three shots, one per word: she arrives (heels in the mist) -> sees (red nails) -> matched
# (his logo sole next to her red sole); the backs first with the Ara Pacis label, bronze; pair backs over zip pair backs
g = gr(b=-0.012, c=1.05, s=0.9); g.update(rh=0.025, bh=-0.01)
R.append(("BT17_veni-vidi-matched", "veni. vidi.\nmatched.",
          [sh("NAILS", 0.8, 39, g, zoom=1.12, crop_y=0.5), sh("SOLES", 1.45, 37, g, zoom=1.35, crop_x=0.45),
           soles_red(18, g, zoom=1.35, crop_x=0.55, crop_y=0.65)],
          pages("17", [("KB", ARA, ROME), ("WB", ARA, ROME), ("ZB", ARA, ROME), ("XWB", ARA, ROME),
                       ("KF", "HIS  ·  BLACK", PRG), ("WF", "HERS  ·  WHITE", PRG)], "bronze", scale=0.9, cy=0.47) +
          [fin(vstacked2(P["PB"], P["ZPB"], o("17f"), "N° VII", tone="bronze"), 3)],
          "NAILS mist + hand -> SOLES red nails tight -> SOLES logo + red sole tight; backs first (AFTER THE ARA PACIS · ROME, 9 BC), bronze; pair backs"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1125b", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=49000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1125b_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1125b.json"), "w"), indent=1)
