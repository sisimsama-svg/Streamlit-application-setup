"""متاجر المنصة واشتراكاتها. نظارات مسلم هو المتجر الأساسي."""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime
from pathlib import Path

from notify import wa_digits
from paths import bundle_root, data_dir

PRIMARY_STORE = "moslem"
SHOP_STATUSES = ("open", "closed", "maintenance")
DEMO_INSTAPAY = "moslem.optics@instapay"
OFFICIAL_WHATSAPP = "01148005679"
OFFICIAL_WA_URL = "https://wa.me/201148005679"
OFFICIAL_INSTAGRAM = "https://www.instagram.com/muslimoptics?srtk=dDE0ODk1aDdicXFs"
OFFICIAL_FACEBOOK = "https://www.facebook.com/share/14soSm3zjRZ/?mibextid=wwXIfr"
SUB_METHODS = ("instapay", "card", "apple", "cash")
PLANS = {
    "monthly": 500,
    "yearly": 4500,
}


def _vendors_path() -> Path:
    return data_dir() / "vendors.json"


def _logos_dir() -> Path:
    path = data_dir() / "logos"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _covers_dir() -> Path:
    path = data_dir() / "covers"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _empty_shipping() -> dict:
    return {"default": None, "overrides": {}}


def receipts_dir() -> Path:
    path = data_dir() / "receipts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _moslem_record() -> dict:
    return {
        "id": PRIMARY_STORE,
        "name": "نظارات مسلم",
        "name_en": "Moslem Optics",
        "logo": "",
        "cover": "",
        "whatsapp": OFFICIAL_WHATSAPP,
        "instagram": OFFICIAL_INSTAGRAM,
        "facebook": OFFICIAL_FACEBOOK,
        "shipping": _empty_shipping(),
        "address": "باب اللوق، القاهرة",
        "governorate": "القاهرة",
        "plan": "primary",
        "status": "active",
        "shop_status": "open",
        "primary": True,
        "code_hash": "",
        "created": "",
        "subscription": {
            "status": "active",
            "plan": "primary",
            "method": "",
            "amount": 0,
            "receipt": "",
            "card_name": "",
            "card_last4": "",
            "paid_at": "",
        },
    }


def _read() -> list[dict]:
    path = _vendors_path()
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(payload, dict):
        return [item for item in payload.get("vendors") or [] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def _write(items: list[dict]) -> None:
    path = _vendors_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"vendors": items}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def hash_code(code: str) -> str:
    return hashlib.sha256(code.strip().upper().encode("utf-8")).hexdigest()


def load_vendors() -> list[dict]:
    items = _read()
    changed = False
    moslem = next((item for item in items if item.get("id") == PRIMARY_STORE), None)
    if moslem is None:
        items.insert(0, _moslem_record())
        changed = True
    else:
        for key, value in _moslem_record().items():
            if key not in moslem:
                moslem[key] = value
                changed = True
        moslem["primary"] = True
        moslem["status"] = "active"
        if not str(moslem.get("whatsapp") or "").strip():
            moslem["whatsapp"] = OFFICIAL_WHATSAPP
            changed = True
        if not str(moslem.get("instagram") or "").strip():
            moslem["instagram"] = OFFICIAL_INSTAGRAM
            changed = True
        if not str(moslem.get("facebook") or "").strip():
            moslem["facebook"] = OFFICIAL_FACEBOOK
            changed = True
    for item in items:
        if str(item.get("shop_status") or "") not in SHOP_STATUSES:
            item["shop_status"] = "open"
            changed = True
        if _ensure_vendor_extras(item):
            changed = True
    if changed:
        _write(items)
    return items


def list_active_vendors() -> list[dict]:
    items = [item for item in load_vendors() if item.get("status") == "active"]
    items.sort(key=lambda item: (0 if item.get("id") == PRIMARY_STORE else 1, str(item.get("name") or "")))
    return items


