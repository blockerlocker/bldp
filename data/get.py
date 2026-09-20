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

bldp.remove_path("bldp/function/get")

entity_midpoint = "\n".join([
    "execute at @s anchored eyes run summon marker ^ ^ ^ {UUID:uuid('1d655d4c-d951-442b-98ed-54ae52c6823f')}",
    "data modify storage bldp:temp all.feet set from entity @s Pos[1]",
    "data modify storage bldp:temp all.eyes set from entity 1d655d4c-d951-442b-98ed-54ae52c6823f Pos[1]",
    "data modify storage bldp:get all.entity_midpoint set compute default float {type:div,left:{type:sub,left:{type:storage,storage:'bldp:temp',path:all.eyes},right:{type:storage,storage:'bldp:temp',path:all.feet}},right:2}",
    "kill 1d655d4c-d951-442b-98ed-54ae52c6823f",
    "data remove storage bldp:temp all"
])
bldp.string_to_file(entity_midpoint,"bldp/function/get","entity_midpoint.mcfunction")

entity_name = "\n".join([
    "tag @s add bldp_get_entity_name",
    "summon text_display ~ ~ ~ {text:{selector:'@n[tag=bldp_get_entity_name]'},UUID:uuid('dd344b15-32c3-4264-b149-f1e0c083f0f2')}",
    "data modify storage bldp:get all.entity_name set from entity dd344b15-32c3-4264-b149-f1e0c083f0f2 text.hover_event.name",
    "tag @s remove bldp_get_entity_name",
    "kill dd344b15-32c3-4264-b149-f1e0c083f0f2"
])
bldp.string_to_file(entity_name,"bldp/function/get","entity_name.mcfunction")

entity_type = "\n".join([
    "tag @s add bldp_get_entity_type",
    "summon text_display ~ ~ ~ {text:{selector:'@n[tag=bldp_get_entity_type]'},UUID:uuid('dd344b15-32c3-4264-b149-f1e0c083f0f2')}",
    "data modify storage bldp:get all.entity_type set from entity dd344b15-32c3-4264-b149-f1e0c083f0f2 text.hover_event.id",
    "tag @s remove bldp_get_entity_type",
    "kill dd344b15-32c3-4264-b149-f1e0c083f0f2"
])
bldp.string_to_file(entity_type,"bldp/function/get","entity_type.mcfunction")