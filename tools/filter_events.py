import json
from pathlib import Path

def filter_events_with_attacker_and_system_state(log_path="events.jsonl"):
    """
    Lee events.jsonl y devuelve solo los eventos que contienen
    simultáneamente 'attacker' y 'system_state' en metadata.
    """
    path = Path(log_path)
    if not path.exists():
        print(f"No se encontró el archivo {log_path}")
        return []

    filtered = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            try:
                event = json.loads(line)
                metadata = event.get("metadata", {})
                if "attacker" in metadata and "system_state" in metadata:
                    filtered.append(event)
            except json.JSONDecodeError:
                continue

    return filtered


if __name__ == "__main__":
    events = filter_events_with_attacker_and_system_state("events.jsonl")
    print(f"Se encontraron {len(events)} eventos con attacker + system_state:")
    for ev in events:
        print(json.dumps(ev, indent=2, ensure_ascii=False))
