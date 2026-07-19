import requests
import os
import json
from pathlib import Path
import sys


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-4"


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def get_block_list():
    block_list_response = requests.get("https://raw.githubusercontent.com/misode/mcmeta/"+MCVERSION+"-registries/block/data.json")
        
    if block_list_response.status_code == 200:
        return(block_list_response.json())
    else:
        print(f"Failed to grab directory!")

def generate_predicate(block_list):
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
        
        term_template["scores"]["bldp.mined."+block] = {"min": 1}

        predicate_template["terms"].append(term_template)
    
    Path("bldp/predicate/").mkdir(parents=True, exist_ok=True)
    
    with open("bldp/predicate/mined_block.json", "w") as predicate_json:
        json.dump(predicate_template,predicate_json,indent=4)

def generate_load(block_list):
    load_template = ""

    for block in block_list:
        load_template += "\nscoreboard objectives add bldp.mined."+block+" minecraft.mined:"+block
    
    Path("bldp/function/mined_block/").mkdir(parents=True, exist_ok=True)

    with open("bldp/function/mined_block/load.mcfunction", "w", encoding="utf-8") as load_mcfunction:
        load_mcfunction.write(load_template)

def generate_reset(block_list):
    reset_template = ""

    for block in block_list:
        reset_template += "\nscoreboard players reset @s bldp.mined."+block
    
    Path("bldp/function/mined_block/").mkdir(parents=True, exist_ok=True)

    with open("bldp/function/mined_block/reset.mcfunction", "w", encoding="utf-8") as reset_mcfunction:
        reset_mcfunction.write(reset_template)

def append_to_load(path,append_value):
    file_path = path + "load.json"
    
    if Path(file_path).is_file():
        with open(file_path, "r", encoding="utf-8") as load_json:
            new_load = json.load(load_json)
            if not append_value in new_load["values"]:
                new_load["values"].append(append_value)
                with open(file_path, "w") as new_load_json:
                    json.dump(new_load,new_load_json,indent=4)
    else:
        Path(path).mkdir(parents=True, exist_ok=True)

        new_load = {"values":[append_value]}

        with open(file_path, "w") as new_load_json:
            json.dump(new_load,new_load_json,indent=4)

def main():
    block_list = get_block_list()
    generate_predicate(block_list)
    generate_load(block_list)
    generate_reset(block_list)
    append_to_load("bldp/tags/function/","bldp:mined_block/load")
    append_to_load("minecraft/tags/function/","#bldp:load")

if __name__ == "__main__":
    main()