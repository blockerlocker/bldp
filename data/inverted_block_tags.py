import os, json, sys, urllib.request
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

bldp.remove_path("bldp/tags/block/inverted")

block_list = bldp.get_registry_data(MCVERSION,"block")
for block in block_list:
    tag_template = {"values":[]}

    tag_template["values"] = [other_block for other_block in block_list if other_block != block]

    Path("bldp/tags/block/inverted/").mkdir(parents=True, exist_ok=True)
    
    with open(f"bldp/tags/block/inverted/{block}.json", "w") as output_file:
        json.dump(tag_template,output_file,indent=4)