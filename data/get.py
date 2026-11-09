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

blpack.remove_paths("data/blpack/function/get")

entity_midpoint = "\n".join([
    "execute at @s anchored eyes run summon marker ^ ^ ^ {UUID:uuid('1d655d4c-d951-442b-98ed-54ae52c6823f')}",
    "data modify storage blpack:temp all.feet set from entity @s Pos[1]",
    "data modify storage blpack:temp all.eyes set from entity 1d655d4c-d951-442b-98ed-54ae52c6823f Pos[1]",
    "data modify storage blpack:get all.entity_midpoint set compute default float {type:div,left:{type:sub,left:{type:storage,storage:'blpack:temp',path:all.eyes},right:{type:storage,storage:'blpack:temp',path:all.feet}},right:2}",
    "kill 1d655d4c-d951-442b-98ed-54ae52c6823f",
    "data remove storage blpack:temp all"
])
blpack.string_to_file(entity_midpoint,"data/blpack/function/get","entity_midpoint.mcfunction")

entity_name = "\n".join([
    "tag @s add blpack_get_entity_name",
    "summon text_display ~ ~ ~ {text:{selector:'@n[tag=blpack_get_entity_name]'},UUID:uuid('dd344b15-32c3-4264-b149-f1e0c083f0f2')}",
    "data modify storage blpack:get all.entity_name set from entity dd344b15-32c3-4264-b149-f1e0c083f0f2 text.hover_event.name",
    "tag @s remove blpack_get_entity_name",
    "kill dd344b15-32c3-4264-b149-f1e0c083f0f2"
])
blpack.string_to_file(entity_name,"data/blpack/function/get","entity_name.mcfunction")

entity_type = "\n".join([
    "tag @s add blpack_get_entity_type",
    "summon text_display ~ ~ ~ {text:{selector:'@n[tag=blpack_get_entity_type]'},UUID:uuid('dd344b15-32c3-4264-b149-f1e0c083f0f2')}",
    "data modify storage blpack:get all.entity_type set from entity dd344b15-32c3-4264-b149-f1e0c083f0f2 text.hover_event.id",
    "tag @s remove blpack_get_entity_type",
    "kill dd344b15-32c3-4264-b149-f1e0c083f0f2"
])
blpack.string_to_file(entity_type,"data/blpack/function/get","entity_type.mcfunction")