# core/integrity_monitor.py
import time
import threading
import logging

class MassModificationDetector:
    """Detecta si se están modificando demasiados archivos en poco tiempo (Ransomware/File Infector)."""
    
    def __init__(self, threshold: int = 50, time_window: int = 5):
        self.threshold = threshold
        self.time_window = time_window
        self.modifications = []
        self.lock = threading.Lock()
        self.log = logging.getLogger("guardianx")
        
    def register_modification(self) -> bool:
        """Llama a esto cada vez que un archivo se modifica. Devuelve True si se superó el umbral."""
        with self.lock:
            now = time.time()
            self.modifications.append(now)
            
            # Limpiar modificaciones viejas fuera de la ventana de tiempo
            self.modifications = [t for t in self.modifications if now - t < self.time_window]
            
            if len(self.modifications) > self.threshold:
                self.log.critical(f"🚨 CONTAMINACIÓN MASIVA DETECTADA: {len(self.modifications)} archivos modificados en {self.time_window}s.")
                # Vaciar la lista para no disparar la alarma repetidamente
                self.modifications = []
                return True
            return False
