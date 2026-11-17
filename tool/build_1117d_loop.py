#!/usr/bin/env python3
"""made 2026-11-17, single test 1117d: W01 "look at her soles." - a reel that loops without a seam.

Kirill: try something newer, at least for Instagram's algorithms; one video at a time, not batches.
Data (Metricool, pulled 11-17): plateau reels match F05 per viewer (R03: 70.6% past 3 s, 6.27 s avg watch,
1.6% saves per reach; F05: 70%, 6.24 s, 1.5%), so the gate is IG expanding past the first ~1-1.5K people,
not how people react. People already replay (views / reach ~1.3-1.45 on every reel).

The loop: the last 15 frames (0.5 s) dissolve from the finale into the 15 frames that come right before the
reel's first frame, so a replay continues the motion instead of restarting it. Total 218 frames = 12 beats at
99 BPM, so the F05 audio also wraps on the beat grid. Hook = F05's (COUPLE, tight on the shoes), mirrored so
the frames are new; black quarter zip pages on slate; black finale (dark into dark street = a clean dissolve).
usage: build_1117d_loop.py <out.mp4>"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compose as C
from build_1024 import img, cat, COLLAR, ARA, ROME, P, O, SP
from vitrine import vpage, vstacked

FPS, W, H = C.FPS, C.W, C.H
MP = "mrpopular"
GR = dict(c=1.04, s=0.92, b=-0.012)
BRIDGE = 15                                   # frames of dissolve at the end = frames of pre-roll before frame 0
HOOK_N = 94                                   # 3.13 s cut on the frame grid
LINE = "look at\nher soles."
TONE = "slate"

hook = dict(type="clip", src=P["COUPLE"], speed=1.12, zoom=1.2, crop_x=0.4, crop_y=0.75, flip=True, grade=GR,
            align_red=True, lead=0.42)
text = dict(text=LINE, y=0.22, size=96, scrim=0.5, font="cg-italic")

pages = [img(vpage(P["KF"], O + "w01y0.jpg", "N° I", cat(1, COLLAR), TONE), 1),
         img(vpage(P["KB"], O + "w01y1.jpg", "N° II", cat(2, ARA, ROME), TONE), 1)]
fin = img(vstacked(P["KF"], P["KB"], O + "w01yc.jpg", "N° III", tone=TONE), 4)

# A: the reel as usual (its hook frames are not used, only pages + finale)
spec_a = dict(seed=37000, track=MP, segments=[dict(hook, until="drop")] + pages + [fin],
              texts=[dict(text, **{"from": 0, "to": "drop"})])
# P: the hook alone, BRIDGE frames longer at the front; the red still lands 0.42 s before its end
spec_p = dict(seed=37000, track=MP, segments=[dict(hook, dur=(HOOK_N + BRIDGE) / FPS)],
              texts=[dict(text, **{"from": 0, "to": "end"})])


def render(spec):
    """compose.compose()'s frame loop, yielding float frames instead of encoding them"""
    tr = C.TRACKS[spec["track"]]
    drop, beat = tr["drop"], 60.0 / tr["bpm"]
    rnd = __import__("random").Random(spec.get("seed", 0))
    bounds, t, beats_after = [], 0.0, 0.0
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
    end_t = bounds[-1][1] / FPS
    texts = []
    for tx in spec["texts"]:
        rgb, a = C.text_layer(tx["text"], tx["y"], tx["size"], scrim=tx["scrim"], face=tx["font"])
        f0 = round(C.resolve_time(tx["from"], drop, beat, end_t) * FPS)
        f1 = round(C.resolve_time(tx["to"], drop, beat, end_t) * FPS)
        texts.append((f0, f1, rgb, a, tx.get("fade", 4)))
    C._FONT_PATH[0] = C.FONT
    fi = 0
    for seg, (b0, b1) in zip(spec["segments"], bounds):
        n = b1 - b0
        if seg["type"] == "clip":
            gen = C.clip_frames(seg, n, rnd, drop)
        else:
            canvas = C.image_canvas(seg)
            gen = (canvas for _ in range(n))
        for fr in gen:
            f = fr.astype(np.float32)
            for f0, f1, rgb, a, fade in texts:
                if f0 <= fi < f1:
                    k = min(1.0, (fi - f0 + 1) / fade, (f1 - fi) / fade) if f0 > 0 else min(1.0, (f1 - fi) / fade)
                    f = f * (1 - a * k) + rgb * (a * k)
            yield f
            fi += 1


def main(out):
    enc =["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-f", "lavfi", "-t", "7.267", "-i", "anullsrc=r=44100:cl=stereo", "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
           "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(enc, stdin=subprocess.PIPE)
    put = lambda f: p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    pre, n = [], 0
    for i, f in enumerate(render(spec_p)):         # hook with BRIDGE frames of pre-roll in front
        if i < BRIDGE:
            pre.append(f.copy())
        else:
            put(f); n += 1
    last = None
    for i, f in enumerate(render(spec_a)):          # pages + finale
        if i >= HOOK_N:
            put(f); n += 1; last = f
    for j in range(BRIDGE):                          # finale dissolves into the pre-roll; frame 0 follows it
        x = (j + 1) / BRIDGE
        a = x * x * (3 - 2 * x)
        put(last * (1 - a) + pre[j] * a); n += 1
    p.stdin.close(); p.wait()
    json.dump(dict(A=spec_a, P=spec_p, bridge=BRIDGE), open(os.path.join(SP, "w1117_W01_look-at-her-soles_loop.json"), "w"),
              indent=1, ensure_ascii=False)
    json.dump([["1117d", "W01_look-at-her-soles_loop", MP, TONE, LINE.replace("\n", " "),
                "seamless loop: last 0.5 s dissolve from the finale into the 15 frames before frame 0; 12 beats; "
                "F05 hook mirrored; black quarter zip pages, black finale"]],
              open(os.path.join(SP, "ledger_1117d.json"), "w"), indent=1)
    print(json.dumps({"frames": n, "seconds": round(n / FPS, 3)}))


if __name__ == "__main__":
    main(sys.argv[1])
