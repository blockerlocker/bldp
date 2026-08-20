import requests, os, json, sys, shutil, urllib.request, re
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_registry_data(mcversion,registry):
    item_list_response = requests.get(f"https://raw.githubusercontent.com/misode/mcmeta/{mcversion}-registries/{registry}/data.json")
        
    if item_list_response.status_code == 200:
        return(item_list_response.json())
    else:
        print(f"Failed to grab directory!")

def remove_path(path):
    if Path(path).exists():
        if Path(path).is_dir(): shutil.rmtree(path,ignore_errors=True)
        elif Path(path).is_file(): os.remove(path)
        print(f"--Removed {path}")

def string_to_file(string,path,file_name):
    Path(path).mkdir(parents=True, exist_ok=True)

    if not path[-2:-1] in ["/", "\\"]:
        path += "/"

    with open(path+file_name, "w", encoding="utf-8") as output_file:
        output_file.write(string)

def append_to_bldp_load(command):
    if Path("bldp/function/main/load.mcfunction").is_file():
        with open("bldp/function/main/load.mcfunction", "r", encoding="utf-8") as bldp_load:
            bldp_load_contents = bldp_load.read()

            if not command in bldp_load_contents:
                bldp_load_contents += f"\n{command}"
                with open("bldp/function/main/load.mcfunction", "w", encoding="utf-8") as new_bldp_load:
                    new_bldp_load.write(bldp_load_contents)
    else:
        string_to_file(command,"bldp/function/main","load.mcfunction")

def append_to_load_tag(path,append_value):
    if not path[-2:-1] in ["/", "\\"]:
        file_path = f"{path}/load.json"
    else:
        file_path = f"{path}load.json"
    
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