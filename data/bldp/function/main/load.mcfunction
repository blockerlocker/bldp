scoreboard objectives add operator dummy

execute unless data storage bldp:icon all.item run function bldp:icon/item

execute unless data storage bldp:registry all.items run function bldp:registry/items
execute unless data storage bldp:registry all.blocks run function bldp:registry/blocks
execute unless data storage bldp:registry all.block_placing_items run function bldp:registry/block_placing_items
execute unless data storage bldp:registry all.biomes run function bldp:registry/biomes
execute unless data storage bldp:registry all.entities run function bldp:registry/entities
execute unless data storage bldp:registry all.mobs run function bldp:registry/mobs
execute unless data storage bldp:registry all.non_mob_entities run function bldp:registry/non_mob_entities
execute unless data storage bldp:registry all.updates run function bldp:registry/updates
execute unless data storage bldp:registry all.updates_with_items run function bldp:registry/updates_with_items
execute unless data storage bldp:registry all.updates_with_blocks run function bldp:registry/updates_with_blocks
execute unless data storage bldp:registry all.updates_with_entities run function bldp:registry/updates_with_entities