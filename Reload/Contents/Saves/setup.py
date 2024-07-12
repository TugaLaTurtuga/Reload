# setup.py
from setuptools import setup

APP = ['Main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame', 'json', 'os', 'ForderFinder', 'Menus', 'SliderCode', 'Main_menu', 'play_next_song', 'mutagen'],
    'plist': {
        'CFBundleName': 'Reload',
        'CFBundleDisplayName': 'Reload'
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)