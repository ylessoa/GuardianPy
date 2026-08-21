# tests/test_crypto_mining_detector_suite.py

import pytest
import logging
from guardianpy.core.crypto_mining_detector import CryptoMiningDetector

# --- Stubs para simular procesos sospechosos ---

class FakeProcessCPU:
    """Proceso simulado con nombre xmrig y CPU alta."""
    def __init__(self, pid=4321, name="xmrig", cpu_percent=95):
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
        return []  # sin conexiones sospechosas


class FakeConnection:
    def __init__(self, port):
        self.laddr = type("LAddr", (), {"port": port})


class FakeProcessNetwork:
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


# --- Tests combinados ---

def test_crypto_mining_detector_marks_xmrig_as_suspicious(monkeypatch, caplog):
    caplog.set_level(logging.CRITICAL)
    detector = CryptoMiningDetector(logger=logging.getLogger("GuardianPy"))

    import guardianpy.core.crypto_mining_detector as mining_detector
    monkeypatch.setattr(mining_detector.psutil, "process_iter", lambda attrs=None: [FakeProcessCPU()])

    suspicious = detector.scan_processes()

    assert suspicious, "El detector no marcó el proceso xmrig como sospechoso"
    assert suspicious[0]["name"] == "xmrig"
    assert any("minería no autorizada" in msg.lower() for msg in caplog.messages)


def test_crypto_mining_detector_marks_network_suspicious(monkeypatch, caplog):
    caplog.set_level(logging.CRITICAL)
    detector = CryptoMiningDetector(logger=logging.getLogger("GuardianPy"))

    import guardianpy.core.crypto_mining_detector as mining_detector
    monkeypatch.setattr(mining_detector.psutil, "process_iter", lambda attrs=None: [FakeProcessNetwork()])

    suspicious = detector.scan_processes()

    assert suspicious, "El detector no marcó el proceso como sospechoso por red"
    assert suspicious[0]["pid"] == 5678
    assert any("minería no autorizada" in msg.lower() for msg in caplog.messages)
