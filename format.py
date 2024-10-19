import subprocess
import sys


def format():
    try:
        import black

        installed = True
    except ImportError:
        installed = False

    if not installed:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "black"])

    subprocess.check_call([sys.executable, "-m", "black", "core.py"])
    subprocess.check_call([sys.executable, "-m", "black", "main.py"])
    subprocess.check_call([sys.executable, "-m", "black", "settings.py"])


if __name__ == "__main__":
    format()