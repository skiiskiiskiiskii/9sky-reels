#!/usr/bin/env python3
"""2026-11-11, batch 1111a: 5 reels on the F05 strategy and content (Kirill: "try the strategy and
content of the reel that took off").

F05 "it starts with the shoes." 63K views, H08 "red goes underneath." 12.6K - both:
  - a Louboutin hook, tight crop on the shoes, the red sole shows ~0.4 s before the 3.13 s cut
  - one short line at the TOP of the frame, a style rule that points at the shoes and makes you wait
    for the payoff (the red collar on the pages)
  - black quarter zip only (H08: + knit), 2 pages one beat each + stacked finale, ~6.8 s,
    F05 timing so Kirill can use the F05 audio (Cyn - North Pole) as is
  - caption: line 1 finishes the story, line 3 a question or a send line
What changes reel to reel: the footage (other clip / crop / flip / slow-down on the sole) and the line.
J01 repeats F05's exact line on new footage - a test of whether the line carries the reel."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked

GR = dict(c=1.04, s=0.92, b=-0.012)
DROP = 3.13
MP = "mrpopular"                                   # F05 grid: pages 1 beat at 99 BPM, finale 4 beats
NUMS = ["I", "II", "III", "IV"]


def lb(key, start=None, dur=None, speed=1.12, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.2, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def ramp(key, onset, total=DROP, slow=0.55, rate=0.5, pre=1.0, **kw):
    """normal speed, then a smooth slow-down for the last `slow` s; the red lands in the slow part"""
    s_end = onset + 0.13
    s_slow = s_end - slow * rate
    first = total - slow
    return [lb(key, start=s_slow - first * pre, dur=first, speed=pre, **kw),
            lb(key, start=s_slow, speed=rate, smooth=True, **kw)]


def t(text, y=0.22, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QKN = [("KF", cat(1, COLLAR)), ("SWF", cat(2, "BLACK KNIT"))]

J = [  # key, tone, hook, texts, pages, finale, idea
    ("J01_starts-with-the-shoes-walk", "vitrine",
     [lb("STREET", start=4.95 - DROP * 1.1, speed=1.1, zoom=1.15, crop_x=0.0, crop_y=0.0)],
     t("it starts\nwith the shoes."), QBK, ("KF", "KB"), "F05 line word for word, new footage (her walk, top-down)"),
    ("J02_ends-with-the-collar", "vitrine",
     [lb("COUPLE", speed=1.2, zoom=1.1, crop_x=0.6, crop_y=0.7, flip=True)],
     t("it ends\nwith the collar."), QBK, ("KF", "KB"), "F05 sequel: its caption's second half on screen"),
    ("J03_shoes-set-the-tone", "vitrine",
     ramp("COUPLE", 4.7, slow=0.6, crop_x=0.42, crop_y=0.78, zoom=1.32),
     t("the shoes\nset the tone."), QBK, ("KF", "KB"), "F05 + H08 slow-down on the sole, tighter crop"),
    ("J04_detail-not-an-outfit", "vitrine",
     [lb("SOLES", start=4.3 - (DROP - 0.42) * 1.12, zoom=1.25, crop_y=0.7, crop_x=0.45, flip=True)],
     t("red is a detail,\nnot an outfit."), QBK, ("KF", "KB"), "style rule on the logo-sole clip"),
    ("J05_look-underneath", "slate",
     [lb("NAILS", start=2.95, dur=DROP - 0.55, speed=1.0, zoom=1.2, crop_y=0.55)]
     + [lb("NAILS", start=2.95 + DROP - 0.55, speed=0.5, zoom=1.2, crop_y=0.55, smooth=True)],
     t("look underneath."), QKN, ("SPF", "SPB"), "H08 sibling: red under the nails -> her own heel lifts, knit"),
]


def build(batch, rows, out_prefix, seed0):
    ledger = []
    for i, (k, tone, hook, texts, pg, fin, idea) in enumerate(rows):
        tag = f"j{i + 1:02d}y"
        pages = [img(vpage(P[pk], O + f"{tag}{j}.jpg", "N° " + NUMS[j], sub, tone), 1) for j, (pk, sub) in enumerate(pg)]
        fimg = vstacked(P[fin[0]], P[fin[1]], O + f"{tag}c.jpg", "N° " + NUMS[len(pg)], tone=tone)
        spec = dict(seed=seed0 + i, track=MP, segments=hook + pages + [img(fimg, 4)], texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{out_prefix}_{k}.json"), "w"), indent=1)
        ledger.append([batch, k, MP, tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{out_prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


build("1111a", J, "j1111", 29000)
