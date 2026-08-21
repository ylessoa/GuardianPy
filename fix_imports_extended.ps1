# fix_imports_extended.ps1
# Corrige referencias obsoletas a guardianpy en GuardianPy (Windows/PowerShell)

Write-Host "🔍 Buscando y corrigiendo referencias obsoletas..."

# Función para reemplazar texto en archivos
function Replace-TextInFiles($pattern, $replacement, $fileTypes) {
    Get-ChildItem -Recurse -Include $fileTypes | ForEach-Object {
        (Get-Content $_.FullName) -replace $pattern, $replacement |
            Set-Content $_.FullName
    }
}

# Archivos Python
Replace-TextInFiles 'from guardianpy\.core\.logger' 'from core.logger' *.py
Replace-TextInFiles 'from guardianpy\.core\.realtime_monitor' 'from core.realtime_monitor' *.py
Replace-TextInFiles 'from guardianpy\.ui\.tk_app' 'from ui.tk_app' *.py
Replace-TextInFiles 'from guardianpy\.core\.scanner' 'from core.scanner' *.py
Replace-TextInFiles 'from guardianpy\.core\.signatures' 'from core.signatures' *.py
Replace-TextInFiles 'from guardianpy\.core\.quarantine' 'from core.quarantine' *.py
Replace-TextInFiles 'from guardianpy\.core\.updater' 'from core.updater' *.py
Replace-TextInFiles 'from Guardianpy\.core\.config' 'from core.config' *.py
Replace-TextInFiles 'from Guardianpy\.core\.logger' 'from core.logger' *.py

# Archivos Markdown (.md)
Replace-TextInFiles 'guardianpy' 'guardianpy' *.md
Replace-TextInFiles 'guardianpy' 'Guardianpy' *.md

# Scripts PowerShell (.ps1)
Replace-TextInFiles 'guardianpy' 'guardianpy' *.ps1
Replace-TextInFiles 'guardianpy' 'Guardianpy' *.ps1

# Scripts Bash (.sh)
Replace-TextInFiles 'guardianpy' 'guardianpy' *.sh
Replace-TextInFiles 'guardianpy' 'Guardianpy' *.sh

Write-Host "✅ Todas las referencias a guardianpy han sido reemplazadas por guardianpy"
