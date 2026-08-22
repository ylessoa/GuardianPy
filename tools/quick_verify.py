#tools/quick_verify.py
import json
from pathlib import Path

def quick_verify_events(log_path="events.jsonl"):
    path = Path(log_path)
    if not path.exists():
        print(f"No se encontró el archivo {log_path}")
        return

    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            try:
                event = json.loads(line)
                metadata = event.get("metadata", {})
                file = metadata.get("file")
                attacker = metadata.get("attacker")
                system_state = metadata.get("system_state")

                print("=" * 60)
                print(f"Archivo crítico: {file}")
                print(f"Attacker: {json.dumps(attacker, indent=2, ensure_ascii=False)}")
                print(f"System State: {json.dumps(system_state, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    quick_verify_events("events.jsonl")
