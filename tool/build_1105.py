#!/usr/bin/env python3
"""2026-11-05: 17 reels (Kirill 11-05).
A  7 - Louboutin hook + quarter zip
B  3 - Louboutin hook + quarter zip + black knit
C  7 - rose + Louboutin in one hook, with zip hoodie, quarter zip, knit (Kirill asked for the zip hoodie here
       explicitly, which overrides the 10-30 "Louboutin never with the zip hoodie" rule for this batch;
       still no "red inside" lines)
Stats behind it (posted 11-02): rose hooks on mr popular 36-49% vs calm 19-30%, so the combos are mostly on
mr popular; Louboutin + quarter zip 55-66% either way; the best combo was the hand-to-hand one
(rose hand -> nails -> red sole, 54%), so three combos use it. One line of text per hook.
9 of 17 are dynamic (mr popular)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP, P

G = "/mnt/user-data/uploads/flowers hooks/"
GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU = 60 / 99.0, 60 / 123.05
DROP = 3.13


def lb(key, flip, crop_x, lead=0.42, speed=0.95, zoom=1.035, **kw):
    d = dict(type="clip", src=P[key], until="drop", align_red=True, speed=speed, zoom=zoom, crop_x=crop_x,
             flip=flip, lead=lead, grade=GR)
    d.update(kw)
    return d


def soles(flip, crop_x, speed=0.95):          # logo sole enters ~4.3 s of the source: keep it ~0.4 s on screen
    return lb("SOLES", flip, crop_x, speed=speed, start=4.3 - 2.73 * speed, align_red=False)


def nails(flip, crop_x, speed=0.95):          # the sole itself appears ~5.7 s of the source
    return lb("NAILS", flip, crop_x, speed=speed, start=5.7 - 2.6 * speed, align_red=False)


def pre(key, start, flip, crop_x, dur, speed=1.1):
    d = lb(key, flip, crop_x, speed=speed, start=start, align_red=False)
    d.pop("until"); d["dur"] = dur
    return d


def rose(name, dur, start=0.0, speed=1.0, flip=False):
    return dict(type="clip", src=G + name + ".mp4", start=start, dur=dur, align_red=False, speed=speed,
                zoom=1.0, crop_x=0.5, flip=flip, grade={})


def combo(rname, lkey, track, beats, rstart=0.0, rflip=False, lflip=False, rspeed=1.1):
    """rose until `beats` before the drop, then the Louboutin shot to the drop"""
    beat = BMP if track == "mrpopular" else BAU
    cut = DROP - beats * beat
    tail = DROP - cut
    r = rose(rname, cut, rstart, rspeed, rflip)
    if lkey == "NAILS":            # hand with nails -> red sole near the end (~0.3 s)
        sp = 1.15 if tail > 1.6 else 1.35
        l = lb("NAILS", lflip, 0.5, speed=sp, start=5.98 - tail * sp, align_red=False)
    elif lkey == "SOLES":
        l = lb("SOLES", lflip, 0.5, speed=1.1, start=4.3 - (tail - 0.42) * 1.1, align_red=False)
    else:
        l = lb(lkey, lflip, 0.5, speed=1.05)
    return [r, l]


def t(text, y=0.40, scrim=0.5):
    return [{"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": scrim, "font": "cg-italic"}]


KNIT = "BLACK KNIT"
QW1 = [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))]
QW2 = [("KF", cat(1, COLLAR)), ("WF", cat(2, "THE SAME RED COLLAR")), ("PF", cat(3, "BLACK  ·  WHITE"))]
QW3 = [("PF", cat(1, COLLAR)), ("KF", cat(2, IX))]
QK = [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))]
QWW = [("WF", cat(1, "THE SAME RED COLLAR")), ("WB", cat(2, ARA, ROME))]
SW1 = [("KF", cat(1, COLLAR)), ("SWF", cat(2, KNIT)), ("SPF", cat(3, "QUARTER ZIP  ·  KNIT"))]
SW2 = [("SPF", cat(1, "QUARTER ZIP  ·  KNIT")), ("SWF", cat(2, KNIT))]
SW3 = [("SWF", cat(1, KNIT)), ("KF", cat(2, COLLAR)), ("SPF", cat(3, "ALL BLACK  ·  ONE RED"))]
ZH = [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))]
ZHB = [("XWF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME)), ("ZPF", cat(3, "BLACK  ·  WHITE"))]
KZ = [("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD)), ("KKF", cat(3, "COLLAR  ·  HOOD"))]
QF, QKF, QWF, SFIN, ZFIN, KZFIN = ("PF", "PB"), ("KF", "KB"), ("WF", "WB"), ("SPF", "SPB"), ("ZPF", "ZPB"), ("KKF", "KKB")
MP, AU = "mrpopular", "aura"

R = [  # key, track, hook segments, texts, pages, page beats, finale
    # A - Louboutin + quarter zip
    ("A01_collar-says-it-all", MP, [lb("COUPLE", False, 0.5, speed=1.15)], t("the collar says it all."), QW1, 1, QF),
    ("A02_museum", MP, [soles(False, 0.5, speed=1.12)], t("what to wear\nto the museum."), QW3, 1, QF),
    ("A03_black-or-white", MP, [pre("STREET", 1.4, False, 0.5, DROP - 2 * BMP), lb("COUPLE", False, 0.62, speed=1.1)],
     t("black or white?"), QW2, 1, QF),
    ("A04_quiet-luxury", AU, [lb("STREET", True, 0.5)], t("quiet luxury.\none red collar."), QWW, 2, QWF),
    ("A05_red-sole-red-collar", AU, [lb("COUPLE", True, 0.45, speed=0.92)], t("red sole. red collar."), QW1, 2, QF),
    ("A06_details", AU, [nails(True, 0.5)], t("it's in the details."), QW3, 2, QF),
    ("A07_opera", AU, [lb("COUPLE", False, 0.6, speed=0.9)], t("dressed for the opera."), QK, 2, QKF),
    # B - Louboutin + quarter zip + knit
    ("B01_collar-knit", MP, [lb("COUPLE", True, 0.55, speed=1.15)], t("the collar says it all."), SW1, 1, SFIN),
    ("B02_only-wears-black", AU, [soles(True, 0.5)], t("for the one who\nonly wears black."), SW3, 2, SFIN),
    ("B03_museum-all-black", AU, [nails(False, 0.5)], t("what to wear\nto the museum."), SW2, 2, SFIN),
    # C - rose + Louboutin in one hook
    ("C01_she-prefers-red", MP, combo("g3", "NAILS", MP, 3), t("she prefers red.", 0.56, 0.45), QW1, 1, QF),
    ("C02_if-love-was-a-color", MP, combo("g1", "NAILS", MP, 3, rstart=0.3), t("if love was a color.", 0.56, 0.45), ZH, 1, ZFIN),
    ("C03_your-color", MP, combo("g2", "COUPLE", MP, 2, rstart=0.2), t("pov: your color is red.", 0.56, 0.45), QW2, 1, QF),
    ("C04_black-and-red", MP, combo("g3", "SOLES", MP, 2, rflip=True, lflip=True), t("black and red >>", 0.56, 0.45), KZ, 1, KZFIN),
    ("C05_favourite-color", MP, combo("g2", "NAILS", MP, 3, rstart=0.2, rflip=True, lflip=True), t("favourite color.", 0.56, 0.45), SW3, 1, SFIN),
    ("C06_red-to-my-black", AU, combo("g1", "COUPLE", AU, 3, rstart=0.4, rflip=True, rspeed=1.0), t("you're red\nto my black.", 0.56, 0.45), ZHB, 2, ZFIN),
    ("C07_my-color", AU, combo("g3", "COUPLE", AU, 3, rspeed=1.0, lflip=True), t("my color.", 0.56, 0.45), QK, 2, QKF),
]
for i, (k, track, hook, texts, pg, pb, fin) in enumerate(R):
    tag = f"v{i + 1:02d}"
    spec = dict(seed=19000 + i, track=track, segments=hook + pages(pg, None, tag, pb) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=texts)
    json.dump(spec, open(os.path.join(SP, f"v1105_{k}.json"), "w"), indent=1)
    print(f"v1105_{k}")
