#!/usr/bin/env python3
"""2026-11-24 04:08, batch 1124c: 2 provocative couple reels V01-V02 for Travis Scott's "twin bitches"
(Kirill adds the track himself; no need to cut to it). 6.77 s.
Hook to 3.13 s as always (both of them / both red soles), then the "twins": black and white cut against each other
on every half beat (6 pages), then the pair finale for 3 beats. Plain cuts only, no effects.
V01 we match. deal with it.  COUPLE full frame, crop low; qz black / white / zip black / white / qz / zip, qz pair
V02 twinning on purpose.     SOLES (his red logo sole + her red soles); zip black / white / qz black / white / ..., zip pair"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, SP, P, O
from build_1115 import lb, t, MP
from vitrine import vpage, vstacked

NUMS = ["I", "II", "III", "IV", "V", "VI", "VII"]
LABEL = {"KF": "HIS  ·  BLACK", "WF": "HERS  ·  WHITE", "ZF": "HIS  ·  BLACK", "XWF": "HERS  ·  WHITE"}

V = [  # key, tone, hook, text, pages (half beat each), finale (3 beats), idea
    ("V01_we-match-deal-with-it", "vitrine", [lb("COUPLE", speed=1.1, zoom=1.0, crop_y=0.7)],
     t("we match.\ndeal with it."), ["KF", "WF", "ZF", "XWF", "KF", "WF"], ("PF", "PB"),
     "COUPLE full frame -> black / white cut on every half beat -> quarter zip pair"),
    ("V02_twinning-on-purpose", "vitrine", [lb("SOLES", start=1.6, speed=1.0, zoom=1.0, crop_y=0.6, flip=True)],
     t("twinning\non purpose."), ["ZF", "XWF", "KF", "WF", "ZF", "XWF"], ("ZPF", "ZPB"),
     "SOLES mirrored (both red soles) -> black / white cut on every half beat -> zip hoodie pair"),
]


def build(batch="1124c", prefix="v1124", seed0=42000):
    ledger = []
    for i, (k, tone, hook, texts, pages, fin, idea) in enumerate(V):
        segs = list(hook)
        for j, pk in enumerate(pages):
            segs.append(img(vpage(P[pk], O + f"v{i + 1:02d}y{j}.jpg", "N° " + NUMS[j], cat(j + 1, LABEL[pk]), tone), 0.5))
        segs.append(img(vstacked(P[fin[0]], P[fin[1]], O + f"v{i + 1:02d}yc.jpg", "N° " + NUMS[len(pages)], tone=tone), 3))
        spec = dict(seed=seed0 + i, track=MP, segments=segs, texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{prefix}_{k}.json"), "w"), indent=1, ensure_ascii=False)
        ledger.append([batch, k, MP, tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    build()
