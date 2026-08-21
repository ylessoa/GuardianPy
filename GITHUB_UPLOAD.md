Subir GuardianPy Community a GitHub
No puedo empujar directamente a https://github.com/ylessoa sin autenticación de GitHub, pero el repositorio está listo.

bash 
git init
git add .
git commit -m "GuardianPy Community 0.2"
git branch -M main
git remote add origin https://github.com/ylessoa/guardianpy.git
git push -u origin main
Crear release descargable
En Windows:

powershell 
packaging\windows\bguardianpy.guardianpy.uild_windows.ps1
Luego adjunta dist\GuardianPyCommunity.exe y, si usas Inno Setup, dist-installer\GuardianPyCommunitySetup.exe.
