"""Render the three CrazyGames listing covers with the game's postal palette."""

from pathlib import Path
from math import sin, cos, pi
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(__file__).parent
FONT = Path(r"C:\Windows\Fonts\trebucbd.ttf")
NAVY = (20, 45, 53)
CREAM = (255, 247, 226)
GOLD = (245, 189, 85)


def font(size):
    return ImageFont.truetype(str(FONT), int(size))


def parcel(kind, size):
    s = 420
    art = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(art)
    stroke = 13
    if kind == "box":
        d.rounded_rectangle((42, 71, 378, 357), 25, fill="#c78c56", outline="#784e30", width=stroke)
        d.rectangle((177, 73, 244, 354), fill="#ead1a1")
        d.line((42, 155, 378, 155), fill="#996c43", width=7)
        d.rounded_rectangle((77, 224, 190, 312), 11, fill="#fff7e4", outline="#784e30", width=8)
        d.line((95, 252, 168, 252), fill="#a79475", width=6)
        d.line((95, 273, 147, 273), fill="#a79475", width=6)
        d.polygon(((177, 70), (244, 70), (237, 92), (184, 92)), fill="#f6dfaf")
    elif kind == "envelope":
        d.rounded_rectangle((26, 91, 394, 331), 25, fill="#fff3d9", outline="#a9844c", width=13)
        d.line((36, 104, 210, 245, 384, 104), fill="#b89964", width=12, joint="curve")
        d.line((35, 318, 165, 210), fill="#ddc5a0", width=8)
        d.line((385, 318, 255, 210), fill="#ddc5a0", width=8)
        d.rounded_rectangle((301, 119, 365, 184), 7, fill="#e26f54", outline="#9d4e3d", width=7)
        d.ellipse((318, 135, 348, 165), fill="#fff3d9")
    elif kind == "tube":
        d.rounded_rectangle((34, 145, 335, 278), 66, fill="#6caed9", outline="#356e99", width=13)
        d.ellipse((290, 145, 389, 278), fill="#acd5ea", outline="#356e99", width=13)
        d.ellipse((326, 174, 365, 249), fill="#356e99")
        d.arc((90, 122, 165, 302), 65, 295, fill="#3b81b0", width=11)
    elif kind == "sack":
        d.polygon(((206, 35), (290, 111), (343, 187), (344, 282), (295, 347), (125, 347), (76, 282), (77, 187), (130, 111)), fill="#81b36f")
        d.line((206, 35, 290, 111, 343, 187, 344, 282, 295, 347, 125, 347, 76, 282, 77, 187, 130, 111, 206, 35), fill="#477640", width=13, joint="curve")
        d.arc((127, 117, 295, 204), 10, 170, fill="#477640", width=13)
        d.rounded_rectangle((158, 247, 263, 309), 10, fill="#eff2d8", outline="#477640", width=8)
    elif kind == "mouse":
        d.arc((18, 242, 163, 391), 40, 260, fill="#adb2b6", width=20)
        d.ellipse((77, 170, 321, 335), fill="#a8afb7", outline="#54626c", width=12)
        d.ellipse((257, 142, 394, 282), fill="#a8afb7", outline="#54626c", width=12)
        d.ellipse((267, 70, 333, 144), fill="#e9b1bd", outline="#54626c", width=11)
        d.ellipse((338, 66, 404, 140), fill="#e9b1bd", outline="#54626c", width=11)
        d.ellipse((351, 188, 372, 209), fill="#26383d")
        d.ellipse((388, 228, 413, 248), fill="#e08391")
        d.line((382, 250, 419, 241), fill="#54626c", width=6)
    return art.resize((size, size), Image.Resampling.LANCZOS)


