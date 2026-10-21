(function () {
  if (window.__moslemPwa) {
    return;
  }
  window.__moslemPwa = true;

  var THEME = "#059669";

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/service-worker.js", { scope: "/" }).catch(function () {});
    });
  }

  function standalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.navigator.standalone === true
    );
  }

  if (standalone()) {
    return;
  }

  var style = document.createElement("style");
  style.textContent =
    "#moslem-install,#moslem-ios{position:fixed;z-index:1000000;left:16px;right:16px;bottom:16px;margin:0 auto;max-width:420px;" +
    "background:" + THEME + ";color:#fff;border:0;border-radius:16px;padding:12px 16px;font:700 15px Cairo,Tahoma,sans-serif;" +
    "box-shadow:0 10px 24px rgba(5,150,105,.28);cursor:pointer;text-align:center}" +
    "#moslem-ios{cursor:default;font-weight:600}" +
    "#moslem-ios button{margin-right:8px;background:transparent;color:#fff;border:0;font:inherit;cursor:pointer}";
  document.head.appendChild(style);

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    if (document.getElementById("moslem-install")) {
      return;
    }
    var button = document.createElement("button");
    button.id = "moslem-install";
    button.type = "button";
    button.textContent = "أضف إلى الشاشة الرئيسية";
    button.setAttribute("aria-label", "Add to Home Screen");
    button.addEventListener("click", function () {
      event.prompt();
      button.disabled = true;
      event.userChoice.finally(function () {
        button.remove();
      });
    });
    document.body.appendChild(button);
  });

  var ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
  if (!ios || localStorage.getItem("moslem-ios-hint") === "1") {
    return;
  }
  var note = document.createElement("div");
  note.id = "moslem-ios";
  note.textContent = "على آيفون: مشاركة ← إضافة إلى الشاشة الرئيسية";
  var close = document.createElement("button");
  close.type = "button";
  close.textContent = "×";
  close.setAttribute("aria-label", "إغلاق");
  close.addEventListener("click", function () {
    localStorage.setItem("moslem-ios-hint", "1");
    note.remove();
  });
  note.prepend(close);
  document.body.appendChild(note);
})();
