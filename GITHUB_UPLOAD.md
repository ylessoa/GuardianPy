Subir GuardianX Community a GitHub
No puedo empujar directamente a https://github.com/ylessoa sin autenticación de GitHub, pero el repositorio está listo.

bash 
git init
git add .
git commit -m "GuardianX Community 0.2"
git branch -M main
git remote add origin https://github.com/ylessoa/guardianx.git
git push -u origin main
Crear release descargable
En Windows:

powershell 
packaging\windows\build_windows.ps1
Luego adjunta dist\GuardianXCommunity.exe y, si usas Inno Setup, dist-installer\GuardianXCommunitySetup.exe.
