import os, sys, urllib.request, re
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


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

MCVERSION = blpack.get_version(MCVERSION)

blpack.remove_paths([
    "data/blpack/function/mined_block",
    "data/blpack/predicate/mined_block.json"
])

block_list = blpack.get_registry_data(MCVERSION,"block")

predicate_template = {
        "type": "minecraft:any_of",
        "terms": []
    }

for block in block_list:
    term_template = {
            "type": "minecraft:entity_scores",
            "entity": "this",
            "scores": {}
        }
    
    term_template["scores"]["blpack.mined."+block] = {"min": 1}

    predicate_template["terms"].append(term_template)

blpack.json_to_file(predicate_template,"data/blpack/predicate","mined_block")

load_commands = [re.sub("(^.*$)",r"scoreboard objectives add blpack.mined.\1 minecraft.mined:\1",block) for block in block_list]
load_commands.insert(0,"scoreboard objectives add blpack.blocks_mined dummy")
load_function = "\n".join(load_commands)
blpack.string_to_file(load_function,"data/blpack/function/mined_block","load.mcfunction")

reset_function = "\n".join([re.sub("(^.*$)",r"scoreboard players reset @s blpack.mined.\1",block) for block in block_list])
blpack.string_to_file(reset_function,"data/blpack/function/mined_block","reset.mcfunction")

identify_function = "\n".join([re.sub("(^.*$)",r"execute if score @s blpack.mined.\1 matches 1.. run data modify storage blpack:mined_block out set value \1",block) for block in block_list])
blpack.string_to_file(identify_function,"data/blpack/function/mined_block","identify.mcfunction")

add_function = "\n".join([re.sub("(^.*$)",r"execute if score @s blpack.mined.\1 matches 1.. run scoreboard players operation @s blpack.blocks_mined += @s blpack.mined.\1",block) for block in block_list])
blpack.string_to_file(add_function,"data/blpack/function/mined_block","add.mcfunction")

blpack.tag_append("data/blpack/tags/function","load","blpack:mined_block/load")
blpack.tag_append("data/minecraft/tags/function","load","#blpack:load")