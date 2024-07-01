import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List your dependencies here
dependencies = [
    'pyautogui',
    'autoit',
    'keyboard',
    'pynput',
    'tk',
    'requests',
    'pygetwindow',
    'numpy',
    'pillow',
    'multiprocessing',  # Multiprocessing is part of the standard library, so this line can be omitted.
    'ctypes',  # ctypes is part of the standard library, so this line can be omitted.
    'webbrowser',  # webbrowser is part of the standard library, so this line can be omitted.
    'configparser',  # configparser is part of the standard library, so this line can be omitted.
]

if __name__ == "__main__":
    for package in dependencies:
        try:
            __import__(package)
        except ImportError:
            install(package)
