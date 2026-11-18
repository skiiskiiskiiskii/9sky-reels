#!/usr/bin/env python3
"""made 2026-11-18, batch 1118a: 5 reels, all ~7 s looped (12 beats). Kirill parked the 4.8 s and 10.9 s lengths:
"7 seconds as before is ideal". Louboutin hooks, quarter zips and zip hoodies (mixed), post with the F05 audio.

Y01 his collar, her soles.    COUPLE wide (K05)               -> his black QZ / her white zip hoodie
Y02 gold watch, red soles.    SOLES, new crop                 -> black zip hoodie
Y03 black nails, red soles.   NAILS -> COUPLE                 -> white QZ, QZ pair finale
Y04 red soles, up close.      COUPLE tight, slows on the sole -> zip hoodie pair
Y05 red under black heels.    SOLES (K01 window), new crop    -> white QZ + white zip hoodie"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
from vitrine import vpage, vstacked
import loopreel

GR = dict(c=1.04, s=0.92, b=-0.012)
OUT = "/mnt/user-data/outputs/ready-2026-11-18a/"


def lb(key, **kw):
    d = dict(type="clip", src=P[key], speed=1.12, zoom=1.2, crop_x=0.5, crop_y=0.5, flip=False, grade=GR)
    if "start" in kw:
        d["align_red"] = False
    else:
        d.update(align_red=True, lead=0.42)
    d.update(kw)
    return d


def pg(key, tag, no, sub, tone):
    return (1, img(vpage(P[key], O + tag + ".jpg", no, sub, tone), 1))


def fin(a, b, tag, tone):
    return (4, img(vstacked(P[a], P[b], O + tag + ".jpg", "N° III", tone=tone), 1))


# COUPLE slows down on the sole: normal speed, then 0.5x for the last 0.6 s; the red shows ~0.4 s before the cut
SLOW_N = 18
s_slow = 4.6
first = (94 - SLOW_N) / 30
RAMP = [lb("COUPLE", start=round(s_slow - first, 3), speed=1.0, zoom=1.3, crop_x=0.42, crop_y=0.78, flip=True, n=94 - SLOW_N),
        lb("COUPLE", start=s_slow, speed=0.5, smooth=True, zoom=1.3, crop_x=0.42, crop_y=0.78, flip=True)]

R = [  # key, line, hook, after, idea
    ("Y01_his-collar-her-soles", "his collar,\nher soles.",
     [lb("COUPLE", zoom=1.0, crop_y=0.6)],
     [pg("KF", "y01a", "N° I", cat(1, "HIS  ·  BLACK"), "vitrine"),
      pg("XWF", "y01b", "N° II", cat(2, "HERS  ·  WHITE"), "vitrine"),
      fin("KF", "XWF", "y01c", "vitrine")],
     "K05 hook; his black quarter zip / her white zip hoodie"),
    ("Y02_gold-watch-red-soles", "gold watch,\nred soles.",
     [lb("SOLES", start=0.78, speed=1.3, zoom=1.25, crop_x=0.45, crop_y=0.65)],
     [pg("ZF", "y02a", "N° I", cat(1, HOOD), "slate"),
      pg("ZB", "y02b", "N° II", cat(2, ARA, ROME), "slate"),
      fin("ZF", "ZB", "y02c", "slate")],
     "SOLES (watch, red nails) -> logo sole, tighter crop; black zip hoodie"),
    ("Y03_black-nails-red-soles", "black nails,\nred soles.",
     [lb("NAILS", start=1.6, speed=1.1, zoom=1.0, n=35), lb("COUPLE", zoom=1.15, crop_x=0.45, crop_y=0.7)],
     [pg("WF", "y03a", "N° I", cat(1, COLLAR), "oxblood"),
      pg("WB", "y03b", "N° II", cat(2, ARA, ROME), "oxblood"),
      fin("PF", "PB", "y03c", "oxblood")],
     "NAILS black nails -> COUPLE red sole; white quarter zip, pair finale"),
    ("Y04_red-soles-up-close", "red soles,\nup close.",
     RAMP,
     [pg("ZPF", "y04a", "N° I", cat(1, HOOD), "vitrine"),
      pg("ZPB", "y04b", "N° II", cat(2, ARA, ROME), "vitrine"),
      fin("ZPF", "ZPB", "y04c", "vitrine")],
     "COUPLE tight, mirrored, slows to 0.5x on the sole; zip hoodie black + white"),
    ("Y05_red-under-black-heels", "red under\nblack heels.",
     [lb("SOLES", start=1.59, speed=1.0, zoom=1.2, crop_x=0.55, crop_y=0.7)],
     [pg("WF", "y05a", "N° I", cat(1, COLLAR), "slate"),
      pg("XWF", "y05b", "N° II", cat(2, HOOD), "slate"),
      fin("WF", "XWF", "y05c", "slate")],
     "SOLES K01 window, new crop; white quarter zip + white zip hoodie"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1118a", k, "mrpopular", line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=39000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"y1118_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1118a.json"), "w"), indent=1)
