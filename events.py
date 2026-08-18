from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import app_data_dir


def event_log_path() -> Path:
    return app_data_dir() / "events.jsonl"


def log_event(kind: str, message: str, severity: str = "info", **metadata: Any) -> None:
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        "severity": severity,
        "message": message,
        "metadata": metadata,
    }
    with event_log_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_recent_events(limit: int = 100) -> list[dict[str, Any]]:
    path = event_log_path()
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[-limit:]
    rows: list[dict[str, Any]] = []
    for line in lines:
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows
