import gfw
from pico2d import *
import gobj
import random
import stage_gen

def make_all_map():
    map_x = 0
    map_y = 0

    file_fmt = 'stages/stage_type%d.txt'
    fn = file_fmt % random.randint(0,3)

    load_count = 0
    while load_count < 16:
        stage_gen.load(gobj.res(fn), map_x, map_y)
        stage_gen.update()
        map_x += 1
        map_x = map_x % 4
        map_y = load_count // 4
        load_count += 1