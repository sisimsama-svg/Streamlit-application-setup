import { mountTryOn } from "./tryon.js";

const CART_KEY = "moslem-cart-v1";
const STEPS = ["تم التجهيز", "جاري التغليف", "خرج للتوصيل"];

let catalog = [];
let shop = {};
let governorates = [];
let lenses = [];
let payments = [];
let viewToken = 0;
let teardown = () => {};
let tryonApi = null;
let toastTimer = 0;

const view = document.getElementById("view");

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

function money(value) {
  return `${new Intl.NumberFormat("en-EG", { maximumFractionDigits: 0 }).format(Number(value) || 0)} ج.م`;
}

function off(product) {
  if (!product.old_price || product.old_price <= product.price) return 0;
  return Math.round((1 - product.price / product.old_price) * 100);
}

function byId(id) {
  return catalog.find((item) => item.id === id) || null;
}

function lensById(id) {
  return lenses.find((item) => item.id === id) || null;
}

function getCart() {
  try {
    const parsed = JSON.parse(localStorage.getItem(CART_KEY) || "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function setCart(items) {
  localStorage.setItem(CART_KEY, JSON.stringify(items));
}

function cartCount() {
  return getCart().reduce((sum, line) => sum + Number(line.qty || 0), 0);
}

function unitPrice(line) {
  const product = byId(line.productId);
  const lens = lensById(line.lens);
  if (!product) return 0;
  return product.price + (lens ? lens.price : 0);
}

function cartSubtotal() {
  return getCart().reduce((sum, line) => sum + unitPrice(line) * Number(line.qty || 0), 0);
}

function addToCart(product, lensId, qty) {
  if (!product || product.stock <= 0) {
    toast("هذا الإطار نفد من التشكيلة.");
    return false;
  }
  const cart = getCart();
  const id = `${product.id}::${lensId}`;
  const found = cart.find((line) => line.id === id);
  const next = (found ? found.qty : 0) + qty;
  if (next > product.stock || next > 5) {
    toast(`المتوفر ${Math.min(product.stock, 5)} قطع.`);
    return false;
  }
  if (found) found.qty = next;
  else cart.push({ id, productId: product.id, lens: lensId, qty });
  setCart(cart);
  refreshChrome(parseRoute());
  return true;
}

function changeQty(lineId, delta) {
  const cart = getCart();
  const line = cart.find((item) => item.id === lineId);
  if (!line) return;
  const product = byId(line.productId);
  const stock = product ? product.stock : 0;
  line.qty += delta;
  if (line.qty <= 0) setCart(cart.filter((item) => item.id !== lineId));
  else {
    line.qty = Math.min(line.qty, stock || line.qty, 5);
    setCart(cart);
  }
  refreshChrome(parseRoute());
}

function removeLine(lineId) {
  setCart(getCart().filter((item) => item.id !== lineId));
  refreshChrome(parseRoute());
}

function toast(html) {
  const node = document.getElementById("toast");
  node.innerHTML = html;
  node.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    node.hidden = true;
  }, 3400);
}

function parseRoute() {
  const raw = location.hash.replace(/^#/, "") || "/";
  let decoded = raw;
  try { decoded = decodeURIComponent(raw); } catch { decoded = raw; }
  const [path, queryText] = decoded.split("?");
  const parts = path.split("/").filter(Boolean);
  const query = new URLSearchParams(queryText || "");
  const name = parts[0] || "home";
  return { name, id: parts[1] || "", parts, query };
}

function shopHref(params) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (!value || value === "الكل" || value === "featured") return;
    if (key === "sale" && value !== "1" && value !== true) return;
    query.set(key, value === true ? "1" : value);
  });
  const text = query.toString();
  return `#/shop${text ? `?${text}` : ""}`;
}

function navKey(route) {
  if (route.name === "tryon") return "tryon";
  if (route.name !== "shop") return "";
  if (route.query.get("sale") === "1" && !route.query.get("kind") && !route.query.get("audience")) return "sale";
  if (route.query.get("audience") === "أطفال" && !route.query.get("kind")) return "kids";
  if (route.query.get("kind") === "شمسية" && !route.query.get("audience") && route.query.get("sale") !== "1") return "sun";
  if (route.query.get("kind") === "طبية" && !route.query.get("audience") && route.query.get("sale") !== "1") return "medical";
  return "";
}

function refreshChrome(route) {
  const count = cartCount();
  const badge = document.getElementById("cart-count");
  badge.textContent = String(count);
  badge.hidden = count <= 0;
  const key = navKey(route);
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.dataset.nav === key) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
}

function closeSearch() {
  const dialog = document.getElementById("search");
  if (dialog.open) dialog.close();
}

function matches(product, text) {
  const hay = [product.name, product.brand, product.category, product.kind, product.audience, product.color, product.description]
    .join(" ")
    .toLowerCase();
  return text.toLowerCase().split(/\s+/).filter(Boolean).every((word) => hay.includes(word));
}

function stockLabel(stock) {
  if (stock <= 0) return "نفد من التشكيلة";
  if (stock <= 3) return `آخر ${stock} قطع`;
  return "متوفر";
}

function brandLabel(brand) {
  const value = String(brand || "");
  if (value === "نظارات مسلم" || value === "مسلم" || /^(moslem|muslam|muslem)$/i.test(value)) return "Muslem";
  return value;
}

function bestsellerIds() {
  return new Set(
    catalog
      .slice()
      .sort((a, b) => Number(b.sold || 0) - Number(a.sold || 0))
      .slice(0, 4)
      .map((item) => item.id),
  );
}

function waHref(text) {
  const digits = String(shop.phone || "01148005679").replace(/\D/g, "");
  const waPhone = digits.startsWith("0") ? `2${digits}` : digits;
  return `https://wa.me/${waPhone}?text=${encodeURIComponent(text)}`;
}

function openBuy(id, qty) {
  const product = byId(id);
  if (!product || product.stock <= 0) {
    toast("هذا الإطار نفد من التشكيلة.");
    return;
  }
  const dialog = document.getElementById("buy-choice");
  dialog.dataset.product = product.id;
  dialog.dataset.qty = String(Math.max(1, Math.min(5, Number(qty) || 1)));
  document.getElementById("buy-choice-name").textContent = `${brandLabel(product.brand)} · ${product.name}`;
  document.getElementById("buy-wa").hidden = true;
  document.getElementById("buy-wa-link").href = waHref("برجاء ارسال الكشف والعدسه المحدده");
  if (!dialog.open) dialog.showModal();
}

