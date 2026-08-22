#guardianpy/core/actor.py
import random
import getpass

def simulate_actor(action: str):
    """
    Devuelve información simulada del actor que realizó la acción.
    """
    users = [
        "jose.gomez@empresa.com",
        "ana.perez@empresa.com",
        "carlos.ruiz@empresa.com",
        "maria.lopez@empresa.com"
    ]
    ips = ["192.168.1.45", "203.0.113.77", "10.0.0.42", "172.16.0.5"]

    return {
        "user": random.choice(users),
        "action": action,
        "timestamp": None,  # se llenará en log_security_event con datetime.now()
        "ip": random.choice(ips),
        "local_user": getpass.getuser()  # usuario local del sistema
    }
