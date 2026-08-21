
# tests/test_guardianpy_full_suite.py

import pytest
import logging
from types import SimpleNamespace
from guardianpy.core import system_monitor
from guardianpy.core.realtime_monitor import RealtimeMonitor

# --- Stubs para minería ---
class FakeCryptoDetector:
    def __init__(self, logger=None):
        self.logger = logger
    def scan_processes(self):
        return [{"pid": 9999, "name": "xmrig", "cpu_percent": 95}]

# --- Stubs para procesos ---
class FakeProcessHighCPU:
    def __init__(self, pid=1234, name="fake_high_cpu", cpu_percent=95.0):
        self.info = {
            "pid": pid,
            "name": name,
            "memory_info": SimpleNamespace(rss=200 * 1024 * 1024),
            "cpu_percent": cpu_percent,
        }
    def net_connections(self, kind="inet"):
        return ["suspicious_connection"]

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

# --- Suite de minería ---
def test_crypto_detector(monkeypatch):
    called = {}
    def fake_log_security_event(event_type, details):
        called["event_type"] = event_type
        called["details"] = details

    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)

    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    monitor._running = True
    monitor._run_cycle()
    monitor._running = False

    assert called.get("event_type") == "CryptoMining"
    assert called.get("details")[0]["name"] == "xmrig"

# --- Suite de lentitud ---
def test_system_slowness_positive(monkeypatch):
    called = {}
    def fake_log_security_event(source, description):
        called["source"] = source
        called["description"] = description

    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    result = system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    assert result is True
    assert "fake_high_cpu" in called.get("description", "")

def test_system_slowness_negative(monkeypatch):
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

# --- Suite de integración extendida ---
def test_realtime_monitor_triggers_all_detectors(monkeypatch):
    called = []

    def fake_log_security_event(event_type=None, details=None, source=None, description=None):
        if event_type == "CryptoMining":
            called.append(("CryptoMining", details))
        elif source == "system_monitor" and "rendimiento" in (description or "").lower():
            called.append(("SystemSlowness", description))
        elif source == "system_monitor" and "red" in (description or "").lower():
            called.append(("NetworkAnomaly", description))

    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    def fake_detect_network_anomalies(conn_threshold=100):
        system_monitor.events.log_security_event(
            source="system_monitor",
            description="Anomalía de red detectada: conexiones sospechosas"
        )
        return True

    monkeypatch.setattr(system_monitor, "detect_network_anomalies", fake_detect_network_anomalies)

    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    monitor._running = True
    monitor._run_cycle()
    system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)
    system_monitor.detect_network_anomalies(conn_threshold=10)
    monitor._running = False

    event_types = [evt[0] for evt in called]
    assert "CryptoMining" in event_types
    assert "SystemSlowness" in event_types
    assert "NetworkAnomaly" in event_types

# tests/test_guardianpy_full_suite.py

import pytest
import logging
from types import SimpleNamespace
from guardianpy.core import system_monitor
from guardianpy.core.realtime_monitor import RealtimeMonitor

# --- Stubs para minería ---
class FakeCryptoDetector:
    def __init__(self, logger=None):
        self.logger = logger
    def scan_processes(self):
        return [{"pid": 9999, "name": "xmrig", "cpu_percent": 95}]

# --- Stubs para procesos ---
class FakeProcessHighCPU:
    def __init__(self, pid=1234, name="fake_high_cpu", cpu_percent=95.0):
        self.info = {
            "pid": pid,
            "name": name,
            "memory_info": SimpleNamespace(rss=200 * 1024 * 1024),
            "cpu_percent": cpu_percent,
        }
    def net_connections(self, kind="inet"):
        return ["suspicious_connection"]

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

# --- Suite de minería ---
def test_crypto_detector(monkeypatch):
    called = {}
    def fake_log_security_event(event_type, details):
        called["event_type"] = event_type
        called["details"] = details

    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)

    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    monitor._running = True
    monitor._run_cycle()
    monitor._running = False

    assert called.get("event_type") == "CryptoMining"
    assert called.get("details")[0]["name"] == "xmrig"

# --- Suite de lentitud ---
def test_system_slowness_positive(monkeypatch):
    called = {}
    def fake_log_security_event(source, description):
        called["source"] = source
        called["description"] = description

    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    result = system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    assert result is True
    assert "fake_high_cpu" in called.get("description", "")

def test_system_slowness_negative(monkeypatch):
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

# --- Suite de integración extendida ---
def test_realtime_monitor_triggers_all_detectors(monkeypatch):
    called = []

    def fake_log_security_event(event_type=None, details=None, source=None, description=None):
        if event_type == "CryptoMining":
            called.append(("CryptoMining", details))
        elif source == "system_monitor" and "rendimiento" in (description or "").lower():
            called.append(("SystemSlowness", description))
        elif source == "system_monitor" and "red" in (description or "").lower():
            called.append(("NetworkAnomaly", description))

    import guardianpy.core.realtime_monitor as rm
    monkeypatch.setattr(rm.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.events, "log_security_event", fake_log_security_event)
    monkeypatch.setattr(system_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcessHighCPU()])
    monkeypatch.setattr(system_monitor.psutil, "cpu_percent", lambda _: None)

    def fake_detect_network_anomalies(conn_threshold=100):
        system_monitor.events.log_security_event(
            source="system_monitor",
            description="Anomalía de red detectada: conexiones sospechosas"
        )
        return True

    monkeypatch.setattr(system_monitor, "detect_network_anomalies", fake_detect_network_anomalies)

    monitor = RealtimeMonitor(interval=1, logger=logging.getLogger("GuardianPy"))
    monitor.crypto_detector = FakeCryptoDetector(logger=monitor.logger)

    monitor._running = True
    monitor._run_cycle()
    system_monitor.detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)
    system_monitor.detect_network_anomalies(conn_threshold=10)
    monitor._running = False

    event_types = [evt[0] for evt in called]
    assert "CryptoMining" in event_types
    assert "SystemSlowness" in event_types
    assert "NetworkAnomaly" in event_types
