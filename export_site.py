"""يجهّز واجهة المتجر للنشر: الكتالوج، صور الإطارات، وصفحة الجذر."""

from __future__ import annotations

import json
import shutil

from paths import bundle_root, user_glasses_dir
from server import WEB, _bootstrap, ensure_assets


def main() -> None:
    ensure_assets()
    glasses = WEB / "glasses"
    glasses.mkdir(parents=True, exist_ok=True)
    for png in user_glasses_dir().glob("*.png"):
        shutil.copy2(png, glasses / png.name)
    data = _bootstrap()
    for item in data["products"]:
        name = str(item.get("image") or "").rsplit("/", 1)[-1]
        item["image"] = f"glasses/{name}"
    (WEB / "bootstrap.json").write_text(
        json.dumps(data, ensure_ascii=False),
        encoding="utf-8",
    )
    icon = bundle_root() / "pwa" / "icons" / "icon-192.png"
    if icon.is_file():
        shutil.copy2(icon, WEB / "favicon.png")
    index = WEB / "index.html"
    if index.is_file():
        shutil.copy2(index, WEB / "404.html")
    (WEB / ".nojekyll").write_text("", encoding="ascii")


if __name__ == "__main__":
    main()
