#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Saturday 21 November 2026.

Everything is drawn from scratch with PIL: masthead, big-number strip,
three large features, ten small illustrated stories, a world map with
numbered pins, twenty one-line briefs and a DATE CHECK footer.
Deterministic: no clock, no randomness, no network. Run it and it writes
entry.png (1024x1024) next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

W, H = 1024, 1024
PAPER = (251, 247, 236)
INK = (20, 20, 20)
SOFT = (74, 74, 74)
RULE = (150, 142, 124)
RED = (176, 32, 32)
BLUE = (29, 78, 137)
GOLD = (176, 132, 24)
PANEL = (255, 255, 255)
SKY = (38, 52, 84)
LAND = (239, 233, 216)
LAND_LINE = (138, 131, 120)

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(text, fnt, max_w, draw)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def hline(draw, x0, x1, y, color=INK, width=1):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def box(draw, x, y, w, h, outline=RULE, fill=None, width=1):
    draw.rectangle([x, y, x + w, y + h], outline=outline, fill=fill, width=width)


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 10)
    draw.text((x, y), text, font=f, fill=color)
    return y + 14


# ---------------------------------------------------------------- art panels

def art_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 26),
               (x + w * 0.55, y + h - 34), (x, y + h - 22)], fill=(28, 44, 34))
    for tx in (0.12, 0.30, 0.82):
        bx = x + w * tx
        d.polygon([(bx, y + h - 52), (bx + 7, y + h - 26), (bx - 7, y + h - 26)],
                  fill=(16, 40, 26))
    d.line([(x + 8, y + 30), (x + w - 14, y + 62)], fill=(255, 255, 255), width=3)
    d.polygon([(x + w - 30, y + 56), (x + w - 12, y + 62), (x + w - 30, y + 68)],
              fill=(255, 255, 255))
    d.polygon([(x + w - 14, y + 60), (x + w - 4, y + 63), (x + w - 14, y + 66)],
              fill=(255, 170, 60))
    d.text((x + 8, y + 6), "POLAND", font=font(SANS_B, 11), fill=(255, 255, 255))
    d.text((x + 8, y + h - 18), "NATO", font=font(SANS_B, 11), fill=(255, 210, 90))


def art_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 96, 122))
    cx, cy = x + w * 0.34, y + h * 0.46
    for r in (52, 40, 28, 17):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=(255, 255, 255), width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 220, 120))
    for i in range(7):
        rx = x + w * (0.62 + 0.05 * i)
        d.line([(rx, y + h - 34), (rx - 4, y + h - 14)], fill=(200, 225, 240), width=2)
    d.polygon([(x + w - 66, y + h - 30), (x + w - 66, y + h - 52),
               (x + w - 30, y + h - 52), (x + w - 30, y + h - 30)],
              fill=(240, 230, 200))
    d.polygon([(x + w - 72, y + h - 50), (x + w - 48, y + h - 68),
               (x + w - 24, y + h - 50)], fill=RED)
    d.text((x + 8, y + 6), "ODISHA, INDIA", font=font(SANS_B, 11), fill=(255, 255, 255))


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(247, 240, 226))
    base = y + h - 22
    vals = [0.86, 0.72, 0.78, 0.55, 0.62, 0.38, 0.46, 0.24]
    bw = (w - 24) / len(vals)
    pts = []
    for i, v in enumerate(vals):
        bx = x + 12 + i * bw
        top = base - v * (h - 44)
        d.rectangle([bx + 2, top, bx + bw - 2, base], fill=RED)
        pts.append((bx + bw / 2, top - 4))
    d.line(pts, fill=INK, width=2)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
    d.text((x + 8, y + 6), "S&P 500  -3.7%", font=font(SANS_B, 12), fill=RED)


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    d.polygon([(x + 8, y + 12), (x + w - 8, y + 12), (x + w / 2, y + 2)],
              fill=(90, 84, 70))
    for i in range(4):
        cx = x + 14 + i * (w - 28) / 3
        d.rectangle([cx - 3, y + 14, cx + 3, y + h - 6], fill=(120, 112, 94))
    d.rectangle([x + 6, y + h - 6, x + w - 6, y + h - 2], fill=(90, 84, 70))


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 226))
    cx, cy, r = x + w * 0.30, y + h * 0.52, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    d.arc([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], 200, 340,
          fill=BLUE, width=2)
    d.line([(cx, cy - r - 8), (cx, cy + r + 8)], fill=RED, width=3)
    d.polygon([(cx, cy - r - 12), (cx + 5, cy - r - 4), (cx - 5, cy - r - 4)],
              fill=RED)
    d.text((x + w * 0.58, y + 8), "1.5 C", font=font(SANS_B, 15), fill=RED)
    d.text((x + w * 0.58, y + 26), "OVERSHOOT", font=font(SANS_B, 9), fill=INK)


