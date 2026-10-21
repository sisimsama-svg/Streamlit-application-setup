"""فواتير وتقارير PDF بخط عربي وثيم المتجر الأخضر."""

from __future__ import annotations

import io
import os

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from i18n import gov_name, lang, money, t, term
from paths import bundle_root
from vendors import get_vendor

FONT_NAME = "MoslemArabic"
PAGE_W, PAGE_H = A4
LEFT = 36
RIGHT = PAGE_W - 36
CONTENT_W = RIGHT - LEFT
GREEN = "#059669"
GREEN_DARK = "#047857"
BG = "#f4faf6"
INK = "#1f2933"
MUTED = "#5c656c"
WHITE = "#ffffff"
ROW = "#e7f6ef"

_READY = False


def _font_candidates() -> list[str]:
    bundled = bundle_root() / "assets" / "fonts" / "NotoNaskhArabic-Regular.ttf"
    return [
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        str(bundled),
        "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoNaskhArabic-Regular.ttf",
    ]


def _ensure_font() -> str:
    global _READY
    if _READY:
        return FONT_NAME
    for path in _font_candidates():
        if path and os.path.isfile(path):
            pdfmetrics.registerFont(TTFont(FONT_NAME, path))
            _READY = True
            return FONT_NAME
    raise RuntimeError("Arabic font missing")


def _shape(text) -> str:
    raw = str(text or "")
    if not raw:
        return ""
    if not any("\u0600" <= ch <= "\u06FF" for ch in raw):
        return raw
    try:
        return get_display(arabic_reshaper.reshape(raw))
    except Exception:
        return raw


def _width(text: str, size: int) -> float:
    return pdfmetrics.stringWidth(_shape(text), FONT_NAME, size)


def _clip(text, width: float, size: int = 9) -> str:
    raw = str(text or "")
    if _width(raw, size) <= width:
        return _shape(raw)
    trimmed = raw
    while trimmed and _width(trimmed + "…", size) > width:
        trimmed = trimmed[:-1]
    return _shape((trimmed + "…") if trimmed else raw[:1])


def _wrap(text, width: float, size: int) -> list[str]:
    raw = " ".join(str(text or "").split())
    if not raw:
        return [""]
    lines: list[str] = []
    current = ""
    for word in raw.split(" "):
        trial = word if not current else f"{current} {word}"
        if _width(trial, size) <= width:
            current = trial
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines or [raw]


def _store_label(store_id: str | None) -> str:
    vendor = get_vendor(str(store_id or "moslem"))
    if not vendor:
        return "نظارات مسلم"
    if lang() == "en" and vendor.get("name_en"):
        return str(vendor["name_en"])
    return str(vendor.get("name") or "نظارات مسلم")


def _method_label(method: str) -> str:
    labels = {
        "instapay": "pay_insta",
        "card": "pay_card",
        "visa": "pay_card",
        "apple": "pay_apple",
        "cash": "pay_cash",
        "vodafone": "pay_voda",
    }
    key = labels.get(str(method or ""))
    if key:
        return t(key)
    if not method:
        return t("method_none")
    return str(method)


def _plan_short(plan: str) -> str:
    if plan == "monthly":
        return t("plan_month_short")
    if plan == "yearly":
        return t("plan_year_short")
    if plan == "primary":
        return t("plan_primary")
    return plan or t("method_none")


