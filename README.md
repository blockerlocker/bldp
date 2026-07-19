bldp is a data pack library I use for my projects. This repo contains the entirety of bldp, but the individual modules can be generated with each individual Python script. The Python scripts must be stored in the `data` folder of your data pack in order to generate correctly. Below are descriptions of each module.

All Python scripts can have the target Minecraft version set manually be editing the **MCVERSION** variable near the top of script, or by running the script via the command line (ie; `python mined_block.py "26.2"`). This is also true of `!all.py`, which installs all modules in the folder using whatever MCVERSION it has set for itself.

These generators are powered using the automatically generated and version-controlled mcmeta data maintained by Misode, check out the repo here: https://github.com/misode/mcmeta

## Modules
**mined_block**: A predicate that can be used to detect if the player mined any block. The predicate is `bldp:mined_block`, and uses a scoreboard for every block in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:mined_block/reset`.

**crafted_item**: A predicate that can be used to detect if the player crafted any item. The predicate is `bldp:crafted_item`, and uses a scoreboard for every item in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:crafted_item/reset`.

**picked_up_item**: A predicate that can be used to detect if the player picked up any item. The predicate is `bldp:picked_up_item`, and uses a scoreboard for every item in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:picked_up_item/reset`.

(Other modules have yet to be converted into Python scripts, and will be documented here once they are.)

## Manually Defined Resources
Some files in this library are manually defined and are not automatically generated. These are typically kept up-to-date to the latest snapshot, since that is the version I tend to develop in.

### Predicates
**interaction_attack**: Used to detect if entities have the `attack` NBT tag.
**interaction_interact**: Used to detect if entities have the `interaction` NBT tag.

### Item Tags
**block_placing_item**: All items that can be used to place blocks.
