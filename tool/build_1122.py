#!/usr/bin/env python3
"""2026-11-22, batch 1122a: 6 reels (Kirill: same hooks, but mix things so Instagram cuts views less).
Products: IX quarter zip and IX zip hoodie, black and white (zip hoodie allowed with louboutins this time).
Variation against the ~70 earlier reels on the same 4 clips: new clip segments and orders, mirror/zoom/speed
changes, one grey-world reel (only the red keeps its colour), three long loops (the 10-11 s format that did best
on 11-17: X03 4.9K, X04 2.9K) with a second red clip in the middle and a crossfade back to the first frame,
light grain on two reels, new finale pairings. Every on-screen line is new (checked against the ledger and the
11-17..11-20 folders).

T01 only the red.            - SOLES 1.22 @1.12 mirrored, grey world: red nail flip, then the logo sole at the cut;
                               black quarter zip + black zip hoodie, finale both blacks
T02 he waits, she arrives.   - LONG. COUPLE mirrored full frame (his shoes standing, her red soles at the cut);
                               white zip hoodie pages, mid SOLES both red soles slowed, black zip page, zip pair finale
T03 her red, his red.        - NAILS 2.92 mirrored: black nails, red nail flip, heel lift with red sole at the cut;
                               black quarter zip, pair finale
T04 stand next to her.       - COUPLE jump cut: her hand at his feet (nails flip red) -> his shoes -> her red soles;
                               white quarter zip, finale white quarter zip + white zip hoodie; grain
T05 the red was her idea.    - MARBLE slowed 0.75, zoomed -> NAILS red nails -> red sole at the cut;
                               black zip hoodie (red-lined hood), front/back finale
T06 for the man beside her.  - LONG. SOLES from frame 0 at 1.4x (his boots beside her heels, nails, walk, logo sole);
                               quarter zip black/white, mid MARBLE slow, pair finale; grain
mrpopular timing (drop 3.13 s, 99 BPM) - post with the F05 audio."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, SP, P, O
from build_1115 import lb, clip, t, MARBLE_LEN, MP
from vitrine import vpage, vstacked

NUMS = ["I", "II", "III", "IV", "V"]


def mid(src_key, start, beats, speed=1.0, **kw):
    """a clip in the middle of a long loop, measured in beats"""
    d = clip(P[src_key], start=start, speed=speed, smooth=speed < 1, **kw)
    d.pop("until", None)
    d["beats"] = beats
    return d


M75 = round(MARBLE_LEN / 0.75, 3)
T = [  # key, tone, hook, text, layout [("p", mockup, sub) | ("c", seg)], finale (a, b, beats), opts, idea
    ("T01_only-the-red", "slate",
     [lb("SOLES", start=1.22, speed=1.12, zoom=1.1, crop_y=0.6, flip=True, keep_red=True)],
     t("only the red."),
     [("p", "KF", cat(1, COLLAR)), ("p", "ZF", cat(2, HOOD))], ("KF", "ZF", 4), {},
     "SOLES 1.22 @1.12 mirrored, grey world (keep_red): red nail flip, logo sole at the cut; black qz + black zip"),
    ("T02_he-waits-she-arrives", "vitrine",
     [lb("COUPLE", start=1.62, speed=1.0, zoom=1.0, flip=True)],
     t("he waits,\nshe arrives."),
     [("p", "XWF", cat(1, HOOD)), ("p", "XWB", cat(2, ARA, ROME)),
      ("c", mid("SOLES", 5.6, 4, speed=0.75, zoom=1.1, crop_y=0.6)),
      ("p", "ZF", cat(3, HOOD))], ("ZPF", "ZPB", 6), {"loop_frames": 10},
     "LONG loop: COUPLE mirrored full frame -> white zip pages -> SOLES both red soles slowed -> black zip -> zip pair"),
    ("T03_her-red-his-red", "oxblood",
     [lb("NAILS", start=2.92, speed=1.0, zoom=1.05, flip=True)],
     t("her red,\nhis red."),
     [("p", "KF", cat(1, COLLAR)), ("p", "KB", cat(2, ARA, ROME))], ("PF", "PB", 4), {},
     "NAILS 2.92 mirrored: black nails, red nail flip, heel lift red sole at the cut; black qz, pair finale"),
    ("T04_stand-next-to-her", "vitrine",
     [clip(P["COUPLE"], start=0.0, dur=1.05, zoom=1.15, crop_y=0.7),
      lb("COUPLE", start=2.82, speed=1.0, zoom=1.15, crop_y=0.7)],
     t("stand next\nto her."),
     [("p", "WF", cat(1, COLLAR)), ("p", "WB", cat(2, ARA, ROME))], ("WF", "XWF", 4), {"grain": 3},
     "COUPLE jump cut: her hand at his feet (nails flip red) -> his shoes -> her red soles; white qz, white qz+zip finale"),
    ("T05_the-red-was-her-idea", "oxblood",
     [clip(P["MARBLE"], start=0.0, dur=M75, speed=0.75, zoom=1.25, smooth=True),
      lb("NAILS", start=4.4, speed=1.0, zoom=1.05)],
     t("the red was\nher idea."),
     [("p", "ZF", cat(1, HOOD)), ("p", "ZB", cat(2, ARA, ROME))], ("ZF", "ZB", 4), {},
     "MARBLE slowed 0.75 zoomed -> NAILS red nails -> red sole at the cut; black zip hoodie front/back"),
    ("T06_for-the-man-beside-her", "slate",
     [lb("SOLES", start=0.1, speed=1.4, zoom=1.0)],
     t("for the man\nbeside her."),
     [("p", "KF", cat(1, COLLAR)), ("p", "WF", cat(2, COLLAR)),
      ("c", mid("MARBLE", 0.0, 3, speed=0.6, zoom=1.1, flip=True)),
      ("p", "KB", cat(3, ARA, ROME))], ("PF", "PB", 6), {"loop_frames": 10, "grain": 3},
     "LONG loop: SOLES from 0 at 1.4x (his boots beside her heels -> logo sole) -> qz pages -> MARBLE slow -> pair"),
]


def build(batch, rows, prefix, seed0, tag="t"):
    ledger = []
    for i, (k, tone, hook, texts, layout, fin, opts, idea) in enumerate(rows):
        segs, n = [], 0
        for item in layout:
            if item[0] == "p":
                segs.append(img(vpage(P[item[1]], O + f"{tag}{i + 1:02d}y{n}.jpg", "N° " + NUMS[n], item[2], tone), 1))
                n += 1
            else:
                segs.append(item[1])
        fimg = vstacked(P[fin[0]], P[fin[1]], O + f"{tag}{i + 1:02d}yc.jpg", "N° " + NUMS[n], tone=tone)
        spec = dict(seed=seed0 + i, track=MP, segments=hook + segs + [img(fimg, fin[2])], texts=texts, **opts)
        json.dump(spec, open(os.path.join(SP, f"{prefix}_{k}.json"), "w"), indent=1, ensure_ascii=False)
        ledger.append([batch, k, MP, tone, texts[0]["text"].replace("\n", " ") if texts else "(no line)", idea])
        print(f"{prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


if __name__ == "__main__":
    build("1122a", T, "t1122", 37000)
