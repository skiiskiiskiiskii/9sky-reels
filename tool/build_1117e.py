#!/usr/bin/env python3
"""made 2026-11-17 (late), batch 1117e: 6 reels with everything discussed after the W01 loop test.
Kirill: the loop stays on every reel; also try both lengths (short ~4.8 s: hook + one page with the pair;
long 10-12 s: the red sole shows twice); use the zip hoodie as well as the quarter zips now (Louboutin + zip
hoodie is now asked for).
All loop seamlessly (tool/loopreel.py), whole beats at 99 BPM - post with the F05 audio, drop on the cut.

X01 short  8 beats  her soles are red.     COUPLE wide, mirrored          -> QZ black+white pair page
X02 short  8 beats  red soles, red hood.   SOLES (K01 window)             -> zip hoodie black+white pair page
X03 long  18 beats  watch her step.        COUPLE tight (F05)  -> KF, KB  -> NAILS heel -> WF -> QZ pair finale
X04 long  18 beats  her shoes. his hood.   SOLES (U02 window)  -> ZF, ZB  -> COUPLE wide -> XWF -> zip pair finale
X05 std   12 beats  all black, red soles.  NAILS -> SOLES                 -> black QZ + black zip hoodie together
X06 std   12 beats  red soles, white hood. COUPLE, tight on her sole      -> white zip hoodie"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
from vitrine import vpage, vstacked
import loopreel

GR = dict(c=1.04, s=0.92, b=-0.012)
OUT = "/mnt/user-data/outputs/ready-2026-11-17e/"
BOTH = "RED COLLAR, RED-LINED HOOD"


def lb(key, **kw):
    d = dict(type="clip", src=P[key], speed=1.12, zoom=1.2, crop_x=0.5, crop_y=0.5, flip=False, grade=GR)
    if "start" in kw:
        d["align_red"] = False
    else:
        d.update(align_red=True, lead=0.42)
    d.update(kw)
    return d


def pg(key, tag, no, sub, tone, beats=1):
    return (beats, img(vpage(P[key], O + tag + ".jpg", no, sub, tone), 1))


def st(a, b, tag, no, tone, beats):
    return (beats, img(vstacked(P[a], P[b], O + tag + ".jpg", no, tone=tone), 1))


R = [  # key, line, y, hook, after, idea
    ("X01_her-soles-are-red_short", "her soles\nare red.", 0.22,
     [lb("COUPLE", zoom=1.0, crop_y=0.6, flip=True)],
     [st("PF", "PB", "x01c", "N° I", "vitrine", 2)],
     "short 8 beats: K05 hook mirrored -> one stacked page, quarter zip black + white"),
    ("X02_red-soles-red-hood_short", "red soles,\nred hood.", 0.22,
     [lb("SOLES", start=1.59, speed=1.0, zoom=1.1, crop_y=0.6)],
     [st("ZPF", "ZPB", "x02c", "N° I", "slate", 2)],
     "short 8 beats: SOLES logo sole -> one stacked page, zip hoodie black + white"),
    ("X03_watch-her-step_long", "watch\nher step.", 0.22,
     [lb("COUPLE", zoom=1.2, crop_x=0.4, crop_y=0.75)],
     [pg("KF", "x03a", "N° I", cat(1, COLLAR), "vitrine"),
      pg("KB", "x03b", "N° II", cat(2, ARA, ROME), "vitrine"),
      (5, lb("NAILS", start=round(5.935 - 91 / 30 * 0.8, 3), speed=0.8, smooth=True, zoom=1.15, crop_y=0.55)),
      pg("WF", "x03d", "N° III", cat(3, "THE SAME RED COLLAR"), "vitrine"),
      st("PF", "PB", "x03c", "N° IV", "vitrine", 4)],
     "long 18 beats: F05 hook -> black QZ -> NAILS red heel (second red) -> white QZ -> pair finale"),
    ("X04_her-shoes-his-hood_long", "her shoes.\nhis hood.", 0.22,
     [lb("SOLES", start=0.78, speed=1.3, zoom=1.1, crop_y=0.6)],
     [pg("ZF", "x04a", "N° I", cat(1, HOOD), "oxblood"),
      pg("ZB", "x04b", "N° II", cat(2, ARA, ROME), "oxblood"),
      (5, lb("COUPLE", zoom=1.0, crop_y=0.6)),
      pg("XWF", "x04d", "N° III", cat(3, "THE SAME RED HOOD"), "oxblood"),
      st("ZPF", "ZPB", "x04c", "N° IV", "oxblood", 4)],
     "long 18 beats: SOLES -> black zip hoodie -> COUPLE wide (second red) -> white zip hoodie -> zip pair finale"),
    ("X05_all-black-red-soles", "all black,\nred soles.", 0.22,
     [lb("NAILS", start=1.6, speed=1.1, zoom=1.0, n=35), lb("SOLES", start=2.29, speed=1.3, zoom=1.15, crop_y=0.6)],
     [pg("KKF", "x05a", "N° I", cat(1, BOTH), "slate"),
      pg("KKB", "x05b", "N° II", cat(2, ARA, ROME), "slate"),
      st("KF", "ZF", "x05c", "N° III", "slate", 4)],
     "12 beats: NAILS -> SOLES logo sole; black quarter zip + black zip hoodie together"),
    ("X06_red-soles-white-hood", "red soles,\nwhite hood.", 0.22,
     [lb("COUPLE", speed=1.0, zoom=1.3, crop_x=0.55, crop_y=0.72)],
     [pg("XWF", "x06a", "N° I", cat(1, HOOD), "oxblood"),
      pg("XWB", "x06b", "N° II", cat(2, ARA, ROME), "oxblood"),
      st("XWF", "XWB", "x06c", "N° III", "oxblood", 4)],
     "12 beats: COUPLE tight on her sole, real speed; white zip hoodie"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, y, hook, after, idea) in enumerate(R):
        ledger.append(["1117e", k, "mrpopular", line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, y=y, seed=38000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"x1117_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1117e.json"), "w"), indent=1)
