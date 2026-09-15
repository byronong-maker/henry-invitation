"""Static invitation card for Henry's First Lap. Usage: python make_card.py [godparents|guests] [out.png]"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math, sys

VARIANT = sys.argv[1] if len(sys.argv) > 1 else 'godparents'
OUT = sys.argv[2] if len(sys.argv) > 2 else f'henry-invite-{VARIANT}.png'

W, H = 1080, 1350
RED, RED_DARK, YELLOW, BLACK, CREAM, WHITE, BLUE = (227, 27, 35), (179, 18, 26), (255, 194, 14), (22, 22, 22), (255, 248, 236), (255, 255, 255), (31, 95, 191)

def racing(size): return ImageFont.truetype('fonts/RacingSansOne.ttf', size)
def nunito(size, weight=700):
    f = ImageFont.truetype('fonts/Nunito.ttf', size); f.set_variation_by_axes([weight]); return f

img = Image.new('RGB', (W, H), RED)
d = ImageDraw.Draw(img)

# ---- sunburst
rays = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rays)
cx, cy = W // 2, 520
for i in range(0, 360, 18):
    a0, a1 = math.radians(i), math.radians(i + 9)
    R = 1600
    rd.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(255, 255, 255, 18))
img.paste(rays, (0, 0), rays)

# ---- checkered strips top and bottom
def checks(y, h=26, cell=26):
    for x in range(0, W, cell):
        for row in range(0, h, cell):
            c = BLACK if ((x // cell) + (row // cell)) % 2 == 0 else WHITE
            d.rectangle((x, y + row, x + cell - 1, y + min(row + cell, h) - 1), fill=c)
checks(0); checks(H - 26)

def text_w(t, f): return d.textlength(t, font=f)
def center(t, y, f, fill, shadow=None, tracking=0):
    if tracking:
        w = sum(text_w(c, f) for c in t) + tracking * (len(t) - 1)
        x = W / 2 - w / 2
        for c in t:
            if shadow: d.text((x, y + shadow[1]), c, font=f, fill=shadow[0])
            d.text((x, y), c, font=f, fill=fill); x += text_w(c, f) + tracking
        return
    x = W / 2 - text_w(t, f) / 2
    if shadow: d.text((x, y + shadow[1]), t, font=f, fill=shadow[0])
    d.text((x, y), t, font=f, fill=fill)

# ---- yellow pill tag
tag = "RACE DAY  ·  SATURDAY, SEPTEMBER 19, 2026"
f = nunito(22, 900); tw = text_w(tag, f) + 8 * 2
px0, py0 = W / 2 - tw / 2 - 22, 58
d.rounded_rectangle((px0, py0, px0 + tw + 44, py0 + 46), radius=23, fill=YELLOW)
d.text((px0 + 22, py0 + 10), tag, font=f, fill=BLACK)

# ---- kicker + name
center("Start your engines! Our little racer", 128, nunito(30, 700), WHITE)
center("HENRY", 158, racing(190), WHITE, shadow=(RED_DARK, 9))
center("THOMPSON ONG", 352, racing(44), YELLOW, tracking=6)

# ---- tyre with photo
tcx, tcy, tr = W // 2, 640, 210
tyre = Image.new('RGBA', (tr * 2, tr * 2), (0, 0, 0, 0)); td = ImageDraw.Draw(tyre)
td.ellipse((0, 0, tr * 2, tr * 2), fill=BLACK)
for i in range(0, 360, 12):  # tread
    a0, a1 = math.radians(i), math.radians(i + 6)
    td.pieslice((0, 0, tr * 2, tr * 2), i, i + 6, fill=(43, 43, 43))
inner = int(tr * 0.62)
td.ellipse((tr - inner, tr - inner, tr + inner, tr + inner), fill=BLACK)
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
sd.ellipse((tcx - tr, tcy - tr + 22, tcx + tr, tcy + tr + 22), fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(18)); img.paste(shadow, (0, 0), shadow)
img.paste(tyre, (tcx - tr, tcy - tr), tyre)
pr = int(tr * 0.72)
photo = ImageOps.fit(Image.open('../img/henry-hero.jpg').convert('RGB'), (pr * 2, pr * 2), Image.LANCZOS)
mask = Image.new('L', (pr * 2, pr * 2), 0); ImageDraw.Draw(mask).ellipse((0, 0, pr * 2, pr * 2), fill=255)
d.ellipse((tcx - pr - 8, tcy - pr - 8, tcx + pr + 8, tcy + pr + 8), fill=YELLOW)
img.paste(photo, (tcx - pr, tcy - pr), mask)
# race number roundel on the tyre
rr = 42; rx, ry = tcx + tr - 52, tcy - tr + 52
d.ellipse((rx - rr, ry - rr, rx + rr, ry + rr), fill=WHITE, outline=BLACK, width=6)
f = racing(52); d.text((rx - text_w("1", f) / 2, ry - 34), "1", font=f, fill=BLACK)

# ---- event line
center("Christening  &  1st Birthday", 868, racing(58), WHITE, shadow=(RED_DARK, 5))

# ---- details card
cx0, cy0, cx1, cy1 = 70, 950, W - 70, 1226
d.rounded_rectangle((cx0 + 10, cy0 + 10, cx1 + 10, cy1 + 10), radius=22, fill=YELLOW)
d.rounded_rectangle((cx0, cy0, cx1, cy1), radius=22, fill=CREAM, outline=BLACK, width=5)
y = cy0 + 22
def row(label, lines, y):
    f1 = nunito(17, 900); f2 = nunito(26, 800); f3 = nunito(21, 600)
    d.text((cx0 + 34, y + 6), label, font=f1, fill=RED)
    d.text((cx0 + 210, y), lines[0], font=f2, fill=BLACK)
    yy = y + 34
    for ln in lines[1:]:
        d.text((cx0 + 210, yy), ln, font=f3, fill=(90, 90, 90)); yy += 27
    return yy + 12
y = row("CEREMONY", ["Cathedral Church", "San Nicolas Street, Surigao City", "Time: to be announced"], y)
y = row("RECEPTION", ["Jollibee Highway Branch", "Outside Villa Corito, Surigao City"], y)
y = row("DRESS CODE", ["To be announced"], y)

# ---- closing line (variant)
if VARIANT == 'godparents':
    l1 = "Byron & Hanna would be honoured to have you"
    l2 = "stand as Ninong or Ninang to Henry."
else:
    l1 = "Byron & Hanna would love for you to join them"
    l2 = "as Henry crosses his very first finish line."
center(l1, 1252, nunito(24, 700), WHITE)
center(l2, 1284, nunito(24, 700), WHITE)

img.save(OUT, quality=95)
print('saved', OUT)
