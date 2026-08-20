#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
echo "GuardianPy instalado. Ejecuta:"
echo "  guardianpy-gui"
echo "  guardianpy full ~/Downloads"
echo "  guardianpy resident --once"
echo "Para modo residente continuo: nohup guardianpy resident >/tmp/guardianpy.log 2>&1 &"
