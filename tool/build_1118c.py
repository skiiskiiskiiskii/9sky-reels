#!/usr/bin/env python3
"""made 2026-11-18, single test 1118c: the first reel made for Edits (Edits for Mac is connected to Claude now).
What is new: the SOUND. Every reel since 1107 used Cyn - North Pole / mr popular; this one is cut to
"LV Sandals" (EsDeeKid, Fakemink, Rico Ace) from the Edits / Instagram music library, so it is posted from Edits
with the licensed track attached. Beat grid read from Edits: 0.632 s (95 BPM), downbeat at source 12.62 s.
Music in-point 9.48 s -> that downbeat lands on the 3.13 s cut. Pages 1 beat each, finale 4 beats, loop = 12 beats
(7.6 s) so the music wraps on the grid.
Hook: 3-shot Louboutin mix at real speed (SOLES -> COUPLE wide mirrored -> COUPLE tight red sole), line = a question.

LV01 his or hers?   SOLES (watch) -> COUPLE wide mirrored -> COUPLE tight red sole; his black / her white QZ"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
from vitrine import vpage, vstacked
from build_1118b import sh, red_end
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-18c/"
BEAT = 0.632
TONE = "vitrine"

hook = [sh("SOLES", 1.0, 34, zoom=1.1), sh("COUPLE", 2.6, 32, zoom=1.0, crop_y=0.6, flip=True),
        red_end("COUPLE", zoom=1.3, crop_x=0.42, crop_y=0.78)]
after = [(1, img(vpage(P["KF"], O + "lv01a.jpg", "N° I", cat(1, "HIS  ·  BLACK"), TONE), 1)),
         (1, img(vpage(P["WF"], O + "lv01b.jpg", "N° II", cat(2, "HERS  ·  WHITE"), TONE), 1)),
         (4, img(vstacked(P["PF"], P["PB"], O + "lv01c.jpg", "N° III", tone=TONE), 1))]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    k = "LV01_his-or-hers"
    r = loopreel.make(OUT + k + ".mp4", hook, "his\nor hers?", after, seed=41000, beat=BEAT, total_beats=12)
    json.dump(dict(hook=hook, line="his or hers?", after=after, beat=BEAT, music="LV Sandals, in-point 9.48 s"),
              open(os.path.join(SP, f"lv1118_{k}.json"), "w"), indent=1, ensure_ascii=False)
    json.dump([["1118c", k, "LV Sandals (Edits library)", "his or hers?",
                "first Edits test: new licensed track LV Sandals, 95 BPM, music in-point 9.48 s; SOLES -> COUPLE wide "
                "mirrored -> COUPLE tight; his black / her white QZ"]], open(os.path.join(SP, "ledger_1118c.json"), "w"), indent=1)
    print(k, json.dumps(r))
