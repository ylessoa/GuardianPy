@echo off
REM setup_guardianpy.bat
REM Script de instalación automatizada para GuardianPy en Windows

echo ================================
echo Configurando entorno GuardianPy
echo ================================

REM 1. Ir al directorio del proyecto (ajusta la ruta si es necesario)
cd %USERPROFILE%\GuardianPy

REM 2. Crear entorno virtual si no existe
if not exist ".venv" (
    python -m venv .venv
)

REM 3. Activar entorno virtual
call .venv\Scripts\activate.bat

REM 4. Actualizar pip, setuptools y wheel
python -m pip install --upgrade pip setuptools wheel

REM 5. Instalar dependencias recomendadas para Python 3.13
pip install psutil==6.1.0 ^
            requests==2.32.3 ^
            yara-python==4.5.4 ^
            pytest==9.1.1 ^
            colorama==0.4.6 ^
            cryptography==43.0.1 ^
            pyinstaller==6.10.0 ^
            watchdog==4.0.1

REM 6. Mostrar lista de paquetes instalados
pip list

echo ================================
echo Instalación completada
echo ================================
pause