function card(product) {
  const discount = off(product);
  const gone = product.stock <= 0;
  const best = bestsellerIds().has(product.id);
  const flags = [
    discount ? `<span class="flag sale">SALE</span>` : "",
    best ? `<span class="flag">BESTSELLER</span>` : "",
    gone ? `<span class="flag sold">SOLD OUT</span>` : "",
  ].filter(Boolean).join("");
  return `
    <article class="card${gone ? " is-out" : ""}">
      <a class="card-visual" href="#/product/${encodeURIComponent(product.id)}">
        ${flags ? `<span class="flags">${flags}</span>` : ""}
        <img src="${esc(product.image)}" alt="${esc(product.name)}">
      </a>
      <p class="card-brand">${esc(brandLabel(product.brand))}</p>
      <a class="card-name" href="#/product/${encodeURIComponent(product.id)}">${esc(product.name)}</a>
      <div class="card-price${discount ? " is-sale" : ""}"><strong>${money(product.price)}</strong>${discount ? `<s>${money(product.old_price)}</s>` : ""}</div>
      <button type="button" class="card-buy" data-buy="${esc(product.id)}" ${gone ? "disabled" : ""}>شراء</button>
    </article>
  `;
}

function filtered(route) {
  const query = route.query;
  let items = catalog.slice();
  const q = (query.get("q") || "").trim();
  const kind = query.get("kind") || "";
  const audience = query.get("audience") || "";
  const category = query.get("category") || "";
  const brand = query.get("brand") || "";
  const sale = query.get("sale") === "1";
  const sort = query.get("sort") || "featured";
  if (q) items = items.filter((item) => matches(item, q));
  if (kind) items = items.filter((item) => item.kind === kind);
  if (audience) {
    items = items.filter((item) => item.audience === audience || (audience !== "أطفال" && item.audience === "للجميع"));
  }
  if (category) items = items.filter((item) => item.category === category);
  if (brand) items = items.filter((item) => item.brand === brand);
  if (sale) items = items.filter((item) => off(item) > 0);
  if (sort === "price-asc") items.sort((a, b) => a.price - b.price);
  if (sort === "price-desc") items.sort((a, b) => b.price - a.price);
  if (sort === "sold") items.sort((a, b) => b.sold - a.sold);
  return items;
}

function shopTitle(route) {
  const query = route.query;
  if (query.get("sale") === "1" && !query.get("kind")) return "تخفيضات";
  if (query.get("audience") === "أطفال") return "نظارات الأطفال";
  if (query.get("kind") === "شمسية" && query.get("audience") === "رجالي") return "نظارات شمسية رجالي";
  if (query.get("kind") === "شمسية" && query.get("audience") === "حريمي") return "نظارات شمسية حريمي";
  if (query.get("kind") === "شمسية") return "النظارات الشمسية";
  if (query.get("kind") === "طبية") return "النظارات الطبية";
  if (query.get("brand")) return query.get("brand");
  if (query.get("q")) return `نتائج «${query.get("q")}»`;
  return "التشكيلة";
}

function unique(key) {
  return [...new Set(catalog.map((item) => item[key]).filter(Boolean))];
}

function option(value, label, current) {
  return `<option value="${esc(value)}"${value === current ? " selected" : ""}>${esc(label)}</option>`;
}