class _Writer:
    def __init__(self, title: str):
        _ensure_font()
        self.title = title
        self.rtl = lang() != "en"
        self.buffer = io.BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=A4)
        self.canvas.setTitle("Moslem Optics")
        self.canvas.setAuthor("نظارات مسلم")
        self.page = 0
        self.y = 0.0
        self.new_page()

    def new_page(self) -> None:
        if self.page:
            self.canvas.showPage()
        self.page += 1
        pen = self.canvas
        pen.setFillColor(BG)
        pen.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        pen.setFillColor(GREEN)
        pen.rect(0, PAGE_H - 88, PAGE_W, 88, stroke=0, fill=1)
        pen.setFillColor(GREEN_DARK)
        pen.rect(0, PAGE_H - 92, PAGE_W, 4, stroke=0, fill=1)
        pen.setFillColor(WHITE)
        pen.setFont(FONT_NAME, 20)
        pen.drawRightString(RIGHT, PAGE_H - 34, _shape("نظارات مسلم"))
        pen.setFont(FONT_NAME, 10)
        pen.drawRightString(RIGHT, PAGE_H - 52, "Moslem Optics")
        pen.drawRightString(RIGHT, PAGE_H - 68, _shape("باب اللوق، القاهرة  ·  Bab El Louk, Cairo"))
        pen.setFillColor(INK)
        pen.setFont(FONT_NAME, 15)
        title = _shape(self.title)
        if self.rtl:
            pen.drawRightString(RIGHT, PAGE_H - 116, title)
        else:
            pen.drawString(LEFT, PAGE_H - 116, title)
        pen.setStrokeColor(GREEN)
        pen.setLineWidth(1.4)
        pen.line(LEFT, PAGE_H - 126, RIGHT, PAGE_H - 126)
        pen.setFillColor(GREEN)
        pen.rect(0, 0, PAGE_W, 24, stroke=0, fill=1)
        pen.setFillColor(WHITE)
        pen.setFont(FONT_NAME, 8)
        pen.drawCentredString(PAGE_W / 2, 9, _shape("نظارات مسلم  ·  Moslem Optics  ·  Bab El Louk"))
        self.y = PAGE_H - 146

    def ensure(self, need: float) -> None:
        if self.y - need < 40:
            self.new_page()

    def _draw(self, text, size: int, color: str, y: float) -> None:
        pen = self.canvas
        pen.setFillColor(color)
        pen.setFont(FONT_NAME, size)
        shown = _shape(text)
        if self.rtl:
            pen.drawRightString(RIGHT, y, shown)
        else:
            pen.drawString(LEFT, y, shown)

    def paragraph(self, text, size: int = 12, color: str = INK, gap: int = 5) -> None:
        for line in _wrap(text, CONTENT_W, size):
            self.ensure(size + gap)
            self._draw(line, size, color, self.y)
            self.y -= size + gap

    def kv(self, label, value) -> None:
        self.ensure(16)
        pen = self.canvas
        pen.setFont(FONT_NAME, 10)
        label_s = _shape(str(label))
        value_s = _clip(value, CONTENT_W - 140, 10)
        if self.rtl:
            pen.setFillColor(MUTED)
            pen.drawRightString(RIGHT, self.y, label_s)
            pen.setFillColor(INK)
            pen.drawRightString(RIGHT - 130, self.y, value_s)
        else:
            pen.setFillColor(MUTED)
            pen.drawString(LEFT, self.y, label_s)
            pen.setFillColor(INK)
            pen.drawString(LEFT + 130, self.y, value_s)
        self.y -= 16

    def gap(self, amount: float = 8) -> None:
        self.y -= amount

    def table(self, headers: list[str], rows: list[list], widths: list[float]) -> None:
        height = 20

        def paint(cells: list, header: bool = False, alt: bool = False) -> None:
            self.ensure(height + 2)
            top = self.y
            pen = self.canvas
            pen.setFillColor(GREEN if header else ROW if alt else WHITE)
            pen.roundRect(LEFT, top - height + 4, CONTENT_W, height, 3, stroke=0, fill=1)
            pen.setFillColor(WHITE if header else INK)
            pen.setFont(FONT_NAME, 9)
            if self.rtl:
                x = RIGHT - 6
                for text, width in zip(cells, widths):
                    pen.drawRightString(x, top - 11, _clip(text, width - 10, 9))
                    x -= width
            else:
                x = LEFT + 6
                for text, width in zip(cells, widths):
                    pen.drawString(x, top - 11, _clip(text, width - 10, 9))
                    x += width
            self.y -= height + 3

        paint(headers, header=True)
        for index, row in enumerate(rows):
            paint(row, alt=index % 2 == 0)
        if not rows:
            self.paragraph(t("no_results"), size=10, color=MUTED)

    def total_bar(self, label, value) -> None:
        self.ensure(36)
        pen = self.canvas
        pen.setFillColor(GREEN)
        pen.roundRect(LEFT, self.y - 20, CONTENT_W, 30, 6, stroke=0, fill=1)
        pen.setFillColor(WHITE)
        pen.setFont(FONT_NAME, 13)
        shown = _shape(f"{label}    {value}")
        if self.rtl:
            pen.drawRightString(RIGHT - 12, self.y - 10, shown)
        else:
            pen.drawString(LEFT + 12, self.y - 10, shown)
        self.y -= 40

    def finish(self) -> bytes:
        self.canvas.save()
        return self.buffer.getvalue()


