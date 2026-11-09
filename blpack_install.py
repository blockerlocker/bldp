import os, sys, urllib.request, subprocess
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


os.chdir(Path(__file__).resolve().parent)

if not Path("blpack.py").is_file():
    with open("blpack.py", "w", encoding="utf-8") as blpack_main:
        blpack_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/blpack/main/blpack.py").read().decode('utf-8'))

import blpack

MCVERSION = blpack.get_version(MCVERSION)

for file in Path("data").iterdir():
    if file.is_file() and file.suffix.lower() == ".py":
        print(f"-Running module {Path(file).name}")
        subprocess.run([sys.executable, file, MCVERSION])
