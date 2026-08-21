# tests/test_realtime_filehandler.py

import pytest
import logging
from pathlib import Path
from guardianpy.core.realtime_monitor import RealtimeFileHandler
from guardianpy.core.signatures import SignatureDB
from guardianpy.core.quarantine import QuarantineManager

def test_mass_modification_triggers_alert(tmp_path, caplog):
    """
    Test de integración:
    - Simula múltiples modificaciones rápidas de archivos.
    - Valida que el MassModificationDetector dispara la alerta de ransomware.
    """

    # Configurar logger para capturar mensajes críticos
    caplog.set_level(logging.CRITICAL)

    # Crear instancias simuladas de dependencias
    signatures = SignatureDB()
    quarantine = QuarantineManager(tmp_path)
    handler = RealtimeFileHandler(signatures, quarantine, auto_quarantine=False, logger=logging.getLogger("GuardianPy"))

    # Simular modificaciones masivas
    for i in range(60):  # más que el threshold=50
        fake_file = tmp_path / f"file_{i}.txt"
        fake_file.write_text("contenido", encoding="utf-8")
        handler.mass_mod_detector.register_modification()

    # Validar que se disparó la alerta crítica
    assert any("CONTAMINACIÓN MASIVA DETECTADA" in message for message in caplog.messages)