def art_flags3(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    fw, fh = (w - 24) / 3, 22
    # United States: stripes + blue canton
    fx = x + 8
    for i in range(5):
        d.rectangle([fx, y + 8 + i * (fh / 5), fx + fw, y + 8 + (i + 1) * (fh / 5)],
                    fill=RED if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, y + 8, fx + fw * 0.45, y + 8 + fh * 0.55], fill=BLUE)
    # China: red field, yellow stars
    fx += fw + 4
    d.rectangle([fx, y + 8, fx + fw, y + 8 + fh], fill=(222, 41, 16))
    d.ellipse([fx + 4, y + 12, fx + 11, y + 19], fill=(255, 222, 0))
    # Russia: white / blue / red bands
    fx += fw + 4
    for i, col in enumerate([(255, 255, 255), BLUE, RED]):
        d.rectangle([fx, y + 8 + i * (fh / 3), fx + fw, y + 8 + (i + 1) * (fh / 3)],
                    fill=col)
    d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 8], fill=(120, 100, 70))


def art_shield(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 48))
    cx, cy = x + w * 0.5, y + h * 0.52
    d.polygon([(cx - 16, cy - 14), (cx + 16, cy - 14), (cx + 16, cy + 2),
               (cx, cy + 18), (cx - 16, cy + 2)], outline=(255, 210, 90), width=3)
    d.line([(cx - 22, y + 8), (cx + 6, cy - 6)], fill=(255, 255, 255), width=2)
    d.polygon([(cx + 2, cy - 10), (cx + 12, cy - 6), (cx + 2, cy - 2)],
              fill=(255, 170, 60))
    for i in range(3):
        bx = x + 10 + i * 22
        d.rectangle([bx, y + h - 12, bx + 14, y + h - 4], fill=(90, 96, 110))


def art_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 200))
    d.polygon([(x + 12, y + h - 16), (x + w - 12, y + h - 16),
               (x + w - 22, y + h - 30), (x + 22, y + h - 30)], fill=(140, 40, 30))
    d.rectangle([x + w * 0.55, y + h - 44, x + w * 0.72, y + h - 30],
                fill=(200, 200, 200))
    d.polygon([(x + w * 0.30, y + 10), (x + w * 0.36, y + 20),
               (x + w * 0.30, y + 30), (x + w * 0.24, y + 20)], fill=(255, 140, 40))
    d.polygon([(x + w * 0.42, y + 16), (x + w * 0.47, y + 24),
               (x + w * 0.42, y + 32), (x + w * 0.37, y + 24)], fill=(255, 90, 30))
    for i in range(4):
        wx = x + 8 + i * 14
        d.arc([wx, y + h - 8, wx + 12, y + h + 2], 180, 360, fill=BLUE, width=2)


def art_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 212))
    d.line([(x + 12, y + h - 10), (x + w - 12, y + h - 10)], fill=INK, width=3)
    d.rectangle([x + w * 0.28, y + 12, x + w * 0.72, y + 22], fill=(120, 80, 40),
                outline=INK)
    d.line([(x + w * 0.5, y + 22), (x + w * 0.62, y + h - 12)], fill=(120, 80, 40),
           width=5)
    d.polygon([(x + w * 0.68, y + 8), (x + w * 0.80, y + 14),
               (x + w * 0.70, y + 24), (x + w * 0.58, y + 18)], fill=(255, 140, 40))


