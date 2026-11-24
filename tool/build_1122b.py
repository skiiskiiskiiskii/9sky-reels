#!/usr/bin/env python3
"""2026-11-22, batch 1122b: 4 colour-moodboard reels copying the format Kirill sent (4 references, 24K-278K likes):
a fast slideshow of one colour, one small lowercase serif line in the middle the whole time, no hook, no catalogue
pages. Adapted to 9sky: dark red / black (one comment under the black reference asked for "this and dark red"),
museum, theatre, candles, busts, our louboutin and rose clips, and the IX zip hoodie / quarter zip (red-lined hood,
red collar) dropped in as 3-4 of the frames, last frame always the product.

A01 my color.             - dark red, copies @c0smic_girl4 "my color." (102K): its 20 cut times, 12.4 s
A02 if i was a color      - black, copies @blackswan__14 "if i was a color" (278K): grey grainy square band,
                            16 cuts at a half beat, played twice; only the dark red keeps its colour
A03 if aura had a color.  - burgundy, copies @rukmini_surve (24K): 16 cuts on the beat, ~10 s
A04 favourite color.      - black + dark red, copies @rukmini_surve "favourite color." (252K): beat cuts with a
                            quarter-beat strobe in the middle, ~14.7 s
Library check 11-22: candles_red_05, candles_red_15 and museum_night_21 carry a Meta AI watermark - never use them.
Silent: post with the reference's sound (Use audio), or the F05 sound for A02-A04 (cut on 99 BPM)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import P, SP
from build_1115 import ROSE, SHOOT

U = "/mnt/user-data/uploads/9sky-reels/"
B = 60 / 99.0                                     # one beat of the F05 sound


def aes(cat, n, **kw):
    return dict(img=f"{U}aesthetics/{cat}/9skyaes_{cat}_{n:02d}.jpg", **kw)


def ff(i, **kw):                                  # ffff folder by sheet position
    name = f"statues_athletic_{i + 1:02d}" if i < 26 else f"statues_dark_{i - 25:02d}"
    return dict(img=f"{U}ffff/9skyaes_{name}.jpg", **kw)


def met(name, **kw):
    return dict(img=f"{U}hooks/art-met/9sky_art_{name}.jpg", **kw)


def mock(key, focus=(0.5, 0.5), z0=1.0, z1=1.05, gamma=0.72, **kw):
    """product frame: darks lifted and no vignette, so the black garment reads on its black background"""
    return dict(img=P[key], focus=list(focus), z0=z0, z1=z1, gamma=gamma, vig=False, **kw)


def clip(src, start, **kw):
    return dict(clip=src, start=start, **kw)


A3 = U + "hooks/inbox/vol2/A3_red-nails-hands.mp4"           # 720x848, dark red nails
A13 = U + "hooks/inbox/vol2/A13_red-polish-closeup.mp4"       # 1080x1080
A7 = U + "hooks/inbox/vol2/A7_holding-hands-black-sleeves.mp4"
A8 = U + "hooks/inbox/vol2/A8_hand-in-hand-car-night.mp4"
OUT = lambda z0, z1: dict(z0=z0, z1=z1)            # push-in (z0<z1) or pull-out (z0>z1)
HOOD = dict(focus=(0.5, 0.27), z0=2.1, z1=2.25)    # close-up of the red-lined hood
COLLAR = dict(focus=(0.5, 0.29), z0=2.3, z1=2.45)  # close-up of the red collar

REELS = {}

# A01 - the c0smic_girl4 cut list, 20 shots
REELS["A01_my-color"] = dict(
    seed=1, text="my color.", text_y=0.48, text_size=56,
    cuts=[0.733, 1.2, 1.933, 2.6, 3.2, 3.733, 4.2, 4.667, 5.067, 5.4, 5.8, 6.267, 6.6, 7.333, 7.933, 8.733,
          9.333, 10.267, 10.8, 12.4],
    look=dict(c=1.05, b=-0.01, grain=2, vignette=0.25),
    shots=[met("m2_02", focus=[0.5, 0.42], **OUT(1.0, 1.08)),
           clip(ROSE + "g1.mp4", 0.5, zoom=1.1, crop_y=0.3),
           aes("candles_red", 14, **OUT(1.06, 1.0)),
           aes("theatre_red", 3),
           aes("busts_red", 2, **OUT(1.0, 1.07)),
           clip(P["SOLES"], 6.6, zoom=1.2, crop_y=0.45),
           mock("ZF", **HOOD),
           aes("candles_red", 10),
           aes("palace_red", 19, **OUT(1.08, 1.0)),
           aes("theatre_red", 24),
           clip(A3, 1.5),
           aes("candles_red", 16),
           met("m2_03", focus=[0.5, 0.5], **OUT(1.05, 1.12)),
           clip(SHOOT + "s12_0.mp4", 2.3),
           aes("theatre_red", 11, **OUT(1.0, 1.06)),
           mock("KF", **COLLAR),
           aes("busts_red", 22),
           aes("theatre_red", 22, **OUT(1.06, 1.0)),
           clip(P["MARBLE"], 0.2, zoom=1.15),
           mock("ZF", z0=1.0, z1=1.05)])

# A02 - blackswan__14 format: square band, half-beat cuts, played twice, grey world with only the red left
REELS["A02_if-i-was-a-color"] = dict(
    seed=2, text="if i was a color", text_y=0.5, text_size=46, band=[0.22, 0.78], repeat=2,
    cuts=[round(B / 2 * k, 3) for k in range(1, 16)],
    look=dict(keep_red=True, c=1.15, b=-0.02, grain=7, vignette=0.35),
    shots=[ff(55),
           clip(P["COUPLE"], 1.8, band_y=0.8),
           ff(48),
           clip(P["NAILS"], 2.2, band_y=0.6),
           clip(P["SOLES"], 0.0, band_y=0.75),
           aes("museum_night", 18),
           ff(63),
           mock("KF", **COLLAR),
           aes("candles_red", 28),
           clip(P["SOLES"], 6.7, zoom=1.15, band_y=0.45),
           ff(57),
           clip(ROSE + "g3.mp4", 0.3, band_y=0.35),
           clip(A7, 2.0, band_y=0.6),
           aes("theatre_red", 14),
           mock("ZF", **HOOD)])

# A03 - rukmini_surve "if aura had a color.": 16 shots on the beat
REELS["A03_if-aura-had-a-color"] = dict(
    seed=3, text="if aura had a color.", text_y=0.48, text_size=54,
    cuts=[round(B * k, 3) for k in range(1, 16)] + [10.3],
    look=dict(c=1.05, b=-0.01, s=0.95, grain=2, vignette=0.2),
    shots=[clip(A13, 5.0, zoom=1.05),
           aes("palace_red", 3, **OUT(1.0, 1.07)),
           aes("theatre_red", 2),
           mock("XWF", focus=(0.5, 0.2), z0=2.1, z1=2.25),   # hood kept below the line (white on white)
           aes("people_museum", 3, **OUT(1.06, 1.0)),
           clip(P["MARBLE"], 0.0, flip=True, zoom=1.1),
           aes("candles_red", 13),
           aes("gallery_red", 27, **OUT(1.0, 1.07)),
           clip(P["COUPLE"], 0.55, zoom=1.2, crop_y=0.5),
           aes("palace_red", 21),
           aes("people_museum", 12, **OUT(1.0, 1.06)),
           mock("KF", z0=1.0, z1=1.06),
           aes("theatre_red", 30),
           clip(P["COUPLE"], 4.55, zoom=1.15, crop_y=0.75),
           aes("busts_red", 26, **OUT(1.07, 1.0)),
           mock("ZPF", z0=1.0, z1=1.04)])

# A04 - rukmini_surve "favourite color.": beats, a quarter-beat strobe of 8 frames, beats, product
q = [round(B * k, 3) for k in range(1, 9)]
q += [round(q[-1] + B / 4 * k, 3) for k in range(1, 9)]
q += [round(q[-1] + B * k, 3) for k in range(1, 13)]
q += [round(q[-1] + 1.4, 3)]
REELS["A04_favourite-color"] = dict(
    seed=4, text="favourite color.", text_y=0.48, text_size=54, cuts=q,
    look=dict(c=1.06, b=-0.01, grain=3, vignette=0.2),
    shots=[aes("palace_red", 8, **OUT(1.0, 1.07)),
           clip(A3, 5.0),
           ff(47),
           clip(P["SOLES"], 1.55, zoom=1.1),
           aes("candles_red", 11, **OUT(1.06, 1.0)),
           mock("ZF", **HOOD),
           aes("museum_night", 8),
           aes("theatre_red", 7, **OUT(1.0, 1.06)),
           aes("candles_red", 24), aes("theatre_red", 20), aes("busts_red", 11), aes("palace_red", 17),
           ff(34), aes("gallery_red", 1), aes("theatre_red", 16), aes("candles_red", 4),
           clip(P["COUPLE"], 4.5, zoom=1.1, crop_y=0.75, flip=True),
           ff(44, **OUT(1.0, 1.06)),
           clip(ROSE + "g2.mp4", 0.5, zoom=1.1, crop_y=0.3),
           mock("KF", **COLLAR),
           aes("palace_red", 31),
           aes("people_museum", 23, **OUT(1.06, 1.0)),
           aes("theatre_red", 25),
           clip(P["NAILS"], 5.5, zoom=1.05),
           aes("busts_red", 4, **OUT(1.0, 1.07)),
           aes("palace_red", 13),
           ff(53),
           aes("candles_red", 26, **OUT(1.0, 1.06)),
           mock("ZF", z0=1.0, z1=1.05)])

if __name__ == "__main__":
    for k, spec in REELS.items():
        for sh in spec["shots"]:
            src = sh.get("img") or sh.get("clip")
            assert os.path.exists(src), src
        json.dump(spec, open(os.path.join(SP, f"a1122_{k}.json"), "w"), indent=1, ensure_ascii=False)
        print(k, len(spec["shots"]), "shots", spec["cuts"][-1] * spec.get("repeat", 1), "s")
