# guardianpy/core/realtime_monitor.py
from __future__ import annotations
import logging
import queue
import threading
import psutil
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from guardianpy.core.scanner import scan_paths
from guardianpy.core.quarantine import QuarantineManager
from guardianpy.core.signatures import SignatureDB
from guardianpy.core.integrity_monitor import MassModificationDetector, check_integrity
from guardianpy.core.system_monitor import detect_network_anomalies
from guardianpy.core.crypto_mining_detector import CryptoMiningDetector
from guardianpy.core import events  # asegúrate de tener events.py con log_security_event


class RealtimeMonitor:
    def __init__(self, interval: int = 30, logger: logging.Logger | None = None):
        """
        Monitor en tiempo real que ejecuta detectores periódicamente.
        :param interval: intervalo en segundos entre ejecuciones
        """
        self.interval = interval
        self._timer = None
        self._running = False
        self.logger = logger or logging.getLogger("GuardianPy")
        self.crypto_detector = CryptoMiningDetector(logger=self.logger)

    def _run_cycle(self):
        """Ejecuta un ciclo de detección y programa el siguiente."""
        if not self._running:
            return

        try:
            # Detector de anomalías de red
            findings = detect_network_anomalies(conn_threshold=100)
            if findings:
                self.logger.warning(f"[RealtimeMonitor] {len(findings)} anomalías de red detectadas.")

            # Detector de integridad de archivos/configuración
            check_integrity()
            self.logger.info("[RealtimeMonitor] Verificación de integridad completada.")

            # Detector de minería no autorizada
            suspicious = self.crypto_detector.scan_processes()
            if suspicious:
                events.log_security_event("CryptoMining", suspicious)
                self.logger.critical("[RealtimeMonitor] 🚨 Minería no autorizada detectada.")

        except Exception as e:
            self.logger.error(f"[RealtimeMonitor] Error en detección: {e}")

        # Programar siguiente ejecución
        self._timer = threading.Timer(self.interval, self._run_cycle)
        self._timer.start()

    def start(self):
        """Inicia el monitor en segundo plano."""
        if not self._running:
            self._running = True
            self.logger.info("[RealtimeMonitor] Iniciando monitor residente...")
            self._run_cycle()

    def stop(self):
        """Detiene el monitor."""
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None
        self.logger.info("[RealtimeMonitor] Monitor detenido.")


class RealtimeFileHandler(FileSystemEventHandler):
    def __init__(self, signatures: SignatureDB, quarantine: QuarantineManager, auto_quarantine: bool, logger: logging.Logger):
        self.signatures = signatures
        self.quarantine = quarantine
        self.auto_quarantine = auto_quarantine
        self.log = logger
        self.mass_mod_detector = MassModificationDetector()

        # FIX: Crear una cola y un hilo trabajador para no saturar watchdog
        self.scan_queue = queue.Queue()
        self.worker = threading.Thread(target=self._process_queue, daemon=True)
        self.worker.start()

    def _process_queue(self):
        """Hilo trabajador que escanea archivos sin congelar watchdog."""
        while True:
            event_path = self.scan_queue.get()
            if event_path is None:
                break  # Señal de cierre

            path = Path(event_path)
            if path.is_dir() or path.suffix.lower() in ['.part', '.crdownload', '.tmp', '.download', '.log']:
                continue

            is_mass_attack = self.mass_mod_detector.register_modification()
            if is_mass_attack:
                self.log.critical("⚔️ Posible Ransomware. Buscando culpable...")
                self._find_and_kill_culprit()
                continue

            try:
                findings = scan_paths([event_path], signatures=self.signatures, max_file_mb=100)
                if findings:
                    for finding in findings:
                        self.log.warning(f"🚨 Amenaza: {finding.threat} en {finding.path}")
                        if self.auto_quarantine:
                            try:
                                dst = self.quarantine.quarantine(finding)
                                self.log.info(f"Neutralizado: {dst}")
                            except Exception as e:
                                self.log.error(f"Fallo cuarentena: {e}")
            except Exception as e:
                self.log.debug(f"Error escaneando {event_path}: {e}")

    def _find_and_kill_culprit(self):
        """Identifica de forma segura qué proceso está escribiendo masivamente en disco."""
        SAFE_PROCESSES = [
            "googledrivesync.exe", "dropbox.exe", "onedrive.exe", "syncthing.exe",
            "explorer.exe", "searchindexer.exe", "system", "smss.exe", "csrss.exe",
            "wininit.exe", "services.exe", "lsass.exe", "svchost.exe"
        ]

        culprit_proc = None
        max_io = 0

        try:
            for proc in psutil.process_iter(["pid", "name", "io_counters"]):
                proc_name = proc.info.get("name", "").lower()
                if proc_name in SAFE_PROCESSES or not proc_name:
                    continue

                io_write = proc.info.get("io_counters", None)
                if io_write:
                    write_bytes = io_write.write_bytes
                    if write_bytes > max_io:
                        max_io = write_bytes
                        culprit_proc = proc

            if culprit_proc and max_io > 50_000_000:
                self.log.critical(
                    f"⚔️ Culpable encontrado: {culprit_proc.info['name']} "
                    f"(PID: {culprit_proc.info['pid']}). Escribió {max_io / 1_000_000:.1f}MB. Neutralizando..."
                )
                culprit_proc.kill()
            else:
                self.log.warning("Se detectó modificación masiva, pero no se identificó un proceso malicioso claro.")
        except Exception as e:
            self.log.error(f"Error en _find_and_kill_culprit: {e}")

    def on_created(self, event):
        if not event.is_directory:
            self.scan_queue.put(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.scan_queue.put(event.src_path)
