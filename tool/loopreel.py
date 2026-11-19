#!/usr/bin/env python3
"""Seamless-loop reels (Kirill 11-17: the loop stays on every reel from now on).

A reel = hook (one or more clip segments, 3.13 s, the line on top) + items after the cut, each lasting whole beats
at 99 BPM (images or clips), + a 15-frame bridge. The bridge dissolves the last frame into the 15 frames that
come right BEFORE the reel's first frame, so a replay continues the motion. With whole beats after the cut the
total is always a whole number of beats (8 = 4.85 s, 12 = 7.27 s, 18 = 10.9 s), so the F05 audio wraps on the grid.

hook: list of clip dicts; every one but the last has "n" (frames); the last fills up to the cut. The first one
must have footage before its start (explicit "start" >= 0.5 s * speed, or align_red far enough into the clip).
after: list of (beats, segment) - segment is an image dict (compose's) or a clip dict (start / align_red + lead)."""
import json, os, random, subprocess
import numpy as np
import compose as C

FPS, W, H = C.FPS, C.W, C.H
BEAT = 60 / 99.0
DROP = 3.13
HOOK_N = round(DROP * FPS)                  # 94
BRIDGE = 15


def _frames_of(seg, n, rnd):
    if seg["type"] == "clip":
        return C.clip_frames(seg, n, rnd, DROP)
    canvas = C.image_canvas(seg)
    return (canvas for _ in range(n))


def make(out, hook, line, after, y=0.22, seed=0, beat=BEAT, drop=DROP, total_beats=None, audio=None):
    """beat / drop: the track's beat length and the cut time (default F05 / mr popular: 99 BPM, 3.13 s).
    total_beats: whole beats of the loop counted from frame 0 (default: hook + after + bridge on the F05 grid)."""
    rnd = random.Random(seed)
    # frame plan
    cut = [HOOK_N]
    b = 0
    for beats, _ in after:
        b += beats
        cut.append(round((drop + b * beat) * FPS))
    if total_beats is None:
        total_beats = b + 6                 # 3.13 s + bridge = 6 beats on the F05 grid
    total = round(total_beats * beat * FPS)
    bridge = total - cut[-1]
    assert 12 <= bridge <= 30, bridge
    # hook frames: the first segment starts `bridge` frames earlier (the pre-roll)
    ns = [s["n"] for s in hook[:-1]]
    ns.append(HOOK_N - sum(ns))
    ns[0] += bridge
    rgb, a = C.text_layer(line, y, 96, scrim=0.5, face="cg-italic")
    C._FONT_PATH[0] = C.FONT
    hook_total = HOOK_N + bridge
    enc = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-"]
    if audio:                                # (path, offset): bake the track in, its drop on the cut
        dur = total / FPS
        enc += ["-ss", f"{audio[1]:.3f}", "-t", f"{dur + 0.1:.3f}", "-i", audio[0],
                "-af", f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.04:.3f}:d=0.04", "-b:a", "192k"]
    else:
        enc += ["-f", "lavfi", "-t", f"{total / FPS + 0.1:.3f}", "-i", "anullsrc=r=44100:cl=stereo", "-b:a", "128k"]
    enc += ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(enc, stdin=subprocess.PIPE)
    put = lambda f: p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    pre, fi, written = [], 0, 0
    for k, (seg, n) in enumerate(zip(hook, ns)):
        seg = {kk: v for kk, v in seg.items() if kk != "n"}
        if k == 0 and "start" in seg:       # explicit start: move it back by the pre-roll
            seg["start"] = seg["start"] - bridge / FPS * seg.get("speed", 1.0)
            assert seg["start"] >= 0, "no footage before the hook start for the pre-roll"
        frames = C.clip_frames(seg, n, rnd, DROP)
        if seg.get("reverse") and k > 0:     # a shot played backwards (not the first one: it carries the pre-roll)
            frames = [f.copy() for f in frames][::-1]
        for fr in frames:
            f = fr.astype(np.float32)
            kk = min(1.0, (hook_total - fi) / 4)          # the line fades out over the last 4 frames before the cut
            f = f * (1 - a * kk) + rgb * (a * kk)
            if fi < bridge:
                pre.append(f.copy())
            else:
                put(f); written += 1
            fi += 1
    last = None
    for (beats, seg), c0, c1 in zip(after, cut[:-1], cut[1:]):
        for fr in _frames_of(seg, c1 - c0, rnd):
            last = fr.astype(np.float32)
            put(last); written += 1
    for j in range(bridge):
        x = (j + 1) / bridge
        w = x * x * (3 - 2 * x)
        put(last * (1 - w) + pre[j] * w); written += 1
    p.stdin.close(); p.wait()
    return {"frames": written, "seconds": round(written / FPS, 3), "beats": total_beats, "cuts": cut}
