from __future__ import annotations

import os
import platform
import shutil
import subprocess

from .models import HardeningFinding


def _cmd_exists(name: str) -> bool:
    return shutil.which(name) is not None


def audit_hardening() -> list[HardeningFinding]:
    system = platform.system().lower()
    findings: list[HardeningFinding] = []
    if system == "linux":
        if _cmd_exists("ufw"):
            try:
                out = subprocess.run(["ufw", "status"], capture_output=True, text=True, timeout=3).stdout.lower()
                active = "status: active" in out
            except Exception:
                active = False
            findings.append(HardeningFinding("Firewall", "high" if not active else "info", "OK" if active else "Needs attention", "Enable UFW: sudo ufw enable"))
        else:
            findings.append(HardeningFinding("Firewall", "medium", "Unknown", "Install/configure ufw, firewalld, or nftables policy."))
        findings.append(HardeningFinding("Updates", "medium", "Manual check", "Keep OS packages patched: sudo apt update && sudo apt upgrade (or distro equivalent)."))
        if os.geteuid() == 0:
            findings.append(HardeningFinding("Privileges", "medium", "Running as root", "Use a standard user for daily work and elevate only when needed."))
    elif system == "windows":
        findings.append(HardeningFinding("Firewall", "high", "Manual check", "Verify Microsoft Defender Firewall is enabled for Domain/Private/Public profiles."))
        findings.append(HardeningFinding("RDP", "medium", "Manual check", "Disable RDP if unused; otherwise require NLA, VPN, MFA and firewall allowlists."))
        findings.append(HardeningFinding("Updates", "medium", "Manual check", "Enable automatic Windows Update and application updates."))
    else:
        findings.append(HardeningFinding("Baseline", "medium", "Manual check", "Enable firewall, automatic updates, disk encryption and least-privilege accounts."))
    return findings
