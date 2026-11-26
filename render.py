#!/usr/bin/env python3
"""news-image-20261125 v9 — draws entry.png (1024x1024, <=1 MiB).

31 stories: 3 heroes + 10 mids + 18 list items, all first reported on
Wednesday 25 November 2026. Flat vector illustration drawn in code with PIL.
No photos, no copied art. Run: python3 render.py  ->  writes entry.png
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (15, 42, 74)
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (185, 28, 28)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

REGION = {
    "Europe": (37, 99, 235),
    "Asia": (220, 38, 38),
    "N. America": (5, 150, 105),
    "Mideast": (217, 119, 6),
    "Africa": (124, 58, 237),
    "Oceania": (8, 145, 178),
    "Latin Am": (219, 39, 119),
    "World": (71, 85, 105),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, path, text, start, max_w):
    """Largest size <= start whose text fits max_w."""
    size = start
    while size > 10 and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def para(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines at x,y; returns y after last line."""
    if leading is None:
        leading = fnt.size + 2
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, label, colour):
    f = font(SANS_B, 11)
    w = int(draw.textlength(label, font=f)) + 14
    draw.rounded_rectangle([x, y, x + w, y + 18], radius=9, fill=colour)
    draw.text((x + 7, y + 3), label, font=f, fill=WHITE)
    return w


def kicker_bar(draw, x, y, w, label, colour):
    f = font(SANS_B, 10)
    draw.rectangle([x, y, x + w, y + 15], fill=colour)
    draw.text((x + 5, y + 2), label, font=f, fill=WHITE)

# ---------------------------------------------------------------- heroes
# Every hero illustration fills >=55% of its box; labels/numbers are drawn
# INSIDE the art. All drawing stays inside (x, y, w, h).
def hero_tariffs(d, x, y, w, h):
    """Container ship with a 2x3 tariff table inside the art."""
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 235))
    d.ellipse([x + w - 50, y + 2, x + w - 16, y + 26], fill=(251, 191, 36))
    for cx in (x + 176, x + 220):
        d.ellipse([cx, y + 8, cx + 36, y + 20], fill=(255, 255, 255))
    # sea (bottom strip) then hull over it
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(30, 90, 140))
    for sx in range(x + 8, x + w - 10, 46):
        d.line([sx, y + h - 14, sx + 22, y + h - 14], fill=(255, 255, 255), width=2)
    # ceiling label, top-left
    d.rectangle([x + 8, y + 6, x + 168, y + 28], fill=(15, 42, 74))
    d.text((x + 13, y + 10), "UP TO 35% · 14 ECONOMIES",
           font=font(SANS_B, 10), fill=(251, 191, 36))
    # containers: 2 rows x 3, labels inside
    cols = [(220, 38, 38), (37, 99, 235), (5, 150, 105),
            (217, 119, 6), (124, 58, 237), (8, 145, 178)]
    labels = ["CHINA 20%", "INDIA 25%", "EU 15%",
              "VIETNAM 35%", "JAPAN 15%", "KOREA 15%"]
    cw = (w - 24) // 3
    for r in range(2):
        for c in range(3):
            i = r * 3 + c
            cx = x + 12 + c * cw
            cy = y + 32 + r * 24
            d.rectangle([cx + 1, cy, cx + cw - 1, cy + 22], fill=cols[i])
            d.text((cx + 5, cy + 5), labels[i], font=font(SANS_B, 10), fill=WHITE)
    # hull
    d.polygon([(x + 10, y + 80), (x + w - 10, y + 80),
               (x + w - 30, y + 106), (x + 30, y + 106)], fill=(15, 42, 74))
    d.rectangle([x + 10, y + 80, x + w - 10, y + 85], fill=(185, 28, 28))


