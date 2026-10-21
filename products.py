"""كتالوج النظارات المعروضة في المتجر."""

from __future__ import annotations

import json
from pathlib import Path

from paths import bundled_glasses_dir, data_dir, ensure_seed_catalog, user_glasses_dir

ensure_seed_catalog()
ASSETS_DIR = user_glasses_dir()
CATALOG_PATH = data_dir() / "catalog.json"

CATALOG_VERSION = 3
CATEGORIES = ["كلاسيك", "دائري", "أفياتور", "كات آي", "رياضي", "مربع", "بيضاوي", "شفاف"]
KINDS = ["طبية", "شمسية"]
AUDIENCES = ["رجالي", "حريمي", "أطفال", "للجميع"]
FACE_SHAPES = ["دائري", "مربع", "بيضاوي", "مستطيل", "قلب"]
CATEGORY_SHAPES = {
    "كلاسيك": ["دائري", "بيضاوي"],
    "مربع": ["دائري"],
    "كات آي": ["دائري", "بيضاوي"],
    "دائري": ["مربع", "مستطيل", "قلب"],
    "بيضاوي": ["مربع", "مستطيل", "قلب"],
    "أفياتور": ["مربع", "بيضاوي", "مستطيل", "قلب"],
    "شفاف": ["بيضاوي"],
    "رياضي": ["بيضاوي", "مستطيل"],
}

