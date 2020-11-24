import random
from pico2d import *
import gfw
import gobj

class Whip:
    whip_ani = [ [240,544],[320,544],[400,544],\
    [480,544],[560,544],[640,544],[720,544],\
    [800,544],[880,544],[960,544],[1040,544]]

    def __init__(self, pos, direction):
        self.pos = pos
        self.image = gfw.image.load(gobj.res('object.png'))
        self.FPS = 18
        self.time = 0
        self.fidx = 0
        self.size = 80
        self.look_left = direction

    def update(self):
        self.time += gfw.delta_time
        frame = self.time * self.FPS
        self.fidx = int(frame) % len(Whip.whip_ani)

        if self.fidx >= len(Whip.whip_ani) - 1:
            self.remove()

    def draw(self):
        sprite = Whip.whip_ani[self.fidx]

        sx = sprite[0]
        sy = sprite[1]

        self.set_pos()

        if self.look_left is False:
            self.image.clip_draw(sx, sy, self.size, self.size, *self.pos, self.size,self.size)
        else:
            self.image.clip_composite_draw(sx, sy, self.size, self.size, 0 , 'h', *self.pos, self.size,self.size)

    def set_pos(self):
        x, y = self.pos
        if self.look_left == True:
            if self.fidx > 4:
                self.pos = x - 30, y - 5  
            else:
                self.pos = x, y + 10
        else:
            if self.fidx > 4:
                self.pos = x + 30, y - 5  
            else:
                self.pos = x, y + 10
        
    def remove(self):
        gfw.world.remove(self)

    def get_bb(self):
        x,y = self.pos
        if self.look_left == False:
            if self.fidx == 0:
                return x - 50, y - 30, x + 10, y + 20
            elif self.fidx == 1:
                return x - 50, y - 30 , x + 10, y + 30
            elif self.fidx == 2:
                return x - 50, y + 10, x + 10, y + 30
            elif self.fidx == 3:
                return x - 50, y + 10, x + 10, y + 40
            elif self.fidx == 4:
                return x - 20, y + 5 , x + 20, y + 35
            elif self.fidx == 5:
                return x - 20, y , x + 30, y + 45
            elif self.fidx == 6:
                return x - 20, y , x + 30, y + 45
            elif self.fidx >= 7:
                return x - 30, y - 20, x + 40, y
        else:
            if self.fidx == 0:
                return x + 50, y - 30, x - 10, y + 20
            elif self.fidx == 1:
                return x + 50, y - 30, x - 10, y + 30
            elif self.fidx == 2:
                return x + 50, y + 10, x - 10, y + 40
            elif self.fidx == 3:
                return x + 50, y + 10, x - 10, y + 35
            elif self.fidx == 4:
                return x + 20, y + 5 , x - 20, y + 45
            elif self.fidx == 5:
                return x + 20, y, x - 30, y + 45
            elif self.fidx == 6:
                return x + 20, y, x - 30, y + 45
            elif self.fidx >= 7:
                return x - 40, y - 20, x + 30, y



