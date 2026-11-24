#!/usr/bin/env python3
"""Colour-moodboard reels ("my color." / "if i was a color" format, 2026-11-22).

A fast slideshow of one-colour images and short clips, cut on a fixed list of times, with one small lowercase
serif line in the middle for the whole reel. Stills get a slow push-in so nothing is fully static.

spec = {
  "cuts": [t1, t2, ...],          # cut times in s; the last value is the end of the loop
  "repeat": 1,                    # play the whole cut list this many times (the 2x loop of "if i was a color")
  "shots": [ {"img": path, "focus": [x, y], "z0": 1.0, "z1": 1.06}
           | {"clip": path, "start": s, "speed": 1.0, "zoom": 1.0, "crop_x": .5, "crop_y": .5, "flip": false} ],
             # any shot may add "keep_red": true (grey world, only the red keeps its colour) or "gray": true
  "look": {"keep_red": false, "gray": false, "c": 1.0, "s": 1.0, "b": 0.0, "grain": 0, "vignette": 0.0},
  "band": null | [y0, y1],        # letterbox: picture only between these y fractions, black above and below
  "text": "my color.", "text_y": 0.48, "text_size": 54, "font": "cg-400",
  "text_to": 3.13,                # optional: the line fades out here (the drop) instead of staying the whole reel
}
Audio is left silent: Kirill puts the sound on in Instagram (Use audio)."""
import json, os, random, subprocess, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as C

W, H, FPS = C.W, C.H, C.FPS
C.FONTS["cg-400"] = os.path.join(C.HERE, "fonts", "cormorant-garamond-latin-400-normal.woff")
_cache = {}


def _cover(path, w, h, over=1.25):
    """the still scaled to cover w x h with room for the push-in"""
    key = (path, w, h)
    if key not in _cache:
        im = Image.open(path).convert("RGB")
        s = max(w / im.width, h / im.height) * over
        _cache[key] = im.resize((max(w, int(im.width * s)), max(h, int(im.height * s))), Image.LANCZOS)
    return _cache[key]


def still_frames(sh, n, w, h):
    im = _cover(sh["img"], w, h, over=max(1.0, sh.get("z1", 1.06), sh.get("z0", 1.0)) * 1.02)
    fx, fy = sh.get("focus", [0.5, 0.5])
    z0, z1 = sh.get("z0", 1.0), sh.get("z1", 1.06)
    base = max(w / im.width, h / im.height)               # scale at which the image just covers the frame
    for i in range(n):
        k = i / max(1, n - 1)
        z = z0 + (z1 - z0) * (k * k * (3 - 2 * k))         # smoothstep push-in
        cw, ch = w / (base * z), h / (base * z)
        x0 = min(max(0, fx * im.width - cw / 2), im.width - cw)
        y0 = min(max(0, fy * im.height - ch / 2), im.height - ch)
        yield np.asarray(im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)))


def clip_frames(sh, n, w, h):
    seg = dict(src=sh["clip"], start=sh.get("start", 0.0), speed=sh.get("speed", 1.0), zoom=sh.get("zoom", 1.0),
               crop_x=sh.get("crop_x", 0.5), crop_y=sh.get("crop_y", 0.5), flip=sh.get("flip", False),
               grade=sh.get("grade", {}), smooth=sh.get("smooth", False), align_red=False)
    for fr in C.clip_frames(seg, n, random.Random(0), 0):
        if (w, h) != (W, H):                              # band: take the middle of the full frame
            y0 = int((H - h) * sh.get("band_y", 0.5))
            fr = fr[y0:y0 + h, :w]
        yield fr


def look(f, L, sh):
    f = f.astype(np.float32)
    if sh.get("gamma"):                                    # lift the darks (black garment on black)
        f = 255.0 * (f / 255.0) ** sh["gamma"]
    if sh.get("keep_red", L.get("keep_red")):
        f = C.keep_red(f.clip(0, 255).astype(np.uint8)).astype(np.float32)
    elif sh.get("gray", L.get("gray")):
        g = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
        f = np.repeat(g[..., None], 3, 2)
    s = L.get("s", 1.0)
    if s != 1.0:
        g = (0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2])[..., None]
        f = g + (f - g) * s
    c, b = L.get("c", 1.0) * sh.get("c", 1.0), L.get("b", 0.0) + sh.get("b", 0.0)
    f = (f - 128) * c + 128 + b * 255
    return f


def render(spec, out):
    cuts, rep = spec["cuts"], spec.get("repeat", 1)
    shots, L = spec["shots"], spec.get("look", {})
    assert len(shots) == len(cuts), (len(shots), len(cuts))
    band = spec.get("band")
    bw, bh = (W, H) if not band else (W, int(round((band[1] - band[0]) * H / 2)) * 2)
    by = 0 if not band else int(band[0] * H)
    loop_t = cuts[-1]
    bounds, t0 = [], 0.0
    for r in range(rep):
        prev = 0.0
        for i, c in enumerate(cuts):
            bounds.append((i, round((r * loop_t + prev) * FPS), round((r * loop_t + c) * FPS)))
            prev = c
    total = bounds[-1][2]
    rgb, a = C.text_layer(spec["text"], spec.get("text_y", 0.48), spec.get("text_size", 54),
                          face=spec.get("font", "cg-400"))
    if spec.get("text_shadow", 1.0) < 1.0:
        pass
    grain = float(L.get("grain", 0))
    grng = np.random.default_rng(spec.get("seed", 0))
    vig = float(L.get("vignette", 0))
    if vig:
        yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32)
        r2 = ((xx / bw - 0.5) / 0.62) ** 2 + ((yy / bh - 0.5) / 0.62) ** 2
        vmask = (1 - vig * np.clip(r2, 0, 1.6) / 1.6)[..., None]
    enc = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-f", "lavfi", "-t", f"{total / FPS:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(enc, stdin=subprocess.PIPE)
    rendered = {}
    t_to = round(spec["text_to"] * FPS) if spec.get("text_to") else 10 ** 9   # line only up to here (the drop)
    fi = 0
    for i, f0, f1 in bounds:
        n = f1 - f0
        sh = shots[i]
        if rep > 1 and i in rendered and len(rendered[i]) == n:
            frames = rendered[i]
        else:
            gen = still_frames(sh, n, bw, bh) if "img" in sh else clip_frames(sh, n, bw, bh)
            vm = vmask if (vig and sh.get("vig", True)) else 1.0
            frames = [np.clip(look(fr, L, sh) * vm, 0, 255).astype(np.uint8) for fr in gen]
            _cache.clear()
            if rep > 1:                                    # kept only for the second pass of a looped reel
                rendered[i] = frames
        for fr in frames:
            fr = fr.astype(np.float32)
            if band:
                full = np.zeros((H, W, 3), np.float32)
                full[by:by + bh] = fr
            else:
                full = fr.copy()
            if grain:
                g = grng.normal(0, grain, (H // 2, W // 2, 1)).astype(np.float32)
                full += np.repeat(np.repeat(g, 2, 0), 2, 1)
                if band:
                    full[:by] = 0
                    full[by + bh:] = 0
            if fi < t_to:
                k = min(1.0, (t_to - fi) / 4.0)                     # 4-frame fade out at the drop
                full = full * (1 - a * k) + rgb * (a * k)
            fi += 1
            p.stdin.write(np.clip(full, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    return {"frames": total, "seconds": round(total / FPS, 2)}


if __name__ == "__main__":
    print(json.dumps(render(json.load(open(sys.argv[1])), sys.argv[2])))
