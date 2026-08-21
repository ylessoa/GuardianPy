# tests/test_guardianpy_suite.py

import pytest
import logging
from types import SimpleNamespace
from guardianpy.core import system_monitor
from guardianpy.core.realtime_monitor import RealtimeMonitor

# --- Stubs para minería ---

class FakeCryptoDetector:
    """Detector falso que siempre devuelve un proceso sospechoso."""
    def __init__(self, logger=None):
        self.logger = logger
    def scan_processes(self):
        return [{"pid": 9999, "name": "xmrig", "cpu_percent": 95}]


# --- Stubs para lentitud del sistema ---

class FakeProcessHighCPU:
    def __init__(self, pid=1234, name="fake_high_cpu", cpu_percent=95.0):
        self.info = {
            "pid": pid,
            "name": name,
            "memory_info": SimpleNamespace(rss=200 * 1024 * 1024),
            "cpu_percent": cpu_percent,
        }
    def net_connections(self, kind="inet"):
        return []


class FakeProcessLowUsage:
    def __init__(self, pid=5678, name="idle_process", cpu_percent=5.0):
        self.info = {
            "pid": pid,
            "name": name,
            "memory_info": SimpleNamespace(rss=50 * 1024 * 1024),
            "cpu_percent": cpu_percent,
        }
    def net_connections(self, kind="inet"):
        return []


# --- Tests de minería ---

def test_realtime_monitor_triggers_crypto_event(monkeypatch):
    called = {}
    def fake_log_security_event(event_type, details):
        called["event_type"] = event_type
        called["details"] = details

    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)

    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    # Ejecutar un ciclo manual y detener
    monitor._running = True
    monitor._run_cycle()
    monitor._running = False

    assert called.get("event_type") == "CryptoMining"
    assert called.get("details")[0]["name"] == "xmrig"


# --- Tests de lentitud del sistema ---

def test_detect_system_slowness_positive(monkeypatch):
    called = {}
    def fake_log_security_event(source, description):
        called["source"] = source
        called["description"] = description

    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    result = system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    assert result is True
    assert called.get("source") == "system_monitor"
    assert "fake_high_cpu" in called.get("description", "")


def test_detect_system_slowness_negative(monkeypatch):
    called = {}
    def fake_log_security_event(source, description):
        called["source"] = source
        called["description"] = description

    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessLowUsage()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    result = system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    assert result is False
    assert called == {}
