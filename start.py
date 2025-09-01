# ======================================================
#  API Endpoint Usage Checker
#  Launcher script (run: python start.py)
#  Copyright (c) 2025 Usama Bakry (ubakry@solvytix.com)
#  Licensed under the MIT License
# ======================================================

import os
import sys
import subprocess
import venv

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(ROOT_DIR, "venv")

def create_virtualenv():
    """Create venv if it does not exist"""
    if not os.path.exists(VENV_DIR):
        print("📦 Creating virtual environment...")
        venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    else:
        print("ℹ️ Virtual environment already exists.")

def get_venv_python():
    """Return path to venv's Python executable"""
    if os.name == "nt":  # Windows
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:  # Linux/Mac
        return os.path.join(VENV_DIR, "bin", "python")

def install_requirements(python_exec):
    """Install requirements.txt inside venv"""
    print("📥 Installing dependencies...")
    subprocess.check_call([python_exec, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([python_exec, "-m", "pip", "install", "-r", "requirements.txt"])

def run_streamlit_app(python_exec):
    """Run app.py using Streamlit inside venv"""
    print("🚀 Starting API Endpoint Usage Checker ...")
    subprocess.run([python_exec, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    create_virtualenv()
    python_exec = get_venv_python()
    install_requirements(python_exec)
    run_streamlit_app(python_exec)
