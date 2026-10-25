#!/usr/bin/env python3
"""Sharp hooks: hard cuts on the beat grid, a punch-in + light flash on every cut, optional beat pulses.
Output: 3.13 s, 1080x1920, 30 fps, silent mp4 (used as a clip in compose specs).

shots: list of dicts {src, t (start s), d (duration s, last may be None = until DROP), speed}
"""
import subprocess, numpy as np
from PIL import Image

W, H, FPS, DROP = 1080, 1920, 30, 3.13
OW, OH = 1210, 2152            # decode oversize (~1.12x) so we can punch in without upscaling much
N = round(DROP * FPS)


def decode(src, t, n, speed=1.0):
    vf = (f"setpts=PTS/{speed:.4f},fps={FPS},scale={OW}:{OH}:force_original_aspect_ratio=increase,"
          f"crop={OW}:{OH}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-t", f"{(n + 4) / FPS * speed:.3f}",
                          "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    k = len(raw) // (OW * OH * 3)
    fr = np.frombuffer(raw, np.uint8)[:k * OW * OH * 3].reshape(k, OH, OW, 3)
    if k < n:  # hold last frame
        fr = np.concatenate([fr, np.repeat(fr[-1:], n - k, 0)])
    return fr[:n]


def view(fr, z):
    """z = 1.0 shows the whole oversize frame, 1.12 is a tight crop"""
    cw, ch = int(OW / z), int(OH / z)
    x, y = (OW - cw) // 2, (OH - ch) // 2
    im = Image.fromarray(fr[y:y + ch, x:x + cw]).resize((W, H), Image.BILINEAR)
    return np.asarray(im).astype(np.float32) / 255


def grade(a, c=1.07, s=1.08):
    g = a.mean(2, keepdims=True)
    a = g + (a - g) * s
    return (a - 0.5) * c + 0.5


def build(shots, out, punch=0.10, punch_frames=5, flash=0.22, pulses=(), pulse=0.07, base_zoom=1.02):
    # frame boundaries
    bounds, t = [], 0.0
    for i, s in enumerate(shots):
        end = DROP if s.get("d") is None else t + s["d"]
        bounds.append((round(t * FPS), min(N, round(end * FPS))))
        t = end
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    pulse_frames = [round(x * FPS) for x in pulses]
    for s, (f0, f1) in zip(shots, bounds):
        n = f1 - f0
        if n <= 0:
            continue
        frs = decode(s["src"], s["t"], n, s.get("speed", 1.0))
        for j in range(n):
            g = f0 + j
            z = base_zoom + s.get("drift", 0.0) * j / max(n, 1)
            if j < punch_frames and f0 > 0:
                e = 1 - (1 - j / punch_frames) ** 2
                z += punch * (1 - e)
            for pf in pulse_frames:
                if 0 <= g - pf < 6:
                    z += pulse * (1 - (g - pf) / 6)
            a = grade(view(frs[j], min(z, 1.12)))
            if f0 == 0:
                pass
            elif j == 0:
                a = a + flash * (1 - a)
            elif j == 1:
                a = a + flash * 0.4 * (1 - a)
            p.stdin.write((np.clip(a, 0, 1) * 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
