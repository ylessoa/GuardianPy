from pathlib import Path
from guardianx.core.quarantine import QuarantineManager
from guardianx.core.models import ThreatFinding

def test_restore_file(tmp_path: Path):
    file = tmp_path / "malware.txt"
    file.write_text("contenido malicioso")
    finding = ThreatFinding(path=file, threat="TestThreat", severity="high", reason="Testing", sha256="abc123")
    qm = QuarantineManager(tmp_path / "vault")
    dst = qm.quarantine(finding)
    assert dst.exists()
    assert not file.exists()
    items = qm.list_items()
    assert len(items) == 1
    restored_path = qm.restore(items[0]["id"])
    assert restored_path.exists()
    assert restored_path.read_text() == "contenido malicioso"
    assert len(qm.list_items()) == 0
