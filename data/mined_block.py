import requests
import os
import json
from pathlib import Path
import sys


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-7"


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

def generate_line_per_item(list,string,path,file_name):
    template = ""

    for item in list:
        template += "\n"
        template += string.replace("%(item)",item)
    
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(path+file_name, "w", encoding="utf-8") as output_file:
        output_file.write(template)

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
    generate_line_per_item(block_list,"scoreboard objectives add bldp.mined.%(item) minecraft.mined:%(item)","bldp/function/mined_block/","load.mcfunction")
    generate_line_per_item(block_list,"scoreboard players reset @s bldp.mined.%(item)","bldp/function/mined_block/","reset.mcfunction")
    generate_line_per_item(block_list,"execute if score @s bldp.mined.%(item) matches 1.. run data modify storage bldp:mined_block out set value %(item)","bldp/function/mined_block/","identify.mcfunction")
    append_to_load("bldp/tags/function/","bldp:mined_block/load")
    append_to_load("minecraft/tags/function/","#bldp:load")

if __name__ == "__main__":
    main()