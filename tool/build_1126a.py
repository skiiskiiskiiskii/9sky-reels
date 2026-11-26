#!/usr/bin/env python3
"""made 2026-11-26, batch 1126a: 5 reels BT18-BT22 on the "bad together." format. Kirill:
- 3 reels with the main couple hook (COUPLE: the pair walking -> red soles on both, as in V01 "bad together.");
- 2 reels with the bright-light hook - his refs: COUPLE ~1.7 s (his shoes standing in a bright flash, as in BT15) and
  the bright marble (MARBLE, as in BT15);
- a separate theme for the line on every reel.
Themes: BT18 chess (black and white pieces), BT19 a superstition (red underneath for luck), BT20 dating ("she has a
type"), BT21 Roman myth (Mars and Venus - the brand is inspired by Rome, never "from Rome"), BT22 paparazzi (bright
flash hook, a camera flash on every cut of the hook).
Same base: one line, black / white pages on half beats, pair finale, loop 12 beats on the 99 BPM grid."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
from vitrine2 import vpage2, vside, vstacked2, vgrid
from build_1119a import gr, sh, couple_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-26a/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
PRG = "PRAGUE, MMXXVI"


def o(name):
    return O + "bt1126_" + name + ".jpg"


def pages(tag, items, tone, scale=0.9, cy=0.47, spot=None):
    """items: (mockup key, catalogue label) -> one page per half beat"""
    return [(0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j], cat(j + 1, lab), tone, scale=scale, cy=cy,
                             spot=spot), 1)) for j, (k, lab) in enumerate(items)]


def fin(path, beats):
    return (beats, img(path, 1))


def flash(path, cuts, peak=0.42):
    """a camera flash on the given frames: +peak brightness on the cut frame, half of it on the next one"""
    terms = "+".join(f"{peak:.2f}*eq(n,{c})+{peak / 2:.2f}*eq(n,{c + 1})" for c in cuts)
    tmp = path[:-4] + "_noflash.mp4"
    os.replace(path, tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-vf", f"eq=brightness='{terms}':eval=frame",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", path], check=True)
    os.remove(tmp)


B = "BLACK"
W = "WHITE"
R = []   # key, line, hook, after, idea, post

# BT18 white moves first. (chess) - COUPLE in one take, mirrored, real speed; white first, checkerboard 2 x 2
g = gr(b=-0.01, c=1.05, s=0.92)
R.append(("BT18_white-moves-first", "white moves first.",
          [couple_red(g, zoom=1.1, crop_x=0.5, crop_y=0.62, flip=True)],
          pages("18", [("WF", W), ("KF", B), ("XWF", W), ("ZF", B), ("WB", W), ("KB", B)], "slate") +
          [fin(vgrid([P["WF"], P["KF"], P["ZF"], P["XWF"]], o("18f"), "N° VII", "FIRST LOOK", "slate"), 3)],
          "COUPLE in one take (V01's hook, mirrored, 1.0x, tighter); white first; finale 2 x 2 set like a chessboard", None))

# BT19 red underneath. for luck. (superstition) - COUPLE cut on the beats, pushing in on every cut; oxblood
g = gr(b=-0.014, c=1.06, s=0.92); g.update(rm=0.02)
R.append(("BT19_red-underneath-for-luck", "red underneath.\nfor luck.",
          [sh("COUPLE", 1.3, 39, g, zoom=1.0, crop_y=0.55), sh("COUPLE", 2.6, 37, g, zoom=1.15, crop_y=0.65),
           couple_red(g, zoom=1.32, crop_x=0.45, crop_y=0.78)],
          pages("19", [("KF", "RED INSIDE  ·  BLACK"), ("WF", "RED INSIDE  ·  WHITE"), ("ZF", "RED INSIDE  ·  BLACK"),
                       ("XWF", "RED INSIDE  ·  WHITE"), ("KF", "RED INSIDE  ·  BLACK"), ("XWF", "RED INSIDE  ·  WHITE")],
                "oxblood", scale=0.92, spot=(0.5, 0.38, 0.56, 0.3)) +
          [fin(vside(P["KF"], P["XWF"], o("19f"), "N° VII", "FIRST LOOK", "oxblood", title="EX MUSEO"), 3)],
          "COUPLE only, three pieces of the walk cut on the beats, zoom 1.0 -> 1.15 -> 1.32 onto the soles; RED INSIDE, oxblood", None))

# BT20 she has a type. (dating) - her hand tight -> the walk, wide -> red on both; HER TYPE labels, smoke
g = gr(b=-0.012, c=1.05, s=0.9); g.update(rh=0.015)
R.append(("BT20_she-has-a-type", "she has a type.",
          [sh("COUPLE", 0.55, 21, g, zoom=1.35, crop_x=0.3, crop_y=0.7),
           couple_red(g, zoom=1.0, crop_x=0.5, crop_y=0.6)],
          pages("20", [("KF", "HER TYPE  ·  BLACK"), ("WF", "HERS  ·  WHITE"), ("ZF", "HER TYPE  ·  BLACK"),
                       ("XWF", "HERS  ·  WHITE"), ("KB", "HER TYPE  ·  BLACK"), ("WB", "HERS  ·  WHITE")], "smoke") +
          [fin(vstacked2(P["PF"], P["ZPF"], o("20f"), "N° VII", tone="smoke"), 3)],
          "COUPLE: her hand tight (0.7 s) -> the whole walk wide, not mirrored -> red on both; HER TYPE / HERS, smoke", None))

# BT21 mars and venus. (Roman myth) - bright: his shoes in the flash -> the marble forward, backwards, the red heel
gb = gr(b=0.02, c=1.06, s=0.86, g=1.05)
R.append(("BT21_mars-and-venus", "mars and venus.",
          [sh("COUPLE", 1.45, 39, gb, zoom=1.25, crop_x=0.5, crop_y=0.62), sh("MARBLE", 0.0, 19, gb, zoom=1.1, crop_y=0.5),
           sh("MARBLE", 0.45, 18, gb, zoom=1.2, crop_y=0.5, reverse=True),
           sh("MARBLE", 0.49, 18, gb, zoom=1.25, crop_x=0.55, crop_y=0.55, flip=True)],
          pages("21", [("ZF", "MARS  ·  BLACK"), ("XWF", "VENUS  ·  WHITE"), ("KF", "MARS  ·  BLACK"),
                       ("WF", "VENUS  ·  WHITE"), ("ZB", "MARS  ·  BLACK"), ("XWB", "VENUS  ·  WHITE")], "bronze") +
          [fin(vside(P["ZF"], P["XWF"], o("21f"), "N° VII", cat(7, "MARS  ·  VENUS"), "bronze"), 3)],
          "bright: COUPLE his shoes in the flash (Kirill's ref) -> MARBLE forward -> backwards -> red heel, mirrored; MARS / VENUS, bronze", None))

# BT22 no photos, please. (paparazzi) - bright and fast, a camera flash on every cut: shoes close -> shoes wide ->
# terrazzo -> marble wide -> red heel; UNSEEN labels, vitrine; zip fronts and backs 2 x 2
gb = gr(b=0.02, c=1.07, s=0.85, g=1.06)
R.append(("BT22_no-photos-please", "no photos,\nplease.",
          [sh("COUPLE", 1.5, 21, gb, zoom=1.4, crop_x=0.5, crop_y=0.62), sh("COUPLE", 1.9, 18, gb, zoom=1.0, crop_y=0.55),
           sh("SOLES", 3.3, 19, gb, zoom=1.1, crop_y=0.5), sh("MARBLE", 0.05, 18, gb, zoom=1.0, crop_y=0.5, flip=True),
           sh("MARBLE", 0.49, 18, gb, zoom=1.3, crop_x=0.5, crop_y=0.55)],
          pages("22", [("XWF", "UNSEEN  ·  WHITE"), ("ZF", "UNSEEN  ·  BLACK"), ("WF", "UNSEEN  ·  WHITE"),
                       ("KF", "UNSEEN  ·  BLACK"), ("XWB", "UNSEEN  ·  WHITE"), ("ZB", "UNSEEN  ·  BLACK")], "vitrine",
                scale=0.9, spot=(0.5, 0.4, 0.62, 0.36)) +
          [fin(vgrid([P["ZF"], P["XWF"], P["ZB"], P["XWB"]], o("22f"), "N° VII", "FIRST LOOK", "vitrine"), 3)],
          "bright, 5 shots with a camera flash on every hook cut: COUPLE shoes close -> wide -> SOLES terrazzo -> MARBLE wide -> red heel; UNSEEN, vitrine",
          lambda p: flash(p, [21, 39, 58, 76])))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea, post) in enumerate(R):
        ledger.append(["1126a", k, "bad together track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=50000 + i)
        if post:
            post(OUT + k + ".mp4")
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1126_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1126a.json"), "w"), indent=1)
