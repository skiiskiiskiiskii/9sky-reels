#!/usr/bin/env python3
"""9sky multi-segment reel composer.

A reel is a JSON spec: a timeline of segments on the track's beat grid plus
timed text cards. The first segment(s) run until the drop; everything after
is measured in beats so cuts land on the music.

segment types
  clip   {"type":"clip","src":..., "until":"drop" | "dur": s, "align_red":true}
  image  {"type":"image","src":..., "beats":n, "crop":[x0,y0,x1,y1]?, "fit":"full|panel|cover"}
  split  {"type":"split","srcs":[a,b], "labels":["I","II"]?, "beats":n}
texts
  {"text":..., "from":s|"drop", "to":s|"drop"|"end", "y":0.45, "size":86}
  times may also be given as "b:<beats after drop>"

usage: compose.py spec.json out.mp4 [--preview-audio track.wav]
"""
import json, os, subprocess, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "noto-serif-display-latin-300-italic.woff")
W, H, FPS = 1080, 1920, 30
TRACKS = {"aura": {"drop": 3.13, "bpm": 123.05}}


# ---------- helpers ----------
def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def red_onset(path):
    w, h = 90, 160
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps=10,scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(int)
    r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
    red = ((r > 110) & (r > g * 1.8) & (r > b * 1.6)).mean(axis=(1, 2)) * 100
    thr = max(1.0, red.max() * 0.3)
    for i in range(10, len(red) - 1):
        if red[i] >= thr and red[i + 1] >= thr:
            return i / 10
    return None


def content_bbox(img, thr=14):
    a = np.asarray(img.convert("L"))
    ys = np.where((a > thr).sum(1) > 4)[0]
    xs = np.where((a > thr).sum(0) > 4)[0]
    return xs[0], ys[0], xs[-1] + 1, ys[-1] + 1


def font(size):
    return ImageFont.truetype(FONT, size)


def wrap(d, text, size, max_w):
    for s in range(size, 69, -2):
        f = font(s)
        if d.textlength(text, font=f) <= max_w:
            return [text], f
    f = font(size)
    words, best = text.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        la, lb = d.textlength(a, font=f), d.textlength(b, font=f)
        cost = abs(la - lb) - (220 if a.endswith((",", ".", "?")) else 0)
        if max(la, lb) <= max_w and (best is None or cost < best[0]):
            best = (cost, [a, b])
    return (best[1] if best else [text]), f


def text_layer(text, y_center=0.45, size=86, max_w=980):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines, f = wrap(d, text, size, max_w)
    lh = int(f.size * 1.2)
    y0 = int(H * y_center - lh * len(lines) / 2)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, ln in enumerate(lines):
        sd.text((W / 2, y0 + i * lh + lh / 2), ln, font=f, fill=(0, 0, 0, 160), anchor="mm")
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(7)))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        d.text((W / 2, y0 + i * lh + lh / 2), ln, font=f, fill=(255, 255, 255, 245), anchor="mm")
    a = np.asarray(img).astype(np.float32)
    return a[..., :3], a[..., 3:4] / 255.0


# ---------- segment renderers (yield HxWx3 uint8 frames) ----------
def clip_frames(seg, n, rnd, drop):
    src = seg["src"]
    dur = n / FPS
    total = probe_duration(src)
    start = seg.get("start")
    if start is None:
        onset = red_onset(src) if seg.get("align_red", True) else None
        end = min(total, (onset + 0.7) if onset is not None else dur)
        start = max(0.0, end - dur)
    speed = min(1.0, (total - start) / dur) if total - start < dur else 1.0
    flip = seg.get("flip", rnd.random() < 0.5)
    zoom = seg.get("zoom", rnd.uniform(1.0, 1.06))
    zw, zh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    vf = (f"setpts=PTS/{speed:.4f},fps={FPS},scale={zw}:{zh}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}{',hflip' if flip else ''},setsar=1")
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", src, "-vf", vf,
                          "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            yield last
            continue
        last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        yield last
    p.stdout.close(); p.wait()


