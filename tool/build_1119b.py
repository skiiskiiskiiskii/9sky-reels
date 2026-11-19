#!/usr/bin/env python3
"""made 2026-11-19, batch 1119b: 8 reels, all four pieces in every reel (black / white quarter zip, black / white zip
hoodie), lines about the choice between them, hooks reworked harder so Instagram can't match them to the old ones.
E07-E08: EsDeeKid - Mist baked in (Kirill asked), the rest: Kirill adds the sound in Instagram.

Hooks: 3-4 Louboutin shots at real speed; tighter reframing (zoom up to 1.35 on other parts of the frame), mirroring,
a middle shot played backwards, a light tint per reel (warm / cool), one grey-with-red; four different red endings.
Pages: four singles + a 2 x 2 page of all four (tool/vitrine2.vgrid), or pairs side by side (black pair, white pair,
then the backs) + the 2 x 2 page; tones vary. Mist reels: pages switch on the track's big hits."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
from vitrine2 import vpage2, vside, vgrid
from build_1119a import gr, sh, couple_red, soles_red, marble_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-19b/"
F05, LV, MIST = 60 / 99.0, 0.632, 60 / 97.5
MIST_AUDIO = (os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "music", "EsDeeKid - Mist (extended intro).mp3"),
              29.595 - 3.13)
FRONTS = ["KF", "WF", "ZF", "XWF"]
BACKS = ["KB", "WB", "ZB", "XWB"]
SUB = {"KF": COLLAR, "WF": COLLAR, "ZF": HOOD, "XWF": HOOD, "KB": ARA, "WB": ARA, "ZB": ARA, "XWB": ARA}
NAME = {"KF": "BLACK QUARTER ZIP", "WF": "WHITE QUARTER ZIP", "ZF": "BLACK ZIP HOODIE", "XWF": "WHITE ZIP HOODIE"}
NUM = ["N° I", "N° II", "N° III", "N° IV", "N° V"]


def o(name):
    return O + "e1119_" + name + ".jpg"


def singles(tag, keys, tone, grid_keys, scale=0.88, **kw):
    """four single pages, 1 beat each, then all four on one page for 2 beats"""
    out = [(1, img(vpage2(P[k], o(f"{tag}{i}"), NUM[i], cat(i + 1, NAME.get(k, SUB[k])), tone, scale=scale, **kw), 1))
           for i, k in enumerate(keys)]
    out.append((2, img(vgrid([P[k] for k in grid_keys], o(f"{tag}g"), NUM[4], "FIRST LOOK", tone), 1)))
    return out


def pairs(tag, tone, beats=(1, 1, 1, 1, 2), grid=FRONTS):
    """black pair, white pair, black backs, white backs, then all four"""
    sets = [("KF", "ZF", "BLACK"), ("WF", "XWF", "WHITE"), ("KB", "ZB", ARA), ("WB", "XWB", ROME)]
    out = [(b, img(vside(P[a], P[c], o(f"{tag}{i}"), NUM[i], cat(i + 1, lab), tone), 1))
           for i, ((a, c, lab), b) in enumerate(zip(sets, beats))]
    out.append((beats[-1], img(vgrid([P[k] for k in grid], o(f"{tag}g"), NUM[4], "FIRST LOOK", tone), 1)))
    return out


def nails_heel(n, grade, **kw):                  # NAILS heel lift, framed so the heel stays in the picture
    return sh("NAILS", round(6.0 - n / 30, 3), n, grade, zoom=1.05, crop_x=0.0, crop_y=0.5, **kw)


R = []   # key, line, beat, hook, after, audio, idea

g = gr(b=-0.012, c=1.05, s=0.92); g.update(rm=0.04, bm=-0.03)                      # warm
R.append(("E01_which-one-would-you-wear", "which one\nwould you wear?", F05,
          [sh("SOLES", 1.0, 22, g, zoom=1.35, crop_x=0.35, crop_y=0.45), sh("NAILS", 2.2, 24, g, zoom=1.3, flip=True),
           sh("COUPLE", 2.5, 22, g, zoom=1.35, crop_x=0.3, crop_y=0.85), soles_red(26, g, zoom=1.25, crop_y=0.62)],
          singles("e01", FRONTS, "vitrine", FRONTS), None,
          "4 shots, tight reframes: SOLES rings -> NAILS mirrored -> COUPLE shoes close -> SOLES logo; warm tint"))

g = gr(b=-0.01, c=1.04, s=0.86); g.update(bs=0.04, bm=0.02)                        # cool
R.append(("E02_black-or-white-collar-or-hood", "black or white,\ncollar or hood?", LV,
          [sh("COUPLE", 1.6, 36, g, zoom=1.0, flip=True), sh("SOLES", 2.6, 30, g, zoom=1.15, reverse=True),
           couple_red(g, zoom=1.3, crop_x=0.42, crop_y=0.78, flip=True)],
          pairs("e02", "ink"), None,
          "COUPLE wide mirrored -> SOLES pumps BACKWARDS -> COUPLE tight mirrored red sole; pairs + 2x2; LV Sandals"))

g = gr(b=-0.016, c=1.06, s=0.9, g=0.97); g.update(rm=0.03, rh=0.02)
R.append(("E03_two-colors-two-cuts", "two colors,\ntwo cuts.", F05,
          [sh("NAILS", 0.9, 30, g, zoom=1.25, crop_y=0.5), sh("COUPLE", 0.5, 24, g, zoom=1.3, crop_y=0.6, reverse=True),
           sh("COUPLE", 3.1, 20, g, zoom=1.0, crop_y=0.6), marble_red(20, g)],
          singles("e03", ["ZF", "KF", "XWF", "WF"], "bronze", BACKS, scale=0.84), None,
          "NAILS close -> COUPLE her nails BACKWARDS -> COUPLE wide -> MARBLE; hoods first; 2x2 of the backs"))

g = gr(b=-0.01, c=1.08, s=1.0)
R.append(("E04_the-whole-first-look", "the whole\nfirst look.", F05,
          [sh("SOLES", 2.4, 30, g, zoom=1.2, keep_red=True), sh("COUPLE", 2.0, 34, g, zoom=1.1, flip=True, keep_red=True),
           nails_heel(30, g, keep_red=True)],
          singles("e04", BACKS, "smoke", FRONTS, scale=0.9), None,
          "grey hook, only red: SOLES pumps -> COUPLE mirrored -> NAILS heel lift; backs first, 2x2 of the fronts"))

g = gr(b=-0.012, c=1.04, s=0.9); g.update(bs=0.05)
R.append(("E05_pick-one-for-tonight", "pick one\nfor tonight.", LV,
          [sh("COUPLE", 0.8, 26, g, zoom=1.2), sh("NAILS", 1.8, 24, g, zoom=1.1, flip=True),
           sh("SOLES", 1.6, 18, g, zoom=1.3, crop_x=0.55), couple_red(g, zoom=1.0, crop_y=0.6)],
          singles("e05", ["XWF", "ZF", "WF", "KF"], "oxblood", FRONTS, scale=0.86, cy=0.48), None,
          "4 shots: COUPLE her nails -> NAILS mirrored -> SOLES watch close -> COUPLE wide red sole; cool tint; LV Sandals"))

g = gr(b=-0.014, c=1.05, s=0.94, g=1.02)
R.append(("E06_red-on-all-four", "red\non all four.", F05,
          [sh("SOLES", 0.6, 30, g, zoom=1.1, flip=True), sh("NAILS", 2.8, 24, g, zoom=1.2, reverse=True),
           sh("COUPLE", 3.4, 20, g, zoom=1.25, crop_y=0.85), marble_red(20, g, flip=True)],
          pairs("e06", "slate"), None,
          "SOLES mirrored -> NAILS BACKWARDS -> COUPLE shoes close -> MARBLE mirrored; pairs + 2x2"))

# Mist baked in: pages on the track's big hits (3.13, 4.515, 5.592, 6.976 s) -> 2.25 / 1.75 / 2.25 beats
g = gr(b=-0.012, c=1.05, s=0.9); g.update(rm=0.02)
R.append(("E07_black-white-collar-hood_mist", "black, white,\ncollar, hood.", MIST,
          [sh("COUPLE", 2.0, 34, g, zoom=1.15), sh("SOLES", 1.2, 32, g, zoom=1.2, crop_x=0.45),
           couple_red(g, zoom=1.3, crop_x=0.42, crop_y=0.78)],
          [(2.25, img(vside(P["KF"], P["ZF"], o("e07a"), "N° I", cat(1, "BLACK"), "vitrine"), 1)),
           (1.75, img(vside(P["WF"], P["XWF"], o("e07b"), "N° II", cat(2, "WHITE"), "vitrine"), 1)),
           (2.25, img(vgrid([P[k] for k in BACKS], o("e07g"), "N° III", "FIRST LOOK", "vitrine"), 1))],
          MIST_AUDIO, "Mist baked in; COUPLE -> SOLES -> COUPLE tight red sole; black pair, white pair, 2x2 backs"))

g = gr(b=-0.01, c=1.04, s=0.88); g.update(bs=0.03)
R.append(("E08_which-one-first_mist", "which one\nfirst?", MIST,
          [sh("NAILS", 1.2, 32, g, zoom=1.15, flip=True), sh("COUPLE", 2.8, 34, g, zoom=1.0, crop_y=0.6),
           soles_red(28, g, zoom=1.2, crop_y=0.62)],
          [(2.25, img(vside(P["ZF"], P["XWF"], o("e08a"), "N° I", cat(1, HOOD), "ink"), 1)),
           (1.75, img(vside(P["KF"], P["WF"], o("e08b"), "N° II", cat(2, COLLAR), "ink"), 1)),
           (2.25, img(vgrid([P[k] for k in FRONTS], o("e08g"), "N° III", "FIRST LOOK", "ink"), 1))],
          MIST_AUDIO, "Mist baked in; NAILS mirrored -> COUPLE wide -> SOLES logo; hoods, collars, 2x2 fronts"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, beat, hook, after, audio, idea) in enumerate(R):
        track = "Mist baked in" if audio else ("LV Sandals from 0:09.5" if beat == LV else "F05 / mr popular")
        ledger.append(["1119b", k, track, line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=43000 + i, beat=beat, total_beats=12, audio=audio)
        json.dump(dict(hook=hook, line=line, after=after, beat=beat, track=track),
                  open(os.path.join(SP, f"e1119_{k}.json"), "w"), indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1119b.json"), "w"), indent=1)
