import requests
import os
import json
from pathlib import Path
import sys


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-5"


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def get_item_list():
    item_list_response = requests.get("https://raw.githubusercontent.com/misode/mcmeta/"+MCVERSION+"-registries/item/data.json")
        
    if item_list_response.status_code == 200:
        return(item_list_response.json())
    else:
        print(f"Failed to grab directory!")

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

def generate_load(item_list):
    load_template = ""

    for item in item_list:
        load_template += "\nscoreboard objectives add bldp.crafted."+item+" minecraft.crafted:"+item
    
    Path("bldp/function/crafted_item/").mkdir(parents=True, exist_ok=True)

    with open("bldp/function/crafted_item/load.mcfunction", "w", encoding="utf-8") as load_mcfunction:
        load_mcfunction.write(load_template)

def generate_reset(item_list):
    reset_template = ""

    for item in item_list:
        reset_template += "\nscoreboard players reset @s bldp.crafted."+item
    
    Path("bldp/function/crafted_item/").mkdir(parents=True, exist_ok=True)

    with open("bldp/function/crafted_item/reset.mcfunction", "w", encoding="utf-8") as reset_mcfunction:
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
    item_list = get_item_list()
    generate_predicate(item_list)
    generate_load(item_list)
    generate_reset(item_list)
    append_to_load("bldp/tags/function/","bldp:crafted_item/load")
    append_to_load("minecraft/tags/function/","#bldp:load")

if __name__ == "__main__":
    main()