function homeHtml() {
  const pick = (id, fallback) => byId(id) || catalog.find(fallback) || catalog[0];
  const heroSun = pick("wayfarer-black", (item) => item.kind === "شمسية");
  const heroTry = pick("aviator-silver", (item) => item.kind === "شمسية");
  const heroRx = pick("classic-black", (item) => item.kind === "طبية");
  const her = pick("round-sun-gold", (item) => item.audience === "حريمي" && item.kind === "شمسية");
  const him = pick("aviator-silver", (item) => item.audience === "رجالي" && item.kind === "شمسية");
  const best = catalog.slice().sort((a, b) => b.sold - a.sold).slice(0, 4);
  const medical = catalog.filter((item) => item.kind === "طبية" && item.audience !== "أطفال").slice(0, 4);
  const kids = catalog.filter((item) => item.audience === "أطفال").slice(0, 4);
  const brands = unique("brand");
  const slide = (theme, product, kicker, title, text, primary, secondary) => `
    <article class="slide ${theme}">
      <div class="hero-copy">
        <p class="kicker${theme === "sand" ? "" : " light"}">${kicker}</p>
        <h1>${title}</h1>
        <p>${text}</p>
        <div class="hero-actions">
          <a class="btn ${theme === "sand" ? "" : "light"}" href="${primary.href}">${primary.label}</a>
          <a class="text-link" href="${secondary.href}">${secondary.label}</a>
        </div>
      </div>
      <div class="hero-visual">${product ? `<img src="${esc(product.image)}" alt="${esc(product.name)}">` : ""}</div>
    </article>
  `;
  return `
    <section class="hero" id="hero">
      ${slide("wine", heroSun, "BAB EL LOUK", "إطلالة أوضح<br>من باب اللوق", "نظارات طبية وشمسية من محل واحد، جاهزة للتجربة على وجهك قبل الطلب.", { href: "#/shop", label: "تسوق التشكيلة" }, { href: "#/tryon", label: "جرّب على وجهك" })}
      ${slide("ink", heroTry, "LIVE TRY-ON", "الإطار على وجهك<br>قبل ما تطلبه", "افتح الكاميرا. التتبّع يثبت النظارة على عينيك مباشرة، والصورة تبقى على جهازك.", { href: "#/tryon", label: "ابدأ التجربة الحية" }, { href: "#/shop?kind=شمسية", label: "النظارات الشمسية" })}
      ${slide("sand", heroRx, "OPTICAL", "أساسيات النظارات<br>الطبية", "إطارات يومية من باب اللوق، مع عدسة عادية أو Blue Cut أو طبية شمسية.", { href: "#/shop?kind=طبية", label: "تسوق الطبية" }, { href: "#/shipping", label: "التوصيل" })}
      <button type="button" class="hero-arrow prev" data-hero="-1" aria-label="الشريحة السابقة">‹</button>
      <button type="button" class="hero-arrow next" data-hero="1" aria-label="الشريحة التالية">›</button>
      <div class="hero-dots" id="hero-dots"></div>
    </section>
    <div class="wrap mosaic">
      <a class="tile rose" href="#/shop?kind=شمسية&audience=حريمي">
        ${her ? `<img src="${esc(her.image)}" alt="">` : ""}
        <span><small>لها</small><strong>نظارات شمسية</strong></span>
      </a>
      <a class="tile stone" href="#/shop?kind=شمسية&audience=رجالي">
        ${him ? `<img src="${esc(him.image)}" alt="">` : ""}
        <span><small>له</small><strong>نظارات شمسية</strong></span>
      </a>
    </div>
    <section class="wrap section">
      <div class="rail-head">
        <div><p class="kicker">BESTSELLERS</p><h2>الأكثر طلباً</h2></div>
        <a href="#/shop?sort=sold">عرض الكل</a>
      </div>
      <div class="grid">${best.map(card).join("")}</div>
    </section>
    <section class="band ink">
      <div class="wrap section try-banner">
        <div>
          <p class="kicker light">LIVE VIRTUAL TRY-ON</p>
          <h2>قف أمام الكاميرا وجرّب الإطار</h2>
          <p>تتبّع للعينين لحظة بلحظة، مع اقتراح شكل الوجه. لا نرفع صورة الكاميرا.</p>
          <a class="btn light" href="#/tryon/${encodeURIComponent(heroTry?.id || "")}">افتح التجربة</a>
        </div>
        <img src="${esc(heroTry?.image || "")}" alt="">
      </div>
    </section>
    <section class="wrap section">
      <div class="rail-head">
        <div><p class="kicker">EVERYDAY</p><h2>أساسيات النظارات الطبية</h2></div>
        <a href="#/shop?kind=طبية">عرض الكل</a>
      </div>
      <div class="grid">${medical.map(card).join("")}</div>
    </section>
    <section class="band">
      <div class="wrap section">
        <div class="rail-head">
          <div><p class="kicker">KIDS</p><h2>إطارات خفيفة للأطفال</h2></div>
          <a href="#/shop?audience=أطفال">عرض الكل</a>
        </div>
        <div class="grid">${kids.map(card).join("")}</div>
      </div>
    </section>
    <section class="wrap">
      <div class="benefits">
        <article><h3>تجربة حية</h3><p>الكاميرا تتبع الوجه والإطار يتحرك معك قبل الشراء.</p></article>
        <article><h3>محل واحد</h3><p>كل الإطارات من مسلم - Muslem Optics في باب اللوق، من غير منصة تجّار.</p></article>
        <article><h3>عدسات على المقاس</h3><p>عدسة عادية، Blue Cut، أو طبية شمسية. الروشتة تُراجع قبل القص.</p></article>
        <article><h3>توصيل المحافظات</h3><p>الرسوم والمدة تظهر قبل تأكيد الطلب، والدفع عند الاستلام متاح.</p></article>
      </div>
    </section>
    <section class="wrap section brands">
      <p class="kicker">AT THE SHOP</p>
      <h2>ماركات تجدها في المحل</h2>
      <div class="brand-row">${brands.map((brand) => `<a href="${shopHref({ brand })}">${esc(brandLabel(brand))}</a>`).join("")}</div>
    </section>
  `;
}

function bindHome() {
  const slides = [...view.querySelectorAll(".slide")];
  const hero = view.querySelector("#hero");
  const dots = view.querySelector("#hero-dots");
  if (!slides.length) return () => {};
  let index = 0;
  dots.innerHTML = slides.map((_, dot) => `<button type="button" data-dot="${dot}" aria-label="شريحة ${dot + 1}"></button>`).join("");
  const showSlide = (next) => {
    index = (next + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => slide.classList.toggle("is-on", slideIndex === index));
    dots.querySelectorAll("button").forEach((button, dot) => button.classList.toggle("is-on", dot === index));
    hero.classList.toggle("theme-sand", slides[index].classList.contains("sand"));
  };
  showSlide(0);
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const timer = reduced ? 0 : setInterval(() => showSlide(index + 1), 6800);
  hero.addEventListener("click", (event) => {
    const arrow = event.target.closest("[data-hero]");
    const dot = event.target.closest("[data-dot]");
    if (arrow) showSlide(index + Number(arrow.dataset.hero));
    if (dot) showSlide(Number(dot.dataset.dot));
  });
  return () => { if (timer) clearInterval(timer); };
}

function shopHtml(route) {
  const items = filtered(route);
  const current = {
    kind: route.query.get("kind") || "الكل",
    audience: route.query.get("audience") || "الكل",
    category: route.query.get("category") || "الكل",
    brand: route.query.get("brand") || "الكل",
    sort: route.query.get("sort") || "featured",
    sale: route.query.get("sale") === "1",
    q: route.query.get("q") || "",
  };
  const kinds = ["الكل", ...unique("kind")];
  const audiences = ["الكل", ...unique("audience").filter((item) => item !== "للجميع")];
  const categories = ["الكل", ...unique("category")];
  const brands = ["الكل", ...unique("brand")];
  return `
    <section class="wrap page">
      <header class="page-head">
        <div>
          <p class="kicker">SHOP</p>
          <h1>${esc(shopTitle(route))}</h1>
        </div>
        <p class="count">${items.length} إطاراً</p>
      </header>
      ${current.q ? `<a class="chip" href="${shopHref({ ...current, q: "", sale: current.sale ? "1" : "" })}">بحث: ${esc(current.q)} ×</a>` : ""}
      <form class="filters" id="filters">
        <label>النوع<select name="kind">${kinds.map((item) => option(item, item === "الكل" ? "الكل" : item, current.kind)).join("")}</select></label>
        <label>الفئة<select name="audience">${audiences.map((item) => option(item, item, current.audience)).join("")}</select></label>
        <label>شكل الإطار<select name="category">${categories.map((item) => option(item, item, current.category)).join("")}</select></label>
        <label>الماركة<select name="brand">${brands.map((item) => option(item, item === "الكل" ? "الكل" : brandLabel(item), current.brand)).join("")}</select></label>
        <label>الترتيب<select name="sort">
          ${option("featured", "ترتيب المحل", current.sort)}
          ${option("sold", "الأكثر طلباً", current.sort)}
          ${option("price-asc", "السعر: الأقل", current.sort)}
          ${option("price-desc", "السعر: الأعلى", current.sort)}
        </select></label>
      </form>
      <label class="stack" style="margin:-12px 0 22px"><span style="display:flex;gap:8px;align-items:center"><input id="sale-only" type="checkbox" ${current.sale ? "checked" : ""} style="width:auto;min-height:0"> التخفيضات فقط</span></label>
      ${items.length ? `<div class="grid">${items.map(card).join("")}</div>` : `<p class="empty">لا توجد إطارات بهذه الاختيارات. <a href="#/shop" style="border-bottom:1px solid #111">اعرض التشكيلة كلها</a></p>`}
    </section>
  `;
}

