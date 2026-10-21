"""أيقونة نظارات مسلم من ملف الشعار الرسمي، من غير إعادة رسم."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

SIZES = (16, 32, 48, 64, 128, 256)


def logo_file() -> Path:
    root = Path(__file__).resolve().parent / "assets"
    for name in ("moslem-logo.png", "moslem-logo.jpg", "moslem-logo.jpeg"):
        path = root / name
        if path.is_file():
            return path
    raise FileNotFoundError("assets/moslem-logo.jpg")


def _square(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image).convert("RGBA")
    side = max(image.size)
    if image.size == (side, side):
        return image
    corner = image.getpixel((0, 0))
    canvas = Image.new("RGBA", (side, side), corner)
    canvas.paste(image, ((side - image.width) // 2, (side - image.height) // 2), image)
    return canvas


def build(dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    source = _square(Image.open(logo_file()))
    images = [source.resize((size, size), Image.Resampling.LANCZOS) for size in SIZES]
    images[-1].save(
        dest,
        format="ICO",
        sizes=[(size, size) for size in SIZES],
        append_images=images[:-1],
    )
    return dest


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "assets" / "moslem.ico"
    build(target)
    with Image.open(target) as icon:
        found = tuple(sorted(size[0] for size in icon.info.get("sizes", ())))
    expected = tuple(sorted(SIZES))
    if found != expected:
        raise SystemExit(f"ICON_SIZES_BAD {found}")
    print("ICON_OK " + ",".join(str(size) for size in found))
