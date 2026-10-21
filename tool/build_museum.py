#!/usr/bin/env python3
"""Build stills + compose specs for the museum-format test reels (M1..M8)."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from museum import exhibit, wall, pick_palette, palette_freeze, palette_card
from PIL import Image

SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "specs")
P = json.load(open(os.path.join(SP, "_paths.json")))["paths"]
L = "/mnt/user-data/outputs/hooks-locations/"
ST = "/mnt/user-data/outputs/museum-stills/"
os.makedirs(ST, exist_ok=True)
DROP = 3.13

def lab(item, detail):
    return [("9sky", "title"), ("(Prague, Czech Republic, 2026)", "sub"), (item, "italic"),
            (detail, "body"), ("Drop II. Private collection.", "body")]
QZ = "Cotton fleece, red ribbed collar."
ZH = "Cotton fleece, red-lined hood."

def frames(hook, start):
    out = []
    for i, t in enumerate([start + 0.2, start + 1.2, start + 2.2, start + DROP - 0.03]):
        p = f"{ST}_{hook}_{i}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", L + hook + ".mp4", "-frames:v", "1", p], check=True)
        out.append(Image.open(p))
    return out

def hook(name, start, b=-0.03):
    return dict(type="clip", src=L + name + ".mp4", start=start, until="drop", align_red=False, speed=1.0,
                zoom=1.0, flip=False, crop_x=0.5, grade=dict(c=1.04, s=1.0, b=b))

def img(path, beats):
    return dict(type="image", src=path, fit="full", beats=beats)

def T(text, f, t, y=0.47, size=86, scrim=0.0):
    d = {"text": text, "from": f, "to": t, "y": y, "size": size}
    if scrim: d["scrim"] = scrim
    return d

def hook_text(text, y=0.47):
    return T(text, 0, "drop", y, 90, 0.5)

specs = {}
# ---------------- EXHIBIT
e = lambda k, item, det, n: exhibit(P[k], f"{ST}{n}.jpg", lab(item, det))
specs["M1_exhibit_museums-dress-code"] = dict(seed=1001, segments=[hook("11_museum-flash-cuts", 0.0),
    img(e("KF", "IX quarter zip, black", QZ, "ex_kf"), 2), img(e("WF", "IX quarter zip, white", QZ, "ex_wf"), 2),
    img(e("PF", "IX quarter zip, black and white", QZ, "ex_pf"), 4)],
    texts=[hook_text("if museums had a dress code."), T("which one goes in the collection?", "b:4", "end", 0.062, 56)])
specs["M2_exhibit_collar-says-it-all"] = dict(seed=1002, segments=[hook("15_dark-baroque-gold", 0.3),
    img(e("KF", "IX quarter zip, black", QZ, "ex_kf"), 2), img(e("KB", "IX quarter zip, black (back)", "Ornament after the Ara Pacis, Rome.", "ex_kb"), 2),
    img(e("PF", "IX quarter zip, black and white", QZ, "ex_pf"), 4)],
    texts=[hook_text("the collar says it all.")])
specs["M3_exhibit_museum-piece-zip"] = dict(seed=1003, segments=[hook("17_dome-ceiling", 0.2),
    img(e("ZF", "IX zip hoodie, black", ZH, "ex_zf"), 2), img(e("XWF", "IX zip hoodie, white", ZH, "ex_xwf"), 2),
    img(e("ZPF", "IX zip hoodie, black and white", ZH, "ex_zpf"), 4)],
    texts=[hook_text("museum piece."), T("black or white?", "b:4", "end", 0.062, 64)])

# ---------------- PALETTE
def pal(name, hookname, start, cards, hook_txt, end_txt, seed, hy=0.47):
    fr = frames(hookname, start)
    cols = pick_palette(fr)
    segs = [hook(hookname, start), img(palette_freeze(fr[-1], f"{ST}{name}_freeze.jpg", cols), 2)]
    for i, (k, beats) in enumerate(cards):
        segs.append(img(palette_card(P[k], f"{ST}{name}_{k}.jpg", cols), beats))
    texts = [hook_text(hook_txt, hy), T("same palette.", "drop", "b:2", 0.40, 80)]
    if end_txt: texts.append(T(end_txt, "b:4", "end", 0.10, 72))
    specs[name] = dict(seed=seed, segments=segs, texts=texts)
pal("M4_palette_room-matched-the-collar", "01_red-room-chandelier", 0.35, [("KF", 2), ("PF", 4)],
    "the room matched the collar.", "which one?", 1004, hy=0.60)
pal("M5_palette_white-outside-red-inside", "08_white-dress-red-room", 0.2, [("XWF", 2), ("ZPF", 4)],
    "white outside. red inside.", "black or white?", 1005, hy=0.45)
pal("M6_palette_colors-that-match", "06_red-gown", 0.2, [("KF", 2), ("PF", 4)],
    "colors that match perfectly.", "one only. which?", 1006, hy=0.36)

# ---------------- WALL
w = lambda ks, n, pl: wall([P[k] for k in ks], f"{ST}{n}.jpg", pl)
specs["M7_wall_dress-code"] = dict(seed=1007, segments=[hook("03_red-velvet-salon", 0.3),
    img(w(["KF"], "wall_kf", ("9sky", "IX quarter zip, black")), 2), img(w(["KB"], "wall_kb", ("9sky", "the back. after the Ara Pacis")), 2),
    img(w(["KF", "WF"], "wall_pair", ("9sky", "IX quarter zip, black & white")), 4)],
    texts=[hook_text("dress code:\nblack. one red detail.", 0.62), T("which one would you hang?", "b:4", "end", 0.14, 70)])
specs["M8_wall_black-or-white"] = dict(seed=1008, segments=[hook("18_red-beat-montage", 0.0, b=-0.05),
    img(w(["KF"], "wall_kf", ("9sky", "IX quarter zip, black")), 2), img(w(["WF"], "wall_wf", ("9sky", "IX quarter zip, white")), 2),
    img(w(["KF", "WF"], "wall_pair", ("9sky", "IX quarter zip, black & white")), 4)],
    texts=[hook_text("black or white?", 0.45), T("black.", "drop", "b:2", 0.14, 86), T("white.", "b:2", "b:4", 0.14, 86),
           T("one only. which?", "b:4", "end", 0.14, 80)])

for k, v in specs.items():
    json.dump(v, open(os.path.join(SP, f"mus_{k}.json"), "w"), indent=1)
print("\n".join(specs))
