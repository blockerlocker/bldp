import os, sys, urllib.request, re
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not Path.cwd().name == "data":
    print(f"Working directory not named 'data'! Instead got '{Path.cwd().name}'. bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

MCVERSION = bldp.get_version(MCVERSION)

bldp.remove_paths(["bldp/function/registry/items.mcfunction",
        "bldp/function/registry/block_placing_items.mcfunction",
        "bldp/function/registry/blocks.mcfunction",
        "bldp/function/registry/entities.mcfunction",
        "bldp/function/registry/mobs.mcfunction",
        "bldp/function/registry/mob_effects.mcfunction",
        "bldp/function/registry/non_air_blocks.mcfunction",
        "bldp/function/registry/non_mob_entities.mcfunction",
        "bldp/function/registry/biomes.mcfunction",
        "bldp/tags/item/all.json",
        "bldp/tags/item/block_placing_items.json",
        "bldp/tags/block/all.json",
        "bldp/tags/block/non_air_blocks.json",
        "bldp/tags/entity_type/all.json",
        "bldp/tags/entity_type/mobs.json",
        "bldp/tags/entity_type/non_mob_entities.json"
    ])

bldp_config = bldp.import_config()

if bldp_config == None:
    bldp_config = {
        "data/data_registries": {
            "all": True
        }
    }

all_registries = ["items","blocks","block_placing_items","non_air_blocks","biomes","entities","mobs","non_mob_entities","mob_effects"]

if "all" in bldp_config["data/data_registries"] and bldp_config["data/data_registries"]["all"] == True:
    for registry in all_registries:
        bldp_config["data/data_registries"][registry] = ["storage","tag"]
else:
    for registry in all_registries:
        if not registry in bldp_config["data/data_registries"]:
            bldp_config["data/data_registries"][registry] = []

def export_files(data,storage_name,type=None,tag_name=None):
    if not storage_name in bldp_config["data/data_registries"]: return
    
    if "storage" in bldp_config["data/data_registries"][storage_name]:
        bldp.string_to_file(f"data modify storage bldp:registry all.{storage_name} set value {data}","bldp/function/registry",f"{storage_name}.mcfunction")
        bldp.tag_append("bldp/tags/function","load",f"bldp:registry/{storage_name}")

    if "tag" in bldp_config["data/data_registries"][storage_name] and not type == None:
        if tag_name == None: tag_name = storage_name
        bldp.json_to_file({"values":data},f"bldp/tags/{type}",tag_name)

item_list = bldp.get_registry_data(MCVERSION,"item")
export_files(item_list,"items","item","all")

block_list = bldp.get_registry_data(MCVERSION,"block")
export_files(block_list,"blocks","block","all")

block_placing_item_list = [item for item in item_list if item in block_list and not re.fullmatch("air|wheat",item)]
block_placing_item_list.extend(["beetroot_seeds", "carrot", "cocoa_beans", "glow_berries", "melon_seeds", "pitcher_pod", "potato", "powder_snow_bucket", "pumpkin_seeds", "redstone", "string", "sweet_berries", "torchflower_seeds", "wheat_seeds"])
export_files(block_placing_item_list,"block_placing_items","item")

non_air_block_list = [block for block in block_list if block not in ["air", "void_air", "cave_air"]]
export_files(non_air_block_list,"non_air_blocks","block")

biome_list = bldp.get_registry_data(MCVERSION,"worldgen/biome")
export_files(biome_list,"biomes")

entity_type_list = bldp.get_registry_data(MCVERSION,"entity_type")
export_files(entity_type_list,"entities","entity_type","all")

mob_list = [mob for mob in entity_type_list if not re.search("_boat|_raft|minecart|potion|item|_display|armor_stand|area_effect_cloud|ball|arrow|firework|llama_spit|trident|skull|wind_charge|cushion|egg|ender_pearl|experience|falling_block|eye_of_ender|fishing_bobber|interaction|leash_knot|lightning_bolt|marker|painting|shulker_bullet|end_crystal|tnt|player|evoker_fangs",mob)]
export_files(mob_list,"mobs","entity_type")

non_mob_entities_list = [entity for entity in entity_type_list if not entity in mob_list]
export_files(non_mob_entities_list,"non_mob_entities","entity_type")

mob_effect_list = bldp.get_registry_data(MCVERSION,"mob_effect")
export_files(mob_effect_list,"mob_effects")

bldp.tag_append("minecraft/tags/function","load","#bldp:load")