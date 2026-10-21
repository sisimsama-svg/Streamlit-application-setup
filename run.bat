@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"

py -3 -m pip install --upgrade pip
py -3 -m pip install -r requirements.txt
py -3 generate_assets.py
py -3 -m streamlit run app.py --server.headless false
