$ErrorActionPreference = "Stop"
Set-Location (Resolve-Path "$PSScriptRoot\..\..")
py -m venv .venv-build
& .\.venv-build\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller packaging\windows\pyinstaller_GuardianPy.spec --clean --noconfirm
Write-Host "EXE generado en dist\GuardianPyCommunity.exe"
Write-Host "Opcional: instala Inno Setup y compila packaging\windows\GuardianPy_installer.iss para crear GuardianXCommunitySetup.exe"
