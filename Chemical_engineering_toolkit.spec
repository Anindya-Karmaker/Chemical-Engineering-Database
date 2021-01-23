# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Chemical_engineering_toolkit.py'],
             pathex=['C:\\Users\\AnindyaJV\\Desktop\\MOOC\\PYTHON LEARNING\\CHEM ENG TOOLKIT\\FINAL'],
             binaries=[],
             datas=[('Master.db', '.'),('icon.ico', '.'),('iapws','iapws')],
             hiddenimports=['iapws'],
             hookspath=[],
             runtime_hooks=[],
excludes=['matplotlib','cryptography','cryptography-2.9.2-py3.7.egg-info','importlib_metadata-1.7.0-py3.7.egg-info','jsonschema','jsonschema-3.2.0-py3.7.egg-info','importlib_metadata-1.7.0-py3.7.egg-info','gevent-20.6.2-py3.7.egg-info','gevent','matplotlib','notebook','PyQt5',
'zope','alabaster','babel','bcrypt','brotli','certifi','docutils','etc','jedi','lib2to3','lxml','matplotlib','nacl','nbconvert','nbconvert-5.6.1-py3.7.egg-info','nbformat','notebook','psutil','PyQt5','pytz','sphinx','tornado','typed_ast','zmq','zope'],
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
          name='Chemical_engineering_toolkit',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
