from pico2d import *
import gfw
import gobj
import objects

tilesetimage = None
objectimage = None

entranceimage = None
exitimage = None

tile_rects = {}

BLOCK_SIZE = 64

def load():
    global tilesetimage, entranceimage, exitimage, objectimage
    if tilesetimage is None:
        tilesetimage = gfw.image.load(gobj.res('tileset.png'))
        with open(gobj.res('all_tile.json')) as f:
            data = json.load(f)
            for name in data:
                tile_rects[name] = tuple(data[name])
    if objectimage is None:
        objectimage = gfw.image.load(gobj.res('object.png'))

    if entranceimage is None:
        entranceimage = gfw.image.load(gobj.res('entrance.png'))
    if exitimage is None:
        exitimage = gfw.image.load(gobj.res('exit.png'))
    
class Tile:
    EXCLUDE_FALL_NAMES = ['entrance', 'exit','ledder_bottom', 'rope_top', 'rope_mid', 'rope_last']
    EXCLUDE_WALL_NAMES = ['entrance', 'exit','ledder_bottom','ledder_top', 'spike', 'rope_top', 'rope_mid', 'rope_last']
    EXCLUDE_FLOOR_NAMES = ['entrance', 'exit','ledder_bottom','ledder_top', 'rope_top', 'rope_mid', 'rope_last']
    EXCLUDE_LEDDER_NAMES = ['entrance', 'exit','cave_block', 'arrow_block', 'spike']
    EXCLUDE_REMOVE = ['exit', 'entrance','cant_break']
    def __init__(self, name, left, bottom):
        self.left = left
        self.bottom = bottom
        self.draw_left = left
        self.draw_bottom = bottom

        self.unit = BLOCK_SIZE
        self.name = name

        self.excludes_block = name in Tile.EXCLUDE_FALL_NAMES
        self.excludes_wall = name in Tile.EXCLUDE_WALL_NAMES
        self.excludes_floor = name in Tile.EXCLUDE_FLOOR_NAMES
        self.excludes_ledder = name in Tile.EXCLUDE_LEDDER_NAMES
        self.excludes_remove = name in Tile.EXCLUDE_REMOVE
        self.rect = tile_rects[name]
    def update(self): pass
    def draw(self):
        tilesetimage.clip_draw_to_origin(*self.rect, self.draw_left, self.draw_bottom, self.unit, self.unit)

    def get_bb(self):
        return self.draw_left, self.draw_bottom,self.draw_left + self.unit, self.draw_bottom + self.unit

    def set_draw_pos(self, LEFT_GAB, BOTTOM_GAB):
        self.draw_left = self.left - LEFT_GAB
        self.draw_bottom = self.bottom - BOTTOM_GAB

    def remove(self):
        gfw.world.remove(self)

    def right(self):
        return self.left + self.unit

    def active(self): 
        pass

class Entrance(Tile):
    def draw(self):
        entranceimage.clip_draw_to_origin(*self.rect,self.draw_left, self.draw_bottom, self.unit, self.unit)

class Exit(Tile):
    def draw(self):
        exitimage.clip_draw_to_origin(*self.rect, self.draw_left, self.draw_bottom, self.unit, self.unit)

class Spike(Tile):
    def get_bb(self):
        return self.draw_left, self.draw_bottom, self.draw_left + self.unit, self.draw_bottom + self.unit//2 

class Arrow_trap(Tile):
    def __init__(self, name, left, bottom, look):
        self.left = left
        self.bottom = bottom
        self.draw_left = left
        self.draw_bottom = bottom

        self.unit = BLOCK_SIZE
        self.name = name
        self.rect = tile_rects[name]

        self.shoot = False
        self.look_left = look

        self.arrow_shoot_sound = load_wav('res/wav/arrowshot.wav')
        self.arrow_shoot_sound.set_volume(20)

        self.excludes_block = False
        self.excludes_wall = False
        self.excludes_floor = False
        self.excludes_ledder = False
        self.excludes_remove = False

    def draw(self):
        if self.look_left is False:
            tilesetimage.clip_draw_to_origin(*self.rect, self.draw_left, self.draw_bottom, self.unit, self.unit)
        else:
            tilesetimage.clip_composite_draw(*self.rect,0,'h', self.draw_left + self.unit // 2, self.draw_bottom + self.unit // 2, self.unit, self.unit)

    def active(self):
        if self.shoot is True: return

        if self.look_left == True:
            x = self.left + self.unit // 2 - 5
        else:
            x = self.left + self.unit // 2 + 5
        y = self.bottom + self.unit // 2 
        pos = x, y
        self.shoot = True
        arrow = objects.Arrow(pos, self.look_left)
        if self.look_left == True:
            arrow.change_dx(-5)
        else:
            arrow.change_dx(5)
        arrow.time = 2
        self.arrow_shoot_sound.play()
        gfw.world.add(gfw.layer.object, arrow)

    def get_active_bb(self):
        if self.look_left == True:
            return self.draw_left - self.unit * 5, self.draw_bottom + 20,self.draw_left,self.draw_bottom + self.unit - 20
        else:
            return self.draw_left + self.unit, self.draw_bottom + 20,self.draw_left + self.unit * 5,self.draw_bottom + self.unit - 20

class Rope_top(Tile):
    def draw(self):
        objectimage.clip_draw_to_origin(*self.rect, self.draw_left, self.draw_bottom, self.unit, self.unit)

class Rope_mid(Rope_top):
    pass
class Rope_last(Rope_top):
    pass

class Rope_maker(Tile):
    def __init__(self, name, left, bottom):
        self.left = left
        self.bottom = bottom
        self.draw_left = left
        self.draw_bottom = bottom

        self.unit = BLOCK_SIZE
        self.name = name
        self.rect = tile_rects[name]
    def update(self): pass