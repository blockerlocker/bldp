import os, sys, urllib.request
from pathlib import Path

os.chdir(Path(__file__).resolve().parent.parent)
sys.path.append(str(Path.cwd()))

if not Path(Path(__file__).resolve().parent).name == "data":
    print(f"!-This module must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("blpack.py").is_file():
    with open("blpack.py", "w", encoding="utf-8") as blpack_main:
        blpack_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/blpack/main/blpack.py").read().decode('utf-8'))

import blpack

blpack.remove_paths("data/blpack/function/test")

within_world = "\n".join([
    "execute store success storage blpack:within_world out byte 1 run clone ~ ~ ~ ~ ~ ~ ~ ~ ~ strict replace force",
    "execute if data storage blpack:within_world {out:true} run return run data remove storage blpack:within_world out",
    "data remove storage blpack:within_world out",
    "return fail"
])
blpack.string_to_file(within_world,"data/blpack/function/test","within_world.mcfunction")