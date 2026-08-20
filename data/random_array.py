import requests, os, json, sys, shutil, urllib.request, re
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

def remove_path(path):
    if Path(path).exists():
        if Path(path).is_dir(): shutil.rmtree(path,ignore_errors=True)
        elif Path(path).is_file(): os.remove(path)
        print(f"--Removed {path}")

remove_path("bldp/function/func/array")
remove_path("bldp/function/func/random")

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

def main():
    string_to_file("$execute store result storage bldp:temp all.random.value int 1 run random value $(x)..$(y)","bldp/function/func/random","value.mcfunction")
    string_to_file("data remove storage bldp:array_random out\nexecute store result score #bldp_array_random operator if data storage bldp:array_random in[]\ndata modify storage bldp:temp all.random.x set value 0\nexecute store result storage bldp:temp all.random.y int 1 run scoreboard players remove #bldp_array_random operator 1\nfunction bldp:func/random/value with storage bldp:temp all.random\nfunction bldp:func/array/random/commit with storage bldp:temp all.random\ndata remove storage bldp:array_random in\ndata remove storage bldp:temp all","bldp/function/func/array/random","init.mcfunction")
    string_to_file("$data modify storage bldp:array_random out set from storage bldp:array_random in[$(value)]\ndata modify storage bldp:array_random index set from storage bldp:temp all.random.value","bldp/function/func/array/random","commit.mcfunction")
    append_to_bldp_load("scoreboard objectives add operator dummy")

    if Path("bldp/function/registry").is_dir():
        for registry in Path("bldp/function/registry").iterdir():
            registry_name = Path(registry).stem
            string_to_file(f"data modify storage bldp:array_random in set from storage bldp:registry all.{registry_name}\nfunction bldp:func/array/random/init","bldp/function/func/random",f"{registry_name}.mcfunction")

    append_to_load_tag("bldp/tags/function/","bldp:main/load")
    append_to_load_tag("minecraft/tags/function/","#bldp:load")

if __name__ == "__main__":
    main()