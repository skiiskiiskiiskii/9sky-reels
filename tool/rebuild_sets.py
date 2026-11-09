#!/usr/bin/env python3
"""Rebuild the two-garment set mockups (pairs) from updated single mockups, keeping the exact layout of the
old sets. For each old set we locate where each old single sits (multi-scale masked template match), then
place the new single at the same centre and scale, back layer first, front layer over it.

usage: rebuild_sets.py <jobs.json>
jobs: [{"old_set": path, "out": path, "layers": [[old_back, new_back], [old_front, new_front]]}, ...]
"""
import json, sys
import numpy as np
import cv2
from PIL import Image
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from editorial import _cut

W, H = 1080, 1920


def lum(img):
    return np.asarray(img.convert("RGB")).astype(np.float32).max(2)


def locate(scene_l, tpl_rgba, scene_mask=None, scales=np.arange(0.55, 1.02, 0.01)):
    """best (score, scale, cx, cy) of the template in the scene"""
    best = (-1, 0, 0, 0)
    t_l = lum(tpl_rgba.convert("RGB"))
    t_a = np.asarray(tpl_rgba)[..., 3].astype(np.float32) / 255
    for s in scales:
        w, h = int(tpl_rgba.width * s), int(tpl_rgba.height * s)
        if w >= W or h >= H or w < 50:
            continue
        tl = cv2.resize(t_l, (w, h), interpolation=cv2.INTER_AREA)
        ta = cv2.resize(t_a, (w, h), interpolation=cv2.INTER_AREA)
        m = (ta > 0.5).astype(np.float32)
        sc = scene_l if scene_mask is None else scene_l * scene_mask
        r = cv2.matchTemplate(sc, tl, cv2.TM_CCORR_NORMED, mask=m)
        r[~np.isfinite(r)] = -1
        _, v, _, loc = cv2.minMaxLoc(r)
        if v > best[0]:
            best = (v, s, loc[0] + w / 2, loc[1] + h / 2)
    return best


def build(job):
    scene = Image.open(job["old_set"]).convert("RGB")
    sl = lum(scene)
    (ob, nb), (of, nf) = job["layers"]
    ofc, obc = _cut(of), _cut(ob)
    vf, sf, fx, fy = locate(sl, ofc)
    # back layer: mask out where the front garment sits
    fmask = Image.new("L", (W, H), 0)
    fr = ofc.resize((int(ofc.width * sf), int(ofc.height * sf)), Image.LANCZOS)
    fmask.paste(fr.split()[-1], (int(fx - fr.width / 2), int(fy - fr.height / 2)))
    fa = np.asarray(fmask).astype(np.float32) / 255
    # both garments in these sets share one scale; search only the position of the back one
    vb, sb, bx, by = locate(sl, obc, scene_mask=(fa < 0.3).astype(np.float32), scales=[sf])
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    for new, s, cx, cy in [(nb, sb, bx, by), (nf, sf, fx, fy)]:
        g = _cut(new)
        g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.paste(g, (int(cx - g.width / 2), int(cy - g.height / 2)), g)
        canvas = Image.alpha_composite(canvas, layer)
    canvas.convert("RGB").save(job["out"])
    return dict(out=job["out"], front=(round(vf, 3), round(sf, 2)), back=(round(vb, 3), round(sb, 2)))


if __name__ == "__main__":
    for j in json.load(open(sys.argv[1])):
        print(build(j))
