import time
from guardianpy.core.realtime_monitor import RealtimeMonitor

def main():
    # Crear monitor con intervalo de 30 segundos
    monitor = RealtimeMonitor(interval=30)
    monitor.start()

    print("🛡️ GuardianPy monitor residente iniciado. Presiona Ctrl+C para detener.")

    try:
        # Mantener el proceso vivo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo GuardianPy...")
        monitor.stop()

if __name__ == "__main__":
    main()