def art_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 244))
    cx, cy = x + w * 0.5, y + h * 0.45
    d.rounded_rectangle([cx - 26, cy - 9, cx + 26, cy + 9], radius=9,
                        fill=(255, 255, 255), outline=RED, width=2)
    d.rounded_rectangle([cx - 26, cy - 9, cx, cy + 9], radius=9, fill=RED)
    d.ellipse([cx - 30, cy - 26, cx - 18, cy - 14], outline=BLUE, width=2)
    d.ellipse([cx + 18, cy + 12, cx + 30, cy + 24], outline=BLUE, width=2)
    d.text((x + 6, y + h - 14), "1 IN 12 CLEAR", font=font(SANS_B, 9), fill=BLUE)


def art_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    # Union Jack, simplified: blue field, white and red crosses
    fx, fy, fw, fh = x + 8, y + 8, (w - 24) / 2, 24
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=BLUE)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=(255, 255, 255), width=3)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=(255, 255, 255), width=3)
    d.line([(fx + fw / 2, fy), (fx + fw / 2, fy + fh)], fill=(255, 255, 255), width=5)
    d.line([(fx, fy + fh / 2), (fx + fw, fy + fh / 2)], fill=(255, 255, 255), width=5)
    d.line([(fx + fw / 2, fy), (fx + fw / 2, fy + fh)], fill=RED, width=2)
    d.line([(fx, fy + fh / 2), (fx + fw, fy + fh / 2)], fill=RED, width=2)
    # EU flag: blue field, ring of gold stars
    ex = fx + fw + 8
    d.rectangle([ex, fy, ex + fw, fy + fh], fill=(0, 51, 153))
    for i in range(8):
        import math
        a = math.pi * 2 * i / 8 - math.pi / 2
        sx = ex + fw / 2 + math.cos(a) * (fw / 2 - 6)
        sy = fy + fh / 2 + math.sin(a) * (fh / 2 - 5)
        d.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(255, 204, 0))


def art_berlin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 228, 232))
    for i in range(5):
        cx = x + 16 + i * (w - 32) / 4
        d.rectangle([cx - 3, y + 12, cx + 3, y + h - 6], fill=(110, 104, 90))
    d.rectangle([x + 8, y + 8, x + w - 8, y + 13], fill=(110, 104, 90))
    d.rectangle([x + 8, y + h - 8, x + w - 8, y + h - 4], fill=(110, 104, 90))
    for i, col in enumerate([INK, RED, GOLD]):
        d.rectangle([x + w - 30 + i * 7, y + 4, x + w - 25 + i * 7, y + 12],
                    fill=col)


# ---------------------------------------------------------------- world map

CONTINENTS = {
    "n_america": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                  (-85, 70), (-76, 62), (-65, 60), (-55, 52), (-60, 46),
                  (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21),
                  (-97, 16), (-105, 20), (-115, 29), (-125, 40), (-125, 49),
                  (-140, 60), (-155, 58), (-165, 60)],
    "s_america": [(-80, 9), (-72, 12), (-60, 8), (-52, 5), (-44, -3),
                  (-35, -8), (-40, -20), (-48, -28), (-58, -38), (-65, -45),
                  (-70, -54), (-73, -37), (-70, -20), (-80, -5)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
               (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
               (32, 70), (40, 68), (44, 68), (40, 60), (35, 55), (30, 50),
               (28, 45), (23, 40), (19, 42), (12, 44), (3, 43), (-2, 37)],
    "africa": [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12),
               (51, 11), (48, 0), (40, -10), (35, -18), (32, -29), (26, -34),
               (19, -35), (15, -27), (12, -18), (9, -1), (4, 6), (-8, 5),
               (-15, 11), (-17, 15), (-16, 20), (-15, 27), (-10, 31)],
    "asia": [(40, 68), (55, 72), (70, 73), (90, 75), (110, 76), (130, 72),
             (150, 70), (170, 67), (178, 65), (170, 60), (162, 56),
             (158, 52), (142, 50), (140, 40), (135, 35), (130, 33),
             (127, 35), (122, 38), (120, 32), (115, 23), (108, 18),
             (105, 10), (100, 8), (97, 16), (92, 21), (88, 22), (86, 20),
             (80, 15), (77, 8), (74, 20), (70, 25), (66, 25), (60, 25),
             (56, 27), (52, 29), (48, 30), (44, 29), (40, 32), (36, 36),
             (33, 36), (30, 36), (27, 37), (26, 39), (30, 41), (35, 42),
             (38, 46), (40, 52), (45, 55), (50, 60)],
    "oceania": [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
                (136, -35), (140, -38), (146, -39), (150, -37), (153, -32),
                (153, -27), (146, -19), (142, -15), (142, -11), (136, -12),
                (132, -12), (126, -14), (122, -17), (118, -20)],
}

