from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Rule:
    id: str
    name: str
    severity: str
    extensions: list[str]
    all_terms: list[str]
    any_terms: list[str]


@dataclass(slots=True)
class SignatureDB:
    version: str
    hashes_sha256: dict[str, str]
    rules: list[Rule]
    risky_ports: dict[int, str]


def default_signature_path() -> Path:
    package_path = Path(__file__).resolve().parents[1] / "signatures" / "signatures.json"
    if package_path.exists():
        return package_path
    return Path(__file__).resolve().parents[2] / "signatures" / "signatures.json"


def load_signatures(path: str | Path | None = None) -> SignatureDB:
    sig_path = Path(path) if path else default_signature_path()
    data = json.loads(sig_path.read_text(encoding="utf-8"))
    rules = [
        Rule(
            id=item["id"],
            name=item["name"],
            severity=item.get("severity", "medium"),
            extensions=[e.lower() for e in item.get("extensions", [])],
            all_terms=[t.lower() for t in item.get("all", [])],
            any_terms=[t.lower() for t in item.get("any", [])],
        )
        for item in data.get("rules", [])
    ]
    risky_ports = {int(k): v for k, v in data.get("risky_ports", {}).items()}
    return SignatureDB(
        version=data.get("version", "unknown"),
        hashes_sha256={k.lower(): v for k, v in data.get("hashes_sha256", {}).items()},
        rules=rules,
        risky_ports=risky_ports,
    )
