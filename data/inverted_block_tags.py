import requests
import os
import json
from pathlib import Path
import sys


if len(sys.argv) > 1:
    MCVERSION = sys.argv[1]
else:
#### SET MINECRAFT VERSION MANUALLY HERE ####
    MCVERSION = "26.3-snapshot-8"


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

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