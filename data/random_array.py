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

bldp.remove_path("bldp/function/func/array")
bldp.remove_path("bldp/function/func/random")

bldp.string_to_file("$execute store result storage bldp:temp all.random.value int 1 run random value $(x)..$(y)","bldp/function/func/random","value.mcfunction")
bldp.string_to_file("data remove storage bldp:array_random out\nexecute store result score #bldp_array_random operator if data storage bldp:array_random in[]\ndata modify storage bldp:temp all.random.x set value 0\nexecute store result storage bldp:temp all.random.y int 1 run scoreboard players remove #bldp_array_random operator 1\nfunction bldp:func/random/value with storage bldp:temp all.random\nfunction bldp:func/array/random/commit with storage bldp:temp all.random\ndata remove storage bldp:array_random in\ndata remove storage bldp:temp all","bldp/function/func/array/random","init.mcfunction")
bldp.string_to_file("$data modify storage bldp:array_random out set from storage bldp:array_random in[$(value)]\ndata modify storage bldp:array_random index set from storage bldp:temp all.random.value","bldp/function/func/array/random","commit.mcfunction")
bldp.mcfunction_append("bldp/function/main","load","scoreboard objectives add operator dummy")

if Path("bldp/function/registry").is_dir():
    for registry in Path("bldp/function/registry").iterdir():
        registry_name = Path(registry).stem
        bldp.string_to_file(f"data modify storage bldp:array_random in set from storage bldp:registry all.{registry_name}\nfunction bldp:func/array/random/init","bldp/function/func/random",f"{registry_name}.mcfunction")

bldp.tag_append("bldp/tags/function","load","bldp:main/load")
bldp.tag_append("minecraft/tags/function","load","#bldp:load")