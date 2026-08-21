# verify_core.py
import os
import re
from pathlib import Path

def check_residual_names():
    """Busca en todo el código si quedó algún rastro de 'GuardianPy' o 'guardianpy'."""
    print("\n[1/4] Verificando rastros del nombre anterior...")
    old_names = ["guardianpy", "GuardianPy"]
    found_residuals = False
    ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', 'build', 'dist', '.eggs'}
    
    for root, dirs, files in os.walk('.'):
        if any(d in ignore_dirs for d in Path(root).parts):
            continue
        for file in files:
            if file.endswith(('.py', '.toml', '.cfg', '.md', '.json', '.spec', '.bat', '.yml')):
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                    for old_name in old_names:
                        if old_name in content:
                            # Ignoramos referencias históricas válidas en el README (ej: "anteriormente GuardianX")
                            if file == "README.md" and "anteriormente" in content.lower():
                                continue
                            print(f"  ❌ ALERTA: Encontrado '{old_name}' en {file_path}")
                            found_residuals = True
                except Exception:
                    pass
    
    if not found_residuals:
        print("  ✅ Limpieza de nombre perfecta. No hay rastros del nombre anterior.")

def check_imports():
    """Verifica que todas las importaciones críticas del nuevo paquete funcionen."""
    print("\n[2/4] Verificando importaciones del paquete 'guardianpy'...")
    try:
        from guardianpy.core.config import AppConfig, load_config
        from guardianpy.core.logger import setup_logging
        from guardianpy.core.scanner import scan_paths
        from guardianpy.core.pe_analyzer import analyze_pe_file
        from guardianpy.core.threat_intel import ThreatIntel
        from guardianpy.core.realtime_monitor import RealtimeMonitor
        from services.resident import ResidentGuard
        from guardianpy.ui.tk_app import GuardianXGUI
        print("  ✅ Todas las importaciones críticas funcionan correctamente.")
    except ImportError as e:
        print(f"  ❌ Error de importación: {e}")
        print("     (Asegúrate de haber ejecutado 'pip install -e .' y de que las carpetas tengan __init__.py)")
    except Exception as e:
        print(f"  ❌ Error inesperado en imports: {e}")

def check_config():
    """Verifica que la configuración tenga el nuevo nombre de la app."""
    print("\n[3/4] Verificando configuración base...")
    try:
        from guardianpy.core.config import APP_NAME, AppConfig
        if APP_NAME == "GuardianPy":
            print("  ✅ APP_NAME configurado correctamente a 'GuardianPy'.")
        else:
            print(f"  ❌ APP_NAME sigue siendo: {APP_NAME}")
            
        cfg = AppConfig()
        if hasattr(cfg, 'vt_api_key'):
            print("  ✅ Campo de API Key de VirusTotal presente en la configuración.")
        else:
            print("  ❌ Falta el campo vt_api_key en AppConfig.")
    except Exception as e:
        print(f"  ❌ Error leyendo configuración: {e}")

def check_packaging():
    """Verifica que el archivo pyproject.toml tenga el nombre correcto."""
    print("\n[4/4] Verificando empaquetado (pyproject.toml)...")
    pyproject = Path('pyproject.toml')
    if not pyproject.exists():
        print("  ⚠️ No se encontró pyproject.toml.")
        return
        
    content = pyproject.read_text(encoding='utf-8')
    if 'name = "GuardianPy"' in content:
        print("  ✅ Nombre del paquete en pyproject.toml es 'GuardianPy'.")
    else:
        print("  ❌ El nombre en pyproject.toml no es 'GuardianPy'.")
        
    if 'guardianpy = "core.cli:main"' in content and 'GuardianPy-gui = "core.app:main"' in content:
        print("  ✅ Puntos de entrada (entry_points) de consola y GUI correctos.")
    else:
        print("  ❌ Los puntos de entrada (comandos guardianpy/guardianpy-gui) no están configurados.")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 AUDITORÍA DE INTEGRIDAD DE GUARDIANPY 🔧")
    print("=" * 60)
    
    check_residual_names()
    check_imports()
    check_config()
    check_packaging()
    
    print("\n" + "=" * 60)
    print("Auditoría finalizada. Si todo dice ✅, el repositorio está 100% íntegro.")
    print("=" * 60)
