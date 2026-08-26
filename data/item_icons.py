import os, sys, urllib.request, re
from pathlib import Path


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "latest-snapshot"


os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

if not Path.cwd().name == "data":
    print("Working directory not named 'data'! bldp generation scripts must be stored within the 'data' folder of your pack to generate correctly!")
    input("Press Enter to exit program...")
    sys.exit()

if not Path("bldp.py").is_file():
    with open("bldp.py", "w", encoding="utf-8") as bldp_main:
        bldp_main.write(urllib.request.urlopen("https://raw.githubusercontent.com/blockerlocker/bldp/main/data/bldp.py").read().decode('utf-8'))

import bldp

MCVERSION = bldp.get_version(MCVERSION)

bldp.remove_path("bldp/function/icon")

item_list = bldp.get_registry_data(MCVERSION,"item")
block_list = bldp.get_registry_data(MCVERSION,"block")

item_icons_list = []

for id in item_list:
    name = id
    color = None

    if re.search("_fence_gate",name): name = name[0:-11]
    if re.search("_stairs|_button",name): name = name[0:-7]
    if re.search("_fence",name): name = name[0:-6]
    if re.search("_slab|_wall|_pane",name): name = name[0:-5]
    if re.search("waxed_",name): name = name[6:]
    if re.search("infested_",name): name = name[9:]

    if re.search("_pressure_plate",name) and not re.search("weighted",name): name = name[0:-15]

    if f"{name}_planks" in item_list: name += "_planks"
    
    if name[-5:] == "_wood": name = f"{name[:-5]}_log"
    if name[-7:] == "_hyphae": name = f"{name[:-7]}_stem"
    if name[-11:] == "moss_carpet": name = f"{name[:-11]}moss_block"
    if name[-7:] == "_carpet": name = f"{name[:-7]}_wool"
    if name[-4:] == "_bed" and name != "straw_bed": name += "_head_up"
    if name[-13:] == "command_block": name += "_back"
    if name[-12:] == "copper_chest": name = f"{name[0:-12]}copper"
    if name[-5:] == "brick" and id in block_list: name += "s"
    if name[-4:] == "tile" and id in block_list: name += "s"

    if re.fullmatch("copper|purpur|quartz",name) and id in block_list: name += "_block"
    if re.fullmatch("shelf_mushroom|straw_bed",name) : name += "_particle"
    if re.fullmatch("magma_block|snow_block",name) : name = name[0:-6]

    if re.search("smooth_quartz",name) : name = "quartz_block_bottom"
    if re.search("smooth_red_sandstone",name) : name = "red_sandstone_top"
    if re.search("smooth_sandstone",name) : name = "sandstone_top"

    if id == "air": name = "structure_void"
    if id == "azalea": name = "potted_azalea_bush_plant"
    if id == "calibrated_sculk_sensor": name = "calibrated_sculk_sensor_input_side"
    if id == "chiseled_bookshelf": name = "chiseled_bookshelf_occupied"
    if id == "crafter": name = "crafter_north"
    if id == "crossbow": name = "crossbow_standby"
    if id == "debug_stick": name = "stick"
    if id == "decorated_pot": name = "flower_pot"
    if id == "dried_ghast": name = "dried_ghast_hydration_0_north"
    if id == "dried_kelp_block": name = "dried_kelp_side"
    if id == "enchanted_golden_apple": name = "golden_apple"
    if id == "ender_chest": name = "end_portal_frame_eye"
    if id == "dragon_head": name = "ender_dragon_spawn_egg"
    if id == "flowering_azalea": name = "potted_flowering_azalea_bush_plant"
    if id == "grindstone": name = "grindstone_round"
    if id == "heavy_weighted_pressure_plate": name = "iron_block"
    if id == "light_weighted_pressure_plate": name = "gold_block"
    if id == "light": name = "light_15"
    if id == "respawn_anchor": name = "respawn_anchor_side4"
    if id == "sticky_piston": name = "piston_top_sticky"
    if id == "stonecutter": name = "stonecutter_saw"
    if id == "test_block": name = "test_block_accept"
    if id == "tipped_arrow": name = "tipped_arrow_head"
    if id == "trial_spawner": name = "trial_spawner_side_inactive"
    if id == "vault": name = "vault_front_off"
    if id == "pale_hanging_moss": name = "pale_hanging_moss_tip"

    if re.fullmatch("chest|petrified_oak_slab|trapped_chest",id): name = "oak_planks"

    if re.fullmatch("ancient_debris|barrel|basalt|bone_block|cactus|composter|dirt_path|enchanting_table|fletching_table|grass_block|hay_block|honey_block|lodestone|mangrove_roots|melon|muddy_mangrove_roots|mycelium|ochre_froglight|pearlescent_froglight|podzol|polished_basalt|pumpkin|quartz_block|reinforced_deepslate|scaffolding|sculk_catalyst|sculk_sensor|sculk_shrieker|target|tnt|verdant_froglight|purpur_pillar|quartz_pillar",name):
        name += "_side"
    if re.fullmatch("bee_nest|beehive|blast_furnace|crafting_table|dispenser|dropper|furnace|loom|observer|smithing_table|smoker|sunflower",name):
        name += "_front"
    if re.fullmatch("anvil|big_dripleaf|cartography_table|chipped_anvil|damaged_anvil|daylight_detector|end_portal_frame|jigsaw|jukebox|large_fern|lectern|lilac|peony|piston|rose_bush|small_dripleaf|smooth_red_sandstone|smooth_sandstone|tall_grass",name):
        name += "_top"
    if re.fullmatch("clock|compass|recovery_compass",name):
        name += "_00"
    if re.fullmatch("suspicious_gravel|suspicious_sand",name):
        name += "_0"
    
    if id in block_list and not re.search("_door|_sign",id) and not re.fullmatch("air|wheat|structure_void|barrier|bell|cake|brewing_stand|cauldron|campfire|soul_campfire|comparator|repeater|dragon_head|hopper|nether_wart|light|pitcher_plant|pointed_dripstone|sniffer_egg|sulfur_spike",id):
        sprite = f"block/{name}"
        atlas = "blocks"
    else:
        sprite = f"item/{name}"
        atlas = "items"
    
    if name[-5:] == "_head" and id in block_list:
        sprite = f"item/{name[0:-5]}_spawn_egg"
        atlas = "items"

    if name[-6:] == "_skull":
        sprite = f"item/{name[0:-6]}_spawn_egg"
        atlas = "items"

    if name[-19:] == "copper_golem_statue":
        sprite = "item/copper_golem_spawn_egg"
        atlas = "items"

    if name[-19:] == "player_head":
        sprite = "item/pufferfish"
        atlas = "items"

    if name[-7:] == "_banner":
        sprite = name
        atlas = "map_decorations"

    if name == "shield":
        sprite = "container/slot/shield"
        atlas = "gui"
        color = "aqua"

    if id == "mangrove_leaves":
        color = "#92c648"

    if id == "spruce_leaves":
        color = "#619961"

    if id == "birch_leaves":
        color = "#80a755"

    if id == "lily_pad":
        color = "#208030"

    if re.fullmatch("short_grass|tall_grass|bush|fern|large_fern",id):
        color = "#7cbd6b"

    if re.fullmatch("oak_leaves|jungle_leaves|acacia_leaves|dark_oak_leaves|vine",id):
        color = "#48b518"
    
    icon = {"id":id,"icon":{"sprite":sprite,"atlas":atlas}}
    if not color == None:
        icon["icon"]["color"] = color
    item_icons_list.append(icon)

bldp.string_to_file(f"data modify storage bldp:icon all.item set value {item_icons_list}","bldp/function/icon","item.mcfunction")

bldp.mcfunction_append("bldp/function/main","load","execute unless data storage bldp:icon all.item run function bldp:icon/item")

bldp.tag_append("bldp/tags/function","load","bldp:crafted_item/load")
bldp.tag_append("minecraft/tags/function","load","#bldp:load")

if DEBUG == True: bldp.json_to_file({"values":item_icons_list},"debug","item_icons")