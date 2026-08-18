# core/realtime_monitor.py (Reemplazar la clase RealtimeFileHandler y RealtimeMonitor)

from __future__ import annotations
import time
import logging
import queue
import threading
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from GuardianPy.core.scanner import scan_paths
from GuardianPy.core.quarantine import QuarantineManager
from GuardianPy.core.signatures import SignatureDB
from GuardianPy.core.integrity_monitor import MassModificationDetector
import psutil

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
            if event_path is None: break # Señal de cierre
            
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

    # core/realtime_monitor.py (Reemplazar la función _find_and_kill_culprit)

    def _find_and_kill_culprit(self):
        """Identifica de forma segura qué proceso está escribiendo masivamente en disco."""
        SAFE_PROCESSES = ["googledrivesync.exe", "dropbox.exe", "onedrive.exe", "syncthing.exe", "explorer.exe", "searchindexer.exe", "system", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe", "svchost.exe"]
        
        culprit_proc = None
        max_io = 0
        
        try:
            # Medir qué proceso tiene mayor actividad de escritura en disco AHORA MISMO
            for proc in psutil.process_iter(["pid", "name", "io_counters"]):
                proc_name = proc.info.get("name", "").lower()
                if proc_name in SAFE_PROCESSES or not proc_name:
                    continue
                
                # Contador de bytes escritos
                io_write = proc.info.get("io_counters", None)
                if io_write:
                    write_bytes = io_write.write_bytes
                    if write_bytes > max_io:
                        max_io = write_bytes
                        culprit_proc = proc

            # Si encontramos un culpable claro (escribió más de 50MB en disco)
            if culprit_proc and max_io > 50_000_000: 
                self.log.critical(f"⚔️ Culpable encontrado: {culprit_proc.info['name']} (PID: {culprit_proc.info['pid']}). Escribió {max_io / 1_000_000:.1f}MB. Neutralizando...")
                culprit_proc.kill()
            else:
                self.log.warning("Se detectó modificación masiva, pero no se identificó un proceso malicioso claro. No se mató nada para proteger la estabilidad del sistema.")
        except Exception as e:
            self.log.error(f"Error en _find_and_kill_culprit: {e}")
    def on_created(self, event):
        if not event.is_directory:
            self.scan_queue.put(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.scan_queue.put(event.src_path)

class RealtimeMonitor:
    def __init__(self, watch_paths: list[str], handler: RealtimeFileHandler):
        self.observer = Observer()
        self.handler = handler
        self.watch_paths = watch_paths

    def start(self):
        for path in self.watch_paths:
            if Path(path).exists():
                self.observer.schedule(self.handler, path, recursive=True)
                self.handler.log.info(f"👁️ Vigilando en tiempo real: {path}")
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.handler.scan_queue.put(None) # Detener el hilo trabajador
        self.observer.join()
