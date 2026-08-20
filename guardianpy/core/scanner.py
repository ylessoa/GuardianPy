from __future__ import annotations
import logging
import re
from pathlib import Path
from typing import Iterable

from guardianpy.core.url_checker import analyze_url
from guardianpy.core.models import ThreatFinding
import logging
import yara
import hashlib
import os
from pathlib import Path
from typing import Callable, Iterable

from core.pe_analyzer import analyze_pe_file
from core.threat_intel import ThreatIntel
from core.models import ThreatFinding
from core.signatures import SignatureDB, load_signatures
from core.updater import active_signature_path
#from services.resident import ResidentGuard
logger = logging.getLogger("GuardianPy")

class Scanner:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def scan_text_for_urls(self, text: str) -> Iterable[ThreatFinding]:
        """
        Escanea un texto en busca de URLs y las analiza con url_checker.
        """
        url_pattern = re.compile(r"https?://[^\s]+")
        urls = url_pattern.findall(text)

        findings = []
        for url in urls:
            suspicious, reason = analyze_url(url, api_key=self.api_key)
            if suspicious:
                logger.warning(f"⚠️ Enlace sospechoso detectado: {url} ({reason})")
                findings.append(
                    ThreatFinding(
                        category="URL",
                        target=url,
                        severity="High",
                        description=f"Enlace sospechoso: {reason}"
                    )
                )
            else:
                logger.info(f"✅ Enlace seguro: {url}")
        return findings

    def scan_file(self, file_path: Path) -> Iterable[ThreatFinding]:
        """
        Escanea un archivo de texto buscando enlaces sospechosos.
        """
        findings = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                findings.extend(self.scan_text_for_urls(content))
        except Exception as e:
            logger.error(f"Error leyendo archivo {file_path}: {e}")
        return findings
def scan_file(path):
    rules = yara.compile(filepath="rules/eicar.yar")
    matches = rules.match(path)
    return matches

TEXT_EXTENSIONS = {".ps1", ".bat", ".cmd", ".js", ".vbs", ".sh", ".py", ".pl", ".reg", ".txt"}
EXECUTABLE_EXTENSIONS = {".exe", ".dll", ".sys"}

# core/scanner.py (Modificar la función scan_paths)

# Añadir extensiones de ejecutables a la lista
EXECUTABLE_EXTENSIONS = {".exe", ".dll", ".sys"}

# core/scanner.py (Modificar la función scan_paths)

def scan_paths(
    roots: Iterable[str | Path],
    signatures: SignatureDB | None = None,
    progress: ProgressCallback | None = None,
    max_file_mb: int = 100,
    vt_api_key: str = "" # Nuevo parámetro opcional
) -> list[ThreatFinding]:
    db = signatures or load_signatures(active_signature_path())
    findings: list[ThreatFinding] = []
    count = 0
    logger = logging.getLogger("GuardianPy")
    
    # Inicializar cliente de Threat Intel si se proporciona API Key
    threat_intel = ThreatIntel(api_key=vt_api_key) if vt_api_key else None
    
    for file_path in iter_files(roots, max_file_mb=max_file_mb):
        count += 1
        if progress:
            progress(file_path, count)
            
        try:
            digest = sha256_file(file_path)
            # 1. Buscar en base de datos local
            if digest in db.hashes_sha256:
                findings.append(
                    ThreatFinding(
                        path=file_path,
                        threat=db.hashes_sha256[digest],
                        severity="critical",
                        reason="SHA-256 hash matched signature database.",
                        sha256=digest,
                    )
                )
                continue # Si ya lo detectamos localmente, pasamos al siguiente
            # 2. Si no está local y tenemos API Key, consultar en la nube
            elif threat_intel and file_path.suffix.lower() in EXECUTABLE_EXTENSIONS:
                vt_result = threat_intel.check_hash(digest)
                if vt_result["malicious"]:
                    findings.append(
                        ThreatFinding(
                            path=file_path,
                            threat="Cloud Threat (VirusTotal)",
                            severity="critical",
                            reason=vt_result["reason"],
                            sha256=digest,
                        )
                    )
        except OSError:
            continue

        # 3. Análisis heurístico local (PE imports y texto)
        ext = file_path.suffix.lower()
        if ext in EXECUTABLE_EXTENSIONS:
            pe_findings = analyze_pe_file(file_path, logger)
            for item in pe_findings:
                item.sha256 = digest
                findings.append(item)
                
        elif ext in TEXT_EXTENSIONS:
            content_findings = _scan_content(file_path, db)
            for item in content_findings:
                item.sha256 = digest
                findings.extend(content_findings)

    return findings
