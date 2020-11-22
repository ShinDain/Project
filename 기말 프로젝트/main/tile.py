from pico2d import *
import gfw
import gobj

tilesetimage = None

entranceimage = None
exitimage = None

tile_rects = {}

def load():
    global tilesetimage, entranceimage, exitimage
    if tilesetimage is None:
        tilesetimage = gfw.image.load(gobj.res('tileset.png'))
        with open(gobj.res('all_tile.json')) as f:
            data = json.load(f)
            for name in data:
                tile_rects[name] = tuple(data[name])
    if entranceimage is None:
        entranceimage = gfw.image.load(gobj.res('entrance.png'))
    if exitimage is None:
        exitimage = gfw.image.load(gobj.res('exit.png'))
    
class tile:
    def __init__(self, name, left, bottom):
        load()
        self.left = left
        self.bottom = bottom
        self.left_gab = 0
        self.bottom_gab = 0
        self.unit = 64
        self.name = name
        self.rect = tile_rects[name]
    def update(self): pass
    def draw(self):
        if self.name is 'entrance':
            entranceimage.clip_draw_to_origin(*self.rect,self.left - self.left_gab, self.bottom - self.bottom_gab, self.unit, self.unit)
        elif self.name is 'exit':
            exitimage.clip_draw_to_origin(*self.rect, self.left - self.left_gab, self.bottom - self.bottom_gab, self.unit, self.unit)
        else:
            tilesetimage.clip_draw_to_origin(*self.rect, self.left - self.left_gab, self.bottom - self.bottom_gab, self.unit, self.unit)
    def get_bb(self):
        return self.left - self.left_gab, self.bottom - self.bottom_gab, self.left + self.unit - self.left_gab, self.bottom + self.unit - self.bottom_gab
    def move(self, dx, dy):
        self.left += dx
    @property
    def remove(self):
        gfw.world.remove(self)
    def right(self):
        return self.left + self.unit
