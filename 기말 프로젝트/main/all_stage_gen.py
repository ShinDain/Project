import gfw
from pico2d import *
import gobj
import random
import stage_gen
from tile import tile

map_pos = []
room_shape = {}

def make_all_map():
    global entrance, exit
    make_map_shape()
    select_room_shape()
    load_stage_data()
    dont_fall_tile()
    return entrance, exit

def make_map_shape():
    global entrance, exit
    map_x = random.randint(0,3)
    map_y = 3

    entrance = map_x, map_y
    map_pos.append(entrance)

    exit = (0,0)

    while map_y >= 0:
        select = random.randint(1,3)        # 좌, 하, 우 
        if select is 1:
            if map_x is 0:                    # 이미 왼쪽 끝이다.
                map_y -= 1
            else:
                map_x -= 1
        elif select is 2:
            map_y -= 1
        else:               
            if map_x is 3:                    # 이미 오른쪽 끝이다.
                map_y -= 1
            else:
                map_x += 1
        if map_y < 0:
            pass
        else:
            map_pos.append((map_x,map_y))
    exit = map_x, 0

def select_room_shape():
    for (x,y) in map_pos:
        if y > 0:
            if (x,y - 1) in map_pos:
                room_shape[(x,y)] = 2
            else:
                room_shape[(x,y)] = random.randint(1,3)
        else:
            if (x,y + 1) in map_pos:
                room_shape[(x,y)] = random.choice([2,3])
            else:
                room_shape[(x,y)] = random.choice([1,3])

def load_stage_data():
    global entrance, exit

    load_count = 0
    map_x = 0
    map_y = 0
    while load_count < 16:
        if (map_x, map_y) in room_shape:
            file_fmt = 'stages/stage_type%d.txt'
            fn = file_fmt % room_shape[(map_x, map_y)]
            stage_gen.load(gobj.res(fn), map_x, map_y)
            stage_gen.update()
        else:
            file_fmt = 'stages/stage_type%d.txt'
            fn = file_fmt % random.randint(0,3)
            stage_gen.load(gobj.res(fn), map_x, map_y)
            stage_gen.update()

        if (map_x, map_y) == entrance:
            fn = 'stages/entrance.txt'
            stage_gen.load_door(gobj.res(fn), map_x, map_y)
            stage_gen.update()
        elif (map_x, map_y) == exit:
            fn = 'stages/exit.txt'
            stage_gen.load_door(gobj.res(fn), map_x, map_y)
            stage_gen.update()

        map_x += 1
        map_x = map_x % 4
        load_count += 1
        map_y = load_count // 4

def dont_fall_tile():
    for i in range(40):
        tmp = tile('cant_break',i * stage_gen.BLOCK_SIZE, - stage_gen.BLOCK_SIZE)
        gfw.world.add(gfw.layer.tile,tmp)