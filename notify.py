"""إشعارات الطلبات والاشتراكات. الويب هوك اختياري، وإلا يُحفظ الحدث محلياً."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from urllib.parse import quote

from paths import data_dir


def _path():
    return data_dir() / "notifications.json"


def _load() -> list[dict]:
    path = _path()
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(payload, dict):
        items = payload.get("notifications")
    else:
        items = payload
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def _save(items: list[dict]) -> None:
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"notifications": items}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def wa_digits(phone: str) -> str:
    digits = "".join(ch for ch in str(phone or "") if ch.isdigit())
    if digits.startswith("00"):
        digits = digits[2:]
    if len(digits) == 11 and digits.startswith("0"):
        digits = "20" + digits[1:]
    return digits


def whatsapp_link(phone: str, text: str) -> str:
    digits = wa_digits(phone)
    if len(digits) < 8:
        return ""
    return f"https://wa.me/{digits}?text={quote(str(text or ''))}"


def _post_webhook(url: str, payload: dict) -> None:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=raw,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        response.read()


def record_event(
    event_type: str,
    store: str,
    total: int = 0,
    phone: str = "",
    order_id: str = "",
    vendor_id: str = "",
    store_id: str = "",
) -> dict:
    event = {
        "id": uuid.uuid4().hex[:12],
        "type": event_type,
        "order_id": order_id,
        "vendor_id": vendor_id,
        "store_id": store_id,
        "store": store,
        "total": int(total or 0),
        "phone": str(phone or ""),
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    items = _load()
    items.insert(0, event)
    _save(items[:300])
    url = os.environ.get("MOSLEM_WEBHOOK_URL", "").strip()
    if url.startswith(("http://", "https://")):
        payload = {
            "type": event["type"],
            "order_id": event["order_id"],
            "vendor_id": event["vendor_id"],
            "store": event["store"],
            "total": event["total"],
            "phone": event["phone"],
        }
        try:
            _post_webhook(url, payload)
        except (OSError, urllib.error.URLError, TimeoutError, ValueError):
            pass
    return event


def list_notifications(store_id: str | None = None) -> list[dict]:
    items = _load()
    if not store_id:
        return items
    return [
        item
        for item in items
        if item.get("store_id") == store_id or item.get("vendor_id") == store_id
    ]
