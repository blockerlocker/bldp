bldp is a data pack library I use for my projects. This repo contains the entirety of bldp, but the individual modules can be generated with each individual Python script. The Python scripts must be stored in the data folder of your data pack in order to generate correctly. Below are descriptions of each module.

All Python scripts can have the target Minecraft version set manually be editing the **MCVERSION** variable near the top of script, or by running the script via the command line (ie; `python mined_block.py "26.2"`). This is also true of `!all.py`, which installs all modules in the folder using whatever MCVERSION it has set for itself.

These generators are powered using the automatically generated and version-controlled mcmeta data maintained by Misode, check out the repo here: https://github.com/misode/mcmeta

## Modules
| Module | Description |
| --- | --- |
| mined_block | A predicate that can be used to detect if the player mined any block. The predicate is `bldp:mined_block`, and uses a scoreboard for every block in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:mined_block/reset`. |
| crafted_item | A predicate that can be used to detect if the player crafted any item. The predicate is `bldp:crafted_item`, and uses a scoreboard for every item in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:crafted_item/reset`. |
| picked_up_item | A predicate that can be used to detect if the player picked up any item. The predicate is `bldp:picked_up_item`, and uses a scoreboard for every item in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:picked_up_item/reset`. |
| update_tags | Sorts every block, entity, and item into different tags based on when they were added to the game. So if you want to kill every entity added in the 1.4.2 Pretty Scary Update, you can run `/kill @e[type=#bldp:update/1.4.2]`. The generator for this pack does not currently support older versions where IDs were different, its designed for the most recent version of the game. |
| data_registries | Adds several registries accessible via `data get storage bldp:registry` and item/entity/block tags. Includes lists for every item, block, entity, and biome, as well as for all block-placing items, all mobs, and all non-mob entities. |
| item_icons | A dictionary that matches item ids with a sprite text component. You can easily retrieve the icon with the text component `{storage:"bldp:icon",nbt:"all.item[{id:<item_id>}].icon",interpret:true}` |
| inverted_block_tags | Creates block tags for every block in the game, which each contain every OTHER block in the game besides the one named. I thought this would be useful for `execute unless blocks` but I forgot how that actually works, so I have no idea what the application is for this right now lol. |

## Manually Defined Resources
Some files in this library are manually defined and are not automatically generated. These are typically kept up-to-date to the latest snapshot, since that is the version I tend to develop in.

### Predicates
| Predicate | Description |
| --- | --- |
| interaction_attack | Used to detect if entities have the `attack` NBT tag. |
| interaction_interact | Used to detect if entities have the `interaction` NBT tag. |

### Functions
| Function | Description |
| --- | --- |
| test/within_world | Returns either true or false depending on whether or not the execution location is within the world (the tile allows block modification). |