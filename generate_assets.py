"""توليد صور نظارات شفافة للعرض وتجربة الارتداء."""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFilter

from paths import user_glasses_dir
SIZE = (1200, 420)


def _blank() -> Image.Image:
    return Image.new("RGBA", SIZE, (0, 0, 0, 0))


def _draw_lens(draw: ImageDraw.ImageDraw, box, fill, outline, width=18):
    draw.rounded_rectangle(box, radius=int((box[3] - box[1]) * 0.35), fill=fill, outline=outline, width=width)


def _bridge(draw: ImageDraw.ImageDraw, y, x1, x2, color, width=14):
    draw.line([(x1, y), (x2, y)], fill=color, width=width)


def _temples(draw: ImageDraw.ImageDraw, left, right, color, width=14):
    lx0, ly0, lx1, ly1 = left
    rx0, ry0, rx1, ry1 = right
    mid_l = (ly0 + ly1) // 2
    mid_r = (ry0 + ry1) // 2
    draw.line([(40, mid_l - 8), (lx0, mid_l)], fill=color, width=width)
    draw.line([(rx1, mid_r), (SIZE[0] - 40, mid_r + 8)], fill=color, width=width)


def save(img: Image.Image, name: str) -> None:
    folder = user_glasses_dir()
    folder.mkdir(parents=True, exist_ok=True)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(folder / name, "PNG")


def classic_black() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (18, 18, 18, 255)
    lens = (40, 40, 40, 70)
    left = (160, 70, 540, 340)
    right = (660, 70, 1040, 340)
    _draw_lens(d, left, lens, color, 22)
    _draw_lens(d, right, lens, color, 22)
    _bridge(d, 180, 540, 660, color, 16)
    _temples(d, left, right, color, 16)
    save(img, "classic_black.png")


def round_gold() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (196, 149, 58, 255)
    lens = (50, 55, 40, 55)
    left = (190, 55, 530, 365)
    right = (670, 55, 1010, 365)
    d.ellipse(left, fill=lens, outline=color, width=18)
    d.ellipse(right, fill=lens, outline=color, width=18)
    _bridge(d, 195, 530, 670, color, 12)
    _temples(d, left, right, color, 12)
    save(img, "round_gold.png")


def aviator_silver() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (170, 178, 188, 255)
    lens = (28, 36, 48, 150)
    left = [(170, 90), (540, 90), (520, 330), (210, 340)]
    right = [(660, 90), (1030, 90), (990, 340), (680, 330)]
    d.polygon(left, fill=lens, outline=color)
    d.polygon(right, fill=lens, outline=color)
    d.line(left + [left[0]], fill=color, width=10)
    d.line(right + [right[0]], fill=color, width=10)
    _bridge(d, 120, 540, 660, color, 10)
    d.line([(60, 150), (190, 120)], fill=color, width=10)
    d.line([(1010, 120), (1140, 150)], fill=color, width=10)
    save(img, "aviator_silver.png")


def cateye_rose() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (214, 112, 140, 255)
    lens = (70, 40, 55, 65)
    left = [(150, 160), (220, 70), (530, 90), (520, 330), (190, 340)]
    right = [(670, 90), (980, 70), (1050, 160), (1010, 340), (680, 330)]
    d.polygon(left, fill=lens, outline=color)
    d.polygon(right, fill=lens, outline=color)
    _bridge(d, 150, 520, 680, color, 12)
    _temples(d, (150, 70, 530, 340), (670, 70, 1050, 340), color, 12)
    save(img, "cateye_rose.png")


def sport_navy() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (18, 48, 92, 255)
    accent = (0, 168, 150, 255)
    lens = (16, 28, 48, 155)
    left = (90, 90, 560, 330)
    right = (640, 90, 1110, 330)
    _draw_lens(d, left, lens, color, 20)
    _draw_lens(d, right, lens, color, 20)
    _bridge(d, 175, 560, 640, color, 18)
    d.arc([40, 80, 200, 260], 200, 320, fill=accent, width=12)
    d.arc([1000, 80, 1160, 260], 220, 340, fill=accent, width=12)
    save(img, "sport_navy.png")


def square_tortoise() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    colors = [(92, 54, 32, 255), (48, 28, 18, 255), (166, 110, 62, 255)]
    lens = (55, 40, 25, 50)
    left = (150, 70, 545, 345)
    right = (655, 70, 1050, 345)
    for i, box in enumerate((left, right)):
        d.rounded_rectangle(box, radius=28, fill=lens, outline=colors[i % 3], width=26)
    _bridge(d, 175, 545, 655, colors[1], 16)
    _temples(d, left, right, colors[0], 16)
    save(img, "square_tortoise.png")


def oval_green() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (62, 107, 62, 255)
    lens = (40, 70, 45, 60)
    left = (170, 90, 540, 330)
    right = (660, 90, 1030, 330)
    d.ellipse(left, fill=lens, outline=color, width=16)
    d.ellipse(right, fill=lens, outline=color, width=16)
    _bridge(d, 190, 540, 660, color, 12)
    _temples(d, left, right, color, 12)
    save(img, "oval_green.png")


