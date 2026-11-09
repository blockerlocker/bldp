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
        blpack_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/blockerlocker_pack/main/blpack.py").read().decode('utf-8'))

import blpack

MCVERSION = blpack.get_version(MCVERSION)

blpack.remove_paths([
    "data/blpack/function/crafted_item",
    "data/blpack/predicate/crafted_item.json"
])

item_list = blpack.get_registry_data(MCVERSION,"item")

predicate_template = {
        "type": "minecraft:any_of",
        "terms": []
    }

for item in item_list:
    term_template = {
            "type": "minecraft:entity_scores",
            "entity": "this",
            "scores": {}
        }
    
    term_template["scores"]["blpack.crafted."+item] = {"min": 1}

    predicate_template["terms"].append(term_template)

blpack.json_to_file(predicate_template,"data/blpack/predicate","crafted_item")

load_function = "\n".join([re.sub("(^.*$)",r"scoreboard objectives add blpack.crafted.\1 minecraft.crafted:\1",item) for item in item_list])
blpack.string_to_file(load_function,"data/blpack/function/crafted_item","load.mcfunction")

reset_function = "\n".join([re.sub("(^.*$)",r"scoreboard players reset @s blpack.crafted.\1",item) for item in item_list])
blpack.string_to_file(reset_function,"data/blpack/function/crafted_item","reset.mcfunction")

identify_function = "\n".join([re.sub("(^.*$)",r"execute if score @s blpack.crafted.\1 matches 1.. run data modify storage blpack:crafted_item out set value \1",item) for item in item_list])
blpack.string_to_file(identify_function,"data/blpack/function/crafted_item","identify.mcfunction")

blpack.tag_append("data/blpack/tags/function","load","blpack:crafted_item/load")
blpack.tag_append("data/minecraft/tags/function","load","#blpack:load")