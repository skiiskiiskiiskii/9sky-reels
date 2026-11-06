#!/usr/bin/env python3
"""2026-11-06: 13 reels, picked from the 11-05 stats.
- Louboutin + quarter zip straight is still the best family (56-67%); COUPLE and SOLES lead, NAILS and STREET
  alone are weakest (46-48%) -> 6 reels, COUPLE x3, SOLES x2, one STREET->COUPLE montage.
- Louboutin + quarter zip + knit brings the most saves/shares (B02: 30 saves, 22 shares) -> 3 reels.
- Rose x Louboutin works when dynamic with several cuts (N04 3-shot 54%, C04 rose->soles 50%); calm combos
  and grey-world sit at 30-44% -> 4 reels, all mr popular, 3-shot or rose->soles.
8 of 13 on mr popular. One line of text per hook."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, pages, fin_path, cat, COLLAR, HOOD, IX, ARA, ROME, SP, P

G = "/mnt/user-data/uploads/flowers hooks/"
GR = dict(c=1.04, s=0.92, b=-0.012)
BMP, BAU, DROP = 60 / 99.0, 60 / 123.05, 3.13
C2, C4 = DROP - 2 * BMP, DROP - 4 * BMP
MP, AU = "mrpopular", "aura"


def lb(key, start=None, dur=None, speed=1.0, flip=False, crop_x=0.5, lead=0.42, **kw):
    d = dict(type="clip", src=P[key], speed=speed, zoom=1.035, crop_x=crop_x, flip=flip, grade=GR)
    d.update(dict(align_red=True, lead=lead) if start is None else dict(start=start, align_red=False))
    d.update(dict(dur=dur) if dur else dict(until="drop"))
    d.update(kw)
    return d


def soles(speed=0.95, flip=False, tail=DROP, dur=None):
    """logo sole enters ~4.3 s of the source; keep it ~0.4 s on screen before the drop"""
    return lb("SOLES", start=4.3 - (tail - 0.42) * speed, speed=speed, flip=flip, dur=dur)


def rose(name, dur, start=0.0, speed=1.15, flip=False):
    return dict(type="clip", src=G + name + ".mp4", start=start, dur=dur, align_red=False, speed=speed,
                zoom=1.0, crop_x=0.5, flip=flip, grade={})


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
ZHB = [("XWF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME)), ("ZPF", cat(3, "BLACK  ·  WHITE"))]
QF, QKF, QWF, SFIN, ZFIN = ("PF", "PB"), ("KF", "KB"), ("WF", "WB"), ("SPF", "SPB"), ("ZPF", "ZPB")

R = [  # key, track, hook segments, texts, pages, page beats, finale
    # Louboutin + quarter zip
    ("L01_red-at-both-ends", MP, [lb("COUPLE", speed=1.15, crop_x=0.55)], t("red at both ends."), QW1, 1, QF),
    ("L02_collar-says-it-all", AU, [lb("COUPLE", speed=0.92, flip=True, crop_x=0.45)], t("the collar says it all."), QW2, 2, QF),
    ("L03_opera", AU, [lb("COUPLE", speed=0.9, crop_x=0.6)], t("dressed for the opera."), QK, 2, QKF),
    ("L04_museum", MP, [soles(speed=1.12, flip=True)], t("what to wear\nto the museum."), QW3, 1, QF),
    ("L05_date-heels", AU, [soles()], t("she wore red soles.\nhe wore the collar."), QW1, 2, QF),
    ("L06_black-or-white", MP, [lb("STREET", start=1.4, dur=C2, speed=1.1, flip=True), lb("COUPLE", speed=1.1, flip=True)],
     t("black or white?"), QWW, 1, QWF),
    # Louboutin + quarter zip + knit
    ("K01_only-wears-black", AU, [soles(flip=True)], t("for the one who\nonly wears black."), SW3, 2, SFIN),
    ("K02_collar-knit", MP, [lb("COUPLE", speed=1.15, flip=True, crop_x=0.5)], t("the collar says it all."), SW1, 1, SFIN),
    ("K03_museum-all-black", AU, [lb("COUPLE", speed=0.92, crop_x=0.5)], t("what to wear\nto the museum."), SW2, 2, SFIN),
    # rose x Louboutin, all dynamic
    ("X01_red-in-the-right-places", MP,
     [rose("g3", C4), lb("NAILS", start=2.0, dur=C2 - C4, speed=1.1), lb("COUPLE", speed=1.1)],
     t("red, in the right places.", 0.56, 0.45), QW2, 1, QF),
    ("X02_black-and-red", MP, [rose("g2", C2, start=0.2, flip=True), soles(speed=1.1, tail=DROP - C2)],
     t("black and red >>", 0.56, 0.45), SW3, 1, SFIN),
    ("X03_if-love-was-a-color", MP,
     [rose("g1", C4, start=0.3), lb("NAILS", start=2.0, dur=C2 - C4, speed=1.1, flip=True), soles(speed=1.1, tail=DROP - C2)],
     t("if love was a color.", 0.56, 0.45), ZHB, 1, ZFIN),
    ("X04_red-always-wins", MP,
     [rose("g2", C4, start=0.2), lb("STREET", start=1.4, dur=C2 - C4, speed=1.1), lb("COUPLE", speed=1.1, flip=True)],
     t("red always wins.", 0.56, 0.45), QW1, 1, QF),
]
for i, (k, track, hook, texts, pg, pb, fin) in enumerate(R):
    tag = f"x{i + 1:02d}"
    spec = dict(seed=21000 + i, track=track, segments=hook + pages(pg, None, tag, pb) +
                [img(fin_path(fin[0], fin[1], tag, "N° III" if len(pg) == 2 else "N° IV"), 4)], texts=texts)
    json.dump(spec, open(os.path.join(SP, f"x1106_{k}.json"), "w"), indent=1)
    print(f"x1106_{k}")
