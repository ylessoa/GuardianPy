import time
import threading
import argparse
import signal
import psutil
from pathlib import Path
from guardianpy.core.config import load_config
from guardianpy.core.events import log_event
from guardianpy.core.process_monitor import detect_memory_misuse, detect_exploit_behavior, terminate_process
from guardianpy.core.quarantine import QuarantineManager
from guardianpy.core.updater import active_signature_path
from guardianpy.core.scanner import scan_paths
from guardianpy.core.signatures import load_signatures
from guardianpy.core.logger import setup_logging
from guardianpy.core.realtime_monitor import RealtimeMonitor, RealtimeFileHandler

class ResidentGuard:
    def __init__(self) -> None:
        self.config = load_config()
        self.stop_event = threading.Event()
        self.quarantine = QuarantineManager()
        self.log = setup_logging(log_to_file=True)
        self.realtime_monitor = None
        self.known_drives = set()
        self.last_full_scan_time = 0.0

    def run_scheduled_scan(self):
        """Ejecuta un escaneo de carpetas críticas cada 12 horas."""
        while not self.stop_event.is_set():
            if self.stop_event.wait(43200):
                break
            self.log.info("⏰ Iniciando escaneo programado de 12 horas...")
            try:
                paths_to_scan = self.config.normalized_watch_paths()
                findings = scan_paths(paths_to_scan, vt_api_key=self.config.vt_api_key)
                if findings:
                    for finding in findings:
                        self.log.warning(f"[Escaneo Programado] Amenaza encontrada: {finding.threat} en {finding.path}")
                        if self.config.auto_quarantine:
                            try:
                                self.quarantine.quarantine(finding)
                            except Exception as e:
                                self.log.error(f"No se pudo cuarentenar: {e}")
                else:
                    self.log.info("✅ Escaneo programado finalizado. Sistema limpio.")
            except Exception as e:
                self.log.error(f"Error en escaneo programado: {e}")

    def monitor_usb_devices(self):
        """Vigila la conexión de memorias USB y las escanea automáticamente."""
        self.log.info("🖥️ Monitor de dispositivos USB iniciado.")
        self.known_drives = {d.device for d in psutil.disk_partitions(all=False)}
        while not self.stop_event.is_set():
            try:
                current_drives = {d.device for d in psutil.disk_partitions(all=False)}
                new_drives = current_drives - self.known_drives
                for drive in new_drives:
                    self.log.info(f"🔌 Nuevo dispositivo detectado: {drive}. Iniciando escaneo automático...")
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
                            self.log.info(f"Archivo de USB neutralizado: {f.path}")
                        except Exception as e:
                            self.log.error(f"No se pudo cuarentenar {f.path}: {e}")
            else:
                self.log.info(f"✅ Escaneo de USB {drive_path} finalizado. Sin amenazas.")
        except Exception as e:
            self.log.error(f"Error escaneando USB {drive_path}: {e}")

    def monitor_system_cycle(self):
        """Monitorea procesos y detecta comportamientos sospechosos."""
        proc_findings = detect_memory_misuse(
            self.config.memory_mb_threshold,
            self.config.cpu_threshold,
            self.config.max_connections,
        )
        for proc in proc_findings[:20]:
            log_event("process", f"PID {proc.pid} {proc.name}: {proc.reason}", proc.severity,
                      rss_mb=proc.rss_mb, cpu=proc.cpu_percent, connections=proc.connections)

        exploit_findings = detect_exploit_behavior()
        for proc in exploit_findings:
            log_event("exploit", f"ALERTA DE EXPLOTACIÓN: {proc.reason}", "critical",
                      pid=proc.pid, name=proc.name)
            self.log.critical(f"🚨 {proc.reason} (PID: {proc.pid})")
            if self.config.auto_quarantine:
                self.log.warning(f"⚔️ Intentando neutralizar proceso malicioso PID: {proc.pid}...")
                if terminate_process(proc.pid):
                    self.log.info(f"✅ Proceso PID {proc.pid} neutralizado exitosamente.")
                else:
                    self.log.error(f"❌ No se pudo matar PID {proc.pid}. ¿Permisos de administrador?")

    def init_realtime_protection(self):
        db = load_signatures(active_signature_path())
        handler = RealtimeFileHandler(
            signatures=db,
            quarantine=self.quarantine,
            auto_quarantine=self.config.auto_quarantine,
            logger=self.log
        )
        self.realtime_monitor = RealtimeMonitor(
            watch_paths=self.config.normalized_watch_paths(),
            handler=handler
        )
        self.realtime_monitor.start()

    def run_forever(self) -> None:
        self.log.info("🛡️ GuardianPy Resident Guard iniciado")
        if self.config.realtime_enabled:
            try:
                self.init_realtime_protection()
            except Exception as e:
                self.log.error(f"Fallo al iniciar protección en tiempo real: {e}")

        threading.Thread(target=self.run_scheduled_scan, daemon=True).start()
        threading.Thread(target=self.monitor_usb_devices, daemon=True).start()

        while not self.stop_event.is_set():
            try:
                self.monitor_system_cycle()
            except Exception as exc:
                self.log.error(f"Error en ciclo de sistema: {exc}", exc_info=True)
            self.stop_event.wait(max(10, int(self.config.scan_interval_seconds)))

        if self.realtime_monitor:
            self.realtime_monitor.stop()
            self.log.info("Protección en tiempo real detenida.")
        self.log.info("GuardianPy Resident Guard detenido")

    def stop(self, *_args) -> None:
        self.stop_event.set()

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GuardianPy Resident Guard")
    parser.add_argument("--once", action="store_true", help="Run one protection cycle and exit")
    args = parser.parse_args(argv)
    guard = ResidentGuard()
    if args.once:
        guard.config.realtime_enabled = False
        guard.run_forever()
        return 0
    signal.signal(signal.SIGTERM, guard.stop)
    signal.signal(signal.SIGINT, guard.stop)
    guard.run_forever()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
