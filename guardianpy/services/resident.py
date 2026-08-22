import time
import threading
import logging
import psutil

from guardianpy.core.realtime_monitor import RealtimeMonitor
from guardianpy.core.autostart import setup_autostart   # evita ciclos de importación
from guardianpy.core.config import load_config
from guardianpy.core.scanner import scan_paths
from guardianpy.core.quarantine import QuarantineManager
from guardianpy.core.logger import setup_logging
from guardianpy.services.bluetooth_guard import BluetoothGuard
from guardianpy.services.bluetooth_guard_windows import BluetoothGuardWindows


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


def main():
    # Configurar auto-inicio en Windows
    setup_autostart()

    # Iniciar GuardianPy ResidentGuard
    guard = ResidentGuard(interval=30)
    threading.Thread(target=guard.run_forever, daemon=True).start()

    # Iniciar BluetoothGuard (Windows) en paralelo
    whitelist = ["MiAuricularBT", "MiTecladoBT", "00:1A:7D:DA:71:13"]
    bt_guard = BluetoothGuardWindows(whitelist=whitelist, scan_interval=20)
    threading.Thread(target=bt_guard.start_monitoring, daemon=True).start()

    # Mantener proceso principal vivo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("🛑 GuardianPy detenido por el usuario.")


if __name__ == "__main__":
    main()



