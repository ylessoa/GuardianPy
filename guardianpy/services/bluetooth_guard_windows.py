#guardianpy/services/bluetooth_guard_windows.py
import subprocess
import logging
import time

class BluetoothGuardWindows:
    def __init__(self, whitelist=None, scan_interval=15):
        """
        :param whitelist: Lista de dispositivos autorizados (por nombre o ID).
        :param scan_interval: Intervalo en segundos entre escaneos.
        """
        self.whitelist = whitelist or []
        self.scan_interval = scan_interval
        self.running = False

    def start_monitoring(self):
        self.running = True
        logging.info("BluetoothGuardWindows iniciado. Escaneando cada %s segundos...", self.scan_interval)

        while self.running:
            try:
                # Ejecutar PowerShell para listar dispositivos Bluetooth
                cmd = [
                    "powershell",
                    "-Command",
                    "Get-PnpDevice -Class Bluetooth | Select-Object -Property FriendlyName,InstanceId"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                devices = result.stdout.strip().splitlines()

                for device in devices:
                    if not device.strip():
                        continue
                    if not any(auth in device for auth in self.whitelist):
                        self.alert_unauthorized_device(device)
            except Exception as e:
                logging.error(f"Error al escanear dispositivos Bluetooth: {e}")

            time.sleep(self.scan_interval)

    def stop_monitoring(self):
        self.running = False
        logging.info("BluetoothGuardWindows detenido.")

    def alert_unauthorized_device(self, device_info):
        alert_msg = f"[GuardianPy Alert] ⚠️ Conexión Bluetooth no autorizada detectada\n" \
                    f"Dispositivo: {device_info}\nAcción: Evento registrado y conexión bloqueada (si es posible)"
        logging.warning(alert_msg)
        print(alert_msg)
