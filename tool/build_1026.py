#!/usr/bin/env python3
"""2026-10-26: 10 calm reels. Moving red-room / chandelier hooks (fresh cuts from the sources), italic hook text,
pages single -> black+white pair, stacked pair finale. AURA grid."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import clip, img, pages, fin_path, ht, cat, COLLAR, ARA, ROME, HOOD, FLEECE, IX, SP

H = "/mnt/user-data/uploads/hooks ids/"
S5, S6 = H + "snaptik_7615821256385924366_hd.mp4", H + "snaptik_7629052842933849364_hd.mp4"
L30 = "/mnt/user-data/outputs/hooks-locations/30_red-altar-chandelier.mp4"
src = lambda p, t, **k: clip("x", t, src=p, until="drop", **k)

S = {}
def reel(key, seed, hook, text, y, items, fin, tag):
    S[key] = dict(seed=seed, segments=[hook] + pages(items, None, tag, 2) + [img(fin_path(fin[0], fin[1], tag, "N° III"), 4)],
                  texts=[ht(text, y)])

reel("C01_collar-says-it-all", 9701, src(S6, 3.8), "the collar says it all.", 0.60,
     [("KF", cat(1, COLLAR)), ("PF", cat(2, "THE SAME RED COLLAR"))], ("PF", "PB"), "c01")
reel("C02_dress-code", 9702, src(S6, 24.0), "if museums had\na dress code.", 0.36,
     [("WF", cat(1, COLLAR)), ("PF", cat(2, "BLACK  ·  WHITE  ·  ONE RED"))], ("PF", "PB"), "c02")
reel("C03_do-not-touch", 9703, src(S5, 29.7), "do not touch\nthe exhibits.", 0.62,
     [("KB", cat(1, ARA, ROME)), ("PB", cat(2, ARA, ROME))], ("PF", "PB"), "c03")
reel("C04_only-colour", 9704, src(L30, 0.2), "red is the only\ncolour we kept.", 0.58,
     [("ZF", cat(1, HOOD)), ("ZPF", cat(2, HOOD))], ("ZPF", "ZPB"), "c04")
reel("C05_black-or-white", 9705, src(S5, 9.2), "black or white?", 0.62,
     [("WF", cat(1, COLLAR)), ("KF", cat(2, COLLAR))], ("PF", "PB"), "c05")
reel("C06_not-loud", 9706, src(S6, 9.6), "not loud. just red.", 0.40,
     [("KF", cat(1, COLLAR)), ("ZPF", cat(2, HOOD))], ("PF", "PB"), "c06")
reel("C07_come-closer", 9707, src(S5, 49.4), "you have to\ncome closer.", 0.62,
     [("KF", cat(1, IX)), ("PF", cat(2, COLLAR))], ("PF", "PB"), "c07")
reel("C08_only-wears-black", 9708, src(S5, 5.3), "for the one who\nonly wears black.", 0.58,
     [("KF", cat(1, COLLAR)), ("ZF", cat(2, HOOD))], ("KKF", "KKB"), "c08")
reel("C09_quiet-until", 9709, src(S5, 17.3), "quiet until it isn't.", 0.60,
     [("ZF", cat(1, HOOD)), ("ZPB", cat(2, ARA, ROME))], ("ZPF", "ZPB"), "c09")
reel("C10_his-and-hers", 9710, src(S5, 41.2), "his & hers.", 0.62,
     [("KF", cat(1, "HIS")), ("WF", cat(2, "HERS"))], ("PF", "PB"), "c10")

for k, v in S.items():
    json.dump(v, open(os.path.join(SP, f"c1026_{k}.json"), "w"), indent=1)
print("\n".join(S))
