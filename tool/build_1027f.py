#!/usr/bin/env python3
"""2026-10-27 batch 6: gothic-cathedral hooks like the 10-23 "second look" reel (4.9k views, 7.6 s avg watch).
Only the hook aesthetic is taken over: cold grey vaults and stained glass. Pages stay on plain black, finale EX MUSEO."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, HOOD, ARA, ROME, COLLAR, SP

H = "/mnt/user-data/uploads/hooks ids/snaptik_"
S2, S3 = H + "7382217770819177761_hd.mp4", H + "7564486079613570360_hd.mp4"


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


R = [  # key, hook, text, y, pages, finale
    ("K01_second-look", clip("x", 5.4, src=S2, flip=True, until="drop"), "the second look\nis the point.", 0.56,
     [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("PF", "PB")),
    ("K02_not-loud", clip("x", 6.6, src=S2, until="drop"), "not loud.\njust red.", 0.50,
     [("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD))], ("KKF", "KKB")),
    # S3 has a watermark at the bottom: framed out with a static 1.07x from the top
    ("K03_quiet-until", clip("x", 0.3, src=S3, zoom=1.07, crop_y=0.0, until="drop"), "quiet until\nit isn't.", 0.56,
     [("ZF", cat(1, HOOD)), ("ZB", cat(2, ARA, ROME))], ("ZPF", "ZPB")),
]
S = {}
for i, (k, hook, text, y, pg, fin) in enumerate(R):
    tag = f"k{i + 1:02d}"
    S[k] = dict(seed=10600 + i, segments=[hook] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"k1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
