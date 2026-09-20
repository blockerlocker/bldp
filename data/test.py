import os, sys, urllib.request
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not Path.cwd().name == "data":
    print(f"Working directory not named 'data'! Instead got '{Path.cwd().name}'. bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

MCVERSION = bldp.get_version(MCVERSION)

bldp.remove_path("bldp/function/test")

within_world = "\n".join([
    "execute store success storage bldp:within_world out byte 1 run clone ~ ~ ~ ~ ~ ~ ~ ~ ~ strict replace force",
    "execute if data storage bldp:within_world {out:true} run return run data remove storage bldp:within_world out",
    "data remove storage bldp:within_world out",
    "return fail"
])
bldp.string_to_file(within_world,"bldp/function/test","within_world.mcfunction")