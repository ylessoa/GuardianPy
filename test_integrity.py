# test_integrity.py
import logging
from core.logger import setup_logging

def test_all_modules():
    log = setup_logging(log_to_file=False)
    log.info("Iniciando prueba de integridad de módulos...")

    try:
        # 1. Probar Configuración
        from core.config import load_config
        cfg = load_config()
        log.info("✅ Módulo 'config' OK")

        # 2. Probar PE Analyzer (Requiere 'pefile' instalado)
        from core.pe_analyzer import analyze_pe_file
        log.info("✅ Módulo 'pe_analyzer' OK")

        # 3. Probar Process Monitor (Requiere 'psutil')
        from core.process_monitor import detect_memory_misuse, detect_exploit_behavior, terminate_process
        log.info("✅ Módulo 'process_monitor' OK")

        # 4. Probar Realtime Monitor (Requiere 'watchdog')
        from core.realtime_monitor import RealtimeMonitor, RealtimeFileHandler
        log.info("✅ Módulo 'realtime_monitor' OK")

        # 5. Probar UI (Requiere 'tkinter', 'pystray', 'Pillow')
        from core.ui.tk_app import GuardianXGUI, QueueLogHandler
        log.info("✅ Módulo 'ui.tk_app' OK")

        # 6. Probar Resident
        from core.services.resident import ResidentGuard
        log.info("✅ Módulo 'services.resident' OK")

        log.info("🎉 ¡Todas las importaciones están correctas! El código está íntegro.")

    except ImportError as e:
        log.error(f"❌ Error de importación: Falta instalar una dependencia o un archivo. {e}")
    except Exception as e:
        log.error(f"❌ Error inesperado en la integridad: {e}")

if __name__ == "__main__":
    test_all_modules()
