# Crea una tarea programada para iniciar el guardián residente al iniciar sesión.
$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path "$PSScriptRoot\..\.."
$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Instala primero con install_windows.ps1" }
$Action = New-ScheduledTaskAction -Execute $Python -Argument "-m GuardianPy.service.resident"
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "GuardianPy Resident Guard" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Protección residente GuardianPy Community" -Force
Write-Host "Tarea instalada: GuardianPy Resident Guard"
