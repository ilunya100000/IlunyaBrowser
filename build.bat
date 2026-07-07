@echo off
setlocal
cd /d "%~dp0"

call .venv\Scripts\activate.bat
if not exist "assets\icon.ico" python make_icon.py
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name IlunyaBrowser --icon assets\icon.ico --add-data "assets\icon.ico;assets" ilunya_browser.py
echo.
echo Build complete: dist\IlunyaBrowser.exe
