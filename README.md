bldp is a data pack library I use for my projects. This repo contains the entirety of bldp, but the individual modules can be generated with each individual Python script. The Python scripts must be stored in the data folder of your data pack in order to generate correctly. Below are descriptions of each module.

All Python scripts can have the MC version set manually be editing the MCVERSION variable near the top of script, or by running the script via the command line (ie; `python mined_block.py "26.2"`). This is also true of `!all.py`, which just installs all modules in the folder.

## Modules
**mined_block**: A predicate that can be used to detect if the player mined any block. The predicate is `bldp:mined_block`, and uses a scoreboard for every block in the game. You must manually program logic for resetting the scoreboard once detected via the function `bldp:mined_block/reset`.


(Other modules have yet to be converted into Python scripts, and will be documented here once they are.)