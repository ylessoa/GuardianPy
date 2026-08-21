from pathlib import Path
from unittest.mock import patch
from guardianpy.core.config import load_config, AppConfig

def test_load_corrupted_config(tmp_path: Path):
    fake_config_path = tmp_path / "config.json"
    fake_config_path.write_text("{ este no es un json valido }")
    with patch('guardianpy.core.config.config_path', return_value=fake_config_path):
        cfg = load_config()
    assert isinstance(cfg, AppConfig)
    assert cfg.realtime_enabled == True
