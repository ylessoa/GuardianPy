# rename_project.py
"""
Script automatizado para renombrar el proyecto.
Cambia 'GuardianX' por el nuevo nombre en todos los archivos.
"""
import os
import re
from pathlib import Path

# CONFIGURACIÓN
OLD_NAME_LOWER = "guardianpy"
OLD_NAME_MIXED = "GuardianPy"
NEW_NAME_LOWER = "Guardianpy"      # <-- Cambia aquí tu nuevo nombre
NEW_NAME_MIXED = "GuardianPy"     # <-- Cambia aquí tu nuevo nombre  

# Extensiones de archivos a procesar
TARGET_EXTENSIONS = {
    '.py', '.md', '.txt', '.toml', '.cfg', '.yml', '.yaml', 
    '.json', '.bat', '.ps1', '.sh', '.spec', '.gitignore', '.gitattributes'
}

# Carpetas a ignorar (no tocar)
IGNORE_DIRS = {
    '.git', '__pycache__', '.venv', 'venv', 'build', 'dist', 
    '.eggs', '*.egg-info', 'node_modules'
}

def should_ignore(path: Path) -> bool:
    """Verifica si la ruta debe ser ignorada."""
    for part in path.parts:
        if part in IGNORE_DIRS or part.endswith('.egg-info'):
            return True
    return False

def replace_in_file(file_path: Path) -> int:
    """Reemplaza el nombre viejo por el nuevo en un archivo. Devuelve el número de reemplazos."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Reemplazar versiones mixtas (GuardianX -> GuardianPy)
        content = content.replace(OLD_NAME_MIXED, NEW_NAME_MIXED)
        # Reemplazar versiones minúsculas 
        content = content.replace(OLD_NAME_LOWER, NEW_NAME_LOWER)
        
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return content.count(NEW_NAME_MIXED) + content.count(NEW_NAME_LOWER)
        return 0
    except Exception as e:
        print(f"  ⚠️ Error en {file_path}: {e}")
        return 0

def rename_files_and_dirs(root: Path):
    """Renombra archivos y carpetas que contengan el nombre viejo."""
    items_to_rename = []
    
    for item in root.rglob('*'):
        if should_ignore(item):
            continue
        
        if OLD_NAME_LOWER in item.name.lower():
            items_to_rename.append(item)
    
    # Renombrar de adentro hacia afuera (archivos primero, luego carpetas)
    items_to_rename.sort(key=lambda x: len(x.parts), reverse=True)
    
    for item in items_to_rename:
        new_name = item.name.replace(OLD_NAME_MIXED, NEW_NAME_MIXED).replace(OLD_NAME_LOWER, NEW_NAME_LOWER)
        new_path = item.parent / new_name
        
        if item.exists() and new_path != item:
            try:
                item.rename(new_path)
                print(f"  📁 Renombrado: {item.name} -> {new_name}")
            except Exception as e:
                print(f"  ⚠️ No se pudo renombrar {item}: {e}")

def main():
    root = Path('.')
    total_replacements = 0
    files_modified = 0
    
    print("=" * 60)
    print(f"🔄 Iniciando renombrado: {OLD_NAME_MIXED} -> {NEW_NAME_MIXED}")
    print("=" * 60)
    
    # Paso 1: Reemplazar contenido de archivos
    print("\n[1/3] Reemplazando contenido en archivos...")
    for file_path in root.rglob('*'):
        if file_path.is_file() and file_path.suffix in TARGET_EXTENSIONS and not should_ignore(file_path):
            count = replace_in_file(file_path)
            if count > 0:
                files_modified += 1
                total_replacements += count
                print(f"  ✅ {file_path}: {count} reemplazos")
    
    # Paso 2: Renombrar archivos y carpetas
    print("\n[2/3] Renombrando archivos y carpetas...")
    rename_files_and_dirs(root)
    
    # Paso 3: Resumen
    print("\n" + "=" * 60)
    print(f"✅ Proceso completado:")
    print(f"   • Archivos modificados: {files_modified}")
    print(f"   • Reemplazos totales: {total_replacements}")
    print(f"   • Nombre nuevo: {NEW_NAME_MIXED}")
    print("=" * 60)
    print("\n⚠️  ACCIONES MANUALES PENDIENTES:")
    print(f"   1. Renombra la carpeta raíz del proyecto a '{NEW_NAME_LOWER}'")
    print(f"   2. Actualiza el remote de Git: git remote set-url origin https://github.com/ylessoa/{NEW_NAME_LOWER}.git")
    print(f"   3. Renombra el repo en GitHub: Settings > Repository name")
    print(f"   4. Actualiza el icono (.ico) con el nuevo logo")
    print(f"   5. Ejecuta: pip install -e .  para reinstalar el paquete con el nuevo nombre")

if __name__ == "__main__":
    main()
