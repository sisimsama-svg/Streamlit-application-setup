@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
where py >nul 2>&1 && (set "PY=py -3") || (set "PY=python")
%PY% -c "import PIL" 2>nul || %PY% -m pip install Pillow
%PY% generate_assets.py
%PY% server.py
