# app.py
from __future__ import annotations
import tkinter as tk
import threading
import logging
from GuardianPy.ui.tk_app import GuardianPyGUI, QueueLogHandler
from GuardianPy.core.logger import setup_logging
from GuardianPy.core.persistence import setup_autostart # NUEVO IMPORT
from guardianpy.gui import start_gui

if __name__ == "__main__":
    
    start_gui()


def main():
    root = tk.Tk()
    app = GuardianPyGUI(root)
    
    logger = setup_logging(log_to_file=True)
    gui_handler = QueueLogHandler(app.log_queue)
    gui_handler.setLevel(logging.INFO)
    gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S'))
    logger.addHandler(gui_handler)
    
    # Configurar auto-inicio con Windows
    setup_autostart() # NUEVA LÍNEA
    
    logger.info("🛡️ GuardianPy GUI iniciada. Listo para protección.")
    
    try:
        from GuardianPy.services.resident import ResidentGuard
        guard = ResidentGuard()
        threading.Thread(target=guard.run_forever, daemon=True).start()
        logger.info("🟢 Servicio residente iniciado en segundo plano.")
    except Exception as e:
        logger.error(f"No se pudo iniciar el servicio residente: {e}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
        threading.Thread(target=guard.run_forever, daemon=True).start()
        logger.info("🟢 Servicio residente iniciado en segundo plano.")
    except Exception as e:
        logger.error(f"No se pudo iniciar el servicio residente: {e}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
