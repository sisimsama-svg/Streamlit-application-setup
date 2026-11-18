const SHAPES = ["كلاسيك", "دائري", "أفياتور", "كات آي", "رياضي", "مربع", "بيضاوي", "شفاف"];
const KINDS = ["طبية", "شمسية", "قراءة"];
const AUDIENCES = ["رجالي", "حريمي", "أطفال", "للجميع"];
const SHAPE_MAP = {
  "كلاسيك": ["دائري", "بيضاوي"],
  "مربع": ["دائري"],
  "كات آي": ["دائري", "بيضاوي"],
  "دائري": ["مربع", "مستطيل", "قلب"],
  "بيضاوي": ["مربع", "مستطيل", "قلب"],
  "أفياتور": ["مربع", "بيضاوي", "مستطيل", "قلب"],
  "شفاف": ["بيضاوي"],
  "رياضي": ["بيضاوي", "مستطيل"],
};
const REPO = "sisimsama-svg/Streamlit-application-setup";
const BRANCH = "main";
const GATE = "mo-admin-open";
const TOKEN_KEY = "mo-admin-github";
const DRAFT_KEY = "mo-admin-draft";
const FALLBACK_HASH = "b7066b76d48bd02e0cab7587f808837277c19ce9c90e50939baabdc2939aa6e1";

const login = document.getElementById("login");
const desk = document.getElementById("desk");
const editor = document.getElementById("editor");
const list = document.getElementById("list");
const category = document.getElementById("category");
category.innerHTML = SHAPES.map((item) => `<option value="${esc(item)}">${esc(item)}</option>`).join("");

let staticMode = false;
let staticProducts = [];

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
  return `${Number(value || 0).toLocaleString("en-EG")} ج.م`;
}

function uid() {
  if (crypto.randomUUID) return crypto.randomUUID().replace(/-/g, "").slice(0, 10);
  return Math.random().toString(16).slice(2, 12);
}

async function digest(value) {
  const bytes = new TextEncoder().encode(String(value || "").trim());
  const buf = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(buf)].map((part) => part.toString(16).padStart(2, "0")).join("");
}

async function expectedHash() {
  try {
    const response = await fetch(
      "https://raw.githubusercontent.com/sisimsama-svg/Streamlit-application-setup/main/data/admin.json",
      { cache: "no-store" },
    );
    if (!response.ok) return FALLBACK_HASH;
    const data = await response.json();
    return String(data.code_hash || "").trim() || FALLBACK_HASH;
  } catch {
    return FALLBACK_HASH;
  }
}

async function readJson(response) {
  const type = response.headers.get("content-type") || "";
  if (!type.includes("json")) return null;
  return await response.json().catch(() => ({}));
}

async function api(url, options) {
  const response = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await readJson(response);
  if (payload === null || !response.ok) {
    throw new Error((payload && payload.error) || "تعذر تنفيذ الطلب.");
  }
  return payload;
}

function showError(id, message) {
  const node = document.getElementById(id);
  node.textContent = message || "";
  node.hidden = !message;
}

function showNote(message) {
  const node = document.getElementById("save-note");
  node.textContent = message || "";
  node.hidden = !message;
}

function resetForm() {
  editor.reset();
  document.getElementById("product-id").value = "";
  document.getElementById("form-title").textContent = "نظارة جديدة";
  document.querySelector("[name=stock]").value = "8";
  showError("form-error", "");
}

function fill(product) {
  document.getElementById("product-id").value = product.id;
  document.getElementById("form-title").textContent = `تعديل: ${product.name}`;
  for (const key of ["brand", "name", "old_price", "price", "audience", "kind", "category", "badge", "stock"]) {
    const field = editor.elements[key];
    if (field) field.value = product[key] ?? "";
  }
  window.scrollTo(0, 0);
}

async function fileData() {
  const file = document.getElementById("image").files[0];
  if (!file) return "";
  return await new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(new Error("تعذر قراءة الصورة."));
    reader.readAsDataURL(file);
  });
}

function toView(item) {
  const asset = String(item.asset || item.image || "").split("/").pop();
  const image = item.preview || (asset ? `/glasses/${asset}` : "");
  return {
    id: item.id,
    name: item.name || "",
    brand: item.brand || "",
    price: Number(item.price || 0),
    old_price: Number(item.old_price || item.price || 0),
    audience: item.audience || "للجميع",
    kind: item.kind || "طبية",
    category: item.category || SHAPES[0],
    badge: item.badge || "",
    stock: Number(item.stock || 0),
    asset,
    image,
  };
}