PRODUCTS = [
    {
        "id": "classic-black",
        "name": "مسلم كلاسيك أسود",
        "brand": "نظارات مسلم",
        "price": 890,
        "old_price": 1100,
        "category": "كلاسيك",
        "kind": "طبية",
        "audience": "رجالي",
        "rating": 4.8,
        "sold": 320,
        "stock": 8,
        "color": "أسود",
        "description": "إطار طبي رجالي من تشكيلة المحل في باب اللوق. مستطيل خفيف يناسب الوجه الدائري والبيضاوي.",
        "asset": "classic_black.png",
        "face_shapes": ["دائري", "بيضاوي"],
    },
    {
        "id": "round-gold",
        "name": "مسلم دائري ذهبي",
        "brand": "نظارات مسلم",
        "price": 980,
        "old_price": 1200,
        "category": "دائري",
        "kind": "طبية",
        "audience": "حريمي",
        "rating": 4.7,
        "sold": 210,
        "stock": 8,
        "color": "ذهبي",
        "description": "إطار طبي حريمي دائري من المحل. المعدن الذهبي الرفيع يليّن الوجه المربع والمستطيل.",
        "face_shapes": ["مربع", "مستطيل", "قلب"],
        "asset": "round_gold.png",
    },
    {
        "id": "aviator-silver",
        "name": "أوكلي أفياتور",
        "brand": "Oakley",
        "price": 3450,
        "old_price": 3900,
        "category": "أفياتور",
        "kind": "شمسية",
        "audience": "رجالي",
        "rating": 4.9,
        "sold": 450,
        "stock": 6,
        "color": "فضي",
        "description": "نظارة شمسية أفياتور من ركن أوكلي الظاهر في المحل. عدسة داكنة وإطار معدني.",
        "face_shapes": ["مربع", "بيضاوي", "مستطيل", "قلب"],
        "asset": "aviator_silver.png",
    },
    {
        "id": "cateye-rose",
        "name": "مسلم كات آي",
        "brand": "نظارات مسلم",
        "price": 1150,
        "old_price": 1400,
        "category": "كات آي",
        "kind": "طبية",
        "audience": "حريمي",
        "rating": 4.6,
        "sold": 180,
        "stock": 8,
        "color": "وردي",
        "description": "إطار طبي حريمي كات آي من تشكيلة باب اللوق. يرفع زاوية العين على الوجه الدائري والبيضاوي.",
        "face_shapes": ["دائري", "بيضاوي"],
        "asset": "cateye_rose.png",
    },
    {
        "id": "sport-navy",
        "name": "أوكلي سبورت",
        "brand": "Oakley",
        "price": 2980,
        "old_price": 3400,
        "category": "رياضي",
        "kind": "شمسية",
        "audience": "رجالي",
        "rating": 4.5,
        "sold": 265,
        "stock": 7,
        "color": "كحلي",
        "description": "نظارة شمسية رياضية من أوكلي بعدسة داكنة وإطار ملتف، كما في ركن الماركات بالمحل.",
        "face_shapes": ["بيضاوي", "مستطيل"],
        "asset": "sport_navy.png",
    },
    {
        "id": "square-tortoise",
        "name": "بوليس تاورتوز",
        "brand": "Police",
        "price": 1890,
        "old_price": 2250,
        "category": "مربع",
        "kind": "طبية",
        "audience": "رجالي",
        "rating": 4.8,
        "sold": 140,
        "stock": 6,
        "color": "تاورتوز",
        "description": "إطار طبي رجالي من بوليس بنقشة تاورتوز. يضيف تحديداً للوجه الدائري.",
        "face_shapes": ["دائري"],
        "asset": "square_tortoise.png",
    },
    {
        "id": "oval-green",
        "name": "مسلم بيضاوي",
        "brand": "نظارات مسلم",
        "price": 820,
        "old_price": 990,
        "category": "بيضاوي",
        "kind": "طبية",
        "audience": "حريمي",
        "rating": 4.4,
        "sold": 96,
        "stock": 8,
        "color": "زيتوني",
        "description": "إطار طبي حريمي بيضاوي من المحل. يوازن الوجه المربع والمستطيل والقلب.",
        "face_shapes": ["مربع", "مستطيل", "قلب"],
        "asset": "oval_green.png",
    },
    {
        "id": "clear-blue",
        "name": "مسلم شفاف",
        "brand": "نظارات مسلم",
        "price": 720,
        "old_price": 890,
        "category": "شفاف",
        "kind": "طبية",
        "audience": "للجميع",
        "rating": 4.3,
        "sold": 390,
        "stock": 12,
        "color": "شفاف",
        "description": "إطار طبي شفاف خفيف من تشكيلة المحل، مناسب للاستخدام اليومي على الوجه البيضاوي.",
        "asset": "clear_blue.png",
        "face_shapes": ["بيضاوي"],
    },
    {
        "id": "browline-brown",
        "name": "مسلم برولاين بني",
        "brand": "نظارات مسلم",
        "price": 1490,
        "old_price": 1750,
        "category": "كلاسيك",
        "kind": "طبية",
        "audience": "رجالي",
        "rating": 4.7,
        "sold": 88,
        "stock": 5,
        "color": "بني",
        "description": "إطار طبي رجالي بحاجب علوي بني من المحل. يحدد الوجه الدائري والبيضاوي.",
        "asset": "browline_brown.png",
        "face_shapes": ["دائري", "بيضاوي"],
    },
    {
        "id": "wayfarer-black",
        "name": "بوليس وايفارير",
        "brand": "Police",
        "price": 2650,
        "old_price": 3100,
        "category": "مربع",
        "kind": "شمسية",
        "audience": "رجالي",
        "rating": 4.6,
        "sold": 240,
        "stock": 8,
        "color": "أسود",
        "description": "نظارة شمسية وايفارير من ركن بوليس في المحل. عدسة داكنة وإطار عريض للوجه الدائري.",
        "asset": "wayfarer_black.png",
        "face_shapes": ["دائري"],
    },
    {
        "id": "kids-round-blue",
        "name": "مسلم أطفال دائري",
        "brand": "نظارات مسلم",
        "price": 480,
        "old_price": 590,
        "category": "دائري",
        "kind": "طبية",
        "audience": "أطفال",
        "rating": 4.8,
        "sold": 150,
        "stock": 14,
        "color": "أزرق",
        "description": "إطار طبي دائري للأطفال من المحل، مرن وخفيف ويناسب الوجه المربع والمستطيل.",
        "asset": "kids_round_blue.png",
        "face_shapes": ["مربع", "مستطيل", "قلب"],
    },
    {
        "id": "kids-flex-pink",
        "name": "مسلم أطفال مرن",
        "brand": "نظارات مسلم",
        "price": 450,
        "old_price": 560,
        "category": "بيضاوي",
        "kind": "طبية",
        "audience": "أطفال",
        "rating": 4.7,
        "sold": 130,
        "stock": 14,
        "color": "وردي",
        "description": "إطار طبي وردي مرن للأطفال من تشكيلة باب اللوق، خفيف للاستخدام المدرسي.",
        "asset": "kids_flex_pink.png",
        "face_shapes": ["مربع", "مستطيل", "قلب"],
    },
    {
        "id": "cateye-sun",
        "name": "بوليس كات آي",
        "brand": "Police",
        "price": 2480,
        "old_price": 2890,
        "category": "كات آي",
        "kind": "شمسية",
        "audience": "حريمي",
        "rating": 4.8,
        "sold": 175,
        "stock": 7,
        "color": "تاورتوز",
        "description": "نظارة شمسية حريمية كات آي من بوليس بعدسة بنية. ترفع الملامح على الوجه الدائري والبيضاوي.",
        "asset": "cateye_sun.png",
        "face_shapes": ["دائري", "بيضاوي"],
    },
    {
        "id": "round-sun-gold",
        "name": "مسلم دائري شمسي",
        "brand": "نظارات مسلم",
        "price": 980,
        "old_price": 1200,
        "category": "دائري",
        "kind": "شمسية",
        "audience": "حريمي",
        "rating": 4.5,
        "sold": 200,
        "stock": 9,
        "color": "ذهبي",
        "description": "نظارة شمسية دائرية من المحل بعدسة داكنة وإطار ذهبي. تنعّم الوجه المربع والمستطيل.",
        "asset": "round_sun_gold.png",
        "face_shapes": ["مربع", "مستطيل", "قلب"],
    },
    {
        "id": "kids-sun-red",
        "name": "مسلم أطفال شمسية",
        "brand": "نظارات مسلم",
        "price": 420,
        "old_price": 520,
        "category": "دائري",
        "kind": "شمسية",
        "audience": "أطفال",
        "rating": 4.6,
        "sold": 210,
        "stock": 16,
        "color": "أحمر",
        "description": "نظارة شمسية صغيرة للأطفال من المحل، بعدسة داكنة وإطار خفيف.",
        "asset": "kids_sun_red.png",
        "face_shapes": ["مربع", "مستطيل", "قلب"],
    },
    {
        "id": "kids-sport-yellow",
        "name": "مسلم أطفال رياضية",
        "brand": "نظارات مسلم",
        "price": 450,
        "old_price": 550,
        "category": "رياضي",
        "kind": "شمسية",
        "audience": "أطفال",
        "rating": 4.5,
        "sold": 98,
        "stock": 12,
        "color": "أصفر",
        "description": "نظارة شمسية رياضية للأطفال من تشكيلة المحل، بإطار ملتف وعدسة داكنة.",
        "asset": "kids_sport_yellow.png",
        "face_shapes": ["بيضاوي", "مستطيل"],
    },
]


