# fix_imports.ps1
# Script para corregir imports en GuardianPy

# 1. Ir al directorio del proyecto (ajusta si es necesario)
Set-Location "$env:USERPROFILE\GuardianPy"

# 2. Buscar todos los archivos .py y aplicar reemplazos
Get-ChildItem -Recurse -Include *.py | ForEach-Object {
    (Get-Content $_.FullName) `
    -replace 'guardianx\.', 'core.' `
    -replace 'GuardianPy\.', 'core.' |
    Set-Content $_.FullName
}

Write-Host "✅ Corrección de imports completada en todos los archivos .py"
