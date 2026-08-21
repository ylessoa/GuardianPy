import psutil
from guardianpy.core import events

def detect_system_slowness(
    memory_mb_threshold: float = 1024,
    cpu_threshold: float = 85,
    max_connections: int = 80
):
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
            description=f"⚠️ Rendimiento lento detectado. Proceso {top['name']} (PID {top['pid']}) consume {top['cpu_percent']}% CPU y {top['rss_mb']:.1f} MB de memoria."
        )
        return True
    return False
