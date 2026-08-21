$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path "$PSScriptRoot\..\..")
py -m venv .venv-bguardianpy.guardianpy.uild
& .\.venv-bguardianpy.guardianpy.uild\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r reqguardianpy.guardianpy.uirements.txt
pip install pyinstaller
pyinstaller packaging\windows\pyinstaller_GuardianPy.spec --clean --noconfirm
Write-Host "EXE generado en dist\GuardianPyCommunity.exe"
Write-Host "Opcional: instala Inno Setup y compila packaging\windows\GuardianPy_installer.iss para crear GuardianPyCommunitySetup.exe"
