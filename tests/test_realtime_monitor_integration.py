import time
import pytest
from guardianpy.core import events
from guardianpy.core.realtime_monitor import RealtimeMonitor

def test_realtime_monitor_integration_with_detector(tmp_path, monkeypatch):
    # Redirigimos el log de eventos a un archivo temporal
    fake_events_file = tmp_path / "events.jsonl"
    monkeypatch.setattr(events, "event_log_path", lambda: fake_events_file)

    # Mock del detector extendido: simula una anomalía real
    def fake_detector(conn_threshold=100):
        return [{
            "pid": 9999,
            "name": "integration_process",
            "reason": "Exceso de conexiones: 200; Conexiones a IPs desconocidas: 203.0.113.99"
        }]

    monkeypatch.setattr(
        "guardianpy.core.system_monitor.detect_network_anomalies",
        fake_detector
    )

    # Usamos un intervalo corto para el test
    monitor = RealtimeMonitor(interval=0.5)
    monitor.start()

    # Esperamos ~1.2 segundos para que se ejecute varias veces
    time.sleep(1.2)
    monitor.stop()

    # Validamos que se registró al menos un evento en el archivo
    log_content = fake_events_file.read_text(encoding="utf-8")
    assert "integration_process" in log_content
    assert "Exceso de conexiones" in log_content
    assert "IPs desconocidas" in log_content
    assert "security" in log_content
    assert "warning" in log_content