def hero_kospi(d, x, y, w, h):
    """Dark trading screen: plunging Kospi line, tickers inside the art."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 32))
    for gy in range(y + 34, y + h - 8, 20):
        d.line([x + 8, gy, x + w - 8, gy], fill=(40, 60, 90), width=1)
    for gx in range(x + 8, x + w - 8, 40):
        d.line([gx, y + 30, gx, y + h - 8], fill=(40, 60, 90), width=1)
    d.text((x + 12, y + 6), "KOSPI", font=font(SANS_B, 13), fill=WHITE)
    d.text((x + w - 104, y + 6), "4,697.51", font=font(SANS_B, 13), fill=(251, 191, 36))
    d.rectangle([x + w - 96, y + 26, x + w - 10, y + 44], fill=(239, 68, 68))
    d.text((x + w - 90, y + 29), "AI DOUBTS", font=font(SANS_B, 10), fill=WHITE)
    pts = [(x + 14, y + 44), (x + 62, y + 52), (x + 110, y + 48),
           (x + 158, y + 68), (x + 206, y + 74), (x + 254, y + 92),
           (x + w - 16, y + h - 30)]
    d.line(pts, fill=(239, 68, 68), width=4, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255))
    d.text((x + 12, y + h - 46), "-6.2%", font=font(SANS_B, 28), fill=(239, 68, 68))
    d.text((x + 116, y + h - 40), "SK HYNIX -11.1%", font=font(SANS_B, 11), fill=WHITE)
    d.text((x + 116, y + h - 24), "SAMSUNG -9.9%  ·  TAIEX -4.8%",
           font=font(SANS_B, 10), fill=(200, 200, 200))


def hero_shenzhou(d, x, y, w, h):
    """Night launch: rocket, Tiangong station, flags, times inside the art."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 12, 28))
    rnd = random.Random(25)
    for _ in range(40):
        sx = x + rnd.randint(4, w - 4)
        sy = y + rnd.randint(4, h - 30)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # earth: bottom sliver only, stays inside the box
    d.chord([x, y + h - 84, x + w, y + h], 0, 180, fill=(37, 99, 235))
    d.arc([x, y + h - 84, x + w, y + h], 0, 180, fill=(147, 197, 253), width=2)
    d.text((x + 12, y + 6), "SHENZHOU-24", font=font(SANS_B, 13), fill=WHITE)
    # flags PK + CN, top-right
    d.rectangle([x + w - 66, y + 6, x + w - 40, y + 22], fill=(20, 90, 50))
    d.text((x + w - 60, y + 8), "PK", font=font(SANS_B, 10), fill=WHITE)
    d.rectangle([x + w - 36, y + 6, x + w - 10, y + 22], fill=(220, 38, 38))
    d.text((x + w - 30, y + 8), "CN", font=font(SANS_B, 10), fill=WHITE)
    # rocket (left)
    rx = x + 44
    d.polygon([(rx, y + 26), (rx + 12, y + 14), (rx + 24, y + 26)], fill=(220, 38, 38))
    d.rectangle([rx, y + 26, rx + 24, y + 76], fill=(255, 255, 255))
    d.rectangle([rx, y + 44, rx + 24, y + 54], fill=(220, 38, 38))
    d.polygon([(rx - 8, y + 76), (rx, y + 62), (rx, y + 76)], fill=(185, 28, 28))
    d.polygon([(rx + 24, y + 76), (rx + 32, y + 76), (rx + 24, y + 62)], fill=(185, 28, 28))
    d.polygon([(rx + 4, y + 76), (rx + 12, y + 94), (rx + 20, y + 76)], fill=(251, 191, 36))
    d.text((rx - 8, y + 96), "LONG MARCH 2F", font=font(SANS_B, 9), fill=WHITE)
    # station (right): modules + solar panels
    sx = x + 128
    d.rectangle([sx, y + 30, sx + 34, y + 48], fill=(200, 210, 220))
    d.rectangle([sx + 34, y + 24, sx + 78, y + 54], fill=(230, 235, 240))
    d.rectangle([sx + 78, y + 30, sx + 104, y + 48], fill=(200, 210, 220))
    d.rectangle([sx - 26, y + 34, sx, y + 44], fill=(37, 99, 235))
    d.rectangle([sx + 104, y + 34, sx + 130, y + 44], fill=(37, 99, 235))
    d.text((sx - 6, y + 58), "TIANGONG", font=font(SANS_B, 11), fill=WHITE)
    d.text((x + 128, y + 74), "1ST PAKISTANI IN SPACE",
           font=font(SANS_B, 12), fill=(251, 191, 36))
    d.rectangle([x + w - 150, y + h - 22, x + w - 8, y + h - 4], fill=(15, 42, 74))
    d.text((x + w - 145, y + h - 19), "LAUNCH 00:18 · DOCK 03:56",
           font=font(SANS_B, 9), fill=(251, 191, 36))

# ---------------------------------------------------------------- mid banners
# Each banner is ~45% of its card: a real scene in the top zone + ONE big
# label line at the bottom, drawn INSIDE the art. Never a thin strip.

def mid_dhaka(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 148, 136))
    for i, c in enumerate([(251, 191, 36), (220, 38, 38), (255, 255, 255)]):
        d.rectangle([x + 12 + i * 30, y + 6, x + 34 + i * 30, y + 26], fill=c)
    d.rectangle([x + 116, y + 8, x + 168, y + 16], fill=(15, 42, 74))
    d.rectangle([x + 116, y + 8, x + 124, y + 26], fill=(15, 42, 74))
    d.rectangle([x + 112, y + 26, x + 176, y + 30], fill=(15, 42, 74))
    d.text((x + 8, y + h - 22), "Tk17,000 (+36%)",
           font=font(SANS_B, 13), fill=WHITE)


