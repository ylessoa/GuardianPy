# 🛡️ GuardianPy

GuardianPy es un sistema de seguridad residente para Windows, diseñado para **detectar, monitorear y mitigar amenazas en tiempo real**.  
Combina análisis de procesos, monitoreo de puertos, detección de conexiones sospechosas y validación de URLs, todo dentro de un paquete modular y extensible.

---

## 🚀 Capacidades principales

### 🔍 Monitoreo en tiempo real
- **System Monitor**: Detecta comportamientos anómalos en el sistema (lentitud, procesos sospechosos).
- **Process Monitor**: Supervisa procesos activos y alerta sobre ejecuciones no autorizadas.
- **Ports Monitor**: Vigila puertos abiertos y conexiones entrantes/salientes.

### 🌐 Seguridad de red
- **URL Checker**: Analiza URLs para detectar conexiones maliciosas o dominios sospechosos.
- **Threat Intel**: Integra fuentes de inteligencia para validar reputación de archivos y dominios.

### 📂 Protección de archivos
- **Scanner**: Escanea rutas específicas en busca de malware o patrones peligrosos.
- **Quarantine**: Aísla archivos sospechosos para evitar su ejecución.
- **Signatures**: Usa reglas YARA y firmas personalizadas para detectar amenazas.

### 🖥️ Interfaz y control
- **Resident Service**: Corre en segundo plano como guardia residente, iniciando junto al sistema.
- **UI (tk_app)**: Interfaz gráfica para usuarios finales, con control de escaneo y reportes.
- **CLI**: Línea de comandos para administración avanzada.

### 🧩 Extensibilidad
- **Core Modules**: Arquitectura modular (`core/`) que permite añadir nuevos detectores.
- **Rules & Signatures**: Reglas YARA y firmas JSON fáciles de actualizar.
- **Updater**: Sistema de actualización automática de firmas y módulos.

---

## ⚡ Quickstart

Sigue estos pasos para instalar y ejecutar GuardianPy en tu sistema:

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu_usuario>/GuardianPy.git
cd GuardianPy

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/MacOS
venv\Scripts\activate      # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servicio residente
python -m guardianpy.services.resident
o solo para defensa. No se aceptan módulos de explotación, evasión, persistencia ofensiva, robo de credenciales, payloads o loaders.

