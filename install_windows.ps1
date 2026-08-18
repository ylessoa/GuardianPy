$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
py -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Write-Host "GuardianX instalado. Ejecuta:"
Write-Host "  guardianx-gui"
Write-Host "  guardianx full $env:USERPROFILE\Downloads"
Write-Host "  guardianx resident --once"
Write-Host "Para protección residente al iniciar sesión: packaging\windows\install_resident_task.ps1"