def mid_farmgate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 64, 40))
    for i in range(5):
        cx = x + 14 + i * 24
        d.rectangle([cx, y + 8, cx + 11, y + 28], fill=(232, 220, 190))
    d.polygon([(x + 8, y + 8), (x + w // 2, y + 0), (x + w - 8, y + 8)],
              fill=(185, 28, 28))
    d.line([x + 158, y + 8, x + 158, y + 28], fill=(251, 191, 36), width=3)
    d.line([x + 144, y + 10, x + 172, y + 10], fill=(251, 191, 36), width=3)
    d.polygon([(x + 139, y + 16), (x + 149, y + 16), (x + 144, y + 24)], fill=(251, 191, 36))
    d.polygon([(x + 167, y + 16), (x + 177, y + 16), (x + 172, y + 24)], fill=(251, 191, 36))
    d.text((x + 8, y + h - 22), "CASE SET ASIDE", font=font(SANS_B, 14), fill=WHITE)


def mid_ofgem(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(76, 29, 149))
    d.polygon([(x + 12, y + 24), (x + 38, y + 6), (x + 64, y + 24)], fill=(251, 191, 36))
    d.rectangle([x + 18, y + 24, x + 58, y + 32], fill=(255, 255, 255))
    d.polygon([(x + 96, y + 4), (x + 82, y + 22), (x + 92, y + 22),
               (x + 84, y + 34), (x + 104, y + 14), (x + 94, y + 14)],
              fill=(251, 191, 36))
    d.text((x + 112, y + 4), "£2,166", font=font(SANS_B, 20), fill=WHITE)
    d.text((x + 108, y + h - 20), "+26% FROM JAN", font=font(SANS_B, 9),
           fill=(251, 191, 36))


def mid_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(154, 52, 18))
    for i, bh in enumerate([14, 20, 12, 17]):
        bx = x + 118 + i * 20
        d.rectangle([bx, y + 28 - bh, bx + 17, y + 28], fill=(60, 20, 10))
        d.rectangle([bx + 4, y + 28 - bh + 3, bx + 8, y + 28 - bh + 7],
                    fill=(251, 191, 36))
    d.ellipse([x + 96, y + 2, x + 122, y + 18], fill=(120, 120, 120))
    d.text((x + 8, y + 2), "SECURITY CHIEF", font=font(SANS_B, 12), fill=WHITE)
    d.text((x + 8, y + h - 22), "KILLED + FAMILY", font=font(SANS_B, 14),
           fill=(251, 191, 36))


def mid_ras(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 40, 66))
    d.rectangle([x + 12, y + 12, x + 24, y + 30], fill=(180, 190, 200))
    d.rectangle([x + 30, y + 18, x + 42, y + 30], fill=(150, 160, 170))
    d.ellipse([x + 48, y + 16, x + 76, y + 30], fill=(220, 225, 230))
    for dx in (96, 122, 148):
        d.ellipse([x + dx, y + 6, x + dx + 14, y + 18], fill=(255, 255, 255))
        d.line([x + dx - 2, y + 4, x + dx + 16, y + 20], fill=(239, 68, 68), width=3)
        d.line([x + dx + 16, y + 4, x + dx - 2, y + 20], fill=(239, 68, 68), width=3)
    d.text((x + 8, y + h - 22), "4 DRONES DOWN", font=font(SANS_B, 14), fill=WHITE)
    d.text((x + 118, y + h - 20), "NO CASUALTIES", font=font(SANS_B, 7),
           fill=(251, 191, 36))


def mid_solomons(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 110, 140))
    d.line([x + 20, y + 4, x + 20, y + 28], fill=(255, 255, 255), width=2)
    d.rectangle([x + 20, y + 4, x + 54, y + 20], fill=(0, 40, 120))
    d.text((x + 24, y + 6), "AU", font=font(SANS_B, 10), fill=WHITE)
    d.line([x + 66, y + 4, x + 66, y + 28], fill=(255, 255, 255), width=2)
    d.rectangle([x + 66, y + 4, x + 100, y + 20], fill=(0, 90, 50))
    d.text((x + 70, y + 6), "SB", font=font(SANS_B, 10), fill=WHITE)
    d.text((x + 104, y + 4), "A$740m", font=font(SANS_B, 15), fill=WHITE)
    d.text((x + 110, y + h - 20), "10-YEAR TREATY", font=font(SANS_B, 9),
           fill=(251, 191, 36))
    for wx in range(x + 4, x + w - 10, 24):
        d.arc([wx, y + h - 12, wx + 22, y + h], 180, 360, fill=WHITE, width=2)


