from pico2d import *
import gfw
import gobj

tilesetimage = None
tile_rects = {}

def load():
    global tilesetimage
    if tilesetimage is None:
        tilesetimage = gfw.image.load(gobj.res('tileset.png'))
        with open(gobj.res('all_tile.json')) as f:
            data = json.load(f)
            for name in data:
                tile_rects[name] = tuple(data[name])
                
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
