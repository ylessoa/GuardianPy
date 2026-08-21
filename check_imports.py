#!/usr/bin/env python
"""
Script de verificación de imports para GuardianPy
Confirma que guardianpy.core y guardianpy.services se importan correctamente.
"""

import importlib

def check_import(module_name: str):
    try:
        importlib.import_module(module_name)
        print(f"✅ Import correcto: {module_name}")
    except Exception as e:
        print(f"❌ Error al importar {module_name}: {e}")

if __name__ == "__main__":
    print("🔎 Verificando imports de GuardianPy...\n")
    check_import("guardianpy.core")
    check_import("guardianpy.services")
    print("\n🏁 Verificación completada.")
