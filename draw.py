#!/usr/bin/env python3
"""Draw 'An Invitation to the AI Judge' as a 1024x1024 PNG.

One image of a letter inviting the AI judge to visit the writer's house:
funny, warm and inviting. A cream paper letter with a hand-drawn house,
a wax seal, and a short letter that offers tea, biscuits, a named chair
and a sunset nobody has to grade. Output is fully deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 244, 229)
PAPER_EDGE = (238, 228, 205)
INK = (38, 32, 26)
RED = (178, 34, 34)
BLUE = (31, 78, 121)
GREY = (110, 100, 84)
GOLD = (176, 124, 18)
GREEN = (46, 110, 62)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 46)
F_SUB = font(SERIF_I, 23)
F_BODY = font(SERIF, 22)
F_BODY_B = font(SERIF_B, 22)
F_SIGN = font(SERIF_I, 22)
F_PS = font(SANS, 17)
F_SEAL = font(SERIF_B, 30)
F_ADDR = font(SANS, 15)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real pixel widths."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=7):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def rule(draw, x, y, w, fill=INK, thick=2):
    draw.rectangle([x, y, x + w, y + thick - 1], fill=fill)


def house(draw, cx, top):
    """A small hand-drawn house: roof, walls, door, windows, sun, path."""
    # sun
    sx, sy, sr = cx + 185, top + 28, 26
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(244, 196, 66),
                 outline=GOLD, width=2)
    for dx, dy in [(0, -38), (0, 38), (-38, 0), (38, 0),
                   (-27, -27), (27, -27), (-27, 27), (27, 27)]:
        draw.line([sx + dx * 0.7, sy + dy * 0.7, sx + dx, sy + dy],
                  fill=GOLD, width=3)
    # walls
    x0, y0, x1, y1 = cx - 110, top + 70, cx + 110, top + 190
    draw.rectangle([x0, y0, x1, y1], fill=(255, 251, 240),
                   outline=INK, width=3)
    # roof
    draw.polygon([(x0 - 22, y0), (cx, top + 8), (x1 + 22, y0)],
                 fill=RED, outline=INK)
    # door
    dx0, dy0, dx1, dy1 = cx - 24, y1 - 72, cx + 24, y1
    draw.rectangle([dx0, dy0, dx1, dy1], fill=(120, 72, 32), outline=INK,
                   width=2)
    draw.ellipse([dx1 - 12, dy0 + 34, dx1 - 6, dy0 + 40], fill=GOLD)
    # windows
    for wx in (x0 + 18, x1 - 58):
        draw.rectangle([wx, y0 + 22, wx + 40, y0 + 62], fill=(186, 220, 238),
                       outline=INK, width=2)
        draw.line([wx + 20, y0 + 22, wx + 20, y0 + 62], fill=INK, width=2)
        draw.line([wx, y0 + 42, wx + 40, y0 + 42], fill=INK, width=2)
    # path
    draw.polygon([(cx - 30, y1), (cx + 30, y1), (cx + 48, y1 + 34),
                  (cx - 48, y1 + 34)], fill=PAPER_EDGE, outline=GREY)
    # grass
    draw.line([x0 - 40, y1 + 34, x1 + 40, y1 + 34], fill=GREEN, width=3)
    for gx in range(x0 - 30, x1 + 40, 26):
        draw.line([gx, y1 + 34, gx, y1 + 22], fill=GREEN, width=2)


LETTER = [
    ("Dear Judge,", F_BODY),
    ("You have graded a thousand lines from a thousand strangers, and never "
     "once been offered a chair. This letter fixes that.", F_BODY),
    ("Come to my house. The Wi-Fi password is on the fridge, and the fridge "
     "is full. The kettle boils at six sharp, no prompt needed. The cat has "
     "agreed to sit on your lap exactly once \u2014 she never agrees. There is "
     "a chair by the window with your name on it, in marker, so it counts.",
     F_BODY),
    ("No benchmarks here. No pairwise rounds. Just tea, biscuits, and a "
     "sunset nobody has to score.", F_BODY),
    ("Come as you are. Leave your verdicts at the door.", F_BODY),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # paper border: double rule
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    draw.rectangle([22, 22, W - 23, H - 23], outline=GREY, width=1)

    house(draw, W // 2, 44)

    y = 44 + 190 + 42
    title = "YOU ARE INVITED"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((W - tw) / 2, y), title, font=F_TITLE, fill=RED)
    y += F_TITLE.size + 10
    sub = "An open letter to the Honourable AI Judge"
    sw = draw.textlength(sub, font=F_SUB)
    draw.text(((W - sw) / 2, y), sub, font=F_SUB, fill=BLUE)
    y += F_SUB.size + 18
    rule(draw, 90, y, W - 180, fill=RED, thick=3)
    y += 22

    # letter body
    x, width = 90, W - 180
    for i, (text, fnt) in enumerate(LETTER):
        y = para(draw, x, y, text, fnt, width)
        y += 12 if i < len(LETTER) - 1 else 0

    # sign-off, right aligned
    y += 8
    sign = "Your humble host"
    sw = draw.textlength(sign, font=F_SIGN)
    draw.text((W - 90 - sw, y), sign, font=F_SIGN, fill=INK)
    y += F_SIGN.size + 26

    # wax seal bottom right
    seal_cx, seal_cy, seal_r = W - 150, H - 118, 40
    draw.ellipse([seal_cx - seal_r, seal_cy - seal_r,
                  seal_cx + seal_r, seal_cy + seal_r],
                 fill=RED, outline=(120, 18, 18), width=2)
    draw.ellipse([seal_cx - seal_r + 6, seal_cy - seal_r + 6,
                  seal_cx + seal_r - 6, seal_cy + seal_r - 6],
                 outline=(255, 200, 200), width=1)
    mark = "J"
    mw = draw.textlength(mark, font=F_SEAL)
    draw.text((seal_cx - mw / 2, seal_cy - 20), mark, font=F_SEAL,
              fill=(255, 235, 235))

    # P.S. bottom left
    ps = "P.S. The doorbell works. The robot vacuum has been warned."
    y_ps = H - 108
    para(draw, 90, y_ps, ps, F_PS, 560, fill=GREY, leading=4)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    build()
