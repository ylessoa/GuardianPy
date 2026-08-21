GuardianPy Community
![GuardianPy CI](https://github.com/ylessoa/GuardianPy/actions/workflows/ci.yml/badge.svg)

GuardianPy Community es una sguardianpy.guardianpy.uite defensiva antivirus / antimalware / antitroyanos en Python, diseñada con una experiencia visual inspirada en Avast, Bitdefender y Norton, pero con una arqguardianpy.guardianpy.uitectura abierta y lista para GitHub.

GuardianPy Community no incluye capacidades ofensivas. Su objetivo es detectar, contener y reducir superficie de ataque.

Novedades versión 0.2 profesional
Panel gráfico rediseñado tipo sguardianpy.guardianpy.uite comercial.
Branding propio y logo SVG.
Escaneo por firmas SHA-256 y heurísticas locales.
Cuarentena / encapsulado de archivos sospechosos.
Guardián residente en segundo plano mediante ciclo de protección.
Registro de eventos en ~/.guardianpy/events.jsonl.
Actualización de firmas por HTTPS.
Auditoría de procesos por memoria, CPU y conexiones.
Auditoría de puertos abiertos riesgosos.
Recomendaciones de hardening.
Scripts para generar .exe Windows con PyInstaller.
Script de instalador Windows con Inno Setup.
Kit Community listo para GitHub: MIT License, CI, SECURITY, CONTRIBUTING y documentación.
Captura conceptual
La guardianpy.guardianpy.ui incluye:

barra lateral estilo centro de seguridad,
tarjetas de estado,
contador de amenazas,
contador de procesos sospechosos,
contador de puertos riesgosos,
tabla de resultados,
botón de actualización de firmas,
acción de encapsulado.
Instalación para desarrollo
bash 
cd GuardianPy
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1
pip install -r reqguardianpy.guardianpy.uirements.txt
pip install -e .
Ejecutar panel gráfico
bash 
GuardianPy-gguardianpy.guardianpy.ui
Alternativas:

bash 
python -m GuardianPy.app
python run_gguardianpy.guardianpy.ui.py
Uso CLI
bash 
# Escanear una carpeta
GuardianPy scan ~/Downloads

# Escanear y encapsular automáticamente detecciones
GuardianPy scan ~/Downloads --quarantine

# Revisar procesos por memoria/CPU/conexiones
GuardianPy monitor

# Auditar puertos peligrosos abiertos
GuardianPy ports

# Recomendaciones de hardening
GuardianPy harden

# Actualizar firmas desde GitHub/raw HTTPS
GuardianPy update

# Ejecutar un ciclo de protección residente
GuardianPy resident --once

# Ejecutar guardián residente continuamente
GuardianPy resident

# Ver eventos recientes
GuardianPy events

# Auditoría completa
GuardianPy full ~/Downloads
Windows: crear .exe
En Windows:

powershell 
cd guardianpy
packaging\windows\bguardianpy.guardianpy.uild_windows.ps1
Salida:

text 
dist\GuardianPyCommunity.exe
Windows: crear instalador .exe
Instala Inno Setup.
Genera primero el EXE portable.
Compila:
text 
packaging\windows\guardianpy_installer.iss
Salida:

text 
dist-installer\GuardianPyCommunitySetup.exe
Más detalles en docs/WINDOWS_Bguardianpy.guardianpy.uiLD.md.

Servicio residente Windows
GuardianPy Community puede instalarse como tarea programada al inicio de sesión:

powershell 
.\install_windows.ps1
packaging\windows\install_resident_task.ps1
La tarea se llama:

text 
GuardianPy Resident Guard
Actualización de firmas
El actualizador descarga un JSON de firmas desde HTTPS. Por defecto apunta a:

text 
https://raw.githubusercontent.com/ylessoa/GuardianPy/main/signatures/signatures.json
Cambia la URL con:

bash 
guardianpy update --url https://tu-servidor/signatures.json
Arqguardianpy.guardianpy.uitectura
text 
GuardianPy/
  GuardianPy/guardianpy.guardianpy.core/scanner.py          # Motor de escaneo
  GuardianPy/guardianpy.guardianpy.core/signatures.py       # Carga de firmas
  GuardianPy/guardianpy.guardianpy.core/updater.py          # Actualización de firmas
  GuardianPy/guardianpy.guardianpy.core/quarantine.py       # Cuarentena
  GuardianPy/guardianpy.guardianpy.core/process_monitor.py  # Procesos: memoria/CPU/red
  GuardianPy/guardianpy.guardianpy.core/ports.py            # Puertos riesgosos
  GuardianPy/guardianpy.guardianpy.core/hardening.py        # Hardening
  GuardianPy/guardianpy.guardianpy.core/events.py           # Eventos del residente
  GuardianPy/service/resident.py      # Guardián residente
  GuardianPy/guardianpy.guardianpy.ui/tk_app.py             # Panel profesional
  packaging/windows/                 # EXE e instalador
Publicar en GitHub
bash 
git init
git add .
git commit -m "GuardianPy Community 0.2"
git branch -M main
git remote add origin https://github.com/ylessoa/GuardianPy.git
git push -u origin main
Pruebas
bash 
pytest -q
Roadmap
Consulta docs/ROADMAP.md.

Seguridad y ética
GuardianPy está diseñado solo para defensa. No se aceptan módulos de explotación, evasión, persistencia ofensiva, robo de credenciales, payloads o loaders.

