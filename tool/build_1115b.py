#!/usr/bin/env python3
"""2026-11-15, batch 1115b: 2 reels, quarter zip only (Kirill: "сделай 2 новых рилса, используй куартеры").
No hooks named, so one louboutin-led and one rose-led. Hooks themselves untouched, only new mixes and new lines.

Q01 you don't wear red. you place it. - COUPLE mirrored, red sole held ~0.4 s (the C01 freeze, 70% past 3 s);
    white quarter zip page + black back, black+white pair finale
Q02 first the rose. then the shoes.   - the big rose g1 -> the whole MARBLE clip (red soles kick right at the cut);
    black quarter zip
Same F05 timing (mrpopular), post with the F05 audio."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, COLLAR, ARA, ROME, SP, P, O
from vitrine import vpage, vstacked
from build_1115 import lb, clip, t, ROSE, MARBLE_LEN, DROP, MP, NUMS


def freeze(key, hold_src, total=DROP, hold=0.4, speed=1.12, **kw):
    """play to the red sole, then hold that frame (very slow creep) for `hold` s up to the drop (as in build_1109cd)"""
    first = total - hold
    return [lb(key, start=hold_src - first * speed, dur=first, speed=speed, **kw),
            lb(key, start=hold_src, speed=0.03, **kw)]


Q = [  # key, tone, hook, texts, pages, finale, idea
    ("Q01_you-place-red", "vitrine",
     freeze("COUPLE", 4.95, crop_y=0.74, crop_x=0.45, flip=True),
     t("you don't wear red.\nyou place it."),
     [("WF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("PF", "PB"),
     "COUPLE mirrored, her red sole held 0.4 s before the cut (C01 mechanic); white front, black back, pair finale"),
    ("Q02_first-the-rose", "oxblood",
     [clip(ROSE + "g1.mp4", start=0.3, dur=round(DROP - MARBLE_LEN, 3), zoom=1.3, crop_y=0.12, grade={}),
      clip(P["MARBLE"], start=0.0, until="drop")],
     t("first the rose.\nthen the shoes.", y=0.70),
     [("KF", cat(1, COLLAR)), ("KB", cat(2, ARA, ROME))], ("KF", "KB"),
     "big rose g1 -> full MARBLE (red soles kick at the cut); the line names the order on screen, the collar is the third red - black quarter zip (v2: Kirill found the line 'roses fade, red soles do not' illogical)"),
]


def build(batch, rows, out_prefix, seed0):
    ledger = []
    for i, (k, tone, hook, texts, pg, fin, idea) in enumerate(rows):
        tag = f"q{i + 1:02d}y"
        pages = [img(vpage(P[pk], O + f"{tag}{j}.jpg", "N° " + NUMS[j], sub, tone), 1) for j, (pk, sub) in enumerate(pg)]
        fimg = vstacked(P[fin[0]], P[fin[1]], O + f"{tag}c.jpg", "N° " + NUMS[len(pg)], tone=tone)
        spec = dict(seed=seed0 + i, track=MP, segments=hook + pages + [img(fimg, 4)], texts=texts)
        json.dump(spec, open(os.path.join(SP, f"{out_prefix}_{k}.json"), "w"), indent=1, ensure_ascii=False)
        ledger.append([batch, k, MP, tone, texts[0]["text"].replace("\n", " "), idea])
        print(f"{out_prefix}_{k}")
    json.dump(ledger, open(os.path.join(SP, f"ledger_{batch}.json"), "w"), indent=1)


if __name__ == "__main__":
    build("1115b", Q, "q1115", 32000)
