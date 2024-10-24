# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/j2live.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/martingeorge/Documents/Git/Personal/J2Live/venv/lib/python3.12/site-packages/nicegui', 'nicegui')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='J2Live',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['j2live.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='J2Live',
)
app = BUNDLE(
    coll,
    name='J2Live.app',
    icon='j2live.icns',
    bundle_identifier='dingo.j2live',
)
