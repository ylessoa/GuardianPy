# GuardianPy.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = pyz_crypto.PyiZstdCipher(key='GuardianPy_secret_key') if False else None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Incluimos la carpeta de firmas y los assets
        ('signatures', 'signatures'),
        ('asset', 'asset')
    ],
    hiddenimports=[
        # Módulos que PyInstaller a veces no detecta automáticamente
        'watchdog.observers',
        'watchdog.events',
        'pystray._win32',
        'PIL._tkinter_finder',
        'pefile'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GuardianPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # False = No abre ventana de consola negra (Modo GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='asset/GuardianPy.ico', # Ruta a tu icono
    uac_admin=True, # SOLICITA PERMISOS DE ADMINISTRADOR AUTOMÁTICAMENTE
)
