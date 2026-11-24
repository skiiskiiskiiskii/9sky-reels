#!/usr/bin/env python3
"""2026-11-24 03:10, batch 1124a: 10 louboutin reels M01-M10, all 6.77 s (Kirill: nothing over 6-7 s, he does not post
the long loops).

What the numbers 11-15..11-23 say (Metricool, ~100 trial reels):
- almost every trial sits at 1.3-1.6K (the first test audience); a few get pushed: K05 18.1K, L01 16.5K, K02 9.0K,
  K01 7.4K, H08r 6.6K, X03 5.0K, N03 4.5K
- every reel above 4K had 63-72 % past 3 s; nothing under ~55 % went past 2.3K (roses, moodboards, locations,
  question lines all 25-45 %)
- the two biggest (K05, L01) and F05 share one build: COUPLE in full frame with both of them, red sole right at the cut,
  short italic line on top about him / her, vitrine pages, quarter zip pair finale.
So: half the batch scales that build with new lines and small visual differences (crop, mirror, speed, pages),
the other half re-uses the next-best mechanics (K01 SOLES, K02 / H08 nails -> soles slow-down, MARBLE -> heel lift).
Quarter zip only, F05 sound, top italic line everywhere (all hits had it), no effects."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import cat, COLLAR, ARA, ROME, P
from build_1115 import lb, clip, t, DROP, MARBLE_LEN
from build_1122 import build

BMP = 60 / 99.0
C2 = DROP - 2 * BMP


def ramp(key, onset, total, slow=0.55, rate=0.5, pre=1.0, **kw):
    """normal speed, then a smooth slow-down on the red for the last `slow` s (K02 / H08 recipe)"""
    s_end = onset + 0.13
    s_slow = s_end - slow * rate
    first = total - slow
    return [lb(key, start=s_slow - first * pre, dur=round(first, 3), speed=pre, **kw),
            lb(key, start=s_slow, speed=rate, smooth=True, **kw)]


def pg(*items):
    out = []
    for i, it in enumerate(items):
        k, sub = (it, None) if isinstance(it, str) else it
        out.append(("p", k, sub or (cat(i + 1, ARA, ROME) if k.endswith("B") else cat(i + 1, COLLAR))))
    return out


HIS, HERS = ("KF", cat(1, "HIS  ·  BLACK")), ("WF", cat(2, "HERS  ·  WHITE"))
M = [  # key, tone, hook, texts, layout, finale, opts, idea
    ("M01_she-wore-red", "vitrine", [lb("COUPLE", speed=1.12, zoom=1.0, crop_y=0.6)],
     t("she wore red."), pg("KF", "KB"), ("PF", "PB", 4), {},
     "K05/L01 build: COUPLE full frame, red at the cut; black qz pages, pair finale"),
    ("M02_he-matched-her", "vitrine", [lb("COUPLE", speed=1.05, zoom=1.0, crop_y=0.55, flip=True)],
     t("he matched her."), pg("KF", "WB"), ("PF", "PB", 4), {},
     "K05/L01 build mirrored, a touch slower; black front, white back"),
    ("M03_dressed-for-her", "vitrine", [lb("COUPLE", speed=1.0, zoom=1.05, crop_x=0.55, crop_y=0.62)],
     t("dressed for her."), pg("WF", "WB"), ("PF", "PB", 4), {},
     "K05/L01 build at normal speed, slight crop right; white qz pages"),
    ("M04_his-black-her-white", "vitrine", [lb("COUPLE", speed=1.12, zoom=1.0, crop_y=0.6, flip=True)],
     t("his black, her white."), [("p",) + HIS, ("p",) + HERS], ("PF", "PB", 4), {},
     "K05 twin (18.1K): mirrored, new line; HIS black / HERS white pages"),
    ("M05_start-with-her-shoes", "oxblood", [lb("COUPLE", zoom=1.2, crop_x=0.45, crop_y=0.74, flip=True)],
     t("start with\nher shoes."), pg("KF", "KB"), ("KF", "KB", 4), {},
     "F05 variant (63K): tight COUPLE mirrored, new line"),
    ("M06_red-for-her-red-for-him", "vitrine", [lb("SOLES", start=1.45, speed=1.05, zoom=1.05, crop_y=0.6, flip=True)],
     t("red for her,\nred for him."), [("p",) + HIS, ("p", "KB", cat(2, ARA, ROME))], ("PF", "PB", 4), {},
     "K01 variant (7.4K): SOLES mirrored - her red nails, his logo sole is red too"),
    ("M07_its-red-underneath", "slate",
     [lb("NAILS", start=1.6, dur=round(C2, 3), speed=1.1, zoom=1.0)]
     + ramp("COUPLE", 4.7, DROP - C2, slow=0.6, crop_y=0.76, crop_x=0.45, zoom=1.3),
     t("it's red\nunderneath."), pg("KF", "KB"), ("PF", "PB", 4), {},
     "K02 / H08 recipe (9.0K / 12.6K): black nails -> COUPLE slow-down on the red sole, not mirrored"),
    ("M08_look-closer", "vitrine",
     [clip(P["SOLES"], start=1.4, dur=1.3, zoom=1.1),
      lb("SOLES", start=4.25, speed=0.85, zoom=1.15, crop_y=0.55, smooth=True)],
     t("look closer."), pg("WF", "WB"), ("PF", "PB", 4), {},
     "H08 idea on SOLES: black nails flip red -> his logo sole and her soles, slightly slowed"),
    ("M09_her-heels-first", "oxblood",
     [clip(P["MARBLE"], start=0.0, dur=MARBLE_LEN, zoom=1.1),
      lb("NAILS", start=4.5, speed=1.0, zoom=1.05)],
     t("her heels first."), pg("KF", "KB"), ("KF", "KB", 4), {},
     "MARBLE -> NAILS red nails -> heel lift with the red sole at the cut"),
    ("M10_black-on-top-red-under", "slate", [lb("NAILS", start=2.85, speed=1.02, zoom=1.0)],
     t("black on top,\nred under."), pg("KF", "WF"), ("PF", "PB", 4), {},
     "R03 variant (3.3K, 69.6 %): NAILS black nails -> red flip -> red sole at the cut"),
]

if __name__ == "__main__":
    build("1124a", M, "m1124", 40000, tag="m")
