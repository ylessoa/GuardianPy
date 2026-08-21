# guardianpy/core/system_monitor.py
import psutil
from guardianpy.core import events

def detect_network_anomalies(conn_threshold: int = 100):
    """
    Detector de anomalías de red (stub temporal).
    Devuelve una lista vacía o simulada de anomalías de red.
    """
    return []


def detect_system_slowness(
    memory_mb_threshold: float = 1024,
    cpu_threshold: float = 85,
    max_connections: int = 80
) -> bool:
    """
    Detecta procesos que causan lentitud en el sistema por alto consumo de CPU,
    memoria o conexiones de red.
    Registra un evento de seguridad si se encuentra algún culpable.
    """
    findings = []
    psutil.cpu_percent(None)  # inicializa medición

    for proc in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent"]):
        try:
            info = proc.info
            mem_info = info.get("memory_info")
            rss_mb = (mem_info.rss / (1024 * 1024)) if mem_info else 0.0
            cpu = float(info.get("cpu_percent") or 0.0)
            conns = len(proc.net_connections(kind="inet"))

            if rss_mb >= memory_mb_threshold or cpu >= cpu_threshold or conns >= max_connections:
                findings.append({
                    "pid": info["pid"],
                    "name": info.get("name") or "unknown",
                    "rss_mb": rss_mb,
                    "cpu_percent": cpu,
                    "connections": conns
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if findings:
        top = max(findings, key=lambda f: (f["cpu_percent"], f["rss_mb"]))
        events.log_security_event(
            source="system_monitor",
            description=(
                f"⚠️ Rendimiento lento detectado. "
                f"Proceso {top['name']} (PID {top['pid']}) consume "
                f"{top['cpu_percent']}% CPU y {top['rss_mb']:.1f} MB de memoria."
            )
        )
        return True

    return False
