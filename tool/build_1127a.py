#!/usr/bin/env python3
"""made 2026-11-27 (night), batch 1127a: 3 reels BT31-BT33. Kirill: 3 more, change the approach to the on-screen text
completely - other ideas, and other hashtags.

Until now every hook carried one short line in Cormorant italic at the top. Here the hook text is a different object
in each reel (tool/textcards.py, passed to loopreel.make as `layer`):
BT31 a museum wall label - the scene described as an exhibit that was never returned (EX MUSEO = taken out of the museum)
BT32 an overheard line - "OVERHEARD IN PRAGUE" + a stranger's question in quotes
BT33 a text-message exchange - her / him bubbles, the red inside as the punchline
The mockup part stays the "bad together" one (black / white on half beats, pair finale), loop 12 beats, 99 BPM grid.
Hashtags: a new set per reel (archive / street style / fit check niches) instead of #redbottoms #coupleoutfits ..."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
import vitrine as V
from vitrine2 import vpage2, vstacked2, vgrid
from build_1119a import gr, sh, couple_red, soles_red
import textcards as T
import loopreel

V.TONES.setdefault("lamp", ((92, 86, 78), (5, 5, 5)))
OUT = "/mnt/user-data/outputs/ready-2026-11-27a/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
WHITE = {"WF", "WB", "XWF", "XWB"}


def o(name):
    return O + "bt1127_" + name + ".jpg"


def pages(tag, keys, tone, labels=("HIS  ·  BLACK", "HERS  ·  WHITE"), scale=0.9, cy=0.47, spot=None):
    return [(0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j], cat(j + 1, labels[1] if k in WHITE else labels[0]),
                             tone, scale=scale, cy=cy, spot=spot), 1)) for j, k in enumerate(keys)]


def fin(path, beats):
    return (beats, img(path, 1))


R = []   # key, ledger text, layer, hook, after, idea

# BT31 museum label - COUPLE in one take, 1.05x, reframed; NOT RETURNED labels on the pages
g = gr(b=-0.012, c=1.05, s=0.9)
R.append(("BT31_exhibit-label", "[museum label] EXHIBIT N° IX / red soles, red collar. / found together. prague, 2026. / on loan from the museum - never returned.",
          T.label("EXHIBIT N° IX", ["red soles, red collar."],
                  ["found together. prague, 2026.", "on loan from the museum - never returned."]),
          [couple_red(g, speed=1.05, zoom=1.15, crop_x=0.55, crop_y=0.66)],
          pages("31", ["KF", "WF", "ZF", "XWF", "KB", "WB"], "vitrine", labels=("NOT RETURNED  ·  BLACK", "NOT RETURNED  ·  WHITE")) +
          [fin(vstacked2(P["PF"], P["ZPF"], o("31f"), "N° VII", tone="vitrine"), 3)],
          "museum wall label on the hook (off-white card); COUPLE one take 1.05x; NOT RETURNED labels, vitrine; QZ pair over zip pair"))

# BT32 overheard - her red nails -> his loafers walking (mirrored) -> his logo sole next to her red sole
g = gr(b=-0.014, c=1.06, s=0.9); g.update(bs=0.012)
R.append(("BT32_overheard-in-prague", "[overheard] OVERHEARD IN PRAGUE / “wait, is his collar red too?”",
          T.quote("OVERHEARD IN PRAGUE", ["“wait, is his collar", "red too?”"]),
          [sh("SOLES", 1.5, 39, g, zoom=1.2, crop_x=0.45), sh("COUPLE", 2.2, 37, g, zoom=1.2, crop_y=0.68, flip=True),
           soles_red(18, g, zoom=1.2, crop_y=0.6)],
          pages("32", ["ZF", "XWF", "KF", "WF", "ZB", "XWB"], "slate") +
          [fin(vgrid([P["KF"], P["WF"], P["ZF"], P["XWF"]], o("32f"), "N° VII", "FIRST LOOK", "slate"), 3)],
          "overheard quote on the hook; SOLES red nails -> COUPLE loafers mirrored -> SOLES logo sole; zips first, slate; 2 x 2"))

# BT33 text messages - bright: one long look at his shoes in the flash -> terrazzo -> the red heel on marble
gb = gr(b=0.02, c=1.06, s=0.86, g=1.05)
R.append(("BT33_text-messages", "[texts] her: wear the black one tonight / him: the one with the red inside? / her: obviously",
          T.chat([("her", "wear the black one tonight"), ("him", "the one with the red inside?"), ("her", "obviously")]),
          [sh("COUPLE", 1.5, 58, gb, zoom=1.2, crop_x=0.5, crop_y=0.6), sh("SOLES", 3.1, 18, gb, zoom=1.1, crop_y=0.5),
           sh("MARBLE", 0.49, 18, gb, zoom=1.15, crop_x=0.5, crop_y=0.55, flip=True)],
          pages("33", ["WF", "KF", "XWF", "ZF", "WB", "KB"], "lamp") +
          [fin(vstacked2(P["ZPF"], P["ZPB"], o("33f"), "N° VII", tone="lamp"), 3)],
          "text messages on the hook; bright: COUPLE shoes in the flash (long) -> SOLES terrazzo -> MARBLE heel mirrored; white first, lamp; zip pair"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, text, layer, hook, after, idea) in enumerate(R):
        ledger.append(["1127a", k, "bad together track (99 BPM grid)", text, idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, text, after, seed=54000 + i, layer=layer)
        json.dump(dict(hook=hook, text=text, after=after), open(os.path.join(SP, f"bt1127_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1127a.json"), "w"), indent=1, ensure_ascii=False)
