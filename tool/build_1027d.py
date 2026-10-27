#!/usr/bin/env python3
"""2026-10-27 batch 4: EX MUSEO hooks from Kirill's research (EX_MUSEO_Hooks.md, top 8).
Each hook was picked so that picture -> phrase -> garment reads as one thread."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, cat, COLLAR, HOOD, ARA, ROME, IX, SP

X = "/mnt/user-data/uploads/EX_MUSEO_hooks/"
QZ = ([("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB"))
QZW = ([("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], ("PF", "PB"))
QIX = ([("KF", cat(1, IX)), ("PF", cat(2, COLLAR))], ("PF", "PB"))
ZH = ([("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
ZHW = ([("XWF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
ZHB = ([("ZB", cat(1, ARA, ROME)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"))
BW = ([("PF", cat(1, "BLACK  ·  WHITE")), ("ZPF", cat(2, HOOD))], ("PF", "PB"))


def tx(text, y):
    return {"text": text, "from": 0, "to": "drop", "y": y, "size": 96, "scrim": 0.5, "font": "cg-italic"}


R = [  # key, file, start, text, y, pages
    ("X01_opera-night", "01_botanic_butique_DPL4oHGjG5n", 0.0, "opera night\ndress code.", 0.24, QZ),
    ("X02_alone-in-the-museum", "02_roberto_celestri_CxNp_Ibssy_", 0.0, "alone\nin the museum.", 0.24, QIX),
    ("X03_first-person-fit-check", "03_luziwei99_DOkuQVDCTd4", 0.0, "first-person\nfit check.", 0.26, QZ),
    ("X04_royal-box", "04_roberto_celestri_DYR7ICqNmLe", 0.0, "royal box\ndress code.", 0.62, ZH),
    ("X05_what-to-wear-museum", "05_roberto_celestri_CsQ7nUrtuyf", 0.0, "what to wear\nto the museum.", 0.62, QZW),
    ("X06_after-closing", "06_antoinebn_C5i3phBInjQ", 0.0, "after closing.", 0.70, ZHW),
    ("X07_opera-ball", "07_vienna_DGh4qUch1cw", 0.0, "opera ball\ndress code.", 0.22, BW),
    ("X08_dressed-for-the-archive", "08_coffeeacademia_CrdjhveADRG", 4.3, "dressed\nfor the archive.", 0.42, ZHB),
]
S = {}
for i, (k, f, t, text, y, (pg, fin)) in enumerate(R):
    tag = f"x{i + 1:02d}"
    S[k] = dict(seed=10400 + i, segments=[clip("x", t, src=X + f + ".mp4", until="drop")] + pages(pg, None, tag, 2) +
                [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)], texts=[tx(text, y)])
for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"x1027_{k}.json"), "w"), indent=1)
print("\n".join(S))
