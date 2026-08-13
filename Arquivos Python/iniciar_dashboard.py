import subprocess
import webbrowser
import time
from pathlib import Path
import sys







PYTHON = r"C:\Users\Joey Usagii\AppData\Local\Programs\Python\Python313\python.exe"
APP = Path(__file__).parent / "app.py"

link_dash = f'"{PYTHON}" -m streamlit run "{APP}"'

processo = subprocess.Popen(
    link_dash,
    shell=True
)

time.sleep(3)

#webbrowser.open("http://localhost:8501")