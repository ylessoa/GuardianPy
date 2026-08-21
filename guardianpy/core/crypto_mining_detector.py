# guardianpy/core/crypto_mining_detector.py

import psutil
import logging

class CryptoMiningDetector:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("GuardianPy")

    def scan_processes(self):
        suspicious = []
        for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "connections"]):
            try:
                info = proc.info

                # Regla 1: CPU sostenida alta
                if info.get("cpu_percent", 0) > 80:
                    suspicious.append(info)

                # Regla 2: nombre sospechoso
                if info.get("name", "").lower() in ["xmrig", "minerd", "ethminer"]:
                    suspicious.append(info)

                # Regla 3: conexiones a puertos típicos de minería
                for conn in proc.connections(kind="inet"):
                    if conn.laddr and conn.laddr.port in [3333, 4444, 5555, 7777]:
                        suspicious.append(info)

            except Exception:
                continue

        if suspicious:
            self.logger.critical(f"⚠️ Minería no autorizada detectada: {suspicious}")
        return suspicious
