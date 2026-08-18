# core/pe_analyzer.py
from __future__ import annotations
import logging
from pathlib import Path
from .models import ThreatFinding

# Funciones de Windows API comúnmente usadas por malware para inyección de procesos, keylogging, etc.
SUSPICIOUS_API_CALLS = {
    "VirtualAllocEx": "Asignación de memoria en proceso externo (Inyección)",
    "WriteProcessMemory": "Escritura en proceso externo (Inyección)",
    "CreateRemoteThread": "Ejecución de hilo en proceso externo (Inyección)",
    "LoadLibraryA": "Carga dinámica de librerías (Técnicas de evasion)",
    "SetWindowsHookExA": "Instalación de hooks (Posible Keylogger o Ransomware)",
    "RegSetValueExA": "Modificación de registro (Persistencia)",
    "InternetOpenA": "Apertura de conexiones HTTP (Posible descarga de payload)",
}

def analyze_pe_file(path: Path, logger: logging.Logger) -> list[ThreatFinding]:
    """Analiza un archivo PE (.exe, .dll) en busca de imports sospechosos."""
    try:
        import pefile
    except ImportError:
        return []

    findings: list[ThreatFinding] = []
    try:
        pe = pefile.PE(str(path), fast_load=True)
        pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
        
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        func_name = imp.name.decode('utf-8', errors='ignore')
                        if func_name in SUSPICIOUS_API_CALLS:
                            reason = SUSPICIOUS_API_CALLS[func_name]
                            findings.append(
                                ThreatFinding(
                                    path=path,
                                    threat=f"Suspicious PE Import: {func_name}",
                                    severity="high",
                                    reason=reason,
                                    metadata={"function": func_name, "dll": entry.dll.decode()}
                                )
                            )
        pe.close()
    except pefile.PEFormatError:
        # No es un archivo PE válido
        pass
    except Exception as e:
        logger.debug(f"Error analizando PE {path}: {e}")
        
    return findings
# core/pe_analyzer.py (Añadir a la función analyze_pe_file)

def analyze_pe_file(path: Path, logger: logging.Logger) -> list[ThreatFinding]:
    # ... (imports y SUSPICIOUS_API_CALLS existentes) ...
    
    findings: list[ThreatFinding] = []
    try:
        import pefile
        pe = pefile.PE(str(path), fast_load=True)
        
        # --- NUEVO: Detección de Contaminación (Overlay/Append) ---
        # Un ejecutable normal termina justo donde dicen sus cabeceras.
        # Si el archivo en disco es más grande que el tamaño declarado en su cabecera PE,
        # significa que alguien le "pegó" datos al final (malware appender o joiner).
        overlay_offset = pe.get_overlay_data_offset()
        file_size = path.stat().st_size
        
        if overlay_offset is not None:
            overlay_size = file_size - overlay_offset
            # Si el overlay es mayor a 10KB, es muy sospechoso
            if overlay_size > 10_240:
                findings.append(
                    ThreatFinding(
                        path=path,
                        threat="Contaminated Executable (Overlay Detected)",
                        severity="high",
                        reason=f"Ejecutable legítimo contaminado con {overlay_size} bytes de datos ocultos al final.",
                        metadata={"overlay_size": overlay_size}
                    )
                )
        pe.close()
        
    except pefile.PEFormatError:
        pass
    except Exception as e:
        logger.debug(f"Error analizando PE {path}: {e}")
        
    return findings
