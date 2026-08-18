Firmas GuardianPy
El archivo de firmas es JSON y contiene:

hashes\_sha256: hash -> nombre de detección.
rules: reglas heurísticas basadas en términos.
risky\_ports: puertos que elevan superficie de ataque.
Actualizar firmas
bash
GuardianPy update
Por defecto descarga desde:

text
https://raw.githubusercontent.com/ylessoa/GuardianPy/main/signatures/signatures.json
Puedes cambiar el origen:

bash
GuardianPy update --url https://tu-servidor/signatures.json
La edición Community valida estructura JSON. Para producción empresarial se recomienda añadir firma criptográfica detached.

