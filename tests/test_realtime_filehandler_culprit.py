# tests/test_realtime_filehandler_culprit.py

import pytest
import logging
from pathlib import Path
from guardianpy.core.realtime_monitor import RealtimeFileHandler
from guardianpy.core.quarantine import QuarantineManager

class FakeSignatureDB:
    def __init__(self):
        self.version = "test"
        self.hashes_sha256 = {}
        self.rules = []
        self.risky_ports = []

class FakeProcess:
    def __init__(self, pid=1234, name="fake_writer"):
        self.pid = pid
        self._name = name
        self.info = {
            "pid": pid,
            "name": name,
            "io_counters": self.io_counters()
        }

    def name(self):
        return self._name

    def io_counters(self):
        class IO:
            write_bytes = 10**9  # 1 GB escrito
        return IO()

    def kill(self):
        return True

def test_find_and_kill_culprit_detects_suspicious_process(tmp_path, caplog, monkeypatch):
    caplog.set_level(logging.CRITICAL)

    signatures = FakeSignatureDB()
    quarantine = QuarantineManager(tmp_path)
    handler = RealtimeFileHandler(
        signatures,
        quarantine,
        auto_quarantine=False,
        logger=logging.getLogger("GuardianPy")
    )

    import guardianpy.core.realtime_monitor as realtime_monitor
    monkeypatch.setattr(realtime_monitor.psutil, "process_iter", lambda attrs=None: [FakeProcess()])

    # Ejecutar el método privado (no devuelve nada útil, solo loguea)
    handler._find_and_kill_culprit()

    # Validar que se registró el mensaje crítico
    assert any("culpable encontrado" in msg.lower() for msg in caplog.messages)
    assert any("neutralizando" in msg.lower() for msg in caplog.messages)
