tag @s add bldp_get_entity_type
summon text_display ~ ~ ~ {text:{selector:'@n[tag=bldp_get_entity_type]'},UUID:uuid('dd344b15-32c3-4264-b149-f1e0c083f0f2')}
data modify storage bldp:get all.entity_type set from entity dd344b15-32c3-4264-b149-f1e0c083f0f2 text.hover_event.id
tag @s remove bldp_get_entity_type
kill dd344b15-32c3-4264-b149-f1e0c083f0f2