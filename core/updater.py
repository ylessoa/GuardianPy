from __future__ import annotations
import json
import os
import shutil
import tempfile
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from .config import DEFAULT_UPDATE_URL, app_data_dir
from .signatures import default_signature_path, load_signatures

def local_signature_path() -> Path:
    return app_data_dir() / "signatures.json"

def active_signature_path() -> Path:
    local = local_signature_path()
    return local if local.exists() else default_signature_path()

def update_signatures(url: str = DEFAULT_UPDATE_URL, timeout: int = 15) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            raw = response.read(5_000_000)
    except urllib.error.URLError as e:
        raise RuntimeError(f"Error de red descargando firmas: {e}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado: {e}")

    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("El archivo de firmas no es un JSON válido")

    if "hashes_sha256" not in data or "rules" not in data:
        raise ValueError("Signature database is missing required fields")
        
    target = local_signature_path()
    if target.exists():
        backup = target.with_suffix(f".backup-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.json")
        shutil.copy2(target, backup)
        
    with tempfile.NamedTemporaryFile(mode='w', dir=target.parent, delete=False, encoding='utf-8') as tmp:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
    os.replace(tmp.name, target)
    
    db = load_signatures(target)
    return {"version": db.version, "rules": len(db.rules), "hashes": len(db.hashes_sha256), "path": str(target)}
