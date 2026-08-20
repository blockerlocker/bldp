import os, sys, urllib.request, re
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

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

bldp.remove_path("bldp/function/registry")
bldp.remove_path("bldp/tags/item/all.json")
bldp.remove_path("bldp/tags/item/block_placing_item.json")
bldp.remove_path("bldp/tags/block/all.json")
bldp.remove_path("bldp/tags/entity_type/all.json")
bldp.remove_path("bldp/tags/entity_type/mobs.json")
bldp.remove_path("bldp/tags/entity_type/non_mobs_entities.json")

item_list = bldp.get_registry_data(MCVERSION,"item")
bldp.string_to_file(f"data modify storage bldp:registry all.items set value {item_list}","bldp/function/registry","items.mcfunction")
bldp.json_to_file({"values":item_list},"bldp/tags/item","all")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.items run function bldp:registry/items")

block_list = bldp.get_registry_data(MCVERSION,"block")
bldp.string_to_file(f"data modify storage bldp:registry all.blocks set value {block_list}","bldp/function/registry","blocks.mcfunction")
bldp.json_to_file({"values":block_list},"bldp/tags/block","all")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.blocks run function bldp:registry/blocks")

block_placing_item_list = [item for item in item_list if item in block_list and not re.fullmatch("air|wheat",item)]
block_placing_item_list.extend(["beetroot_seeds", "carrot", "cocoa_beans", "glow_berries", "melon_seeds", "pitcher_pod", "potato", "powder_snow_bucket", "pumpkin_seeds", "redstone", "string", "sweet_berries", "torchflower_seeds", "wheat_seeds"])
bldp.string_to_file(f"data modify storage bldp:registry all.block_placing_items set value {block_placing_item_list}","bldp/function/registry","block_placing_items.mcfunction")
bldp.json_to_file({"values":block_placing_item_list},"bldp/tags/item","block_placing_item")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.block_placing_items run function bldp:registry/block_placing_items")

biome_list = bldp.get_registry_data(MCVERSION,"worldgen/biome")
bldp.string_to_file(f"data modify storage bldp:registry all.biomes set value {biome_list}","bldp/function/registry","biomes.mcfunction")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.biomes run function bldp:registry/biomes")

entity_type_list = bldp.get_registry_data(MCVERSION,"entity_type")
bldp.string_to_file(f"data modify storage bldp:registry all.entities set value {entity_type_list}","bldp/function/registry","entities.mcfunction")
bldp.json_to_file({"values":entity_type_list},"bldp/tags/entity_type","all")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.entities run function bldp:registry/entities")

mob_list = [mob for mob in entity_type_list if not re.search("_boat|_raft|minecart|potion|item|_display|armor_stand|area_effect_cloud|ball|arrow|firework|llama_spit|trident|skull|wind_charge|cushion|egg|ender_pearl|experience|falling_block|eye_of_ender|fishing_bobber|interaction|leash_knot|lightning_bolt|marker|painting|shulker_bullet|end_crystal|tnt|player",mob)]
bldp.string_to_file(f"data modify storage bldp:registry all.mobs set value {mob_list}","bldp/function/registry","mobs.mcfunction")
bldp.json_to_file({"values":mob_list},"bldp/tags/entity_type","mobs")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.mobs run function bldp:registry/mobs")

non_mob_entities_list = [entity for entity in entity_type_list if not entity in mob_list]
bldp.string_to_file(f"data modify storage bldp:registry all.non_mob_entities set value {non_mob_entities_list}","bldp/function/registry","non_mob_entities.mcfunction")
bldp.json_to_file({"values":non_mob_entities_list},"bldp/tags/entity_type","non_mob_entities")
bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:registry all.non_mob_entities run function bldp:registry/non_mob_entities")

bldp.tag_append("bldp/tags/function","load","bldp:main/load")
bldp.tag_append("minecraft/tags/function","load","#bldp:load")