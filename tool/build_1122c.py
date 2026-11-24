#!/usr/bin/env python3
"""2026-11-22 06:14, batch 1122c: the 1122b moodboards rebuilt the way Kirill asked -
"the start only picture frames, no mockups, 2-4 s, then the drop, and after it frames of my mockups".

Structure (F05 timing, mrpopular 99 BPM, drop 3.13 s, post with the F05 sound):
  0 - 3.13 s   moodboard of pictures only (aesthetics library + Met paintings), cut on the beat grid that ends on the drop,
               the small serif line from the reference in the middle, fading out on the drop
  3.13 s -     only mockup frames (fronts, backs, hood / collar close-ups, pairs), last frame held 2 beats
A01v2 my color.            dark red; 5 pictures on the beat; 6 beats of mockups (half beats, then beats) - 6.77 s
A02v2 if i was a color     grey square band, grain, only red keeps colour; 10 pictures on half beats,
                           mockups on half beats in the same look - 6.77 s
A03v2 if aura had a color. burgundy; 5 pictures on the beat; white zip / white quarter zip on the beat - 6.77 s
A04v2 favourite color.     black + dark red; 3 pictures on the beat, then an 8-frame quarter-beat strobe into the drop;
                           8 beats of mockups - 7.98 s"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import SP
from build_1122b import aes, ff, met, mock, OUT, HOOD, COLLAR, B

DROP = 3.13


def intro(n, step):
    """n picture cuts on a grid of `step` that ends exactly on the drop (the first picture takes what is left)"""
    return [round(DROP - step * k, 3) for k in range(n - 1, -1, -1)]


def after(beats):
    """cut times after the drop, from a list of shot lengths in beats"""
    out, t = [], DROP
    for b in beats:
        t += b * B
        out.append(round(t, 3))
    return out


WHOOD = dict(focus=(0.5, 0.27), z0=2.1, z1=2.25)     # white hood close-up (the line is gone after the drop)
BACK = dict(focus=(0.5, 0.47), z0=1.45, z1=1.55)    # embossed ornament on the back
R = {}

R["A01v2_my-color"] = dict(
    seed=11, text="my color.", text_y=0.48, text_size=56, text_to=DROP,
    cuts=intro(5, B) + after([0.5, 0.5, 0.5, 0.5, 1, 1, 2]),
    look=dict(c=1.05, b=-0.01, grain=2, vignette=0.25),
    shots=[met("m2_02", focus=[0.5, 0.42], **OUT(1.0, 1.08)),
           aes("candles_red", 14, **OUT(1.06, 1.0)),
           aes("theatre_red", 24),
           aes("busts_red", 22, **OUT(1.0, 1.07)),
           aes("theatre_red", 22, **OUT(1.06, 1.0)),
           # drop - mockups only
           mock("ZF", **HOOD),
           mock("KF", **COLLAR),
           mock("ZF", z0=1.0, z1=1.04),
           mock("KF", z0=1.04, z1=1.0),
           mock("ZB", gamma=0.62, **BACK),
           mock("KB", gamma=0.65),
           mock("ZPF", z0=1.0, z1=1.05)])

R["A02v2_if-i-was-a-color"] = dict(
    seed=12, text="if i was a color", text_y=0.5, text_size=46, text_to=DROP, band=[0.22, 0.78],
    cuts=intro(10, B / 2) + after([0.5] * 8 + [2]),
    look=dict(keep_red=True, c=1.15, b=-0.02, grain=7, vignette=0.35),
    shots=[ff(55), ff(53), ff(65), ff(63), aes("candles_red", 28),
           ff(57), aes("theatre_red", 14), ff(44), aes("busts_red", 11), aes("theatre_red", 21),
           # drop - mockups only, same grey world (the red lining and collar stay red)
           mock("ZF", **HOOD),
           mock("KF", **COLLAR),
           mock("XWF", **WHOOD),
           mock("ZF", z0=1.0, z1=1.04),
           mock("WF", z0=1.0, z1=1.04),
           mock("KF", z0=1.04, z1=1.0),
           mock("XWF", z0=1.0, z1=1.04),
           mock("KB", gamma=0.65),
           mock("ZPF", z0=1.0, z1=1.05)])

R["A03v2_if-aura-had-a-color"] = dict(
    seed=13, text="if aura had a color.", text_y=0.48, text_size=54, text_to=DROP,
    cuts=intro(5, B) + after([1, 1, 1, 1, 2]),
    look=dict(c=1.05, b=-0.01, s=0.95, grain=2, vignette=0.2),
    shots=[aes("palace_red", 3, **OUT(1.0, 1.07)),
           aes("theatre_red", 2),
           aes("people_museum", 3, **OUT(1.06, 1.0)),
           aes("gallery_red", 27, **OUT(1.0, 1.07)),
           aes("busts_red", 26, **OUT(1.07, 1.0)),
           # drop - white editions, burgundy lining
           mock("XWF", **WHOOD),
           mock("XWF", z0=1.0, z1=1.05),
           mock("XWB", z0=1.05, z1=1.0),
           mock("WF", z0=1.0, z1=1.05),
           mock("ZPF", z0=1.0, z1=1.05)])

R["A04v2_favourite-color"] = dict(
    seed=14, text="favourite color.", text_y=0.48, text_size=54, text_to=DROP,
    cuts=[round(DROP - 2 * B - B * k, 3) for k in (2, 1, 0)] +                  # 3 pictures on the beat
         [round(DROP - 2 * B + B / 4 * k, 3) for k in range(1, 9)] +              # strobe, last cut = drop
         after([1, 1, 1, 0.5, 0.5, 1, 1, 2]),
    look=dict(c=1.06, b=-0.01, grain=3, vignette=0.2),
    shots=[aes("palace_red", 8, **OUT(1.0, 1.07)),
           ff(47),
           aes("candles_red", 11, **OUT(1.06, 1.0)),
           # quarter-beat strobe into the drop
           aes("candles_red", 24), aes("theatre_red", 20), aes("busts_red", 4), aes("palace_red", 17),
           ff(34), aes("theatre_red", 16), aes("candles_red", 4), aes("theatre_red", 7),
           # drop - mockups only
           mock("ZF", z0=1.0, z1=1.05),
           mock("ZF", **HOOD),
           mock("ZB", gamma=0.62, **BACK),
           mock("KF", **COLLAR),
           mock("KF", z0=1.04, z1=1.0),
           mock("KB", gamma=0.65),
           mock("PF", z0=1.0, z1=1.04),
           mock("ZPF", z0=1.0, z1=1.05)])

if __name__ == "__main__":
    for k, spec in R.items():
        assert len(spec["cuts"]) == len(spec["shots"]), (k, len(spec["cuts"]), len(spec["shots"]))
        assert DROP in spec["cuts"], (k, "no cut on the drop")
        for sh in spec["shots"]:
            assert os.path.exists(sh["img"]), sh["img"]
        json.dump(spec, open(os.path.join(SP, f"c1122_{k}.json"), "w"), indent=1, ensure_ascii=False)
        print(k, len(spec["shots"]), "shots", spec["cuts"][-1], "s", spec["cuts"][:spec["cuts"].index(DROP) + 2])
