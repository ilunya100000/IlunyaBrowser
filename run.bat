@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 exit /b 1
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

if not exist "assets\icon.ico" (
    python make_icon.py
)

if exist "dist\IlunyaBrowser.exe" (
    start "" "dist\IlunyaBrowser.exe"
    exit /b 0
)

python ilunya_browser.py
