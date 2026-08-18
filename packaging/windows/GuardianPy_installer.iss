; Inno Setup script. Build after PyInstaller creates dist\GuardianXCommunity.exe.
#define MyAppName "GuardianPy Community"
#define MyAppVersion "0.2.0"
#define MyAppPublisher "GuardianPy Community"
#define MyAppExeName "GuardianXCommunity.exe"

[Setup]
AppId={{A7D353D9-4D8B-4965-A09D-GUARDIANX02}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\GuardianX Community
DefaultGroupName=GuardianPy Community
AllowNoIcons=yes
LicenseFile=..\..\LICENSE
OutputDir=..\..\dist-installer
OutputBaseFilename=GuardianXCommunitySetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear icono en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked

[Files]
Source: "..\..\dist\GuardianPyCommunity.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\signatures\signatures.json"; DestDir: "{app}\signatures"; Flags: ignoreversion
Source: "..\..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\GuardianPy Community"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\GuardianPy Community"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar GuardianPy Community"; Flags: nowait postinstall skipifsilent
