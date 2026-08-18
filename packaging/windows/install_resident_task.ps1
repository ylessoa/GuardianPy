# Crea una tarea programada para iniciar el guardián residente al iniciar sesión.
$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path "$PSScriptRoot\..\.."
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Instala primero con install_windows.ps1" }
$Action = New-ScheduledTaskAction -Execute $Python -Argument "-m guardianx.service.resident"
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "GuardianX Resident Guard" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Protección residente GuardianX Community" -Force
Write-Host "Tarea instalada: GuardianX Resident Guard"
