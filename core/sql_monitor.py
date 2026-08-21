import re
from guardianpy.core import events

# Patrones básicos de SQL Injection
SQLI_PATTERNS = [
    r"(?i)\bunion\b\s+\bselect\b",
    r"(?i)\bor\b\s+1=1",
    r"(?i)\band\b\s+1=1",
    r"(?i)--",
    r"(?i)/\*.*\*/",
    r"(?i)\bxp_cmdshell\b",
    r"(?i)\bsleep\(",
    r"(?i)\bbenchmark\(",
]

def detect_sql_injection(query: str) -> bool:
    """Detecta si una consulta SQL contiene patrones sospechosos."""
    for pattern in SQLI_PATTERNS:
        if re.search(pattern, query):
            # Registrar evento de seguridad
            events.log_security_event(
                source="sql_monitor",
                description=f"Posible SQL Injection detectado en consulta: {query}"
            )
            return True
    return False

def sanitize_query(query: str) -> str:
    """Ejemplo simple de sanitización: elimina comentarios y normaliza espacios."""
    query = re.sub(r"--.*", "", query)  # elimina comentarios tipo --
    query = re.sub(r"/\*.*?\*/", "", query)  # elimina comentarios tipo /* */
    return " ".join(query.split())
