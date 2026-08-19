import time
import threading
import argparse
import signal
import psutil
from core.config import load_config
from core.scanner import scan_paths
from core.quarantine import QuarantineManager
from core.logger import setup_logging

class ResidentGuard:
    def __init__(self) -> None:
        self.config = load_config()
        self.stop_event = threading.Event()
        self.quarantine = QuarantineManager()
        self.log = setup_logging(log_to_file=True)
        self.known_drives = set()

    def monitor_usb_devices(self):
        self.log.info("🖥️ Monitor de dispositivos USB iniciado.")
        self.known_drives = {d.device for d in psutil.disk_partitions(all=False)}
        while not self.stop_event.is_set():
            try:
                current_drives = {d.device for d in psutil.disk_partitions(all=False)}
                new_drives = current_drives - self.known_drives
                for drive in new_drives:
                    self.log.info(f"🔌 Nuevo dispositivo detectado: {drive}")
                    self.known_drives.add(drive)
                    threading.Thread(target=self.scan_usb, args=(drive,), daemon=True).start()
            except Exception as e:
                self.log.error(f"Error en monitor de USB: {e}")
            self.stop_event.wait(10)

    def scan_usb(self, drive_path):
        """Escanea una memoria USB recién conectada."""
        try:
            findings = scan_paths([drive_path], vt_api_key=self.config.vt_api_key)
            if findings:
                for f in findings:
                    self.log.warning(f"🚨 Amenaza en USB: {f.threat} en {f.path}")
                    if self.config.auto_quarantine:
                        try:
                            self.quarantine.quarantine(f)
                            self.log.info(f"Archivo neutralizado: {f.path}")
                        except Exception as e:
                            self.log.error(f"No se pudo cuarentenar {f.path}: {e}")
            else:
                self.log.info(f"✅ Escaneo de USB {drive_path} finalizado. Sin amenazas.")
        except Exception as e:
            self.log.error(f"Error escaneando USB {drive_path}: {e}")

