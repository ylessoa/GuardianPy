i# core/persistence.py
import sys
import platform
import logging

def setup_autostart():
    """Registra GuardianPy para que inicie con Windows (solo funciona si es un .exe compilado)."""
    log = logging.getLogger("GuardianPy")
    
    if platform.system() != "Windows":
        return
        
    # Si no es un ejecutable de PyInstaller, no hacer nada (para no ejecutar Python al inicio)
    if not getattr(sys, 'frozen', False):
        log.debug("No es un ejecutable compilado, se omite el auto-inicio.")
        return

    try:
        import winreg
        exe_path = sys.executable
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "GuardianPy", 0, winreg.REG_SZ, f'"{exe_path}"')
        log.info("Auto-inicio con Windows configurado correctamente.")
    except Exception as e:
        log.error(f"No se pudo configurar el auto-inicio: {e}")