function render(products) {
  list.innerHTML = products.map((item) => `
    <article class="item">
      <img src="${esc(item.image)}" alt="">
      <div>
        <h3>${esc(item.name)}</h3>
        <p>${esc(item.brand)} · ${esc(item.audience)} · ${esc(item.kind)}${item.badge === "bestseller" ? " · BESTSELLER" : ""}</p>
        <p><s>${esc(money(item.old_price))}</s> ${esc(money(item.price))}</p>
      </div>
      <div class="btns">
        <button type="button" data-edit="${esc(item.id)}">تعديل</button>
        <button type="button" class="ghost" data-delete="${esc(item.id)}">حذف</button>
      </div>
    </article>
  `).join("");
  list.querySelectorAll("[data-edit]").forEach((button) => {
    button.addEventListener("click", () => fill(products.find((item) => item.id === button.dataset.edit)));
  });
  list.querySelectorAll("[data-delete]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!confirm("حذف هذه النظارة من المتجر؟")) return;
      try {
        if (staticMode) await removeStatic(button.dataset.delete);
        else {
          await api("/api/admin/products/delete", {
            method: "POST",
            body: JSON.stringify({ id: button.dataset.delete }),
          });
        }
        await load();
      } catch (error) {
        if (error.needToken) document.getElementById("token").hidden = false;
        showError("form-error", error.message);
      }
    });
  });
}

function remember(products) {
  const clean = products.map((item) => {
    const copy = { ...item };
    delete copy.preview;
    return copy;
  });
  localStorage.setItem(DRAFT_KEY, JSON.stringify({ at: Date.now(), products: clean }));
}

function recall(live) {
  try {
    const saved = JSON.parse(localStorage.getItem(DRAFT_KEY) || "null");
    if (!saved || !Array.isArray(saved.products)) return live;
    if (Date.now() - Number(saved.at || 0) > 10 * 60 * 1000) return live;
    return saved.products;
  } catch {
    return live;
  }
}

async function load() {
  if (staticMode) {
    render(staticProducts.map(toView));
    return;
  }
  const data = await api("/api/admin/products");
  render(data.products || []);
}

async function openDesk() {
  login.hidden = true;
  desk.hidden = false;
  await load();
}

async function openStatic() {
  staticMode = true;
  const response = await fetch("/bootstrap.json", { cache: "no-store" });
  if (!response.ok) throw new Error("تعذر تحميل التشكيلة.");
  const data = await response.json();
  staticProducts = recall(data.products || []);
  sessionStorage.setItem(GATE, "1");
  login.hidden = true;
  desk.hidden = false;
  render(staticProducts.map(toView));
}

