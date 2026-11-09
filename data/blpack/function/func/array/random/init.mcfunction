data remove storage blpack:array_random out
execute store result score #blpack_array_random operator if data storage blpack:array_random in[]
data modify storage blpack:temp all.random.x set value 0
execute store result storage blpack:temp all.random.y int 1 run scoreboard players remove #blpack_array_random operator 1
function blpack:func/random/value with storage blpack:temp all.random
function blpack:func/array/random/commit with storage blpack:temp all.random
data remove storage blpack:array_random in
data remove storage blpack:temp all