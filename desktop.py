"""تشغيل نظارات مسلم بنقرة واحدة: خادم محلي ثم فتح الواجهة."""

from __future__ import annotations

import multiprocessing
import os
import socket
import sys
import threading
import time
import traceback
import urllib.request
import webbrowser


def _setup_log():
    from paths import log_path

    path = log_path()
    try:
        handle = path.open("a", encoding="utf-8")
    except OSError:
        return None
    sys.stdout = handle
    sys.stderr = handle

    def hook(etype, value, tb):
        traceback.print_exception(etype, value, tb, file=handle)
        handle.flush()

    sys.excepthook = hook
    return handle


def _port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        try:
            sock.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def _pick_port(start: int = 8501) -> int:
    for port in range(start, start + 50):
        if _port_free(port):
            return port
    raise RuntimeError("No free local port between 8501 and 8550")


def _wait_and_open(port: int) -> None:
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 180
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as resp:
                if getattr(resp, "status", 200) < 500:
                    print(f"READY {url}", flush=True)
                    if os.environ.get("MOSLEM_NO_BROWSER") != "1":
                        webbrowser.open(url)
                    return
        except Exception:
            time.sleep(0.5)
    print(f"TIMEOUT {url}", flush=True)


def main() -> None:
    multiprocessing.freeze_support()
    _setup_log()
    from paths import bundle_root, writable_root

    bundle = bundle_root()
    script = bundle / "app.py"
    runtime = writable_root() / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime)
    if str(bundle) not in sys.path:
        sys.path.insert(0, str(bundle))

    port = _pick_port(8501)
    print(f"PORT {port}", flush=True)
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "127.0.0.1"
    os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
    os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "true"
    os.environ["STREAMLIT_SERVER_SHOW_EMAIL_PROMPT"] = "false"

    threading.Thread(target=_wait_and_open, args=(port,), daemon=True).start()

    from streamlit import config as _config
    from streamlit.runtime.credentials import check_credentials
    from streamlit.web import bootstrap

    flag_options = {
        "global_developmentMode": False,
        "server_headless": True,
        "server_port": port,
        "server_address": "127.0.0.1",
        "server_fileWatcherType": "none",
        "server_runOnSave": False,
        "server_enableCORS": False,
        "server_enableXsrfProtection": True,
        "server_showEmailPrompt": False,
        "browser_gatherUsageStats": False,
    }
    _config._main_script_path = str(script)
    bootstrap.load_config_options(flag_options=flag_options)
    check_credentials()
    bootstrap.run(str(script), False, [], flag_options)


if __name__ == "__main__":
    main()
