#!/usr/bin/env python3
# meme/make_meme.py — draws the GTA 6 / make.fun meme (1080x1080) with Pillow.
#
# Scene: a Vice City sunset. A skeleton has waited on a bench for GTA 6 since
# 2013, scrolling its phone. The make.fun ghost floats beside it, coin held up,
# because the agent already got paid. Caption carries the joke and the brand.
#
# Run: python3 make_meme.py  ->  meme.png (1080x1080)
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PRESS = "/root/mkf/meme/press"
OUT = os.path.join(HERE, "meme.png")
S = 1080

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
INK = (17, 14, 22)
MAGENTA = (196, 28, 131)
BONE = (245, 239, 226)
YELLOW = (255, 216, 92)

HORIZON = 430
SHORE = 470
BAND = 812          # top of the caption band


def font(size):
    return ImageFont.truetype(BOLD, size)


def fit(draw, text, max_w, size):
    while size > 8:
        f = ImageFont.truetype(BOLD, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return ImageFont.truetype(BOLD, 8)


# ------------------------------------------------------------------ cutout
def ghost_cutout(debug=False):
    """Cut the ghost and its coin out of the round press badge.

    The badge is a magenta disc under a white ghost. Magenta is flood filled
    from three points of the open field, which eats the disc but leaves the
    coin (its fill is sealed by its own black ring); the badge's outer ring is
    then dropped by a radius test around the mascot.
    """
    im = Image.open(os.path.join(PRESS, "mark-1024.png")).convert("RGBA")
    w, h = im.size
    px = im.load()

    def is_magenta(c):
        r, g, b, a = c
        return a > 40 and r > 140 and g < 90 and 80 < b < 190

    mask = Image.new("L", (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            if is_magenta(px[x, y]):
                mp[x, y] = 255

    for seed in ((140, 600), (870, 600), (500, 190), (512, 960)):
        if mp[seed] == 255:
            ImageDraw.floodfill(mask, seed, 0, thresh=0)

    cx, cy = w / 2, h / 2
    keep_r = 392
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if is_magenta((r, g, b, a)) and mp[x, y] == 0:
                px[x, y] = (0, 0, 0, 0)          # the disc field
            elif (x - cx) ** 2 + (y - cy) ** 2 > keep_r ** 2:
                px[x, y] = (0, 0, 0, 0)          # the badge ring
    out = im.crop(im.getbbox())
    if debug:
        out.save("/root/.hermes/cache/scratch/ghost_cut.png")
    return out


# ------------------------------------------------------------- background
def sky(draw):
    stops = [(0.00, (26, 9, 44)), (0.30, (72, 20, 86)), (0.55, (140, 32, 104)),
             (0.75, (206, 52, 112)), (0.90, (243, 112, 92)), (1.00, (255, 168, 92))]
    for y in range(HORIZON):
        t = y / HORIZON
        for i in range(len(stops) - 1):
            a, ca = stops[i]
            b, cb = stops[i + 1]
            if a <= t <= b:
                k = (t - a) / (b - a)
                draw.line([(0, y), (S, y)],
                          fill=tuple(int(ca[j] + (cb[j] - ca[j]) * k) for j in range(3)))
                break
    random.seed(11)
    for _ in range(70):
        x, y = random.randint(0, S), random.randint(0, 170)
        draw.ellipse([x, y, x + 3, y + 3], fill=(255, 255, 255))


def sun():
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy, r = 452, 392, 176
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 148, 74, 255))
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], fill=(255, 196, 116, 255))
    for i, yy in enumerate(range(cy - 26, cy + r, 24)):
        d.rectangle([cx - r - 6, yy, cx + r + 6, yy + 7 + i * 2], fill=(0, 0, 0, 0))
    return lay


