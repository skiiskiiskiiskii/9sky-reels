#!/usr/bin/env python3
"""2026-11-22 evening, batch 1123a: 20 louboutin reels L01-L20 for 11-23..11-26 (Kirill: "each one unique in its own way,
but similar - somewhere a line, somewhere a shade or something else").
Same F05 skeleton (hook to the drop at 3.13 s, 2 vitrine pages, EX MUSEO finale, mrpopular timing, F05 sound),
quarter zip only (louboutin rule). What changes from reel to reel:
- hook: clip segment, start, mirror, crop, speed, freeze on the red sole, jump cuts inside a clip, two-clip mixes
- finish before the drop: line on top (italic), small upright serif in the middle / top / bottom, line at the bottom,
  no line at all; soft shade from the top / bottom / both; letterbox bars. All of it ends on the drop, pages stay clean.
- pages: order (back first on two), black / white / mixed, tone, finale pairing; 3 long loops (~10.4 s).
No zoom moves, strobes, colour effects or grain (Kirill 11-22: those look cheap)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import cat, COLLAR, ARA, ROME, P
from build_1115 import lb, clip, t, DROP, MARBLE_LEN
from build_1122 import build, mid


def serif(text, y=0.48, size=56):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": size, "scrim": 0, "font": "cg-400"}]


def freeze(key, hold_src, hold=0.5, speed=1.0, **kw):
    first = DROP - hold
    return [lb(key, start=hold_src - first * speed, dur=round(first, 3), speed=speed, **kw),
            lb(key, start=hold_src, speed=0.03, **kw)]


def pages(*items):
    return [("p", k, cat(i + 1, ARA, ROME) if k.endswith("B") else cat(i + 1, COLLAR)) for i, k in enumerate(items)]


def mlen(speed):
    return round(MARBLE_LEN / speed, 3)


NO = []
L = [  # key, tone, hook, texts, layout, finale, opts, idea
    ("L01_she-chose-red", "vitrine", [lb("COUPLE", zoom=1.0, flip=True)], t("she chose red."),
     pages("KF", "KB"), ("PF", "PB", 4), {}, "COUPLE red at the cut, full frame mirrored; F05 line on top"),
    ("L02_matching-red-bottoms", "slate", [lb("SOLES", start=1.0, speed=1.1, zoom=1.1)], serif("matching red bottoms."),
     pages("WF", "WB"), ("WF", "WB", 4), {"hook_fx": {"bars": 0.1}},
     "SOLES 1.0 @1.1: red nail flip -> walk -> logo sole at the cut; letterbox bars"),
    ("L03_red-under-black-nails", "oxblood", [lb("NAILS", start=2.95, speed=1.0, zoom=1.1, crop_y=0.45)],
     serif("red under black nails."), pages("KF", "WB"), ("KF", "WB", 4), {"hook_fx": {"shade_bottom": 0.5}},
     "NAILS 2.95: black nails flip red, heel lift red sole; small serif centre, shade bottom"),
    ("L04_her-red-heels", "vitrine",
     [clip(P["MARBLE"], start=0.0, dur=mlen(0.6), speed=0.6, smooth=True, zoom=1.1),
      lb("COUPLE", start=4.4, speed=1.0, zoom=1.15, crop_y=0.74)],
     t("her red heels.", y=0.78), pages("WF", "KF"), ("PF", "PB", 4), {},
     "MARBLE slowed 0.6 -> COUPLE red soles; italic line at the bottom"),
    ("L05_wear-her-color", "oxblood",
     [clip(P["SOLES"], start=1.4, dur=1.2, zoom=1.15), lb("COUPLE", start=3.8, speed=1.0, zoom=1.2, crop_y=0.74)],
     serif("wear her color.", y=0.16, size=64), pages("KF", "KB"), ("KF", "WF", 4), {},
     "SOLES red nail flip -> COUPLE his shoes -> her red soles; small serif on top"),
    ("L06_couple-outfit-idea", "slate", freeze("COUPLE", 4.8, zoom=1.15, crop_x=0.55, crop_y=0.72), t("couple outfit idea."),
     pages("WF", "WB"), ("WF", "KB", 4), {"hook_fx": {"shade_top": 0.55, "shade_bottom": 0.55}},
     "COUPLE, red sole held 0.5 s before the cut; shade top and bottom"),
    ("L07_red-soles-only", "vitrine", [lb("SOLES", start=4.6, speed=0.8, zoom=1.15, crop_y=0.55, smooth=True)],
     serif("red soles only."), pages("KF", "KB"), ("KF", "KB", 4), {},
     "SOLES 4.6 slowed 0.8: red soles from the first frame; small serif centre"),
    ("L08_shes-wearing-red", "oxblood",
     [clip(P["NAILS"], start=1.5, dur=1.6, zoom=1.05), lb("NAILS", start=5.0, speed=1.0, zoom=1.05)],
     t("she's wearing red."), pages("WF", "KF"), ("WF", "WB", 4), {"hook_fx": {"bars": 0.08}},
     "NAILS jump cut: black nails -> heel lift red sole (red nails skipped); top line + thin bars"),
    ("L09_date-night-shoes", "slate",
     [clip(P["MARBLE"], start=0.0, dur=mlen(1.0), zoom=1.3, crop_y=0.6, flip=True),
      lb("SOLES", start=5.9, speed=0.8, zoom=1.15, crop_y=0.55, smooth=True)],
     serif("date night shoes.", y=0.82), pages("KF", "KB"), ("PF", "PB", 4), {},
     "MARBLE mirrored tight -> SOLES both red soles slowed; small serif at the bottom"),
    ("L10_his-collar-matches-her-heels", "vitrine", [lb("COUPLE", start=1.55, speed=1.0, zoom=1.0)],
     t("his collar matches\nher heels."),
     pages("KF", "KB")[:2] + [("c", mid("NAILS", 5.5, 3, speed=0.55, zoom=1.05))] + [("p", "PF", cat(3, COLLAR))],
     ("PF", "PB", 6), {"loop_frames": 10}, "LONG loop: COUPLE wide -> qz pages -> NAILS heel lift slowed -> pair"),
    ("L11_what-he-wears-next-to-her", "vitrine", [lb("SOLES", start=0.2, speed=1.3, zoom=1.0)], t("what he wears\nnext to her.", y=0.76),
     pages("WF", "WB"), ("PF", "PB", 4), {"hook_fx": {"shade_bottom": 0.6}},
     "SOLES from the start @1.3 (boots beside her heels -> nails -> logo sole); shade bottom"),
    ("L12_the-color-of-her-heels", "oxblood",
     [clip(P["COUPLE"], start=0.4, dur=1.2, speed=0.6, smooth=True, zoom=1.1),
      lb("COUPLE", start=4.6, speed=0.9, zoom=1.2, crop_y=0.74)],
     serif("the color of her heels."), pages("KF", "WF"), ("KF", "WF", 4), {},
     "COUPLE nail flip slowed -> COUPLE red soles; small serif centre"),
    ("L13_date-night-details", "slate", [lb("NAILS", start=3.6, speed=0.85, zoom=1.15, crop_y=0.5, smooth=True)], serif("date night details.", y=0.2, size=64),
     pages("KB", "KF"), ("KF", "KB", 4), {"hook_fx": {"bars": 0.12}},
     "NAILS 3.6 slowed: red nails -> heel lift; wide bars; back page first"),
    ("L14_she-walks-in-red", "vitrine",
     [clip(P["MARBLE"], start=0.0, dur=mlen(0.75), speed=0.75, smooth=True, zoom=1.15),
      lb("NAILS", start=4.6, speed=1.0, zoom=1.05, flip=True)],
     t("she walks in red."), pages("WF", "WB"), ("WF", "KB", 4), {},
     "MARBLE slowed -> NAILS mirrored heel lift; top line"),
    ("L15_his-fit-her-heels", "slate", [lb("SOLES", start=2.9, speed=1.0, zoom=1.1, flip=True)],
     serif("his fit, her heels."),
     pages("WF", "WB")[:2] + [("c", mid("COUPLE", 4.5, 3, speed=0.6, zoom=1.15, crop_y=0.74))] +
     [("p", "KF", cat(3, COLLAR))], ("PF", "PB", 6), {"loop_frames": 10},
     "LONG loop: SOLES walk -> logo sole mirrored -> white qz -> COUPLE red soles slowed -> black qz -> pair"),
    ("L16_his-fit-for-date-night", "slate", [lb("COUPLE", zoom=1.35, crop_x=0.4, crop_y=0.78)], t("his fit for date night."),
     pages("KB", "KF"), ("KF", "KB", 4), {"hook_fx": {"shade_top": 0.6}},
     "COUPLE tight on her heel; shade top; back page first"),
    ("L17_next-to-her-heels", "vitrine",
     [clip(P["SOLES"], start=1.3, dur=1.3, zoom=1.1), lb("SOLES", start=4.25, speed=1.0, zoom=1.15, crop_y=0.55)],
     t("next to her heels.", y=0.78), pages("WF", "KB"), ("WF", "WB", 4), {},
     "SOLES jump cut: red nail flip -> his logo sole next to her heels; italic line at the bottom"),
    ("L18_red-bottoms-tonight", "oxblood",
     [clip(P["NAILS"], start=0.0, dur=1.2, zoom=1.05), lb("NAILS", start=4.45, speed=1.0, zoom=1.05)], serif("red bottoms tonight."),
     pages("KF", "KB"), ("PF", "PB", 4), {"hook_fx": {"bars": 0.1, "shade_bottom": 0.45}},
     "NAILS heels on the floor -> red nails tail -> heel lift; bars + shade bottom"),
    ("L19_red-heels-black-shoes", "oxblood",
     [clip(P["MARBLE"], start=0.0, dur=mlen(0.5), speed=0.5, smooth=True, zoom=1.1, flip=True),
      lb("COUPLE", start=5.3, speed=1.0, zoom=1.15, crop_y=0.74)],
     serif("red heels, black shoes.", y=0.16, size=64), pages("WF", "WB"), ("KF", "WF", 4), {},
     "MARBLE mirrored half speed -> COUPLE red soles walking away; small serif on top"),
    ("L20_match-her-heels", "oxblood", [lb("NAILS", start=3.0, speed=1.0, zoom=1.2, crop_y=0.4)],
     t("match her heels."),
     pages("KF", "KB")[:2] + [("c", mid("SOLES", 5.6, 3, speed=0.75, zoom=1.15, crop_y=0.55))] +
     [("p", "WF", cat(3, COLLAR))], ("PF", "PB", 6), {"loop_frames": 10},
     "LONG loop: NAILS red nails -> red sole -> black qz -> SOLES both soles slowed -> white qz -> pair"),
]

if __name__ == "__main__":
    build("1123a", L, "l1123", 39000, tag="l")
