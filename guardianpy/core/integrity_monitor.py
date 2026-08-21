"""
guardianpy/core/integrity_monitor.py
Monitor de integridad: detecta cambios inesperados en archivos críticos
y configuraciones del sistema, comparando contra un baseline en JSON.
"""

import os
import json
import hashlib
import time
import threading
import logging
from pathlib import Path
from guardianpy.core import events

# Ruta donde se guarda el baseline
BASELINE_FILE = Path("guardianpy/core/integrity_baseline.json")

# Archivos críticos a vigilar (puedes ampliar esta lista)
CRITICAL_PATHS = [
    "guardianpy/core/config.py",
    "guardianpy/core/scanner.py",
    "guardianpy/core/system_monitor.py",
    "guardianpy/core/sql_monitor.py",
    "rules/eicar.yar",
    "signatures/signatures.json"
]


def file_hash(path: str) -> str:
    """Genera el hash SHA256 de un archivo."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def load_baseline() -> dict:
    """Carga el baseline desde JSON, o devuelve dict vacío si no existe."""
    if BASELINE_FILE.exists():
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_baseline(baseline: dict):
    """Guarda el baseline en JSON."""
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)


def initialize_baseline():
    """Crea baseline inicial con hashes de archivos críticos."""
    baseline = {}
    for path in CRITICAL_PATHS:
        if os.path.exists(path):
            baseline[path] = file_hash(path)
    save_baseline(baseline)
    events.log_security_event(
        "integrity_monitor",
        "Baseline inicial creado para archivos críticos."
    )


def check_integrity():
    """Verifica integridad de archivos críticos contra baseline."""
    baseline = load_baseline()
    for path in CRITICAL_PATHS:
        if not os.path.exists(path):
            continue
        current_hash = file_hash(path)
        baseline_hash = baseline.get(path)
        if baseline_hash and current_hash != baseline_hash:
            events.log_security_event(
                "integrity_monitor",
                f"Cambio inesperado detectado en {path}"
            )
            # Actualizar baseline para reflejar nuevo estado
            baseline[path] = current_hash
    save_baseline(baseline)


class MassModificationDetector:
    """Detecta si se están modificando demasiados archivos en poco tiempo (Ransomware/File Infector)."""

    def __init__(self, threshold: int = 50, time_window: int = 5):
        self.threshold = threshold
        self.time_window = time_window
        self.modifications = []
        self.lock = threading.Lock()
        self.log = logging.getLogger("GuardianPy")

    def register_modification(self) -> bool:
        """Llama a esto cada vez que un archivo se modifica. Devuelve True si se superó el umbral."""
        with self.lock:
            now = time.time()
            self.modifications.append(now)

            # Limpiar modificaciones viejas fuera de la ventana de tiempo
            self.modifications = [t for t in self.modifications if now - t < self.time_window]

            if len(self.modifications) > self.threshold:
                self.log.critical(
                    f"🚨 CONTAMINACIÓN MASIVA DETECTADA: {len(self.modifications)} archivos modificados en {self.time_window}s."
                )
                # Vaciar la lista para no disparar la alarma repetidamente
                self.modifications = []
                return True
            return False