def mid_netanyahu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(68, 64, 60))
    d.rectangle([x + 16, y + 8, x + 62, y + 18], fill=(160, 110, 60))
    d.rectangle([x + 52, y + 18, x + 60, y + 28], fill=(120, 80, 40))
    d.rectangle([x + 10, y + 28, x + 120, y + 31], fill=(200, 190, 170))
    d.line([x + 150, y + 6, x + 150, y + 26], fill=(251, 191, 36), width=3)
    d.line([x + 136, y + 8, x + 164, y + 8], fill=(251, 191, 36), width=3)
    d.text((x + 8, y + h - 22), "DROP BRIBERY CHARGE", font=font(SANS_B, 13),
           fill=WHITE)


def mid_zap(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 24, 40))
    for tx in (16, 48):
        d.polygon([(x + tx, y + 6), (x + tx + 24, y + 6),
                   (x + tx + 20, y + 30), (x + tx + 4, y + 30)],
                  fill=(120, 125, 135))
    d.line([x + 100, y + 6, x + 100, y + 30], fill=(200, 200, 200), width=2)
    d.line([x + 88, y + 10, x + 112, y + 10], fill=(200, 200, 200), width=2)
    d.line([x + 112, y + 10, x + 140, y + 6], fill=(239, 68, 68), width=2)
    d.line([x + 140, y + 6, x + 146, y + 14], fill=(239, 68, 68), width=2)
    d.text((x + 8, y + h - 22), "17TH POWER LOSS", font=font(SANS_B, 14),
           fill=(251, 191, 36))


def mid_cairo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 26))
    d.rectangle([x + 12, y + 6, x + 62, y + 18], fill=(200, 200, 200))
    d.ellipse([x + 20, y + 18, x + 30, y + 26], fill=(40, 40, 40))
    d.ellipse([x + 46, y + 18, x + 56, y + 26], fill=(40, 40, 40))
    d.polygon([(x + 22, y + 6), (x + 30, y - 2), (x + 40, y + 2),
               (x + 48, y - 2), (x + 54, y + 6)], fill=(249, 115, 22))
    d.rectangle([x + 76, y + 10, x + 106, y + 20], fill=(37, 99, 235))
    d.rectangle([x + 116, y + 10, x + 146, y + 20], fill=(220, 38, 38))
    d.text((x + 8, y + h - 24), "31 DEAD", font=font(SANS_B, 20), fill=WHITE)
    d.text((x + 100, y + h - 20), "TANKER FIRE", font=font(SANS_B, 10),
           fill=(251, 191, 36))


def mid_java(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(92, 52, 20))
    d.line([x + 30, y + 4, x + 30, y + 30], fill=(40, 25, 10), width=5)
    d.line([x + 58, y + 4, x + 58, y + 30], fill=(40, 25, 10), width=5)
    d.polygon([(x + 22, y + 4), (x + 44, y - 2), (x + 66, y + 4)], fill=(60, 35, 15))
    d.rectangle([x + 32, y + 24, x + 56, y + 30], fill=(37, 99, 235))
    d.ellipse([x + 80, y + 6, x + 112, y + 24], fill=(251, 191, 36))
    d.polygon([(x + 80, y + 20), (x + 112, y + 20), (x + 96, y + 28)], fill=(251, 191, 36))
    d.text((x + 112, y + 4), "9 DEAD", font=font(SANS_B, 14), fill=WHITE)
    d.text((x + 112, y + h - 20), "17 TRAPPED", font=font(SANS_B, 9),
           fill=(251, 191, 36))

# ---------------------------------------------------------------- data
# (num, region, kicker, dateline, headline, body, why, source, badge, art)
HEROES = [
    (1, "N. America", "TOP STORY", "WASHINGTON · TRADE",
     "US proposes tariffs on 14 economies",
     "China 20%, India 25% (17% if deal), Vietnam 35% (20% if deal), EU 15%.",
     "WHY IT MATTERS: Biggest US tariff move of the year.",
     "Reuters · USTR", "OFFICIAL", hero_tariffs),
    (2, "Asia", "MARKETS", "SEOUL · TOKYO · TAIPEI",
     "AI doubts sink Asian chip stocks; Kospi -6.2%",
     "Kospi 4,697.51; SK Hynix -11.1%, Samsung -9.9%; Taiex -4.8%, Nikkei -2.8%.",
     "WHY IT MATTERS: AI-spending doubt hits chip stocks.",
     "AP · Barchart", "REPORTED", hero_kospi),
    (3, "Asia", "SPACE", "JIUQUAN, CHINA · SPACE",
     "Pakistan's first astronaut docks at China's space station",
     "Launched 00:18 UTC, docked 03:56; Muhammad Zeeshan Ali, 40, first "
     "foreigner aboard.",
     "WHY IT MATTERS: First foreigner aboard Tiangong.",
     "Reuters · Xinhua", "OFFICIAL", hero_shenzhou),
]