def invoice_pdf(order: dict) -> bytes:
    writer = _Writer(t("pdf_invoice"))
    writer.kv(t("order_no"), order.get("id") or "")
    writer.kv(t("pdf_date"), order.get("created") or "")
    writer.kv(t("pdf_status"), term(str(order.get("status") or "")))
    writer.kv(t("pdf_customer"), order.get("name") or "")
    writer.kv(t("pdf_phone"), order.get("phone") or "")
    writer.kv(t("gov"), gov_name(str(order.get("governorate") or "")))
    writer.kv(t("pdf_address"), order.get("address") or "")
    writer.kv(t("pdf_payment"), term(str(order.get("payment") or "")))
    writer.gap(6)
    rows = []
    for line in order.get("lines") or []:
        qty = int(line.get("qty") or 0)
        price = int(line.get("price") or 0)
        rows.append(
            [
                line.get("name") or "",
                str(qty),
                term(str(line.get("lens_label") or "")),
                _store_label(line.get("store_id")),
                money(qty * price),
            ]
        )
    writer.table(
        [t("pdf_item"), t("pdf_qty"), t("pdf_lens"), t("pdf_store"), t("pdf_price")],
        rows,
        [190, 50, 90, 110, 83],
    )
    writer.gap(8)
    writer.kv(t("pdf_subtotal"), money(order.get("subtotal") or 0))
    writer.kv(t("pdf_delivery"), money(order.get("fee") or 0))
    writer.total_bar(t("pdf_total"), money(order.get("total") or 0))
    return writer.finish()


def vendor_report_pdf(vendor: dict, orders: list[dict], sales: int, days_left: int) -> bytes:
    writer = _Writer(t("pdf_vendor"))
    writer.kv(t("store_name"), _store_label(vendor.get("id")))
    writer.kv(t("gov"), gov_name(str(vendor.get("governorate") or "")))
    writer.kv(t("whatsapp"), vendor.get("whatsapp") or "—")
    writer.kv(t("metric_orders"), str(len(orders)))
    writer.kv(t("metric_sales"), money(sales))
    writer.kv(t("metric_days"), str(days_left))
    writer.gap(8)
    rows = []
    for order in orders:
        line_total = 0
        names = []
        for line in order.get("lines") or []:
            line_total += int(line.get("qty") or 0) * int(line.get("price") or 0)
            names.append(str(line.get("name") or ""))
        rows.append(
            [
                order.get("id") or "",
                order.get("created") or "",
                term(str(order.get("status") or "")),
                "، ".join(names),
                money(line_total),
            ]
        )
    writer.table(
        [t("order_no"), t("pdf_date"), t("pdf_status"), t("pdf_item"), t("pdf_total")],
        rows,
        [90, 100, 90, 153, 90],
    )
    writer.gap(8)
    writer.total_bar(t("metric_sales"), money(sales))
    return writer.finish()


def admin_report_pdf(vendors: list[dict], orders: list[dict]) -> bytes:
    writer = _Writer(t("pdf_admin"))
    sales = sum(int(order.get("total") or 0) for order in orders)
    writer.kv(t("pdf_stores"), str(len(vendors)))
    writer.kv(t("pdf_orders_n"), str(len(orders)))
    writer.kv(t("pdf_sales"), money(sales))
    writer.gap(6)
    writer.paragraph(t("vendors_title"), size=13)
    store_rows = []
    for vendor in vendors:
        sub = vendor.get("subscription") or {}
        store_rows.append(
            [
                _store_label(vendor.get("id")),
                gov_name(str(vendor.get("governorate") or "")),
                _plan_short(str(sub.get("plan") or vendor.get("plan") or "")),
                _method_label(str(sub.get("method") or "")),
                money(sub.get("amount") or 0),
            ]
        )
    writer.table(
        [t("store_name"), t("gov"), t("pdf_plan"), t("pdf_method"), t("pdf_amount")],
        store_rows,
        [150, 110, 80, 110, 73],
    )
    writer.gap(8)
    writer.paragraph(t("pdf_orders_n"), size=13)
    order_rows = []
    for order in orders[:80]:
        order_rows.append(
            [
                order.get("id") or "",
                order.get("created") or "",
                order.get("name") or "",
                term(str(order.get("status") or "")),
                money(order.get("total") or 0),
            ]
        )
    writer.table(
        [t("order_no"), t("pdf_date"), t("pdf_customer"), t("pdf_status"), t("pdf_total")],
        order_rows,
        [90, 100, 140, 110, 83],
    )
    writer.gap(8)
    writer.total_bar(t("pdf_sales"), money(sales))
    return writer.finish()
