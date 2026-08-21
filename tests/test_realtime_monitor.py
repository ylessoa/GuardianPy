# tests/test_realtime_monitor.py

import time
import pytest
from pathlib import Path
from guardianpy.core import events
from guardianpy.core.realtime_monitor import RealtimeMonitor
from guardianpy.core.integrity_monitor import initialize_baseline

def test_realtime_monitor_detects_file_changes(tmp_path, monkeypatch):
    """
    Test de integración:
    - Inicializa baseline con un archivo crítico.
    - Simula modificación del archivo.
    - Verifica que se registra alerta en events.jsonl.
    """

    # Crear archivo crítico simulado
    critical_file = tmp_path / "config.py"
    critical_file.write_text("valor_inicial", encoding="utf-8")

    # Redirigir baseline y log de eventos a archivos temporales
    monkeypatch.setattr("guardianpy.core.integrity_monitor.BASELINE_FILE", tmp_path / "baseline.json")
    monkeypatch.setattr(events, "event_log_path", lambda: tmp_path / "events.jsonl")

    # Inicializar baseline con el archivo crítico
    monkeypatch.setattr("guardianpy.core.integrity_monitor.CRITICAL_PATHS", [str(critical_file)])
    initialize_baseline()

    # Arrancar monitor con intervalo corto
    monitor = RealtimeMonitor(interval=0.5)
    monitor.start()

    # Simular modificación del archivo
    time.sleep(0.6)
    critical_file.write_text("valor_modificado", encoding="utf-8")

    # Esperar a que el monitor detecte el cambio
    time.sleep(1.2)
    monitor.stop()

    # Validar que se registró alerta en events.jsonl
    log_content = (tmp_path / "events.jsonl").read_text(encoding="utf-8")
    assert "integrity_monitor" in log_content
    assert "Cambio inesperado" in log_content
