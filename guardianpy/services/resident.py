import time
import threading
import logging
import psutil

from guardianpy.core.realtime_monitor import RealtimeMonitor
from guardianpy.core.autostart import setup_autostart   # mueve setup_autostart aquí para evitar ciclos
from guardianpy.core.config import load_config
from guardianpy.core.scanner import scan_paths
from guardianpy.core.quarantine import QuarantineManager
from guardianpy.core.logger import setup_logging
from guardianpy.services.bluetooth_guard import BluetoothGuard


class ResidentGuard:
    def __init__(self, interval: int = 30):
        """
        Servicio residente de GuardianPy.
        Ejecuta el monitor en segundo plano y vigila dispositivos USB.
        """
        self.config = load_config()
        self.stop_event = threading.Event()
        self.quarantine = QuarantineManager()
        self.log = setup_logging(log_to_file=True)
        self.known_drives = set()
        self.monitor = RealtimeMonitor(interval=interval)
        self.thread = None
        self.logger = logging.getLogger("ResidentGuard")

    def run_forever(self):
        """Mantiene el monitor corriendo indefinidamente."""
        self.logger.info("🛡️ GuardianPy ResidentGuard iniciado.")
        self.monitor.start()

        # Lanzar monitor de USB en segundo plano
        threading.Thread(target=self.monitor_usb_devices, daemon=True).start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("🛑 ResidentGuard detenido por el usuario.")
            self.stop_event.set()
            self.monitor.stop()

    def start_background(self):
        """Inicia el servicio en un hilo separado."""
        self.thread = threading.Thread(target=self.run_forever, daemon=True)
        self.thread.start()
        self.logger.info("🟢 ResidentGuard corriendo en segundo plano.")

    def monitor_usb_devices(self):
        """Vigila dispositivos USB conectados y lanza escaneo."""
        self.log.info("🖥️ Monitor de dispositivos USB iniciado.")
        self.known_drives = {d.device for d in psutil.disk_partitions(all=False)}
        while not self.stop_event.is_set():



