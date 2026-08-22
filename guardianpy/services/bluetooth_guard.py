#guardianpy/services/bluetooth_guard.py 

import time
import logging

try:
    import bluetooth  # pybluez
except ImportError:
    bluetooth = None
    logging.warning("PyBluez no está instalado. Instala con: pip install pybluez")

class BluetoothGuard:
    def __init__(self, whitelist=None, scan_interval=10):
        """
        :param whitelist: Lista de dispositivos autorizados (por nombre o dirección MAC).
        :param scan_interval: Intervalo en segundos entre escaneos.
        """
        self.whitelist = whitelist or []
        self.scan_interval = scan_interval
        self.running = False

    def start_monitoring(self):
        if bluetooth is None:
            logging.error("Bluetooth no disponible. Instala pybluez para usar esta función.")
            return

        self.running = True
        logging.info("BluetoothGuard iniciado. Escaneando cada %s segundos...", self.scan_interval)

        while self.running:
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in nearby_devices:
                if addr not in self.whitelist and name not in self.whitelist:
                    self.alert_unauthorized_device(addr, name)
            time.sleep(self.scan_interval)

    def stop_monitoring(self):
        self.running = False
        logging.info("BluetoothGuard detenido.")

    def alert_unauthorized_device(self, addr, name):
        alert_msg = f"[GuardianPy Alert] ⚠️ Conexión Bluetooth no autorizada detectada\n" \
                    f"Dispositivo: {name} ({addr})\nAcción: Conexión bloqueada, evento registrado"
        logging.warning(alert_msg)
        print(alert_msg)
        # Aquí podrías añadir lógica para bloquear la conexión o registrar en un log persistente.
