execute at @s anchored eyes run summon marker ^ ^ ^ {UUID:uuid('1d655d4c-d951-442b-98ed-54ae52c6823f')}
data modify storage bldp:temp all.feet set from entity @s Pos[1]
data modify storage bldp:temp all.eyes set from entity 1d655d4c-d951-442b-98ed-54ae52c6823f Pos[1]
data modify storage bldp:get all.entity_midpoint set compute default float {type:div,left:{type:sub,left:{type:storage,storage:'bldp:temp',path:all.eyes},right:{type:storage,storage:'bldp:temp',path:all.feet}},right:2}
kill 1d655d4c-d951-442b-98ed-54ae52c6823f
data remove storage bldp:temp all