function bindShop() {
  const form = view.querySelector("#filters");
  const sale = view.querySelector("#sale-only");
  const apply = () => {
    const data = Object.fromEntries(new FormData(form).entries());
    if (sale.checked) data.sale = "1";
    const q = parseRoute().query.get("q") || "";
    if (q) data.q = q;
    location.hash = shopHref(data);
  };
  form.addEventListener("change", apply);
  sale.addEventListener("change", apply);
}

function productHtml(id) {
  const product = byId(id);
  if (!product) {
    return `<section class="wrap page"><h1>الإطار غير موجود</h1><p class="empty"><a href="#/shop">العودة إلى التشكيلة</a></p></section>`;
  }
  const discount = off(product);
  const related = catalog.filter((item) => item.id !== product.id && item.kind === product.kind).slice(0, 4);
  return `
    <section class="wrap page">
      <nav class="crumbs" aria-label="مسار الصفحة">
        <a href="#/">الرئيسية</a><span>/</span>
        <a href="${shopHref({ kind: product.kind })}">${esc(product.kind)}</a><span>/</span>
        <span>${esc(product.name)}</span>
      </nav>
      <div class="pdp">
        <div class="pdp-gallery">
          <a class="try-live" href="#/tryon/${encodeURIComponent(product.id)}">👓 التجربة الحية (افتح الكاميرا)</a>
          <img src="${esc(product.image)}" alt="${esc(product.name)}">
        </div>
        <div class="pdp-info">
          <p class="card-brand">${esc(brandLabel(product.brand))}</p>
          <h1>${esc(product.name)}</h1>
          <div class="price-row${discount ? " is-sale" : ""}"><strong>${money(product.price)}</strong>${discount ? `<s>${money(product.old_price)}</s><span class="badge">SALE</span>` : ""}</div>
          <p class="lead">${esc(product.description)}</p>
          <div class="facts">
            <span>${esc(product.color)} · ${esc(product.category)} · ${esc(product.audience)}</span>
            <span>${stockLabel(product.stock)} · تقييم ${esc(product.rating)}</span>
            <span>يناسب الوجه: ${esc((product.face_shapes || []).join("، "))}</span>
          </div>
          <div class="buy-row">
            <label>الكمية<input id="buy-qty" type="number" min="1" max="${Math.max(1, Math.min(product.stock, 5))}" value="1" ${product.stock ? "" : "disabled"}></label>
            <button class="btn" type="button" data-buy="${esc(product.id)}" ${product.stock ? "" : "disabled"}>${product.stock ? "شراء" : "نفد"}</button>
          </div>
          <p class="note">بدون عدسات تنتقل إلى بيانات الشحن. العدسات الطبية تُطلب عبر واتساب المحل.</p>
        </div>
      </div>
      ${related.length ? `<div class="section"><div class="rail-head"><h2>إطارات قريبة</h2></div><div class="grid">${related.map(card).join("")}</div></div>` : ""}
    </section>
  `;
}

function lineHtml(line) {
  const product = byId(line.productId);
  const lens = lensById(line.lens);
  if (!product) {
    return `<article class="line"><div></div><div><h3>إطار لم يعد في التشكيلة</h3><button class="textish" type="button" data-remove="${esc(line.id)}">حذف</button></div><div></div></article>`;
  }
  return `
    <article class="line">
      <a href="#/product/${encodeURIComponent(product.id)}"><img src="${esc(product.image)}" alt=""></a>
      <div>
        <h3><a href="#/product/${encodeURIComponent(product.id)}">${esc(product.name)}</a></h3>
        <p class="muted">${esc(brandLabel(product.brand))}${lens ? ` · ${esc(lens.label)}` : ""}</p>
        <div class="qty">
          <button type="button" data-qty="-1" data-line="${esc(line.id)}" aria-label="تقليل">−</button>
          <span>${line.qty}</span>
          <button type="button" data-qty="1" data-line="${esc(line.id)}" aria-label="زيادة">+</button>
          <button type="button" class="textish" data-remove="${esc(line.id)}">حذف</button>
        </div>
      </div>
      <strong class="line-price">${money(unitPrice(line) * line.qty)}</strong>
    </article>
  `;
}

function cartHtml() {
  const lines = getCart();
  if (!lines.length) {
    return `<section class="wrap page"><p class="kicker">BAG</p><h1>السلة فارغة</h1><p class="empty">اختر إطاراً من التشكيلة أو جرّبه على وجهك أولاً.</p><a class="btn" href="#/shop">تسوق التشكيلة</a></section>`;
  }
  return `
    <section class="wrap page">
      <p class="kicker">BAG</p>
      <h1>السلة</h1>
      <div class="layout" style="margin-top:22px">
        <div>${lines.map(lineHtml).join("")}</div>
        <aside class="summary">
          <h2>الملخص</h2>
          <div><span>الإطارات</span><strong>${money(cartSubtotal())}</strong></div>
          <p class="muted">رسوم التوصيل تُضاف في الخطوة التالية حسب المحافظة.</p>
          <a class="btn block" href="#/checkout">إتمام الطلب</a>
          <a class="text-link" href="#/shop">متابعة التسوق</a>
        </aside>
      </div>
    </section>
  `;
}

