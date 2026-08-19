from __future__ import annotations
import psutil
from .models import ProcessFinding

# Procesos de oficina y navegadores que NO deberían lanzar consolas
PARENT_TARGETS = {
    "winword.exe", "excel.exe", "powerpnt.exe", "outlook.exe",
    "chrome.exe", "msedge.exe", "firefox.exe", "acrobat.exe"
}

# Procesos hijos que indican explotación o shell inmediato
SUSPICIOUS_CHILDREN = {
    "cmd.exe", "powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe"
}

def detect_crawler_behavior() -> list[ProcessFinding]:
    """Detecta procesos que están haciendo muchas peticiones de red (comportamiento crawler/bot)."""
    findings: list[ProcessFinding] = []
    CRAWLER_CONNECTION_THRESHOLD = 50
    
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            connections = proc.net_connections(kind="inet")
            active_remote_conns = [
                c for c in connections 
                if c.status == psutil.CONN_ESTABLISHED and c.raddr
            ]
            if len(active_remote_conns) > CRAWLER_CONNECTION_THRESHOLD:
                findings.append(
                    ProcessFinding(
                        pid=int(proc.info["pid"]),
                        name=proc.info.get("name") or "unknown",
                        severity="high",
                        reason=f"Posible Crawler/Bot detectado: {len(active_remote_conns)} conexiones remotas activas simultáneas.",
                        rss_mb=0.0,
                        cpu_percent=0.0,
                        connections=len(active_remote_conns),
                    )
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return findings

def detect_exploit_behavior() -> list[ProcessFinding]:
    findings: list[ProcessFinding] = []
    for proc in psutil.process_iter(["pid", "name", "ppid"]):
        try:
            info = proc.info
            proc_name = (info.get("name") or "unknown").lower()
            if proc_name in SUSPICIOUS_CHILDREN:
                ppid = info.get("ppid")
                if ppid:
                    try:
                        parent = psutil.Process(ppid)
                        parent_name = parent.name().lower()
                        if parent_name in PARENT_TARGETS:
                            findings.append(
                                ProcessFinding(
                                    pid=proc.pid,
                                    name=proc_name,
                                    severity="high",
                                    reason=f"Suspicious child {proc_name} with parent {parent_name}"
                                )
                            )
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return findings

def detect_memory_misuse(memory_mb_threshold: float = 1024, cpu_threshold: float = 85, max_connections: int = 80) -> list[ProcessFinding]:
    findings: list[ProcessFinding] = []
    psutil.cpu_percent(None)
    
    for proc in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent"]):
        try:
            info = proc.info
            mem_info = info.get("memory_info")
            rss_mb = (mem_info.rss / (1024 * 1024)) if mem_info else 0.0
            cpu = float(info.get("cpu_percent") or 0.0)
            conns = len(proc.net_connections(kind="inet"))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
        
        reasons = []
        severity = "low"
        if rss_mb >= memory_mb_threshold:
            reasons.append(f"High memory usage: {rss_mb:.1f} MB")
            severity = "medium"
        if cpu >= cpu_threshold:
            reasons.append(f"High CPU usage: {cpu:.1f}%")
            severity = "medium"
        if conns >= max_connections:
            reasons.append(f"Unusually many network connections: {conns}")
            severity = "high"
            
        if reasons:
            findings.append(
                ProcessFinding(
                    pid=int(info["pid"]),
                    name=info.get("name") or "unknown",
                    severity=severity,
                    reason="; ".join(reasons),
                    rss_mb=rss_mb,
                    cpu_percent=cpu,
                    connections=conns,
                )
            )
    return sorted(findings, key=lambda f: (f.severity, f.rss_mb), reverse=True)

def terminate_process(pid: int) -> bool:
    """Intenta matar un proceso de forma agresiva."""
    try:
        proc = psutil.Process(pid)
        proc.kill()
        proc.wait(timeout=3)
        return True
    except psutil.NoSuchProcess:
        return False
    except psutil.AccessDenied:
        return False
    except Exception:
        return False
