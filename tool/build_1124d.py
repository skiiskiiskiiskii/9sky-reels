#!/usr/bin/env python3
"""made 2026-11-24 (evening), batch 1124d: 8 reels BT01-BT08 on the format of V01 "bad together." (batch 1124c,
made in another chat; Kirill: the latest reel, make 8 new ones on its base - different lines, Louboutin hook but
different videos, keep the mockup second part, change the order of the mockups or something else, same style but
not 1:1).

The V01 format, kept: a Louboutin hook to the 3.13 s cut with one short provocative line on top (Cormorant italic),
then black and white cut against each other on every half beat (HIS / HERS labels), then the pair finale.
What changes reel to reel:
- hook: a different clip / moment in each (V01 was COUPLE in one take): 2-4 shot mixes at real speed and two
  single takes from other clips; the red ends differ (COUPLE both soles, SOLES logo sole, SOLES pair close-up,
  MARBLE, NAILS heel lift); SOLES never mirrored;
- line: 8 new lines in the "bad together." register - couple bait + the EX MUSEO wink (taken / missing / last seen);
- pages: white-first or black-first, quarter zip or zip hoodie first, backs mixed in, 6 or 8 half-beat pages or
  side-by-side his | hers pages, tones (oxblood, slate, ink, vitrine, bronze, smoke), labels (HIS / HERS,
  EXHIBIT A / B, MISSING), finales (side by side, zip pair stacked, 2 x 2, all four backs, his QZ + her zip);
- loop: 12 beats (7.27 s) instead of V01's 6.77 s, cuts on the same 99 BPM grid -> post with the V01 track."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_1024 import img, cat, P, O, SP
from vitrine2 import vpage2, vside, vstacked2, vgrid
from build_1119a import gr, sh, couple_red, soles_red, marble_red
import loopreel

OUT = "/mnt/user-data/outputs/ready-2026-11-24d/"
NUMS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
LBL = {  # label sets: key -> (black, white)
    "his": ("HIS  ·  BLACK", "HERS  ·  WHITE"),
    "exhibit": ("EXHIBIT A  ·  BLACK", "EXHIBIT B  ·  WHITE"),
    "missing": ("MISSING  ·  BLACK", "MISSING  ·  WHITE"),
}
WHITE = {"WF", "WB", "XWF", "XWB"}


def o(name):
    return O + "bt1124_" + name + ".jpg"


def half_pages(tag, keys, tone, labels="his", scale=0.9, cy=0.47, spot=None):
    """V01's run: one garment per half beat, numbered N° I.., labelled black / white"""
    out = []
    for j, k in enumerate(keys):
        lab = LBL[labels][1 if k in WHITE else 0]
        out.append((0.5, img(vpage2(P[k], o(f"{tag}{j}"), "N° " + NUMS[j], cat(j + 1, lab), tone, scale=scale,
                                    cy=cy, spot=spot), 1)))
    return out


def nails_heel(n, grade, **kw):                       # NAILS: her heel lifts, red sole at ~5.6 s
    return sh("NAILS", round(6.0 - n / 30, 3), n, grade, zoom=1.05, crop_x=0.0, crop_y=0.5, **kw)


R = []   # key, line, hook, after, idea

# BT01 matching red flags. - black nails -> red nails -> red soles on both; white first, oxblood; zip pair side by side
g = gr(b=-0.014, c=1.06, s=0.92); g.update(rm=0.02)
R.append(("BT01_matching-red-flags", "matching\nred flags.",
          [sh("NAILS", 1.75, 39, g, zoom=1.1), sh("SOLES", 1.45, 37, g, zoom=1.2, crop_x=0.45),
           couple_red(g, zoom=1.15, crop_y=0.72)],
          half_pages("01", ["WF", "KF", "XWF", "ZF", "WF", "KF"], "oxblood") +
          [(3, img(vside(P["ZF"], P["XWF"], o("01f"), "N° VII", "FIRST LOOK", "oxblood", title="EX MUSEO"), 1))],
          "NAILS black nails -> SOLES red nails -> COUPLE red on both; white first, oxblood; zip his | hers finale"))

