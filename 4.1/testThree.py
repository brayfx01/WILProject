import subprocess

# Attempt to run PyInstaller in a subprocess
try:
    subprocess.run(["pyinstaller", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print("PyInstaller is in your PATH.")
except subprocess.CalledProcessError:
    print("PyInstaller is not in your PATH.")
except FileNotFoundError:
    print("PyInstaller is not installed or not in your PATH.")
