import os
from pathlib import Path
import sys
import subprocess


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-9"


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

if not Path.cwd().name == "data":
    print("Working directory not named 'data'! bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

def main():
    current_path = Path(dname)

    for file in current_path.iterdir():
        if file.is_file() and file.suffix.lower() == ".py" and not file.name == "!all.py":
            print(f"-Running module {Path(file).name}")
            subprocess.run([sys.executable, file, MCVERSION])

if __name__ == "__main__":
    main()