function checkoutHtml() {
  const lines = getCart();
  if (!lines.length) return cartHtml();
  const missing = lines.some((line) => !byId(line.productId));
  const medical = lines.some((line) => line.lens && line.lens !== "none" && byId(line.productId)?.kind === "طبية");
  const gov = governorates.map((item) => `<option value="${esc(item.name)}">${esc(item.name)} · ${money(item.fee)}</option>`).join("");
  const pays = payments.map((item, index) => `<label><span><input type="radio" name="payment" value="${esc(item.id)}" ${index === 0 ? "checked" : ""}> ${esc(item.label)}</span></label>`).join("");
  return `
    <section class="wrap page">
      <p class="kicker">CHECKOUT</p>
      <h1>إتمام الطلب</h1>
      <div class="layout" style="margin-top:22px">
        <form class="stack" id="checkout">
          ${missing ? `<p class="form-error">في السلة إطار لم يعد متاحاً. احذفه قبل المتابعة.</p>` : ""}
          <label>الاسم<input name="name" autocomplete="name" required placeholder="الاسم الثلاثي"></label>
          <label>الهاتف<input name="phone" autocomplete="tel" inputmode="tel" required placeholder="01xxxxxxxxx"></label>
          <label>المحافظة<select name="governorate" id="gov">${gov}</select></label>
          <label>العنوان<textarea name="address" required placeholder="الشارع، العلامة، رقم العمارة"></textarea></label>
          <fieldset class="lenses"><legend class="kicker">الدفع</legend>${pays}</fieldset>
          <div class="pay-box" id="pay-box" hidden>
            <p id="pay-help"></p>
            <label style="margin-top:8px">رقم العملية<input name="reference" placeholder="رقم التحويل"></label>
          </div>
          ${medical ? `
            <div class="measures">
              <h3>مقاس الروشتة، إن وُجد</h3>
              <label>العين اليمنى SPH<input name="od_sph" inputmode="decimal" placeholder="0.00"></label>
              <label>العين اليسرى SPH<input name="os_sph" inputmode="decimal" placeholder="0.00"></label>
              <label>اليمنى CYL<input name="od_cyl" inputmode="decimal" placeholder="0.00"></label>
              <label>اليسرى CYL<input name="os_cyl" inputmode="decimal" placeholder="0.00"></label>
              <label>اليمنى AXIS<input name="od_axis" inputmode="numeric" placeholder="0"></label>
              <label>اليسرى AXIS<input name="os_axis" inputmode="numeric" placeholder="0"></label>
            </div>
            <p class="muted">يمكن ترك المقاس فارغاً وإرسال صورة الروشتة على واتساب بعد الطلب. العدسة لا تُقص قبل المراجعة.</p>
          ` : ""}
          <label>ملاحظة<textarea name="note" placeholder="موعد مفضّل، أو تفصيل للعنوان"></textarea></label>
          <p class="form-error" id="checkout-error" hidden></p>
          <button class="btn" id="place" type="submit">تأكيد الطلب</button>
        </form>
        <aside class="summary" id="summary"></aside>
      </div>
    </section>
  `;
}

function feeFor(name) {
  return governorates.find((item) => item.name === name) || governorates[0] || { fee: 0, eta: "" };
}

function siteBase() {
  const path = location.pathname || "/";
  return path.endsWith("/") ? path : path.replace(/[^/]*$/, "");
}

function readSavedOrder(id) {
  try {
    const parsed = JSON.parse(sessionStorage.getItem(`moslem-order-${id}`) || "null");
    return parsed && parsed.id ? parsed : null;
  } catch {
    return null;
  }
}

function rememberOrder(data, lines) {
  const ship = feeFor(data.governorate);
  const detailed = lines.map((line) => {
    const product = byId(line.productId);
    const lens = lensById(line.lens);
    const unit = (product ? product.price : 0) + (lens ? lens.price : 0);
    return {
      name: product?.name || "إطار",
      qty: line.qty,
      lens_label: lens?.label || "",
      price: unit,
      image: product?.image || "",
    };
  });
  const subtotal = detailed.reduce((sum, line) => sum + line.price * Number(line.qty || 0), 0);
  const id = `MO-${Math.random().toString(16).slice(2, 8).toUpperCase()}`;
  const payment = payments.find((item) => item.id === data.payment);
  const text = [
    "مرحباً، أتممت طلباً من مسلم - Muslem Optics.",
    `رقم الطلب: ${id}`,
    `الاسم: ${data.name}`,
    `الهاتف: ${data.phone}`,
    `العنوان: ${data.address} — ${data.governorate}`,
    ...detailed.map((line) => `${line.name} × ${line.qty}${line.lens_label ? ` (${line.lens_label})` : ""}`),
    `الإجمالي: ${subtotal + Number(ship.fee || 0)} جنيه`,
    data.note ? `ملاحظة: ${data.note}` : "",
  ].filter(Boolean).join("\n");
  const digits = String(shop.phone || "01148005679").replace(/\D/g, "");
  const waPhone = digits.startsWith("0") ? `2${digits}` : digits;
  const order = {
    id,
    created: new Date().toISOString().slice(0, 16).replace("T", " "),
    status: STEPS[0],
    name: data.name,
    phone: data.phone,
    address: data.address,
    governorate: data.governorate,
    eta: ship.eta,
    fee: ship.fee,
    subtotal,
    total: subtotal + Number(ship.fee || 0),
    payment: payment?.label || data.payment,
    payment_ref: data.reference || "",
    lines: detailed,
    whatsapp: `https://wa.me/${waPhone}?text=${encodeURIComponent(text)}`,
  };
  sessionStorage.setItem(`moslem-order-${id}`, JSON.stringify(order));
  return order;
}

