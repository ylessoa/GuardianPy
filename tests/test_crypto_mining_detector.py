# tests/test_crypto_mining_detector.py

import pytest
import logging
from guardianpy.core.crypto_mining_detector import CryptoMiningDetector

class FakeProcess:
    """Proceso simulado con nombre xmrig y CPU alta."""
    def __init__(self, pid=4321, name="xmrig", cpu_percent=95):
        self.pid = pid
        self._name = name
        self._cpu_percent = cpu_percent
        self.info = {
            "pid": pid,
            "name": name,
            "cpu_percent": cpu_percent,
        }

    def name(self):
        return self._name

    def cpu_percent(self, interval=None):
        return self._cpu_percent

    def connections(self, kind="inet"):
        # No conexiones sospechosas en este stub
        return []

def test_crypto_mining_detector_marks_xmrig_as_suspicious(monkeypatch, caplog):
    caplog.set_level(logging.CRITICAL)

    detector = CryptoMiningDetector(logger=logging.getLogger("GuardianPy"))

    # Monkeypatch psutil para devolver nuestro proceso falso
    import guardianpy.core.crypto_mining_detector as mining_detector
    monkeypatch.setattr(mining_detector.psutil, "process_iter", lambda attrs=None: [FakeProcess()])

    suspicious = detector.scan_processes()

    # Validar que el proceso xmrig fue detectado
    assert suspicious, "El detector no marcó el proceso como sospechoso"
    assert suspicious[0]["name"] == "xmrig"
    assert any("minería no autorizada" in msg.lower() for msg in caplog.messages)
