#!/usr/bin/env python3
"""9sky trial-reel renderer.

Layout (AURA template): hook clip with serif italic text until the drop,
hard cut on the drop, then mockups switching on the beat.

usage:
  render.py --hook HOOK.mp4 --text "only up close" --mockups front.png back.png set.png \
            --out out.mp4 [--preview-audio aura.wav] [--seed 3]
"""
import argparse, json, os, random, subprocess, tempfile
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "noto-serif-display-latin-300-italic.woff")
W, H, FPS = 1080, 1920, 30

# Track templates: drop = seconds from video start where the drop must land,
# bpm = tempo, pattern = how many beats each mockup stays on screen.
TRACKS = {
    "aura": {"drop": 3.13, "bpm": 123.05, "pattern": [2, 2, 4]},
}


def sh(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def red_onset(path):
    """First moment the red sole / red nails become clearly visible."""
    w, h = 90, 160
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps=10,scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(int)
    r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
    red = ((r > 110) & (r > g * 1.8) & (r > b * 1.6)).mean(axis=(1, 2)) * 100
    peak = red.max()
    thr = max(1.0, peak * 0.3)
    for i in range(10, len(red) - 1):           # ignore the first second
        if red[i] >= thr and red[i + 1] >= thr:
            return i / 10, red
    return None, red


def hook_window(path, drop, lead=0.7):
    """Pick [start, start+drop] so the red appears ~lead seconds before the drop."""
    dur = probe_duration(path)
    onset, _ = red_onset(path)
    if onset is None:
        end = min(dur, drop)
    else:
        end = min(dur, onset + lead)
    start = max(0.0, end - drop)
    speed = 1.0
    if dur < drop:                                # too short: slow it down to fit
        speed = dur / drop
        start = 0.0
    return start, speed, onset


def best_text_y(path, start, dur, candidates=(0.30, 0.38, 0.45, 0.55, 0.65)):
    """Pick the vertical position where the text sits on the darkest, calmest area."""
    w, h = 90, 160
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}",
                          "-i", path, "-vf", f"fps=6,scale={w}:{h}", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)
    best, best_score = 0.45, 1e9
    for c in candidates:
        y0, y1 = int((c - 0.05) * h), int((c + 0.05) * h)
        band = fr[:, y0:y1, 8:-8]
        score = band.mean() + 1.5 * band.std(axis=(1, 2)).mean()
        score += abs(c - 0.45) * 40            # prefer the usual centre position
        if score < best_score:
            best, best_score = c, score
    return best


def text_png(text, path, size=86, y_center=0.45, max_w=980):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 1) one line, shrinking down to 74px if needed
    lines = None
    for s in range(size, 73, -2):
        font = ImageFont.truetype(FONT, s)
        if d.textlength(text, font=font) <= max_w:
            lines, size = [text], s
            break
    # 2) otherwise two balanced lines, preferring a break after , or .
    if lines is None:
        font = ImageFont.truetype(FONT, size)
        words = text.split()
        best = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            la, lb = d.textlength(a, font=font), d.textlength(b, font=font)
            cost = abs(la - lb) - (200 if a.endswith((",", ".")) else 0)
            if max(la, lb) <= max_w and (best is None or cost < best[0]):
                best = (cost, [a, b])
        lines = best[1] if best else [text]
    lh = int(size * 1.18)
    y0 = int(H * y_center - lh * len(lines) / 2)
    # soft shadow for legibility on bright floors
    sh_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh_img)
    for i, ln in enumerate(lines):
        sd.text((W / 2, y0 + i * lh + lh / 2), ln, font=font, fill=(0, 0, 0, 150), anchor="mm")
    sh_img = sh_img.filter(ImageFilter.GaussianBlur(6))
    img = Image.alpha_composite(img, sh_img)
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        d.text((W / 2, y0 + i * lh + lh / 2), ln, font=font, fill=(255, 255, 255, 245), anchor="mm")
    img.save(path)


def render(hook, text, mockups, out, track="aura", preview_audio=None, seed=None):
    t = TRACKS[track]
    rnd = random.Random(seed)
    drop, beat = t["drop"], 60.0 / t["bpm"]
    durs = [n * beat for n in t["pattern"]][: len(mockups)]
    start, speed, onset = hook_window(hook, drop)

    # light variation so repeated hooks aren't byte-identical re-uploads
    flip = rnd.random() < 0.5
    zoom = rnd.uniform(1.0, 1.07)
    grade = rnd.uniform(-0.04, 0.0)

    tmp = tempfile.mkdtemp()
    tp = os.path.join(tmp, "text.png")
    ty = best_text_y(hook, start, drop / speed)
    text_png(text, tp, y_center=ty)

    inputs = ["-ss", f"{start:.3f}", "-t", f"{drop / speed:.3f}", "-i", hook, "-i", tp]
    for m, dur in zip(mockups, durs):
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{dur:.4f}", "-i", m]

    zw, zh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    f = []
    hookchain = (f"[0:v]setpts=PTS/{speed:.4f},fps={FPS},"
                 f"scale={zw}:{zh}:force_original_aspect_ratio=increase,crop={W}:{H},"
                 f"{'hflip,' if flip else ''}eq=brightness={grade:.3f},setsar=1,"
                 f"trim=duration={drop:.4f},setpts=PTS-STARTPTS[h0]")
    f.append(hookchain)
    f.append("[h0][1:v]overlay=0:0:format=auto[hook]")
    seg = ["[hook]"]
    for i, dur in enumerate(durs):
        n = int(round(dur * FPS))
        idx = i + 2
        # mockups stay static (no zoom), exactly as designed
        f.append(f"[{idx}:v]scale={W}:{H},setsar=1,fps={FPS},"
                 f"trim=duration={dur:.4f},setpts=PTS-STARTPTS[m{i}]")
        seg.append(f"[m{i}]")
    f.append("".join(seg) + f"concat=n={len(seg)}:v=1:a=0,format=yuv420p[v]")
    total = drop + sum(durs)

    cmd = ["ffmpeg", "-y", "-v", "error"] + inputs
    if preview_audio:
        cmd += ["-i", preview_audio]
        amap = ["-map", f"{len(mockups) + 2}:a", "-t", f"{total:.3f}"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]
        amap = ["-map", f"{len(mockups) + 2}:a"]
    cmd += ["-filter_complex", ";".join(f), "-map", "[v]"] + amap + [
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS),
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out]
    sh(cmd)
    meta = {"hook": os.path.basename(hook), "hook_start": round(start, 2), "speed": round(speed, 3),
            "red_onset": onset, "text": text, "mockups": [os.path.basename(m) for m in mockups],
            "track": track, "drop": drop, "duration": round(total, 2), "flip": flip,
            "zoom": round(zoom, 3), "text_y": ty}
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--mockups", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--track", default="aura")
    ap.add_argument("--preview-audio")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    print(json.dumps(render(a.hook, a.text, a.mockups, a.out, a.track, a.preview_audio, a.seed)))
