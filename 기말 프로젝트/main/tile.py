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
        self.unit = 80
        self.rect = tile_rects[name]
    def update(self): pass
    def draw(self):
        tilesetimage.clip_draw_to_origin(*self.rect, self.left, self.bottom, self.unit, self.unit)
    def get_bb(self):
        return self.left, self.bottom, self.left + self.unit, self.bottom + self.unit
    def move(self, dx):
        self.left += dx
        if self.left + self.unit < 0:
            # print('count was:', gfw.world.count_at(gfw.layer.platform))
            gfw.world.remove(self)
    @property
    def right(self):
        return self.left + self.unit
