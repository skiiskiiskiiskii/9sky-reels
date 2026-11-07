#!/usr/bin/env python3
"""2026-11-07 morning, batch 1107b: 5 more new treatments on top of the 1107a look that did well
(vitrine/oxblood pages, story lines, tight crops, slow-down on the sole). New here:
F01 double take   - the red sole flashes at normal speed, then the same moment replays slowed down
F02 rule IX       - the line sits at the top and plays on the brand number; third page tone (slate)
F03 rose -> sole with the slow-down on the sole
F04 rose hand -> nails -> couple, slow-down on the sole, oxblood
F05 the line at the top, tight crop on the shoes
Every caption carries the batch code (cat. 1107b-NN) so Metricool rows map back to this batch."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, IX, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked

BATCH = "1107b"
G = "/mnt/user-data/uploads/flowers hooks/"
GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU, DROP = 60 / 99.0, 60 / 123.05, 3.13
C2 = DROP - 2 * BMP
MP, AU = "mrpopular", "aura"
NUMS = ["I", "II", "III", "IV"]


def lb(key, start=None, dur=None, speed=1.0, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.035, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def ramp(key, onset, total=DROP, slow=0.55, rate=0.5, pre=1.0, **kw):
    """normal speed, then a smooth slow-down for the last `slow` s of `total`; the red lands in the slow part"""
    s_end = onset + 0.13
    s_slow = s_end - slow * rate
    first = total - slow
    return [lb(key, start=s_slow - first * pre, dur=first, speed=pre, **kw),
            lb(key, start=s_slow, speed=rate, smooth=True, **kw)]


def double_take(key, onset, replay=1.1, rate=0.5, **kw):
    """red at normal speed, then the same moment again, slowed down"""
    s_end = onset + 0.25
    first = DROP - replay
    return [lb(key, start=s_end - first, dur=first, **kw),
            lb(key, start=s_end - replay * rate, speed=rate, smooth=True, **kw)]


def rose(name, dur, start=0.0, speed=1.15, flip=False):
    return dict(type="clip", src=G + name + ".mp4", start=start, dur=dur, align_red=False, speed=speed,
                zoom=1.0, crop_x=0.5, flip=flip, grade={})


def t(text, y=0.40, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


def vpages(items, tone, tag, beats):
    return [img(vpage(P[k], O + f"{tag}{i}.jpg", "N° " + NUMS[i], sub, tone), beats) for i, (k, sub) in enumerate(items)]


def vfin(front, back, tag, no, tone):
    return img(vstacked(P[front], P[back], O + f"{tag}c.jpg", no, tone=tone), 4)


KNIT = "BLACK KNIT"
QBW = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QBK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QKN = [("SWF", cat(1, KNIT)), ("KF", cat(2, COLLAR)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]
QW = [("PF", cat(1, COLLAR)), ("WF", cat(2, IX))]

R = [  # key, track, tone, hook, texts, pages, finale(front, back)
    ("F01_look-again", AU, "oxblood", double_take("COUPLE", 4.7, crop_x=0.55),
     t("wait.\nlook again."), QBW, ("PF", "PB")),
    ("F02_rule-ix", MP, "slate", [lb("SOLES", start=4.3 - 2.82 * 1.12, speed=1.12, zoom=1.12, crop_y=0.6, flip=True)],
     t("rule IX:\none red detail per outfit.", 0.22), QKN, ("SPF", "SPB")),
    ("F03_dinner-at-nine", MP, "vitrine",
     [rose("g3", C2)] + ramp("COUPLE", 4.7, total=DROP - C2, slow=0.6, flip=True),
     t("dinner at nine.\nred, as usual.", 0.56, 0.45), QW, ("PF", "PB")),
    ("F04_quiet-except-one-place", AU, "oxblood",
     [rose("g1", DROP - 4 * BAU, start=0.3, speed=1.0), lb("NAILS", start=2.0, dur=2 * BAU, speed=1.1)]
     + ramp("COUPLE", 4.7, total=2 * BAU, slow=0.55),
     t("quiet everywhere\nexcept one place.", 0.56, 0.45), QKN, ("SPF", "SPB")),
    ("F05_starts-with-the-shoes", MP, "vitrine", [lb("COUPLE", speed=1.12, zoom=1.2, crop_y=0.75, crop_x=0.4)],
     t("it starts\nwith the shoes.", 0.22), QBK, ("KF", "KB")),
]
ledger = []
for i, (k, track, tone, hook, texts, pg, fin) in enumerate(R):
    tag = f"f{i + 1:02d}"
    pb = 1 if track == MP else 2
    segs = hook + vpages(pg, tone, tag, pb) + [vfin(fin[0], fin[1], tag, "N° " + NUMS[len(pg)], tone)]
    spec = dict(seed=23000 + i, track=track, segments=segs, texts=texts)
    json.dump(spec, open(os.path.join(SP, f"f1107_{k}.json"), "w"), indent=1)
    ledger.append([BATCH, f"cat. {BATCH}-{i + 1:02d}", k, track, tone, texts[0]["text"].replace("\n", " ")])
    print(f"f1107_{k}")
json.dump(ledger, open(os.path.join(SP, f"ledger_{BATCH}.json"), "w"), indent=1)
