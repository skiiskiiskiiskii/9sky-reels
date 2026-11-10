#!/usr/bin/env python3
"""2026-11-10: first reels with the sound baked in - EsDeeKid - Mist (extended intro).

Kirill sent the track and asked to try it on a couple of the Louboutin reels from 1109c/1109d.
The drop (first 808 hit, 29.595 s of the file) lands on the 3.13 s cut, see TRACKS["mist"].
Pages switch on the track's big hits instead of every beat:
  3.13 drop -> page I, 4.515 hit -> page II, 5.592 next bar -> finale,
  end on the next big hit (6.976, F05 length) or on the bar after (8.05).
Hooks are the 1109c/d ones re-cut to the Mist beat; on-screen lines, page sets and finales are new
so IG does not see them as copies of the posted reels."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked

GR = dict(c=1.04, s=0.92, b=-0.012)
BEAT, DROP = 60 / 97.5, 3.13
C2, C4 = DROP - 2 * BEAT, DROP - 4 * BEAT        # 1.90 / 0.67 - beats of the intro bar
PAGE_BEATS = [2.25, 1.75]                         # drop -> big hit (9/16) -> next downbeat
NUMS = ["I", "II", "III", "IV"]
RED = "/mnt/user-data/uploads/9sky-reels/hooks/red-graphic/"
ROSE = "/mnt/user-data/uploads/flowers hooks/"


def lb(key, start=None, dur=None, speed=1.12, flip=False, crop_x=0.5, crop_y=0.5, zoom=1.2, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=zoom, crop_x=crop_x, crop_y=crop_y, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def clip(src, start=0.0, dur=None, speed=1.0, zoom=1.0, crop_y=0.5, flip=False, grade=GR, **kw):
    d = dict(type="clip", src=src, start=start, align_red=False, speed=speed, zoom=zoom,
             crop_x=0.5, crop_y=crop_y, flip=flip, grade=grade)
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def freeze(key, hold_src, total=DROP, hold=0.4, speed=1.12, **kw):
    first = total - hold
    return [lb(key, start=hold_src - first * speed, dur=first, speed=speed, **kw),
            lb(key, start=hold_src, speed=0.03, **kw)]


def soles_tail(tail, speed=1.1, **kw):
    return lb("SOLES", start=4.3 - (tail - 0.42) * speed, speed=speed, zoom=1.1, **kw)


def t(text, y=0.22, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


KNIT = "BLACK KNIT"
M = [  # key, tone, hook, texts, pages, finale(kind, a, b), finale beats, idea
    ("M01_wait-for-the-red", "vitrine", freeze("COUPLE", 4.95, crop_y=0.74, crop_x=0.45),
     t("wait for the red."), [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))],
     ("stack", "KF", "KB"), 2.25, "C01 freeze hook, the drop hits on the frozen sole"),
    ("M02_count-the-reds", "vitrine",
     [lb("NAILS", start=2.2, dur=C2, speed=1.0, zoom=1.35, crop_y=0.55), lb("COUPLE", speed=1.1, crop_y=0.74)],
     t("count the reds."), [("KF", cat(1, COLLAR)), ("PB", cat(2, ARA, ROME))],
     ("stack", "KF", "KB"), 2.25, "D05 nails -> sole"),
    ("M03_out-of-the-museum", "oxblood",
     [clip(RED + "statue_low.mp4", start=0.4, dur=C2, grade={}), soles_tail(DROP - C2)],
     t("ex museo -\nout of the museum."), [("KF", cat(1, "BLACK")), ("WF", cat(2, "WHITE"))],
     ("stack", "PF", "PB"), 4, "D02 statue -> soles, explains the collection name"),
    ("M04_no-other-color", "slate",
     [clip(ROSE + "g3.mp4", dur=C4, speed=1.15, grade={}), lb("NAILS", start=2.0, dur=C2 - C4, speed=1.1),
      lb("COUPLE", speed=1.1, crop_y=0.74)],
     t("no other color\ntonight."), [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT))],
     ("stack", "SPF", "SPB"), 4, "D01 rose -> nails -> sole, knit"),
]


def build(batch, rows, out_prefix, seed0):
    ledger = []
    for i, (k, tone, hook, texts, pg, fin, fin_beats, idea) in enumerate(rows):
        tag = f"mist{i + 1:02d}x"
        pages = [img(vpage(P[pk], O + f"{tag}{j}.jpg", "N° " + NUMS[j], sub, tone), PAGE_BEATS[j])
                 for j, (pk, sub) in enumerate(pg)]
        fimg = vstacked(P[fin[1]], P[fin[2]], O + f"{tag}c.jpg", "N° " + NUMS[len(pg)], tone=tone)
        segs = hook + pages + [img(fimg, fin_beats)]
        spec = dict(seed=seed0 + i, track="mist", segments=segs, texts=texts, audio_fade_out=0.3)
        json.dump(spec, open(os.path.join(SP, f"{out_prefix}_{k}.json"), "w"), indent=1)
        ledger.append([batch, k, "mist", tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{out_prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


build("1110m", M, "m1110", 28000)
