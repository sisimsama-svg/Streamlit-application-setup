"""تجميع MoslemOptics.exe. المسارات الداخلية للبناء بالإنجليزية لتفادي فشل PyInstaller."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

def _install_ascii_stdio() -> None:
    os.environ["PYTHONIOENCODING"] = "ascii:backslashreplace"
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="ascii", errors="backslashreplace")
        except Exception:
            pass


_install_ascii_stdio()

ROOT = Path(__file__).resolve().parent
BUILD = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "MoslemOpticsBuild"
SRC = BUILD / "src"
DIST = BUILD / "dist"
WORK = BUILD / "work"

CONFIG = """[global]
developmentMode = false

[server]
headless = true
address = "127.0.0.1"
fileWatcherType = "none"
runOnSave = false
enableCORS = false
enableXsrfProtection = true
showEmailPrompt = false

[browser]
gatherUsageStats = false

[theme]
base = "light"
primaryColor = "#059669"
backgroundColor = "#f4faf6"
secondaryBackgroundColor = "#ffffff"
textColor = "#2e3236"
linkColor = "#047857"
"""

MODULES = (
    "app.py",
    "products.py",
    "tryon.py",
    "generate_assets.py",
    "paths.py",
    "i18n.py",
    "vendors.py",
    "notify.py",
    "pdf_docs.py",
    "backup_export.py",
    "platform_cfg.py",
    "desktop.py",
)


def _out(message: str) -> None:
    safe = str(message).encode("ascii", "backslashreplace")
    sys.stdout.buffer.write(safe + b"\n")
    sys.stdout.buffer.flush()


def _run(cmd: list[str]) -> None:
    _out("RUN " + subprocess.list2cmdline(cmd))
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "ascii:backslashreplace"
    subprocess.check_call(cmd, cwd=str(BUILD), env=env)


def _ensure(package: str, import_name: str | None = None) -> None:
    name = import_name or package
    try:
        __import__(name)
    except ImportError:
        _run([sys.executable, "-m", "pip", "install", package])


def _stage() -> Path:
    import make_icon

    icon = make_icon.build(ROOT / "assets" / "moslem.ico")
    if SRC.exists():
        shutil.rmtree(SRC)
    SRC.mkdir(parents=True)
    for name in MODULES:
        shutil.copy2(ROOT / name, SRC / name)
    shutil.copytree(ROOT / "assets", SRC / "assets")
    (SRC / "data").mkdir()
    catalog = ROOT / "data" / "catalog.json"
    if catalog.is_file():
        shutil.copy2(catalog, SRC / "data" / "catalog.json")
    config_dir = SRC / ".streamlit"
    config_dir.mkdir()
    (config_dir / "config.toml").write_text(CONFIG, encoding="utf-8")
    staged_icon = SRC / "assets" / "moslem.ico"
    if staged_icon.resolve() != icon.resolve():
        shutil.copy2(icon, staged_icon)
    return staged_icon


def _spec(icon: Path) -> str:
    src = SRC.as_posix()
    icon_path = icon.as_posix()
    return f"""# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, copy_metadata

datas = []
binaries = []
hidden = [
    "i18n",
    "vendors",
    "platform_cfg",
    "notify",
    "pdf_docs",
    "backup_export",
    "paths",
    "products",
    "tryon",
    "generate_assets",
    "streamlit.runtime.scriptrunner.magic_funcs",
    "streamlit.web.cli",
    "uvicorn",
    "uvicorn.logging",
    "uvicorn.loops",
    "uvicorn.loops.auto",
    "uvicorn.protocols",
    "uvicorn.protocols.http",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan",
    "uvicorn.lifespan.on",
    "starlette.routing",
    "websockets",
    "watchdog.observers",
]

for pkg in ("streamlit", "mediapipe", "altair", "cv2", "PIL", "numpy"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hidden += h
    except Exception as exc:
        print("collect skip", pkg, ascii(exc))

for dist_name in (
    "streamlit",
    "mediapipe",
    "altair",
    "numpy",
    "pandas",
    "pillow",
    "opencv-python-headless",
    "protobuf",
):
    try:
        datas += copy_metadata(dist_name)
    except Exception:
        pass

datas += [
    ("{src}/app.py", "."),
    ("{src}/products.py", "."),
    ("{src}/tryon.py", "."),
    ("{src}/generate_assets.py", "."),
    ("{src}/paths.py", "."),
    ("{src}/i18n.py", "."),
    ("{src}/vendors.py", "."),
    ("{src}/platform_cfg.py", "."),
    ("{src}/notify.py", "."),
    ("{src}/pdf_docs.py", "."),
    ("{src}/backup_export.py", "."),
    ("{src}/desktop.py", "."),
    ("{src}/assets", "assets"),
    ("{src}/data", "data"),
    ("{src}/.streamlit", ".streamlit"),
]

a = Analysis(
    ["{src}/desktop.py"],
    pathex=[r"{src}"],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=["pytest", "tkinter"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="MoslemOptics",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon="{icon_path}",
)
"""


def _publish(built: Path) -> Path:
    out_dir = ROOT / "dist"
    out_dir.mkdir(exist_ok=True)
    final = out_dir / "MoslemOptics.exe"
    shutil.copy2(built, final)
    return final


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    _ensure("pyinstaller", "PyInstaller")
    _ensure("arabic-reshaper", "arabic_reshaper")
    _ensure("python-bidi", "bidi")
    _ensure("reportlab", "reportlab")
    _ensure("openpyxl", "openpyxl")
    icon = _stage()
    spec = BUILD / "MoslemOptics.spec"
    spec.write_text(_spec(icon), encoding="utf-8")
    _run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", str(spec), "--distpath", str(DIST), "--workpath", str(WORK)])
    built = DIST / "MoslemOptics.exe"
    if not built.is_file():
        raise SystemExit("EXE missing after PyInstaller")
    final = _publish(built)
    size = final.stat().st_size
    _out(f"EXE dist/MoslemOptics.exe bytes={size}")
    _out(f"SIZE_MB {size / (1024 * 1024):.1f}")
    _out("ICON assets/moslem.ico")


if __name__ == "__main__":
    try:
        main()
    except UnicodeEncodeError:
        exe = ROOT / "dist" / "MoslemOptics.exe"
        if exe.is_file():
            _out(f"EXE_OK bytes={exe.stat().st_size}")
        else:
            raise
