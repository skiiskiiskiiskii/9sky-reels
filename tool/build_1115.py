#!/usr/bin/env python3
"""2026-11-15, batch 1115a: 6 reels. Products this time: only the IX quarter zip and the IX zip hoodie,
black and white (Kirill, 11-15). Louboutin hooks go with the quarter zip, rose hooks may carry the zip hoodie.
Half louboutin-led, half rose-led. Every on-screen line is new.

N01 nobody looks at the face   - NEW clip MARBLE (first 1.10 s, before its own text) -> COUPLE red
N02 dress from the floor up    - MARBLE mirrored, gently slowed -> NAILS tail (red nails flash, red sole)
N03 the first red is never his - the F05 hook itself (COUPLE, same crop), new line; near-hit
N04 she answered in red        - rose g2 -> SOLES logo sole; white quarter zip
N05 red looks best near the face - roses g1 -> g3; black zip hoodie (red-lined hood frames the face)
N06 roses for the curtain call - rose g3 -> red curtain s12_0; white zip hoodie, black+white zip finale
Rose-led reels with the rose at the top of the frame keep the line at y=0.56 (as the 1105/1106 rose reels did).
All on the F05 timing (mrpopular, pages 1 beat at 99 BPM, finale 4 beats) - post with the F05 audio."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked

GR = dict(c=1.04, s=0.92, b=-0.012)
DROP, BMP = 3.13, 60 / 99.0
MP = "mrpopular"
NUMS = ["I", "II", "III", "IV"]
ROSE = "/mnt/user-data/uploads/flowers hooks/"
SHOOT = "/mnt/user-data/uploads/Downloads/исходники/_разбор/hooks_src/"
MARBLE_LEN = 1.10                                   # 33 frames, the clip's own text starts on frame 34


def lb(key, start=None, dur=None, speed=1.12, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.2, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def clip(src, start=0.0, dur=None, speed=1.0, zoom=1.0, crop_x=0.5, crop_y=0.5, flip=False, grade=GR, **kw):
    d = dict(type="clip", src=src, start=start, align_red=False, speed=speed, zoom=zoom,
             crop_x=crop_x, crop_y=crop_y, flip=flip, grade=grade)
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def t(text, y=0.22, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


def marble(speed=1.0, flip=False):
    return clip(P["MARBLE"], start=0.0, dur=round(MARBLE_LEN / speed, 3), speed=speed, flip=flip, smooth=speed < 1)


M2 = MARBLE_LEN / 0.85                              # N02 marble length after the slow-down
QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
N = [  # key, tone, hook, texts, pages, finale, idea
    ("N01_nobody-looks-at-the-face", "vitrine",
     [marble(), lb("COUPLE", zoom=1.2, crop_x=0.4, crop_y=0.75)],
     t("nobody looks at\nthe face first."), QBK, ("KF", "KB"),
     "NEW clip MARBLE (red soles on marble, 1.1 s) -> COUPLE men's shoes -> her red sole at the cut"),
    ("N02_dress-from-the-floor-up", "slate",
     [marble(speed=0.85, flip=True), lb("NAILS", start=6.0 - (DROP - M2) * 1.0, speed=1.0, zoom=1.15, crop_y=0.55)],
     t("dress from\nthe floor up."),
     [("KF", cat(1, "BLACK  ·  RED COLLAR")), ("WF", cat(2, "WHITE  ·  THE SAME RED COLLAR"))], ("PF", "PB"),
     "MARBLE mirrored + gently slowed -> NAILS tail (red nails flash, heel lift, red sole); black/white pair finale"),
    ("N03_the-first-red-is-never-his", "oxblood",
     [lb("COUPLE", zoom=1.2, crop_x=0.4, crop_y=0.75)],
     t("the first red\nis never his."), QBK, ("KF", "KB"),
     "the F05 hook unchanged (COUPLE, same crop), new line: his black shoes, her red first, his red on the collar"),
    ("N04_she-answered-in-red", "vitrine",
     [clip(ROSE + "g2.mp4", start=0.4, dur=1.5, zoom=1.15, crop_y=0.0),
      lb("SOLES", start=4.3 - (DROP - 1.5 - 0.42), speed=1.0, zoom=1.1, crop_y=0.6)],
     t("she answered\nin red."), [("WF", cat(1, COLLAR)), ("WB", cat(2, ARA, ROME))], ("WF", "WB"),
     "rose g2 (he brings it) -> SOLES logo sole (her answer); white quarter zip edition"),
    ("N05_red-looks-best-near-the-face", "oxblood",
     [clip(ROSE + "g1.mp4", start=0.3, dur=1.6, zoom=1.15, crop_y=0.3, grade={}),
      clip(ROSE + "g3.mp4", start=0.0, zoom=1.08, crop_y=0.3, grade={})],
     t("red looks best\nnear the face.", y=0.56), [("ZF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME))], ("ZF", "ZB"),
     "two rose shots, no shoes; black zip hoodie - the red-lined hood is the red near the face"),
    ("N06_roses-for-the-curtain-call", "slate",
     [clip(ROSE + "g3.mp4", start=0.0, dur=1.4, zoom=1.08, crop_y=0.3, grade={}),
      clip(SHOOT + "s12_0.mp4", start=2.3)],
     t("roses for the\ncurtain call.", y=0.56), [("XWF", cat(1, HOOD)), ("XWB", cat(2, ARA, ROME))], ("XWF", "XWB"),
     "rose g3 -> red curtain closing (own shoot); white zip hoodie (finale changed 11-16 to white front/back so it does not repeat R04)"),
]


def build(batch, rows, out_prefix, seed0, tag_letter="n"):
    ledger = []
    for i, (k, tone, hook, texts, pg, fin, idea) in enumerate(rows):
        tag = f"{tag_letter}{i + 1:02d}y"
        pages = [img(vpage(P[pk], O + f"{tag}{j}.jpg", "N° " + NUMS[j], sub, tone), 1) for j, (pk, sub) in enumerate(pg)]
        fimg = vstacked(P[fin[0]], P[fin[1]], O + f"{tag}c.jpg", "N° " + NUMS[len(pg)], tone=tone)
        spec = dict(seed=seed0 + i, track=MP, segments=hook + pages + [img(fimg, 4)], texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{out_prefix}_{k}.json"), "w"), indent=1, ensure_ascii=False)
        ledger.append([batch, k, MP, tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{out_prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


if __name__ == "__main__":
    build("1115a", N, "n1115", 31000)
