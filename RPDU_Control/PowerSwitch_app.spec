# -*- mode: python ; coding: utf-8 -*-
import os
block_cipher = None

current_wd = os.getcwd()
a = Analysis(['PowerSwitch_app.pyw'],
             pathex=[current_wd],
             binaries=[],
             datas=[('app.ico', '.'), ('PowerSwitchList.json', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PowerSwitch_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='app.ico')
