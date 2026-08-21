# 🛡️ GuardianPy – Seguridad en tiempo real

> *“Tu guardián digital contra amenazas invisibles.”*

GuardianPy protege tu equipo contra minería no autorizada, ransomware, conexiones sospechosas y conflictos de código. Diseñado para usuarios que buscan seguridad y estabilidad sin complicaciones.

---

## 📊 Dashboard visual

![GuardianPy Dashboard](dashboard.png)

Este panel muestra:
- **System Monitoring**: CPU y GPU en tiempo real, actividad de red.  
- **Threat Alerts**: alertas de minería, ransomware y conexiones sospechosas.  
- **Repo Sync Status**: estado de conflictos y sincronización con el remoto.  

---

## 🎯 Utilidades principales

| 🔧 Función | Descripción breve |
|------------|------------------|
| ⚡ Detección de minería no autorizada | Bloquea procesos que usan tus recursos sin permiso. |
| 🛑 Bloqueo de ransomware | Detiene cifrados masivos antes de que dañen tus archivos. |
| 🌐 Conexiones sospechosas | Analiza URLs y bloquea dominios peligrosos. |
| 📂 Cuarentena de archivos | Aísla archivos maliciosos automáticamente. |
| 🔄 Sincronización segura | Actualiza tu proyecto sin conflictos. |
| ⚙️ Verificación de conflictos | Detecta merges sin resolver en tu repositorio. |

---

## 👁️ Casos de uso reales

### 🧩 Descargas un archivo sospechoso
```text
[GuardianPy Alert]
⚠️ Archivo sospechoso detectado: invoice_2026.pdf
Tipo: PDF con macros ocultas
Acción: Archivo movido a cuarentena

###🔥 Tu sistema se pone lento
[GuardianPy Alert]
⚠️ Proceso sospechoso detectado: xmrig.exe
Uso de CPU: 95%
Acción: Proceso bloqueado y registrado en log.

###🌐 Conexión peligrosa
[GuardianPy Alert]
🚫 Conexión bloqueada: phishing-login.example.net
Motivo: Dominio malicioso
Acción: Conexión cerrada y URL marcada como insegura.

###⚙️ Sincronización limpia
[GuardianPy Git Helper]
✔️ Conflictos descartados automáticamente
✔️ Rama local sincronizada con origin/main

###🚀 Inicio rápido
git clone https://github.com/tuusuario/GuardianPy.git
cd GuardianPy
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

###Ejecuta el servicio residente:
python -m guardianpy.services.resident


python -m guardianpy.services.resident

✅ Estado actual
GuardianPy combina seguridad informática avanzada (detección de minería, ransomware y conexiones sospechosas) con herramientas de productividad (sincronización limpia y verificación de conflictos), para que trabajes y uses tu equipo sin preocupaciones.