# (num, region, dateline, headline, body, source, badge, art)
MIDS = [
    (4, "Asia", "DHAKA · LABOUR", "Garment workers offered 36% pay rise",
     "Wage board: Tk12,500 to Tk17,000 a month; effective Dec, paid Jan.",
     "TBS", "REPORTED", mid_dhaka),
    (5, "Africa", "CAPE TOWN · JUSTICE", "Ramaphosa wins Farmgate case",
     "High Court sets aside the 2022 panel report; impeachment falls away.",
     "RTR", "OFFICIAL", mid_farmgate),
    (6, "Europe", "LONDON · ENERGY", "UK energy price cap rises 26% in January",
     "Typical bill £1,723 to £2,166 a year from 1 Jan; ~20m households hit.",
     "Ofgem", "OFFICIAL", mid_ofgem),
    (7, "Mideast", "GAZA CITY · WAR", "Strike kills Hamas security chief, family",
     "Abuelouf, 47, Hamas security chief in north Gaza, dies with his family.",
     "RTR", "REPORTED", mid_gaza),
    (8, "Mideast", "RAS TANURA · WAR", "Saudis down 4 Houthi drones over refinery",
     "Air defences destroy four drones over the kingdom's largest refinery.",
     "RTR", "REPORTED", mid_ras),
    (9, "Oceania", "CANBERRA · DIPLOMACY", "Solomons sign security treaty",
     "A$740m over 10 years; Australia is primary security partner; no base.",
     "PM", "OFFICIAL", mid_solomons),
    (10, "Mideast", "JERUSALEM · JUSTICE", "Netanyahu trial: judges urge dropping charge",
     "Judges urge prosecutors to drop the Case 4000 bribery charge.",
     "RTR", "REPORTED", mid_netanyahu),
    (11, "Europe", "KYIV · WAR", "Zaporizhzhia plant loses power, 17th time",
     "Shelling cuts the only external line at 04:28; power out in 5 regions.",
     "RTR", "OFFICIAL", mid_zap),
    (12, "Africa", "CAIRO · DISASTER", "Fuel-tanker fire kills 31 near Cairo",
     "Tanker overturns and explodes on the ring road; 27+ cars burn.",
     "AFP", "REPORTED", mid_cairo),
    (13, "Asia", "BOGOR, JAVA · DISASTER", "9 dead, 17 trapped in flooded gold pit",
     "Flood in a 100-metre shaft at Pongkor; rescuers pull bodies out.",
     "AP", "REPORTED", mid_java),
]

# (num, region, city, fragment, badge, source)
LIST = [
    (14, "Mideast", "Hormuz", "Iran says mines set two tankers ablaze", "CL", "RTR"),
    (15, "N. America", "Washington", "FinCEN probes breach after CIA hack", "R", "Bleep."),
    (16, "Africa", "Damazin", "RSF drones kill 19 in Blue Nile", "R", "RTR"),
    (17, "Latin Am", "Cartagena", "Police free ~20 hostages, 1 captor killed", "R", "AP"),
    (18, "Europe", "Brussels", "EU-Balkans summit held, Serbia absent", "O", "EC"),
    (19, "Europe", "Brussels", "EU proposes \u20ac50bn quantum fund", "O", "RTR"),
    (20, "Oceania", "Canberra", "Australia CPI jumps to 4.9%", "O", "ABS"),
    (21, "N. America", "Iowa", "Army detonates 5 tons of lead azide", "O", "US Army"),
    (22, "Asia", "Seoul", "Bithumb breach widens to 19 data types", "O", "Bithumb"),
    (23, "Asia", "Karachi", "Building collapse kills 3, hurts 14", "R", "AP"),
    (24, "Latin Am", "Paran\u00e1", "Storms kill 6, affect ~10,000", "R", "Civil Def."),
    (25, "Europe", "London", "Met still institutionally racist, review finds", "O", "Review"),
    (26, "Europe", "London", "Eurostar strike cancels 8 trains", "R", "BBC"),
    (27, "Asia", "Pyongyang", "N. Korea expels Swiss envoy", "O", "KCNA"),
    (28, "World", "San Francisco", "GPT-6.2 reaches Copilot", "R", "Microsoft"),
    (29, "World", "Vatican", "Pope Leo laments COP31 collapse", "O", "RTR"),
    (30, "N. America", "Washington", "US PCE inflation hits 3.8%", "O", "BEA"),
    (31, "N. America", "Washington", "US GDP revised up to +4.3%", "O", "BEA"),
]

