# tests/test_system_monitor_slowness_negative.py

import pytest
from types import SimpleNamespace
from guardianpy.core import system_monitor

class FakeProcessLowUsage:
    """Proceso simulado con CPU y memoria bajas."""
    def __init__(self, pid=5678, name="idle_process", cpu_percent=5.0):
        self.info = {
            "pid": pid,
            "name": name,
            "memory_info": SimpleNamespace(rss=50 * 1024 * 1024),  # 50 MB
            "cpu_percent": cpu_percent,
        }

    def net_connections(self, kind="inet"):
        return []  # sin conexiones sospechosas


def test_detect_system_slowness_returns_false_and_no_event(monkeypatch):
    called = {}
    def fake_log_security_event(source, description):
        called["source"] = source
        called["description"] = description

    # Stub de log_security_event
    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)

    # Stub de psutil para devolver solo nuestro proceso con bajo consumo
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessLowUsage()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    result = system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    # Validar que no se detectó lentitud y no se llamó a log_security_event
    assert result is False
    assert called == {}
