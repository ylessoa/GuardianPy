# GuardianPy

GuardianPy es un sistema de monitoreo y detección de amenazas en tiempo real, diseñado para identificar comportamientos sospechosos, conflictos de código y anomalías en entornos de desarrollo.

---

## 🚀 Funcionalidades principales

- **Detección de conflictos de merge**  
  Script `detect_conflicts.sh` que analiza el repositorio y marca líneas con `<<<<<<<`, `=======`, `>>>>>>>` para resolver conflictos rápidamente.

- **Flujo seguro de sincronización (`safe_pull.sh`)**  
  Automatiza la actualización de la rama `main`:
  - Ejecuta `git pull --rebase --autostash` para evitar merges innecesarios.
  - Si se detectan conflictos, descarta cambios locales y sincroniza con el remoto (`git reset --hard origin/main`).
  - Verifica automáticamente que no queden marcas de conflicto en `guardianpy/` y `tests/`.

- **Monitoreo en tiempo real**  
  Integración con detectores de minería de criptomonedas, conexiones sospechosas y slowness del sistema.

- **Suite de pruebas automatizadas**  
  Conjunto de tests unitarios e integrados para validar cada módulo del sistema.

---

## 🛠️ Instalación

```bash
git clone https://github.com/tuusuario/GuardianPy.git
cd GuardianPy
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
