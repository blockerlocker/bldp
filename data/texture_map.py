import os, sys, urllib.request, json, math
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

TEMP_DIR = "temp_bldp"

bldp.remove_path(TEMP_DIR)
bldp.remove_path("bldp/function/texture_map")

bldp.unpack_client(MCVERSION,TEMP_DIR,("assets/minecraft/blockstates","assets/minecraft/models/block","assets/minecraft/textures"))

print("--Generating Block Texture Map")
blockstate_dir = f"{TEMP_DIR}/assets/minecraft/blockstates/"
block_map = []
for file in os.listdir(blockstate_dir):

    block_id = file.replace(".json","")

    if not block_id in ["item_frame", "glow_item_frame", "air"]:
        with open(f"{blockstate_dir}/{file}", "r") as blockstate_json:
            blockstate_raw = json.load(blockstate_json)

        model_paths = []

        def append_if_new(array,new_path):
            if not new_path in array:
                array.append(new_path)

        def scan_textures(raw_model_json):
            if "textures" in raw_model_json:
                for key in raw_model_json["textures"]:
                    if "sprite" in raw_model_json["textures"][key]:
                        new_texture = raw_model_json["textures"][key]["sprite"]
                    else:
                        new_texture = raw_model_json["textures"][key]

                    if new_texture[0:10] == "minecraft:":
                        new_texture = new_texture[10:]

                    if not new_texture.startswith("#"):
                        append_if_new(texture_paths,new_texture)

        if "variants" in blockstate_raw:
            for key in blockstate_raw["variants"]:
                if "model" in blockstate_raw["variants"][key]:
                    append_if_new(model_paths,blockstate_raw["variants"][key]["model"])
                else:
                    for random_variant in blockstate_raw["variants"][key]:
                        append_if_new(model_paths,random_variant["model"])
                
        elif "multipart" in blockstate_raw:
            for part in blockstate_raw["multipart"]:
                if "model" in part["apply"]:
                    append_if_new(model_paths,part["apply"]["model"])
                else:
                    for application in part["apply"]:
                        append_if_new(model_paths,application["model"])

        texture_paths = []

        for model_path in model_paths:

            if model_path[0:10] == "minecraft:":
                model_path = model_path[10:]
            actual_model_path = f"{TEMP_DIR}/assets/minecraft/models/{model_path}.json"
            with open (actual_model_path, "r") as model_json:
                model_raw = json.load(model_json)
                scan_textures(model_raw)

            if "parent" in model_raw:
                parent_path = model_raw["parent"]
                if parent_path[0:10] == "minecraft:":
                    parent_path = parent_path[10:]
                actual_parent_path = f"{TEMP_DIR}/assets/minecraft/models/{parent_path}.json"
                with open (actual_parent_path, "r") as parent_json:
                    parent_raw = json.load(parent_json)
                    scan_textures(parent_raw)
            
        if len(texture_paths) == 1\
        or block_id.endswith("lightning_rod")\
        or block_id == "spore_blossom"\
        or block_id == "test_block"\
        or block_id == "pointed_dripstone"\
        or block_id == "sulfur_spike"\
        or block_id == "dried_ghast"\
        or block_id == "redstone_wire"\
        or block_id == "bell"\
        or block_id == "frosted_ice"\
        or block_id == "lever"\
        or block_id == "bamboo"\
        or block_id == "bamboo_fence"\
        or block_id == "bamboo_fence_gate"\
        or block_id == "shelf_mushroom":
            main_texture = texture_paths[0]
        elif block_id == "large_fern"\
        or block_id == "tall_grass"\
        or block_id == "tall_seagrass"\
        or block_id == "pale_hanging_moss"\
        or block_id == "structure_block"\
        or block_id == "torchflower_crop"\
        or block_id == "wheat"\
        or block_id == "cocoa"\
        or block_id == "beetroots"\
        or block_id == "carrots"\
        or block_id == "potatoes"\
        or block_id == "redstone_torch"\
        or block_id == "redstone_wall_torch"\
        or block_id == "straw_bed"\
        or block_id == "nether_wart"\
        or block_id == "pitcher_plant"\
        or block_id == "sweet_berry_bush":
            main_texture = texture_paths[-1]
        elif block_id == "tripwire_hook"\
        or block_id == "creaking_heart"\
        or block_id == "brewing_stand"\
        or block_id == "brown_mushroom_block"\
        or block_id == "red_mushroom_block"\
        or block_id == "mushroom_stem"\
        or block_id == "flower_pot"\
        or block_id == "farmland"\
        or block_id == "comparator"\
        or block_id == "repeater"\
        or block_id == "redstone_lamp"\
        or block_id == "wildflowers"\
        or block_id == "pink_petals"\
        or block_id == "bookshelf"\
        or block_id == "firefly_bush"\
        or block_id == "rail"\
        or block_id == "detector_rail"\
        or block_id == "powered_rail"\
        or block_id == "activator_rail"\
        or block_id == "cave_vines"\
        or block_id == "cave_vines_plant"\
        or block_id == "chorus_flower"\
        or block_id == "mangrove_propagule"\
        or block_id == "open_eyeblossom"\
        or block_id == "beacon"\
        or block_id == "pale_moss_carpet"\
        or block_id == "turtle_egg":
            main_texture = f"block/{block_id}"
        elif block_id == "vault":
            main_texture = "block/vault_front_off"
        elif block_id == "light":
            main_texture = "item/light_15"
        elif block_id == "sniffer_egg":
            main_texture = "block/sniffer_egg_not_cracked_north"
        elif block_id == "trial_spawner":
            main_texture = "block/trial_spawner_side_active"
        elif block_id.endswith("campfire"):
            main_texture = "block/campfire_log"
        elif block_id.endswith("_cake"):
            main_texture = "block/cake_top"
        elif block_id.endswith("cauldron"):
            main_texture = "block/cauldron_side"
        elif block_id.startswith("potted_"):
            main_texture = "block/flower_pot"
        elif block_id.endswith("_log") or block_id.endswith("_hanging_sign") or block_id.endswith("_shelf"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_log")),None)
        elif block_id.endswith("_bed"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_bed_foot_up")),None)
        elif block_id.endswith("candle"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("candle")),None)
        elif block_id.endswith("glass_pane"):
            main_texture = next((tex for tex in texture_paths if not tex.endswith("top")),None)
        elif block_id.endswith("_door"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_door_top")),None)
        elif block_id.endswith("_sign"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_planks")),None)
        elif block_id.endswith("copper_bulb"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("copper_bulb")),None)
        elif block_id.endswith("_stem"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_stem")),None)
        elif block_id.endswith("_nylium"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_nylium_side")),None)
        elif block_id.startswith("suspicious_") or block_id.endswith("fire"):
            main_texture = next((tex for tex in texture_paths if tex.endswith("_0")),None)
        elif block_id == "azalea"\
            or block_id == "calibrated_sculk_sensor"\
            or block_id == "flowering_azalea":
            main_texture = next((tex for tex in texture_paths if tex.endswith("_top")),None)
        elif next((tex for tex in texture_paths if tex.endswith("_front")),None) in texture_paths:
            main_texture = next((tex for tex in texture_paths if tex.endswith("_front")),None)
        elif next((tex for tex in texture_paths if tex.endswith("_side")),None) in texture_paths:
            main_texture = next((tex for tex in texture_paths if tex.endswith("_side")),None)
        elif next((tex for tex in texture_paths if tex.endswith("_top")),None) in texture_paths:
            main_texture = next((tex for tex in texture_paths if not tex.endswith("_top")),None)
        else:
            print(f"{block_id}: {texture_paths}")
            main_texture = texture_paths[0]

        block_map.append({"id":block_id,"main_texture":main_texture,"all_textures":texture_paths})

bldp.string_to_file(f"data modify storage bldp:texture_map all.block set value {block_map}","bldp/function/texture_map","block.mcfunction")
bldp.tag_append("bldp/tags/function","load","bldp:texture_map/block")

bldp.tag_append("minecraft/tags/function","load","#bldp:load")

bldp.remove_path(TEMP_DIR)