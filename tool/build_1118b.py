#!/usr/bin/env python3
"""made 2026-11-18, batch 1118b: 5 reels, redo of 1118a after Kirill's notes:
- 1118a reused the same clips (COUPLE / SOLES / NAILS, no MARBLE) and slowed one down -> now every hook is a MIX of
  three Louboutin shots at real speed (COUPLE, SOLES, NAILS, MARBLE), the red sole lands ~0.4 s before the cut;
- 1118a lines were all "x, red soles" -> Kirill picked: 3 lines about the place / the evening, 2 questions.
Hooks: Louboutin only (Kirill). All 12-beat seamless loops (7.27 s), post with the F05 audio, drop on the cut.

Z01 date night at the opera.     NAILS -> COUPLE (his shoes) -> SOLES logo sole        black quarter zip
Z02 collar or hood?              COUPLE (her nails) -> SOLES (watch) -> MARBLE red heel  black QZ vs black zip hoodie
Z03 dinner under the chandeliers. SOLES (rings) -> NAILS -> COUPLE red sole            white zip hoodie
Z04 after the museum closes.     COUPLE wide, mirrored -> NAILS -> MARBLE red heel     black zip hoodie
Z05 black or white tonight?      COUPLE wide -> SOLES (hand) -> COUPLE tight red sole   black / white quarter zip"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
from vitrine import vpage, vstacked
import loopreel

GR = dict(c=1.04, s=0.92, b=-0.012)
OUT = "/mnt/user-data/outputs/ready-2026-11-18b/"


def sh(key, start, n, speed=1.0, **kw):
    """one shot: explicit start, n frames, real speed"""
    d = dict(type="clip", src=P[key], start=start, align_red=False, speed=speed, zoom=1.15, crop_x=0.5,
             crop_y=0.6, flip=False, grade=GR, n=n)
    d.update(kw)
    return d


def red_end(key, **kw):
    """last shot: the red lands 0.42 s before the cut"""
    d = dict(type="clip", src=P[key], speed=1.0, zoom=1.15, crop_x=0.5, crop_y=0.6, flip=False, grade=GR,
             align_red=True, lead=0.42)
    d.update(kw)
    return d


def soles_end(n, **kw):       # SOLES logo sole shows at ~4.3 s; end the shot at 4.72 so it is on screen ~0.4 s
    return dict(sh("SOLES", round(4.72 - n / 30, 3), n, **kw))


def marble_end(n, **kw):      # MARBLE is 1.1 s and red the whole time - keep it short, at the end
    return dict(sh("MARBLE", round(1.09 - n / 30, 3), n, zoom=1.1, crop_y=0.5, **kw))


def pg(key, tag, no, sub, tone):
    return (1, img(vpage(P[key], O + tag + ".jpg", no, sub, tone), 1))


def fin(a, b, tag, tone):
    return (4, img(vstacked(P[a], P[b], O + tag + ".jpg", "N° III", tone=tone), 1))


R = [  # key, line, hook (shots), after, idea
    ("Z01_date-night-at-the-opera", "date night\nat the opera.",
     [sh("NAILS", 1.0, 36, zoom=1.0), sh("COUPLE", 2.4, 30, zoom=1.2, crop_x=0.4, crop_y=0.75), soles_end(28)],
     [pg("KF", "z01a", "N° I", cat(1, COLLAR), "vitrine"),
      pg("KB", "z01b", "N° II", cat(2, ARA, ROME), "vitrine"),
      fin("KF", "KB", "z01c", "vitrine")],
     "mix NAILS -> COUPLE his shoes -> SOLES logo sole; black quarter zip"),
    ("Z02_collar-or-hood", "collar\nor hood?",
     [sh("COUPLE", 0.6, 40, zoom=1.15, crop_y=0.6), sh("SOLES", 1.3, 36, zoom=1.1), marble_end(18)],
     [pg("KF", "z02a", "N° I", cat(1, COLLAR), "slate"),
      pg("ZF", "z02b", "N° II", cat(2, HOOD), "slate"),
      fin("KF", "ZF", "z02c", "slate")],
     "mix COUPLE her nails -> SOLES watch -> MARBLE red heel; black quarter zip vs black zip hoodie"),
    ("Z03_dinner-under-the-chandeliers", "dinner under\nthe chandeliers.",
     [sh("SOLES", 0.6, 36, zoom=1.1), sh("NAILS", 2.6, 30, zoom=1.05), red_end("COUPLE", zoom=1.25, crop_x=0.45, crop_y=0.75)],
     [pg("XWF", "z03a", "N° I", cat(1, HOOD), "oxblood"),
      pg("XWB", "z03b", "N° II", cat(2, ARA, ROME), "oxblood"),
      fin("ZPF", "ZPB", "z03c", "oxblood")],
     "mix SOLES rings -> NAILS -> COUPLE red sole; white zip hoodie, zip pair finale"),
    ("Z04_after-the-museum-closes", "after the\nmuseum closes.",
     [sh("COUPLE", 2.8, 40, zoom=1.0, crop_y=0.6, flip=True), sh("NAILS", 2.4, 36, zoom=1.0), marble_end(18)],
     [pg("ZF", "z04a", "N° I", cat(1, HOOD), "slate"),
      pg("ZB", "z04b", "N° II", cat(2, ARA, ROME), "slate"),
      fin("KF", "ZF", "z04c", "slate")],
     "mix COUPLE wide mirrored -> NAILS -> MARBLE red heel; black zip hoodie, all-black finale"),
    ("Z05_black-or-white-tonight", "black or white\ntonight?",
     [sh("COUPLE", 1.6, 36, zoom=1.0, crop_y=0.6), sh("SOLES", 0.5, 30, zoom=1.1), red_end("COUPLE", zoom=1.3, crop_x=0.42, crop_y=0.78)],
     [pg("KF", "z05a", "N° I", cat(1, "BLACK"), "vitrine"),
      pg("WF", "z05b", "N° II", cat(2, "WHITE"), "vitrine"),
      fin("PF", "PB", "z05c", "vitrine")],
     "mix COUPLE wide -> SOLES hand -> COUPLE tight red sole; black / white quarter zip, pair finale"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1118b", k, "mrpopular", line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=40000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"z1118_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1118b.json"), "w"), indent=1)
