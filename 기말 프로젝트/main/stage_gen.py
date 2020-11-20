import gfw
from pico2d import *
from tile import tile
import gobj
import random

UNIT_PER_LINE = 10
SCREEN_LINES = 9
BLOCK_SIZE = 64

lines = []

def load(file, x, y):
    global lines, current_x, current_y, map_index
    with open(file, 'r') as f:
        lines = f.readlines()
    current_x = x * UNIT_PER_LINE * BLOCK_SIZE
    current_y = y * (SCREEN_LINES - 1) * BLOCK_SIZE
    map_index = random.randint(0,9)

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

def create_object(ch, x, y):
    for i in range(len(ch)):
        if ch[i] == '1':
            obj = tile('cave_block', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'A':
            obj = tile('arrow_block', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'L':
            obj = tile('ledder_top', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        elif ch[i] == 'l':
            obj = tile('ledder_bottom', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        else:
            x += BLOCK_SIZE
            pass

def get(x, y):
    col = x % UNIT_PER_LINE
    row = x * SCREEN_LINES + SCREEN_LINES - y - 1
    print('lines[row] = ', lines[row])
    return lines[row]

def test_gen_2():
    open_canvas()
    gfw.world.init(['tile'])
    load(gobj.res('stages/stage_type0.txt'))

    print('count=', count())

    for i in range(100):
        update()

    close_canvas()

if __name__ == '__main__':
    test_gen_2()