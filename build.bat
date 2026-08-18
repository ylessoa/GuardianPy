@echo off
echo ===================================================
echo Iniciando compilacion de GuardianPy Community...
echo ===================================================

echo [1/4] Verificando dependencias...
pip install pyinstaller pefile > nul 2>&1

echo [2/4] Limpiando compilaciones anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "GuardianPy.spec" del /q "GuardianPy.spec"

echo [3/4] Compilando el ejecutable...
pyinstaller --noconfirm --onefile --windowed --uac-admin ^
    --add-data "signatures;signatures" ^
    --add-data "asset;asset" ^
    --hidden-import "watchdog.observers" ^
    --hidden-import "watchdog.events" ^
    --hidden-import "pystray._win32" ^
    --hidden-import "PIL._tkinter_finder" ^
    --hidden-import "pefile" ^
    --name "GuardianPy" ^
    app.py

echo [4/4] Compilacion finalizada!
echo ===================================================
echo El ejecutable se encuentra en la carpeta: dist\GuardianPy.exe
echo ===================================================
pause
