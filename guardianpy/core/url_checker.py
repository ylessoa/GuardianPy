"""
url_checker.py
Módulo para detectar enlaces falsos o sospechosos en GuardianPy.
"""

import re
import requests
import logging

logger = logging.getLogger("GuardianPy")

# Lista de patrones sospechosos comunes (puedes ampliarla)
SUSPICIOUS_PATTERNS = [
    "paypa1", "micros0ft", "login-verify", "secure-update", "banking-check"
]

def is_url_valid(url: str) -> bool:
    """
    Verifica si la URL tiene un formato válido (http/https).
    """
    return bool(re.match(r"^https?://", url))


def is_url_suspicious(url: str) -> tuple[bool, str]:
    """
    Aplica heurísticas simples para detectar enlaces sospechosos.
    Devuelve (True, razón) si el enlace parece peligroso.
    """
    if not is_url_valid(url):
        return True, "Formato inválido o protocolo no seguro"

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in url.lower():
            return True, f"Patrón sospechoso detectado: {pattern}"

    return False, "Seguro"


def check_with_safe_browsing(url: str, api_key: str | None = None) -> tuple[bool, str]:
    """
    Consulta la API de Google Safe Browsing para verificar si la URL está reportada.
    Requiere un api_key válido.
    """
    if not api_key:
        return False, "Sin verificación externa (API key no configurada)"

    endpoint = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    payload = {
        "client": {"clientId": "guardianpy", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        response = requests.post(f"{endpoint}?key={api_key}", json=payload, timeout=5)
        data = response.json()
        if data.get("matches"):
            return True, "Reportado como malicioso en Safe Browsing"
        return False, "No reportado en Safe Browsing"
    except Exception as e:
        logger.error(f"Error consultando Safe Browsing: {e}")
        return False, "Error en verificación externa"


def analyze_url(url: str, api_key: str | None = None) -> tuple[bool, str]:
    """
    Función principal: combina heurísticas locales y verificación externa.
    """
    suspicious, reason = is_url_suspicious(url)
    if suspicious:
        return True, reason

    external_suspicious, external_reason = check_with_safe_browsing(url, api_key)
    if external_suspicious:
        return True, external_reason

    return False, "Enlace seguro"
