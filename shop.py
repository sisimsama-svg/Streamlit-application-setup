"""نظارات مسلم — باب اللوق. تجربة ارتداء، روشتة، ودفع محلي."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import uuid
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from PIL import Image

from generate_assets import main as generate_assets
from backup_export import backup_xlsx, backup_zip
from i18n import (
    GOV_EN,
    TERMS,
    direction,
    eta_label,
    gov_name,
    hero,
    join,
    lang,
    money,
    overlay_message,
    shape_advice,
    shape_label,
    stock_message,
    t,
    term,
)
from notify import list_notifications, record_event, wa_digits, whatsapp_link
from platform_cfg import (
    admin_hash,
    ensure_support_whatsapp,
    save_admin_hash,
    save_support_whatsapp,
    support_whatsapp,
)
from pdf_docs import admin_report_pdf, invoice_pdf, vendor_report_pdf
from paths import bundle_root, data_dir, sample_face_path
from products import (
    CATEGORIES,
    FACE_SHAPES,
    AUDIENCES,
    KINDS,
    PRIMARY_STORE,
    PRODUCTS,
    StockError,
    delete_product,
    get_product,
    load_products,
    product_image_dest,
    product_image_path,
    replace_product,
    reserve_stock,
)
from vendors import (
    DEMO_INSTAPAY,
    OFFICIAL_FACEBOOK,
    OFFICIAL_INSTAGRAM,
    OFFICIAL_WA_URL,
    PLANS,
    change_vendor_code,
    cover_path,
    fees_for_cart,
    get_vendor,
    list_active_vendors,
    load_vendors,
    logo_path,
    register_vendor,
    reset_vendor_by_whatsapp,
    set_shop_status,
    shop_status,
    subscription_days_left,
    update_vendor_profile,
    update_vendor_shipping,
    vendor_by_code,
)
from tryon import FACE_MESH_VERSION, detect_face_anchor, overlay_glasses

_PAGE_ICON = bundle_root() / "pwa" / "icons" / "icon-192.png"
if not _PAGE_ICON.is_file():
    _PAGE_ICON = bundle_root() / "assets" / "moslem.ico"
st.set_page_config(
    page_title="نظارات مسلم | Moslem Optics",
    page_icon=str(_PAGE_ICON) if _PAGE_ICON.is_file() else "👓",
    layout="wide",
    initial_sidebar_state="collapsed",
)
ensure_support_whatsapp()
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

ASSETS_READY = all(product_image_path(p).exists() for p in PRODUCTS)
if not ASSETS_READY:
    generate_assets()

SHOP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+Bhaijaan+2:wght@700;800&family=Cairo:wght@400;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Cairo', 'Tajawal', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    direction: rtl;
}

.stApp {
    background: #f4faf6;
    color: #2e3236;
}

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

a, .stApp a { color: #047857; }
a:hover, .stApp a:hover { color: #059669; }

.nv-top {
    background: #059669;
    color: #ffffff;
    padding: 12px 22px 14px;
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 18px;
    border: 1px solid #047857;
    border-bottom: 5px solid #047857;
    box-shadow: 0 10px 28px rgba(5, 150, 105, 0.16);
}
.nv-logo {
    width: 112px;
    height: 112px;
    object-fit: contain;
    display: block;
    flex: 0 0 auto;
    background: #ffffff;
    border-radius: 16px;
}
.nv-footer-logo {
    width: 88px;
    height: 88px;
    object-fit: contain;
    display: block;
    margin: 0 auto 10px;
    background: #ffffff;
    border-radius: 16px;
}
.nv-social {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}
.nv-footer .nv-social { justify-content: center; }
.nv-social a {
    color: #047857 !important;
    background: #ffffff;
    border: 1px solid #a7f3d0;
    border-radius: 999px;
    padding: 4px 12px;
    font-weight: 800;
    font-size: 13px;
    text-decoration: none !important;
    line-height: 1.5;
}
.nv-brand {
    font-family: 'Baloo Bhaijaan 2', 'Cairo', sans-serif;
    font-size: 28px;
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff;
}
.nv-en {
    font-size: 13px;
    letter-spacing: 0.12em;
    color: rgba(255, 255, 255, 0.82);
    font-weight: 700;
    margin-top: 2px;
}
.nv-sub { color: rgba(255, 255, 255, 0.92); font-size: 14px; line-height: 1.5; margin-top: 2px; }
.nv-cart-pill {
    background: #ffffff;
    color: #047857;
    border-radius: 999px;
    padding: 8px 16px;
    font-weight: 800;
    white-space: nowrap;
}

.nv-card {
    background: #fff;
    border-radius: 18px;
    padding: 14px;
    border: 1px solid #e4efe9;
    box-shadow: 0 8px 20px rgba(5, 150, 105, 0.05);
    height: 100%;
}
.nv-name { font-weight: 800; font-size: 18px; margin: 8px 0 2px; color: #2e3236; }
.nv-meta { color: #5c656c; font-size: 13px; }
.nv-price { color: #059669; font-weight: 800; font-size: 22px; }
.nv-old { color: #b0b4b8; text-decoration: line-through; margin-right: 8px; font-size: 14px; }
.nv-badge {
    background: #d1fae5;
    color: #047857;
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}
.nv-status { font-weight: 800; font-size: 13px; }
.nv-status-open { color: #059669; }
.nv-status-closed { color: #9f1239; }
.nv-status-maintenance { color: #b45309; }
.nv-hero {
    background: #fff;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 16px;
    border: 1px solid #e4efe9;
    border-right: 6px solid #059669;
    box-shadow: 0 8px 20px rgba(5, 150, 105, 0.05);
}
.nv-hero h2 { color: #2e3236; }
.nv-chip {
    display: inline-block;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-radius: 999px;
    padding: 6px 14px;
    margin: 0 6px 8px 0;
    font-weight: 700;
    color: #047857;
}
.nv-total {
    background: #059669;
    color: #fff;
    border-radius: 16px;
    padding: 16px;
}
.nv-advice {
    background: #fff;
    border-radius: 18px;
    padding: 16px 18px;
    border-right: 6px solid #059669;
    margin: 4px 0 14px;
    box-shadow: 0 8px 20px rgba(5, 150, 105, 0.05);
}
.nv-advice h3 { margin: 0 0 6px; font-size: 20px; color: #2e3236; }
.nv-advice p { margin: 0; color: #2e3236; line-height: 1.7; }
div.stButton > button {
    background: #059669;
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 800;
    height: 46px;
}
div.stButton > button:hover {
    background: #047857;
    color: white;
    border-color: #047857;
}
div.stButton > button:focus,
div.stButton > button:focus-visible {
    background: #059669;
    color: white;
    outline: 2px solid #047857;
    box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.35);
}
div[data-testid="stDownloadButton"] > button {
    background: #fff;
    color: #047857;
    border: 1.5px solid #059669;
    border-radius: 12px;
    font-weight: 800;
    height: 46px;
}
div[data-testid="stDownloadButton"] > button:hover,
div[data-testid="stDownloadButton"] > button:focus {
    background: #ecfdf5;
    color: #047857;
    border-color: #047857;
    box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.25);
}
.nv-steps {
    display: flex;
    gap: 8px;
    margin: 8px 0 14px;
}
.nv-step {
    flex: 1;
    background: #fff;
    border-radius: 14px;
    padding: 12px 8px;
    text-align: center;
    color: #5c656c;
    font-weight: 700;
    border: 1px solid #e4efe9;
}
.nv-step.done { background: #d1fae5; color: #047857; }
.nv-step.on { background: #059669; color: #fff; border-color: #047857; }
.nv-footer {
    margin-top: 32px;
    padding: 16px 8px 4px;
    border-top: 4px solid #059669;
    text-align: center;
    color: #047857;
    font-weight: 800;
}
.nv-policy p, .nv-policy li { line-height: 1.85; color: #2e3236; }

button[data-testid="stBaseButton-segmented_controlActive"],
[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stPills"] button[aria-selected="true"],
[data-testid="stPills"] button[aria-pressed="true"] {
    background: #059669 !important;
    color: #ffffff !important;
    border-color: #047857 !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus,
.stDateInput input:focus {
    border-color: #059669 !important;
    box-shadow: 0 0 0 1px #059669 !important;
}
</style>
"""


def _shop_css() -> str:
    side = "right" if lang() == "ar" else "left"
    css = SHOP_CSS.replace("direction: rtl", f"direction: {direction()}")
    css = css.replace("border-right: 6px solid #059669", f"border-{side}: 6px solid #059669")
    return css


st.markdown(_shop_css(), unsafe_allow_html=True)

LENS_OPTIONS = {
    "plain": {"label": "عادية", "price": 0},
    "blue": {"label": "Blue Cut", "price": 250},
    "sun": {"label": "طبية شمسية", "price": 450},
}

# الرسوم ومدة الوصول تقديرية لطلب تجريبي، وتُحسب من المحافظة المختارة.
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

PAYMENTS = {
    "cod": "الدفع عند الاستلام",
    "instapay": "InstaPay",
    "vodafone": "فودافون كاش",
}

ORDER_STATUSES = ["تم التجهيز", "جاري التغليف", "خرج للتوصيل"]
ADMIN_CODE = "1611"
_BLOCKED_SUPPORT = {"01000000000", "1000000000", "201000000000", "2001000000000"}
DATA_DIR = data_dir()
ORDERS_PATH = DATA_DIR / "orders.json"
RX_DIR = DATA_DIR / "rx"

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "page" not in st.session_state:
    st.session_state.page = "store"
if "tryon_product" not in st.session_state:
    _opening = load_products()
    st.session_state.tryon_product = _opening[0]["id"] if _opening else ""
if "face_bytes" not in st.session_state:
    st.session_state.face_bytes = None
if "ship_gov" not in st.session_state:
    st.session_state.ship_gov = "القاهرة"
if "pay_method" not in st.session_state:
    st.session_state.pay_method = "cod"
if "track_query" not in st.session_state:
    st.session_state.track_query = ""
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False
if "vendor_id" not in st.session_state:
    st.session_state.vendor_id = ""