def get_vendor(vendor_id: str) -> dict | None:
    for item in load_vendors():
        if item.get("id") == vendor_id:
            return item
    return None


def vendor_by_code(code: str) -> dict | None:
    wanted = hash_code(code)
    if not code.strip():
        return None
    for item in load_vendors():
        if item.get("primary"):
            continue
        if item.get("code_hash") and item.get("code_hash") == wanted and item.get("status") == "active":
            return item
    return None


def _ensure_vendor_extras(item: dict) -> bool:
    changed = False
    if "cover" not in item:
        item["cover"] = ""
        changed = True
    shipping = item.get("shipping")
    if not isinstance(shipping, dict):
        item["shipping"] = _empty_shipping()
        return True
    if "default" not in shipping:
        shipping["default"] = None
        changed = True
    if not isinstance(shipping.get("overrides"), dict):
        shipping["overrides"] = {}
        changed = True
    return changed


def _image_file(folder: Path, name: str) -> Path | None:
    filename = Path(str(name or "")).name
    if not filename:
        return None
    path = folder / filename
    return path if path.is_file() else None


def bundled_logo_path() -> Path | None:
    assets = bundle_root() / "assets"
    for name in ("moslem-logo.jpg", "moslem-logo.jpeg", "moslem-logo.png"):
        path = assets / name
        if path.is_file():
            return path
    return None


def logo_path(vendor: dict | None) -> Path | None:
    if not vendor:
        return None
    found = _image_file(_logos_dir(), str(vendor.get("logo") or ""))
    if found is not None:
        return found
    if vendor.get("id") == PRIMARY_STORE or vendor.get("primary"):
        return bundled_logo_path()
    return None


def cover_path(vendor: dict | None) -> Path | None:
    if not vendor:
        return None
    return _image_file(_covers_dir(), str(vendor.get("cover") or ""))


def _write_image(folder: Path, vendor_id: str, raw: bytes, suffix: str, allowed: set[str]) -> str:
    ext = suffix.lower() if suffix.lower() in allowed else ".png"
    filename = f"{vendor_id}{ext}"
    for old in folder.glob(f"{vendor_id}.*"):
        if old.name != filename and old.is_file():
            try:
                old.unlink()
            except OSError:
                pass
    (folder / filename).write_bytes(raw)
    return filename


def save_logo(vendor_id: str, raw: bytes, suffix: str) -> str:
    return _write_image(_logos_dir(), vendor_id, raw, suffix, {".jpg", ".jpeg", ".png", ".webp"})


def save_cover(vendor_id: str, raw: bytes, suffix: str) -> str:
    return _write_image(_covers_dir(), vendor_id, raw, suffix, {".jpg", ".jpeg", ".png"})


def _fee_amount(value) -> int | None:
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    try:
        amount = int(value)
    except (TypeError, ValueError):
        return None
    if amount < 0:
        return None
    return amount


def resolve_delivery_fee(vendor: dict | None, governorate: str, platform_fee: int) -> int:
    shipping = (vendor or {}).get("shipping") if isinstance(vendor, dict) else None
    overrides = shipping.get("overrides") if isinstance(shipping, dict) else None
    if isinstance(overrides, dict) and governorate in overrides:
        parsed = _fee_amount(overrides.get(governorate))
        if parsed is not None:
            return parsed
    if isinstance(shipping, dict):
        parsed = _fee_amount(shipping.get("default"))
        if parsed is not None:
            return parsed
    fallback = _fee_amount(platform_fee)
    return 0 if fallback is None else fallback


def fees_for_cart(
    store_ids: list[str],
    vendors_by_id: dict[str, dict | None],
    governorate: str,
    platform_fee: int,
) -> list[tuple[str, int]]:
    parts: list[tuple[str, int]] = []
    seen: list[str] = []
    for store_id in store_ids:
        if store_id in seen:
            continue
        seen.append(store_id)
        amount = resolve_delivery_fee(vendors_by_id.get(store_id), governorate, platform_fee)
        parts.append((store_id, amount))
    return parts


