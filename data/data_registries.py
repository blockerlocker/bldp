import os, sys, urllib.request, re
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


os.chdir(Path(__file__).resolve().parent.parent)
sys.path.append(str(Path.cwd()))

if not Path(Path(__file__).resolve().parent).name == "data":
    print(f"!-This module must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("blpack.py").is_file():
    with open("blpack.py", "w", encoding="utf-8") as blpack_main:
        blpack_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/blockerlocker_pack/main/blpack.py").read().decode('utf-8'))

import blpack

MCVERSION = blpack.get_version(MCVERSION)

blpack.remove_paths([
    "data/blpack/function/registry/items.mcfunction",
    "data/blpack/function/registry/block_placing_items.mcfunction",
    "data/blpack/function/registry/blocks.mcfunction",
    "data/blpack/function/registry/entities.mcfunction",
    "data/blpack/function/registry/mobs.mcfunction",
    "data/blpack/function/registry/mob_effects.mcfunction",
    "data/blpack/function/registry/non_air_blocks.mcfunction",
    "data/blpack/function/registry/non_mob_entities.mcfunction",
    "data/blpack/function/registry/biomes.mcfunction",
    "data/blpack/tags/item/all.json",
    "data/blpack/tags/item/block_placing_items.json",
    "data/blpack/tags/block/all.json",
    "data/blpack/tags/block/non_air_blocks.json",
    "data/blpack/tags/entity_type/all.json",
    "data/blpack/tags/entity_type/mobs.json",
    "data/blpack/tags/entity_type/non_mob_entities.json"
])

blpack_config = blpack.import_config()

if blpack_config == None:
    blpack_config = {
        "data/data_registries": {
            "all": True
        }
    }

all_registries = ["items","blocks","block_placing_items","non_air_blocks","biomes","entities","mobs","non_mob_entities","mob_effects"]

if "all" in blpack_config["data/data_registries"] and blpack_config["data/data_registries"]["all"] == True:
    for registry in all_registries:
        blpack_config["data/data_registries"][registry] = ["storage","tag"]
else:
    for registry in all_registries:
        if not registry in blpack_config["data/data_registries"]:
            blpack_config["data/data_registries"][registry] = []

def export_files(data,storage_name,type=None,tag_name=None):
    if not storage_name in blpack_config["data/data_registries"]: return
    
    if "storage" in blpack_config["data/data_registries"][storage_name]:
        blpack.string_to_file(f"data modify storage blpack:registry all.{storage_name} set value {data}","data/blpack/function/registry",f"{storage_name}.mcfunction")
        blpack.tag_append("data/blpack/tags/function","load",f"blpack:registry/{storage_name}")

    if "tag" in blpack_config["data/data_registries"][storage_name] and not type == None:
        if tag_name == None: tag_name = storage_name
        blpack.json_to_file({"values":data},f"data/blpack/tags/{type}",tag_name)

item_list = blpack.get_registry_data(MCVERSION,"item")
export_files(item_list,"items","item","all")

block_list = blpack.get_registry_data(MCVERSION,"block")
export_files(block_list,"blocks","block","all")

block_placing_item_list = [item for item in item_list if item in block_list and not re.fullmatch("air|wheat",item)]
block_placing_item_list.extend(["beetroot_seeds", "carrot", "cocoa_beans", "glow_berries", "melon_seeds", "pitcher_pod", "potato", "powder_snow_bucket", "pumpkin_seeds", "redstone", "string", "sweet_berries", "torchflower_seeds", "wheat_seeds"])
export_files(block_placing_item_list,"block_placing_items","item")

non_air_block_list = [block for block in block_list if block not in ["air", "void_air", "cave_air"]]
export_files(non_air_block_list,"non_air_blocks","block")

biome_list = blpack.get_registry_data(MCVERSION,"worldgen/biome")
export_files(biome_list,"biomes")

entity_type_list = blpack.get_registry_data(MCVERSION,"entity_type")
export_files(entity_type_list,"entities","entity_type","all")

mob_list = [mob for mob in entity_type_list if not re.search("_boat|_raft|minecart|potion|item|_display|armor_stand|area_effect_cloud|ball|arrow|firework|llama_spit|trident|skull|wind_charge|cushion|egg|ender_pearl|experience|falling_block|eye_of_ender|fishing_bobber|interaction|leash_knot|lightning_bolt|marker|painting|shulker_bullet|end_crystal|tnt|player|evoker_fangs",mob)]
export_files(mob_list,"mobs","entity_type")

non_mob_entities_list = [entity for entity in entity_type_list if not entity in mob_list]
export_files(non_mob_entities_list,"non_mob_entities","entity_type")

mob_effect_list = blpack.get_registry_data(MCVERSION,"mob_effect")
export_files(mob_effect_list,"mob_effects")


blpack.tag_append("data/minecraft/tags/function","load","#blpack:load")