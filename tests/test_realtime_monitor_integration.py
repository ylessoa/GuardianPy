
# tests/test_realtime_monitor_integration.py

import pytest
import logging
from types import SimpleNamespace
from guardianpy.core.realtime_monitor import RealtimeMonitor
from guardianpy.core import system_monitor

# --- Stubs para minería ---
class FakeCryptoDetector:
    def __init__(self, logger=None):
        self.logger = logger
    def scan_processes(self):
        return [{"pid": 9999, "name": "xmrig", "cpu_percent": 95}]

# --- Stub para proceso con CPU alta ---
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

def test_realtime_monitor_triggers_crypto_and_slowness(monkeypatch):
    called = []

    # Stub de log_security_event para capturar eventos
    def fake_log_security_event(event_type=None, details=None, source=None, description=None):
        if event_type == "CryptoMining":
            called.append(("CryptoMining", details))
        elif source == "system_monitor":
            called.append(("SystemSlowness", description))

    # Parchear eventos y psutil
    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    # Crear monitor con detector falso de minería
    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    # Ejecutar un ciclo manual y además forzar la detección de lentitud
    monitor._running = True
    monitor._run_cycle()
    system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)
    monitor._running = False

    # Validar que se registraron ambos eventos
    event_types = [evt[0] for evt in called]
    assert "CryptoMining" in event_types
    assert "SystemSlowness" in event_types

# tests/test_realtime_monitor_integration.py

import pytest
import logging
from types import SimpleNamespace
from guardianpy.core.realtime_monitor import RealtimeMonitor
from guardianpy.core import system_monitor

# --- Stubs para minería ---
class FakeCryptoDetector:
    def __init__(self, logger=None):
        self.logger = logger
    def scan_processes(self):
        return [{"pid": 9999, "name": "xmrig", "cpu_percent": 95}]

# --- Stub para proceso con CPU alta ---
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

def test_realtime_monitor_triggers_crypto_and_slowness(monkeypatch):
    called = []

    # Stub de log_security_event para capturar eventos
    def fake_log_security_event(event_type=None, details=None, source=None, description=None):
        if event_type == "CryptoMining":
            called.append(("CryptoMining", details))
        elif source == "system_monitor":
            called.append(("SystemSlowness", description))

    # Parchear eventos y psutil
    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    # Crear monitor con detector falso de minería
    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    # Ejecutar un ciclo manual y además forzar la detección de lentitud
    monitor._running = True
    monitor._run_cycle()
    system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)
    monitor._running = False

    # Validar que se registraron ambos eventos
    event_types = [evt[0] for evt in called]
    assert "CryptoMining" in event_types
    assert "SystemSlowness" in event_types
