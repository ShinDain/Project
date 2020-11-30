import gfw
from pico2d import *
from tile import *
import gobj
import random

import objects
import monster

UNIT_PER_LINE = 10
SCREEN_LINES = 9
BLOCK_SIZE = 64

OBJECT_COUNT = 0
MAX_OBJECT_COUNT = 1

lines = []

def load(file, x, y):
    global lines, current_x, current_y, map_index
    with open(file, 'r') as f:
        lines = f.readlines()
    current_x = x * UNIT_PER_LINE * BLOCK_SIZE
    current_y = y * (SCREEN_LINES - 1) * BLOCK_SIZE
    map_index = random.randint(0,9)

def load_door(file,x,y):
    global lines, current_x, current_y, map_index
    with open(file, 'r') as f:
        lines = f.readlines()
    current_x = x * UNIT_PER_LINE * BLOCK_SIZE
    current_y = y * (SCREEN_LINES - 1) * BLOCK_SIZE
    map_index = 0

def count():
    return len(lines) // SCREEN_LINES * UNIT_PER_LINE

def update():
    create_column()

def create_column():
    global current_x,current_y, map_index
    y = current_y;
    for row in range(SCREEN_LINES):
        ch = get(map_index, row)
        create_object(ch, current_x, y)
        y += BLOCK_SIZE
    print('map_index:', map_index)
    global OBJECT_COUNT
    OBJECT_COUNT = 0

def remove_double(x,y):
    for t in gfw.world.objects_at(gfw.layer.tile):
            if t.left == x and t.bottom == y:
                gfw.world.remove(t)

def create_object(ch, x, y):
    global OBJECT_COUNT
    for i in range(len(ch)):
        if ch[i] == '1':
            remove_double(x,y)
            obj = tile('cave_block', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'A':
            remove_double(x,y)
            obj = arrow_trap('arrow_block', x, y, True)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'a':
            remove_double(x,y)
            obj = arrow_trap('arrow_block', x, y, False)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'L':
            remove_double(x,y)
            obj = tile('ledder_top', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'l':
            remove_double(x,y)
            obj = tile('ledder_bottom', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'S':
            remove_double(x,y)
            obj = spike('spike', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == '9':
            obj = entrance('entrance', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == '8':
            obj = exit('exit', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == '-':
            global OBJECT_COUNT
            if OBJECT_COUNT < MAX_OBJECT_COUNT:
                choice = random.choice([ monster.Monster])
                name = random.choice(['snake', 'bat'])
                pos = x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2
                obj = choice(pos, name)
                gfw.world.add(gfw.layer.monster, obj)
                OBJECT_COUNT += 1
            x += BLOCK_SIZE
        else:
            x += BLOCK_SIZE

def get(x, y):
    col = x % UNIT_PER_LINE
    row = x * SCREEN_LINES + SCREEN_LINES - y - 1
    #print('lines[row] = ', lines[row])
    return lines[row]

def dont_fall_tile():
    for i in range(40):
        tmp = tile('cant_break',i * BLOCK_SIZE, - BLOCK_SIZE)
        gfw.world.add(gfw.layer.tile,tmp)