def place(base, art, x, y, size, angle=0):
    icon = parcel(art, size).rotate(angle, Image.Resampling.BICUBIC, expand=True)
    shadow = Image.new("RGBA", icon.size)
    shadow.putalpha(icon.getchannel("A"))
    shadow = Image.new("RGBA", icon.size, (0, 0, 0, 0))
    shadow.paste((0, 15, 19, 125), (0, 0, icon.width, icon.height), icon.getchannel("A"))
    shadow = shadow.filter(ImageFilter.GaussianBlur(max(4, size // 35)))
    at = (int(x - icon.width / 2), int(y - icon.height / 2))
    base.alpha_composite(shadow, (at[0] + size // 35, at[1] + size // 28))
    base.alpha_composite(icon, at)


def base_canvas(w, h):
    canvas = Image.new("RGBA", (w, h), NAVY + (255,))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((-w * .2, -h * .3, w * .65, h * .65), fill=(67, 133, 127, 75))
    g.ellipse((w * .4, h * .4, w * 1.2, h * 1.3), fill=(64, 124, 115, 80))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(int(min(w, h) * .12))))
    d = ImageDraw.Draw(canvas)
    grid = max(40, int(min(w, h) * .048))
    for x in range(0, w, grid):
        d.line((x, 0, x, h), fill=(193, 227, 218, 24), width=2)
    for y in range(0, h, grid):
        d.line((0, y, w, y), fill=(193, 227, 218, 24), width=2)
    return canvas


def title(draw, x, y, size):
    f = font(size)
    gap = int(size * .91)
    for line, color, yy in (("PARCEL", CREAM, y), ("PANIC!", GOLD, y + gap)):
        draw.text((x + 6, yy + 10), line, font=f, fill=(9, 26, 32), stroke_width=0)
        draw.text((x, yy), line, font=f, fill=color, stroke_width=max(1, size // 160), stroke_fill=color)


def cover(name, w, h):
    img = base_canvas(w, h)
    d = ImageDraw.Draw(img)
    if w > h * 1.3:
        title(d, int(w * .045), int(h * .23), int(h * .17))
        cx, cy, r = w * .72, h * .51, h * .35
        items = [("box", .65, .41, .34, -10), ("envelope", .87, .55, .30, 8), ("tube", .78, .23, .23, 15), ("sack", .58, .71, .23, -14), ("mouse", .9, .78, .17, 0)]
    elif h > w * 1.3:
        title(d, int(w * .075), int(h * .08), int(w * .19))
        cx, cy, r = w * .51, h * .62, w * .43
        items = [("box", .28, .51, .54, -11), ("envelope", .70, .57, .43, 8), ("tube", .73, .39, .32, 15), ("sack", .30, .77, .33, -12), ("mouse", .75, .78, .30, 5)]
    else:
        title(d, int(w * .07), int(h * .065), int(w * .165))
        cx, cy, r = w * .53, h * .66, w * .40
        items = [("box", .29, .55, .43, -10), ("envelope", .73, .64, .39, 8), ("tube", .72, .43, .29, 15), ("sack", .34, .81, .27, -12), ("mouse", .79, .83, .23, 3)]
    d = ImageDraw.Draw(img)
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(116, 171, 158, 125), width=max(4, w // 180))
    d.ellipse((cx-r*.77, cy-r*.77, cx+r*.77, cy+r*.77), outline=(85, 146, 138, 80), width=max(12, w // 60))
    for i in range(13):
        a = i * 2*pi / 13
        sx, sy = cx + cos(a) * r * 1.16, cy + sin(a) * r * 1.16
        rad = max(3, w // 225)
        d.ellipse((sx-rad, sy-rad, sx+rad, sy+rad), fill=GOLD + (220,))
    for kind, px, py, frac, angle in items:
        place(img, kind, w*px, h*py, int(min(w, h)*frac), angle)
    output = OUT / f"cover-{name}.png"
    img.convert("RGB").save(output, optimize=True)
    print(output, output.stat().st_size)


if __name__ == "__main__":
    cover("landscape", 1920, 1080)
    cover("portrait", 800, 1200)
    cover("square", 800, 800)
