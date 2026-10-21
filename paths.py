"""مسارات القراءة من الحزمة ومسارات الكتابة.

مجلد البيانات الافتراضي هو ``data`` داخل المشروع. على نسخة ويندوز المجمّعة
يبقى بجانب ملف التشغيل إن كان المجلد قابلاً للكتابة. المتغير
``MOSLEM_DATA_DIR`` ينقل كل الملفات القابلة للكتابة (الكتالوج، المتاجر،
الطلبات، الروشتات، الإيصالات، الشعارات، الأغلفة، الإشعارات، وإعداد المنصة)
إلى مسار آخر، مثل قرص دائم على Render.

على Streamlit Community Cloud نظام الملفات مؤقت ويُمسح عند إيقاف التطبيق
أو إعادة نشره، لذلك الطلبات والإيصالات والشعارات لا تبقى هناك.

إذا كان مجلد التثبيت للقراءة فقط تُنقل الكتابة إلى مجلد خارج الحزمة
حتى لا تُفترض الملفات القابلة للكتابة داخل التثبيت.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

_WRITABLE_ROOT: Path | None = None
_DATA_DIR: Path | None = None
_DATA_CHILDREN = ("rx", "receipts", "logos", "covers")


def frozen() -> bool:
    return bool(getattr(sys, "frozen", False)) and hasattr(sys, "_MEIPASS")


def bundle_root() -> Path:
    if frozen():
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def install_dir() -> Path:
    if frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def _can_write(folder: Path) -> bool:
    try:
        folder.mkdir(parents=True, exist_ok=True)
        probe = folder / ".write_probe"
        probe.write_text("ok", encoding="ascii")
        try:
            probe.unlink()
        except OSError:
            pass
        return True
    except OSError:
        return False


def _fallback_root() -> Path:
    local = os.environ.get("LOCALAPPDATA") or os.environ.get("TEMP") or tempfile.gettempdir()
    path = Path(local) / "MoslemOptics"
    path.mkdir(parents=True, exist_ok=True)
    return path


def writable_root() -> Path:
    global _WRITABLE_ROOT
    if _WRITABLE_ROOT is not None:
        return _WRITABLE_ROOT
    if not frozen():
        _WRITABLE_ROOT = Path(__file__).resolve().parent
        return _WRITABLE_ROOT
    beside = install_dir()
    if _can_write(beside):
        _WRITABLE_ROOT = beside
        return _WRITABLE_ROOT
    _WRITABLE_ROOT = _fallback_root()
    return _WRITABLE_ROOT


def _prepare_data(path: Path) -> Path | None:
    if not _can_write(path):
        return None
    try:
        for name in _DATA_CHILDREN:
            (path / name).mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    return path


def _env_data_dir() -> Path | None:
    raw = os.environ.get("MOSLEM_DATA_DIR", "").strip().strip('"').strip("'")
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = install_dir() / path
    return path


def data_dir() -> Path:
    """مجلد البيانات القابل للكتابة. يُنشأ مع مجلداته الفرعية إن غابت."""
    global _DATA_DIR
    if _DATA_DIR is not None:
        return _DATA_DIR
    override = _env_data_dir()
    if override is not None:
        prepared = _prepare_data(override)
        if prepared is not None:
            _DATA_DIR = prepared
            return _DATA_DIR
    prepared = _prepare_data(writable_root() / "data")
    if prepared is None:
        prepared = _prepare_data(_fallback_root() / "data")
    if prepared is None:
        raise OSError("data directory is not writable")
    _DATA_DIR = prepared
    return _DATA_DIR


def user_glasses_dir() -> Path:
    if data_dir() != writable_root() / "data":
        path = data_dir() / "glasses"
    else:
        path = writable_root() / "assets" / "glasses"
    path.mkdir(parents=True, exist_ok=True)
    return path


def bundled_glasses_dir() -> Path:
    return bundle_root() / "assets" / "glasses"


def model_path() -> Path:
    return bundle_root() / "assets" / "models" / "face_landmarker.task"


def sample_face_path() -> Path:
    return bundle_root() / "assets" / "sample_face.jpg"


def log_path() -> Path:
    return install_dir() / "MoslemOptics.log"


def ensure_seed_catalog() -> None:
    dest = data_dir() / "catalog.json"
    if dest.exists():
        return
    src = bundle_root() / "data" / "catalog.json"
    try:
        if src.is_file() and src.resolve() != dest.resolve():
            shutil.copy2(src, dest)
    except OSError:
        return