SEED_ASSETS = {item["asset"] for item in PRODUCTS}
PRIMARY_STORE = "moslem"


class StockError(ValueError):
    """الكمية المطلوبة أكبر من المخزون المتاح."""

    def __init__(self, message: str, code: str = "generic", **data) -> None:
        super().__init__(message)
        self.code = code
        self.data = data


def _asset_name(product: dict) -> str:
    return Path(str(product.get("asset") or "")).name


def product_image_path(product: dict) -> Path:
    name = _asset_name(product)
    user = user_glasses_dir() / name
    if user.is_file():
        return user
    bundled = bundled_glasses_dir() / name
    if bundled.is_file():
        return bundled
    return user


def product_image_dest(product: dict) -> Path:
    return user_glasses_dir() / _asset_name(product)


def _normalize(item: dict) -> dict:
    record = dict(item)
    record["price"] = int(record.get("price") or 0)
    record["old_price"] = int(record.get("old_price") or record["price"])
    record["stock"] = max(0, int(record.get("stock", 8)))
    shapes = [shape for shape in (record.get("face_shapes") or []) if shape in FACE_SHAPES]
    if not shapes:
        shapes = list(CATEGORY_SHAPES.get(str(record.get("category") or ""), ["بيضاوي"]))
    record["face_shapes"] = shapes
    record.setdefault("kind", "طبية")
    record.setdefault("audience", "للجميع")
    record.setdefault("brand", "نظارات مسلم")
    record.setdefault("rating", 5.0)
    record.setdefault("sold", 0)
    record.setdefault("color", record.get("category") or "")
    record.setdefault("description", "")
    record.setdefault("asset", "")
    record["store_id"] = str(record.get("store_id") or PRIMARY_STORE)
    return record


