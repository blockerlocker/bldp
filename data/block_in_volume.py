import os, sys, urllib.request, re
from pathlib import Path

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

config = blpack.import_config_settings(f"{Path(__file__).resolve().parent.name}/{Path(__file__).stem}")

if config == None:
    config = {}

if "volume_input" not in config:
    config["volume_input"] = input("What volumes would you like to generate a test for? Enter in 16x16x16 format, separated by commas.\n> ")

volumes_raw = config["volume_input"].split(",")
all_volumes = []
for volume in volumes_raw:
    volume_dimensions = re.split(r'[x: ]', volume)
    volume_dimensions = [int(dim) for dim in volume_dimensions if dim != ""]
    all_volumes.append(volume_dimensions)

if "block_id_input" not in config:
    config["block_id_input"] = input("What block are you testing for? Accepts block ids and block tags.\nIf no block is provided, a macro function is generated instead.\n> ")

if config["block_id_input"] == "":
    generate_macro = True
else:
    generate_macro = False

if generate_macro == False and ("#" in config["block_id_input"] or ":" in config["block_id_input"]):
    auto_path = config["block_id_input"].replace(":","/").replace("#","")
    
    if "path_input" not in config:
        config["path_input"] = input(f"You have entered a block tag, would you like to specify a custom path? If you enter nothing, the file will end up at \"data/blpack/predicate/block_in_volume/{auto_path}\"\n> ")
    
    if config["path_input"] == "":
        custom_path = f"data/blpack/predicate/block_in_volume/{auto_path}"
    else:
        custom_path = config["path_input"]
    
    use_custom_path = True
else:
    use_custom_path = False

for current_volume in all_volumes:
    predicate_template = {
        "type": "any_of",
        "terms": []
    }

    for x in range(0,current_volume[0]):
        for y in range(0,current_volume[1]):
            for z in range(0,current_volume[2]):
                subpredicate_entry = {
                    "type": "location_check",
                    "offsetX": x,
                    "offsetY": y,
                    "offsetZ": z,
                    "predicate": {
                        "block": {
                            "blocks": "$(id)"
                        }
                    }
                }

                if subpredicate_entry["offsetX"] == 0:
                    subpredicate_entry.pop("offsetX")
                if subpredicate_entry["offsetY"] == 0:
                    subpredicate_entry.pop("offsetY")
                if subpredicate_entry["offsetZ"] == 0:
                    subpredicate_entry.pop("offsetZ")

                predicate_template["terms"].append(subpredicate_entry)

    if generate_macro == True:
        predicate_string = str(predicate_template)
        predicate_string = predicate_string.replace("'","").replace(" ","")

        function = "\n".join([
            f"$execute if predicate {predicate_string} run return 1",
            "return 0"
        ])

        blpack.string_to_file(function,"data/blpack/function/block_in_volume",f"{current_volume[0]}x{current_volume[1]}x{current_volume[2]}.mcfunction")
    elif generate_macro == False:
        for subpredicate in predicate_template["terms"]:
            subpredicate["predicate"]["block"]["blocks"] = config["block_id_input"]

        if use_custom_path == True:
            path = custom_path
        else:
            path = f"data/blpack/predicate/block_in_volume/{config["block_id_input"]}"

        blpack.json_to_file(predicate_template,path,f"{current_volume[0]}x{current_volume[1]}x{current_volume[2]}")