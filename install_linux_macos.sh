#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
echo "GuardianX instalado. Ejecuta:"
echo "  guardianx-gui"
echo "  guardianx full ~/Downloads"
echo "  guardianx resident --once"
echo "Para modo residente continuo: nohup guardianx resident >/tmp/guardianx.log 2>&1 &"
