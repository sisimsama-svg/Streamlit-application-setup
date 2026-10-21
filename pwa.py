"""ملفات PWA: الأيقونات، manifest، وعامل الخدمة على جذر التطبيق."""

from __future__ import annotations

from pathlib import Path

from starlette.responses import FileResponse
from starlette.routing import Route

ROOT = Path(__file__).resolve().parent
ICONS = ROOT / "pwa" / "icons"
THEME = (5, 150, 105, 255)
ALLOWED = {
    "icon-192.png": 192,
    "icon-512.png": 512,
    "icon-maskable-512.png": 512,
    "apple-touch-180.png": 180,
}

HEAD = """
<link id="moslem-manifest" rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#059669">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="نظارات مسلم">
<link rel="apple-touch-icon" href="/pwa/apple-touch-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="/pwa/icon-192.png">
<script src="/pwa/register.js" defer></script>
""".encode("utf-8")


def _logo():
    from PIL import Image, ImageOps

    assets = ROOT / "assets"
    for name in ("moslem-logo.png", "moslem-logo.jpg", "moslem-logo.jpeg"):
        path = assets / name
        if path.is_file():
            image = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
            return image
    raise FileNotFoundError("assets/moslem-logo.jpg")


def _badge(image):
    from PIL import Image, ImageDraw

    pixels = image.load()
    width, height = image.size
    xs = []
    ys = []
    for y in range(height):
        for x in range(width):
            red, green, blue, _alpha = pixels[x, y]
            if red > 228 and green > 228 and blue > 228:
                xs.append(x)
                ys.append(y)
    if not xs:
        return image
    left, right = min(xs), max(xs)
    top, bottom = min(ys), max(ys)
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2
    radius = max(right - left, bottom - top) // 2
    side = radius * 2
    box = (
        max(0, center_x - radius),
        max(0, center_y - radius),
        min(width, center_x + radius),
        min(height, center_y + radius),
    )
    crop = image.crop(box)
    if crop.size != (side, side):
        crop = crop.resize((side, side), Image.Resampling.LANCZOS)
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, side - 1, side - 1), fill=255)
    crop.putalpha(mask)
    return crop


def _icon(mark, size: int, *, maskable: bool):
    from PIL import Image

    canvas = Image.new("RGBA", (size, size), THEME)
    scale = 0.62 if maskable else 0.86
    side = max(1, int(size * scale))
    fitted = mark.copy()
    fitted.thumbnail((side, side), Image.Resampling.LANCZOS)
    origin = ((size - fitted.width) // 2, (size - fitted.height) // 2)
    canvas.paste(fitted, origin, fitted)
    return canvas


def build_icons() -> None:
    ICONS.mkdir(parents=True, exist_ok=True)
    mark = _badge(_logo())
    targets = {
        "icon-192.png": (192, False),
        "icon-512.png": (512, False),
        "icon-maskable-512.png": (512, True),
        "apple-touch-180.png": (180, False),
    }
    for name, (size, maskable) in targets.items():
        _icon(mark, size, maskable=maskable).save(ICONS / name, format="PNG")


def _file(path: Path, media_type: str, extra: dict[str, str] | None = None) -> FileResponse:
    headers = {"Cache-Control": "no-cache"}
    if extra:
        headers.update(extra)
    return FileResponse(path, media_type=media_type, headers=headers)


async def manifest(_request):
    path = ROOT / "manifest.json"
    if not path.is_file():
        from starlette.responses import PlainTextResponse

        return PlainTextResponse("manifest missing", status_code=404)
    return _file(path, "application/manifest+json")


async def service_worker(_request):
    path = ROOT / "service-worker.js"
    if not path.is_file():
        from starlette.responses import PlainTextResponse

        return PlainTextResponse("service worker missing", status_code=404)
    return _file(path, "application/javascript", {"Service-Worker-Allowed": "/"})


async def asset(request):
    from starlette.responses import PlainTextResponse

    name = request.path_params.get("name", "")
    if name == "register.js":
        path = ROOT / "pwa" / "register.js"
        media = "application/javascript"
    elif name in ALLOWED:
        path = ICONS / name
        media = "image/png"
    else:
        return PlainTextResponse("not found", status_code=404)
    if not path.is_file():
        return PlainTextResponse("not found", status_code=404)
    return _file(path, media)


def routes():
    if not (ICONS / "icon-192.png").is_file():
        build_icons()
    return [
        Route("/manifest.json", manifest, methods=["GET"]),
        Route("/service-worker.js", service_worker, methods=["GET"]),
        Route("/pwa/{name}", asset, methods=["GET"]),
    ]


class PWAMiddleware:
    """يضيف manifest واللون والأيقونة إلى صفحة Streamlit."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http" or scope.get("path") not in ("/", "/index.html"):
            await self.app(scope, receive, send)
            return

        started: dict = {}
        chunks = bytearray()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                started["message"] = message
                return
            if message["type"] != "http.response.body":
                await send(message)
                return
            chunks.extend(message.get("body") or b"")
            if message.get("more_body"):
                return
            start = started.get("message")
            if start is None:
                await send(message)
                return
            payload = bytes(chunks)
            headers = list(start.get("headers") or [])
            content_type = ""
            for key, value in headers:
                if key.lower() == b"content-type":
                    content_type = value.decode("latin1", "ignore")
            status = int(start.get("status", 200))
            if (
                status == 200
                and "text/html" in content_type
                and b"moslem-manifest" not in payload
                and b"</head>" in payload
            ):
                payload = payload.replace(b"</head>", HEAD + b"</head>", 1)
                headers = [(key, value) for key, value in headers if key.lower() != b"content-length"]
                headers.append((b"content-length", str(len(payload)).encode("ascii")))
            await send({**start, "headers": headers})
            await send({"type": "http.response.body", "body": payload, "more_body": False})

        await self.app(scope, receive, send_wrapper)
