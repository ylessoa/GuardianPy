import time
import pytest
from guardianpy.core.realtime_monitor import RealtimeMonitor

def test_realtime_monitor_calls_detector(monkeypatch):
    calls = []

    # Mock de detect_network_anomalies para registrar llamadas
    def fake_detector(conn_threshold=100):
        calls.append(time.time())
        return []

    monkeypatch.setattr(
        "guardianpy.core.system_monitor.detect_network_anomalies",
        fake_detector
    )

    # Usamos un intervalo corto para el test (0.5 segundos)
    monitor = RealtimeMonitor(interval=0.5)
    monitor.start()

    # Esperamos ~1.2 segundos para que se ejecute varias veces
    time.sleep(1.2)
    monitor.stop()

    # Validamos que se llamó al menos 2 veces
    assert len(calls) >= 2

    # Validamos que las llamadas tienen separación aproximada al intervalo
    intervals = [calls[i+1] - calls[i] for i in range(len(calls)-1)]
    # Deben estar alrededor de 0.5 segundos (con tolerancia)
    assert all(0.3 <= iv <= 0.8 for iv in intervals)

