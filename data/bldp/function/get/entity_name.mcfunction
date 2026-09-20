tag @s add bldp_get_entity_name
summon text_display ~ ~ ~ {text:{selector:'@n[tag=bldp_get_entity_name]'},UUID:uuid('dd344b15-32c3-4264-b149-f1e0c083f0f2')}
data modify storage bldp:get all.entity_name set from entity dd344b15-32c3-4264-b149-f1e0c083f0f2 text.hover_event.name
tag @s remove bldp_get_entity_name
kill dd344b15-32c3-4264-b149-f1e0c083f0f2