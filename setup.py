import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
executables = [
    Executable('main.py', base=base)
]

build_options = {'build_exe': {'include_files':['character', 'enemies', 'levels', 'objects', 'sprites']}}

results = setup(name='Run And Gun',
      version='0.1',
      description='Shooter Game Engine',
      options = build_options,
      executables=executables
      )

print('done:', results)
