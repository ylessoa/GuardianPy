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
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.core\.logger' 'from guardianpy.guardianpy.core.logger' *.py
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.core\.realtime_monitor' 'from guardianpy.guardianpy.core.realtime_monitor' *.py
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.ui\.tk_app' 'from guardianpy.guardianpy.ui.tk_app' *.py
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.core\.scanner' 'from guardianpy.guardianpy.core.scanner' *.py
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.core\.signatures' 'from guardianpy.guardianpy.core.signatures' *.py
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.core\.quarantine' 'from guardianpy.guardianpy.core.quarantine' *.py
Replace-TextInFiles 'from guardianpy\.guardianpy.guardianpy.core\.updater' 'from guardianpy.guardianpy.core.updater' *.py
Replace-TextInFiles 'from Guardianpy\.guardianpy.guardianpy.core\.config' 'from guardianpy.guardianpy.core.config' *.py
Replace-TextInFiles 'from Guardianpy\.guardianpy.guardianpy.core\.logger' 'from guardianpy.guardianpy.core.logger' *.py

# Archivos Markdown (.md)
Replace-TextInFiles 'guardianpy' 'guardianpy' *.md
Replace-TextInFiles 'guardianpy' 'guardianpy' *.md

# Scripts PowerShell (.ps1)
Replace-TextInFiles 'guardianpy' 'guardianpy' *.ps1
Replace-TextInFiles 'guardianpy' 'guardianpy' *.ps1

# Scripts Bash (.sh)
Replace-TextInFiles 'guardianpy' 'guardianpy' *.sh
Replace-TextInFiles 'guardianpy' 'guardianpy' *.sh

Write-Host "✅ Todas las referencias a guardianx han sido reemplazadas por guardianpy "

