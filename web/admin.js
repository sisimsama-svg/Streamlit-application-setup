const SHAPES = ["كلاسيك", "دائري", "أفياتور", "كات آي", "رياضي", "مربع", "بيضاوي", "شفاف"];
const login = document.getElementById("login");
const desk = document.getElementById("desk");
const editor = document.getElementById("editor");
const list = document.getElementById("list");
const category = document.getElementById("category");
category.innerHTML = SHAPES.map((item) => `<option value="${item}">${item}</option>`).join("");

function money(value) {
  return `${Number(value || 0).toLocaleString("en-EG")} ج.م`;
}

async function api(url, options) {
  const response = await fetch(url, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || "تعذر تنفيذ الطلب.");
  return payload;
}

function showError(id, message) {
  const node = document.getElementById(id);
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

function render(products) {
  list.innerHTML = products.map((item) => `
    <article class="item">
      <img src="${item.image}" alt="">
      <div>
        <h3>${item.name}</h3>
        <p>${item.brand} · ${item.audience} · ${item.kind}${item.badge === "bestseller" ? " · BESTSELLER" : ""}</p>
        <p><s>${money(item.old_price)}</s> ${money(item.price)}</p>
      </div>
      <div class="btns">
        <button type="button" data-edit="${item.id}">تعديل</button>
        <button type="button" class="ghost" data-delete="${item.id}">حذف</button>
      </div>
    </article>
  `).join("");
  list.querySelectorAll("[data-edit]").forEach((button) => {
    button.addEventListener("click", () => fill(products.find((item) => item.id === button.dataset.edit)));
  });
  list.querySelectorAll("[data-delete]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!confirm("حذف هذه النظارة من المتجر؟")) return;
      await api("/api/admin/products/delete", {
        method: "POST",
        body: JSON.stringify({ id: button.dataset.delete }),
      });
      await load();
    });
  });
}

async function load() {
  const data = await api("/api/admin/products");
  render(data.products || []);
}

async function openDesk() {
  login.hidden = true;
  desk.hidden = false;
  await load();
}

login.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("login-error", "");
  try {
    await api("/api/admin/login", {
      method: "POST",
      body: JSON.stringify({ password: document.getElementById("password").value }),
    });
    await openDesk();
  } catch (error) {
    showError("login-error", error.message);
  }
});

document.getElementById("logout").addEventListener("click", async () => {
  await api("/api/admin/logout", { method: "POST", body: "{}" });
  desk.hidden = true;
  login.hidden = false;
});

document.getElementById("reset").addEventListener("click", resetForm);

editor.addEventListener("submit", async (event) => {
  event.preventDefault();
  showError("form-error", "");
  const data = Object.fromEntries(new FormData(editor).entries());
  try {
    data.image = await fileData();
    await api("/api/admin/products", { method: "POST", body: JSON.stringify(data) });
    resetForm();
    await load();
  } catch (error) {
    showError("form-error", error.message);
  }
});

api("/api/admin/products").then(openDesk).catch(() => {});
