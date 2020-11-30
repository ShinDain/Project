from pico2d import *
import gfw
import gobj
import objects

tilesetimage = None

entranceimage = None
exitimage = None

tile_rects = {}

BLOCK_SIZE = 64

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
        self.unit = BLOCK_SIZE
        self.name = name
        self.rect = tile_rects[name]
    def update(self): pass
    def draw(self):
        left = self.left - self.left_gab
        bottom = self.bottom - self.bottom_gab
        if left < -64 or left > get_canvas_width() + 64: return
        if bottom < -64 or bottom > get_canvas_height() + 64: return
        
        if self.name is 'entrance':
            entranceimage.clip_draw_to_origin(*self.rect,left, bottom, self.unit, self.unit)
        elif self.name is 'exit':
            exitimage.clip_draw_to_origin(*self.rect, left, bottom, self.unit, self.unit)
        else:
            tilesetimage.clip_draw_to_origin(*self.rect, left, bottom, self.unit, self.unit)
    def get_bb(self):
        if self.name == 'spike':
            return self.left - self.left_gab, self.bottom - self.bottom_gab, self.left + self.unit - self.left_gab, self.bottom + self.unit//2 - self.bottom_gab

        return self.left - self.left_gab, self.bottom - self.bottom_gab, self.left + self.unit - self.left_gab, self.bottom + self.unit - self.bottom_gab
    def move(self, dx, dy):
        self.left += dx

    def remove(self):
        gfw.world.remove(self)

    def right(self):
        return self.left + self.unit

    def active(self): 
        pass

class arrow_trap(tile):
    def __init__(self, name, left, bottom, look):
        load()
        self.left = left
        self.bottom = bottom
        self.left_gab = 0
        self.bottom_gab = 0
        self.unit = BLOCK_SIZE
        self.name = name
        self.rect = tile_rects[name]

        self.shoot = False
        self.look_left = look

        self.arrow_shoot_sound = load_wav('res/wav/arrowshot.wav')

    def draw(self):
        left = self.left - self.left_gab
        bottom = self.bottom - self.bottom_gab
        if left < -64 or left > get_canvas_width() + 64: return
        if bottom < -64 or bottom > get_canvas_height() + 64: return
        
        if self.look_left is False:
            tilesetimage.clip_draw_to_origin(*self.rect, self.left - self.left_gab, self.bottom - self.bottom_gab, self.unit, self.unit)
        else:
            tilesetimage.clip_composite_draw(*self.rect,0,'h', self.left - self.left_gab + self.unit // 2, self.bottom - self.bottom_gab + self.unit // 2, self.unit, self.unit)

    def active(self):
        if self.shoot is True: return

        if self.look_left == True:
            x = self.left + self.unit // 2 - 5
        else:
            x = self.left + self.unit // 2 + 5
        y = self.bottom + self.unit // 2 
        pos = x, y
        self.shoot = True
        arrow = objects.Arrow(pos, 'arrow', self.look_left)
        if self.look_left == True:
            arrow.change_dx(-5)
        else:
            arrow.change_dx(5)
        self.arrow_shoot_sound.play()
        gfw.world.add(gfw.layer.object, arrow)

    def get_active_bb(self):
        if self.look_left == True:
            return self.left - self.left_gab - self.unit * 5, self.bottom - self.bottom_gab + 20,\
            self.left - self.left_gab,self.bottom + self.unit - self.bottom_gab - 20
        else:
            return self.left + self.unit - self.left_gab, self.bottom - self.bottom_gab + 20,\
            self.left + self.unit * 5 - self.left_gab,self.bottom + self.unit - self.bottom_gab - 20