def _read_catalog() -> tuple[int, list]:
    if not CATALOG_PATH.exists():
        return 0, []
    try:
        payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0, []
    if isinstance(payload, list):
        return 1, payload
    if isinstance(payload, dict):
        return int(payload.get("version") or 1), list(payload.get("products") or [])
    return 0, []


def _ordered(items: list[dict]) -> list[dict]:
    seed_index = {item["id"]: index for index, item in enumerate(PRODUCTS)}

    def sort_key(pair: tuple[int, dict]) -> tuple[int, int]:
        index, item = pair
        group = 0 if item.get("store_id") == PRIMARY_STORE else 1
        if item["id"] in seed_index:
            inner = seed_index[item["id"]]
        else:
            inner = 1000 + index
        return group, inner

    return [item for _, item in sorted(enumerate(items), key=sort_key)]


def load_products() -> list[dict]:
    version, saved = _read_catalog()
    raw = [item for item in saved if isinstance(item, dict) and item.get("id")]
    needs_store = any(not item.get("store_id") for item in raw)
    saved_items = [_normalize(item) for item in raw]
    if version >= CATALOG_VERSION and saved_items:
        if needs_store:
            save_products(saved_items)
        return _ordered(saved_items)
    stock_by_id = {item["id"]: item["stock"] for item in saved_items}
    seeded_ids = {item["id"] for item in PRODUCTS}
    seeded = [
        _normalize({**item, "stock": stock_by_id.get(item["id"], item.get("stock", 8))})
        for item in PRODUCTS
    ]
    custom = [item for item in saved_items if item["id"] not in seeded_ids]
    merged = seeded + custom
    save_products(merged)
    return _ordered(merged)


def save_products(items: list[dict]) -> None:
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": CATALOG_VERSION, "products": items}
    CATALOG_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def get_product(product_id: str) -> dict | None:
    for item in load_products():
        if item["id"] == product_id:
            return item
    return None


def replace_product(updated: dict, store_id: str | None = None) -> None:
    items = load_products()
    existing = next((item for item in items if item["id"] == updated["id"]), None)
    if store_id and existing and existing.get("store_id") != store_id:
        return
    payload = dict(updated)
    if store_id:
        payload["store_id"] = store_id
    found = False
    for index, item in enumerate(items):
        if item["id"] == payload["id"]:
            items[index] = _normalize(payload)
            found = True
            break
    if not found:
        items.append(_normalize(payload))
    save_products(items)


def delete_product(product_id: str, store_id: str | None = None) -> None:
    items = load_products()
    removed = next((item for item in items if item["id"] == product_id), None)
    if store_id and removed and removed.get("store_id") != store_id:
        return
    save_products([item for item in items if item["id"] != product_id])
    if removed is None:
        return
    asset = str(removed.get("asset") or "")
    if asset and asset not in SEED_ASSETS:
        path = user_glasses_dir() / Path(asset).name
        if path.is_file():
            path.unlink()


def reserve_stock(needed: dict[str, int]) -> None:
    if not needed:
        return
    items = load_products()
    by_id = {item["id"]: item for item in items}
    for product_id, qty in needed.items():
        product = by_id.get(product_id)
        if product is None:
            raise StockError("إحدى النظارات لم تعد موجودة في المتجر.", code="missing")
        available = int(product.get("stock") or 0)
        if qty > available:
            raise StockError(
                f"المخزون لا يكفي لـ {product['name']}. المتبقي {available}.",
                code="short",
                name=product["name"],
                available=available,
            )
    for product_id, qty in needed.items():
        by_id[product_id]["stock"] = int(by_id[product_id]["stock"]) - qty
    save_products(items)
