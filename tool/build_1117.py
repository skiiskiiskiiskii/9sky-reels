#!/usr/bin/env python3
"""made 2026-11-16 night, batch 1117a: 3 reels for 11-17 (Kirill: today's 5 did not collect well, wants 3 more).
Recommended to post the next day: 5 trials were already out on 11-16, and 11 in one day on 11-15 ended in a stop.
Lines v2 (Kirill picked them, 11-16 22:15: the first lines were "too strange" - keep lines short and plain).
Back to the two strongest 11-15 mechanics with the hooks unchanged, only new lines, plus one new pair line.

S01 one second of red. that's all she gives. - the K02 hook as is (NAILS -> COUPLE, smooth slow-down on the red sole;
    K02 = 8.7K); black quarter zip
S02 let her wear the red.                       - the K01 hook as is (SOLES up to the logo sole; K01 = 6.5K, 69%);
    his black quarter zip, pair finale
S03 black shoes for him. red soles for her.     - MARBLE (his black shoe, her red heels) -> SOLES both red soles
    (4.8-6.8 s, not used by S02); his/hers pages, pair finale
mrpopular timing, post with the F05 audio."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import cat, COLLAR, ARA, ROME, P
from build_1115 import lb, clip, t, MARBLE_LEN, build as build1115

C2 = 1.9178787878787877            # K02 segment lengths, copied from specs/k1112_K02
HIS, HERS = "HIS  ·  BLACK", "HERS  ·  WHITE"
S = [  # key, tone, hook, texts, pages, finale, idea
    ("S01_red-soles-red-collar", "oxblood",
     [lb("NAILS", start=1.6, dur=C2, speed=1.1, zoom=1.0),
      lb("COUPLE", start=3.917878787878788, dur=0.6121212121212122, speed=1.0, zoom=1.3, crop_x=0.42, crop_y=0.76, flip=True),
      lb("COUPLE", start=4.53, speed=0.5, zoom=1.3, crop_x=0.42, crop_y=0.76, flip=True, smooth=True)],
     t("red soles,\nred collar."),
     [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("KF", "KB"),
     "K02 hook unchanged (NAILS -> COUPLE slow on the red sole), new line; black quarter zip"),
    ("S02_dress-to-match-her", "vitrine",
     [lb("SOLES", start=1.59, speed=1.0, zoom=1.1, crop_y=0.6)],
     t("dress to\nmatch her."),
     [("KF", cat(1, HIS + "  ·  RED COLLAR")), ("KB", cat(2, ARA, ROME))], ("PF", "PB"),
     "K01 hook unchanged (SOLES to the logo sole), new imperative line from his side; pair finale"),
    ("S03_his-and-hers", "slate",
     [clip(P["MARBLE"], start=0.0, dur=MARBLE_LEN),
      lb("SOLES", start=4.8, speed=1.0, zoom=1.1, crop_y=0.6)],
     t("his and hers."),
     [("KF", cat(1, HIS)), ("WF", cat(2, HERS))], ("PF", "PB"),
     "MARBLE (his black shoe + her red heels) -> SOLES both red soles 4.8-6.8; his/hers pages, pair finale"),
]

if __name__ == "__main__":
    build1115("1117a", S, "s1117", 34000, tag_letter="s")
