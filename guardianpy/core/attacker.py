#guardianpy/core/attacker.py
import psutil

def identify_attacker(file_path: str) -> dict:
    """
    Intenta identificar el proceso que abrió/modificó un archivo crítico.
    Devuelve PID, nombre de proceso, usuario e IP remota si existe.
    """
    for proc in psutil.process_iter(["pid", "name", "username"]):
        try:
            # Revisar archivos abiertos por el proceso
            for f in proc.open_files() or []:
                if f.path == file_path:
                    attacker_info = {
                        "pid": proc.info["pid"],
                        "process": proc.info.get("name", "unknown"),
                        "user": proc.info.get("username", "unknown"),
                        "remote_ip": None,
                        "remote_port": None
                    }

                    # Revisar conexiones de red del proceso
                    for c in proc.connections(kind="inet"):
                        if c.raddr:  # conexión remota activa
                            attacker_info["remote_ip"] = c.raddr.ip
                            attacker_info["remote_port"] = c.raddr.port
                            break

                    return attacker_info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Si no se encontró proceso sospechoso
    return {
        "pid": None,
        "process": None,
        "user": None,
        "remote_ip": None,
        "remote_port": None
    }
