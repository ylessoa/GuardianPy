
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/guardianx_mono_white.png">
    <img src="assets/guardianx_mono_black_solid.png" width="200" alt="GuardianX">
  </picture>
</p>

# GuardianX CommunityGuardianX Community
GuardianX Community es una suite defensiva antivirus / antimalware / antitroyanos en Python, diseñada con una experiencia visual inspirada en Avast, Bitdefender y Norton, pero con una arquitectura abierta y lista para GitHub.

GuardianX Community no incluye capacidades ofensivas. Su objetivo es detectar, contener y reducir superficie de ataque.

Novedades versión 0.2 profesional
Panel gráfico rediseñado tipo suite comercial.
Branding propio y logo SVG.
Escaneo por firmas SHA-256 y heurísticas locales.
Cuarentena / encapsulado de archivos sospechosos.
Guardián residente en segundo plano mediante ciclo de protección.
Registro de eventos en ~/.guardianx/events.jsonl.
Actualización de firmas por HTTPS.
Auditoría de procesos por memoria, CPU y conexiones.
Auditoría de puertos abiertos riesgosos.
Recomendaciones de hardening.
Scripts para generar .exe Windows con PyInstaller.
Script de instalador Windows con Inno Setup.
Kit Community listo para GitHub: MIT License, CI, SECURITY, CONTRIBUTING y documentación.
Captura conceptual
La UI incluye:

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
cd guardianx
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pip install -e .
Ejecutar panel gráfico
bash 
guardianx-gui
Alternativas:

bash 
python -m guardianx.app
python run_gui.py
Uso CLI
bash 
# Escanear una carpeta
guardianx scan ~/Downloads

# Escanear y encapsular automáticamente detecciones
guardianx scan ~/Downloads --quarantine

# Revisar procesos por memoria/CPU/conexiones
guardianx monitor

# Auditar puertos peligrosos abiertos
guardianx ports

# Recomendaciones de hardening
guardianx harden

# Actualizar firmas desde GitHub/raw HTTPS
guardianx update

# Ejecutar un ciclo de protección residente
guardianx resident --once

# Ejecutar guardián residente continuamente
guardianx resident

# Ver eventos recientes
guardianx events

# Auditoría completa
guardianx full ~/Downloads
Windows: crear .exe
En Windows:

powershell 
cd guardianx
packaging\windows\build_windows.ps1
Salida:

text 
dist\GuardianXCommunity.exe
Windows: crear instalador .exe
Instala Inno Setup.
Genera primero el EXE portable.
Compila:
text 
packaging\windows\guardianx_installer.iss
Salida:

text 
dist-installer\GuardianXCommunitySetup.exe
Más detalles en docs/WINDOWS_BUILD.md.

Servicio residente Windows
GuardianX Community puede instalarse como tarea programada al inicio de sesión:

powershell 
.\install_windows.ps1
packaging\windows\install_resident_task.ps1
La tarea se llama:

text 
GuardianX Resident Guard
Actualización de firmas
El actualizador descarga un JSON de firmas desde HTTPS. Por defecto apunta a:

text 
https://raw.githubusercontent.com/ylessoa/guardianx/main/signatures/signatures.json
Cambia la URL con:

bash 
guardianx update --url https://tu-servidor/signatures.json
Arquitectura
text 
guardianx/
  guardianx/core/scanner.py          # Motor de escaneo
  guardianx/core/signatures.py       # Carga de firmas
  guardianx/core/updater.py          # Actualización de firmas
  guardianx/core/quarantine.py       # Cuarentena
  guardianx/core/process_monitor.py  # Procesos: memoria/CPU/red
  guardianx/core/ports.py            # Puertos riesgosos
  guardianx/core/hardening.py        # Hardening
  guardianx/core/events.py           # Eventos del residente
  guardianx/service/resident.py      # Guardián residente
  guardianx/ui/tk_app.py             # Panel profesional
  packaging/windows/                 # EXE e instalador
Publicar en GitHub
bash 
git init
git add .
git commit -m "GuardianX Community 0.2"
git branch -M main
git remote add origin https://github.com/ylessoa/guardianx.git
git push -u origin main
Pruebas
bash 
pytest -q
Roadmap
Consulta docs/ROADMAP.md.

Seguridad y ética
GuardianX está diseñado solo para defensa. No se aceptan módulos de explotación, evasión, persistencia ofensiva, robo de credenciales, payloads o loaders