PINS = [  # (number, lon, lat, display dx, display dy in px)
    (1, 19, 52, 0, 0), (2, 85, 20, 0, 0), (3, -74, 41, 0, 0),
    (4, 4, 52, -16, -9), (5, 30, 37, 12, 9),
    (6, 114, 22, 0, 0), (7, 47, 25, 0, 0), (8, 56, 26, 0, 0),
    (9, -118, 34, 0, 0), (10, -87, 41, 0, 0),
    (11, 4, 51, 16, 7), (12, 13, 52, 0, -11), (13, 21, 42, -10, 11),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    lat_top, lat_bot = 84, -58
    for pts in CONTINENTS.values():
        xy = [(x + (lon + 180) / 360 * w,
               y + (lat_top - lat) / (lat_top - lat_bot) * h)
              for lon, lat in pts]
        d.polygon(xy, fill=LAND, outline=LAND_LINE)
    nf = font(SANS_B, 9)
    for num, lon, lat, dx, dy in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (lat_top - lat) / (lat_top - lat_bot) * h
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (qx, qy)], fill=RED, width=1)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        tw = d.textlength(str(num), font=nf)
        d.text((qx - tw / 2, qy - 6), str(num), font=nf, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories

FEATURES = [
    ("1 · POLAND", "RUSSIAN MISSILES LAND ON NATO SOIL",
     "Two Russian missiles and a suspected drone came down in south-east "
     "Poland during a huge overnight strike on Ukraine. PM Tusk called it "
     "an intentional provocation; NATO called it a grave violation.",
     "AP · CBS News", art_poland),
    ("2 · INDIA", "AFTER AKVAN: 370,000 SAFE, NO DEATHS",
     "Cyclone Akvan crossed Odisha's coast near Gopalpur on Friday, winds "
     "gusting to 90 km/h. Over 370,000 people had been moved to shelters; "
     "officials reported no deaths or major damage as rain ran on.",
     "IMD · Reuters", art_akvan),
    ("3 · MARKETS", "WALL STREET SLIDES INTO CORRECTION",
     "The S&P 500 fell 3.7% on Friday and the Nasdaq lost more than 5%, "
     "both in correction territory as AI shares sold off. Japan's Nikkei "
     "fell 5.06%; gold dropped about 4%.",
     "BBC · UPI", art_markets),
]

SMALLS = [
    ("4 · THE HAGUE", "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
     "The ICJ ruled Myanmar committed state-sponsored genocide against "
     "the Rohingya — a first for the court.",
     "PBS · Sky News", art_court),
    ("5 · ANTALYA", "COP31 IN OVERTIME, FOSSIL FUELS CUT",
     "Talks ran past Friday's deadline with no deal; the draft drops "
     "fossil fuels and a $120bn target.",
     "Reuters · UN News", art_cop),
    ("6 · SHENZHEN", "AFTER THE TRILATERAL: A NEW FORMAT",
     "US envoy Jared Kushner said Moscow had agreed to a multilateral "
     "format, with Europe in the room.",
     "RFE/RL · SRN", art_flags3),
    ("7 · RIYADH", "HOUTHI MISSILES DOWNED OVER RIYADH",
     "The Saudi-led coalition said it destroyed three Houthi missiles "
     "fired at Riyadh, then struck Hodeidah.",
     "Middle East Eye", art_shield),
    ("8 · HORMUZ", "IRAN WAR: TRUMP IN NO RUSH",
     "Trump is not rushing Iran decisions and may not decide until 2027. "
     "A tanker caught fire near Hormuz.",
     "CBS News", art_tanker),
    ("9 · LOS ANGELES", "PALISADES FIRE: GUILTY ON BOTH COUNTS",
     "A jury convicted Jonathan Rinderknecht, 30, of arson over the "
     "January 2025 fire that killed 12.",
     "AP · CNN", art_gavel),
    ("10 · HEALTH", "A PILL THAT HALTS PANCREATIC CANCER",
     "Trial of daraxonrasib: tumours stopped growing in nearly all "
     "patients; cancer became undetectable in one in 12.",
     "The Guardian", art_pill),
    ("11 · BRUSSELS", "UK AND EU SIGN THREE DEALS",
     "PM Andy Burnham signed deals on food trade, carbon markets and "
     "youth travel.",
     "BBC · RFI", art_ukeu),
    ("12 · BERLIN", "EUROPE DEMANDS A SEAT AT THE TABLE",
     "30+ European leaders met Zelenskyy on Thursday and backed a "
     "four-party format. No date set. [THU]",
     "AFP · QNC News", art_berlin),
    ("13 · KOSOVO", "THACI GUILTY OF OBSTRUCTING JUSTICE",
     "The Kosovo court found ex-president Hashim Thaci guilty of "
     "obstruction and jailed him for 17 months.",
     "RFE/RL", art_gavel),
]

BRIEFS = [
    ("14 · IRAQ", "Iraqi forces entered Jurf al-Sakhar after 12 years of Hezbollah rule."),
    ("15 · AFGHANISTAN", "UN: ISIS-K is gaining drones; its threat is rising."),
    ("16 · SOUTH AFRICA", "Murders eased, but homicides still run at 60 a day."),
    ("17 · INDONESIA", "Jakarta asked Google about 19,000 removed YouTube accounts."),
    ("18 · SPACE", "Voyager 1 sent a message from one light-day away."),
    ("19 · CHIPS", "US approved sale of ~900,000 AI chips to China in six months."),
    ("20 · NVIDIA", "California AG subpoenaed Nvidia over ex-CEO's China ties."),
    ("21 · DENMARK", "Two Danes charged over a Russian plot to kill a Ukrainian rapper."),
    ("22 · KOREA", "Trump said he was too busy to see Kim Jong-un on his Asia trip."),
    ("23 · IRAN WAR COST", "US campaign against Iran has cost $48.3bn, Pentagon said."),
    ("24 · UKRAINE WAR", "Russian troop losses put at 1.6 million since the invasion."),
    ("25 · WASHINGTON", "A second judge blocked Trump's triumphal arch as a 'rushed job'."),
    ("26 · INDIA", "Modi called for dialogue and trust at the SCO civilizational conference."),
    ("27 · BRAZIL", "Leader advanced legal protection of Indigenous land with chief Raoni."),
    ("28 · BERLIN", "Students marched against rearmament and mandatory service."),
    ("29 · BRUSSELS", "EU Council put up 1 billion euros in military aid for Ukraine."),
    ("30 · ARGENTINA", "Argentina's bonds fell into distress as markets sold off."),
    ("31 · MARKETS", "Sensex rose 2.3% while Brent crude held near $90."),
    ("32 · BRAZIL", "The real is down 18% against the dollar over the month."),
    ("33 · JAPAN", "Japan's inflation rose as the Nikkei slid."),
]

NUMBERS = [
    ("3", "WEAPONS INTO POLAND"),
    ("370,000", "EVACUATED BEFORE AKVAN"),
    ("-3.7%", "S&P 500 ON FRIDAY"),
    ("41", "KILLED IN HODEIDAH, HOUTHIS SAY"),
    ("1 IN 12", "TUMOURS UNDETECTABLE"),
    ("17 MO", "THACI'S SENTENCE"),
]


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx, cw = 28, W - 56

    # Masthead
    title_f = font(SERIF, 46)
    d.text((mx, 14), "THE WORLD TODAY", font=title_f, fill=INK)
    rf = font(SANS_B, 15)
    d.text((W - mx - d.textlength("SATURDAY", font=rf), 18), "SATURDAY",
           font=rf, fill=RED)
    df = font(SANS_B, 15)
    d.text((W - mx - d.textlength("21 NOVEMBER 2026", font=df), 38),
           "21 NOVEMBER 2026", font=df, fill=INK)
    d.text((W - mx - d.textlength("33 STORIES", font=font(SANS_B, 10)), 60),
           "33 STORIES", font=font(SANS_B, 10), fill=SOFT)
    hline(d, mx, W - mx, 84, width=3)
    hline(d, mx, W - mx, 88, width=1)
    kf = font(SANS_B, 11)
    kick = "33 STORIES  ·  SIX CONTINENTS  ·  ALL FROM THIS ONE DAY"
    d.text(((W - d.textlength(kick, font=kf)) / 2, 96), kick, font=kf, fill=INK)

    # Big-number strip
    y = 120
    cell_w = (cw - 5 * 6) // 6
    for i, (num, label) in enumerate(NUMBERS):
        x = mx + i * (cell_w + 6)
        box(d, x, y, cell_w, 60, outline=RULE, fill=PANEL)
        nf = font(SANS_B, 24 if len(num) <= 7 else 20)
        d.text((x + 8, y + 4), num, font=nf, fill=RED)
        para(d, x + 8, y + 33, label, font(SANS, 8), cell_w - 14, 10,
             color=SOFT, max_lines=2)

    # Region counts
    rf2 = font(SANS_B, 10)
    regions = "ASIA 9  ·  EUROPE 8  ·  MIDDLE EAST 4  ·  AMERICAS 7  ·  AFRICA 1  ·  GLOBAL 4"
    d.text(((W - d.textlength(regions, font=rf2)) / 2, 188), regions, font=rf2,
           fill=SOFT)

    # Three features
    y = 206
    fw = (cw - 20) // 3
    fh = 228
    for i, (kick_t, head, body, src, art) in enumerate(FEATURES):
        x = mx + i * (fw + 10)
        box(d, x, y, fw, fh, outline=RULE, fill=PANEL)
        art(d, x + 1, y + 1, fw - 2, 96)
        yy = y + 104
        yy = kicker(d, x + 8, yy, kick_t)
        yy = para(d, x + 8, yy, head, font(SANS_B, 14), fw - 16, 17,
                  max_lines=2)
        yy = para(d, x + 8, yy + 2, body, font(SANS, 10), fw - 16, 13,
                  max_lines=4)
        d.text((x + 8, y + fh - 16), "Source: " + src, font=font(SANS, 8),
               fill=SOFT)

    # Ten small stories, 5 x 2
    y = 442
    sw = (cw - 4 * 8) // 5
    sh = 108
    for i, (kick_t, head, body, src, art) in enumerate(SMALLS):
        col, row = i % 5, i // 5
        x = mx + col * (sw + 8)
        yy = y + row * (sh + 8)
        box(d, x, yy, sw, sh, outline=RULE, fill=PANEL)
        art(d, x + 1, yy + 1, sw - 2, 40)
        ty = yy + 44
        ty = para(d, x + 6, ty, head, font(SANS_B, 10), sw - 12, 12,
                  max_lines=2)
        para(d, x + 6, ty + 1, body, font(SANS, 9), sw - 12, 11, max_lines=3)

    # Map band
    y = 674
    mf = font(SANS_B, 11)
    d.text((mx, y), "WHERE IT HAPPENED — STORIES 1–13 ON THE MAP", font=mf, fill=INK)
    draw_map(d, mx, y + 18, cw, 120)

    # Briefs
    y = 820
    d.text((mx, y), "ALSO ON SATURDAY — 14–33", font=mf, fill=INK)
    bf = font(SANS, 10)
    col_w = (cw - 16) // 2
    for i, (tag, text) in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x = mx + col * (col_w + 16)
        yy = y + 18 + row * 13
        d.text((x, yy), tag + " — " + text, font=bf, fill=INK)

    # Footer: DATE CHECK
    y = 972
    d.rectangle([mx, y, W - mx, y + 34], fill=INK)
    ff = font(SANS_B, 10)
    d.text((mx + 8, y + 4),
           "DATE CHECK \u2713 — Stories 1–11 and 13–33 happened or were first reported Fri 20 – Sat 21 Nov 2026.",
           font=ff, fill=(255, 255, 255))
    d.text((mx + 8, y + 19),
           "No. 12 is a Thu 19 Nov follow-up. Left out: Crimea Bridge damage (17 Nov); unverified social-media claims of a North Korean launch — no credible source.",
           font=font(SANS, 9), fill=(220, 220, 220))
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