function paintSummary() {
  const box = view.querySelector("#summary");
  if (!box) return;
  const govName = view.querySelector("#gov")?.value || governorates[0]?.name;
  const ship = feeFor(govName);
  const subtotal = cartSubtotal();
  box.innerHTML = `
    <h2>طلبك</h2>
    ${getCart().map((line) => {
      const product = byId(line.productId);
      return `<div><span>${esc(product?.name || "إطار")} × ${line.qty}</span><span>${money(unitPrice(line) * line.qty)}</span></div>`;
    }).join("")}
    <div class="sum-row"><span>الإطارات</span><span>${money(subtotal)}</span></div>
    <div class="sum-row"><span>التوصيل إلى ${esc(govName || "")}</span><span>${money(ship.fee)}</span></div>
    <div class="sum-row total"><span>الإجمالي</span><span>${money(subtotal + ship.fee)}</span></div>
    <p class="muted">الوصول المتوقع: ${esc(ship.eta)}</p>
  `;
}

function bindCheckout() {
  const form = view.querySelector("#checkout");
  if (!form) return;
  const box = view.querySelector("#pay-box");
  const help = view.querySelector("#pay-help");
  const error = view.querySelector("#checkout-error");
  const describe = () => {
    const method = new FormData(form).get("payment");
    box.hidden = method === "cod";
    if (method === "instapay") help.textContent = `حوّل إلى InstaPay: ${shop.instapay} ثم اكتب رقم العملية.`;
    if (method === "vodafone") help.textContent = `حوّل فودافون كاش إلى ${shop.vodafone} ثم اكتب رقم العملية.`;
  };
  form.addEventListener("change", () => {
    describe();
    paintSummary();
  });
  describe();
  paintSummary();
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    error.hidden = true;
    const data = Object.fromEntries(new FormData(form).entries());
    const lines = getCart();
    if (!lines.length || lines.some((line) => !byId(line.productId))) {
      error.textContent = "راجع السلة قبل تأكيد الطلب.";
      error.hidden = false;
      return;
    }
    const button = view.querySelector("#place");
    button.disabled = true;
    const measures = {
      od: { sph: data.od_sph, cyl: data.od_cyl, axis: data.od_axis },
      os: { sph: data.os_sph, cyl: data.os_cyl, axis: data.os_axis },
    };
    const finish = (orderId) => {
      setCart([]);
      sessionStorage.setItem("moslem-just-ordered", orderId);
      refreshChrome(parseRoute());
      location.hash = `#/order/${encodeURIComponent(orderId)}`;
    };
    try {
      const response = await fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: data.name,
          phone: data.phone,
          address: data.address,
          governorate: data.governorate,
          payment: data.payment,
          reference: data.reference || "",
          note: data.note || "",
          measures,
          lines: lines.map((line) => ({ product_id: line.productId, qty: line.qty, lens: line.lens })),
        }),
      });
      const raw = await response.text();
      let payload = null;
      try {
        payload = JSON.parse(raw);
      } catch {
        payload = null;
      }
      if (payload && payload.error && response.status >= 400 && response.status < 500) {
        throw new Error(payload.error);
      }
      if (!response.ok || !payload || !payload.id) throw new Error("offline");
      finish(payload.id);
    } catch (err) {
      if (err && err.message && err.message !== "offline") {
        error.textContent = err.message;
        error.hidden = false;
        button.disabled = false;
        return;
      }
      finish(rememberOrder(data, lines).id);
    }
  });
}

function orderHtml(order, fresh) {
  const step = Math.max(0, STEPS.indexOf(order.status));
  const measureText = order.measures ? `مقاس مرفق مع الطلب.` : "";
  return `
    <section class="wrap page">
      <p class="kicker">${fresh ? "THANK YOU" : "ORDER"}</p>
      <h1>${fresh ? "استلمنا طلبك" : "حالة الطلب"}</h1>
      <p class="order-id">${esc(order.id)}</p>
      <p>${fresh ? "سيجهز المحل الطلب من باب اللوق. احتفظ برقم الطلب لتتبعه." : `بتاريخ ${esc(order.created)}`}</p>
      <div class="steps">${STEPS.map((label, index) => `<span class="${index <= step ? "is-on" : ""}">${esc(label)}</span>`).join("")}</div>
      <div class="layout">
        <div>
          ${(order.lines || []).map((line) => `
            <article class="line">
              <img src="${esc(line.image || "")}" alt="">
              <div>
                <h3>${esc(line.name)}</h3>
                <p class="muted">${esc(line.lens_label || "")} · الكمية ${esc(line.qty)}</p>
              </div>
              <strong>${money(line.price * line.qty)}</strong>
            </article>
          `).join("")}
        </div>
        <aside class="summary">
          <h2>التسليم</h2>
          <p>${esc(order.name)}</p>
          <p>${esc(order.phone)}</p>
          <p>${esc(order.address)} — ${esc(order.governorate)}</p>
          <p class="muted">الوصول المتوقع: ${esc(order.eta)}</p>
          <div class="sum-row"><span>الإطارات</span><span>${money(order.subtotal)}</span></div>
          <div class="sum-row"><span>التوصيل</span><span>${money(order.fee)}</span></div>
          <div class="sum-row total"><span>الإجمالي</span><span>${money(order.total)}</span></div>
          <p>الدفع: ${esc(order.payment)}${order.payment_ref ? ` · ${esc(order.payment_ref)}` : ""}</p>
          ${measureText ? `<p class="muted">${measureText}</p>` : ""}
          ${order.whatsapp ? `<a class="btn block" href="${esc(order.whatsapp)}" target="_blank" rel="noopener">إرسال الطلب على واتساب</a>` : ""}
        </aside>
      </div>
    </section>
  `;
}

function showOrder(order) {
  const fresh = sessionStorage.getItem("moslem-just-ordered") === order.id;
  if (fresh) sessionStorage.removeItem("moslem-just-ordered");
  view.innerHTML = orderHtml(order, fresh);
}

async function renderOrder(id, token) {
  document.title = "الطلب | مسلم";
  const saved = readSavedOrder(id);
  try {
    const response = await fetch(`/api/orders/${encodeURIComponent(id)}`);
    const raw = await response.text();
    let payload = null;
    try {
      payload = JSON.parse(raw);
    } catch {
      payload = null;
    }
    if (token !== viewToken) return;
    if (response.ok && payload && payload.id) {
      showOrder(payload);
      return;
    }
  } catch {
    if (token !== viewToken) return;
  }
  if (saved) {
    showOrder(saved);
    return;
  }
  view.innerHTML = `<section class="wrap page"><h1>لا يوجد طلب بهذا الرقم</h1><p class="empty">تأكد من الرقم، مثل MO-AB12CD.</p><a class="btn" href="#/track">تتبّع طلب</a></section>`;
}

