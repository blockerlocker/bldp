import requests, os, json, sys, shutil
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

if Path("bldp/tags/block/inverted").exists():
    shutil.rmtree("bldp/tags/block/inverted", ignore_errors=True)
    print("--Removed existing block tags")

def get_block_list():
    block_list_response = requests.get("https://raw.githubusercontent.com/misode/mcmeta/"+MCVERSION+"-registries/block/data.json")
        
    if block_list_response.status_code == 200:
        return(block_list_response.json())
    else:
        print(f"Failed to grab directory!")

def generate_inverted_block_tags(block_list):
    for block in block_list:
        tag_template = {"values":[]}

        tag_template["values"] = [other_block for other_block in block_list if other_block != block]
    
        Path("bldp/tags/block/inverted/").mkdir(parents=True, exist_ok=True)
        
        with open(f"bldp/tags/block/inverted/{block}.json", "w") as output_file:
            json.dump(tag_template,output_file,indent=4)

def main():
    block_list = get_block_list()
    generate_inverted_block_tags(block_list)

if __name__ == "__main__":
    main()