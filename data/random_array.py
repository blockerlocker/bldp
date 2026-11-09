import os, sys, urllib.request
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

blpack.remove_paths([
    "data/blpack/function/func/array",
    "data/blpack/function/func/random"
])

blpack.string_to_file("$execute store result storage blpack:temp all.random.value int 1 run random value $(x)..$(y)","data/blpack/function/func/random","value.mcfunction")

init_function = "\n".join([
    "data remove storage blpack:array_random out",
    "execute store result score #blpack_array_random operator if data storage blpack:array_random in[]",
    "data modify storage blpack:temp all.random.x set value 0",
    "execute store result storage blpack:temp all.random.y int 1 run scoreboard players remove #blpack_array_random operator 1",
    "function blpack:func/random/value with storage blpack:temp all.random",
    "function blpack:func/array/random/commit with storage blpack:temp all.random",
    "data remove storage blpack:array_random in",
    "data remove storage blpack:temp all"
])
blpack.string_to_file(init_function,"data/blpack/function/func/array/random","init.mcfunction")

commit_function = "\n".join([
    "$data modify storage blpack:array_random out set from storage blpack:array_random in[$(value)]",
    "data modify storage blpack:array_random index set from storage blpack:temp all.random.value"
])
blpack.string_to_file(commit_function,"data/blpack/function/func/array/random","commit.mcfunction")

blpack.mcfunction_append("data/blpack/function/main","load","scoreboard objectives add operator dummy")

def registry_crawl(registry):
    for sub_registry in registry.iterdir():
        if sub_registry.is_file():
            registry_path = str(registry).replace("\\","/").replace("data/blpack/function/registry/","")
            subregistry_name = Path(sub_registry).stem
            blpack.string_to_file(f"data modify storage blpack:array_random in set from storage blpack:registry all.\"{subregistry_name}\"\nfunction blpack:func/array/random/init",f"data/blpack/function/func/random/{registry_path}",f"{subregistry_name}.mcfunction")
        elif sub_registry.is_dir():
            registry_crawl(sub_registry)

if Path("data/blpack/function/registry").is_dir():
    for registry in Path("data/blpack/function/registry").iterdir():
        if registry.is_file():
            registry_name = Path(registry).stem
            blpack.string_to_file(f"data modify storage blpack:array_random in set from storage blpack:registry all.\"{registry_name}\"\nfunction blpack:func/array/random/init","data/blpack/function/func/random",f"{registry_name}.mcfunction")
        elif registry.is_dir():
            registry_crawl(registry)
        
blpack.tag_append("data/blpack/tags/function","load","blpack:main/load")
blpack.tag_append("data/minecraft/tags/function","load","#blpack:load")