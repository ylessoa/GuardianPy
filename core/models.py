from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ThreatFinding:
    path: Path
    threat: str
    severity: str
    reason: str
    sha256: str | None = None
    action: str = "detected"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProcessFinding:
    pid: int
    name: str
    severity: str
    reason: str
    rss_mb: float
    cpu_percent: float
    connections: int


@dataclass(slots=True)
class PortFinding:
    port: int
    protocol: str
    address: str
    pid: int | None
    process: str | None
    severity: str
    reason: str


@dataclass(slots=True)
class HardeningFinding:
    area: str
    severity: str
    status: str
    recommendation: str