# BT02 partners in red. - her pumps by his shoes -> his loafers walking (mirrored) -> logo sole; zip hoodies first, slate
g = gr(b=-0.016, c=1.06, s=0.9, g=0.97)
R.append(("BT02_partners-in-red", "partners\nin red.",
          [sh("SOLES", 0.55, 39, g, zoom=1.12, crop_y=0.55), sh("COUPLE", 2.1, 37, g, zoom=1.1, crop_y=0.7, flip=True),
           soles_red(18, g, zoom=1.15, crop_y=0.62)],
          half_pages("02", ["ZF", "XWF", "ZB", "XWB", "ZF", "XWF"], "slate", scale=0.88) +
          [(3, img(vstacked2(P["ZPF"], P["ZPB"], o("02f"), "N° VII", tone="slate"), 1))],
          "SOLES pumps by his shoes -> COUPLE loafers mirrored -> SOLES logo sole; zip hoodies front / back, slate; zip pair finale"))

# BT03 caught red-handed. - three hands (red nails) -> red heel on marble; EXHIBIT labels, ink; 2 x 2 finale
g = gr(b=-0.012, c=1.05, s=0.92); g.update(bs=0.02)
R.append(("BT03_caught-red-handed", "caught\nred-handed.",
          [sh("COUPLE", 0.55, 21, g, zoom=1.1, crop_y=0.7), sh("SOLES", 1.5, 37, g, zoom=1.25, crop_x=0.4),
           sh("NAILS", 2.3, 18, g, zoom=1.12), marble_red(18, g)],
          half_pages("03", ["KF", "KB", "WF", "WB", "ZF", "XWF"], "ink", labels="exhibit", scale=0.88,
                     spot=(0.5, 0.42, 0.6, 0.34)) +
          [(3, img(vgrid([P["KF"], P["WF"], P["ZF"], P["XWF"]], o("03f"), "N° VII", "FIRST LOOK", "ink"), 1))],
          "COUPLE hand -> SOLES red nails -> NAILS hand -> MARBLE; QZ front/back pairs then zips, EXHIBIT A / B, ink; 2 x 2"))

# BT04 trouble comes in pairs. - pair of heels in the mist -> his pair walking -> both soles close; his | hers pages
g = gr(b=-0.01, c=1.05, s=0.93)
side = lambda a, b, n, no, sub: (0.5, img(vside(P[a], P[b], o(f"04{n}"), no, sub, "vitrine"), 1))
R.append(("BT04_trouble-comes-in-pairs", "trouble comes\nin pairs.",
          [sh("NAILS", 0.55, 21, g, zoom=1.05, crop_y=0.55), sh("COUPLE", 1.7, 55, g, zoom=1.0, crop_y=0.6),
           sh("SOLES", 5.42, 18, g, zoom=1.12, crop_y=0.5)],
          [side("KF", "WF", 0, "N° I", cat(1, "HIS  ·  HERS")), side("ZF", "XWF", 1, "N° II", cat(2, "HIS  ·  HERS")),
           side("KB", "WB", 2, "N° III", cat(3, "HIS  ·  HERS")), side("ZB", "XWB", 3, "N° IV", cat(4, "HIS  ·  HERS")),
           (4, img(vstacked2(P["PF"], P["ZPF"], o("04f"), "N° V", tone="vitrine"), 1))],
          "NAILS heels in the mist -> COUPLE his pair walking -> SOLES both soles close; his | hers pairs on every half beat; QZ pair over zip pair"))

# BT05 accomplices. - her hand over his shoes -> walking off -> red on both (COUPLE, mirrored); 8 pages, bronze
g = gr(b=-0.014, c=1.06, s=0.9); g.update(rh=0.02)
R.append(("BT05_accomplices", "accomplices.",
          [sh("COUPLE", 0.55, 39, g, zoom=1.12, crop_y=0.55, flip=True),
           couple_red(g, speed=1.12, zoom=1.12, crop_x=0.5, crop_y=0.7, flip=True)],
          half_pages("05", ["KF", "XWF", "ZF", "WF", "KB", "XWB", "ZB", "WB"], "bronze", scale=0.86, cy=0.46) +
          [(2, img(vside(P["KF"], P["XWF"], o("05f"), "N° IX", "FIRST LOOK", "bronze", title="EX MUSEO"), 1))],
          "COUPLE mirrored: her hand over his shoes -> jump to the walk -> red on both; QZ and zip crossed, 8 pages, bronze; his QZ | her zip"))

# BT06 no one saw us leave. - heels in the mist -> walking away -> legs -> red heel on marble; MISSING, smoke, 4 backs
g = gr(b=-0.018, c=1.05, s=0.88, g=0.97)
R.append(("BT06_no-one-saw-us-leave", "no one saw\nus leave.",
          [sh("NAILS", 0.5, 21, g, zoom=1.08, crop_y=0.5), sh("COUPLE", 2.3, 37, g, zoom=1.05, crop_y=0.6, flip=True),
           sh("SOLES", 3.4, 18, g, zoom=1.1, crop_y=0.5), marble_red(18, g, flip=True)],
          half_pages("06", ["XWF", "ZF", "XWB", "ZB", "WF", "KF"], "smoke", labels="missing") +
          [(3, img(vgrid([P["KB"], P["WB"], P["ZB"], P["XWB"]], o("06f"), "N° VII", "FIRST LOOK", "smoke"), 1))],
          "NAILS heels in the mist -> COUPLE walking mirrored -> SOLES legs -> MARBLE mirrored; MISSING labels, smoke; all four backs"))

# BT07 matching, unfortunately. - pumps -> black nails -> red nails -> red on both; same garment black / white
g = gr(b=-0.012, c=1.05, s=0.92); g.update(rm=0.015, bs=0.01)
R.append(("BT07_matching-unfortunately", "matching,\nunfortunately.",
          [sh("SOLES", 0.6, 21, g, zoom=1.15, crop_y=0.6), sh("NAILS", 2.0, 18, g, zoom=1.15),
           sh("SOLES", 1.55, 19, g, zoom=1.2, crop_x=0.5), couple_red(g, zoom=1.25, crop_x=0.45, crop_y=0.78)],
          half_pages("07", ["KF", "WF", "ZF", "XWF", "KB", "WB"], "vitrine", scale=0.92, cy=0.46,
                     spot=(0.5, 0.4, 0.62, 0.36)) +
          [(3, img(vside(P["KF"], P["WF"], o("07f"), "N° VII", "FIRST LOOK", "vitrine", title="EX MUSEO"), 1))],
          "SOLES pumps -> NAILS black nails -> SOLES red nails -> COUPLE red on both; each piece black then white; QZ his | hers"))

# BT08 last seen together. - NAILS in one take (like V01, other clip): hand over his shoes -> her heel lifts, red
g = gr(b=-0.016, c=1.06, s=0.9)
R.append(("BT08_last-seen-together", "last seen\ntogether.",
          [sh("NAILS", 2.85, 94, g, zoom=1.08, crop_x=0.0, crop_y=0.5)],
          half_pages("08", ["ZF", "XWF", "KF", "WF", "ZF", "XWF"], "oxblood", labels="missing", scale=0.9, cy=0.48,
                     spot=(0.42, 0.44, 0.6, 0.36)) +
          [(3, img(vstacked2(P["PF"], P["PB"], o("08f"), "N° VII", tone="oxblood"), 1))],
          "NAILS in one take: hand over his shoes -> her heel lifts, red; MISSING labels, oxblood; QZ pair finale"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    ledger = []
    for i, (k, line, hook, after, idea) in enumerate(R):
        ledger.append(["1124d", k, "V01 track (99 BPM grid)", line.replace("\n", " "), idea])
        if only and k.split("_")[0] not in only:
            continue
        assert abs(sum(b for b, _ in after) - 6) < 1e-6, k
        r = loopreel.make(OUT + k + ".mp4", hook, line, after, seed=47000 + i)
        json.dump(dict(hook=hook, line=line, after=after), open(os.path.join(SP, f"bt1124_{k}.json"), "w"),
                  indent=1, ensure_ascii=False)
        print(k, json.dumps(r))
    json.dump(ledger, open(os.path.join(SP, "ledger_1124d.json"), "w"), indent=1)
