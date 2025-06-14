import subprocess
import sys
import shutil

required_packages = ["pygame", "ffmpeg-python"]

def install_dependencies():
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            print(f"[Setup] Installing: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    if shutil.which("ffmpeg") is None:
        print("⚠️ FFmpeg executable not found in PATH.")
        print("➡️ Please install it from: https://ffmpeg.org/download.html")
