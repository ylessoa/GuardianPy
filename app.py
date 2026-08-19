from __future__ import annotations
import tkinter as tk
import threading
import logging

from ui.tk_app import GuardianPyGUI, QueueLogHandler
from core.logger import setup_logging
from core.persistence import setup_autostart
from services.resident import ResidentGuard

def main():
 root = tk.Tk()
 app = GuardianPyGUI(root)

 logger = setup_logging(log_to_file=True)
 gui_handler = QueueLogHandler(app.log_queue)
 gui_handler.setLevel(logging.INFO)
 gui_handler.setFormatter(
     logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
 )
 logger.addHandler(gui_handler)

 # Configurar auto-inicio con Windows
 setup_autostart()

 logger.info("🛡️ GuardianPy GUI iniciada. Listo para protección.")

 try:
     guard = ResidentGuard()
     threading.Thread(target=guard.run_forever, daemon=True).start()
     logger.info("🟢 Servicio residente iniciado en segundo plano.")
 except Exception as e:
     logger.error(f"No se pudo iniciar el servicio residente: {e}")

 root.mainloop()

if __name__ == "__main__":
 main()
