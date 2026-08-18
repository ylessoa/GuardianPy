# PyInstaller spec for GuardianPy Community.
# Build on Windows for a native .exe:
#   pip install pyinstaller pillow
#   pyinstaller packaging/windows/pyinstaller_GuardianPy.spec --clean --noconfirm

from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
root = Path.cwd()

a = Analysis(
    ['run_gui.py'],
    pathex=[str(root)],
    binaries=[],
    datas=[('signatures', 'signatures'), ('GuardianPy/assets', 'GuardianPy/assets')],
    hiddenimports=['psutil'],
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
    name='GuardianPyCommunity',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
