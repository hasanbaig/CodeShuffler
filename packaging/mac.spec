import os
import sys
spec_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
repo_root = os.path.abspath(os.path.join(spec_dir, ".."))

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    [os.path.join(repo_root, 'main.py')],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join(repo_root, 'codeshuffler/gui/icons'),
         'codeshuffler/gui/icons'),
    ],
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
    name='CodeShuffler',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    argv_emulation=True,
    bundle_identifier="com.codeshuffler.app",
    icon=os.path.join(
        repo_root,
        'codeshuffler/gui/icons/codeshuffler-icon.icns',
    ),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CodeShuffler',
)
