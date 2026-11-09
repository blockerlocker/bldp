execute store success storage blpack:within_world out byte 1 run clone ~ ~ ~ ~ ~ ~ ~ ~ ~ strict replace force
execute if data storage blpack:within_world {out:true} run return run data remove storage blpack:within_world out
data remove storage blpack:within_world out
return fail