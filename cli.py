from __future__ import annotations
import argparse
from pathlib import Path
from core.hardening import audit_hardening
from core.events import read_recent_events
from core.updater import active_signature_path, update_signatures
from core.ports import audit_open_ports
from core.process_monitor import detect_memory_misuse
from core.quarantine import QuarantineManager
from core.scanner import scan_paths
from core.logger import setup_logging

def _print_rows(title: str, rows: list) -> None:
    print(f"\n=== {title} ===")
    if not rows:
        print("Sin hallazgos.")
        return
    for item in rows:
        print(item)

def main(argv: list[str] | None = None) -> int:
    setup_logging(log_to_file=False)
    parser = argparse.ArgumentParser(description="GuardianPy defensive antimalware prototype")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    scan = sub.add_parser("scan", help="Scan files/directories for signatures and heuristics")
    scan.add_argument("paths", nargs="+", help="Files or directories to scan")
    scan.add_argument("--quarantine", action="store_true", help="Move detected files into quarantine vault")
    scan.add_argument("--max-file-mb", type=int, default=100)
    
    sub.add_parser("monitor", help="Detect suspicious memory/CPU/network process usage")
    sub.add_parser("ports", help="Audit risky listening ports")
    sub.add_parser("harden", help="Show baseline hardening recommendations")
    sub.add_parser("events", help="Show recent resident guard events")
    
    upd = sub.add_parser("update", help="Update malware signatures from HTTPS JSON feed")
    upd.add_argument("--url", default=None, help="Override signature update URL")
    
    svc = sub.add_parser("resident", help="Run resident background protection loop")
    svc.add_argument("--once", action="store_true", help="Run one cycle and exit")
    
    full = sub.add_parser("full", help="Run scan + process + port + hardening audit")
    full.add_argument("paths", nargs="*", default=[str(Path.home())])
    
    args = parser.parse_args(argv)
    
    if args.cmd == "scan":
        findings = scan_paths(args.paths, max_file_mb=args.max_file_mb)
        _print_rows("Amenazas detectadas", findings)
        if args.quarantine and findings:
            qm = QuarantineManager()
            for finding in findings:
                try:
                    dst = qm.quarantine(finding)
                    print(f"Encapsulado: {finding.path} -> {dst}")
                except Exception as exc:
                    print(f"No se pudo encapsular {finding.path}: {exc}")
        return 2 if findings else 0
        
    if args.cmd == "monitor":
        _print_rows("Procesos sospechosos por memoria/CPU/red", detect_memory_misuse())
        return 0
        
    if args.cmd == "ports":
        _print_rows("Puertos riesgosos abiertos", audit_open_ports())
        return 0
        
    if args.cmd == "harden":
        _print_rows("Cierre de brechas / hardening", audit_hardening())
        return 0
        
    if args.cmd == "events":
        _print_rows("Eventos recientes", read_recent_events())
        return 0
        
    if args.cmd == "update":
        try:
            result = update_signatures(args.url) if args.url else update_signatures()
            print(f"Firmas actualizadas: v{result['version']} ({result['rules']} reglas, {result['hashes']} hashes) -> {result['path']}")
        except Exception as e:
            print(f"Error actualizando firmas: {e}")
            return 1
        return 0
        
    if args.cmd == "resident":
        from GuardianPy.services.resident import main as resident_main
        return resident_main(["--once"] if args.once else [])
        
    if args.cmd == "full":
        _print_rows("Amenazas detectadas", scan_paths(args.paths))
        _print_rows("Procesos sospechosos", detect_memory_misuse())
        _print_rows("Puertos riesgosos abiertos", audit_open_ports())
        _print_rows("Hardening", audit_hardening())
        return 0
        
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
