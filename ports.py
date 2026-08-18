from __future__ import annotations

import psutil

from .models import PortFinding
from .signatures import SignatureDB, load_signatures


def audit_open_ports(signatures: SignatureDB | None = None) -> list[PortFinding]:
    db = signatures or load_signatures()
    findings: list[PortFinding] = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.status != psutil.CONN_LISTEN or not conn.laddr:
            continue
        port = int(conn.laddr.port)
        reason = db.risky_ports.get(port)
        if not reason:
            continue
        process = None
        if conn.pid:
            try:
                process = psutil.Process(conn.pid).name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process = None
        findings.append(
            PortFinding(
                port=port,
                protocol="tcp" if conn.type.name == "SOCK_STREAM" else "udp",
                address=conn.laddr.ip,
                pid=conn.pid,
                process=process,
                severity="high" if port in {23, 445, 3389, 5900} else "medium",
                reason=reason,
            )
        )
    return findings
