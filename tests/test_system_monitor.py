from unittest.mock import patch, MagicMock
from guardianpy.core.sql_monitor import detect_sql_injection  # ejemplo de otro módulo
from guardianpy.core import events
from guardianpy.core.system_monitor import detect_system_slowness

def test_detect_system_slowness_high_cpu(monkeypatch):
    # Simulamos un proceso con alto consumo de CPU
    fake_proc = MagicMock()
    fake_proc.info = {
        "pid": 1234,
        "name": "fake_process",
        "memory_info": MagicMock(rss=200 * 1024 * 1024),  # 200 MB
        "cpu_percent": 95.0,  # CPU muy alto
    }
    fake_proc.net_connections.return_value = []

    # Mockeamos psutil.process_iter para devolver solo este proceso
    monkeypatch.setattr("psutil.process_iter", lambda _: [fake_proc])
    monkeypatch.setattr("psutil.cpu_percent", lambda _: None)

    # Ejecutamos la detección
    result = detect_system_slowness(memory_mb_threshold=100, cpu_threshold=85)

    assert result is True
