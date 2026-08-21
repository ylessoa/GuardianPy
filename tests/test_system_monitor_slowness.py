# tests/test_system_monitor_slowness.py

import pytest
import logging
from types import SimpleNamespace

from guardianpy.core import system_monitor

class FakeProcess:
    """Proceso simulado con CPU muy alta."""
    def __init__(self, pid=1234, name="fake_high_cpu", cpu_percent=95.0):
        self.info = {
            "pid": pid,
            "name": name,
            "memory_info": SimpleNamespace(rss=200 * 1024 * 1024),  # 200 MB
            "cpu_percent": cpu_percent,
        }

    def net_connections(self, kind="inet"):
        return []  # sin conexiones sospechosas


def test_detect_system_slowness_triggers_log_security_event(monkeypatch, caplog):
    caplog.set_level(logging.CRITICAL)

    # Stub de log_security_event para capturar llamadas
    called = {}
    def fake_log_security_event(source, description):
        called["source"] = source
        called["description"] = description

    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)

    # Stub de psutil para devolver solo nuestro proceso falso
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcess()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    result = system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    # Validar que detectó lentitud y llamó a log_security_event
    assert result is True
    assert called.get("source") == "system_monitor"
    assert "fake_high_cpu" in called.get("description", "")
    assert any("rendimiento lento" in msg.lower() for msg in caplog.messages)
