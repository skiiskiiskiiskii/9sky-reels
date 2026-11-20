#!/usr/bin/env python3
"""made 2026-11-20, batch 1120b: 3 reels, each a new idea. Kirill: something completely new, dynamic, in the
aesthetic, ready to post. Why: the last ~90 reels all cut the same 4 Louboutin clips and Instagram's test audience
for them is saturated (11-20 diagnosis in the handoff).

New footage: palace / opera / salon clips from EX_MUSEO_hooks and hooks ids (never used in the Louboutin era).
Dynamic = a cut on every beat of the hook (5 shots, cuts on the F05 grid: 0.706 / 1.312 / 1.918 / 2.524 / 3.13 s).
Pages: the garment standing in a real room (tool/vitrine3.py: a blurred, darkened frame of the footage behind the
clean mockup). Loop 12 beats, post with the F05 audio (drop on the 3.13 s cut).
Kirill (22:35): the concept is that the clothes come FROM the museum, not clothes FOR the museum / palace /
opera - never say it is classy; keep the bait of the lines. So "a night at the palace" -> "missing from the palace".

C01 follow the red.          red in every shot: opera box, damask salon, red-lit hall, red room -> her red sole
C02 missing from the palace. walking through gold: gallery, Garnier foyer, gilded mirror, opera boxes -> red dress
C03 taken from the red salon. chandelier, gilded mirror, red damask, red salon -> red heel on a marble floor"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
import vitrine3 as V3
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-20b/"
EX = "/mnt/user-data/uploads/EX_MUSEO_hooks/"
ID = "/mnt/user-data/uploads/hooks ids/"
HI = "/mnt/user-data/uploads/hooks ideas/"
OPERA_RED = EX + "01_botanic_butique_DPL4oHGjG5n.mp4"
RED_HALL = EX + "09_baroqueblockbuster_DFfNGH9I1PK.mp4"
GALLERY = EX + "06_antoinebn_C5i3phBInjQ.mp4"
GARNIER = EX + "10_roberto_celestri_DUDpdsQDZAd.mp4"
OPERA_GOLD = EX + "04_roberto_celestri_DYR7ICqNmLe.mp4"
BOXES = EX + "12_roberto_celestri_DbQ7v2ENPlB.mp4"
LOUVRE = ID + "snaptik_7615821256385924366_hd.mp4"
DAMASK = ID + "snaptik_7629052842933849364_hd.mp4"
RED_ROOM = HI + "Video-10602.mp4"
NS = [21, 18, 19, 18]                       # shots 1-4 end on the beats; shot 5 fills to the cut (18 frames)


def g(**kw):
    d = dict(c=1.05, s=0.95, b=-0.01)
    d.update(kw)
    return d


def sh(src, start, n, zoom=1.08, cx=0.5, cy=0.5, flip=False, grade=None, **kw):
    d = dict(type="clip", src=src, start=start, align_red=False, speed=1.0, zoom=zoom, crop_x=cx, crop_y=cy,
             flip=flip, grade=grade or g(), n=n)
    d.update(kw)
    return d


def o(n):
    return O + "c1120_" + n + ".jpg"


def pg(path, beats=1):
    return (beats, img(path, 1))


R = []
# C01 follow the red. - every shot has red in it, the last one is her red sole; pages on the red damask room
red_bg = V3.frame_bg(DAMASK, 11.0, blur=8, dark=0.36, cx=0.3)
R.append(("C01_follow-the-red", "follow\nthe red.",
          [sh(OPERA_RED, 0.6, NS[0], zoom=1.1, cy=0.55), sh(DAMASK, 9.4, NS[1], zoom=1.05),
           sh(RED_HALL, 3.4, NS[2], zoom=1.1), sh(RED_ROOM, 7.6, NS[3], zoom=1.15, cx=0.4),
           dict(type="clip", src=P["COUPLE"], speed=1.12, zoom=1.2, crop_x=0.45, crop_y=0.75, flip=False, grade=g(),
                align_red=True, lead=0.42)],
          [pg(V3.page_single(red_bg, P["KF"], o("01a"), "N° I", cat(1, COLLAR))),
           pg(V3.page_single(red_bg, P["ZF"], o("01b"), "N° II", cat(2, HOOD))),
           pg(V3.page_stacked(red_bg, P["KF"], P["ZF"], o("01c"), "N° III"), 4)],
          "red thread: opera box in red -> red damask salon -> red-lit hall -> red room -> COUPLE red sole; pages in the red salon"))

# C02 missing from the palace. - forward through gold, ends on the woman in red on the opera stage; all four pieces
gold_bg = V3.frame_bg(GALLERY, 2.0, blur=9, dark=0.34)
R.append(("C02_missing-from-the-palace", "missing from\nthe palace.",
          [sh(GALLERY, 0.6, NS[0], zoom=1.05), sh(GARNIER, 2.0, NS[1], zoom=1.05),
           sh(OPERA_GOLD, 8.3, NS[2], zoom=1.1), sh(BOXES, 4.0, NS[3], zoom=1.05),
           sh(OPERA_RED, 13.4, 18, zoom=1.15, cy=0.5)],
          [pg(V3.page_single(gold_bg, P["KF"], o("02a"), "N° I", cat(1, COLLAR))),
           pg(V3.page_single(gold_bg, P["WF"], o("02b"), "N° II", cat(2, COLLAR))),
           pg(V3.page_single(gold_bg, P["ZF"], o("02c"), "N° III", cat(3, HOOD))),
           pg(V3.page_single(gold_bg, P["XWF"], o("02d"), "N° IV", cat(4, HOOD))),
           pg(V3.page_grid(gold_bg, [P["KF"], P["WF"], P["ZF"], P["XWF"]], o("02e"), "N° V"), 2)],
          "palace walk: gold gallery -> Garnier foyer -> gilded mirror -> opera boxes -> red dress on the stage; all four pieces in the gallery"))

# C03 taken from the red salon. - Louvre / Versailles salons, ends on the red heel on marble; black + white QZ on the red wall
salon_bg = V3.frame_bg(DAMASK, 14.5, blur=8, dark=0.38, cx=0.5, cy=0.4)
R.append(("C03_taken-from-the-red-salon", "taken from\nthe red salon.",
          [sh(LOUVRE, 7.0, NS[0], zoom=1.05), sh(LOUVRE, 24.0, NS[1], zoom=1.08),
           sh(DAMASK, 14.3, NS[2], zoom=1.05), sh(LOUVRE, 48.0, NS[3], zoom=1.08),
           sh(P["MARBLE"], round(1.09 - 18 / 30, 3), 18, zoom=1.1)],
          [pg(V3.page_single(salon_bg, P["WF"], o("03a"), "N° I", cat(1, COLLAR))),
           pg(V3.page_single(salon_bg, P["KF"], o("03b"), "N° II", cat(2, COLLAR))),
           pg(V3.page_stacked(salon_bg, P["WF"], P["KF"], o("03c"), "N° III"), 4)],
          "red salon: chandelier -> gilded mirror -> red damask -> red salon -> MARBLE red heel; white + black QZ on the red wall"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1120b", k, "F05 / mr popular", line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=46000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"c1120_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1120b.json"), "w"), indent=1)