REGIONS = [("Europe", 6), ("Asia", 7), ("N. America", 5), ("Mideast", 4),
           ("Africa", 3), ("Oceania", 2), ("Latin Am", 2), ("World", 2)]

NUMBERS = [
    ("-6.2%", "Kospi close, worst in AI sell-off"),
    ("20%", "proposed tariff on China"),
    ("31", "dead in Cairo tanker fire"),
    ("+36%", "Bangladesh garment wage"),
    ("\u00a32,166", "Ofgem cap from January"),
    ("1st", "Pakistani in space"),
]

TIMELINE = [
    ("00:18", "Shenzhou launches"),
    ("03:56", "Tiangong docks"),
    ("~04:00", "Gaza strike"),
    ("04:28", "Zaporizhzhia out"),
    ("06:30", "Cartagena rescue"),
    ("13:30", "PCE +3.8%, GDP +4.3%"),
    ("15:00", "Iowa blast done"),
]

# map pins: story num -> (lon, lat, display dx, display dy) in px
PINS = {1: (-77, 39, 0, 0), 2: (127, 37, 0, 0), 3: (99, 40, 0, 0),
        4: (90, 24, 0, 0), 5: (18, -34, 0, 0), 6: (0, 51, 0, 0),
        7: (34, 31, 18, -10), 8: (50, 26, 0, 0), 9: (149, -35, 0, 0),
        10: (35, 32, -16, 12), 11: (35, 48, 0, 0), 12: (31, 30, -20, -2),
        13: (107, -6, 0, 0)}

DATE_LEFT = ("Dow 50,018.70 (Tue 24) \u00b7 Huawei verdict (Tue 24) \u00b7 "
             "Riyadh tower strike, 11 hurt (Tue 24) \u00b7 Chen Jining probe "
             "(Tue 24) \u00b7 CIA\u2013ODNI breach first reported (Tue 24) \u00b7 "
             "UN femicide report (Tue 24) \u00b7 Nvidia reinstates Huang "
             "(Mon 23) \u00b7 COP31 collapse (Sun 22) \u00b7 Nepal quake "
             "(Tue 24) \u00b7 Miss Universe crowned (Tue 24) \u00b7 "
             "Saudi-led strike on Hodeidah (Tue 24) \u00b7 Sinner's knee "
             "surgery (Tue 24).")
DATE_NOTYET = ("US Thanksgiving (Thu 26 Nov) \u00b7 Argentina 2027 budget "
               "vote (Thu 26 Nov)")

