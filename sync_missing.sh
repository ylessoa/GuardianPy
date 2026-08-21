#!/bin/bash
# Script para sincronizar archivos faltantes desde origin/main

echo "🔄 Sincronizando archivos faltantes desde origin/main..."

git fetch origin

git checkout origin/main -- \
guardianpy/core/sql_monitor.py \
guardianpy/core/system_monitor.py \
url_checker.py \
tests/test_system_monitor.py \
tests/tests_scanner.py \
tests/test_config.py \
tests/test_quarantine.py \
verify_guardianpy.py \
rules/eicar.yar \
signatures/signatures.json

echo "✅ Sincronización completada. Revisa que los archivos estén presentes."
echo "Ahora puedes ejecutar: python -m guardianpy.services.resident"
