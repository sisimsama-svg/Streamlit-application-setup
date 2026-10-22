const MODEL =
  "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task";
const WASM = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.17/wasm";
const VISION = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.17";

const LM = {
  forehead: 10,
  chin: 152,
  cheekL: 234,
  cheekR: 454,
  templeL: 54,
  templeR: 284,
  jawL: 172,
  jawR: 397,
  jawCL: 132,
  jawCR: 361,
  eyeR: 33,
  eyeL: 263,
  nose: 1,
};

const GUIDES = {
  round: {
    label: "دائري",
    advice: "وجهك متقارب الطول والعرض. الإطارات الزاوية والمربعة والكات آي تضيف تحديداً أوضح.",
  },
  square: {
    label: "مربع",
    advice: "زوايا الفك واضحة. الإطارات الدائرية والأفياتور تنعّم الملامح وتوازن الوجه.",
  },
  oval: {
    label: "بيضاوي",
    advice: "نسب الوجه متوازنة. أغلب الإطارات تليق إذا كان عرضها قريباً من عرض الوجه.",
  },
  rectangle: {
    label: "مستطيل",
    advice: "الوجه أطول من عرضه. الإطارات العريضة والدائرية والأفياتور تكسر الطول.",
  },
  heart: {
    label: "قلب",
    advice: "الجبهة أعرض من الذقن. الإطارات الخفيفة والدائرية توازن الوجه دون ثقل من الأعلى.",
  },
};

let landmarkerPromise = null;

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));
}

function dist(a, b) {
  return Math.hypot(a[0] - b[0], a[1] - b[1]);
}

function corner(a, b, c) {
  const ba = [a[0] - b[0], a[1] - b[1]];
  const bc = [c[0] - b[0], c[1] - b[1]];
  const denom = Math.hypot(ba[0], ba[1]) * Math.hypot(bc[0], bc[1]);
  if (denom < 1e-6) return 180;
  const cos = (ba[0] * bc[0] + ba[1] * bc[1]) / denom;
  return (Math.acos(Math.min(1, Math.max(-1, cos))) * 180) / Math.PI;
}

function classify(lengthRatio, templeRatio, jawRatio, jawAngle) {
  const taper = templeRatio - jawRatio;
  if (taper >= 0.12 && jawRatio < 0.8) return "heart";
  if (lengthRatio >= 1.4) return "rectangle";
  if (lengthRatio < 1.34 && jawRatio >= 0.86 && jawAngle <= 150) return "square";
  if (lengthRatio < 1.2 && jawRatio >= 0.8 && jawAngle >= 130) return "round";
  return "oval";
}

function point(landmarks, index, width, height) {
  const mark = landmarks[index];
  if (!mark) return null;
  return [mark.x * width, mark.y * height];
}

function shapeFrom(landmarks, width, height) {
  if (!landmarks || landmarks.length <= LM.cheekR) return null;
  const xy = (index) => point(landmarks, index, width, height);
  const cheekL = xy(LM.cheekL);
  const cheekR = xy(LM.cheekR);
  if (!cheekL || !cheekR) return null;
  const cheek = dist(cheekL, cheekR);
  if (cheek < 8) return null;
  const lengthRatio = dist(xy(LM.forehead), xy(LM.chin)) / cheek;
  const templeRatio = dist(xy(LM.templeL), xy(LM.templeR)) / cheek;
  const jawRatio = dist(xy(LM.jawL), xy(LM.jawR)) / cheek;
  const jawAngle = (corner(cheekL, xy(LM.jawCL), xy(LM.jawL)) + corner(cheekR, xy(LM.jawCR), xy(LM.jawR))) / 2;
  return classify(lengthRatio, templeRatio, jawRatio, jawAngle);
}

async function createLandmarker() {
  const vision = await import(VISION);
  const fileset = await vision.FilesetResolver.forVisionTasks(WASM);
  const options = {
    numFaces: 1,
    runningMode: "VIDEO",
    outputFaceBlendshapes: false,
  };
  try {
    return await vision.FaceLandmarker.createFromOptions(fileset, {
      ...options,
      baseOptions: { modelAssetPath: MODEL, delegate: "GPU" },
    });
  } catch {
    return vision.FaceLandmarker.createFromOptions(fileset, {
      ...options,
      baseOptions: { modelAssetPath: MODEL, delegate: "CPU" },
    });
  }
}

function landmarker() {
  if (!landmarkerPromise) {
    landmarkerPromise = createLandmarker().catch((error) => {
      landmarkerPromise = null;
      throw error;
    });
  }
  return landmarkerPromise;
}

const imageCache = new Map();