if "vendor_code_once" not in st.session_state:
    st.session_state.vendor_code_once = ""
load_vendors()

notice = st.session_state.pop("notice", None)
if notice:
    st.toast(notice)


def _secret_digest(code: str) -> str:
    return hashlib.sha256(code.strip().encode("utf-8")).hexdigest()


def admin_code_matches(code: str) -> bool:
    given = str(code or "").strip()
    if not given:
        return False
    saved = admin_hash()
    if saved:
        return _secret_digest(given) == saved
    return given == ADMIN_CODE


def change_admin_code(current: str, new_code: str) -> str:
    if not admin_code_matches(current):
        return "bad_current"
    fresh = str(new_code or "").strip()
    if len(fresh) < 4:
        return "bad_new"
    save_admin_hash(_secret_digest(fresh))
    return "ok"


def _support_number_ok(number: str) -> bool:
    digits = wa_digits(number)
    if len(digits) < 8:
        return False
    if digits in _BLOCKED_SUPPORT or set(digits) <= {"0"}:
        return False
    return True


def cart_count() -> int:
    return sum(int(item["qty"]) for item in st.session_state.cart.values())


def cart_total() -> int:
    return sum(int(item["qty"]) * int(item["price"]) for item in st.session_state.cart.values())


def delivery_for(governorate: str) -> tuple[int, str]:
    return GOVERNORATES.get(governorate, (60, "3–5 أيام"))


def cart_shipping(governorate: str) -> tuple[int, str, list[tuple[str, int]]]:
    platform, eta = delivery_for(governorate)
    store_ids = [
        str(item.get("store_id") or PRIMARY_STORE) for item in st.session_state.cart.values()
    ]
    unique = list(dict.fromkeys(store_ids))
    vendors = {store_id: get_vendor(store_id) for store_id in unique}
    parts = fees_for_cart(store_ids, vendors, governorate, platform)
    total = sum(amount for _store_id, amount in parts)
    return total, eta, parts


def _lens_caption(key: str) -> str:
    lens = LENS_OPTIONS[key]
    extra = f"+{money(lens['price'])}" if lens["price"] else t("included")
    return f"{term(lens['label'])} ({extra})"