# ---------------------------------------------------------------- compose
def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 12  # margin

    # 1. top bar
    d.rectangle([0, 0, W, 20], fill=NAVY)
    text(d, (W // 2, 4),
         "THE WORLD IN ONE DAY  \u00b7  31 STORIES  \u00b7  8 REGIONS  \u00b7  "
         "15 FIELDS  \u00b7  ALL FIRST REPORTED ON WEDNESDAY 25 NOVEMBER 2026",
         font(SANS_B, 11), fill=WHITE, anchor="ma")

    # 2. masthead (auto-fit so it never clips)
    mf = fit_font(d, SERIF, "Wednesday 25 November 2026", 62, W - 2 * mx)
    text(d, (mx, 22), "Wednesday 25 November 2026", mf, fill=NAVY)

    # 3. lede
    text(d, (mx, 86),
         "US proposes tariffs on 14 economies \u00b7 AI doubts sink Asian chip "
         "stocks \u00b7 Pakistan's first astronaut docks at Tiangong",
         font(SERIF_IT, 20), fill=RED)

    # 4. region strip
    x = mx
    y = 112
    for name, n in REGIONS:
        x += chip(d, x, y, f"{name} {n}", REGION[name]) + 6

    # 5. number strip
    y = 136
    bw = (W - 2 * mx - 5 * 6) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        bx = mx + i * (bw + 6)
        d.rectangle([bx, y, bx + bw, y + 44], outline=NAVY, width=1)
        d.rectangle([bx, y, bx + bw, y + 4], fill=NAVY)
        text(d, (bx + 8, y + 8), num, font(SANS_B, 22), fill=RED)
        lf = font(SANS, 10)
        while d.textlength(lab, font=lf) > bw - 12 and lf.size > 8:
            lf = font(SANS, lf.size - 1)
        d.text((bx + 8, y + 31), lab, font=lf, fill=GREY)

    # 6. timeline (short labels, 9px, fits the width)
    y = 186
    d.rectangle([mx, y, W - mx, y + 18], fill=NAVY)
    tx = mx + 6
    d.text((tx, y + 4), "THE DAY IN UTC", font=font(SANS_B, 9), fill=(251, 191, 36))
    tx += int(d.textlength("THE DAY IN UTC", font=font(SANS_B, 9))) + 12
    for t, ev in TIMELINE:
        d.text((tx, y + 4), t, font=font(SANS_B, 9), fill=(251, 191, 36))
        tx += int(d.textlength(t + " ", font=font(SANS_B, 9)))
        d.text((tx, y + 4), ev, font=font(SANS, 9), fill=WHITE)
        tx += int(d.textlength(ev, font=font(SANS, 9))) + 14

    # 7. heroes
    hy, hh = 206, 236
    hw = (W - 2 * mx - 2 * 8) // 3
    for i, (num, region, kick, date, head, body, why, src, bdg, art) in enumerate(HEROES):
        hx = mx + i * (hw + 8)
        d.rectangle([hx, hy, hx + hw, hy + hh], outline=NAVY, width=1)
        kicker_bar(d, hx, hy, hw, kick, REGION[region])
        d.ellipse([hx + hw - 26, hy + 20, hx + hw - 4, hy + 42], fill=RED)
        d.text((hx + hw - 15, hy + 25), str(num), font=font(SANS_B, 13),
               fill=WHITE, anchor="ma")
        art_h = 118  # 50% of box + kicker = ~57% of the box area
        art(d, hx + 1, hy + 16, hw - 2, art_h)
        ty = hy + 16 + art_h + 4
        d.text((hx + 6, ty), date, font=font(SANS_B, 9), fill=GREY)
        d.text((hx + hw - 6, ty), bdg, font=font(SANS_B, 9),
               fill=REGION[region] if bdg == "OFFICIAL" else RED, anchor="ra")
        ty += 13
        ty = para(d, hx + 6, ty, wrap(d, head, font(SERIF, 18), hw - 12),
                  font(SERIF, 18), leading=19)
        ty = para(d, hx + 6, ty + 1, wrap(d, body, font(SANS, 10), hw - 12),
                  font(SANS, 10), leading=12)
        d.text((hx + 6, ty + 1), why, font=font(SANS, 9), fill=GREY)
        d.text((hx + hw - 6, ty + 1), f"({src})", font=font(SANS, 9),
               fill=GREY, anchor="ra")

    # 8. mids — 2 rows of 5
    my, mh = 448, 118
    mw = (W - 2 * mx - 4 * 6) // 5
    for i, (num, region, date, head, body, src, bdg, art) in enumerate(MIDS):
        row, col = divmod(i, 5)
        x = mx + col * (mw + 6)
        yy = my + row * (mh + 6)
        d.rectangle([x, yy, x + mw, yy + mh], outline=NAVY, width=1)
        bh = 46  # 39% of card + banner label inside the art
        art(d, x + 1, yy + 1, mw - 2, bh)
        d.ellipse([x + mw - 22, yy + 4, x + mw - 4, yy + 22], fill=RED)
        d.text((x + mw - 13, yy + 8), str(num), font=font(SANS_B, 11),
               fill=WHITE, anchor="ma")
        ty = yy + bh + 3
        d.text((x + 5, ty), f"{date} · {src}", font=font(SANS_B, 7), fill=GREY)
        d.text((x + mw - 5, ty), bdg, font=font(SANS_B, 8),
               fill=REGION[region] if bdg == "OFFICIAL" else RED, anchor="ra")
        ty += 11
        ty = para(d, x + 5, ty, wrap(d, head, font(SERIF, 13), mw - 10)[:2],
                  font(SERIF, 13), leading=14)
        para(d, x + 5, ty, wrap(d, body, font(SANS, 9), mw - 10)[:2],
             font(SANS, 9), leading=10)

    # 9. map (bottom-left) + 10. list (bottom-right)
    by = 696
    map_x0, map_y0, map_w, map_h = mx, by, 288, 190
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                outline=NAVY, width=1)
    d.text((map_x0 + 6, map_y0 + 4), "WHERE IT HAPPENED",
           font=font(SANS_B, 12), fill=NAVY)
    d.text((map_x0 + 6, map_y0 + 20), "pins = story numbers",
           font=font(SANS, 9), fill=GREY)

    def lonlat(lon, lat):
        px = map_x0 + 10 + (lon + 170) / 360 * (map_w - 20)
        py = map_y0 + 34 + (75 - lat) / 130 * (map_h - 52)
        return px, py

    continents = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 60),
         (-55, 47), (-70, 42), (-80, 32), (-90, 21), (-105, 20), (-120, 34),
         (-125, 49), (-150, 60), (-168, 66)],
        [(-10, 37), (0, 43), (10, 45), (20, 45), (30, 46), (40, 42),
         (35, 36), (28, 36), (20, 40), (10, 38), (0, 36), (-10, 37)],
        [(60, 70), (90, 75), (130, 72), (160, 66), (180, 65), (160, 60),
         (140, 40), (127, 35), (120, 25), (105, 10), (95, 8), (80, 8),
         (75, 20), (60, 25), (50, 30), (45, 40), (55, 55), (60, 70)],
        [(-18, 35), (-10, 31), (0, 35), (10, 37), (20, 32), (30, 31),
         (35, 28), (43, 12), (51, 11), (48, -5), (40, -15), (35, -25),
         (28, -33), (18, -35), (15, -25), (12, -10), (9, 0), (-5, 5),
         (-15, 12), (-18, 35)],
        [(113, -22), (130, -12), (142, -11), (150, -20), (153, -27),
         (150, -37), (140, -38), (130, -32), (115, -32), (113, -22)],
    ]
    for poly in continents:
        d.polygon([lonlat(lo, la) for lo, la in poly], fill=(214, 205, 180),
                  outline=(150, 140, 120))
    allstories = {h[0]: h[1] for h in HEROES}
    allstories.update({m[0]: m[1] for m in MIDS})
    for num, (lon, lat, dx, dy) in PINS.items():
        px, py = lonlat(lon, lat)
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=REGION[allstories[num]],
                  outline=WHITE, width=1)
        d.text((px, py - 6), str(num), font=font(SANS_B, 9), fill=WHITE, anchor="ma")
    d.text((map_x0 + 6, map_y0 + map_h - 14),
           "Europe 6 · Asia 7 · N. America 5 · Mideast 4",
           font=font(SANS, 9), fill=GREY)

    # list
    lx, lw = map_x0 + map_w + 10, W - mx - (map_x0 + map_w + 10)
    d.text((lx, by + 2), "ALSO ON WEDNESDAY 25 NOVEMBER \u2014 18 MORE STORIES",
           font=font(SANS_B, 12), fill=NAVY)
    d.line([lx, by + 20, lx + lw, by + 20], fill=NAVY, width=1)
    col_w = lw // 2
    for i, (num, region, city, frag, bdg, src) in enumerate(LIST):
        col, row = divmod(i, 9)
        x = lx + col * col_w
        yy = by + 26 + row * 18
        d.ellipse([x, yy + 1, x + 14, yy + 15], fill=REGION[region])
        d.text((x + 7, yy + 3), str(num), font=font(SANS_B, 8), fill=WHITE, anchor="ma")
        tag = f"[{bdg}·{src}]"
        f = font(SANS, 10)
        maxw = col_w - 18 - int(d.textlength(tag, font=font(SANS_B, 9))) - 8
        s = f"{city}: {frag}"
        while d.textlength(s, font=f) > maxw and len(s) > 20:
            s = s[:-4] + "\u2026"
        d.text((x + 18, yy + 2), s, font=f, fill=INK)
        d.text((x + col_w - 6, yy + 2), tag, font=font(SANS_B, 9),
               fill=RED if bdg == "CL" else NAVY, anchor="ra")

    # 11. DATE CHECK
    dy = 888
    d.rectangle([mx, dy, W - mx, dy + 84], outline=RED, width=2)
    d.text((mx + 8, dy + 5), "DATE CHECK",
           font=font(SANS_B, 12), fill=RED)
    d.text((mx + 96, dy + 5),
           "Every story above happened or was first reported on Wednesday "
           "25 November 2026.",
           font=font(SANS_B, 11), fill=INK)
    ty = dy + 22
    ty = para(d, mx + 8, ty,
              wrap(d, "Left out as earlier news: " + DATE_LEFT,
                   font(SANS, 11), W - 2 * mx - 16),
              font(SANS, 11), leading=13)
    para(d, mx + 8, ty + 1,
         wrap(d, "Not yet: " + DATE_NOTYET, font(SANS_B, 11), W - 2 * mx - 16),
         font(SANS_B, 11), leading=13)

    # 12. footer
    fy = 978
    d.text((mx, fy),
           "OFFICIAL an authority's own word \u00b7 REPORTED press report \u00b7 "
           "CLAIM one side's say, unverified \u00b7 CONFIRMED 2+ major outlets",
           font=font(SANS, 10), fill=GREY)
    d.text((mx, fy + 13),
           "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Xinhua, Yonhap, ABS, "
           "BEA, Ofgem, EC, NZX \u2014 all reported 25 November 2026.",
           font=font(SANS, 10), fill=GREY)
    d.text((mx, fy + 26),
           "Every drawing original \u2014 drawn in code, not photos.",
           font=font(SANS, 10), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