function loadImage(src) {
  if (imageCache.has(src)) return imageCache.get(src);
  const pending = new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error("image"));
    image.src = src;
  });
  imageCache.set(src, pending);
  return pending;
}

export function mountTryOn(root, options) {
  const products = options.products.filter((item) => item.stock > 0);
  let currentId = options.initialId && products.some((item) => item.id === options.initialId)
    ? options.initialId
    : (products[0] ? products[0].id : "");
  let stream = null;
  let raf = 0;
  let stopped = false;
  let tracker = null;
  let facing = "user";
  let smooth = null;
  let missed = 0;
  let pendingKey = "";
  let pendingCount = 0;
  let stableKey = "";
  let glasses = null;
  let lastTs = 0;
  const state = { scale: 108, dy: 0 };

  root.innerHTML = `
    <section class="wrap try-page">
      <p class="kicker">LIVE TRY-ON</p>
      <div class="try-layout">
        <div>
          <div class="stage" id="stage">
            <div class="stage-placeholder" id="stage-empty">
              <div>
                <h2>انظر إلى الكاميرا</h2>
                <p>التتبّع يتم داخل المتصفح. صورة وجهك لا تُرسل إلى الخادم ولا تُحفظ.</p>
                <button type="button" class="btn light" id="start-cam">تشغيل الكاميرا</button>
              </div>
            </div>
            <canvas id="stage-canvas" hidden></canvas>
            <p class="hint" id="turn-hint" hidden>انظر مباشرة إلى الكاميرا حتى يثبت الإطار</p>
            <div class="stage-bar" id="stage-bar" hidden>
              <button type="button" id="shot">التقاط</button>
              <button type="button" id="flip">تبديل الكاميرا</button>
              <button type="button" id="stop-cam">إيقاف</button>
            </div>
          </div>
          <div class="film" id="film"></div>
        </div>
        <aside class="try-panel">
          <p class="kicker" id="try-brand"></p>
          <h1 id="try-name"></h1>
          <div class="price-row" id="try-price"></div>
          <p id="try-desc"></p>
          <label class="slider">حجم الإطار
            <input id="scale" type="range" min="80" max="150" value="108">
          </label>
          <label class="slider">ارتفاع الإطار
            <input id="dy" type="range" min="-80" max="80" value="0">
          </label>
          <label id="lens-wrap">العدسة
            <select id="lens-pick"></select>
          </label>
          <button type="button" class="btn block" id="try-add">أضف إلى السلة</button>
          <a class="btn ghost block" id="try-product" href="#/shop">صفحة الإطار</a>
          <div class="advice" id="advice">حرّك وجهك أمام الكاميرا لنقترح الإطارات الأقرب لشكل الوجه.</div>
          <div id="shot-box"></div>
        </aside>
      </div>
    </section>
  `;

  const stage = root.querySelector("#stage");
  const empty = root.querySelector("#stage-empty");
  const canvas = root.querySelector("#stage-canvas");
  const ctx = canvas.getContext("2d");
  const video = document.createElement("video");
  video.playsInline = true;
  video.muted = true;
  video.autoplay = true;
  video.setAttribute("playsinline", "");
  video.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;pointer-events:none";
  stage.appendChild(video);
  const film = root.querySelector("#film");
  const advice = root.querySelector("#advice");
  const turnHint = root.querySelector("#turn-hint");

  function current() {
    return products.find((item) => item.id === currentId) || products[0] || null;
  }

  function paintPanel() {
    const product = current();
    if (!product) return;
    root.querySelector("#try-brand").textContent = product.brand;
    root.querySelector("#try-name").textContent = product.name;
    const discount = product.old_price > product.price;
    root.querySelector("#try-price").innerHTML = `${options.money(product.price)}${discount ? `<s>${options.money(product.old_price)}</s>` : ""}`;
    root.querySelector("#try-desc").textContent = product.description;
    root.querySelector("#try-product").href = `#/product/${encodeURIComponent(product.id)}`;
    const lensWrap = root.querySelector("#lens-wrap");
    const select = root.querySelector("#lens-pick");
    const medical = product.kind === "طبية";
    lensWrap.hidden = !medical;
    if (medical) {
      select.innerHTML = options.lenses
        .filter((item) => item.id !== "none")
        .map((item) => `<option value="${esc(item.id)}">${esc(item.label)}${item.price ? ` · +${options.money(item.price)}` : ""}</option>`)
        .join("");
    }
    film.querySelectorAll("button").forEach((button) => {
      button.classList.toggle("is-on", button.dataset.id === product.id);
    });
    loadImage(product.image).then((image) => {
      if (current()?.id === product.id) glasses = image;
    }).catch(() => {
      glasses = null;
    });
  }

  film.innerHTML = products.map((product) => `
    <button type="button" data-id="${esc(product.id)}" class="${product.id === currentId ? "is-on" : ""}">
      <img src="${esc(product.image)}" alt="">
      <small>${esc(product.name)}</small>
    </button>
  `).join("");
  film.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-id]");
    if (!button) return;
    const next = `#/tryon/${encodeURIComponent(button.dataset.id)}`;
    if (location.hash === next) select(button.dataset.id);
    else location.hash = next;
  });

  root.querySelector("#scale").addEventListener("input", (event) => {
    state.scale = Number(event.target.value);
  });
  root.querySelector("#dy").addEventListener("input", (event) => {
    state.dy = Number(event.target.value);
  });
  root.querySelector("#try-add").addEventListener("click", () => {
    const product = current();
    if (!product) return;
    const lens = product.kind === "طبية" ? root.querySelector("#lens-pick").value : "none";
    options.onAdd(product, lens);
  });
  root.querySelector("#start-cam").addEventListener("click", () => { start().catch(showCameraError); });
  root.querySelector("#stop-cam").addEventListener("click", stopCamera);
  root.querySelector("#flip").addEventListener("click", () => {
    facing = facing === "user" ? "environment" : "user";
    start().catch(showCameraError);
  });
  root.querySelector("#shot").addEventListener("click", capture);

  function showCameraError(error) {
    const name = error && error.name;
    let message = "تعذر فتح الكاميرا.";
    if (name === "NotAllowedError" || name === "SecurityError") {
      message = "لم يُسمح بالكاميرا. اسمح بها من أيقونة القفل بجانب العنوان ثم أعد المحاولة.";
    } else if (name === "NotFoundError" || name === "OverconstrainedError") {
      message = "لا توجد كاميرا متاحة على هذا الجهاز.";
    } else if (!navigator.mediaDevices) {
      message = "المتصفح لا يتيح الكاميرا من هذا العنوان. افتح المتجر من كروم أو إيدج.";
    }
    empty.hidden = false;
    empty.innerHTML = `<div><h2>الكاميرا غير متاحة</h2><p>${esc(message)}</p><button type="button" class="btn light" id="start-cam">إعادة المحاولة</button></div>`;
    empty.querySelector("#start-cam").addEventListener("click", () => { start().catch(showCameraError); });
    canvas.hidden = true;
    root.querySelector("#stage-bar").hidden = true;
  }

  function stopCamera() {
    cancelAnimationFrame(raf);
    if (stream) stream.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
    canvas.hidden = true;
    root.querySelector("#stage-bar").hidden = true;
    turnHint.hidden = true;
    empty.hidden = false;
    empty.innerHTML = `<div><h2>انظر إلى الكاميرا</h2><p>التتبّع يتم داخل المتصفح. صورة وجهك لا تُرسل إلى الخادم ولا تُحفظ.</p><button type="button" class="btn light" id="start-cam">تشغيل الكاميرا</button></div>`;
    empty.querySelector("#start-cam").addEventListener("click", () => { start().catch(showCameraError); });
  }

  async function start() {
    if (!navigator.mediaDevices?.getUserMedia) {
      throw Object.assign(new Error("no camera"), { name: "SecurityError" });
    }
    if (stream) stream.getTracks().forEach((track) => track.stop());
    empty.hidden = false;
    empty.innerHTML = `<div><h2>جاري فتح الكاميرا</h2><p>ثم يُجهَّز تتبّع الوجه. قد يأخذ ذلك بضع ثوانٍ في أول مرة.</p></div>`;
    stream = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: { facingMode: facing, width: { ideal: 1280 }, height: { ideal: 720 } },
    });
    if (stopped) {
      stream.getTracks().forEach((track) => track.stop());
      return;
    }
    video.srcObject = stream;
    await video.play();
    canvas.hidden = false;
    empty.hidden = true;
    root.querySelector("#stage-bar").hidden = false;
    if (!tracker) {
      try {
        tracker = await landmarker();
      } catch {
        empty.hidden = false;
        canvas.hidden = true;
        empty.innerHTML = `<div><h2>تعذر تتبّع الوجه</h2><p>تحقق من الاتصال بالإنترنت حتى يُحمَّل نموذج التتبّع، ثم أعد المحاولة. الكاميرا نفسها تبقى على جهازك.</p><button type="button" class="btn light" id="start-cam">إعادة المحاولة</button></div>`;
        empty.querySelector("#start-cam").addEventListener("click", () => { start().catch(showCameraError); });
        return;
      }
    }
    if (stopped) return;
    cancelAnimationFrame(raf);
    const loop = () => {
      if (stopped) return;
      draw();
      raf = requestAnimationFrame(loop);
    };
    loop();
  }

  function draw() {
    const width = video.videoWidth;
    const height = video.videoHeight;
    if (!width || !height) return;
    if (canvas.width !== width) canvas.width = width;
    if (canvas.height !== height) canvas.height = height;
    const mirror = facing === "user";
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, width, height);
    ctx.save();
    if (mirror) {
      ctx.translate(width, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, width, height);
    if (tracker && video.readyState >= 2) {
      try {
        let ts = performance.now();
        if (ts <= lastTs) ts = lastTs + 1;
        lastTs = ts;
        const result = tracker.detectForVideo(video, ts);
        const marks = result?.faceLandmarks?.[0];
        if (marks) {
          missed = 0;
          const right = point(marks, LM.eyeR, width, height);
          const left = point(marks, LM.eyeL, width, height);
          if (right && left) {
            if (!smooth) smooth = { x1: right[0], y1: right[1], x2: left[0], y2: left[1] };
            else {
              const blend = 0.42;
              smooth.x1 += (right[0] - smooth.x1) * blend;
              smooth.y1 += (right[1] - smooth.y1) * blend;
              smooth.x2 += (left[0] - smooth.x2) * blend;
              smooth.y2 += (left[1] - smooth.y2) * blend;
            }
            drawGlasses(smooth);
            const eyeDist = dist(right, left);
            const nose = point(marks, LM.nose, width, height);
            const mid = (right[0] + left[0]) / 2;
            const turned = nose ? Math.abs(nose[0] - mid) / Math.max(eyeDist, 1) > 0.2 : false;
            turnHint.hidden = !turned;
            const key = shapeFrom(marks, width, height);
            if (key) rememberShape(key);
          }
        } else {
          missed += 1;
          if (missed > 12) {
            smooth = null;
            turnHint.hidden = true;
          }
        }
      } catch {
        turnHint.hidden = true;
      }
    }
    ctx.restore();
  }

  function drawGlasses(eyes) {
    if (!glasses) return;
    const eyeDist = Math.hypot(eyes.x2 - eyes.x1, eyes.y2 - eyes.y1);
    if (eyeDist < 12) return;
    const span = 0.74;
    const drawW = (eyeDist / span) * (state.scale / 100);
    const drawH = drawW * (glasses.height / glasses.width);
    const angle = Math.atan2(eyes.y2 - eyes.y1, eyes.x2 - eyes.x1);
    ctx.save();
    ctx.translate((eyes.x1 + eyes.x2) / 2, (eyes.y1 + eyes.y2) / 2 + state.dy);
    ctx.rotate(angle);
    ctx.drawImage(glasses, -drawW / 2, -drawH * 0.48, drawW, drawH);
    ctx.restore();
  }

  function rememberShape(key) {
    if (key === pendingKey) pendingCount += 1;
    else {
      pendingKey = key;
      pendingCount = 1;
    }
    if (pendingCount >= 8 && stableKey !== key) {
      stableKey = key;
      const guide = GUIDES[key];
      const matches = options.products.filter((item) => (item.face_shapes || []).includes(guide.label) && item.stock > 0).slice(0, 3);
      const names = matches.map((item) => item.name).join("، ");
      advice.innerHTML = `<strong>شكل الوجه: ${esc(guide.label)}</strong><br>${esc(guide.advice)}${names ? `<br><br><b>من التشكيلة:</b> ${esc(names)}` : ""}`;
    }
  }

  function capture() {
    if (!canvas.width) return;
    canvas.toBlob((blob) => {
      if (!blob) return;
      const url = URL.createObjectURL(blob);
      const box = root.querySelector("#shot-box");
      box.innerHTML = `<img class="shot" alt="لقطة التجربة" src="${url}"><a class="btn ghost block" style="margin-top:8px" href="${url}" download="moslem-tryon.jpg">حفظ الصورة</a>`;
    }, "image/jpeg", 0.92);
  }

  function select(id) {
    if (!products.some((item) => item.id === id)) return;
    currentId = id;
    paintPanel();
    document.title = `${current().name} — تجربة حية | مسلم`;
  }

  paintPanel();
  document.title = `${current()?.name || "التجربة الحية"} — تجربة حية | مسلم`;

  return {
    select,
    destroy() {
      stopped = true;
      cancelAnimationFrame(raf);
      if (stream) stream.getTracks().forEach((track) => track.stop());
      stream = null;
      stage.replaceChildren();
    },
  };
}
