@echo off
cd /d "%~dp0"
py -3 -m pip install pyinstaller arabic-reshaper python-bidi
py -3 build_exe.py
