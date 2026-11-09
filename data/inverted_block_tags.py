import os, json, sys, urllib.request
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

MCVERSION = blpack.import_config_version()

blpack.remove_paths("data/blpack/tags/block/inverted")

block_list = blpack.get_registry_data(MCVERSION,"block")
for block in block_list:
    tag_template = {"values":[]}

    tag_template["values"] = [other_block for other_block in block_list if other_block != block]

    blpack.json_to_file(tag_template,"data/blpack/tags/block/inverted",block)