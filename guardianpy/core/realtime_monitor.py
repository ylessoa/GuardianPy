#guardianpy/core/realtime_monitor.py
import psutil
import logging
import threading
import time

class RealtimeMonitor:
    def __init__(self, interval=30):
        self.interval = interval
        self.running = False
        self.logger = logging.getLogger("RealtimeMonitor")

    def start(self):
        self.running = True
        self.logger.info("RealtimeMonitor iniciado.")
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.logger.info("RealtimeMonitor detenido.")

    def _loop(self):
        while self.running:
            # Aquí va la lógica de monitoreo en tiempo real
            time.sleep(self.interval)


class RealtimeFileHandler:
    """
    Stub de RealtimeFileHandler para pruebas.
    """
    def __init__(self, path=None):
        self.path = path

    def monitor(self):
        # Simulación: no hace nada
        return True


def detect_system_slowness(threshold=90):
    """
    Detecta si algún proceso está consumiendo CPU por encima del umbral.
    Retorna True si hay lentitud, False en caso contrario.
    """
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if proc.cpu_percent(interval=0.1) > threshold:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def detect_network_anomalies():
    """
    Simulación: detecta anomalías de red.
    Por defecto retorna False, pero los tests pueden parchearla.
    """
    return False