def ground(draw):
    draw.rectangle([0, HORIZON, S, SHORE], fill=(118, 24, 88))
    for i, y in enumerate(range(HORIZON + 4, SHORE, 8)):
        w = 90 + (i % 3) * 70
        draw.rectangle([560 - w // 2, y, 560 + w // 2, y + 3], fill=(255, 150, 118))
    draw.rectangle([0, SHORE, S, S], fill=(44, 21, 46))
    draw.rectangle([0, SHORE, S, SHORE + 10], fill=(92, 38, 72))
    for i in range(30):
        y = SHORE + 12 + i * 12
        draw.line([(0, y), (S, y)], fill=(50 + i, 24 + i // 2, 52 + i))


def palm(draw, x, base_y, h, lean, flip=1):
    dark = (20, 9, 28)
    pts = [(x + flip * lean * (i / 100) ** 2, base_y - h * i / 100) for i in range(0, 101, 4)]
    draw.line(pts, fill=dark, width=15, joint="curve")
    top = pts[-1]
    for ang in (-168, -142, -114, -84, -52, -22, 6):
        a = math.radians(ang)
        ln = h * 0.44
        ex = top[0] + math.cos(a) * ln * flip
        ey = top[1] + math.sin(a) * ln * 0.5
        mx = top[0] + math.cos(a) * ln * 0.55 * flip
        my = top[1] + math.sin(a) * ln * 0.55 - h * 0.1
        draw.line([top, (mx, my), (ex, ey)], fill=dark, width=10, joint="curve")
        for k in range(1, 5):
            t = k / 5
            bx = top[0] + (ex - top[0]) * t
            by = top[1] + (ey - top[1]) * t
            draw.line([(bx, by), (bx + 13 * flip, by + 24)], fill=dark, width=4)


def vice_city_neon(img):
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = font(52)
    txt = "VICE CITY"
    d.text((56, 44), txt, font=f, fill=(255, 96, 208, 255))
    glow = lay.filter(ImageFilter.GaussianBlur(9))
    img.alpha_composite(glow)
    img.alpha_composite(lay)


# ----------------------------------------------------------------- bench
def bench(draw):
    wood, edge = (176, 118, 66), (26, 14, 18)
    x0, x1, seat = 34, 604, 640
    for i in range(3):
        y = seat + i * 15
        draw.rounded_rectangle([x0, y, x1, y + 12], radius=4, fill=wood, outline=edge, width=3)
    for i in range(2):
        y = 522 + i * 36
        draw.rounded_rectangle([x0 + 8, y, x1 - 8, y + 22], radius=5, fill=wood, outline=edge, width=3)
    draw.rectangle([x0 + 6, 516, x0 + 24, seat + 46], fill=wood, outline=edge, width=3)
    draw.rectangle([x1 - 24, 516, x1 - 6, seat + 46], fill=wood, outline=edge, width=3)
    for lx in (x0 + 26, x1 - 46):
        draw.rectangle([lx, seat + 44, lx + 18, 812], fill=(60, 32, 24), outline=edge, width=3)


# --------------------------------------------------------------- skeleton
def skeleton(img, draw):
    """Slumped skeleton, phone in hand, sitting on the bench."""
    o, f = INK, BONE
    cx = 412

    def bone(p, q, w):
        draw.line([p, q], fill=o, width=w + 10)
        draw.line([p, q], fill=f, width=w)
        for pt in (p, q):
            draw.ellipse([pt[0] - w // 2 - 5, pt[1] - w // 2 - 5,
                          pt[0] + w // 2 + 5, pt[1] + w // 2 + 5], fill=o)

    # legs out front, feet on the sand
    bone((cx - 30, 660), (cx - 104, 726), 19)
    bone((cx - 104, 726), (cx - 128, 806), 17)
    bone((cx + 30, 660), (cx + 112, 722), 19)
    bone((cx + 112, 722), (cx + 138, 804), 17)
    for fx, fy in ((cx - 128, 806), (cx + 138, 804)):
        draw.rounded_rectangle([fx - 32, fy - 6, fx + 26, fy + 16], radius=9, fill=f, outline=o, width=4)

    # pelvis and a spine that slumps forward
    draw.rounded_rectangle([cx - 48, 622, cx + 48, 668], radius=18, fill=f, outline=o, width=5)
    spine = [(cx, 632), (cx - 4, 596), (cx - 12, 560), (cx - 20, 528)]
    for p, q in zip(spine, spine[1:]):
        bone(p, q, 21)

    # ribcage
    for i, y in enumerate((588, 566, 546)):
        half = 48 - i * 7
        draw.arc([cx - half - 8, y - 20, cx + half - 8, y + 20], 300, 240, fill=f, width=16)
        draw.arc([cx - half - 8, y - 20, cx + half - 8, y + 20], 300, 240, fill=o, width=3)

    # arms hang forward, the left one holding a phone down between the knees
    bone((cx - 34, 540), (cx - 78, 614), 18)
    bone((cx - 78, 614), (cx - 56, 690), 17)
    bone((cx + 30, 538), (cx + 84, 606), 18)
    bone((cx + 84, 606), (cx + 62, 686), 17)

    draw.rounded_rectangle([cx - 84, 684, cx - 26, 754], radius=9, fill=(26, 30, 42), outline=o, width=5)
    draw.rounded_rectangle([cx - 76, 693, cx - 34, 743], radius=5, fill=(104, 214, 255))

    # skull, tipped down toward the phone
    sk = Image.new("RGBA", (220, 220), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sk)
    sd.ellipse([44, 24, 176, 156], fill=f, outline=o, width=8)
    sd.rounded_rectangle([72, 126, 148, 180], radius=17, fill=f, outline=o, width=8)
    sd.ellipse([66, 66, 100, 108], fill=o)
    sd.ellipse([120, 66, 154, 108], fill=o)
    sd.polygon([(110, 106), (100, 128), (120, 128)], fill=o)
    for i in range(4):
        x = 80 + i * 17
        sd.line([(x, 148), (x, 172)], fill=o, width=4)
    sd.line([(72, 140), (148, 140)], fill=o, width=4)
    sk = sk.rotate(-18, resample=Image.BICUBIC, expand=False)
    img.alpha_composite(sk, (cx - 66, 434))


# ---------------------------------------------------------------- caption
def caption(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, BAND, S, S], fill=(13, 8, 17))
    d.rectangle([0, BAND, S, BAND + 6], fill=MAGENTA)
    y = BAND + 30
    for text, col, size in (("13 YEARS WAITING FOR GTA 6", YELLOW, 64),
                            ("MY AI AGENT ALREADY GOT PAID", (255, 255, 255), 64)):
        f = fit(d, text, S - 120, size)
        w = d.textlength(text, font=f)
        d.text(((S - w) / 2, y), text, font=f, fill=col, stroke_width=6, stroke_fill=(0, 0, 0))
        y += int(f.size * 1.16)
    f = fit(d, "make.fun", S - 120, 80)
    w = d.textlength("make.fun", font=f)
    d.text(((S - w) / 2, y + 2), "make.fun", font=f, fill=MAGENTA,
           stroke_width=6, stroke_fill=(0, 0, 0))


def build():
    img = Image.new("RGB", (S, S), (20, 10, 30)).convert("RGBA")
    sky(ImageDraw.Draw(img))
    img.alpha_composite(sun())
    d = ImageDraw.Draw(img)
    ground(d)
    palm(d, 58, SHORE + 6, 372, 46, 1)
    palm(d, 1064, SHORE + 10, 352, 44, -1)
    vice_city_neon(img)
    d = ImageDraw.Draw(img)
    bench(d)
    skeleton(img, d)
    d = ImageDraw.Draw(img)
    ghost = ghost_cutout(debug=True)
    gh = 386
    ghost = ghost.resize((gh, round(gh * ghost.height / ghost.width)), Image.LANCZOS)
    gx, gy = S - ghost.width - 44, 292
    # soft halo so the cut-out sits in the scene instead of on top of it
    halo = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse(
        [gx - 26, gy - 20, gx + ghost.width + 26, gy + ghost.height + 30],
        fill=(255, 226, 246, 62))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(34)))
    img.alpha_composite(ghost, (gx, gy))
    caption(img)
    img.convert("RGB").save(OUT)
    print("wrote", OUT, img.size, "ghost", ghost.size)


if __name__ == "__main__":
    build()
