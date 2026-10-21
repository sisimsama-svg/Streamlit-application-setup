"""إعدادات المنصة في data/admin.json. رمز الإدارة يُحفظ كبصمة فقط."""

from __future__ import annotations

import json
from pathlib import Path

from paths import data_dir


def _path() -> Path:
    return data_dir() / "admin.json"


def _load() -> dict:
    path = _path()
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _save(payload: dict) -> None:
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    clean: dict[str, str] = {}
    digest = str(payload.get("code_hash") or "")
    if digest:
        clean["code_hash"] = digest
    clean["support_whatsapp"] = str(payload.get("support_whatsapp") or "").strip()
    path.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")


def admin_hash() -> str:
    return str(_load().get("code_hash") or "")


def save_admin_hash(digest: str) -> None:
    data = _load()
    data["code_hash"] = str(digest or "")
    _save(data)


def _official_support() -> str:
    from vendors import OFFICIAL_WHATSAPP

    return OFFICIAL_WHATSAPP


def support_whatsapp() -> str:
    saved = str(_load().get("support_whatsapp") or "").strip()
    return saved or _official_support()


def ensure_support_whatsapp() -> None:
    data = _load()
    if str(data.get("support_whatsapp") or "").strip():
        return
    data["support_whatsapp"] = _official_support()
    _save(data)


def save_support_whatsapp(number: str) -> None:
    data = _load()
    data["support_whatsapp"] = str(number or "").strip()
    _save(data)