def _load_orders() -> list[dict]:
    if not ORDERS_PATH.exists():
        return []
    try:
        payload = json.loads(ORDERS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return payload if isinstance(payload, list) else []


def _save_orders(orders: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ORDERS_PATH.write_text(json.dumps(orders, ensure_ascii=False, indent=2), encoding="utf-8")


def _rx_suffix(name: str | None, mime: str) -> str:
    if name and "." in name:
        ext = Path(name).suffix.lower()
        if ext in {".jpg", ".jpeg", ".png", ".pdf"}:
            return ext
    if "png" in mime:
        return ".png"
    if "pdf" in mime:
        return ".pdf"
    return ".jpg"


def find_order(order_id: str) -> dict | None:
    wanted = order_id.strip().upper()
    for order in _load_orders():
        if str(order.get("id", "")).upper() == wanted:
            return order
    return None


def set_order_status(order_id: str, status: str) -> None:
    if status not in ORDER_STATUSES:
        return
    orders = _load_orders()
    for order in orders:
        if order.get("id") == order_id:
            order["status"] = status
            break
    _save_orders(orders)


def place_order(
    name: str,
    phone: str,
    address: str,
    governorate: str,
    method: str,
    reference: str,
) -> str:
    fee, eta, _parts = cart_shipping(governorate)
    subtotal = cart_total()
    RX_DIR.mkdir(parents=True, exist_ok=True)
    orders = _load_orders()
    taken = {order.get("id") for order in orders}
    order_id = f"MO-{uuid.uuid4().hex[:6].upper()}"
    while order_id in taken:
        order_id = f"MO-{uuid.uuid4().hex[:6].upper()}"
    needed: dict[str, int] = {}
    for item in st.session_state.cart.values():
        product_id = item.get("product_id")
        if product_id:
            needed[product_id] = needed.get(product_id, 0) + int(item["qty"])
    reserve_stock(needed)
    lines = []
    for line_id, item in st.session_state.cart.items():
        rx_file = None
        rx_bytes = item.get("rx_bytes")
        if rx_bytes:
            rx_file = f"{order_id}-{line_id}{_rx_suffix(item.get('rx_name'), item.get('rx_mime') or '')}"
            (RX_DIR / rx_file).write_bytes(rx_bytes)
        lines.append(
            {
                "name": item["name"],
                "qty": int(item["qty"]),
                "price": int(item["price"]),
                "frame_price": int(item.get("frame_price") or item["price"]),
                "lens_label": item.get("lens_label", "عادية"),
                "lens_price": int(item.get("lens_price") or 0),
                "measures": item.get("measures"),
                "rx_name": item.get("rx_name"),
                "rx_file": rx_file,
                "store_id": item.get("store_id") or PRIMARY_STORE,
            }
        )
    orders.insert(
        0,
        {
            "id": order_id,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": ORDER_STATUSES[0],
            "name": name.strip(),
            "phone": phone.strip(),
            "address": address.strip(),
            "governorate": governorate,
            "eta": eta,
            "fee": fee,
            "subtotal": subtotal,
            "total": subtotal + fee,
            "payment": PAYMENTS.get(method, method),
            "payment_ref": reference.strip() if method == "instapay" else "",
            "lines": lines,
        },
    )
    _save_orders(orders)
    try:
        _notify_order(order_id, phone.strip(), lines)
    except Exception:
        pass
    return order_id


def _notify_order(order_id: str, phone: str, lines: list[dict]) -> None:
    totals: dict[str, int] = {}
    for line in lines:
        store_id = str(line.get("store_id") or PRIMARY_STORE)
        totals[store_id] = totals.get(store_id, 0) + int(line.get("qty") or 0) * int(line.get("price") or 0)
    for store_id, total in totals.items():
        vendor = get_vendor(store_id)
        store = str((vendor or {}).get("name") or store_id)
        record_event(
            "order",
            store=store,
            total=total,
            phone=phone,
            order_id=order_id,
            vendor_id=store_id,
            store_id=store_id,
        )


def prescription_detail(item: dict) -> str:
    measures = item.get("measures")
    if measures:
        return t(
            "rx_detail",
            od_sph=f"{measures['od_sph']:+.2f}",
            od_cyl=f"{measures['od_cyl']:+.2f}",
            od_axis=measures["od_axis"],
            os_sph=f"{measures['os_sph']:+.2f}",
            os_cyl=f"{measures['os_cyl']:+.2f}",
            os_axis=measures["os_axis"],
            pd=measures["pd"],
        )
    if item.get("rx_name"):
        return t("rx_uploaded", name=item["rx_name"])
    return t("no_rx")


def prescription_summary(item: dict) -> str:
    measures = item.get("measures")
    if measures:
        return t(
            "manual_rx",
            od=f"{measures['od_sph']:+.2f}",
            os=f"{measures['os_sph']:+.2f}",
            pd=measures["pd"],
        )
    if item.get("rx_name"):
        return t("rx_uploaded", name=item["rx_name"])
    return t("no_rx")


def _orders_blocked_note(vendor: dict | None) -> str:
    status = shop_status(vendor)
    if status == "closed":
        return t("shop_closed_note")
    if status == "maintenance":
        return t("shop_maint_note")
    return ""


def _product_wa_text(product: dict, vendor: dict) -> str:
    store = str(vendor.get("name") or "المتجر")
    name = str(product.get("name") or "المنتج")
    return f"مرحباً، أريد الاستفسار عن {name} من متجر {store}."


def _store_wa_text(vendor: dict) -> str:
    store = str(vendor.get("name") or "المتجر")
    return f"مرحباً، أريد الاستفسار عن متجر {store}."


def add_configured(product: dict, lens_key: str, upload, measures: dict | None) -> None:
    vendor = get_vendor(str(product.get("store_id") or PRIMARY_STORE))
    blocked = _orders_blocked_note(vendor)
    if blocked:
        st.error(blocked)
        return
    lens = LENS_OPTIONS[lens_key]
    line_id = uuid.uuid4().hex[:10]
    st.session_state.cart[line_id] = {
        "name": product["name"],
        "frame_price": int(product["price"]),
        "lens_key": lens_key,
        "lens_label": lens["label"],
        "lens_price": int(lens["price"]),
        "price": int(product["price"]) + int(lens["price"]),
        "qty": 1,
        "product_id": product["id"],
        "store_id": product.get("store_id") or PRIMARY_STORE,
        "asset": product["asset"],
        "rx_name": upload.name if upload is not None else None,
        "rx_bytes": upload.getvalue() if upload is not None else None,
        "rx_mime": (upload.type or "") if upload is not None else "",
        "measures": measures,
    }
    st.session_state.notice = t("added", name=product["name"], lens=term(lens["label"]))


@st.dialog(t("lens_dialog"), width="large")
def configure_and_add(product_id: str) -> None:
    product = get_product(product_id)
    if product is None:
        st.error(t("gone"))
        return
    vendor = get_vendor(str(product.get("store_id") or PRIMARY_STORE))
    blocked = _orders_blocked_note(vendor)
    if blocked:
        st.warning(blocked)
        return
    if int(product.get("stock") or 0) < 1:
        st.error(t("out_of_stock"))
        return
    held = sum(int(item["qty"]) for item in st.session_state.cart.values() if item.get("product_id") == product["id"])
    if held >= int(product["stock"]):
        st.error(t("cart_holds", name=product["name"], stock=product["stock"]))
        return
    st.write(t("config_line", name=product["name"], price=money(product["price"]), stock=product["stock"]))
    lens_key = st.radio(t("lens_type"), list(LENS_OPTIONS), format_func=_lens_caption, horizontal=True)
    mode = st.radio(
        t("rx_data"),
        ["رفع صورة الروشتة", "إدخال المقاسات يدوياً"],
        format_func=term,
        horizontal=True,
    )
    upload = None
    measures = None
    if mode == "رفع صورة الروشتة":
        upload = st.file_uploader(
            t("rx_caption_img"),
            type=["jpg", "jpeg", "png", "pdf"],
            key=f"rx-file-{product_id}",
        )
    else:
        st.caption(t("rx_caption"))
        eye_r, eye_l = st.columns(2)
        with eye_r:
            st.markdown(f"**{t('right_eye')}**")
            od_sph = st.number_input(t("sph_r"), -20.0, 20.0, 0.0, 0.25, key=f"od-sph-{product_id}")
            od_cyl = st.number_input(t("cyl_r"), -10.0, 10.0, 0.0, 0.25, key=f"od-cyl-{product_id}")
            od_axis = st.number_input(t("axis_r"), 0, 180, 0, key=f"od-ax-{product_id}")
        with eye_l:
            st.markdown(f"**{t('left_eye')}**")
            os_sph = st.number_input(t("sph_l"), -20.0, 20.0, 0.0, 0.25, key=f"os-sph-{product_id}")
            os_cyl = st.number_input(t("cyl_l"), -10.0, 10.0, 0.0, 0.25, key=f"os-cyl-{product_id}")
            os_axis = st.number_input(t("axis_l"), 0, 180, 0, key=f"os-ax-{product_id}")
        pd = st.number_input(t("pd"), 50.0, 80.0, 62.0, 0.5, key=f"pd-{product_id}")
        measures = {
            "od_sph": round(float(od_sph), 2),
            "od_cyl": round(float(od_cyl), 2),
            "od_axis": int(od_axis),
            "os_sph": round(float(os_sph), 2),
            "os_cyl": round(float(os_cyl), 2),
            "os_axis": int(os_axis),
            "pd": round(float(pd), 1),
        }
    unit = int(product["price"]) + int(LENS_OPTIONS[lens_key]["price"])
    st.write(t("unit_price", price=money(unit)))
    if st.button(t("confirm_add"), width="stretch"):
        if mode == "رفع صورة الروشتة" and upload is None:
            st.error(t("need_rx"))
            return
        add_configured(product, lens_key, upload, measures)
        st.rerun()


def go(page: str, product_id: str | None = None) -> None:
    st.session_state.page = page
    if product_id:
        st.session_state.tryon_product = product_id
    st.rerun()


_WA_HELLO = "مرحباً، أريد الاستفسار من نظارات مسلم."


def _official_logo_src() -> str:
    assets = bundle_root() / "assets"
    path = assets / "moslem-logo.jpg"
    if not path.is_file():
        path = assets / "moslem-logo.png"
    if not path.is_file():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _social_bar() -> str:
    wa = f"{OFFICIAL_WA_URL}?text={quote(_WA_HELLO)}"
    links = (
        (wa, t("social_whatsapp")),
        (OFFICIAL_INSTAGRAM, t("social_instagram")),
        (OFFICIAL_FACEBOOK, t("social_facebook")),
    )
    anchors = "".join(
        '<a class="nv-social-link" href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'.format(
            href=href,
            label=label,
        )
        for href, label in links
    )
    return f'<div class="nv-social">{anchors}</div>'


cart_n = cart_count()
lang_col, _lang_space = st.columns([1.6, 4.4])
with lang_col:
    _lang_kwargs = {
        "format_func": lambda code: "العربية" if code == "ar" else "English",
        "key": "lang_choice",
        "width": "content",
    }
    if "lang_choice" not in st.session_state:
        _lang_kwargs["default"] = st.session_state.get("lang", "ar")
    picked_lang = st.segmented_control(t("language"), ["ar", "en"], **_lang_kwargs)
if picked_lang in ("ar", "en") and picked_lang != st.session_state.get("lang", "ar"):
    st.session_state.lang = picked_lang
    st.rerun()
brand_title = "نظارات مسلم" if lang() == "ar" else "Moslem Optics"
brand_en = "MOSLEM OPTICS" if lang() == "ar" else "نظارات مسلم"
_logo_src = _official_logo_src()
st.markdown(
    f"""
    <div class="nv-top">
        <img class="nv-logo" src="{_logo_src}" alt="نظارات مسلم">
        <div>
            <div class="nv-brand">{brand_title}</div>
            <div class="nv-en">{brand_en}</div>
            <div class="nv-sub">{t("loc_ar")}</div>
            {_social_bar()}
        </div>
        <div class="nv-cart-pill">{t("cart_pill", n=cart_n)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

nav1, nav2, nav3, nav4, nav5 = st.columns(5)
with nav1:
    if st.button(t("shop"), width="stretch"):
        go("store")
with nav2:
    if st.button(t("tryon"), width="stretch"):
        go("tryon")
with nav3:
    if st.button(t("cart_n", n=cart_n), width="stretch"):
        go("cart")
with nav4:
    if st.button(t("track"), width="stretch"):
        go("track")
with nav5:
    if st.button(t("admin"), width="stretch"):
        go("admin")
join_col, vendor_col = st.columns(2)
with join_col:
    if st.button(t("join_store"), width="stretch"):
        go("join")
with vendor_col:
    vendor_label = t("my_dashboard") if st.session_state.get("vendor_id") else t("vendor_login")
    if st.button(vendor_label, width="stretch"):
        go("vendor")
support_col, _support_space = st.columns([1.6, 4.4])
with support_col:
    _support_link = whatsapp_link(
        support_whatsapp(),
        "مرحباً، أحتاج دعماً فنياً في منصة نظارات مسلم.",
    )
    if _support_link:
        st.link_button(t("tech_support"), _support_link)
    else:
        st.button(t("tech_support"), disabled=True, key="support-wa-missing")
        st.caption(t("support_unset"))


def _search_blob(product: dict) -> str:
    store_id = str(product.get("store_id") or PRIMARY_STORE)
    vendor = get_vendor(store_id) or {}
    governorate = str(vendor.get("governorate") or "")
    values = [
        product.get("name"),
        product.get("brand"),
        product.get("color"),
        product.get("category"),
        product.get("kind"),
        product.get("audience"),
        " ".join(product.get("face_shapes") or []),
        vendor.get("name"),
        vendor.get("name_en"),
        governorate,
        GOV_EN.get(governorate, ""),
        vendor.get("address"),
    ]
    for value in (
        product.get("category"),
        product.get("kind"),
        product.get("audience"),
        *(product.get("face_shapes") or []),
    ):
        values.append(TERMS.get(str(value or ""), ""))
    return " ".join(str(value) for value in values if value).casefold()


def _matches_query(product: dict, query: str) -> bool:
    q = query.strip().casefold()
    if not q:
        return True
    return q in _search_blob(product)


def _area_choices() -> list[str]:
    found: list[str] = []
    for vendor in list_active_vendors():
        governorate = str(vendor.get("governorate") or "")
        if governorate and governorate not in found:
            found.append(governorate)
    found.sort(key=lambda name: (0 if name == "القاهرة" else 1, name))
    return ["الكل", *found]


def _area_label(value: str) -> str:
    if value == "الكل":
        return t("all_areas")
    return gov_name(value)


def _store_choice_label(sid: str) -> str:
    if sid == "الكل":
        return t("all_stores")
    vendor = get_vendor(sid)
    return f"{_vendor_name(sid)} — {t('shop_' + shop_status(vendor))}"


def _render_store_board() -> None:
    vendors = list_active_vendors()
    if not vendors:
        return
    st.subheader(t("stores_heading"))
    for vendor in vendors:
        status_key = shop_status(vendor)
        cover = cover_path(vendor)
        if cover is not None:
            st.image(str(cover), width="stretch")
        mark = logo_path(vendor)
        if mark is not None:
            st.image(str(mark), width=72)
        st.markdown(
            f"**{_vendor_name(vendor.get('id'))}** — "
            f"<span class='nv-status nv-status-{status_key}'>{t('shop_' + status_key)}</span>",
            unsafe_allow_html=True,
        )
        link = whatsapp_link(str(vendor.get("whatsapp") or ""), _store_wa_text(vendor))
        if link:
            st.link_button(t("wa_store"), link, key=f"store-wa-{vendor.get('id')}")
        else:
            st.caption(t("no_store_whatsapp"))


def _vendor_name(store_id: str | None) -> str:
    vendor = get_vendor(str(store_id or PRIMARY_STORE))
    if vendor is None:
        return "نظارات مسلم"
    if lang() == "en" and vendor.get("name_en"):
        return str(vendor["name_en"])
    return str(vendor.get("name") or "نظارات مسلم")


def _plan_label(plan: str) -> str:
    if plan == "monthly":
        return t("plan_monthly", price=money(PLANS["monthly"]))
    if plan == "yearly":
        return t("plan_yearly", price=money(PLANS["yearly"]))
    return t("plan_primary")


def _sub_method(method: str) -> str:
    labels = {
        "instapay": t("pay_insta"),
        "card": t("pay_card"),
        "visa": t("pay_card"),
        "apple": t("pay_apple"),
        "cash": t("pay_cash"),
        "vodafone": t("pay_voda"),
    }
    if method in labels:
        return labels[method]
    if not method:
        return t("method_none")
    return str(method)


def render_store() -> None:
    st.markdown(hero(t("hero_title"), t("hero_body")), unsafe_allow_html=True)
    st.caption(t("marketplace_note"))
    _render_store_board()

    catalog = load_products()
    active_ids = {item["id"] for item in list_active_vendors()}
    catalog = [item for item in catalog if item.get("store_id") in active_ids]
    store_ids = ["الكل"] + [item["id"] for item in list_active_vendors()]
    pick_store, pick_area = st.columns(2)
    with pick_store:
        picked_store = st.selectbox(
            t("store_filter"),
            store_ids,
            format_func=_store_choice_label,
        )
    with pick_area:
        picked_area = st.selectbox(t("gov_filter"), _area_choices(), format_func=_area_label)
    cats = ["الكل"] + sorted({p["category"] for p in catalog})
    query = st.text_input(t("search"), placeholder=t("search_ph"))
    f1, f2, f3 = st.columns(3)
    with f1:
        kind = st.selectbox(t("use"), ["الكل", *KINDS], format_func=term)
    with f2:
        audience = st.selectbox(t("audience"), ["الكل", *AUDIENCES], format_func=term)
    with f3:
        category = st.selectbox(t("frame_shape"), cats, format_func=term)

    filtered = catalog
    if picked_store != "الكل":
        filtered = [p for p in filtered if p.get("store_id") == picked_store]
    if picked_area != "الكل":
        area_ids = {
            item["id"]
            for item in list_active_vendors()
            if str(item.get("governorate") or "") == picked_area
        }
        filtered = [p for p in filtered if p.get("store_id") in area_ids]
    if kind != "الكل":
        filtered = [p for p in filtered if p.get("kind") == kind]
    if audience != "الكل":
        filtered = [p for p in filtered if p.get("audience") == audience]
    if category != "الكل":
        filtered = [p for p in filtered if p["category"] == category]
    if query:
        filtered = [p for p in filtered if _matches_query(p, query)]
    filtered.sort(key=lambda product: 0 if product.get("store_id") == PRIMARY_STORE else 1)

    if not filtered:
        st.info(t("no_results"))
        return

    if picked_store != "الكل":
        chosen_cover = cover_path(get_vendor(picked_store))
        if chosen_cover is not None:
            st.image(str(chosen_cover), width="stretch")

    rows = [filtered[i : i + 4] for i in range(0, len(filtered), 4)]
    for row in rows:
        cols = st.columns(4)
        for col, product in zip(cols, row):
            with col:
                st.markdown('<div class="nv-card">', unsafe_allow_html=True)
                st.image(str(product_image_path(product)), width="stretch")
                card_vendor = get_vendor(str(product.get("store_id") or PRIMARY_STORE)) or {}
                mark = logo_path(card_vendor)
                if mark is not None:
                    st.image(str(mark), width=56)
                shapes = join(term(shape) for shape in (product.get("face_shapes") or []))
                stock = int(product.get("stock") or 0)
                stock_label = t("sold_out") if stock <= 0 else t("left", n=stock)
                old_price = (
                    f'<span class="nv-old">{money(product["old_price"])}</span>'
                    if int(product.get("old_price") or 0) > int(product["price"])
                    else ""
                )
                kind_label = term(product.get("kind", "طبية"))
                audience_label = term(product.get("audience", "للجميع"))
                status_key = shop_status(card_vendor)
                blocked = _orders_blocked_note(card_vendor)
                st.markdown(
                    f"""
                    <span class="nv-badge">{kind_label} · {audience_label}</span>
                    <div class="nv-name">{product['name']}</div>
                    <div class="nv-meta">{t("sold_by", store=_vendor_name(product.get("store_id")))}</div>
                    <div class="nv-status nv-status-{status_key}">{t("shop_" + status_key)}</div>
                    <div class="nv-meta">{term(product['category'])} · {product['brand']} · ⭐ {product['rating']} · {stock_label}</div>
                    <div class="nv-meta">{t("suits", shapes=shapes)}</div>
                    <div><span class="nv-price">{money(product['price'])}</span>
                    {old_price}</div>
                    """,
                    unsafe_allow_html=True,
                )
                b1, b2 = st.columns(2)
                with b1:
                    if st.button(
                        t("add_to_cart") if stock else t("sold_out"),
                        key=f"add-{product['id']}",
                        width="stretch",
                        disabled=stock <= 0 or bool(blocked),
                    ):
                        configure_and_add(product["id"])
                with b2:
                    if st.button(t("try"), key=f"try-{product['id']}", width="stretch"):
                        go("tryon", product["id"])
                if blocked:
                    st.caption(blocked)
                product_link = whatsapp_link(
                    str(card_vendor.get("whatsapp") or ""),
                    _product_wa_text(product, card_vendor),
                )
                if product_link:
                    st.link_button(t("wa_product"), product_link, key=f"wa-product-{product['id']}")
                else:
                    st.caption(t("no_store_whatsapp"))
                st.markdown("</div>", unsafe_allow_html=True)


def _load_face() -> Image.Image | None:
    if st.session_state.face_bytes:
        return Image.open(io.BytesIO(st.session_state.face_bytes)).convert("RGB")
    return None


@st.cache_data(show_spinner=False)
def _cached_anchor(image_bytes: bytes, _version: str) -> dict | None:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return detect_face_anchor(image)


def _init_tryon_controls() -> None:
    st.session_state.setdefault("try_scale", 100)
    st.session_state.setdefault("try_dx", 0)
    st.session_state.setdefault("try_dy", 0)
    st.session_state.setdefault("try_rot", 0)


def _share_result(image: Image.Image, filename: str) -> None:
    share = image.convert("RGB")
    if max(share.size) > 1200:
        share.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    share.save(buffer, format="JPEG", quality=88)
    payload = base64.b64encode(buffer.getvalue()).decode("ascii")
    st.iframe(
        f"""
        <style>
          html,body{{margin:0;padding:0;overflow:hidden;background:transparent;}}
          #nv-share{{width:100%;height:46px;border:none;border-radius:12px;
            background:#059669;color:#fff;font-weight:800;font-size:16px;cursor:pointer;}}
          #nv-share:hover,#nv-share:focus{{background:#047857;outline:2px solid #047857;}}
        </style>
        <div style="font-family: Cairo, Tajawal, Tahoma, sans-serif; direction: {direction()};">
          <button id="nv-share">{t("share_look")}</button>
          <div id="nv-share-status" style="margin-top:8px;font-size:13px;color:#444;min-height:18px;"></div>
        </div>
        <script>
        const btn = document.getElementById("nv-share");
        const status = document.getElementById("nv-share-status");
        btn.onclick = async () => {{
          status.textContent = "";
          const blob = await (await fetch("data:image/jpeg;base64,{payload}")).blob();
          const file = new File([blob], "{filename}", {{type: "image/jpeg"}});
          const payload = {{
            title: "{t("share_title")}",
            text: "{t("share_text")}",
            files: [file]
          }};
          try {{
            if (navigator.share && (!navigator.canShare || navigator.canShare(payload))) {{
              await navigator.share(payload);
              status.textContent = "{t("share_opened")}";
              return;
            }}
          }} catch (error) {{
            if (error && error.name === "AbortError") return;
          }}
          try {{
            await navigator.clipboard.write([new ClipboardItem({{"image/jpeg": blob}})]);
            status.textContent = "{t("share_copied")}";
            return;
          }} catch (error) {{}}
          status.textContent = "{t("share_unavailable")}";
        }};
        </script>
        """,
        height=72,
    )


def _recommended_products(shape: dict | None) -> list[dict]:
    if not shape:
        return []
    label = shape.get("label")
    wanted = set(shape.get("categories") or [])
    matched = []
    for item in load_products():
        if int(item.get("stock") or 0) <= 0:
            continue
        shapes = item.get("face_shapes") or []
        if label and shapes:
            if label in shapes:
                matched.append(item)
        elif item.get("category") in wanted:
            matched.append(item)
    return matched


def render_tryon() -> None:
    _init_tryon_controls()
    st.markdown(hero(t("tryon_title"), t("tryon_body"), "#666"), unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.2])
    with left:
        source = st.radio(t("image_source"), ["رفع صورة", "الكاميرا"], format_func=term, horizontal=True)
        uploaded = None
        camera = None
        if source == "رفع صورة":
            uploaded = st.file_uploader(t("face_photo"), type=["jpg", "jpeg", "png"])
        else:
            camera = st.camera_input(t("take_photo"))

        file_obj = uploaded or camera
        if file_obj is not None:
            st.session_state.face_bytes = file_obj.getvalue()
        demo_path = sample_face_path()
        if demo_path.exists() and st.button(t("use_sample"), width="stretch"):
            st.session_state.face_bytes = demo_path.read_bytes()
            st.rerun()

        face = _load_face()
        anchor = None
        if face is not None:
            with st.spinner(t("locating_eyes")):
                anchor = _cached_anchor(st.session_state.face_bytes, FACE_MESH_VERSION)
        shape = (anchor or {}).get("shape") if anchor and anchor.get("method") == "facemesh" else None

        if face is None:
            st.info(t("advisor_prompt"))
        elif shape:
            names_text = join(item["name"] for item in _recommended_products(shape))
            tilt = t("tilt_note") if abs(float(shape.get("yaw") or 0)) > 18 else ""
            st.markdown(
                f"""
                <div class="nv-advice">
                    <h3>{t("advisor_title", label=shape_label(shape))}</h3>
                    <p>{shape_advice(shape)}{tilt}</p>
                    <p style="margin-top:8px"><b>{t("suggested")}</b> {names_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            filtered = bool(st.session_state.get("advisor_only"))
            if st.button(
                t("show_all") if filtered else t("show_matches"),
                width="stretch",
            ):
                st.session_state.advisor_only = not filtered
                if st.session_state.advisor_only:
                    suggested = [item["id"] for item in _recommended_products(shape)]
                    if suggested and st.session_state.tryon_product not in suggested:
                        st.session_state.tryon_product = suggested[0]
                st.rerun()
        else:
            st.info(t("face_unclear"))

        all_products = load_products()
        catalog = _recommended_products(shape) if shape and st.session_state.get("advisor_only") else all_products
        if not catalog:
            catalog = all_products
        if not catalog:
            st.info(t("no_products"))
            return
        if st.session_state.tryon_product not in {item["id"] for item in catalog}:
            st.session_state.tryon_product = catalog[0]["id"]
        names = {
            item["id"]: f"{item['name']} — {_vendor_name(item.get('store_id'))} — {money(item['price'])}"
            for item in catalog
        }
        selected_id = st.selectbox(
            t("choose_glasses"),
            list(names.keys()),
            index=[item["id"] for item in catalog].index(st.session_state.tryon_product),
            format_func=lambda pid: names[pid],
        )
        st.session_state.tryon_product = selected_id
        product = get_product(selected_id)
        if product is None:
            st.error(t("gone"))
            return
        st.image(str(product_image_path(product)), caption=product["name"], width="stretch")
        st.write(product["description"])
        try_vendor = get_vendor(str(product.get("store_id") or PRIMARY_STORE))
        st.caption(
            f"{t('sold_by', store=_vendor_name(product.get('store_id')))} — {t('shop_' + shop_status(try_vendor))}"
        )
        try_blocked = _orders_blocked_note(try_vendor)

        st.markdown(f"**{t('manual_fit')}**")
        if st.button(t("reset_fit"), width="stretch"):
            st.session_state.try_scale = 100
            st.session_state.try_dx = 0
            st.session_state.try_dy = 0
            st.session_state.try_rot = 0
            st.rerun()
        st.slider(t("size"), 50, 180, key="try_scale", help=t("size_help"))
        st.slider(t("shift_x"), -80, 80, key="try_dx", help=t("shift_help"))
        st.slider(t("shift_y"), -80, 80, key="try_dy", help=t("shift_help"))
        st.slider(t("angle"), -30, 30, key="try_rot", help=t("angle_help"))

        in_stock = int(product.get("stock") or 0) > 0
        if try_blocked:
            st.warning(try_blocked)
        if st.button(
            t("add_frame") if in_stock else t("frame_gone"),
            width="stretch",
            disabled=not in_stock or bool(try_blocked),
        ):
            configure_and_add(product["id"])

    with right:
        if face is None:
            st.info(t("upload_face"))
            return
        result, message, method = overlay_glasses(
            face,
            product_image_path(product),
            scale=st.session_state.try_scale / 100.0,
            offset_x=st.session_state.try_dx / 100.0,
            offset_y=st.session_state.try_dy / 100.0,
            angle_delta=float(st.session_state.try_rot),
            anchor=anchor,
        )
        shown = overlay_message(message)
        st.image(result, width="stretch")
        if method == "facemesh":
            st.success(shown)
        elif method:
            st.warning(shown)
        else:
            st.error(shown)
        png = io.BytesIO()
        result.save(png, format="PNG")
        save_col, share_col = st.columns(2)
        with save_col:
            st.download_button(
                t("save_look"),
                data=png.getvalue(),
                file_name=f"tryon-{product['id']}.png",
                mime="image/png",
                width="stretch",
            )
        with share_col:
            _share_result(result, f"tryon-{product['id']}.jpg")
        st.caption(t("share_hint"))


def _phone_digits(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def _gov_option(name: str) -> str:
    fee, eta = GOVERNORATES[name]
    return f"{gov_name(name)} — {money(fee)} · {eta_label(eta)}"


def _line_sales(orders: list[dict]) -> int:
    total = 0
    for order in orders:
        for line in order.get("lines") or []:
            total += int(line.get("qty") or 0) * int(line.get("price") or 0)
    return total


def _pdf_download(label: str, payload: bytes | None, filename: str, key: str) -> None:
    if not payload:
        return
    st.download_button(label, data=payload, file_name=filename, mime="application/pdf", key=key, width="stretch")


def _invoice_button(order_id: str, key: str) -> None:
    order = find_order(order_id)
    if not order:
        return
    try:
        payload = invoice_pdf(order)
    except Exception:
        st.error(t("pdf_failed"))
        return
    _pdf_download(t("download_invoice"), payload, f"invoice-{order['id']}.pdf", key)


def _render_notifications(store_id: str | None = None) -> None:
    st.subheader(t("notifications"))
    items = list_notifications(store_id)[:8]
    if not items:
        st.caption(t("no_notifications"))
        return
    for item in items:
        if item.get("type") == "subscription":
            title = t("notif_sub", store=item.get("store") or "", total=money(item.get("total") or 0))
            message = t(
                "wa_sub",
                store=item.get("store") or "",
                total=money(item.get("total") or 0),
                phone=item.get("phone") or "",
            )
        else:
            title = t(
                "notif_order",
                id=item.get("order_id") or "",
                store=item.get("store") or "",
                total=money(item.get("total") or 0),
            )
            message = t(
                "wa_order",
                id=item.get("order_id") or "",
                store=item.get("store") or "",
                total=money(item.get("total") or 0),
                phone=item.get("phone") or "",
            )
        st.write(f"{title} · {item.get('created') or ''}")
        link = whatsapp_link(str(item.get("phone") or ""), message)
        if link:
            st.link_button(t("open_whatsapp"), link, key=f"wa-{item.get('id')}")


def render_cart() -> None:
    st.markdown(hero(t("cart_title"), t("cart_body"), "#666"), unsafe_allow_html=True)
    if not st.session_state.cart:
        notice = st.session_state.pop("order_notice", None)
        if st.session_state.pop("celebrate", None):
            st.balloons()
        if notice:
            st.success(notice)
        last = st.session_state.get("last_order")
        if last:
            st.success(t("last_order", id=last))
            _invoice_button(str(last), f"invoice-cart-{last}")
            if st.button(t("follow_order"), width="stretch"):
                go("track")
        st.warning(t("empty_cart"))
        return

    items = list(st.session_state.cart.items())
    for line_id, item in items:
        with st.container(border=True):
            photo, info, qty_col, delete_col = st.columns([1.1, 3.2, 1.1, 0.8])
            with photo:
                if item.get("asset"):
                    st.image(str(product_image_path(item)), width="stretch")
            with info:
                lens_price = int(item.get("lens_price") or 0)
                lens_label = term(item.get("lens_label", "عادية"))
                frame_price = int(item.get("frame_price") or item["price"])
                st.markdown(f"**{item['name']}**")
                st.caption(t("frame_line", frame=money(frame_price), lens=lens_label, extra=money(lens_price)))
                st.write(prescription_summary(item))
                rx_bytes = item.get("rx_bytes")
                mime = item.get("rx_mime") or ""
                if rx_bytes and mime.startswith("image/"):
                    st.image(rx_bytes, caption=item.get("rx_name") or t("rx_caption_img"), width=180)
                elif item.get("rx_name"):
                    st.caption(t("rx_file", name=item["rx_name"]))
            with qty_col:
                live = get_product(item.get("product_id") or "")
                available = int(live["stock"]) if live else 10
                ceiling = max(int(item["qty"]), available, 1)
                qty = st.number_input(t("qty"), 1, ceiling, min(int(item["qty"]), ceiling), key=f"qty-{line_id}")
                st.session_state.cart[line_id]["qty"] = int(qty)
                st.write(f"**{money(int(qty) * int(item['price']))}**")
            with delete_col:
                if st.button(t("delete"), key=f"del-{line_id}"):
                    del st.session_state.cart[line_id]
                    st.rerun()

    subtotal = cart_total()
    gov = st.selectbox(t("gov"), list(GOVERNORATES), key="ship_gov", format_func=_gov_option)
    fee, eta, parts = cart_shipping(gov)
    grand = subtotal + fee
    lines = "<br>".join(
        t("store_ship_line", store=_vendor_name(store_id), fee=money(amount))
        for store_id, amount in parts
    )
    st.markdown(
        f"""
        <div class="nv-total">
            {t("totals_detail", sub=money(subtotal), gov=gov_name(gov), fee=money(fee), eta=eta_label(eta), grand=money(grand), lines=lines)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(t("ship_details"))
    name = st.text_input(t("full_name"), key="ship_name")
    phone = st.text_input(t("mobile"), key="ship_phone")
    address = st.text_area(t("address"), key="ship_address")

    st.subheader(t("pay_heading"))
    method = st.radio(
        t("pay_method"),
        list(PAYMENTS),
        format_func=lambda key: term(PAYMENTS[key]),
        horizontal=True,
        key="pay_method",
    )
    reference = ""
    sender_wallet = ""
    if method == "instapay":
        st.info(t("instapay_info", grand=money(grand)))
        reference = st.text_input(t("instapay_ref"), key="instapay_ref")
    elif method == "vodafone":
        st.info(t("vf_info", grand=money(grand)))
        sender_wallet = st.text_input(t("vf_wallet"), key="vf_wallet")
    else:
        st.info(t("cod_info", grand=money(grand), gov=gov_name(gov)))

    cart_blocks = []
    for item in st.session_state.cart.values():
        note = _orders_blocked_note(get_vendor(str(item.get("store_id") or PRIMARY_STORE)))
        if note and note not in cart_blocks:
            cart_blocks.append(note)
    for note in cart_blocks:
        st.warning(note)

    if st.button(t("confirm_order"), width="stretch", disabled=bool(cart_blocks)):
        missing = []
        if not name.strip() or not phone.strip() or not address.strip():
            missing.append(t("need_contact"))
        if len(_phone_digits(phone)) < 10:
            missing.append(t("bad_phone"))
        if method == "instapay" and len(reference.strip()) < 4:
            missing.append(t("need_instapay"))
        if method == "vodafone" and len(_phone_digits(sender_wallet)) < 10:
            missing.append(t("need_wallet"))
        if missing:
            for message in missing:
                st.error(message)
        else:
            try:
                order_id = place_order(name, phone, address, gov, method, reference)
            except StockError as error:
                st.error(stock_message(error))
                return
            st.session_state.cart = {}
            st.session_state.last_order = order_id
            st.session_state.track_query = order_id
            st.session_state.order_notice = t(
                "order_ok",
                name=name.strip(),
                id=order_id,
                status=term(ORDER_STATUSES[0]),
                gov=gov_name(gov),
                eta=eta_label(eta),
                pay=term(PAYMENTS[method]),
                grand=money(grand),
            )
            st.session_state.celebrate = True
            st.rerun()


def _status_steps(status: str) -> str:
    current = ORDER_STATUSES.index(status) if status in ORDER_STATUSES else 0
    parts = []
    for index, label in enumerate(ORDER_STATUSES):
        kind = "on" if index == current else "done" if index < current else ""
        parts.append(f'<div class="nv-step {kind}">{index + 1}. {term(label)}</div>')
    return f'<div class="nv-steps">{"".join(parts)}</div>'


def render_track() -> None:
    st.markdown(hero(t("track_title"), t("track_body"), "#666"), unsafe_allow_html=True)
    query = st.text_input(t("order_no"), key="track_query", placeholder=t("order_ph"))
    if not query.strip():
        st.info(t("order_hint"))
        return
    order = find_order(query)
    if order is None:
        st.error(t("order_missing"))
        return
    st.markdown(f"### {t('order_heading', id=order['id'])}")
    st.caption(
        t(
            "track_meta",
            created=order["created"],
            gov=gov_name(order["governorate"]),
            eta=eta_label(order["eta"]),
        )
    )
    st.markdown(_status_steps(order["status"]), unsafe_allow_html=True)
    st.write(t("status_now", status=term(order["status"])))
    for line in order.get("lines") or []:
        st.write(t("line_item", name=line["name"], qty=line["qty"], lens=term(line["lens_label"])))
    st.caption(t("track_total", total=money(order["total"]), pay=term(order["payment"])))
    _invoice_button(str(order["id"]), f"invoice-track-{order['id']}")


def _rx_bytes(rx_file: str | None) -> bytes | None:
    if not rx_file:
        return None
    path = RX_DIR / Path(rx_file).name
    if not path.is_file():
        return None
    return path.read_bytes()


def _store_png(upload, dest: Path) -> str | None:
    if upload is None:
        return "png_required"
    raw = upload.getvalue()
    if not raw:
        return "png_empty"
    if len(raw) > 8_000_000:
        return "png_large"
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except Exception:
        return "png_unreadable"
    if image.format != "PNG":
        return "png_format"
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest, format="PNG")
    return None


def _render_product_admin(store_id: str = PRIMARY_STORE) -> None:
    st.subheader(t("add_glasses"))
    st.caption(t("add_help"))
    with st.form(f"add-glasses-{store_id}", clear_on_submit=True):
        new_name = st.text_input(t("glasses_name"))
        price_col, stock_col = st.columns(2)
        with price_col:
            new_price = st.number_input(t("price_egp"), min_value=1, max_value=20000, value=199, step=1)
        with stock_col:
            new_stock = st.number_input(t("stock"), min_value=0, max_value=999, value=5, step=1)
        new_category = st.selectbox(t("frame_shape"), CATEGORIES, format_func=term)
        kind_col, audience_col = st.columns(2)
        with kind_col:
            new_kind = st.selectbox(t("use"), KINDS, format_func=term)
        with audience_col:
            new_audience = st.selectbox(t("audience"), AUDIENCES, index=AUDIENCES.index("للجميع"), format_func=term)
        new_shapes = st.multiselect(t("face_match"), FACE_SHAPES, default=["بيضاوي"], format_func=term)
        new_image = st.file_uploader(t("png_image"), type=["png"])
        submitted = st.form_submit_button(t("add_glasses_btn"), width="stretch")
    if submitted:
        shapes = [shape for shape in new_shapes if shape in FACE_SHAPES]
        if not new_name.strip():
            st.error(t("name_required"))
        elif not shapes:
            st.error(t("shape_required"))
        else:
            product_id = f"custom-{uuid.uuid4().hex[:8]}"
            asset = f"{product_id}.png"
            error = _store_png(new_image, product_image_dest({"asset": asset}))
            if error:
                st.error(t(error))
            else:
                shape_text = "، ".join(shapes)
                replace_product(
                    {
                        "id": product_id,
                        "name": new_name.strip(),
                        "brand": _vendor_name(store_id),
                        "store_id": store_id,
                        "price": int(new_price),
                        "old_price": int(new_price),
                        "category": new_category,
                        "kind": new_kind,
                        "audience": new_audience,
                        "rating": 5.0,
                        "sold": 0,
                        "color": new_category,
                        "description": f"إطار {new_category} يناسب شكل الوجه: {shape_text}.",
                        "asset": asset,
                        "stock": int(new_stock),
                        "face_shapes": shapes,
                    },
                    store_id=store_id,
                )
                st.session_state.notice = t("added_notice", name=new_name.strip())
                st.rerun()

    st.subheader(t("current_glasses"))
    products = [item for item in load_products() if item.get("store_id") == store_id]
    if not products:
        st.info(t("no_glasses_admin"))
        return
    for product in products:
        stock = int(product.get("stock") or 0)
        title = t("product_admin_title", name=product["name"], price=money(product["price"]), stock=stock)
        with st.expander(title, expanded=st.session_state.get("confirm_delete") == product["id"]):
            preview, fields = st.columns([1, 2])
            with preview:
                image_path = product_image_path(product)
                if image_path.is_file():
                    st.image(str(image_path), width="stretch")
                else:
                    st.warning(t("image_missing"))
                st.caption(join(term(shape) for shape in (product.get("face_shapes") or [])))
            with fields:
                with st.form(f"edit-{product['id']}"):
                    edited_name = st.text_input(t("full_name"), product["name"])
                    edited_price = st.number_input(
                        t("price_egp"),
                        min_value=1,
                        max_value=20000,
                        value=int(product["price"]),
                        step=1,
                    )
                    options = list(CATEGORIES)
                    if product["category"] not in options:
                        options.append(product["category"])
                    edited_category = st.selectbox(
                        t("frame_shape"),
                        options,
                        index=options.index(product["category"]),
                        format_func=term,
                    )
                    kind_options = list(KINDS)
                    if product.get("kind") not in kind_options:
                        kind_options.append(product.get("kind") or "طبية")
                    audience_options = list(AUDIENCES)
                    if product.get("audience") not in audience_options:
                        audience_options.append(product.get("audience") or "للجميع")
                    edited_kind = st.selectbox(
                        t("use"),
                        kind_options,
                        index=kind_options.index(product.get("kind") or "طبية"),
                        format_func=term,
                    )
                    edited_audience = st.selectbox(
                        t("audience"),
                        audience_options,
                        index=audience_options.index(product.get("audience") or "للجميع"),
                        format_func=term,
                    )
                    edited_shapes = st.multiselect(
                        t("face_match"),
                        FACE_SHAPES,
                        default=[shape for shape in product.get("face_shapes") or [] if shape in FACE_SHAPES],
                        format_func=term,
                    )
                    edited_stock = st.number_input(
                        t("stock"),
                        min_value=0,
                        max_value=999,
                        value=stock,
                        step=1,
                    )
                    replacement = st.file_uploader(t("replace_png"), type=["png"])
                    saved = st.form_submit_button(t("save_edit"), width="stretch")
            if saved:
                shapes = [shape for shape in edited_shapes if shape in FACE_SHAPES]
                if not edited_name.strip():
                    st.error(t("name_required"))
                elif not shapes:
                    st.error(t("shape_required"))
                else:
                    updated = dict(product)
                    updated["name"] = edited_name.strip()
                    updated["price"] = int(edited_price)
                    updated["category"] = edited_category
                    updated["kind"] = edited_kind
                    updated["audience"] = edited_audience
                    updated["face_shapes"] = shapes
                    updated["stock"] = int(edited_stock)
                    if str(product["id"]).startswith("custom-"):
                        updated["description"] = f"إطار {edited_category} يناسب شكل الوجه: {'، '.join(shapes)}."
                    if replacement is not None:
                        error = _store_png(replacement, product_image_dest(product))
                        if error:
                            st.error(t(error))
                            updated = None
                    if updated is not None:
                        updated["store_id"] = store_id
                        replace_product(updated, store_id=store_id)
                        st.session_state.notice = t("saved_notice", name=updated["name"])
                        st.rerun()
            if st.session_state.get("confirm_delete") == product["id"]:
                yes_col, no_col = st.columns(2)
                with yes_col:
                    if st.button(t("confirm_delete"), key=f"yes-del-{product['id']}", width="stretch"):
                        delete_product(product["id"], store_id=store_id)
                        st.session_state.confirm_delete = None
                        st.session_state.notice = t("deleted_notice", name=product["name"])
                        st.rerun()
                with no_col:
                    if st.button(t("cancel"), key=f"no-del-{product['id']}", width="stretch"):
                        st.session_state.confirm_delete = None
                        st.rerun()
            elif st.button(t("delete_glasses"), key=f"del-product-{product['id']}", width="stretch"):
                st.session_state.confirm_delete = product["id"]
                st.rerun()


def _render_order_admin() -> None:
    orders = _load_orders()
    st.write(f"**{t('orders_count', n=len(orders))}**")
    if not orders:
        st.info(t("no_orders"))
        return

    for order in orders:
        title = f"{order['id']} — {term(order['status'])} — {order['name']}"
        with st.expander(title, expanded=order["status"] == ORDER_STATUSES[0]):
            st.markdown(_status_steps(order["status"]), unsafe_allow_html=True)
            chosen = st.selectbox(
                t("update_status"),
                ORDER_STATUSES,
                index=ORDER_STATUSES.index(order["status"]) if order["status"] in ORDER_STATUSES else 0,
                format_func=term,
                key=f"status-{order['id']}",
            )
            if st.button(t("save_status"), key=f"save-status-{order['id']}"):
                set_order_status(order["id"], chosen)
                st.rerun()
            info_col, contact_col = st.columns(2)
            with info_col:
                st.markdown(f"**{t('ship_contact')}**")
                st.write(t("field_name", value=order["name"]))
                st.write(t("field_phone", value=order["phone"]))
                st.write(t("field_gov", value=gov_name(order["governorate"])))
                st.write(t("field_address", value=order["address"]))
                st.write(t("field_recorded", value=order["created"]))
                st.write(t("field_pay", value=term(order["payment"])))
                if order.get("payment_ref"):
                    st.write(t("field_ref", value=order["payment_ref"]))
                st.write(
                    t(
                        "money_line",
                        sub=money(order["subtotal"]),
                        fee=money(order["fee"]),
                        total=money(order["total"]),
                    )
                )
            with contact_col:
                st.markdown(f"**{t('rx_heading')}**")
                for index, line in enumerate(order.get("lines") or [], start=1):
                    st.write(
                        t(
                            "admin_line",
                            i=index,
                            name=line["name"],
                            qty=line["qty"],
                            lens=term(line["lens_label"]),
                            price=money(line["price"]),
                        )
                    )
                    st.text(prescription_detail(line))
                    rx_bytes = _rx_bytes(line.get("rx_file"))
                    if rx_bytes and str(line.get("rx_file", "")).lower().endswith((".jpg", ".jpeg", ".png")):
                        st.image(rx_bytes, caption=line.get("rx_name") or t("rx_caption_img"), width=220)
                    elif rx_bytes:
                        st.download_button(
                            t("download_rx", name=line.get("rx_name") or t("file_fallback")),
                            data=rx_bytes,
                            file_name=line.get("rx_name") or line["rx_file"],
                            key=f"rx-{order['id']}-{index}",
                        )


def render_admin() -> None:
    st.markdown(hero(t("admin_title"), t("admin_body"), "#666"), unsafe_allow_html=True)
    if not st.session_state.admin_ok:
        code = st.text_input(t("admin_code"), type="password", key="admin_code")
        if st.button(t("enter"), width="stretch"):
            if admin_code_matches(code):
                st.session_state.admin_ok = True
                st.rerun()
            st.error(t("bad_code"))
        return

    st.session_state.pop("admin_code", None)
    head_left, head_right = st.columns([3, 1])
    with head_left:
        section = st.radio(
            t("section"),
            ["الطلبات", "إدارة المنتجات", "المتاجر", "إعدادات المنصة"],
            format_func=term,
            horizontal=True,
            key="admin_section",
        )
    with head_right:
        if st.button(t("logout"), width="stretch"):
            st.session_state.admin_ok = False
            st.rerun()
    _render_backup()
    _render_notifications()
    if section == "إعدادات المنصة":
        _render_platform_settings()
    elif section == "إدارة المنتجات":
        _render_product_admin(PRIMARY_STORE)
    elif section == "المتاجر":
        _render_platform_vendors()
    else:
        _render_order_admin()


_BRAND_LIMIT = 5 * 1024 * 1024


def _brand_upload(upload) -> tuple[bytes | None, str, str | None]:
    if upload is None:
        return None, "", None
    raw = upload.getvalue()
    if not raw:
        return None, "", "png_empty"
    if len(raw) > _BRAND_LIMIT:
        return None, "", "image_too_big"
    suffix = Path(getattr(upload, "name", "") or "").suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png"}:
        return None, "", "image_type"
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except Exception:
        return None, "", "logo_bad"
    if image.format not in {"JPEG", "PNG"}:
        return None, "", "image_type"
    return raw, suffix, None


def _optional_fee(raw: str) -> tuple[int | None, str | None]:
    text = str(raw or "").strip()
    if not text:
        return None, None
    if not text.isdigit():
        return None, "ship_bad"
    return int(text), None


def _upload_bytes(upload) -> tuple[bytes | None, str, str | None]:
    if upload is None:
        return None, "", None
    raw = upload.getvalue()
    if not raw:
        return None, "", "png_empty"
    if len(raw) > 8_000_000:
        return None, "", "png_large"
    suffix = Path(upload.name).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".pdf"}:
        suffix = ".png"
    if suffix != ".pdf":
        try:
            image = Image.open(io.BytesIO(raw))
            image.load()
        except Exception:
            return None, "", "logo_bad"
    return raw, suffix, None


def _render_backup() -> None:
    st.subheader(t("backup_title"))
    vendors = load_vendors()
    orders = _load_orders()
    csv_col, excel_col = st.columns(2)
    with csv_col:
        st.download_button(
            t("backup_csv"),
            data=backup_zip(vendors, orders),
            file_name="moslem-optics-backup.zip",
            mime="application/zip",
            key="backup-csv",
            width="stretch",
        )
    workbook = backup_xlsx(vendors, orders)
    with excel_col:
        if workbook:
            st.download_button(
                t("backup_xlsx"),
                data=workbook,
                file_name="moslem-optics-backup.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="backup-xlsx",
                width="stretch",
            )
    try:
        report = admin_report_pdf(vendors, orders)
    except Exception:
        st.error(t("pdf_failed"))
        report = None
    _pdf_download(t("download_admin_pdf"), report, "moslem-optics-report.pdf", "admin-pdf")


def _render_platform_settings() -> None:
    if st.session_state.pop("admin_code_saved", False):
        st.success(t("admin_code_changed"))
    st.subheader(t("admin_change_code"))
    with st.form("admin-change-code"):
        current = st.text_input(t("current_code"), type="password")
        new_code = st.text_input(t("new_code"), type="password")
        submitted = st.form_submit_button(t("save_code"), width="stretch")
    if submitted:
        result = change_admin_code(current, new_code)
        if result == "ok":
            st.session_state.admin_code_saved = True
            st.rerun()
        elif result == "bad_new":
            st.error(t("code_too_short"))
        else:
            st.error(t("bad_current_code"))
    st.subheader(t("support_whatsapp"))
    with st.form("admin-support-wa"):
        number = st.text_input(t("whatsapp"), value=support_whatsapp())
        save_support = st.form_submit_button(t("save_support"), width="stretch")
    if save_support:
        raw = number.strip()
        if raw and not _support_number_ok(raw):
            st.error(t("support_bad"))
        else:
            save_support_whatsapp(raw)
            st.success(t("support_saved"))
            st.rerun()


def _render_platform_vendors() -> None:
    st.subheader(t("vendors_title"))
    options = ["open", "closed", "maintenance"]
    for vendor in load_vendors():
        phone = vendor.get("whatsapp") or "—"
        st.write(
            t(
                "vendor_row",
                name=_vendor_name(vendor.get("id")),
                status=t("status_active") if vendor.get("status") == "active" else vendor.get("status"),
                plan=_plan_label(str(vendor.get("plan") or "")),
                gov=gov_name(str(vendor.get("governorate") or "")),
                phone=phone,
            )
        )
        current = shop_status(vendor)
        with st.form(f"admin-shop-{vendor['id']}"):
            picked = st.radio(
                t("shop_status"),
                options,
                index=options.index(current),
                format_func=lambda key: t(f"shop_{key}"),
                horizontal=True,
                key=f"admin-shop-choice-{vendor['id']}",
            )
            if st.form_submit_button(t("save_shop_status"), width="stretch"):
                set_shop_status(str(vendor["id"]), picked)
                st.success(t("shop_status_saved"))
                st.rerun()


def render_join() -> None:
    st.markdown(hero(t("join_title"), t("join_body"), "#666"), unsafe_allow_html=True)
    once = st.session_state.get("vendor_code_once") or ""
    if once:
        vendor = get_vendor(st.session_state.get("vendor_id") or "")
        name = vendor["name"] if vendor else ""
        st.success(t("join_ok", name=name))
        st.code(once)
        if st.button(t("code_saved"), width="stretch"):
            st.session_state.vendor_code_once = ""
            go("vendor")
        return

    plan = st.radio(
        t("plan_pick"),
        ["monthly", "yearly"],
        format_func=lambda key: _plan_label(key),
        horizontal=True,
    )
    name = st.text_input(t("store_name"))
    logo = st.file_uploader(t("store_logo"), type=["png", "jpg", "jpeg", "webp"])
    phone = st.text_input(t("whatsapp"))
    address = st.text_area(t("address"))
    governorate = st.selectbox(t("gov"), list(GOVERNORATES), format_func=gov_name)
    method = st.radio(
        t("sub_pay"),
        ["instapay", "card", "apple", "cash"],
        format_func=_sub_method,
        horizontal=True,
    )
    price = money(PLANS[plan])
    receipt = None
    card_name = ""
    card_last4 = ""
    if method == "instapay":
        st.info(t("sub_insta_info", price=price, handle=DEMO_INSTAPAY))
        receipt = st.file_uploader(t("receipt"), type=["jpg", "jpeg", "png", "pdf"], key="sub-receipt")
    elif method == "card":
        st.info(t("sub_card_info"))
        card_name = st.text_input(t("card_name"), key="sub-card-name", max_chars=80)
        card_last4 = st.text_input(t("card_last4"), key="sub-card-last4", max_chars=4)
    elif method == "apple":
        st.info(t("sub_apple_info"))
    else:
        st.info(t("sub_cash_info"))
    if st.button(t("activate"), width="stretch"):
        blocked = False
        if not name.strip() or not phone.strip() or not address.strip():
            st.error(t("need_store"))
            blocked = True
        elif len(_phone_digits(phone)) < 10:
            st.error(t("bad_phone"))
            blocked = True
        logo_raw, logo_suffix, logo_error = _upload_bytes(logo)
        if logo_error:
            st.error(t(logo_error))
            blocked = True
        elif not logo_raw:
            st.error(t("need_logo"))
            blocked = True
        receipt_raw = None
        receipt_suffix = ""
        if method == "instapay":
            if receipt is None:
                st.error(t("need_receipt"))
                blocked = True
            else:
                receipt_raw, receipt_suffix, receipt_error = _upload_bytes(receipt)
                if receipt_error:
                    st.error(t(receipt_error))
                    blocked = True
                elif not receipt_raw:
                    st.error(t("need_receipt"))
                    blocked = True
        if method == "card":
            last4 = card_last4.strip()
            if not card_name.strip() or not last4.isdigit() or len(last4) != 4:
                st.error(t("need_card"))
                blocked = True
        if blocked:
            return
        try:
            record, plain = register_vendor(
                name,
                phone,
                address,
                governorate,
                plan,
                method,
                logo_bytes=logo_raw,
                logo_suffix=logo_suffix,
                receipt_bytes=receipt_raw,
                receipt_suffix=receipt_suffix,
                card_name=card_name,
                card_last4=card_last4.strip(),
            )
        except ValueError:
            if method == "instapay":
                st.error(t("need_receipt"))
            elif method == "card":
                st.error(t("need_card"))
            else:
                st.error(t("need_store"))
            return
        st.session_state.vendor_id = record["id"]
        st.session_state.vendor_code_once = plain
        try:
            record_event(
                "subscription",
                store=record["name"],
                total=int((record.get("subscription") or {}).get("amount") or 0),
                phone=record.get("whatsapp") or "",
                vendor_id=record["id"],
                store_id=record["id"],
            )
        except Exception:
            pass
        st.rerun()


def _render_vendor_shipping(vendor: dict) -> None:
    st.subheader(t("ship_fees_title"))
    st.caption(t("ship_fees_help"))
    shipping = vendor.get("shipping") if isinstance(vendor.get("shipping"), dict) else {}
    overrides = shipping.get("overrides") if isinstance(shipping.get("overrides"), dict) else {}
    current_default = shipping.get("default")
    try:
        default_shown = "" if current_default in (None, "") else str(int(current_default))
    except (TypeError, ValueError):
        default_shown = ""
    with st.form(f"vendor-shipping-{vendor['id']}"):
        default_raw = st.text_input(t("ship_default"), default_shown, placeholder=t("ship_default_ph"))
        edited: dict[str, str] = {}
        cols = st.columns(2)
        for index, gov in enumerate(GOVERNORATES):
            platform_fee, _eta = GOVERNORATES[gov]
            label = f"{gov_name(gov)} · {t('ship_platform', fee=money(platform_fee))}"
            raw_fee = overrides.get(gov, "")
            try:
                shown = "" if raw_fee in (None, "") else str(int(raw_fee))
            except (TypeError, ValueError):
                shown = ""
            with cols[index % 2]:
                edited[gov] = st.text_input(label, shown)
        submitted = st.form_submit_button(t("save_ship"), width="stretch")
    if not submitted:
        return
    default_fee, default_error = _optional_fee(default_raw)
    if default_error:
        st.error(t(default_error))
        return
    clean: dict[str, int] = {}
    for gov, raw in edited.items():
        amount, error = _optional_fee(raw)
        if error:
            st.error(t(error))
            return
        if amount is not None:
            clean[gov] = amount
    if update_vendor_shipping(str(vendor["id"]), default_fee, clean) is None:
        st.error(t("ship_bad"))
        return
    st.success(t("ship_saved"))
    st.rerun()


def _vendor_orders(store_id: str) -> list[dict]:
    owned = []
    for order in _load_orders():
        lines = []
        for line in order.get("lines") or []:
            line_store = line.get("store_id") or PRIMARY_STORE
            if line_store == store_id:
                lines.append(line)
        if lines:
            owned.append({**order, "lines": lines})
    return owned


def _render_vendor_login() -> None:
    revealed = st.session_state.pop("vendor_reset_once", "")
    st.markdown(hero(t("vendor_title"), t("vendor_body"), "#666"), unsafe_allow_html=True)
    if revealed:
        st.success(t("reset_ok"))
        st.code(revealed)
    code = st.text_input(t("vendor_code"), type="password")
    if st.button(t("vendor_enter"), width="stretch"):
        found = vendor_by_code(code)
        if found is None:
            st.error(t("bad_vendor_code"))
        else:
            st.session_state.vendor_id = found["id"]
            st.rerun()
    st.divider()
    st.subheader(t("reset_code_title"))
    st.caption(t("reset_code_help"))
    reset_name = st.text_input(t("store_name"), key="vendor-reset-name")
    reset_phone = st.text_input(t("whatsapp"), key="vendor-reset-phone")
    if st.button(t("reset_code_btn"), width="stretch"):
        status, plain = reset_vendor_by_whatsapp(reset_name, reset_phone)
        if status == "ok" and plain:
            st.session_state.vendor_reset_once = plain
            st.rerun()
        elif status == "no_whatsapp":
            st.warning(t("reset_no_whatsapp"))
        elif status == "primary":
            st.info(t("reset_primary"))
        else:
            st.error(t("reset_mismatch"))


def _render_vendor_controls(vendor: dict) -> None:
    revealed = st.session_state.pop("vendor_new_code_once", "")
    if revealed:
        st.success(t("code_changed"))
        st.code(revealed)
    options = ["open", "closed", "maintenance"]
    current = shop_status(vendor)
    with st.form(f"vendor-shop-{vendor['id']}"):
        picked = st.radio(
            t("shop_status"),
            options,
            index=options.index(current),
            format_func=lambda key: t(f"shop_{key}"),
            horizontal=True,
        )
        if st.form_submit_button(t("save_shop_status"), width="stretch"):
            set_shop_status(str(vendor["id"]), picked)
            st.success(t("shop_status_saved"))
            st.rerun()
    st.subheader(t("change_code"))
    with st.form("vendor-change-code"):
        current_code = st.text_input(t("current_code"), type="password")
        new_code = st.text_input(t("new_code"), type="password")
        submitted = st.form_submit_button(t("save_code"), width="stretch")
    if not submitted:
        return
    result = change_vendor_code(str(vendor["id"]), current_code, new_code)
    if result == "ok":
        st.session_state.vendor_new_code_once = new_code.strip()
        st.rerun()
    elif result == "bad_new":
        st.error(t("code_too_short"))
    elif result == "primary":
        st.info(t("reset_primary"))
    else:
        st.error(t("bad_current_code"))


def render_vendor() -> None:
    vendor_id = st.session_state.get("vendor_id") or ""
    vendor = get_vendor(vendor_id) if vendor_id else None
    if vendor is None or vendor.get("primary"):
        st.session_state.vendor_id = ""
        _render_vendor_login()
        return

    st.markdown(hero(vendor["name"], t("vendor_body"), "#666"), unsafe_allow_html=True)
    _render_vendor_controls(vendor)
    sub = vendor.get("subscription") or {}
    st.caption(
        t(
            "sub_status",
            plan=_plan_label(str(sub.get("plan") or vendor.get("plan") or "")),
            price=money(sub.get("amount") or PLANS.get(vendor.get("plan")) or 0),
            method=_sub_method(str(sub.get("method") or "")),
        )
    )
    cover = cover_path(vendor)
    if cover is not None:
        st.image(str(cover), width="stretch")
    mark = logo_path(vendor)
    if mark is not None:
        st.image(str(mark), width=160)
    orders = _vendor_orders(vendor["id"])
    sales = _line_sales(orders)
    days_left = subscription_days_left(vendor)
    stat_orders, stat_sales, stat_days = st.columns(3)
    stat_orders.metric(t("metric_orders"), len(orders))
    stat_sales.metric(t("metric_sales"), money(sales))
    stat_days.metric(t("metric_days"), days_left)
    try:
        vendor_pdf = vendor_report_pdf(vendor, orders, sales, days_left)
    except Exception:
        st.error(t("pdf_failed"))
        vendor_pdf = None
    _pdf_download(t("download_vendor_pdf"), vendor_pdf, f"{vendor['id']}-orders.pdf", "vendor-pdf")
    _render_notifications(vendor["id"])
    section = st.radio(
        t("section"),
        ["منتجاتي", "بيانات المتجر", "رسوم التوصيل", "طلبات متجري"],
        format_func=term,
        horizontal=True,
        key="vendor_section",
    )
    if st.button(t("vendor_out"), width="stretch"):
        st.session_state.vendor_id = ""
        st.rerun()
    if section == "بيانات المتجر":
        with st.form("vendor-profile"):
            edited_name = st.text_input(t("store_name"), vendor["name"])
            edited_phone = st.text_input(t("whatsapp"), vendor.get("whatsapp") or "")
            edited_address = st.text_area(t("address"), vendor.get("address") or "")
            govs = list(GOVERNORATES)
            current = vendor.get("governorate") or govs[0]
            if current not in govs:
                govs.append(current)
            edited_gov = st.selectbox(t("gov"), govs, index=govs.index(current), format_func=gov_name)
            new_logo = st.file_uploader(
                t("store_logo"),
                type=["jpg", "jpeg", "png"],
                help=t("logo_replace_help"),
            )
            new_cover = st.file_uploader(
                t("store_cover"),
                type=["jpg", "jpeg", "png"],
                help=t("cover_help"),
            )
            saved = st.form_submit_button(t("save_profile"), width="stretch")
        if saved:
            if not edited_name.strip() or not edited_phone.strip() or not edited_address.strip():
                st.error(t("need_store"))
            elif len(_phone_digits(edited_phone)) < 10:
                st.error(t("bad_phone"))
            else:
                logo_raw, logo_suffix, logo_error = _brand_upload(new_logo)
                cover_raw, cover_suffix, cover_error = _brand_upload(new_cover)
                if logo_error:
                    st.error(t(logo_error))
                elif cover_error:
                    st.error(t(cover_error))
                else:
                    update_vendor_profile(
                        vendor["id"],
                        edited_name,
                        edited_phone,
                        edited_address,
                        edited_gov,
                        logo_bytes=logo_raw,
                        logo_suffix=logo_suffix,
                        cover_bytes=cover_raw,
                        cover_suffix=cover_suffix,
                    )
                    st.success(t("profile_saved"))
                    st.rerun()
    elif section == "رسوم التوصيل":
        _render_vendor_shipping(vendor)
    elif section == "طلبات متجري":
        orders = _vendor_orders(vendor["id"])
        if not orders:
            st.info(t("no_vendor_orders"))
        for order in orders:
            with st.expander(f"{order['id']} — {term(order['status'])}"):
                st.caption(t("track_meta", created=order["created"], gov=gov_name(order["governorate"]), eta=eta_label(order["eta"])))
                for line in order["lines"]:
                    st.write(t("line_item", name=line["name"], qty=line["qty"], lens=term(line.get("lens_label") or "")))
    else:
        _render_product_admin(vendor["id"])


def render_policy() -> None:
    st.markdown(hero(t("policy_title"), t("policy_intro")), unsafe_allow_html=True)
    st.info(t("policy_disclaimer"))
    st.subheader(t("terms_heading"))
    st.markdown(t("terms_body"))
    st.subheader(t("returns_heading"))
    st.markdown(t("returns_body"))
    if st.button(t("back_shop"), key="policy-back", width="stretch"):
        go("store")


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="nv-footer">
            <img class="nv-footer-logo" src="{_official_logo_src()}" alt="نظارات مسلم">
            <div>{t("footer_note")}</div>
            {_social_bar()}
        </div>
        """,
        unsafe_allow_html=True,
    )
    terms_col, returns_col = st.columns(2)
    with terms_col:
        if st.button(t("terms_heading"), key="footer-terms", width="stretch"):
            go("policy")
    with returns_col:
        if st.button(t("returns_heading"), key="footer-returns", width="stretch"):
            go("policy")


page = st.session_state.page
if page == "store":
    render_store()
elif page == "tryon":
    render_tryon()
elif page == "track":
    render_track()
elif page == "admin":
    render_admin()
elif page == "join":
    render_join()
elif page == "vendor":
    render_vendor()
elif page == "policy":
    render_policy()
else:
    render_cart()

render_footer()