async function remoteLogin(password) {
  let response;
  try {
    response = await fetch("/api/admin/login", {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
  } catch {
    return "static";
  }
  const payload = await readJson(response);
  if (payload === null) return "static";
  if (response.ok) return "ok";
  if (response.status === 401) return "denied";
  throw new Error(payload.error || "تعذر تنفيذ الطلب.");
}

async function enter(password) {
  const remote = await remoteLogin(password);
  if (remote === "ok") {
    staticMode = false;
    sessionStorage.removeItem(GATE);
    await openDesk();
    return;
  }
  if (remote === "denied") throw new Error("كلمة السر غير صحيحة.");
  const hash = await digest(password);
  const expected = (await expectedHash()).toLowerCase();
  if (!expected || hash !== expected) throw new Error("كلمة السر غير صحيحة.");
  await openStatic();
}

function askToken(error) {
  if (error && error.needToken) document.getElementById("token").hidden = false;
}

function githubToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

async function gh(path, options = {}) {
  const key = githubToken();
  if (!key) {
    const error = new Error("الصقي مفتاح GitHub مرة واحدة، وبعدين اضغطي حفظ.");
    error.needToken = true;
    throw error;
  }
  let response;
  try {
    response = await fetch(`https://api.github.com${path}`, {
      method: options.method || "GET",
      headers: {
        Authorization: `Bearer ${key}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        ...(options.body ? { "Content-Type": "application/json" } : {}),
      },
      body: options.body,
    });
  } catch {
    throw new Error("تعذر الاتصال لحفظ التعديل.");
  }
  const payload = await response.json().catch(() => ({}));
  if (response.status === 401) {
    localStorage.removeItem(TOKEN_KEY);
    const error = new Error("مفتاح GitHub غير صحيح.");
    error.needToken = true;
    throw error;
  }
  if (!response.ok) throw new Error("تعذر حفظ التعديل على الموقع.");
  return payload;
}

function encodeBase64(bytes) {
  let binary = "";
  const size = 0x8000;
  for (let index = 0; index < bytes.length; index += size) {
    binary += String.fromCharCode(...bytes.subarray(index, index + size));
  }
  return btoa(binary);
}

function decodeBase64(text) {
  const binary = atob(String(text || "").replace(/\s/g, ""));
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
  return bytes;
}

async function readRepoFile(path) {
  const payload = await gh(`/repos/${REPO}/contents/${path}?ref=${BRANCH}`);
  return {
    sha: payload.sha,
    text: new TextDecoder().decode(decodeBase64(payload.content)),
  };
}

async function writeRepoBase64(path, base64, message, sha) {
  const body = {
    message,
    content: String(base64 || "").replace(/\s/g, ""),
    branch: BRANCH,
  };
  if (sha) body.sha = sha;
  return gh(`/repos/${REPO}/contents/${path}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

async function toPngBase64(dataUrl) {
  const image = new Image();
  await new Promise((resolve, reject) => {
    image.onload = resolve;
    image.onerror = () => reject(new Error("تعذر قراءة الصورة."));
    image.src = dataUrl;
  });
  const max = 1400;
  const scale = Math.min(1, max / Math.max(image.naturalWidth || 1, image.naturalHeight || 1));
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(1, Math.round(image.naturalWidth * scale));
  canvas.height = Math.max(1, Math.round(image.naturalHeight * scale));
  canvas.getContext("2d").drawImage(image, 0, 0, canvas.width, canvas.height);
  const png = canvas.toDataURL("image/png").split(",")[1];
  if (!png) throw new Error("تعذر قراءة الصورة.");
  return png;
}

function buildRecord(existing, data, asset) {
  const name = String(data.name || "").trim();
  const kind = String(data.kind || "").trim();
  const audience = String(data.audience || "").trim();
  let shape = String(data.category || "").trim();
  let badge = String(data.badge || "").trim();
  if (name.length < 2) throw new Error("اكتب اسم الموديل.");
  if (!KINDS.includes(kind)) throw new Error("اختر نظارة شمسية أو طبية.");
  if (!AUDIENCES.includes(audience)) throw new Error("اختر القسم: رجالي أو حريمي أو أطفال.");
  if (!SHAPES.includes(shape)) shape = SHAPES[0];
  if (!["", "bestseller", "sale"].includes(badge)) badge = "";
  const price = Number(data.price);
  const oldPrice = data.old_price === "" || data.old_price == null ? price : Number(data.old_price);
  const stock = data.stock === "" || data.stock == null ? 8 : Number(data.stock);
  if (![price, oldPrice, stock].every((value) => Number.isInteger(value))) {
    throw new Error("اكتب السعر بالأرقام.");
  }
  if (price < 0 || oldPrice < 0 || stock < 0 || stock > 999) {
    throw new Error("السعر أو الكمية غير صالحة.");
  }
  if (!asset) throw new Error("أضف صورة النظارة.");
  const record = { ...(existing || {}) };
  record.id = existing?.id || `frame-${uid()}`;
  record.name = name.slice(0, 80);
  record.brand = (String(data.brand || "").trim() || "نظارات مسلم").slice(0, 40);
  record.price = price;
  record.old_price = Math.max(oldPrice, price);
  record.kind = kind;
  record.audience = audience;
  record.category = shape;
  record.badge = badge;
  record.stock = stock;
  record.asset = asset;
  record.face_shapes = SHAPE_MAP[shape] || ["بيضاوي"];
  record.store_id = "moslem";
  if (record.rating == null) record.rating = 5;
  if (record.sold == null) record.sold = 0;
  if (!record.color) record.color = shape;
  if (!record.description) record.description = "";
  return record;
}

async function publishSave(data) {
  const existingId = String(data.id || "").trim();
  const file = await readRepoFile("data/catalog.json");
  let catalog;
  try {
    catalog = JSON.parse(file.text);
  } catch {
    throw new Error("تعذر قراءة تشكيلة المتجر.");
  }
  const products = Array.isArray(catalog.products) ? catalog.products : [];
  const existing = products.find((item) => item.id === existingId) || null;
  let asset = String((existing && existing.asset) || "").split("/").pop();
  buildRecord(existing, data, asset || (data.image ? "pending.png" : ""));
  if (data.image) {
    asset = `frame_${uid()}.png`;
    await writeRepoBase64(
      `assets/glasses/${asset}`,
      await toPngBase64(data.image),
      "Add a frame photo from the shop admin.",
    );
  }
  const record = buildRecord(existing, data, asset);
  const next = existing
    ? products.map((item) => (item.id === record.id ? record : item))
    : products.concat(record);
  const encoded = encodeBase64(new TextEncoder().encode(`${JSON.stringify({ version: catalog.version || 3, products: next }, null, 2)}\n`));
  await writeRepoBase64("data/catalog.json", encoded, "Update the shop frames from the admin page.", file.sha);
  return record;
}

async function publishDelete(id) {
  const file = await readRepoFile("data/catalog.json");
  let catalog;
  try {
    catalog = JSON.parse(file.text);
  } catch {
    throw new Error("تعذر قراءة تشكيلة المتجر.");
  }
  const products = Array.isArray(catalog.products) ? catalog.products : [];
  const next = products.filter((item) => item.id !== id);
  if (next.length === products.length) throw new Error("النظارة غير موجودة.");
  const encoded = encodeBase64(new TextEncoder().encode(`${JSON.stringify({ version: catalog.version || 3, products: next }, null, 2)}\n`));
  await writeRepoBase64("data/catalog.json", encoded, "Remove a frame from the shop.", file.sha);
}

async function removeStatic(id) {
  await publishDelete(id);
  staticProducts = staticProducts.filter((item) => item.id !== id);
  remember(staticProducts);
  showNote("تم الحذف. هيختفي من الموقع خلال دقيقة أو اتنين.");
}

login.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("login-error", "");
  const button = login.querySelector("button");
  button.disabled = true;
  try {
    await enter(document.getElementById("password").value);
  } catch (error) {
    showError("login-error", error.message);
  } finally {
    button.disabled = false;
  }
});

document.getElementById("logout").addEventListener("click", async () => {
  sessionStorage.removeItem(GATE);
  if (!staticMode) {
    try {
      await api("/api/admin/logout", { method: "POST", body: "{}" });
    } catch {
      /* الخروج المحلي يكفي */
    }
  }
  staticMode = false;
  desk.hidden = true;
  login.hidden = false;
});

document.getElementById("reset").addEventListener("click", () => {
  resetForm();
  showNote("");
});

document.getElementById("token").addEventListener("submit", (event) => {
  event.preventDefault();
  const value = document.getElementById("github-token").value.trim();
  if (!value) return;
  localStorage.setItem(TOKEN_KEY, value);
  document.getElementById("github-token").value = "";
  document.getElementById("token").hidden = true;
  showError("form-error", "");
  showNote("اتحفظ المفتاح. اضغطي حفظ تاني عشان التعديل ينزل على الموقع.");
});

editor.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("form-error", "");
  showNote("");
  const button = editor.querySelector("[type=submit]");
  const data = Object.fromEntries(new FormData(editor).entries());
  button.disabled = true;
  try {
    data.image = await fileData();
    if (staticMode) {
      const saved = await publishSave(data);
      const view = {
        ...saved,
        preview: data.image || "",
        image: `glasses/${saved.asset}`,
      };
      const index = staticProducts.findIndex((item) => item.id === saved.id);
      if (index >= 0) staticProducts[index] = view;
      else staticProducts.unshift(view);
      remember(staticProducts);
      showNote("تم الحفظ. هيظهر على الموقع خلال دقيقة أو اتنين.");
    } else {
      await api("/api/admin/products", { method: "POST", body: JSON.stringify(data) });
    }
    resetForm();
    await load();
  } catch (error) {
    askToken(error);
    showError("form-error", error.message);
  } finally {
    button.disabled = false;
  }
});

async function boot() {
  try {
    const response = await fetch("/api/admin/products", { credentials: "same-origin" });
    const payload = await readJson(response);
    if (payload && response.ok) {
      staticMode = false;
      await openDesk();
      return;
    }
  } catch {
    /* الموقع المنشور يفتح بكلمة السر من غير السيرفر */
  }
  if (sessionStorage.getItem(GATE) === "1") {
    try {
      await openStatic();
    } catch {
      sessionStorage.removeItem(GATE);
    }
  }
}

boot();
