"""متجر نظارات مسلم: واجهة المتجر وواجهة الطلبات، لمحل واحد فقط."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import secrets
import sys
import threading
import uuid
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from notify import record_event, whatsapp_link
from paths import bundle_root, data_dir, user_glasses_dir
from platform_cfg import admin_hash
from products import (
    AUDIENCES,
    CATEGORIES,
    KINDS,
    StockError,
    delete_product,
    get_product,
    load_products,
    replace_product,
    reserve_stock,
)

WEB = Path(__file__).resolve().parent / "web"
LOCAL_PORTS = (8765, 8766, 8770)
LOCK = threading.Lock()
ADMIN_SESSIONS: set[str] = set()
ADMIN_COOKIE = "muslem_admin"
ASSET_NAME = re.compile(r"[a-z0-9_]+\.png")
TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml",
    ".webmanifest": "application/manifest+json",
}

SHOP = {
    "name": "مسلم",
    "name_en": "Muslem Optics",
    "address": "باب اللوق، القاهرة",
    "phone": "01148005679",
    "whatsapp": "https://wa.me/201148005679",
    "instagram": "https://www.instagram.com/muslimoptics?srtk=dDE0ODk1aDdicXFs",
    "facebook": "https://www.facebook.com/share/14soSm3zjRZ/?mibextid=wwXIfr",
    "instapay": "moslem.optics@instapay",
    "vodafone": "01148005679",
}

GOVERNORATES = {
    "القاهرة": (25, "1–2 يوم"),
    "الجيزة": (25, "1–2 يوم"),
    "القليوبية": (30, "1–2 يوم"),
    "الإسكندرية": (40, "2–3 أيام"),
    "البحيرة": (45, "2–3 أيام"),
    "المنوفية": (40, "2–3 أيام"),
    "الغربية": (45, "2–3 أيام"),
    "كفر الشيخ": (50, "2–4 أيام"),
    "الدقهلية": (45, "2–3 أيام"),
    "دمياط": (50, "2–4 أيام"),
    "الشرقية": (45, "2–3 أيام"),
    "بورسعيد": (50, "2–3 أيام"),
    "الإسماعيلية": (50, "2–3 أيام"),
    "السويس": (55, "2–4 أيام"),
    "الفيوم": (50, "2–4 أيام"),
    "بني سويف": (55, "2–4 أيام"),
    "المنيا": (60, "3–4 أيام"),
    "أسيوط": (65, "3–5 أيام"),
    "سوهاج": (70, "3–5 أيام"),
    "قنا": (75, "3–5 أيام"),
    "الأقصر": (75, "3–5 أيام"),
    "أسوان": (80, "4–6 أيام"),
    "البحر الأحمر": (90, "4–6 أيام"),
    "الوادي الجديد": (95, "4–6 أيام"),
    "مطروح": (90, "4–6 أيام"),
    "شمال سيناء": (100, "4–6 أيام"),
    "جنوب سيناء": (100, "4–6 أيام"),
}

LENSES = {
    "none": {"label": "الإطار كما هو", "price": 0},
    "plain": {"label": "عدسة طبية عادية", "price": 0},
    "blue": {"label": "عدسة Blue Cut", "price": 250},
    "sun": {"label": "عدسة طبية شمسية", "price": 450},
}

PAYMENTS = {
    "cod": "الدفع عند الاستلام",
    "instapay": "InstaPay",
    "vodafone": "فودافون كاش",
}

ORDER_STATUSES = ["تم التجهيز", "جاري التغليف", "خرج للتوصيل"]


def _orders_path() -> Path:
    return data_dir() / "orders.json"


def _load_orders() -> list[dict]:
    path = _orders_path()
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return payload if isinstance(payload, list) else []


def _save_orders(orders: list[dict]) -> None:
    path = _orders_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(orders, ensure_ascii=False, indent=2), encoding="utf-8")


def _clip(value, limit: int) -> str:
    return str(value or "").strip()[:limit]


def _number(value, low: float, high: float):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number < low or number > high:
        return None
    return round(number, 2)


def _clean_measures(raw) -> dict | None:
    if not isinstance(raw, dict):
        return None
    cleaned = {}
    for eye in ("od", "os"):
        block = raw.get(eye)
        if not isinstance(block, dict):
            continue
        sph = _number(block.get("sph"), -20, 20)
        cyl = _number(block.get("cyl"), -10, 10)
        axis = _number(block.get("axis"), 0, 180)
        if sph is None and cyl is None:
            continue
        cleaned[eye] = {
            "sph": 0 if sph is None else sph,
            "cyl": 0 if cyl is None else cyl,
            "axis": int(axis or 0),
        }
    return cleaned or None


def _public_products() -> list[dict]:
    items = []
    for item in load_products():
        if str(item.get("store_id") or "moslem") != "moslem":
            continue
        asset = Path(str(item.get("asset") or "")).name
        items.append(
            {
                "id": item["id"],
                "name": item["name"],
                "brand": item.get("brand") or SHOP["name"],
                "price": int(item["price"]),
                "old_price": int(item.get("old_price") or item["price"]),
                "category": item.get("category") or "",
                "kind": item.get("kind") or "طبية",
                "audience": item.get("audience") or "للجميع",
                "rating": item.get("rating") or 0,
                "sold": int(item.get("sold") or 0),
                "stock": int(item.get("stock") or 0),
                "color": item.get("color") or "",
                "description": item.get("description") or "",
                "face_shapes": list(item.get("face_shapes") or []),
                "badge": item.get("badge") or "",
                "image": f"/media/glasses/{asset}",
            }
        )
    return items


def _bootstrap() -> dict:
    return {
        "shop": SHOP,
        "products": _public_products(),
        "governorates": [
            {"name": name, "fee": fee, "eta": eta}
            for name, (fee, eta) in GOVERNORATES.items()
        ],
        "lenses": [
            {"id": key, "label": value["label"], "price": value["price"]}
            for key, value in LENSES.items()
        ],
        "payments": [{"id": key, "label": label} for key, label in PAYMENTS.items()],
    }


def _public_order(order: dict) -> dict:
    return {
        "id": order.get("id"),
        "created": order.get("created"),
        "status": order.get("status"),
        "name": order.get("name"),
        "phone": order.get("phone"),
        "address": order.get("address"),
        "governorate": order.get("governorate"),
        "eta": order.get("eta"),
        "fee": order.get("fee"),
        "subtotal": order.get("subtotal"),
        "total": order.get("total"),
        "payment": order.get("payment"),
        "payment_ref": order.get("payment_ref") or "",
        "note": order.get("note") or "",
        "measures": order.get("measures"),
        "lines": order.get("lines") or [],
        "whatsapp": order.get("whatsapp") or "",
    }


def _build_order(body: dict) -> dict:
    name = _clip(body.get("name"), 80)
    phone = _clip(body.get("phone"), 20)
    address = _clip(body.get("address"), 240)
    governorate = _clip(body.get("governorate"), 40)
    method = _clip(body.get("payment"), 20)
    reference = _clip(body.get("reference"), 48)
    note = _clip(body.get("note"), 500)
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(name) < 3:
        raise ValueError("اكتب الاسم الثلاثي.")
    if len(digits) < 10 or len(digits) > 15:
        raise ValueError("رقم الهاتف غير مكتمل.")
    if len(address) < 8:
        raise ValueError("اكتب العنوان بالتفصيل.")
    if governorate not in GOVERNORATES:
        raise ValueError("اختر المحافظة.")
    if method not in PAYMENTS:
        raise ValueError("اختر طريقة الدفع.")
    if method != "cod" and len(reference) < 4:
        raise ValueError("اكتب رقم عملية التحويل.")
    incoming = body.get("lines")
    if not isinstance(incoming, list) or not incoming or len(incoming) > 20:
        raise ValueError("السلة فارغة.")

    needed: dict[str, int] = {}
    lines = []
    for raw in incoming:
        if not isinstance(raw, dict):
            raise ValueError("بند غير صالح في السلة.")
        product_id = _clip(raw.get("product_id"), 80)
        product = get_product(product_id)
        if product is None or str(product.get("store_id") or "moslem") != "moslem":
            raise ValueError("أحد الإطارات لم يعد متاحاً.")
        try:
            qty = int(raw.get("qty") or 0)
        except (TypeError, ValueError):
            qty = 0
        if qty < 1 or qty > 5:
            raise ValueError("الكمية يجب أن تكون بين 1 و 5.")
        medical = product.get("kind") == "طبية"
        lens_key = _clip(raw.get("lens") or "", 20)
        if medical:
            if lens_key not in {"plain", "blue", "sun"}:
                lens_key = "plain"
        else:
            lens_key = "none"
        lens = LENSES[lens_key]
        unit = int(product["price"]) + int(lens["price"])
        needed[product_id] = needed.get(product_id, 0) + qty
        lines.append(
            {
                "product_id": product_id,
                "name": product["name"],
                "brand": product.get("brand") or SHOP["name"],
                "qty": qty,
                "price": unit,
                "frame_price": int(product["price"]),
                "lens": lens_key,
                "lens_label": lens["label"],
                "lens_price": int(lens["price"]),
                "kind": product.get("kind") or "",
                "image": f"/media/glasses/{Path(str(product.get('asset') or '')).name}",
            }
        )

    reserve_stock(needed)
    fee, eta = GOVERNORATES[governorate]
    subtotal = sum(int(line["qty"]) * int(line["price"]) for line in lines)
    measures = _clean_measures(body.get("measures"))
    if not any(line["kind"] == "طبية" for line in lines):
        measures = None
    orders = _load_orders()
    taken = {order.get("id") for order in orders}
    order_id = f"MO-{uuid.uuid4().hex[:6].upper()}"
    while order_id in taken:
        order_id = f"MO-{uuid.uuid4().hex[:6].upper()}"
    text = (
        f"مرحباً، أتممت طلباً من مسلم - Muslem Optics.\n"
        f"رقم الطلب: {order_id}\n"
        f"الإجمالي: {subtotal + fee} جنيه"
    )
    order = {
        "id": order_id,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": ORDER_STATUSES[0],
        "name": name,
        "phone": phone,
        "address": address,
        "governorate": governorate,
        "eta": eta,
        "fee": fee,
        "subtotal": subtotal,
        "total": subtotal + fee,
        "payment": PAYMENTS[method],
        "payment_method": method,
        "payment_ref": "" if method == "cod" else reference,
        "note": note,
        "measures": measures,
        "lines": lines,
        "store_id": "moslem",
        "whatsapp": whatsapp_link(SHOP["phone"], text),
    }
    orders.insert(0, order)
    _save_orders(orders)
    return order


def _admin_digest(code: str) -> str:
    return hashlib.sha256(code.strip().encode("utf-8")).hexdigest()


def _admin_password_ok(code: str) -> bool:
    given = str(code or "").strip()
    if not given:
        return False
    saved = admin_hash()
    if saved:
        return _admin_digest(given) == saved
    return given == os.environ.get("MUSLEM_ADMIN_PASSWORD", "")


def _cookie_token(header: str) -> str:
    for part in str(header or "").split(";"):
        name, _, value = part.strip().partition("=")
        if name == ADMIN_COOKIE:
            return value.strip()
    return ""


def _admin_product_view(item: dict) -> dict:
    asset = Path(str(item.get("asset") or "")).name
    return {
        "id": item.get("id"),
        "name": item.get("name") or "",
        "brand": item.get("brand") or "",
        "price": int(item.get("price") or 0),
        "old_price": int(item.get("old_price") or item.get("price") or 0),
        "category": item.get("category") or "",
        "kind": item.get("kind") or "طبية",
        "audience": item.get("audience") or "للجميع",
        "stock": int(item.get("stock") or 0),
        "badge": item.get("badge") or "",
        "image": f"/media/glasses/{asset}" if asset else "",
    }


def _store_upload(raw: str) -> str:
    payload = str(raw or "").strip()
    if not payload:
        return ""
    if "," in payload and payload.lower().startswith("data:"):
        payload = payload.split(",", 1)[1]
    try:
        binary = base64.b64decode(payload, validate=True)
    except Exception as exc:
        raise ValueError("تعذر قراءة الصورة.") from exc
    if not binary or len(binary) > 4_000_000:
        raise ValueError("الصورة أكبر من المسموح.")
    from PIL import Image

    image = Image.open(io.BytesIO(binary)).convert("RGBA")
    name = f"frame_{uuid.uuid4().hex[:10]}.png"
    dest = user_glasses_dir() / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, "PNG")
    return name


def _save_admin_product(body: dict) -> dict:
    name = _clip(body.get("name"), 80)
    brand = _clip(body.get("brand"), 40) or "نظارات مسلم"
    kind = _clip(body.get("kind"), 20)
    audience = _clip(body.get("audience"), 20)
    category = _clip(body.get("category"), 40)
    badge = _clip(body.get("badge"), 20)
    if len(name) < 2:
        raise ValueError("اكتب اسم الموديل.")
    if kind not in KINDS:
        raise ValueError("اختر نظارة شمسية أو طبية.")
    if audience not in AUDIENCES:
        raise ValueError("اختر القسم: رجالي أو حريمي أو أطفال.")
    if category not in CATEGORIES:
        category = CATEGORIES[0]
    if badge not in {"", "bestseller", "sale"}:
        badge = ""
    try:
        price = int(body.get("price"))
        old_price = int(body.get("old_price") if body.get("old_price") not in (None, "") else price)
        stock = int(body.get("stock") if body.get("stock") not in (None, "") else 8)
    except (TypeError, ValueError) as exc:
        raise ValueError("اكتب السعر بالأرقام.") from exc
    if price < 0 or old_price < 0 or stock < 0 or stock > 999:
        raise ValueError("السعر أو الكمية غير صالحة.")
    if old_price < price:
        old_price = price
    product_id = _clip(body.get("id"), 80)
    existing = get_product(product_id) if product_id else None
    if product_id and existing is None:
        raise ValueError("هذه النظارة لم تعد موجودة.")
    if not product_id:
        product_id = f"frame-{uuid.uuid4().hex[:8]}"
    asset = _store_upload(str(body.get("image") or ""))
    if not asset:
        asset = str((existing or {}).get("asset") or "")
    if not asset:
        raise ValueError("أضف صورة النظارة.")
    record = dict(existing or {})
    record.update(
        {
            "id": product_id,
            "name": name,
            "brand": brand,
            "price": price,
            "old_price": old_price,
            "kind": kind,
            "audience": audience,
            "category": category,
            "badge": badge,
            "stock": stock,
            "store_id": "moslem",
            "asset": Path(asset).name,
        }
    )
    replace_product(record)
    saved = get_product(product_id)
    return _admin_product_view(saved or record)


def ensure_assets() -> None:
    try:
        from generate_assets import main as generate

        folder = user_glasses_dir()
        if len(list(folder.glob("*.png"))) < 16:
            generate()
    except Exception as exc:
        print("asset generation failed:", exc)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        try:
            super().log_message(fmt, *args)
        except Exception:
            return

    def _send(self, code: int, payload: dict, extra: dict | None = None) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(raw)

    def _admin_token(self) -> str:
        return _cookie_token(self.headers.get("Cookie") or "")

    def _admin_authed(self) -> bool:
        token = self._admin_token()
        return bool(token) and token in ADMIN_SESSIONS

    def _file(self, path: Path, cache: str, body: bool = True) -> None:
        if not path.is_file():
            self.send_error(404)
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", TYPES.get(path.suffix.lower(), "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        if body:
            self.wfile.write(data)

    def _storefront(self, body: bool) -> None:
        self._file(WEB / "index.html", "no-cache", body)

    def do_HEAD(self) -> None:
        self._route(body=False)

    def do_GET(self) -> None:
        self._route(body=True)

    def _route(self, body: bool) -> None:
        path = unquote(urlparse(self.path).path) or "/"
        if len(path) > 1 and path.endswith("/"):
            path = path.rstrip("/")
        if path in {"/", "/index.html", "/index"}:
            self._storefront(body)
            return
        if path == "/admin":
            self._file(WEB / "admin.html", "no-cache", body)
            return
        if path == "/api/admin/products":
            if not self._admin_authed():
                self._send(401, {"error": "يلزم تسجيل الدخول."})
                return
            items = [
                _admin_product_view(item)
                for item in load_products()
                if str(item.get("store_id") or "moslem") == "moslem"
            ]
            self._send(200, {"products": items})
            return
        if path == "/health":
            self._send(200, {"ok": True, "shop": "moslem"})
            return
        if path == "/api/bootstrap":
            self._send(200, _bootstrap())
            return
        if path.startswith("/api/orders/"):
            wanted = path.split("/")[-1].strip().upper()
            found = next(
                (order for order in _load_orders() if str(order.get("id", "")).upper() == wanted),
                None,
            )
            if found is None:
                self._send(404, {"error": "لا يوجد طلب بهذا الرقم."})
                return
            self._send(200, _public_order(found))
            return
        if path.startswith("/media/glasses/"):
            name = Path(path).name
            if not ASSET_NAME.fullmatch(name):
                self.send_error(404)
                return
            self._file(user_glasses_dir() / name, "public, max-age=86400", body)
            return
        if path in {"/favicon.ico", "/favicon.png"}:
            icon = bundle_root() / "pwa" / "icons" / "icon-192.png"
            if not icon.is_file():
                icon = WEB / "favicon.png"
            self._file(icon, "public, max-age=86400", body)
            return
        rel = path.lstrip("/")
        target = (WEB / rel).resolve()
        root = WEB.resolve()
        if target != root and root not in target.parents:
            self.send_error(403)
            return
        if target.is_file() and target.suffix.lower() in TYPES:
            self._file(target, "no-cache", body)
            return
        if "." not in Path(path).name:
            self._storefront(body)
            return
        self.send_error(404)

    def _read_json(self, limit: int) -> dict | None:
        length = int(self.headers.get("Content-Length") or 0)
        if length < 0 or length > limit:
            self._send(413, {"error": "الطلب أكبر من المسموح."})
            return None
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send(400, {"error": "تعذر قراءة البيانات."})
            return None
        if not isinstance(body, dict):
            self._send(400, {"error": "بيانات ناقصة."})
            return None
        return body

    def _admin_post(self, path: str) -> None:
        body = self._read_json(6_000_000)
        if body is None:
            return
        if path == "/api/admin/login":
            if not _admin_password_ok(str(body.get("password") or "")):
                self._send(401, {"error": "كلمة السر غير صحيحة."})
                return
            token = secrets.token_urlsafe(24)
            ADMIN_SESSIONS.add(token)
            self._send(
                200,
                {"ok": True},
                {"Set-Cookie": f"{ADMIN_COOKIE}={token}; HttpOnly; Path=/; SameSite=Lax"},
            )
            return
        if not self._admin_authed():
            self._send(401, {"error": "يلزم تسجيل الدخول."})
            return
        if path == "/api/admin/logout":
            ADMIN_SESSIONS.discard(self._admin_token())
            self._send(
                200,
                {"ok": True},
                {"Set-Cookie": f"{ADMIN_COOKIE}=; HttpOnly; Path=/; Max-Age=0; SameSite=Lax"},
            )
            return
        if path == "/api/admin/products":
            try:
                with LOCK:
                    saved = _save_admin_product(body)
            except ValueError as exc:
                self._send(400, {"error": str(exc)})
                return
            self._send(200, saved)
            return
        if path == "/api/admin/products/delete":
            product_id = _clip(body.get("id"), 80)
            if not product_id or get_product(product_id) is None:
                self._send(404, {"error": "النظارة غير موجودة."})
                return
            with LOCK:
                delete_product(product_id, "moslem")
            self._send(200, {"ok": True})
            return
        self._send(404, {"error": "غير موجود."})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path.startswith("/api/admin/"):
            self._admin_post(path)
            return
        body = self._read_json(1_000_000)
        if body is None:
            return
        if path != "/api/orders":
            self._send(404, {"error": "غير موجود."})
            return
        if not isinstance(body, dict):
            self._send(400, {"error": "بيانات ناقصة."})
            return
        try:
            with LOCK:
                order = _build_order(body)
        except StockError as exc:
            self._send(409, {"error": str(exc)})
            return
        except ValueError as exc:
            self._send(400, {"error": str(exc)})
            return
        try:
            record_event(
                "order",
                store=SHOP["name"],
                total=int(order["total"]),
                phone=str(order["phone"]),
                order_id=str(order["id"]),
                vendor_id="moslem",
                store_id="moslem",
            )
        except Exception:
            pass
        self._send(201, _public_order(order))


def _listen() -> tuple[str, int, bool]:
    raw = os.environ.get("PORT", "").strip()
    if raw:
        return "0.0.0.0", int(raw), False
    return "127.0.0.1", 0, True


def serve() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ensure_assets()
    host, forced_port, local = _listen()
    ports = (forced_port,) if not local else LOCAL_PORTS
    httpd = None
    for port in ports:
        try:
            httpd = ThreadingHTTPServer((host, port), Handler)
        except OSError:
            continue
        shown = os.environ.get("RENDER_EXTERNAL_URL") or f"http://{host}:{httpd.server_address[1]}"
        print(f"مسلم - Muslem Optics  {shown}")
        if local:
            threading.Timer(0.8, lambda u=shown: webbrowser.open(u)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("stopped")
        finally:
            httpd.server_close()
        return
    raise SystemExit("تعذر فتح منفذ للمتجر.")


if __name__ == "__main__":
    serve()
