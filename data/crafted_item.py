import requests, os, json, sys, shutil
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-8"


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not Path.cwd().name == "data":
    print("Working directory not named 'data'! bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    sys.exit()

if Path("bldp/function/crafted_item").exists():
    shutil.rmtree("bldp/function/crafted_item", ignore_errors=True)
    print("--Removed existing functions")
if Path("bldp/predicate/crafted_item.json").exists():
    os.remove("bldp/predicate/crafted_item.json")
    print("--Removed existing predicate")

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
    item_list = get_item_list()
    generate_predicate(item_list)
    generate_line_per_item(item_list,"scoreboard objectives add bldp.crafted.%(item) minecraft.crafted:%(item)","bldp/function/crafted_item/","load.mcfunction")
    generate_line_per_item(item_list,"scoreboard players reset @s bldp.crafted.%(item)","bldp/function/crafted_item/","reset.mcfunction")
    generate_line_per_item(item_list,"execute if score @s bldp.crafted.%(item) matches 1.. run data modify storage bldp:crafted_item out set value %(item)","bldp/function/crafted_item/","identify.mcfunction")
    append_to_load("bldp/tags/function/","bldp:crafted_item/load")
    append_to_load("minecraft/tags/function/","#bldp:load")

if __name__ == "__main__":
    main()