function prose(kicker, title, body) {
  document.title = `${title} | مسلم`;
  return `<article class="wrap prose"><p class="kicker">${kicker}</p><h1>${title}</h1>${body}</article>`;
}

function pageHtml(name) {
  const phone = esc(shop.phone || "");
  const wa = esc(shop.whatsapp || "#");
  if (name === "about") {
    return prose("THE SHOP", "عن مسلم", `
      <p>مسلم - Muslem Optics محل نظارات في باب اللوق بالقاهرة. هذا الموقع واجهة المحل نفسه: الإطارات المعروضة تُختار وتُشحن منه، وليست سوقاً لمحلات أخرى.</p>
      <p>تجد في التشكيلة نظارات طبية وشمسية للرجال والنساء والأطفال، وبعض الماركات الموجودة داخل المحل مثل أوكلي وبوليس إلى جانب إطارات مسلم.</p>
      <p>يمكن تجربة الإطار على الوجه بالكاميرا قبل الطلب. الصورة تُعالج في متصفحك ولا تُرفع إلينا.</p>
    `);
  }
  if (name === "shipping") {
    const rows = governorates.map((item) => `<tr><td>${esc(item.name)}</td><td>${money(item.fee)}</td><td>${esc(item.eta)}</td></tr>`).join("");
    return prose("DELIVERY", "الشحن والتوصيل", `
      <p>يخرج الطلب من باب اللوق. الرسوم تقديرية وتظهر في صفحة الإتمام قبل التأكيد.</p>
      <table class="table"><thead><tr><th>المحافظة</th><th>الرسوم</th><th>الوصول المتوقع</th></tr></thead><tbody>${rows}</tbody></table>
    `);
  }
  if (name === "returns") {
    return prose("RETURNS", "الاستبدال والإرجاع", `
      <p>يمكن طلب استبدال الإطار خلال 14 يوماً إذا كان بحالته الأصلية ومن غير خدش أو تعديل.</p>
      <p>العدسة الطبية التي قُصّت على مقاس الروشتة لا تُستبدل إلا إذا كان الخطأ من المحل في تنفيذ المقاس.</p>
      <p>لبدء طلب، أرسل رقم الطلب على واتساب <a href="${wa}" target="_blank" rel="noopener">${phone}</a>.</p>
    `);
  }
  if (name === "faq") {
    return prose("FAQ", "الأسئلة الشائعة", `
      <h2>هل التجربة الحية ترفع صورتي؟</h2>
      <p>لا. الكاميرا وتتبع الوجه يعملان داخل المتصفح، واللقطة التي تحفظها تبقى على جهازك.</p>
      <h2>كيف أرسل الروشتة؟</h2>
      <p>اكتب المقاس عند إتمام الطلب، أو أرسل صورة الروشتة على واتساب مع رقم الطلب قبل قص العدسة.</p>
      <h2>ما طرق الدفع؟</h2>
      <p>الدفع عند الاستلام، أو InstaPay على ${esc(shop.instapay || "")}، أو فودافون كاش على ${phone}.</p>
      <h2>من أين يصل الطلب؟</h2>
      <p>من مسلم - Muslem Optics في ${esc(shop.address || "باب اللوق")}. لا يوجد تجار آخرون على الموقع.</p>
    `);
  }
  if (name === "contact") {
    return prose("VISIT", "تواصل معنا", `
      <p>العنوان: ${esc(shop.address || "")}</p>
      <p>الهاتف: <a href="tel:${phone}">${phone}</a></p>
      <p><a href="${wa}" target="_blank" rel="noopener">واتساب</a></p>
      <p><a href="${esc(shop.instagram || "#")}" target="_blank" rel="noopener">إنستغرام</a></p>
      <p><a href="${esc(shop.facebook || "#")}" target="_blank" rel="noopener">فيسبوك</a></p>
    `);
  }
  if (name === "privacy") {
    return prose("PRIVACY", "الخصوصية", `
      <p>نحفظ بيانات الطلب التي تكتبها: الاسم والهاتف والعنوان ومحتوى السلة، حتى نجهّز الشحنة من المحل. تبقى هذه البيانات على جهاز تشغيل المتجر.</p>
      <p>صورة الكاميرا في التجربة الحية لا تُرسل إلى الخادم. نموذج تتبع الوجه يُحمَّل في متصفحك من خدمة MediaPipe.</p>
    `);
  }
  if (name === "terms") {
    return prose("TERMS", "الشروط", `
      <p>الأسعار بالجنيه المصري وتشمل الإطار والعدسة المختارة، ولا تشمل التوصيل إلا بعد اختيار المحافظة.</p>
      <p>المخزون يُحدَّث عند تأكيد الطلب. إذا نفدت الكمية قبل التأكيد تظهر رسالة ولن يُخصم المبلغ من المخزون.</p>
      <p>الموقع خاص بمسلم - Muslem Optics في باب اللوق، وليس منصة لتسجيل محلات.</p>
    `);
  }
  return prose("404", "الصفحة غير موجودة", `<p><a href="#/">العودة إلى الرئيسية</a></p>`);
}

function render(route, token) {
  const titles = {
    home: "مسلم | Muslem Optics",
    shop: `${shopTitle(route)} | مسلم`,
    product: "الإطار | مسلم",
    cart: "السلة | مسلم",
    checkout: "إتمام الطلب | مسلم",
    track: "تتبّع الطلب | مسلم",
    tryon: "التجربة الحية | مسلم",
  };
  if (titles[route.name]) document.title = titles[route.name];
  if (route.name === "home") return homeHtml();
  if (route.name === "shop") return shopHtml(route);
  if (route.name === "product") {
    const product = byId(route.id);
    if (product) document.title = `${product.name} | مسلم`;
    return productHtml(route.id);
  }
  if (route.name === "cart") return cartHtml();
  if (route.name === "checkout") return checkoutHtml();
  if (route.name === "order") {
    renderOrder(route.id, token);
    return `<section class="wrap page"><p class="loading">جاري جلب الطلب…</p></section>`;
  }
  if (route.name === "track") {
    return `<section class="wrap page"><p class="kicker">TRACK</p><h1>تتبّع الطلب</h1><form class="stack" id="track" style="max-width:460px;margin-top:18px"><label>رقم الطلب<input name="id" required placeholder="MO-AB12CD" value="${esc(route.query.get("id") || "")}"></label><button class="btn" type="submit">عرض الحالة</button></form></section>`;
  }
  if (route.name === "tryon") return `<div id="try-root"></div>`;
  return pageHtml(route.name);
}

