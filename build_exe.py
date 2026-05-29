"""
考研复习系统 —— PyInstaller 打包脚本
用法: python build_exe.py
"""

import os
import sys
import shutil

ROOT = os.path.abspath(os.path.dirname(__file__))

for d in ['build', 'dist']:
    shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)

sep = os.pathsep

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--name', 'ReviewSystem',
    '--onedir',
    '--windowed',
    '--add-data', f'database/subjects.json{sep}database',
    '--add-data', f'app/templates{sep}app/templates',
    '--add-data', f'app/static{sep}app/static',
    '--exclude-module', 'setuptools',
    '--exclude-module', 'pkg_resources',
    '--exclude-module', 'numpy',
    '--hidden-import', 'app.config',
    '--hidden-import', '_cffi_backend',
    '--collect-all', 'cffi',
    '--collect-submodules', 'webview',
    '--collect-submodules', 'flask_sqlalchemy',
    '--collect-submodules', 'flask',
    'desktop_app.py',
]

print('=' * 60)
print('Building ReviewSystem...')
print('=' * 60)
sys.stdout.flush()

result = os.system(' '.join(cmd))

if result == 0:
    print()
    print('=' * 60)
    print('BUILD SUCCESS!')
    print('=' * 60)
    exe_path = os.path.join(ROOT, 'dist', 'ReviewSystem', 'ReviewSystem.exe')
    print(f'  EXE: {exe_path}')
else:
    print()
    print('BUILD FAILED')
    sys.exit(1)