def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

def iter_files(roots: Iterable[str | Path], max_file_mb: int = 100) -> Iterable[Path]:
    max_bytes = max_file_mb * 1024 * 1024
    for root in roots:
        p = Path(root).expanduser()
        if p.is_file():
            yield p
            continue
        if not p.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(p, topdown=True, onerror=lambda _: None):
            dirnames[:] = [d for d in dirnames if d.lower() not in DEFAULT_EXCLUDES]
            for filename in filenames:
                f = Path(dirpath) / filename
                try:
                    if f.is_file() and f.stat().st_size <= max_bytes:
                        yield f
                except OSError:
                    continue

def _scan_content(path: Path, db: SignatureDB) -> list[ThreatFinding]:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return []
    try:
        raw = path.read_bytes()[:2_000_000]
        try:
            text = raw.decode('utf-8').lower()
        except UnicodeDecodeError:
            try:
                text = raw.decode('utf-16').lower()
            except UnicodeDecodeError:
                text = raw.decode('latin-1', errors='replace').lower()
    except OSError:
        return []
        
    findings: list[ThreatFinding] = []
    for rule in db.rules:
        if rule.extensions and path.suffix.lower() not in rule.extensions:
            continue
        if all(term in text for term in rule.all_terms) and (not rule.any_terms or any(term in text for term in rule.any_terms)):
            findings.append(
                ThreatFinding(
                    path=path,
                    threat=rule.name,
                    severity=rule.severity,
                    reason=f"Matched heuristic rule: {rule.id}",
                    metadata={"rule_id": rule.id},
                )
            )
    return findings

def scan_paths(
    roots: Iterable[str | Path],
    signatures: SignatureDB | None = None,
    progress: ProgressCallback | None = None,
    max_file_mb: int = 100,
) -> list[ThreatFinding]:
    db = signatures or load_signatures(active_signature_path())
    findings: list[ThreatFinding] = []
    count = 0
    for file_path in iter_files(roots, max_file_mb=max_file_mb):
        count += 1
        if progress:
            progress(file_path, count)
        try:
            digest = sha256_file(file_path)
        except OSError:
            continue
        if digest in db.hashes_sha256:
            findings.append(
                ThreatFinding(
                    path=file_path,
                    threat=db.hashes_sha256[digest],
                    severity="critical",
                    reason="SHA-256 hash matched signature database.",
                    sha256=digest,
                )
            )
        content_findings = _scan_content(file_path, db)
        for item in content_findings:
            item.sha256 = digest
        findings.extend(content_findings)
    return findings
# core/scanner.py (Añadir a la función _scan_content o crear una nueva función)

# Signaturas hexadecimales de exploits comunes (Metasploit, shellcode genérico)
EXPLOIT_SIGNATURES = {
    b"\xfc\xe8\x89\x00\x00\x00": "Metasploit Shellcode (Stager)",
    b"\x90\x90\x90\x90\x90\x90": "NOP Sled (Típico de Buffer Overflow)",
    b"\x60\x89\xe5\x31\xc0\x64": "Shellcode Linux x86 (Execve)",
    b"fcsdb": "FAT32 Malformed Cluster (Exploit de Sistema de Archivos)"
}

def _scan_for_shellcode(path: Path) -> list[ThreatFinding]:
    try:
        # Leer los primeros 2MB del archivo en formato binario
        with path.open("rb") as fh:
            raw = fh.read(2_000_000)
            
        findings: list[ThreatFinding] = []
        for signature, threat_name in EXPLOIT_SIGNATURES.items():
            if signature in raw:
                findings.append(
                    ThreatFinding(
                        path=path,
                        threat=threat_name,
                        severity="critical",
                        reason=f"Exploit signature found: {signature.hex()}",
                        metadata={"type": "shellcode"}
                    )
                )
        return findings
    except Exception:
        return []
