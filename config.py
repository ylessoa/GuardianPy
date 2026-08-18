from __future__ import annotations
import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path

APP_NAME = "GuardianX"
APP_EDITION = "Community"
APP_ID = "guardianx-community"
DEFAULT_UPDATE_URL = "https://raw.githubusercontent.com/ylessoa/guardianx/main/signatures/signatures.json"
# core/config.py (Dentro de la clase AppConfig)

@dataclass(slots=True)
class AppConfig:
    realtime_enabled: bool = True
    watch_paths: list[str] | None = None
    scan_interval_seconds: int = 60
    memory_mb_threshold: float = 1024
    cpu_threshold: float = 85
    max_connections: int = 80
    signature_update_url: str = DEFAULT_UPDATE_URL
    vt_api_key: str = "" # NUEVO CAMPO
    auto_quarantine: bool = False
    
def app_data_dir() -> Path:
    base = Path.home() / ".guardianx"
    base.mkdir(parents=True, exist_ok=True)
    return base

def normalized_watch_paths(self) -> list[str]:
        if self.watch_paths:
            return self.watch_paths
        return [str(Path.home() / "Downloads"), str(Path.home() / "Desktop")]

def config_path() -> Path:
    return app_data_dir() / "config.json"

def load_config() -> AppConfig:
    path = config_path()
    if not path.exists():
        cfg = AppConfig()
        save_config(cfg)
        return cfg
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return AppConfig(**{k: v for k, v in data.items() if k in AppConfig.__dataclass_fields__})
    except Exception as e:
        logging.warning(f"Archivo de configuración corrupto ({path}). Usando valores por defecto. Error: {e}")
        return AppConfig()

def save_config(config: AppConfig) -> None:
    config_path().write_text(json.dumps(asdict(config), indent=2, ensure_ascii=False), encoding="utf-8")
