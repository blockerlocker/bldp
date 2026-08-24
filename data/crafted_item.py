import os, json, sys, urllib.request, re
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-9"


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not Path.cwd().name == "data":
    print("Working directory not named 'data'! bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

bldp.remove_path("bldp/function/crafted_item")
bldp.remove_path("bldp/predicate/crafted_item.json")

def generate_predicate(item_list):
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
        
        term_template["scores"]["bldp.crafted."+item] = {"min": 1}

        predicate_template["terms"].append(term_template)
    
    Path("bldp/predicate/").mkdir(parents=True, exist_ok=True)
    
    with open("bldp/predicate/crafted_item.json", "w") as predicate_json:
        json.dump(predicate_template,predicate_json,indent=4)

def main():
    item_list = bldp.get_registry_data(MCVERSION,"item")

    generate_predicate(item_list)

    load_function = "\n".join([re.sub("(^.*$)",r"scoreboard objectives add bldp.crafted.\1 minecraft.crafted:\1",item) for item in item_list])
    bldp.string_to_file(load_function,"bldp/function/crafted_item","load.mcfunction")

    reset_function = "\n".join([re.sub("(^.*$)",r"scoreboard players reset @s bldp.crafted.\1",item) for item in item_list])
    bldp.string_to_file(reset_function,"bldp/function/crafted_item","reset.mcfunction")

    identify_function = "\n".join([re.sub("(^.*$)",r"execute if score @s bldp.crafted.\1 matches 1.. run data modify storage bldp:crafted_item out set value \1",item) for item in item_list])
    bldp.string_to_file(identify_function,"bldp/function/crafted_item","identify.mcfunction")
    
    bldp.tag_append("bldp/tags/function","load","bldp:crafted_item/load")
    bldp.tag_append("minecraft/tags/function","load","#bldp:load")

if __name__ == "__main__":
    main()