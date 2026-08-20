# setup_guardianpy.ps1
Set-Location "$env:USERPROFILE\GuardianPy"

if (-Not (Test-Path ".venv")) {
    python -m venv .venv
}

.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

pip install psutil==6.1.0 `
            requests==2.32.3 `
            yara-python==4.5.4 `
            pytest==9.1.1 `
            colorama==0.4.6 `
            cryptography==43.0.1 `
            pyinstaller==6.10.0 `
            watchdog==4.0.1

pip list
