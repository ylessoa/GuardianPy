from __future__ import annotations
import json
import os
import shutil
import tempfile
import threading
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from .models import ThreatFinding

class QuarantineManager:
    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir or Path.home() / ".GuardianPy" / "quarantine")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.base_dir / "index.json"
        self.lock = threading.Lock()

    def _load_index(self) -> list[dict]:
        if not self.index_path.exists():
            return []
        try:
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

    def _save_index(self, rows: list[dict]) -> None:
        with tempfile.NamedTemporaryFile(mode='w', dir=self.base_dir, delete=False, encoding='utf-8') as tmp:
            json.dump(rows, tmp, indent=2, ensure_ascii=False)
        os.replace(tmp.name, self.index_path)

    def quarantine(self, finding: ThreatFinding) -> Path:
        with self.lock:
            src = finding.path
            if not src.exists() or not src.is_file():
                raise FileNotFoundError(src)
            entry_id = uuid4().hex
            safe_name = f"{entry_id}.qtn"
            dst = self.base_dir / safe_name
            shutil.move(str(src), str(dst))
            try:
                os.chmod(dst, 0o600)
            except OSError:
                pass
            rows = self._load_index()
            rows.append({
                "id": entry_id,
                "quarantined_at": datetime.now(timezone.utc).isoformat(),
                "original_path": str(src),
                "vault_path": str(dst),
                "threat": finding.threat,
                "severity": finding.severity,
                "reason": finding.reason,
                "sha256": finding.sha256,
            })
            self._save_index(rows)
            return dst

    def list_items(self) -> list[dict]:
        return self._load_index()

    def restore(self, entry_id: str, destination: str | Path | None = None) -> Path:
        with self.lock:
            rows = self._load_index()
            for row in rows:
                if row["id"] == entry_id:
                    src = Path(row["vault_path"])
                    dst = Path(destination or row["original_path"])
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    try:
                        os.chmod(dst, 0o644)
                    except OSError:
                        pass
                    self._save_index([r for r in rows if r["id"] != entry_id])
                    return dst
            raise KeyError(f"No quarantine entry: {entry_id}")