def save_receipt(vendor_id: str, raw: bytes, suffix: str) -> str:
    ext = suffix.lower() if suffix.lower() in {".jpg", ".jpeg", ".png", ".pdf"} else ".jpg"
    filename = f"{vendor_id}-{uuid.uuid4().hex[:8]}{ext}"
    (receipts_dir() / filename).write_bytes(raw)
    return filename


def _new_code(existing: set[str]) -> tuple[str, str]:
    for _ in range(8):
        plain = f"ST-{uuid.uuid4().hex[:8].upper()}"
        digest = hash_code(plain)
        if digest not in existing:
            return plain, digest
    plain = f"ST-{uuid.uuid4().hex[:12].upper()}"
    return plain, hash_code(plain)


def register_vendor(
    name: str,
    whatsapp: str,
    address: str,
    governorate: str,
    plan: str,
    method: str,
    logo_bytes: bytes | None = None,
    logo_suffix: str = "",
    receipt_bytes: bytes | None = None,
    receipt_suffix: str = "",
    card_name: str = "",
    card_last4: str = "",
) -> tuple[dict, str]:
    if method not in SUB_METHODS:
        raise ValueError("unsupported subscription method")
    if method == "instapay" and not receipt_bytes:
        raise ValueError("instapay receipt required")
    holder = " ".join(str(card_name or "").split())
    last4 = str(card_last4 or "").strip()
    if method == "card":
        if not holder or not last4.isdigit() or len(last4) != 4:
            raise ValueError("card details required")
    else:
        holder = ""
        last4 = ""
    items = load_vendors()
    vendor_id = f"store-{uuid.uuid4().hex[:8]}"
    plain, digest = _new_code({str(item.get("code_hash") or "") for item in items})
    logo_name = ""
    if logo_bytes:
        logo_name = save_logo(vendor_id, logo_bytes, logo_suffix)
    receipt_name = ""
    if method == "instapay" and receipt_bytes:
        receipt_name = save_receipt(vendor_id, receipt_bytes, receipt_suffix)
    record = {
        "id": vendor_id,
        "name": name.strip(),
        "name_en": "",
        "logo": logo_name,
        "cover": "",
        "whatsapp": whatsapp.strip(),
        "shipping": _empty_shipping(),
        "address": address.strip(),
        "governorate": governorate,
        "plan": plan,
        "status": "active",
        "shop_status": "open",
        "primary": False,
        "code_hash": digest,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "subscription": {
            "status": "active",
            "plan": plan,
            "method": method,
            "amount": int(PLANS.get(plan) or 0),
            "receipt": receipt_name,
            "card_name": holder,
            "card_last4": last4,
            "paid_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    }
    items.append(record)
    _write(items)
    return record, plain


def subscription_days_left(vendor: dict, today: datetime | None = None) -> int:
    sub = vendor.get("subscription") or {}
    plan = str(sub.get("plan") or vendor.get("plan") or "")
    span = 30 if plan == "monthly" else 365 if plan == "yearly" else 0
    if span <= 0:
        return 0
    raw = str(sub.get("paid_at") or vendor.get("created") or "").strip()
    started = None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            started = datetime.strptime(raw, fmt)
            break
        except ValueError:
            continue
    if started is None:
        return 0
    now = today or datetime.now()
    elapsed = max(0, (now.date() - started.date()).days)
    return max(0, span - elapsed)


def update_vendor_profile(
    vendor_id: str,
    name: str,
    whatsapp: str,
    address: str,
    governorate: str,
    logo_bytes: bytes | None = None,
    logo_suffix: str = "",
    cover_bytes: bytes | None = None,
    cover_suffix: str = "",
) -> dict | None:
    items = load_vendors()
    found = None
    for item in items:
        if item.get("id") != vendor_id or item.get("primary"):
            continue
        item["name"] = name.strip()
        item["whatsapp"] = whatsapp.strip()
        item["address"] = address.strip()
        item["governorate"] = governorate
        if logo_bytes:
            item["logo"] = save_logo(vendor_id, logo_bytes, logo_suffix)
        if cover_bytes:
            item["cover"] = save_cover(vendor_id, cover_bytes, cover_suffix)
        found = item
        break
    if found is None:
        return None
    _write(items)
    return found


def update_vendor_shipping(vendor_id: str, default: int | None, overrides: dict[str, int]) -> dict | None:
    items = load_vendors()
    found = None
    for item in items:
        if item.get("id") != vendor_id or item.get("primary"):
            continue
        clean: dict[str, int] = {}
        for key, value in overrides.items():
            amount = _fee_amount(value)
            if amount is None:
                continue
            clean[str(key)] = amount
        item["shipping"] = {
            "default": None if default is None else int(default),
            "overrides": clean,
        }
        found = item
        break
    if found is None:
        return None
    _write(items)
    return found


def shop_status(vendor: dict | None) -> str:
    value = str((vendor or {}).get("shop_status") or "")
    if value in SHOP_STATUSES:
        return value
    return "open"


def set_shop_status(vendor_id: str, status: str) -> dict | None:
    if status not in SHOP_STATUSES:
        return None
    items = load_vendors()
    found = None
    for item in items:
        if item.get("id") != vendor_id:
            continue
        item["shop_status"] = status
        found = item
        break
    if found is None:
        return None
    _write(items)
    return found


def _norm_name(value: str) -> str:
    return " ".join(str(value or "").split()).casefold()


def _phones_match(saved: str, given: str) -> bool:
    left = wa_digits(saved)
    right = wa_digits(given)
    if len(left) < 8 or len(right) < 8:
        return False
    return left == right


def change_vendor_code(vendor_id: str, current: str, new_code: str) -> str:
    items = load_vendors()
    for item in items:
        if item.get("id") != vendor_id:
            continue
        if item.get("primary") and not str(item.get("code_hash") or ""):
            return "primary"
        given = str(current or "").strip()
        digest = str(item.get("code_hash") or "")
        if not given or not digest or hash_code(given) != digest:
            return "bad_current"
        fresh = str(new_code or "").strip()
        if len(fresh) < 4:
            return "bad_new"
        item["code_hash"] = hash_code(fresh)
        _write(items)
        return "ok"
    return "missing"


def reset_vendor_by_whatsapp(name: str, whatsapp: str) -> tuple[str, str]:
    wanted = _norm_name(name)
    if not wanted:
        return "not_found", ""
    items = load_vendors()
    matches = [
        item
        for item in items
        if _norm_name(item.get("name")) == wanted or _norm_name(item.get("name_en")) == wanted
    ]
    if not matches:
        return "not_found", ""
    usable: list[dict] = []
    saw_primary_without_code = False
    saw_missing_phone = False
    for item in matches:
        if item.get("primary") and not str(item.get("code_hash") or ""):
            saw_primary_without_code = True
            continue
        if len(wa_digits(str(item.get("whatsapp") or ""))) < 8:
            saw_missing_phone = True
            continue
        usable.append(item)
    if not usable:
        if saw_missing_phone and not saw_primary_without_code:
            return "no_whatsapp", ""
        if saw_primary_without_code:
            return "primary", ""
        if saw_missing_phone:
            return "no_whatsapp", ""
        return "not_found", ""
    chosen = next(
        (item for item in usable if _phones_match(str(item.get("whatsapp") or ""), whatsapp)),
        None,
    )
    if chosen is None:
        return "mismatch", ""
    plain, digest = _new_code({str(item.get("code_hash") or "") for item in items})
    chosen["code_hash"] = digest
    _write(items)
    return "ok", plain

