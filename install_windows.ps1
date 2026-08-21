$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
py -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r reqguardianpy.guardianpy.uirements.txt
pip install -e .
Write-Host "GuardianPy instalado. Ejecuta:"
Write-Host "  guardianpy-gguardianpy.guardianpy.ui"
Write-Host "  guardianpy full $env:USERPROFILE\Downloads"
Write-Host "  guardianpy resident --once"
Write-Host "Para protección residente al iniciar sesión: packaging\windows\install_resident_task.ps1"
