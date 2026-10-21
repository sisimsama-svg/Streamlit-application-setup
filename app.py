"""خادم نظارات مسلم: واجهة المتجر مع manifest وعامل الخدمة."""

from __future__ import annotations

import streamlit as st
from starlette.middleware import Middleware

from pwa import PWAMiddleware, routes

app = st.App(
    "shop.py",
    routes=routes(),
    middleware=[Middleware(PWAMiddleware)],
)

if __name__ == "__main__":
    app.run()
