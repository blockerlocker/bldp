import requests, os, json, shutil
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

def json_to_file(json_object,path,file_name):
    Path(path).mkdir(parents=True, exist_ok=True)

    if not path[-2:-1] in ["/", "\\"]:
        path += "/"

    if not file_name[-5:] == ".json":
            file_name += ".json"

    with open(f"{path}{file_name}", "w", encoding="utf-8") as output_file:
        json.dump(json_object,output_file,indent=4)

def mcfunction_append(path,function,command):
    if not path[-2:-1] in ["/", "\\"]:
        file_path = f"{path}/{function}.mcfunction"
    else:
        file_path = f"{path}{function}.mcfunction"

    if Path(file_path).is_file():
        with open(file_path, "r", encoding="utf-8") as mcfunction:
            mcfunction_contents = mcfunction.read()

            if not command in mcfunction_contents:
                mcfunction_contents += f"\n{command}"
                with open(file_path, "w", encoding="utf-8") as new_mcfunction:
                    new_mcfunction.write(mcfunction_contents)
    else:
        string_to_file(command,path,f"{function}.mcfunction")

def tag_append(path,tag,append_value):
    if not path[-2:-1] in ["/", "\\"]:
        file_path = f"{path}/{tag}.json"
    else:
        file_path = f"{path}{tag}.json"
    
    if Path(file_path).is_file():
        with open(file_path, "r", encoding="utf-8") as tag_json:
            new_tag = json.load(tag_json)
            if not append_value in new_tag["values"]:
                new_tag["values"].append(append_value)
                with open(file_path, "w") as new_tag_json:
                    json.dump(new_tag,new_tag_json,indent=4)
    else:
        Path(path).mkdir(parents=True, exist_ok=True)

        new_tag = {"values":[append_value]}

        with open(file_path, "w") as new_tag_json:
            json.dump(new_tag,new_tag_json,indent=4)