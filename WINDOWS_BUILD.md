Crear .exe e instalador Windows
GuardianPy incluye los scripts para producir un .exe real en Windows.

Requisitos
Windows 10/11.
Python 3.10+.
Opcional para instalador: Inno Setup.
EXE portable
powershell
cd GuardianPy
packaging\\windows\\build\_windows.ps1
Salida esperada:

text
dist\\GuardianPyCommunity.exe
Instalador .exe
Instala Inno Setup.
Ejecuta primero build\_windows.ps1.
Abre y compila:
text
packaging\\windows\\GuardianPy\_installer.iss
Salida:

text
dist-installer\\GuardianPyCommunitySetup.exe
Servicio residente
Para activar el guardián residente al iniciar sesión:

powershell
.\\install\_windows.ps1
packaging\\windows\\install\_resident\_task.ps1
Esto crea una tarea programada llamada GuardianPy Resident Guard.

