import gfw
from pico2d import *
from tile import tile
import gobj

UNIT_PER_LINE = 10
SCREEN_LINES = 9
BLOCK_SIZE = 64

lines = []

def load(file):
    global lines, current_x, map_index, create_at
    with open(file, 'r') as f:
        lines = f.readlines()
    current_x = 0
    map_index = 0
    create_at = get_canvas_width() + 2 * BLOCK_SIZE

def count():
    return len(lines) // SCREEN_LINES * UNIT_PER_LINE

def update():
    global current_x, create_at, map_index
    while map_index < 1: 
        create_column()

def create_column():
    global current_x, map_index
    y = 0;
    for row in range(SCREEN_LINES + 1):
        ch = get(map_index, row)
        create_object(ch, current_x, y)
        current_x = 0
        y += BLOCK_SIZE
    map_index += 1
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
            obj = tile('ledder_bottom', x, y)
            gfw.world.add(gfw.layer.tile, obj)
            x += BLOCK_SIZE
        else:
            x += BLOCK_SIZE
            pass

def get(x, y):
    col = x % UNIT_PER_LINE
    row = x // UNIT_PER_LINE + SCREEN_LINES - y - 1
    print('lines[row] = ', lines[row])
    return lines[row]

def test_gen():
    load(gobj.res('stages/stage_type0.txt'))
    print('count=', count())
    line = 0
    for x in range(10):
        s = ''
        for y in range(10):
            s += get(x,y)
        line += 1
        print('%03d:' % line, s)

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