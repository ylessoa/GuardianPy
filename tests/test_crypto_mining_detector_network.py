
# tests/test_crypto_mining_detector_network.py

import pytest
import logging
from guardianpy.core.crypto_mining_detector import CryptoMiningDetector

class FakeConnection:
    def __init__(self, port):
        self.laddr = type("LAddr", (), {"port": port})

class FakeProcess:
    """Proceso simulado con conexión sospechosa a puerto 3333."""
    def __init__(self, pid=5678, name="legit_app", cpu_percent=10):
        self.pid = pid
        self._name = name
        self.info = {
            "pid": pid,
            "name": name,
            "cpu_percent": cpu_percent,
        }

    def name(self):
        return self._name

    def cpu_percent(self, interval=None):
        return self.info["cpu_percent"]

    def connections(self, kind="inet"):
        return [FakeConnection(3333)]  # puerto típico de minería

def test_crypto_mining_detector_marks_network_suspicious(monkeypatch, caplog):
    caplog.set_level(logging.CRITICAL)

    detector = CryptoMiningDetector(logger=logging.getLogger("GuardianPy"))

    import guardianpy.core.crypto_mining_detector as mining_detector
    monkeypatch.setattr(mining_detector.psutil, "process_iter", lambda attrs=None: [FakeProcess()])

    suspicious = detector.scan_processes()

    # Validar que el proceso fue detectado por conexión sospechosa
    assert suspicious, "El detector no marcó el proceso como sospechoso por red"
    assert suspicious[0]["pid"] == 5678
    assert any("minería no autorizada" in msg.lower() for msg in caplog.messages)

# tests/test_crypto_mining_detector_network.py

import pytest
import logging
from guardianpy.core.crypto_mining_detector import CryptoMiningDetector

class FakeConnection:
    def __init__(self, port):
        self.laddr = type("LAddr", (), {"port": port})

class FakeProcess:
    """Proceso simulado con conexión sospechosa a puerto 3333."""
    def __init__(self, pid=5678, name="legit_app", cpu_percent=10):
        self.pid = pid
        self._name = name
        self.info = {
            "pid": pid,
            "name": name,
            "cpu_percent": cpu_percent,
        }

    def name(self):
        return self._name

    def cpu_percent(self, interval=None):
        return self.info["cpu_percent"]

    def connections(self, kind="inet"):
        return [FakeConnection(3333)]  # puerto típico de minería

def test_crypto_mining_detector_marks_network_suspicious(monkeypatch, caplog):
    caplog.set_level(logging.CRITICAL)

    detector = CryptoMiningDetector(logger=logging.getLogger("GuardianPy"))

    import guardianpy.core.crypto_mining_detector as mining_detector
    monkeypatch.setattr(mining_detector.psutil, "process_iter", lambda attrs=None: [FakeProcess()])

    suspicious = detector.scan_processes()

    # Validar que el proceso fue detectado por conexión sospechosa
    assert suspicious, "El detector no marcó el proceso como sospechoso por red"
    assert suspicious[0]["pid"] == 5678
    assert any("minería no autorizada" in msg.lower() for msg in caplog.messages)