function bind(route, token) {
  if (route.name === "home") return bindHome();
  if (route.name === "shop") { bindShop(); return null; }
  if (route.name === "product") return null;
  if (route.name === "checkout") { bindCheckout(); return null; }
  if (route.name === "track") {
    view.querySelector("#track").addEventListener("submit", (event) => {
      event.preventDefault();
      const id = new FormData(event.target).get("id");
      location.hash = `#/order/${encodeURIComponent(String(id || "").trim())}`;
    });
    return null;
  }
  if (route.name === "tryon") {
    tryonApi = mountTryOn(view.querySelector("#try-root"), {
      products: catalog,
      initialId: route.id,
      lenses,
      money,
      onAdd(product, lens) {
        if (addToCart(product, lens, 1)) toast(`أُضيف ${esc(product.name)} إلى السلة. <a href="#/cart">عرض السلة</a>`);
      },
    });
    return () => {
      tryonApi.destroy();
      tryonApi = null;
    };
  }
  return null;
}

function show({ scroll = true } = {}) {
  const token = ++viewToken;
  const route = parseRoute();
  if (tryonApi && route.name === "tryon") {
    tryonApi.select(route.id);
    refreshChrome(route);
    closeSearch();
    return;
  }
  teardown();
  teardown = () => {};
  tryonApi = null;
  closeSearch();
  refreshChrome(route);
  const html = render(route, token);
  if (typeof html === "string") view.innerHTML = html;
  const extra = bind(route, token);
  if (typeof extra === "function") teardown = extra;
  if (scroll) window.scrollTo(0, 0);
}

function renderSearch(text) {
  const list = document.getElementById("search-results");
  const q = text.trim();
  if (!q) {
    list.innerHTML = "";
    return;
  }
  const found = catalog.filter((item) => matches(item, q)).slice(0, 8);
  list.innerHTML = found.map((item) => `
    <a href="#/product/${encodeURIComponent(item.id)}">
      <img src="${esc(item.image)}" alt="">
      <span>${esc(item.name)}<br><small class="muted">${esc(brandLabel(item.brand))}</small></span>
      <em>${money(item.price)}</em>
    </a>
  `).join("") + `<a class="search-all" href="${shopHref({ q })}">عرض كل النتائج</a>`;
}

function bootChrome() {
  document.getElementById("open-search").addEventListener("click", () => {
    document.getElementById("search").showModal();
    document.getElementById("q").focus();
  });
  document.getElementById("close-search").addEventListener("click", closeSearch);
  document.getElementById("q").addEventListener("input", (event) => renderSearch(event.target.value));
  document.getElementById("search-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const q = document.getElementById("q").value.trim();
    if (q) location.hash = shopHref({ q });
    closeSearch();
  });
  document.getElementById("buy-plain").addEventListener("click", () => {
    const dialog = document.getElementById("buy-choice");
    const product = byId(dialog.dataset.product || "");
    const qty = Math.max(1, Number(dialog.dataset.qty || 1));
    if (product && addToCart(product, "none", qty)) {
      dialog.close();
      location.hash = "#/checkout";
    }
  });
  document.getElementById("buy-rx").addEventListener("click", () => {
    document.getElementById("buy-wa").hidden = false;
  });
  document.getElementById("buy-close").addEventListener("click", () => {
    document.getElementById("buy-choice").close();
  });
  view.addEventListener("click", (event) => {
    const buy = event.target.closest("[data-buy]");
    if (buy && !buy.disabled) {
      const qtyField = buy.closest(".pdp") ? view.querySelector("#buy-qty") : null;
      openBuy(buy.dataset.buy, qtyField ? qtyField.value : 1);
      return;
    }
    const add = event.target.closest("[data-add]");
    if (add) {
      const product = byId(add.dataset.add);
      if (!product) return;
      const lens = product.kind === "طبية" ? "plain" : "none";
      if (addToCart(product, lens, 1)) toast(`أُضيف ${esc(product.name)} إلى السلة. <a href="#/cart">عرض السلة</a>`);
      return;
    }
    const qty = event.target.closest("[data-qty]");
    if (qty) {
      changeQty(qty.dataset.line, Number(qty.dataset.qty));
      show({ scroll: false });
      return;
    }
    const remove = event.target.closest("[data-remove]");
    if (remove) {
      removeLine(remove.dataset.remove);
      show({ scroll: false });
    }
  });
  window.addEventListener("hashchange", () => show());
}

function applyBootstrap(data) {
  const base = siteBase();
  catalog = (data.products || []).map((item) => {
    const image = String(item.image || "");
    if (image && !/^(https?:|\/)/.test(image)) item.image = base + image;
    return item;
  });
  shop = data.shop || {};
  governorates = data.governorates || [];
  lenses = data.lenses || [];
  payments = data.payments || [];
}

async function loadBootstrap() {
  try {
    const response = await fetch("/api/bootstrap");
    const type = response.headers.get("content-type") || "";
    if (response.ok && type.includes("json")) return await response.json();
  } catch {
    /* النسخة المنشورة تقرأ الملف الثابت */
  }
  const response = await fetch(`${siteBase()}bootstrap.json`);
  if (!response.ok) throw new Error("bootstrap");
  return await response.json();
}

async function boot() {
  bootChrome();
  try {
    applyBootstrap(await loadBootstrap());
  } catch {
    view.innerHTML = `<section class="wrap page"><h1>تعذر فتح التشكيلة</h1><p class="empty">أعد تشغيل المتجر من ملف run.bat ثم حدّث الصفحة.</p></section>`;
    return;
  }
  if (!location.hash) location.hash = "#/";
  else show();
}

boot();