def clear_blue() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (90, 150, 210, 210)
    lens = (80, 140, 200, 55)
    left = (160, 75, 540, 335)
    right = (660, 75, 1040, 335)
    _draw_lens(d, left, lens, color, 16)
    _draw_lens(d, right, lens, color, 16)
    _bridge(d, 180, 540, 660, color, 12)
    _temples(d, left, right, color, 12)
    save(img, "clear_blue.png")


def browline_brown() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    frame = (98, 62, 38, 255)
    metal = (186, 154, 96, 255)
    lens = (55, 48, 36, 50)
    left = (155, 95, 535, 340)
    right = (665, 95, 1045, 340)
    _draw_lens(d, left, lens, metal, 8)
    _draw_lens(d, right, lens, metal, 8)
    d.line([(150, 118), (545, 100)], fill=frame, width=34)
    d.line([(655, 100), (1050, 118)], fill=frame, width=34)
    _bridge(d, 130, 535, 665, frame, 16)
    _temples(d, left, right, frame, 14)
    save(img, "browline_brown.png")


def wayfarer_black() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (16, 16, 16, 255)
    lens = (22, 24, 28, 155)
    left = [(145, 115), (555, 78), (525, 325), (185, 345)]
    right = [(645, 78), (1055, 115), (1015, 345), (675, 325)]
    d.polygon(left, fill=lens)
    d.polygon(right, fill=lens)
    d.line(left + [left[0]], fill=color, width=20)
    d.line(right + [right[0]], fill=color, width=20)
    _bridge(d, 130, 525, 675, color, 16)
    d.line([(45, 175), (160, 140)], fill=color, width=16)
    d.line([(1040, 140), (1155, 175)], fill=color, width=16)
    save(img, "wayfarer_black.png")


def kids_round_blue() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (38, 116, 196, 255)
    lens = (70, 150, 220, 60)
    left = (250, 95, 520, 335)
    right = (680, 95, 950, 335)
    d.ellipse(left, fill=lens, outline=color, width=20)
    d.ellipse(right, fill=lens, outline=color, width=20)
    _bridge(d, 200, 520, 680, color, 14)
    _temples(d, left, right, color, 14)
    save(img, "kids_round_blue.png")


def kids_flex_pink() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (214, 92, 140, 255)
    lens = (255, 170, 196, 55)
    left = (230, 110, 530, 320)
    right = (670, 110, 970, 320)
    _draw_lens(d, left, lens, color, 18)
    _draw_lens(d, right, lens, color, 18)
    _bridge(d, 190, 530, 670, color, 16)
    _temples(d, left, right, color, 16)
    save(img, "kids_flex_pink.png")


def cateye_sun() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (72, 42, 28, 255)
    lens = (40, 26, 18, 150)
    left = [(155, 165), (230, 75), (535, 95), (520, 325), (195, 340)]
    right = [(665, 95), (970, 75), (1045, 165), (1005, 340), (680, 325)]
    d.polygon(left, fill=lens)
    d.polygon(right, fill=lens)
    d.line(left + [left[0]], fill=color, width=16)
    d.line(right + [right[0]], fill=color, width=16)
    _bridge(d, 155, 520, 680, color, 14)
    _temples(d, (155, 75, 535, 340), (665, 75, 1045, 340), color, 14)
    save(img, "cateye_sun.png")


def round_sun_gold() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (196, 149, 58, 255)
    lens = (36, 28, 16, 145)
    left = (200, 70, 530, 360)
    right = (670, 70, 1000, 360)
    d.ellipse(left, fill=lens, outline=color, width=16)
    d.ellipse(right, fill=lens, outline=color, width=16)
    _bridge(d, 190, 530, 670, color, 12)
    _temples(d, left, right, color, 12)
    save(img, "round_sun_gold.png")


def kids_sun_red() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (176, 42, 48, 255)
    lens = (40, 16, 18, 145)
    left = (245, 115, 525, 315)
    right = (675, 115, 955, 315)
    _draw_lens(d, left, lens, color, 18)
    _draw_lens(d, right, lens, color, 18)
    _bridge(d, 190, 525, 675, color, 14)
    _temples(d, left, right, color, 14)
    save(img, "kids_sun_red.png")


def kids_sport_yellow() -> None:
    img = _blank()
    d = ImageDraw.Draw(img)
    color = (214, 164, 28, 255)
    lens = (30, 36, 48, 150)
    left = (210, 120, 545, 300)
    right = (655, 120, 990, 300)
    _draw_lens(d, left, lens, color, 16)
    _draw_lens(d, right, lens, color, 16)
    _bridge(d, 185, 545, 655, color, 16)
    _temples(d, left, right, color, 14)
    save(img, "kids_sport_yellow.png")


def main() -> None:
    classic_black()
    round_gold()
    aviator_silver()
    cateye_rose()
    sport_navy()
    square_tortoise()
    oval_green()
    clear_blue()
    browline_brown()
    wayfarer_black()
    kids_round_blue()
    kids_flex_pink()
    cateye_sun()
    round_sun_gold()
    kids_sun_red()
    kids_sport_yellow()
    print("Saved glasses assets:", len(list(user_glasses_dir().glob("*.png"))), "files")


if __name__ == "__main__":
    main()