def image_canvas(seg):
    im = Image.open(seg["src"]).convert("RGB")
    fit = seg.get("fit", "full")
    if seg.get("crop"):
        im = im.crop(tuple(seg["crop"]))
    if fit == "full":
        return np.asarray(im.resize((W, H), Image.LANCZOS))
    if fit == "cover":
        s = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * s + 1), int(im.height * s + 1)), Image.LANCZOS)
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))
    # panel: artwork centered on black, like a framed piece
    target_h = seg.get("panel_h", 1360)
    s = min(target_h / im.height, (W - 120) / im.width)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    c = Image.new("RGB", (W, H), "black")
    c.paste(im, ((W - im.width) // 2, int(H * seg.get("panel_y", 0.53) - im.height / 2)))
    return np.asarray(c)


def diptych_canvas(seg):
    """Two collage panels side by side at ~1.6x - sharper than one panel blown up."""
    c = Image.new("RGB", (W, H), "black")
    gap, margin = 24, 18
    cell_w = (W - 2 * margin - gap) // 2
    ims = []
    for src, crop in seg["panels"]:
        im = Image.open(src).convert("RGB").crop(tuple(crop))
        s = cell_w / im.width
        im = im.resize((cell_w, int(im.height * s)), Image.LANCZOS)
        ims.append(im.filter(ImageFilter.UnsharpMask(radius=1.5, percent=50, threshold=2)))
    h = max(i.height for i in ims)
    y = int(H * seg.get("panel_y", 0.53) - h / 2)
    for k, im in enumerate(ims):
        c.paste(im, (margin + k * (cell_w + gap), y + (h - im.height) // 2))
    return np.asarray(c)


def split_canvas(seg):
    c = Image.new("RGB", (W, H), "black")
    half = W // 2
    labels = seg.get("labels") or [None, None]
    tops = []
    for i, src in enumerate(seg["srcs"]):
        im = Image.open(src).convert("RGB")
        im = im.crop(content_bbox(im))
        s = min((half - 40) / im.width, 820 / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        x = i * half + (half - im.width) // 2
        y = int(H * 0.43 - im.height / 2)
        c.paste(im, (x, y))
        tops.append((x + im.width // 2, y + im.height))
    d = ImageDraw.Draw(c)
    base = max(b for _, b in tops) + 90          # one shared baseline for both labels
    for (cx, _), lab in zip(tops, labels):
        if lab:
            d.text((cx, base), lab, font=font(72), fill=(235, 235, 235), anchor="mm")
    return np.asarray(c)


# ---------- main ----------
def resolve_time(v, drop, beat, end):
    if isinstance(v, (int, float)):
        return float(v)
    if v == "drop":
        return drop
    if v == "end":
        return end
    if isinstance(v, str) and v.startswith("b:"):
        return drop + float(v[2:]) * beat
    raise ValueError(v)


def compose(spec, out, preview_audio=None):
    tr = TRACKS[spec.get("track", "aura")]
    drop, beat = tr["drop"], 60.0 / tr["bpm"]
    rnd = random.Random(spec.get("seed", 0))

    # segment boundaries on the frame grid
    bounds, t = [], 0.0
    beats_after = 0.0
    for seg in spec["segments"]:
        if seg.get("until") == "drop":
            t_end = drop
        elif "dur" in seg:
            t_end = t + seg["dur"]
        else:
            beats_after += seg["beats"]
            t_end = drop + beats_after * beat
        bounds.append((round(t * FPS), round(t_end * FPS)))
        t = t_end
    total_frames = bounds[-1][1]
    end_t = total_frames / FPS

    texts = []
    for tx in spec.get("texts", []):
        rgb, a = text_layer(tx["text"], tx.get("y", 0.45), tx.get("size", 86))
        f0 = round(resolve_time(tx.get("from", 0), drop, beat, end_t) * FPS)
        f1 = round(resolve_time(tx.get("to", "end"), drop, beat, end_t) * FPS)
        texts.append((f0, f1, rgb, a, tx.get("fade", 4)))

    enc = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if preview_audio:
        enc += ["-i", preview_audio, "-map", "0:v", "-map", "1:a", "-af", "apad", "-t", f"{end_t:.3f}"]
    else:
        enc += ["-f", "lavfi", "-t", f"{end_t:.3f}", "-i", "anullsrc=r=44100:cl=stereo",
                "-map", "0:v", "-map", "1:a"]
    enc += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(enc, stdin=subprocess.PIPE)

    loop_n = int(spec.get("loop_frames", 0))
    first = None
    fi = 0
    for seg, (b0, b1) in zip(spec["segments"], bounds):
        n = b1 - b0
        if seg["type"] == "clip":
            gen = clip_frames(seg, n, rnd, drop)
        else:
            canvas = {"image": image_canvas, "split": split_canvas,
                      "diptych": diptych_canvas}[seg["type"]](seg)
            if seg.get("dim"):                     # darken bright stills so white text stays legible
                canvas = (canvas.astype(np.float32) * seg["dim"]).astype(np.uint8)
            gen = (canvas for _ in range(n))
        for fr in gen:
            f = fr.astype(np.float32)
            for f0, f1, rgb, a, fade in texts:
                if f0 <= fi < f1:
                    k = 1.0
                    if fade:
                        k = min(1.0, (fi - f0 + 1) / fade, (f1 - fi) / fade) if f0 > 0 else min(1.0, (f1 - fi) / fade)
                    f = f * (1 - a * k) + rgb * (a * k)
            if first is None:
                first = f.copy()
            if loop_n and fi >= total_frames - loop_n:
                k = (fi - (total_frames - loop_n) + 1) / loop_n
                f = f * (1 - k) + first * k
            p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
            fi += 1
    p.stdin.close(); p.wait()
    return {"frames": total_frames, "seconds": round(end_t, 2)}


if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    pa = sys.argv[sys.argv.index("--preview-audio") + 1] if "--preview-audio" in sys.argv else None
    print(json.dumps(compose(spec, sys.argv[2], pa)))
