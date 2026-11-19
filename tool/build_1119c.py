#!/usr/bin/env python3
"""made 2026-11-19, batch 1119c: remasters of the 4 biggest reels of the last 15 days (Metricool 11-19):
F05 67.8K, H08 15.7K, K02 8.9K, K01 7.4K (Kirill's pick, from his screenshots; each keeps its own track:
F05 and K02 Cyn - North Pole, H08 mr popular, K01 Tragic Freestyle). Kirill: repost them, keep the on-screen line and the music and the
combination people liked, but so that Instagram pushes them as new.

Kept: the same hook moment (same clip, same seconds, same speed, the slow-down where the original had one),
the same line word for word, the same sound (F05 audio, drop on the 3.13 s cut), the same page order and garments.
Changed (so the file is not a copy): re-rendered from the sources, hook mirrored and reframed 5-10 %, a light
grade shift, pages re-drawn with vitrine2 (scale / glow position), seamless loop (12 beats, 7.27 s instead of
6.77 s). H08 and K02 had the black knit, which is no longer in the line-up -> replaced by the black zip hoodie
(same all-black pair)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, HOOD, ARA, ROME, P, O, SP
from vitrine2 import vpage2, vstacked2
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-19c/"


def grade(**kw):
    g = dict(c=1.04, s=0.92, b=-0.012)
    g.update(kw)
    return g


def couple(**kw):
    d = dict(type="clip", src=P["COUPLE"], speed=1.12, zoom=1.2, crop_x=0.5, crop_y=0.6, flip=True, grade=grade(),
             align_red=True, lead=0.42)
    d.update(kw)
    return d


def clip(key, start, n, speed=1.0, **kw):
    d = dict(type="clip", src=P[key], start=start, align_red=False, speed=speed, zoom=1.1, crop_x=0.5, crop_y=0.5,
             flip=False, grade=grade(), n=n)
    d.update(kw)
    return d


def o(n):
    return O + "r1119_" + n + ".jpg"


def pg(path, beats=1):
    return (beats, img(path, 1))


R = []
# F05 it starts with the shoes. - COUPLE tight on the shoes; black QZ front, back, stacked finale, vitrine
R.append(("F05r_it-starts-with-the-shoes", "it starts\nwith the shoes.",
          [couple(zoom=1.26, crop_x=0.43, crop_y=0.72, grade=grade(c=1.05, s=0.9, b=-0.016, rm=0.02))],
          [pg(vpage2(P["KF"], o("f0"), "N° I", cat(1, COLLAR), "vitrine", scale=0.92, cy=0.46)),
           pg(vpage2(P["KB"], o("f1"), "N° II", cat(2, ARA, ROME), "vitrine", scale=0.92, cy=0.46)),
           pg(vstacked2(P["KF"], P["KB"], o("fc"), "N° III", tone="vitrine"), 4)],
          "F05 remaster: same COUPLE moment, mirrored, reframed; same line; pages re-drawn; loop"))
# K01 match her red. - SOLES (her nails, watch, pumps -> logo sole); black QZ front, back, stacked finale, vitrine.
# SOLES is not mirrored: the signature on the sole would read backwards.
R.append(("K01r_match-her-red", "match her red.",
          [clip("SOLES", 1.59, 94, zoom=1.18, crop_x=0.46, crop_y=0.58, grade=grade(c=1.05, s=0.9, bs=0.02))],
          [pg(vpage2(P["KF"], o("k10"), "N° I", cat(1, COLLAR), "vitrine", scale=0.9, spot=(0.5, 0.44, 0.6, 0.35))),
           pg(vpage2(P["KB"], o("k11"), "N° II", cat(2, ARA, ROME), "vitrine", scale=0.9, spot=(0.5, 0.44, 0.6, 0.35))),
           pg(vstacked2(P["KF"], P["KB"], o("k1c"), "N° III", tone="vitrine"), 4)],
          "K01 remaster: same SOLES moment, reframed, cooler; same line; pages re-drawn; loop"))
# H08 red goes underneath. - NAILS -> COUPLE -> COUPLE 0.5x on the sole; QZ + (knit ->) black zip hoodie, slate
SLOW = 24
R.append(("H08r_red-goes-underneath", "red goes\nunderneath.",
          [clip("NAILS", 2.05, 52, speed=1.1, zoom=1.15, flip=True),
           clip("COUPLE", 3.918, 18, zoom=1.26, crop_y=0.7, flip=True),
           clip("COUPLE", 4.53, SLOW, speed=0.5, smooth=True, zoom=1.26, crop_y=0.7, flip=True)],
          [pg(vpage2(P["KF"], o("h0"), "N° I", cat(1, COLLAR), "slate", scale=0.9)),
           pg(vpage2(P["ZF"], o("h1"), "N° II", cat(2, HOOD), "slate", scale=0.9)),
           pg(vstacked2(P["KF"], P["ZF"], o("hc"), "N° III", tone="slate"), 4)],
          "H08 remaster: same nails -> sole slow-down, mirrored, reframed; knit swapped for the black zip hoodie; loop"))
# K02 never show all the red. - same recipe, tighter; (knit ->) black zip hoodie, QZ, slate
R.append(("K02r_never-show-all-the-red", "never show\nall the red.",
          [clip("NAILS", 1.65, 52, speed=1.1, zoom=1.06),
           clip("COUPLE", 3.918, 18, zoom=1.36, crop_x=0.44, crop_y=0.74),
           clip("COUPLE", 4.53, SLOW, speed=0.5, smooth=True, zoom=1.36, crop_x=0.44, crop_y=0.74)],
          [pg(vpage2(P["ZF"], o("k20"), "N° I", cat(1, HOOD), "slate", scale=0.88, spot=(0.5, 0.42, 0.6, 0.34))),
           pg(vpage2(P["KF"], o("k21"), "N° II", cat(2, COLLAR), "slate", scale=0.88, spot=(0.5, 0.42, 0.6, 0.34))),
           pg(vstacked2(P["ZF"], P["KF"], o("k2c"), "N° III", tone="slate"), 4)],
          "K02 remaster: same nails -> sole slow-down, un-mirrored now, tighter; knit swapped for the black zip hoodie; loop"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1119c", k, "F05 / mr popular", line.replace("\n", " "), idea])
        if only and k[:3] not in only:
            continue
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=44000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"r1119_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1119c.json"), "w"), indent=1)
