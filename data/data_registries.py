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

remove_path("bldp/function/registry")
remove_path("bldp/tags/item/all.json")
remove_path("bldp/tags/item/block_placing_item.json")
remove_path("bldp/tags/block/all.json")
remove_path("bldp/tags/entity_type/all.json")
remove_path("bldp/tags/entity_type/mobs.json")
remove_path("bldp/tags/entity_type/non_mobs_entities.json")

def get_item_list():
    item_list_response = requests.get("https://raw.githubusercontent.com/misode/mcmeta/"+MCVERSION+"-registries/item/data.json")
        
    if item_list_response.status_code == 200:
        return(item_list_response.json())
    else:
        print(f"Failed to grab directory!")

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
    item_list = json.load(urllib.request.urlopen(f"https://raw.githubusercontent.com/misode/mcmeta/{MCVERSION}-registries/item/data.json"))
    string_to_file(f"data modify storage bldp:registry all.items set value {item_list}","bldp/function/registry","items.mcfunction")
    json_to_file({"values":item_list},"bldp/tags/item","all")
    append_to_bldp_load("execute unless data storage bldp:registry all.items run function bldp:registry/items")

    block_list = json.load(urllib.request.urlopen(f"https://raw.githubusercontent.com/misode/mcmeta/{MCVERSION}-registries/block/data.json"))
    string_to_file(f"data modify storage bldp:registry all.blocks set value {block_list}","bldp/function/registry","blocks.mcfunction")
    json_to_file({"values":block_list},"bldp/tags/block","all")
    append_to_bldp_load("execute unless data storage bldp:registry all.blocks run function bldp:registry/blocks")

    block_placing_item_list = [item for item in item_list if item in block_list and not re.fullmatch("air|wheat",item)]
    block_placing_item_list.extend(["beetroot_seeds", "carrot", "cocoa_beans", "glow_berries", "melon_seeds", "pitcher_pod", "potato", "powder_snow_bucket", "pumpkin_seeds", "redstone", "string", "sweet_berries", "torchflower_seeds", "wheat_seeds"])
    string_to_file(f"data modify storage bldp:registry all.block_placing_items set value {block_placing_item_list}","bldp/function/registry","block_placing_items.mcfunction")
    json_to_file({"values":block_placing_item_list},"bldp/tags/item","block_placing_item")
    append_to_bldp_load("execute unless data storage bldp:registry all.block_placing_items run function bldp:registry/block_placing_items")

    biome_list = json.load(urllib.request.urlopen(f"https://raw.githubusercontent.com/misode/mcmeta/{MCVERSION}-registries/worldgen/biome/data.json"))
    string_to_file(f"data modify storage bldp:registry all.biomes set value {biome_list}","bldp/function/registry","biomes.mcfunction")
    append_to_bldp_load("execute unless data storage bldp:registry all.biomes run function bldp:registry/biomes")
    
    entity_type_list = json.load(urllib.request.urlopen(f"https://raw.githubusercontent.com/misode/mcmeta/{MCVERSION}-registries/entity_type/data.json"))
    string_to_file(f"data modify storage bldp:registry all.entities set value {entity_type_list}","bldp/function/registry","entities.mcfunction")
    json_to_file({"values":entity_type_list},"bldp/tags/entity_type","all")
    append_to_bldp_load("execute unless data storage bldp:registry all.entities run function bldp:registry/entities")

    mob_list = [mob for mob in entity_type_list if not re.search("_boat|_raft|minecart|potion|item|_display|armor_stand|area_effect_cloud|ball|arrow|firework|llama_spit|trident|skull|wind_charge|cushion|egg|ender_pearl|experience|falling_block|eye_of_ender|fishing_bobber|interaction|leash_knot|lightning_bolt|marker|painting|shulker_bullet|end_crystal|tnt|player",mob)]
    string_to_file(f"data modify storage bldp:registry all.mobs set value {mob_list}","bldp/function/registry","mobs.mcfunction")
    json_to_file({"values":mob_list},"bldp/tags/entity_type","mobs")
    append_to_bldp_load("execute unless data storage bldp:registry all.mobs run function bldp:registry/mobs")

    non_mob_entities_list = [entity for entity in entity_type_list if not entity in mob_list]
    string_to_file(f"data modify storage bldp:registry all.non_mob_entities set value {non_mob_entities_list}","bldp/function/registry","non_mob_entities.mcfunction")
    json_to_file({"values":non_mob_entities_list},"bldp/tags/entity_type","non_mob_entities")
    append_to_bldp_load("execute unless data storage bldp:registry all.non_mob_entities run function bldp:registry/non_mob_entities")

    append_to_load_tag("bldp/tags/function/","bldp:main/load")
    append_to_load_tag("minecraft/tags/function/","#bldp:load")

if __name__ == "__main__":
    main()