# core/threat_intel.py
import requests
import logging
import time

class ThreatIntel:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.log = logging.getLogger("guardianx")
        self.base_url = "https://www.virustotal.com/api/v3/files/"
        # Controlar rate limits (VirusTotal gratis permite 4 peticiones por minuto)
        self.last_request_time = 0 

   # core/threat_intel.py (Reemplazar la función check_hash)

    def check_hash(self, file_hash: str) -> dict:
        if not self.api_key:
            return {"malicious": False, "reason": "No API Key configured"}

        headers = {"x-apikey": self.api_key}
        try:
            response = requests.get(f"{self.base_url}{file_hash}", headers=headers, timeout=3)
            
            # FIX: Si VirusTotal nos limita (429), paramos de consultar la nube para no congelar el PC
            if response.status_code == 429:
                self.log.warning("Límite de peticiones de VirusTotal alcanzado. Omitiendo análisis en la nube por ahora.")
                return {"malicious": False, "reason": "Rate limited"}
                
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious_count = stats.get("malicious", 0)
                suspicious_count = stats.get("suspicious", 0)
                
                if malicious_count > 0:
                    return {"malicious": True, "reason": f"Detectado por {malicious_count} motores en VT"}
                elif suspicious_count > 0:
                    return {"malicious": True, "reason": f"Sospechoso según {suspicious_count} motores en VT"}
                else:
                    return {"malicious": False, "reason": "Limpio en VT"}
            elif response.status_code == 404:
                return {"malicious": False, "reason": "Desconocido para VT"}
            else:
                return {"malicious": False, "reason": "Error de API"}
        except Exception as e:
            self.log.debug(f"Error consultando VT: {e}")
            return {"malicious": False, "reason": "Error de red"}
